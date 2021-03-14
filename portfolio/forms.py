from django import forms 
from portfolio.models import *
from django.forms import ModelForm

class SearchForm(forms.Form):
  search = forms.CharField(label='Ticker Search', max_length=4)

class StockForm(ModelForm):
  class Meta:
    model = Stock
    fields = '__all__'
    labels = {
      'shares': 'Number of shares to buy'
    }
    widgets = {
      'ticker': forms.HiddenInput(),
      'company': forms.HiddenInput(),
      'price': forms.HiddenInput(),
      'portfolio': forms.HiddenInput(),
      'stock_cost': forms.HiddenInput(),
    }

class StockSellForm(ModelForm):
  class Meta:
    model = Stock
    fields = '__all__'
    labels = {
      'shares': 'Number of shares to sell'
    }
    widgets = {
      'ticker': forms.HiddenInput(),
      'company': forms.HiddenInput(),
      'price': forms.HiddenInput(),
      'portfolio': forms.HiddenInput(),
      'stock_cost': forms.HiddenInput(),
    }

class PortfolioForm(ModelForm):
  class Meta:
    model = Portfolio
    fields = '__all__'
    widgets = {
      'investor': forms.HiddenInput(),
      'portfolio_available_funds': forms.HiddenInput(),
    }
