from django.urls import path
from portfolio.views import *

urlpatterns = [
  path('', IndexView.as_view(), name='index'),
  path('portfolio', PortfolioDetailView.as_view(), name='portfolio_detail' )
]