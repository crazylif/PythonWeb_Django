from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def home(request):
  return HttpResponse('<h1>Hello World</h1>')

def home2(request):
  return HttpResponse('<h1 style="color:red; font-size: 300%;">Hello World2</h1>')

def home(request):
  allproduct = Product.objects.all()
  context = {'pd': allproduct}
  return render(request, 'myapp/home.html', context)

def aboutUs(request):
  return render(request, 'myapp/aboutus.html')