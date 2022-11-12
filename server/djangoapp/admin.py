from django.contrib import admin
from .models import CarMake, CarModel
from django.contrib.admin.options import StackedInline


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel 

# CarModelAdmin class
@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    pass

# CarMakeAdmin class with CarModelInline
@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
