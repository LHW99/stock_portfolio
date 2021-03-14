from portfolio.models import Stock, Portfolio
from portfolio.forms import StockForm, PortfolioForm, StockSellForm
from django.shortcuts import render, redirect
from stock_portfolio.settings.private_settings import CLOUD_API_KEY
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
import requests
import numpy as np

def api_call(request):
  if request.method == 'GET':
    try:
    # to get the ticker information
      ticker = request.GET['ticker_search']
      symbol = ticker.upper()
      response = requests.get(f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote&token={CLOUD_API_KEY}')
      data = response.json()
      
      return render(request, 'search.html',{
        'companyName': data[symbol]['quote']['companyName'],
        'iexRealtimePrice': data[symbol]['quote']['iexClose'],
        'symbol': symbol,
      })

    except:
      return render(request, 'search.html',{
        'iexRealtimePrice': 'Could not find ticker. Try again.'
      })
  
  else: 
    return HttpResponse('search')

  return render(request, 'search.html')

def buy_stocks(request, symbol):
  if request.method == 'GET':
    # to get the ticker information
    response = requests.get(f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote&token={CLOUD_API_KEY}')
    data = response.json()
    company = data[symbol]['quote']['companyName']
    price = data[symbol]['quote']['iexClose']
    investor = request.user
    # instantiate form prefilled
    form = StockForm(initial={
      'ticker': symbol, 
      'company': company, 
      'price': price,
      'portfolio': investor.portfolio,
      'stock_cost': 0,
      })
    return render(request, 'buy_stocks.html',{
      'form': form,
      'symbol': symbol,
      'price': price
    })

  if request.method == 'POST':
    form = StockForm(request.POST)
    investor = request.user
    if form.is_valid(): 
      # data for the form
      purchase = form.save(commit=False)
      pshares = request.POST.get('shares')
      pprice = request.POST.get('price')
      pcost = float(pshares)*float(pprice)

      # if not enough funds
      if pcost>investor.portfolio.portfolio_available_funds:
        return redirect('buy_error')

      else:
        #data for existing shares if they exist
        try:
          existing = Stock.objects.get(ticker=symbol, portfolio=investor.portfolio.id)
          existing_stock = StockForm(instance=existing).save(commit=False)
          new_shares = float(existing.shares) + float(pshares)
          existing_cost = float(existing.shares)*float(existing.price)
          new_cost = pcost + existing_cost
          new_average = new_cost/new_shares
          existing_stock.shares = new_shares
          existing_stock.price = new_average
          existing_stock.stock_cost = new_cost
          existing_stock.save()

        #if new ticker in portfolio
        except:
          purchase = form.save(commit=False)
          purchase.stock_cost = pcost
          purchase.save()

        # update portfolio funds
        my_portfolio = PortfolioForm(instance=investor.portfolio).save(commit=False)
        new_funds = float(investor.portfolio.portfolio_available_funds) - pcost
        my_portfolio.portfolio_available_funds = new_funds
        my_portfolio.save()

        return redirect('portfolio_detail')

    else:
      return redirect('portfolio_detail')

  return render(request, 'buy_stocks.html')

def sell_stocks(request, symbol):
  if request.method == 'GET':
    # to get the ticker information
    response = requests.get(f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote&token={CLOUD_API_KEY}')
    data = response.json()
    company = data[symbol]['quote']['companyName']
    price = data[symbol]['quote']['iexClose']
    investor = request.user
    try:
      current_shares = Stock.objects.get(ticker=symbol, portfolio=investor.portfolio.id)
      curr = current_shares.shares
    except:
      curr = 0
    #selling form
    form = StockSellForm(initial={
      'ticker': symbol, 
      'company': company, 
      'price': price,
      'portfolio': investor.portfolio,
      'stock_cost': 0,
      })

    return render(request, 'sell_stocks.html',{
      'company': company,
      'price': price,
      'symbol': symbol,
      'current_shares': curr,
      'form': form,
    })

  else: 
    form = StockSellForm(request.POST)
    investor = request.user
    if form.is_valid(): 
      # data for the form
      sold = form.save(commit=False)
      sshares = request.POST.get('shares')
      sprice = request.POST.get('price')
      scost = float(sshares)*float(sprice)

      # if trying to sell negative shares or more shares than held
      if float(sshares)<0:
        return redirect('sell_error')

      else:
        #data for existing shares
        existing = Stock.objects.get(ticker=symbol, portfolio=investor.portfolio.id)
        existing_stock = StockSellForm(instance=existing).save(commit=False)
        new_shares = float(existing.shares) - float(sshares)
        if new_shares < 0:
          return redirect('sell_error')

        else:
          existing_cost = existing.stock_cost
          new_cost = existing_cost - scost
          existing_stock.shares = new_shares
          existing_stock.stock_cost = new_cost
          existing_stock.save()

          # update portfolio funds
          my_portfolio = PortfolioForm(instance=investor.portfolio).save(commit=False)
          new_funds = float(investor.portfolio.portfolio_available_funds) + scost
          my_portfolio.portfolio_available_funds = new_funds
          my_portfolio.save()

          if new_shares==0:
            existing.delete()
            return redirect('portfolio_detail')
          
          else:
            return redirect('portfolio_detail')

        return redirect('portfolio_detail')

    else:
      return redirect('portfolio_detail')

    return redirect('portfolio_detail')

  return render(request, 'sell_stocks.html')

def index(request):
  return render(request, 'index.html')

def portfolio(request):
  if request.method == 'POST':
    form = PortfolioForm(request.POST)
    if form.is_valid(): 
      create = form.save()
      create.save()
      return redirect('portfolio_detail')
      print('yes')
    else:
      return redirect('portfolio_detail')
      print('no')

  else:
    # for the create new portfolio button
    user = request.user
    form = PortfolioForm(initial={
      'investor': user,
      'portfolio_available_funds': 1000000,})
    
    # for the current value
    batch_symbols = []
    batch_shares = []
    current_share_prices = []
    if user.portfolio.stock_set.all():
      for stock in user.portfolio.stock_set.all():
        batch_symbols.append(stock.ticker)
        batch_shares.append(float(stock.shares))
      response = requests.get(f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={batch_symbols}&types=quote&token={CLOUD_API_KEY}')
      data = response.json()
      for tick in data:
        current_share_prices.append(float(data[tick]['quote']['iexClose']))
      current_values = np.multiply(current_share_prices,batch_shares)
      portfolio_value = sum(current_values) + user.portfolio.portfolio_available_funds
    
      return render(request, 'portfolio_detail.html', {
        'form': form, 
        'current_values': current_values,
        'portfolio_value': portfolio_value,
        })

    else:
      portfolio_value=user.portfolio.portfolio_available_funds

      return render(request, 'portfolio_detail.html', {
        'form': form, 
        'portfolio_value': portfolio_value
        })

  return render(request, 'portfolio_detail.html')

def buy_error(request):
  return render(request, 'buy_error.html')

def sell_error(request):
  return render(request, 'sell_error.html')

def leaderboard(request):
  if request.method=='GET':
    user = get_user_model()
    users = user.objects.all()
    users_list = []
    for u in users:
      try:
        stock_list = []
        user_stock_list = u.portfolio.stock_set.all()
        user_value = 0
        if user_stock_list:
          for stock in user_stock_list:
            stock_list.append(stock.ticker)
      
          response = requests.get(f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={stock_list}&types=quote&token={CLOUD_API_KEY}')
          data = response.json()
          
          for stock in user_stock_list:
            value = float(stock.shares)*float(data[stock.ticker]['quote']['iexClose'])
            user_value+=float(value)   

          user_value+=u.portfolio.portfolio_available_funds
          users_list.append({'investor': u.portfolio.investor, 'value': user_value})
        else:
          users_list.append({'investor': u.portfolio.investor, 'value': u.portfolio.portfolio_available_funds})
      except:
        users_list.append({'investor': u, 'value': 0})

    def myFun(e):
      return e['value']
    users_list.sort(key=myFun, reverse=True)

    page_number = request.GET.get('page', 1)
    paginator = Paginator(users_list, 5)
    page_obj = paginator.get_page(page_number)

    return render(request, 'leaderboard.html', {'users_list': users_list, 'page_obj': page_obj})

  return render(request, 'leaderboard.html', {'page_obj': page_obj})