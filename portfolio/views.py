from portfolio.models import Stock, Portfolio
from portfolio.forms import StockForm, PortfolioForm
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from rest_framework.views import APIView
from stock_portfolio.settings.private_settings import CLOUD_API_KEY
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
    try:
      # to get the ticker information
      response = requests.get(f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote,stats,advanced-stats&token={CLOUD_API_KEY}')
      data = response.json()
      company = data[symbol]['quote']['companyName']
      price = data[symbol]['quote']['iexClose']
      # instantiate form prefilled
      form = StockForm(initial={
        'ticker': symbol, 
        'company': company, 
        'price': price,
        #'user': request.user
        })
      
      return render(request, 'buy_stocks.html',{
        'form': form,
        'symbol': symbol,
        'price': price
      })

    except:
      return render(request, 'buy_stocks.html')

  if request.method == 'POST':
    form = StockForm(request.POST)
    if form.is_valid(): 
      purchase = form.save(commit=False)
      purchase.portfolio = 'nut'
      purchase.save()
      return redirect('index')
    else:
      return redirect('index')

  return render(request, 'buy_stocks.html')

def sell_stocks(request, symbol):
  if request.method == 'GET':
    try:
    # to get the ticker information
      response = requests.get(f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote,stats,advanced-stats&token={CLOUD_API_KEY}')
      data = response.json()
      
      return render(request, 'sell_stocks.html',{
        'companyName': data[symbol]['quote']['companyName'],
        'iexRealtimePrice': data[symbol]['quote']['iexRealtimePrice'],
        'symbol': symbol,
      })

    except:
      return render(request, 'sell_stocks.html')

  else: 
    return HttpResponse('sell_stocks.html')

  return render(request, 'sell_stocks.html')

def index(request):

  return render(request, 'index.html')

def portfolio(request):

  if request.method == 'POST':
    form = PortfolioForm(request.POST)
    #if form.is_valid(): 
    #  purchase = form.save(commit=False)
    #  purchase.portfolio = 'nut'
    #  purchase.save()
    #  return redirect('index')
    #else:
    #  return redirect('index')
    print(request.user)

  else:
    form = PortfolioForm()
    return render(request, 'portfolio_detail.html', {'form': form})

  return render(request, 'portfolio_detail.html', {'form': form})

