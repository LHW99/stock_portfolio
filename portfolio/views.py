from portfolio.models import Stock, Portfolio
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from stock_portfolio.settings.private_settings import CLOUD_API_KEY

class IndexView(TemplateView):
  template_name = 'index.html'

class SearchMixin:
  def get_ticker(self):
    return self.request.GET.get('ticker_search')



      query = request.GET['ticker_search']
      symbol = query.upper()
      response = request.get(f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol}&types=quote&token={CLOUD_API_KEY}')
      data = response.json()


class SearchView(SearchMixin, TemplateView):
  template_name = 'search.html'

  def get_content_data(self, **kwargs):
    context = super(SearchView, self).get_context_data(**kwargs)
    context['companyName'] = self.get_ticker(query_string)
    context['iexRealtimePrice'] = self.get_ticker(query_string)
    context['symbol'] = symbol
    return context

class PortfolioDetailView(DetailView):
  model = Portfolio
  template_name = "portfolio_detail.html"

