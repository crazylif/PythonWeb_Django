from django.urls import path

# from .views import home,home2,aboutUs
from .views import *
from django.contrib.auth import views

urlpatterns = [
  path('', home, name="home-page"),
  path('home2', home2),
  path('about/', aboutUs, name="aboutUs-page"),
  path('contact/', contact, name="contact-page"),
]
