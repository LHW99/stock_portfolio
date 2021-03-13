from portfolio.models import Stock, Portfolio
from portfolio.forms import StockForm, PortfolioForm
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from rest_framework.views import APIView
from stock_portfolio.settings.private_settings import CLOUD_API_KEY
from django.contrib.auth.models import User
import requests

def api_call(request):
  if request.method == 'GET':
    try:
    # to get the ticker information
      ticker = request.GET['ticker_search']
      symbol = ticker.upper()
      response = requests.get(f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote,stats,advanced-stats&token={CLOUD_API_KEY}')
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
    response = requests.get(f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote,stats,advanced-stats&token={CLOUD_API_KEY}')
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
    response = requests.get(f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote,stats,advanced-stats&token={CLOUD_API_KEY}')
    data = response.json()
    company = data[symbol]['quote']['companyName']
    price = data[symbol]['quote']['iexRealtimePrice']
    investor = request.user
    try:
      current_shares = Stock.objects.get(ticker=symbol, portfolio=investor.portfolio.id)
      curr = current_shares.shares
    except:
      curr = 0

    return render(request, 'sell_stocks.html',{
      'company': company,
      'price': price,
      'symbol': symbol,
      'current_shares': curr,
    })

  else: 
    return HttpResponse('sell_stocks.html')

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
    user = request.user
    form = PortfolioForm(initial={
      'investor': user,
      'portfolio_available_funds': 1000000,})
    return render(request, 'portfolio_detail.html', {'form': form})

  return render(request, 'portfolio_detail.html')

def buy_error(request):
  return render(request, 'buy_error.html')