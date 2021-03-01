from portfolio.models import Stock, Portfolio
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from stock_portfolio.settings.private_settings import CLOUD_API_KEY

class IndexView(TemplateView):
  template_name = 'index.html'

class SearchView(DetailView):
  model = Stock
  template_name = 'search.html'

  def get(self, request, **args, **kwargs):
    query = request.GET('ticker_search')
    symbol = query.upper()
f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote,stats,advanced-stats&token={CLOUD_API_KEY}'

  def get_context_data(self, *args, **kwargs):
    context = super(SearchView, self).get_context 

    if query: 


class PortfolioDetailView(DetailView):
  model = Portfolio
  template_name = "portfolio_detail.html"

