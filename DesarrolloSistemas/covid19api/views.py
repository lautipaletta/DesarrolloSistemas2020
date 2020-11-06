from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

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

        user = User.objects.get(username=request.user)

        if user.is_authenticated:
            return render(request, "covid19api/index.html")
        else:
            return render(request, "covid19api/login.hmtl")