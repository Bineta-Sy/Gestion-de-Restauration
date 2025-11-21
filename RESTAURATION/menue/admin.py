from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Plat, Categorie

admin.site.register(Plat)
admin.site.register(Categorie)
