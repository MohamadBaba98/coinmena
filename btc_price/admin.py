from django.contrib import admin
from .models import ApiKey, Price

@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
  list_display = [field.name for field in ApiKey._meta.get_fields()]

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
  list_display = [field.name for field in Price._meta.get_fields()]