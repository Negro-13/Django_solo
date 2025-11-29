from django.shortcuts import render

# Páginas principales
def pagina_principal(request):
    return render(request, 'Taller/pagina_principal.html')

def login_view(request):
    return render(request, 'Taller/login.html')

def register(request):
    return render(request, 'Taller/register.html')

# @login_required
def administracion(request):
    return render(request, 'Taller/administracion.html')

# @login_required
def presupuesto(request):
    return render(request, 'Taller/presupuesto.html', {})

def quienes_somos(request):
    return render(request, 'Taller/quienes_somos.html')

def ubicacion_contacto(request):
    return render(request, 'Taller/ubicacion_contacto.html')


# Panel de administración
def clientes(request):
    return render(request, 'Taller/adminis/clientes.html')
