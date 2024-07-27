from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Profile)


#mix profile info and user info

class ProfileInline(admin.StackedInline):
    model = Profile
    
# extend the user model

class  UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]
    
# unregister the old user model

admin.site.unregister(User)

# now re register it
admin.site.register(User, UserAdmin)