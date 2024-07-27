from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm

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
        messages.success(request, "category does not exist......")
        # return redirect("home")
        pass
    
def category_summary(request):
    categories = Category.objects.all()

    return render(request, "category_summary.html", {"categories" : categories})


def update_user(request):
    
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "updated successfully")
            return redirect("home")
        else:
            return render(request, "update_user.html", {"user_form" : user_form})
            
    else:
        messages.success(request, "You need to login first")
        return redirect("login")
    
    
def update_password(request):
    if  request.user.is_authenticated:
        current_user = request.user
        
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # is the form valid
            if form.is_valid():
                form.save()
                # login(request, current_user)
                messages.success(request, "log in again")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)                
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {"form" : form})
            
    else:
        messages.success(request, "You need to login first")
        return redirect("login") 
       