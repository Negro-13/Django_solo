from django.shortcuts import render, redirect
import mysql.connector
from .forms import LoginForm

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="Taller_Mecanico_dj",
        port=3306
    )
# Páginas principales
def pagina_principal(request):
    return render(request, 'Taller/pagina_principal.html')

def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            usuario = form.cleaned_data["usuario"]
            clave = form.cleaned_data["clave"]

            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT * FROM usuarios 
                WHERE usuario = %s AND clave = %s
            """, (usuario, clave))

            user = cursor.fetchone()
            conn.close()

            if user:
                response = redirect("administracion")
                response.set_cookie("usuario", usuario)
                response.set_cookie("rol", user["rol"])
                return response
            else:
                return render(request, "Taller/login.html", {
                    "form": form,
                    "error": "Usuario o clave incorrectos"
                })

    return render(request, "Taller/login.html", {"form": form})

def register(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario")
        clave = request.POST.get("clave")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO usuarios (usuario, clave) VALUES (%s, %s)",
            (usuario, clave)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("login")

    return render(request, "Taller/register.html")

def logout_view(request):
    response = redirect("login")
    response.delete_cookie("usuario")
    response.delete_cookie("rol")
    return response

def administracion(request):
    if not request.COOKIES.get("usuario"):
        return redirect("login")
    return render(request, 'Taller/administracion.html')

def presupuesto(request):
    return render(request, 'Taller/presupuesto.html', {})

def quienes_somos(request):
    return render(request, 'Taller/quienes_somos.html')

def ubicacion_contacto(request):
    return render(request, 'Taller/ubicacion_contacto.html')


# Panel de administración: CRUD de clientes
def clientes(request):
    if not request.COOKIES.get("usuario"):
        return redirect("login")

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
    q = request.GET.get("q")

    if q:
        cursor.execute("""
        SELECT * FROM Clientes 
        WHERE DNI LIKE %s 
           OR Nombre LIKE %s 
           OR Apellido LIKE %s
    """, (f"%{q}%", f"%{q}%", f"%{q}%"))
    else:
        cursor.execute("SELECT * FROM Clientes")

    clientes_db = cursor.fetchall()

    cursor.close()
    conn.close()

    return render(request, 'Taller/adminis/clientes/clientes.html', {"clientes": clientes_db})

def editar_cliente(request, dni):
    if not request.COOKIES.get("usuario"):
        return redirect("login")

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
    if not request.COOKIES.get("usuario"):
        return redirect("login")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Clientes WHERE DNI=%s", (dni,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('clientes')

#Panel de administracion de Vehiculos
# Panel de administración: CRUD de vehículos
def vehiculos(request):
    # Si se está editando un vehículo, pasa el objeto 'vehiculo' al template
    vehiculo = None
    if not request.COOKIES.get("usuario"):
        return redirect("login")
    if request.method == "POST":
        patente = request.POST.get("patente")
        dni = request.POST.get("dni")
        marca = request.POST.get("marca")
        modelo = request.POST.get("modelo")
        color = request.POST.get("color")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Vehiculos (Patente, DNI, Marca, Modelo, Color) VALUES (%s, %s, %s, %s, %s)",
            (patente, dni, marca, modelo, color)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect('vehiculos')

    # Leer los datos de la tabla Vehiculos
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    q = request.GET.get("q")

    if q:
        cursor.execute("""
        SELECT * FROM Vehiculos
        WHERE Patente LIKE %s
           OR DNI LIKE %s
           OR Marca LIKE %s
           OR Modelo LIKE %s
    """, (f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"))
    else:
        cursor.execute("SELECT * FROM Vehiculos")

    vehiculos_db = cursor.fetchall()

    cursor.close()
    conn.close()
    return render(request, 'Taller/adminis/vehiculos/vehiculos.html', {"vehiculos": vehiculos_db, "vehiculo": vehiculo})

def editar_vehiculo(request, patente):
    if not request.COOKIES.get("usuario"):
        return redirect("login")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        dni = request.POST.get("dni")
        marca = request.POST.get("marca")
        modelo = request.POST.get("modelo")
        color = request.POST.get("color")

        cursor.execute(
            "UPDATE Vehiculos SET DNI=%s, Marca=%s, Modelo=%s, Color=%s WHERE Patente=%s",
            (dni, marca, modelo, color, patente)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('vehiculos')

    # Obtener datos actuales del vehículo
    cursor.execute("SELECT * FROM Vehiculos WHERE Patente=%s", (patente,))
    vehiculo = cursor.fetchone()
    cursor.close()
    conn.close()

    return render(request, 'Taller/adminis/vehiculos/vehiculos.html', {"vehiculos": [], "vehiculo": vehiculo})


def eliminar_vehiculo(request, patente):
    if not request.COOKIES.get("usuario"):
        return redirect("login")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Vehiculos WHERE Patente=%s", (patente,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('vehiculos')
# Panel de administración: CRUD de fichas técnicas
def fichas_tecnicas(request):
    if not request.COOKIES.get("usuario"):
        return redirect("login")
    if request.method == "POST":
        cod_cliente = request.POST.get("cod_cliente")
        vehiculo = request.POST.get("vehiculo")
        subtotal = request.POST.get("subtotal")
        mano_obra = request.POST.get("mano_obra")
        total_general = float(subtotal) + float(mano_obra)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ficha_tecnica (cod_cliente, vehiculo, subtotal, mano_obra, total_general) "
            "VALUES (%s, %s, %s, %s, %s)",
            (cod_cliente, vehiculo, subtotal, mano_obra, total_general)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('fichas_tecnicas')

    # Leer los datos de la tabla ficha_tecnica
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    q = request.GET.get("q")

    if q:
        cursor.execute("""
        SELECT f.nro_ficha, f.cod_cliente, f.vehiculo, f.subtotal, f.mano_obra, f.total_general,
               c.Nombre, c.Apellido, v.Marca, v.Modelo
        FROM ficha_tecnica f
        JOIN Clientes c ON f.cod_cliente = c.DNI
        JOIN Vehiculos v ON f.vehiculo = v.Patente
        WHERE c.Nombre LIKE %s
           OR c.Apellido LIKE %s
           OR v.Marca LIKE %s
           OR v.Modelo LIKE %s
    """, (f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"))
    else:
        cursor.execute("""
        SELECT f.nro_ficha, f.cod_cliente, f.vehiculo, f.subtotal, f.mano_obra, f.total_general,
               c.Nombre, c.Apellido, v.Marca, v.Modelo
        FROM ficha_tecnica f
        JOIN Clientes c ON f.cod_cliente = c.DNI
        JOIN Vehiculos v ON f.vehiculo = v.Patente
        ORDER BY f.nro_ficha
    """)

    fichas_db = cursor.fetchall()


    # Obtener clientes y vehículos para el formulario
    cursor.execute("SELECT DNI, Nombre, Apellido FROM Clientes")
    clientes = cursor.fetchall()
    cursor.execute("SELECT Patente, Marca, Modelo FROM Vehiculos")
    vehiculos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render(request, 'Taller/adminis/fichas_tecnicas/fichas_tecnicas.html', {
        "fichas": fichas_db,
        "clientes": clientes,
        "vehiculos": vehiculos
    })

def editar_ficha_tecnica(request, nro_ficha):
    if not request.COOKIES.get("usuario"):
        return redirect("login")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        subtotal = request.POST.get("subtotal")
        mano_obra = request.POST.get("mano_obra")
        total_general = float(subtotal) + float(mano_obra)

        cursor.execute(
            "UPDATE ficha_tecnica SET subtotal=%s, mano_obra=%s, total_general=%s WHERE nro_ficha=%s",
            (subtotal, mano_obra, total_general, nro_ficha)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('fichas_tecnicas')

    # Obtener datos de la ficha técnica
    cursor.execute("""
        SELECT f.nro_ficha, f.cod_cliente, f.vehiculo, f.subtotal, f.mano_obra, f.total_general,
               c.Nombre, c.Apellido, v.Marca, v.Modelo
        FROM ficha_tecnica f
        JOIN Clientes c ON f.cod_cliente = c.DNI
        JOIN Vehiculos v ON f.vehiculo = v.Patente
        WHERE f.nro_ficha = %s
    """, (nro_ficha,))
    ficha = cursor.fetchone()

    cursor.close()
    conn.close()

    return render(request, 'Taller/adminis/fichas_tecnicas/editar_ficha_tecnica.html', {"ficha": ficha})

def eliminar_ficha_tecnica(request, nro_ficha):
    if not request.COOKIES.get("usuario"):
        return redirect("login")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ficha_tecnica WHERE nro_ficha=%s", (nro_ficha,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('fichas_tecnicas')
# Panel de administración: CRUD de mecánicos
def mecanicos(request):
    if not request.COOKIES.get("usuario"):
        return redirect("login")
    if request.method == "POST":
        legajo = request.POST.get("legajo")
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        rol = request.POST.get("rol")
        estado = request.POST.get("estado")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Mecanicos (Legajo, Nombre, Apellido, Rol, Estado) VALUES (%s, %s, %s, %s, %s)",
            (legajo, nombre, apellido, rol, estado)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('mecanicos')

    # Leer los datos de la tabla Mecanicos
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    q = request.GET.get("q")

    if q:
        cursor.execute("""
        SELECT * FROM Mecanicos
        WHERE Legajo LIKE %s
           OR Nombre LIKE %s
           OR Apellido LIKE %s
           OR Rol LIKE %s
    """, (f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"))
    else:
        cursor.execute("SELECT * FROM Mecanicos")

    mecanicos_db = cursor.fetchall()

    cursor.close()
    conn.close()

    return render(request, 'Taller/adminis/mecanicos/mecanicos.html', {"mecanicos": mecanicos_db})

def editar_mecanico(request, legajo):
    if not request.COOKIES.get("usuario"):
        return redirect("login")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        rol = request.POST.get("rol")
        estado = request.POST.get("estado")

        cursor.execute(
            "UPDATE Mecanicos SET Nombre=%s, Apellido=%s, Rol=%s, Estado=%s WHERE Legajo=%s",
            (nombre, apellido, rol, estado, legajo)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('mecanicos')

    # Obtener datos actuales del mecánico
    cursor.execute("SELECT * FROM Mecanicos WHERE Legajo=%s", (legajo,))
    mecanico = cursor.fetchone()
    cursor.close()
    conn.close()

    return render(request, 'Taller/adminis/mecanicos/editar_mecanico.html', {"mecanico": mecanico})

def eliminar_mecanico(request, legajo):
    if not request.COOKIES.get("usuario"):
        return redirect("login")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Mecanicos WHERE Legajo=%s", (legajo,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('mecanicos')
# Panel de administración: CRUD de proveedores
def proveedores(request):
    if not request.COOKIES.get("usuario"):
        return redirect("login")
    if request.method == "POST":
        cod_prov = request.POST.get("cod_prov")
        nombre = request.POST.get("nombre")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        direccion = request.POST.get("direccion")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Proveedores (Cod_prov, Nombre, Telefono, Email, Direccion) VALUES (%s, %s, %s, %s, %s)",
            (cod_prov, nombre, telefono, email, direccion)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('proveedores')

    # Leer los datos de la tabla Proveedores
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    q = request.GET.get("q")

    if q:
        cursor.execute("""
        SELECT * FROM Proveedores
        WHERE Cod_prov LIKE %s
           OR Nombre LIKE %s
           OR Telefono LIKE %s
           OR Email LIKE %s
    """, (f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"))
    else:
        cursor.execute("SELECT * FROM Proveedores")

    proveedores_db = cursor.fetchall()

    cursor.close()
    conn.close()

    return render(request, 'Taller/adminis/proveedores/proveedores.html', {"proveedores": proveedores_db})

def editar_proveedor(request, cod_prov):
    if not request.COOKIES.get("usuario"):
        return redirect("login")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        direccion = request.POST.get("direccion")

        cursor.execute(
            "UPDATE Proveedores SET Nombre=%s, Telefono=%s, Email=%s, Direccion=%s WHERE Cod_prov=%s",
            (nombre, telefono, email, direccion, cod_prov)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('proveedores')

    # Obtener datos actuales del proveedor
    cursor.execute("SELECT * FROM Proveedores WHERE Cod_prov=%s", (cod_prov,))
    proveedor = cursor.fetchone()
    cursor.close()
    conn.close()

    return render(request, 'Taller/adminis/proveedores/editar_proveedor.html', {"proveedor": proveedor})

def eliminar_proveedor(request, cod_prov):
    if not request.COOKIES.get("usuario"):
        return redirect("login")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Proveedores WHERE Cod_prov=%s", (cod_prov,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('proveedores')
# Panel de administración: CRUD de repuestos
def repuestos(request):
    if not request.COOKIES.get("usuario"):
        return redirect("login")
    if request.method == "POST":
        codigo_repuesto = request.POST.get("codigo_repuesto")
        descripcion = request.POST.get("descripcion")
        cant_rep_libre = request.POST.get("cant_rep_libre")
        cant_rep_total = request.POST.get("cant_rep_total")
        proveedor = request.POST.get("proveedor")
        precio = request.POST.get("precio")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Stock (Codigo_repuesto, Descripcion, Cant_rep_libre, Cant_rep_total, Proveedor, Precio) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (codigo_repuesto, descripcion, cant_rep_libre, cant_rep_total, proveedor, precio)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('repuestos')

    # Leer los datos de la tabla Stock
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.Codigo_repuesto, s.Descripcion, s.Cant_rep_libre, s.Cant_rep_total, s.Proveedor, s.Precio, p.Nombre as NombreProveedor
        FROM Stock s
        JOIN Proveedores p ON s.Proveedor = p.Cod_prov
    """)
    repuestos_db = cursor.fetchall()

    # Obtener proveedores para el formulario
    cursor.execute("SELECT Cod_prov, Nombre FROM Proveedores")
    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    return render(request, 'Taller/adminis/repuestos/repuestos.html', {
        "repuestos": repuestos_db,
        "proveedores": proveedores
    })

def editar_repuesto(request, codigo_repuesto):
    if not request.COOKIES.get("usuario"):
        return redirect("login")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        descripcion = request.POST.get("descripcion")
        cant_rep_libre = request.POST.get("cant_rep_libre")
        cant_rep_total = request.POST.get("cant_rep_total")
        proveedor = request.POST.get("proveedor")
        precio = request.POST.get("precio")

        cursor.execute(
            "UPDATE Stock SET Descripcion=%s, Cant_rep_libre=%s, Cant_rep_total=%s, Proveedor=%s, Precio=%s "
            "WHERE Codigo_repuesto=%s",
            (descripcion, cant_rep_libre, cant_rep_total, proveedor, precio, codigo_repuesto)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('repuestos')

    # Obtener datos actuales del repuesto
    q = request.GET.get("q")

    if q:
        cursor.execute("""
        SELECT s.Codigo_repuesto, s.Descripcion, s.Cant_rep_libre, s.Cant_rep_total, 
               s.Proveedor, s.Precio, p.Nombre as NombreProveedor
        FROM Stock s
        JOIN Proveedores p ON s.Proveedor = p.Cod_prov
        WHERE s.Codigo_repuesto LIKE %s
           OR s.Descripcion LIKE %s
           OR p.Nombre LIKE %s
    """, (f"%{q}%", f"%{q}%", f"%{q}%"))
    else:
        cursor.execute("""
        SELECT s.Codigo_repuesto, s.Descripcion, s.Cant_rep_libre, s.Cant_rep_total, 
               s.Proveedor, s.Precio, p.Nombre as NombreProveedor
        FROM Stock s
        JOIN Proveedores p ON s.Proveedor = p.Cod_prov
    """)

    repuesto = cursor.fetchall()


    # Obtener proveedores para el formulario
    cursor.execute("SELECT Cod_prov, Nombre FROM Proveedores")
    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    return render(request, 'Taller/adminis/repuestos/editar_repuesto.html', {
        "repuesto": repuesto,
        "proveedores": proveedores
    })


def eliminar_repuesto(request, codigo_repuesto):
    if not request.COOKIES.get("usuario"):
        return redirect("login")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Stock WHERE Codigo_repuesto=%s", (codigo_repuesto,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('repuestos')