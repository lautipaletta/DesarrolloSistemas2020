from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist

from . models import User

# Create your views here.
def index(request):
    
    if request.method == "POST":

        username = User.objects.get(email=request.POST["email"]).username
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            return render(request, "covid19api/index.html")

        else:
            return render(request, "covid19api/login.html")

    else:

        try:
            user = User.objects.get(username=request.user)

            if user.is_authenticated:
                return render(request, "covid19api/index.html")
        
        except (ObjectDoesNotExist):
            pass

        return render(request, "covid19api/login.html")
