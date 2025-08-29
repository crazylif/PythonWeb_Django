from django.urls import path

# from .views import home,home2,aboutUs
from .views import *

urlpatterns = [
  path('', home),
  path('home2', home2),
  path('about/', aboutUs, name="aboutUs-page")
]
