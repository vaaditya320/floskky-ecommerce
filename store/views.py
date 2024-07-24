from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {"products" : products})

def about(request):
    return render(request, "about.html")


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or any other page after successful login
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect("login")
    
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    messages.success(request, "you have been logged out")
    return redirect("home")

def register_user(request):
    form  = SignUpForm()
    
    if request.method == 'POST':
        form  = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            
            login(request, user)
            messages.success(request, "you have been logged out")
            # Redirect to a success page or any other page after successful login
            return redirect('home')
            
    
    return render(request, "register.html", {"form" : form})


def product(request, pk):
    
    product = Product.objects.get(id=pk)
    
    return render(request, "product.html", {"product" : product})

def product_category(request, category_name):
    try:
        # print(category_name)
        
       # replacing space with - (like  a slug)
        
        category = Category.objects.get(name=category_name)
        
        products = Product.objects.filter(category=category)
        context = {"products" : products}
        return render(request, "category.html", context)
        
    except ValueError:
        # messages.success(request, "category does not exist......")
        # return redirect("home")
        pass
    
def category_summary(request):
    categories = Category.objects.all()

    return render(request, "category_summary.html", {"categories" : categories})