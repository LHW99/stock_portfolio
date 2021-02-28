from portfolio.models import Stock, Portfolio
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import DetailView

class IndexView(TemplateView):
  template_name = 'index.html'

class PortfolioDetailView(DetailView):
  model = Portfolio
  template_name = "portfolio_detail.html"

