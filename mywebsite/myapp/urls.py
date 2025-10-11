from django.urls import path

# from .views import home,home2,aboutUs
from .views import *
# from django.contrib.auth import views
from . import views

urlpatterns = [
  path('', home, name="home-page"),
  path('home', home2),
  path('about/', aboutUs, name="aboutUs-page"),
  path('contact/', contact, name="contact-page"),
  path('login/', views.login_user, name='login'),
  path('logout/', views.logout_user, name='logout'),
  path('showcontact/', showContact, name='showcontact-page'),
  path('register/', userRegist, name="register-page"),
  path('profile/', userProfile, name="profile-page"),
  path('editprofile/', editProfile, name="editprofile-page"),
  path('action/<int:cid>/', actionPage, name="action-page"),
  path('addproduct/', addProduct, name="addproduct-page"),
  

]
