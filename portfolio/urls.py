from django.urls import path
from portfolio.views import *
from . import views

urlpatterns = [
  path('', IndexView.as_view(), name='index'),
  path('portfolio', PortfolioDetailView.as_view(), name='portfolio_detail'),
  path('search', views.api_call, name='search'),
  path('buy/<str:symbol>', views.buy_stocks, name='buy'),
  path('sell/<str:symbol>', views.sell_stocks, name='sell'),
]