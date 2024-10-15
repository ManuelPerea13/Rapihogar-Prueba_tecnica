from django.contrib import admin
from .models import User, Scheme, Company, Pedido


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'scheme', 'hours_worked')
