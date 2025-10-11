import requests
import json

from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from dotenv import load_dotenv
import os

load_dotenv() # take environment variables from .env.


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

########## register 
def userRegist(request):
  context={}
  if request.method == 'POST':
    data = request.POST.copy()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    repassword = data.get('repassword')

    try:
      User.objects.get(username=username)
      context['message'] = "Username duplicate"
    except:
      newuser = User()
      newuser.username = username
      newuser.first_name = firstname
      newuser.last_name = lastname
      newuser.email = email

      if (password == repassword):
        newuser.set_password(password)
        newuser.save()
        newprofile = Profile()
        newprofile.user = User.objects.get(username=username)
        newprofile.save()
        context['message'] = "register complate."
      else:
        context['message'] = "password or re-password is incorrect."
  return render(request, 'myapp/register.html', context)

##############

########### login and logout
def login_user(request):
  context = {}

  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, "You have been logged in.")
      context['message'] = "You have been logged in."
      return redirect('home-page')
    else:
      messages.success(request, "There was an error, please try again..!")
      context['message'] = "username or password is incorrect."
      return redirect('login')

  else:
    return render(request, 'myapp/login.html', {})

def logout_user(request):
  logout(request)
  messages.success(request, ("You have been logged out...!"))
  return redirect('home-page')

###############

######## edit profile
def editProfile(request):
  context = {}
  if request.method == 'POST':
    data = request.POST.copy()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    current_user = User.objects.get(id=request.user.id)
    current_user.first_name = firstname
    current_user.last_name = lastname
    current_user.username = username
    current_user.email = email
    current_user.set_password(password)
    current_user.save()

    try:
      user = authenticate(username=current_user.username,
                          password=current_user.password)
      login(request, user)
      return redirect('home-page')
    except:
      context['message'] = "myapp/editprofile.html"
  return render(request, 'myapp/editprofile.html')

###########

######### user profile
def userProfile(request):
  context = {}
  userprofile = Profile.objects.get(user=request.user)
  context['profile'] = userprofile
  return render(request, 'myapp/profile.html', context)

#####


# def userLogin(request):
#   context = {}
#   print("dfdfdfdf")
  
#   if request.method == 'POST':
#     data = request.POST.copy()
#     username = data.get('username')
#     password = data.get('password')

#     print(username)
#     print(password)
#     print('---------------------------')

#     try:
#        user = authenticate(username=username, password=password)
#        login(request, user)
#     except:
#        context['message'] = "username or password is incorrect."

#   return render(request, 'myapp/login.html', context)

def contact(request):

  context = {} # message to notify

  if request.method == 'POST':
    data = request.POST.copy()
    topic = data.get('topic')
    email = data.get('email')
    detail = data.get('detail')

    if (topic == '' or email == '' or detail == ''):
      context['message'] = 'Please, fill in all contact information !'
      return render(request, 'myapp/contact.html', context)

    newRecord = contactList()  #create object
    newRecord.topic = topic
    newRecord.email = email
    newRecord.detail = detail
    newRecord.save() #save data

    context['message'] = 'The message has been received'

    print(topic)
    print(email)
    print(detail)
    print('---------------------------')

    #### fetch to line message api
    channel_access_token = os.getenv("channel_access_token")
    user_id = os.getenv("user_id")
    print("=====================")
    print(channel_access_token,"  ||||  ",user_id)
    send_line_message(user_id, "contact message:\ntopic:{0}\nemail:{1}\ndetail:{2}"\
                      .format(topic, email, detail), channel_access_token)

  return render(request, 'myapp/contact.html', context)

def showContact(request):
  allcontact = contactList.objects.all()
  context = {'contact': allcontact}
  return render(request, 'myapp/showcontact.html', context)

def send_line_message(user_id: str, message: str, channel_access_token: str):
  """
  Send a push message to a LINE user using Messaging API.

  Args:
      user_id (str): The LINE user ID (or group ID).
      message (str): The message text to send.
      channel_access_token (str): Channel Access Token from LINE Developers.
  """
  url = "https://api.line.me/v2/bot/message/push"
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {channel_access_token}"
  }
  payload = {
      "to": user_id,
      "messages": [
          {
              "type": "text",
              "text": message
          }
      ]
  }

  response = requests.post(url, headers=headers, data=json.dumps(payload))
  if response.status_code == 200:
      print("✅ Message sent successfully!")
  else:
      print(f"❌ Failed: {response.status_code}, {response.text}")

def actionPage(request, cid):
  # id = contactList
  context = {}
  contact = contactList.objects.get(id=cid)
  context['contact'] = contact
  return render(request, 'myapp/action.html', context)

def addProduct(request):
  if request.method == 'POST':
    data = request.POST.copy()
    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    quantity = data.get('quantity')
    instock = data.get('instock')

    print(title)
    print(description)
    print(price)
    print(quantity)
    print(instock)
    print('File: ', request.FILES)

  return render(request, 'myapp/addProduct.html')