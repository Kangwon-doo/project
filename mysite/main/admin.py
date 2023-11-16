from django.contrib import admin
<<<<<<< HEAD
 
=======
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(CustomUser,UserAdmin)
>>>>>>> 7c74a337878871921a1648c2342bcaa36a8eef0a
