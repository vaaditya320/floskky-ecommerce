from django.urls import path, include
from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("register/", register_user, name="register"),
    path("product/<int:pk>", product, name="product"),
    path("category/<str:category_name>", product_category, name="category"),
    path("category_summary/", category_summary, name="category_summary")
    
]