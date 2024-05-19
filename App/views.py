from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages

# Create your views here.

def login(request):
    if request.method == 'GET':
      return render(request, "login.html")
    elif request.method == 'POST':
        if request.POST['hidden'] == "login":
            correo = request.POST.get('email_login')
            password = request.POST.get('password_login')  
            try:
                user = get_user_model().objects.get(email=correo)
            except get_user_model().DoesNotExist:
                messages.error(request, 'El usuario no existe')
                return redirect('/auth')

            if user.check_password(password):
                url = "/welcome/" + user.get_username()
                return redirect(url)
            else:
                messages.error(request, 'La contraseña es incorrecta')
                return redirect('/auth')
        
        if request.POST['hidden'] == "register":
            username = request.POST['username_register']
            email = request.POST['email_register']
            password = request.POST['password_register']
            hashed_password = make_password(password)
            User = get_user_model()
            try:
                user = User(username=username, email=email, password=hashed_password)
                user.save()
                return redirect ('/auth')
            except:
                messages.error(request, 'El usuario ya existía')
                return redirect ('/auth')
        else:
            messages.error(request, 'Algo Salio Mal')
            return redirect ('/auth')

def welcome_view(request, name):
    return render(request, 'welcome.html', {'name': name})
   
def index(request):
    return render(request, 'index.html')