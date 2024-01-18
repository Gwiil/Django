from django.contrib import admin
from .models import Filme, Episodio, Usuario
from django.contrib.auth.admin import UserAdmin
# CASO QUEIRA QUE AS INFORMAÇÔES PERSONALIZADAS APAREÇA NA AREA ADMIN
campos_usuarios = list(UserAdmin.fieldsets)
campos_usuarios.append(
    ("Historico",{'fields': ("filmes_vistos",)})
)
UserAdmin.fieldsets = tuple(campos_usuarios)

# Register your models here.
admin.site.register(Filme)
admin.site.register(Episodio)
admin.site.register(Usuario, UserAdmin)
