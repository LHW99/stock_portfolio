from django import forms 

class SearchForm(forms.Form):
  search = forms.CharField(label='Ticker Search', max_length=4)