import requests
import json

from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate, login

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

def userLogin(request):
  context = {}
  print("dfdfdfdf")
  
  if request.method == 'POST':
    data = request.POST.copy()
    username = data.get('username')
    password = data.get('password')

    print(username)
    print(password)
    print('---------------------------')

    try:
       user = authenticate(username=username, password=password)
       login(request, user)
    except:
       context['message'] = "username or password is incorrect."

  return render(request, 'myapp/login.html', context)

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

    # Example usage:
    channel_access_token = "w/Z5V72x/AtK7/Ix8dSjhayhuRyQ6svtbj2qCHRreIwBssebUjTpShVltYWMj/BL4A/VH2FX7XfjN46FcC91r5BHd+9WsaEfhK/PC+tSjW4AGXi0nW3fJH8duygnOcWJiXFMV60WPzTbb5/R0kIPFgdB04t89/1O/w1cDnyilFU="
    user_id = "U9d31c54e1b22ec3cf731814c95d75bf1"
    send_line_message(user_id, "contact message:\ntopic:{0}\nemail:{1}\ndetail:{2}"\
                      .format(topic, email, detail), channel_access_token)

  return render(request, 'myapp/contact.html', context)

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
