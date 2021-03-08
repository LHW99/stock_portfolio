from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

class Stock(models.Model):
  ticker = models.CharField(max_length=5)
  #portfolio = models.ForeignKey('Portfolio', on_delete=models.SET_NULL, null=True)
  company = models.CharField(max_length=100)
  price = models.FloatField()
  shares = models.IntegerField()
  #stock_value = price*shares

  def __str__(self):
    return self.ticker

class Portfolio(models.Model):
  investor = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, unique=False)
  portfolio_value = models.IntegerField()
  portfolio_available_funds = models.IntegerField()

  def get_absolute_url(self):
    return reverse("portfolio-detail", kwargs={"pk": self.pk})
  
  def __str__(self):
    return f"{self.User}'s Portfolio"