from django.shortcuts import render, redirect
from django.contrib import messages
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired
import mysql.connector

# Configuración de la conexión MySQL
DB_CONFIG = {
    'host': 'localhost',
    'port': '3306',
    'user': 'root',
    'password': '',
    'database': 'Taller_Mecanico_dj'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def pagina_principal(request):
    return render(request, 'Taller_mecanico/pagina_principal.html')

def login_view(request):
    return render(request, 'Taller_mecanico/login.html')

def register(request):
    return render(request, 'Taller_mecanico/register.html')

# @login_required
def administracion(request):
    return render(request, 'Taller_mecanico/administracion.html')

# @login_required
def presupuesto(request):
    return render(request, 'Taller_mecanico/presupuesto.html', {})

def quienes_somos(request):
    return render(request, 'Taller_mecanico/quienes_somos.html')

def ubicacion_contacto(request):
    return render(request, 'Taller_mecanico/ubicacion_contacto.html')


#Panel de administracion

def clientes(request):
    return render(request, 'Taller_mecanico/adminis/clientes.html')