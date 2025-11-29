from django.shortcuts import render, redirect
from .db import get_connection

# Páginas principales
def pagina_principal(request):
    return render(request, 'Taller/pagina_principal.html')

def login_view(request):
    return render(request, 'Taller/login.html')

def register(request):
    return render(request, 'Taller/register.html')

def administracion(request):
    return render(request, 'Taller/administracion.html')

def presupuesto(request):
    return render(request, 'Taller/presupuesto.html', {})

def quienes_somos(request):
    return render(request, 'Taller/quienes_somos.html')

def ubicacion_contacto(request):
    return render(request, 'Taller/ubicacion_contacto.html')


# Panel de administración: CRUD de clientes
def clientes(request):
    if request.method == "POST":
        dni = request.POST.get("dni")
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        direccion = request.POST.get("direccion")
        telefono = request.POST.get("telefono")

        # Conexión a la base de datos
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (dni, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
            (dni, nombre, apellido, direccion, telefono)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('clientes')  # Redirige para evitar reenvío de formulario

    # Si no es POST, simplemente muestra la página
    return render(request, 'Taller/adminis/clientes.html')
