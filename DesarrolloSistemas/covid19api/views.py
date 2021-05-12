from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import PasswordChangeForm # Formulario para cambiar la contraseña
from django.contrib.auth import update_session_auth_hash # Funcion para que no cierre sesion al cambiarla

from urllib.request import urlopen # API
import json # API

from . models import User
from . forms import UserForm

# Custom Exception

class contrasegnaIncorrecta(Exception):
    pass

# Create your views here.
def index(request):
    
    if request.method == "POST":

        errormsg = None

        try: 
            username = User.objects.get(email=request.POST["email"]).username
            password = request.POST["password"]

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('index')
            else:
                raise contrasegnaIncorrecta
        
        except (ObjectDoesNotExist):
            errormsg = 'el mail no corresponde a ningun usuario registrado.'
        except contrasegnaIncorrecta:
            errormsg = 'la contraseña es incorrecta.'
        
        return render(request, "covid19api/login.html", {'errormsg':errormsg})

    else:
        if request.user.is_authenticated:

            url = "https://api.covid19api.com/summary"
            response = urlopen(url)
            data = json.loads(response.read())
            context = {}

            for dictionary in data['Countries']:
                if dictionary['Country'] == request.user.country.capitalize():
                    context = {
                    'country_code': dictionary['CountryCode'],
                    'slug': dictionary['Slug'],
                    'new_confirmed': dictionary['NewConfirmed'],
                    'total_confirmed': dictionary['TotalConfirmed'],
                    'new_deaths': dictionary['NewDeaths'],
                    'total_deaths': dictionary['TotalDeaths'],
                    'new_recovered': dictionary['NewRecovered'],
                    'total_recovered': dictionary['TotalRecovered'],
                    'total_active': (dictionary['TotalConfirmed'] - dictionary['TotalRecovered']),
                    'date': dictionary['Date'][0:10],
                    'time': dictionary['Date'][11:19]
                    }

            return render(request, "covid19api/index.html", context)
        else:
            return render(request, "covid19api/login.html")

def logout_view(request):
    """
    Logout the current user.
    """
    logout(request)
    return redirect('index')


def profile(request):
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance = request.user)
        if form.is_valid:
            form.save()
        return redirect('index')
    else:
        form = UserForm(instance = request.user)

    context = {'form':form}

    return render(request, 'covid19api/profile.html', context)

def change_password(request):

    if request.method == 'POST':
        
        form = PasswordChangeForm(data = request.POST, user = request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # Mantiene la sesión activa
            return redirect('index')
    else:
        form = PasswordChangeForm(user = request.user)

    context = {'form':form}

    return render(request, 'covid19api/change_password.html', context)


# def profile(request, username):
    
#     if request.method == "POST":

#         for field in request.POST:

#             if request.POST[field] != "":
#                 print(request.POST[field])

#     else:
#         return render(request, "covid19api/profile.html", {
#             "form" : UserForm()
#         })