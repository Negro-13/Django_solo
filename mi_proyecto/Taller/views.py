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

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Clientes (DNI, Nombre, Apellido, Direccion, Telefono) VALUES (%s, %s, %s, %s, %s)",
            (dni, nombre, apellido, direccion, telefono)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('clientes')

    # Leer los datos de la tabla Clientes
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # Devuelve diccionarios
    cursor.execute("SELECT * FROM Clientes")
    clientes_db = cursor.fetchall()
    cursor.close()
    conn.close()

    return render(request, 'Taller/adminis/clientes/clientes.html', {"clientes": clientes_db})

def editar_cliente(request, dni):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        direccion = request.POST.get("direccion")
        telefono = request.POST.get("telefono")
        
        cursor.execute(
            "UPDATE Clientes SET Nombre=%s, Apellido=%s, Direccion=%s, Telefono=%s WHERE DNI=%s",
            (nombre, apellido, direccion, telefono, dni)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('clientes')
    
    # Obtener datos actuales del cliente
    cursor.execute("SELECT * FROM Clientes WHERE DNI=%s", (dni,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render(request, 'Taller/adminis/clientes/editar_cliente.html', {"cliente": cliente})


def eliminar_cliente(request, dni):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Clientes WHERE DNI=%s", (dni,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('clientes')

#Panel de administracion de Vehiculos