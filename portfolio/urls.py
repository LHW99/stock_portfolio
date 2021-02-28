from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('/portfolio', PortfolioDetailView.as_view(), name='portfolio_detail' )
]