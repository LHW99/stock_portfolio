from portfolio.models import Stock, Portfolio
from portfolio.forms import SearchForm
from django.shortcuts import render
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
        'iexRealtimePrice': data[symbol]['quote']['iexRealtimePrice'],
        'symbol': symbol,
      })

    except:
      return render(request, 'search.html')
  
  else: 
    return HttpResponse('search')

  return render(request, 'search.html')

class IndexView(TemplateView):
  template_name = 'index.html'

class PortfolioDetailView(DetailView):
  model = Portfolio
  template_name = "portfolio_detail.html"

