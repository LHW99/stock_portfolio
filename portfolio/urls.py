from django.urls import path
from portfolio.views import *
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('portfolio', views.portfolio, name='portfolio_detail'),
  path('search', views.api_call, name='search'),
  path('buy/<str:symbol>', views.buy_stocks, name='buy'),
  path('sell/<str:symbol>', views.sell_stocks, name='sell'),
  path('buy_error', views.buy_error, name='buy_error'),
  path('sell_error', views.sell_error, name='sell_error'),
  path('leaderboard', views.leaderboard, name='leaderboard'),
  path('signup', views.signup, name='signup'),
]