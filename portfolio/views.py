from django.shortcuts import render

def index(request):

  return render(request, 'index.html')

class PortfolioDetailView(DetailView):
    model = Portfolio
    template_name = "portfolio_detail.html"

    