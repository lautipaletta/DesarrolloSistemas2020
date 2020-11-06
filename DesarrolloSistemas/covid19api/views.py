from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist

from . models import User
from . forms import UserForm

# Create your views here.
def index(request):
    
    if request.method == "POST":

        username = User.objects.get(email=request.POST["email"]).username
        password = request.POST["password"]

        try: 
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return render(request, "covid19api/index.html")
        
        except (ObjectDoesNotExist):
            pass
        
        return render(request, "covid19api/login.html")

    else:

        try:
            user = User.objects.get(username=request.user)

            if user.is_authenticated:
                return render(request, "covid19api/index.html")
        
        except (ObjectDoesNotExist):
            pass

        return render(request, "covid19api/login.html")

def logout_view(request):
    """
    Logout the current user.
    """
    logout(request)
    return render(request, "covid19api/login.html")

def profile(request, username):
    
    if request.method == "POST":

        for field in request.POST:

            if request.POST[field] != "":
                print(request.POST[field])

    else:
        return render(request, "covid19api/profile.html", {
            "form" : UserForm()
        })