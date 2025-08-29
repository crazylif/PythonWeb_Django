from django.shortcuts import render

from django.http import HttpResponse

def home(request):
  return HttpResponse('<h1>Hello World</h1>')

def home2(request):
  return HttpResponse('<h1 style="color:red; font-size: 300%;">Hello World2</h1>')

def home(request):
  return render(request, 'myapp/home.html')