from django.shortcuts import render
from auction.models import Auction 

def home(request):
 
    return render(request, 'auction/home.html')