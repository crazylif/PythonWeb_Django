import requests
import json

from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator

from django.core.files.storage import FileSystemStorage


from dotenv import load_dotenv
import os

load_dotenv() # take environment variables from .env.

def adminPage(request):
    return render(request, 'myapp/admin.html')

# def home(request):
#   return HttpResponse('<h1>Hello World</h1>')

def home2(request):
  return HttpResponse('<h1 style="color:red; font-size: 300%;">Hello World2</h1>')

def home(request):
  allproduct = Product.objects.all()
  product_per_page = 3
  paginator = Paginator(allproduct, product_per_page)
  page = request.GET.get('page')
  allproduct = paginator.get_page(page)

  context = {'allproduct': allproduct}

  #1 row 3 colums
  allrow = []
  row =[]
  for i,p in enumerate(allproduct):
    if i % 3 == 0:
      if i != 0:
        allrow.append(row)
      row = []
      row.append(p)
    else:
      row.append(p)

  allrow.append(row)
  context['allrow'] = allrow

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
  try:
    context = {}
    contact = contactList.objects.get(id=cid)
    context['contact'] = contact

    try:
      action = Action.objects.get(contactList=contact)
      context['action'] = action
    except:
      pass

    if request.method == 'POST':
      data = request.POST.copy()
      actiondetail = data.get('actiondetail')

      if 'save' in data:
        try:
          check = Action.objects.get(contactList=contact)
          check.actionDetail = actiondetail
          check.save()
          context['action'] = check
          return redirect('showcontact-page')
        except:
          new = Action()
          new.contactList = contact
          new.actionDetail = actiondetail
          new.save()
          return redirect('showcontact-page')
        
      elif 'delete' in data:
        try:
          contact.delete()
          return redirect('showcontact-page')
        except:
          pass
        
      elif 'complete' in data:
        contact.complete = True
        contact.save()
        return redirect('showcontact-page')

    return render(request, 'myapp/action.html', context)
  
  except contactList.DoesNotExist:
    return HttpResponse("<h1 style=\"padding: 30px;\">Contact not found</h1>", status=404)


def addProduct(request):
  if request.method == 'POST':
    data = request.POST.copy()
    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    quantity = data.get('quantity')
    instock = data.get('instock')

    new = Product()
    new.title = title
    new.description = description
    new.price = float(price)
    new.quantity = int(quantity)

    if instock == "instock":
      new.instock = True
    else:
      new.instock = False

    if 'picture' in request.FILES:
      file_image = request.FILES['picture']
      file_image_name = file_image.name.replace(' ', '')
      fs = FileSystemStorage(location='media/product')
      filename = fs.save(file_image_name, file_image)
      upload_file_url = fs.url(filename)
      print("Picture url:", upload_file_url)
      new.picture = 'product' + upload_file_url[6:]

    if 'specfile' in request.FILES:
      file_specfile = request.FILES['specfile']
      file_specfile_name = file_specfile.name.replace(' ', '')
      fs = FileSystemStorage(location='media/specfile')
      filename = fs.save(file_specfile_name, file_specfile)
      upload_file_url = fs.url(filename)
      print("Specfile url:", upload_file_url)
      new.specfile = 'product' + upload_file_url[6:]

    new.save()
    

    print(title)
    print(description)
    print(price)
    print(quantity)
    print(instock)
    print('File: ', request.FILES)

  return render(request, 'myapp/addProduct.html')

# def handler404(request, exception):
#   return render(request, 'myapp/404errorPage.html')


