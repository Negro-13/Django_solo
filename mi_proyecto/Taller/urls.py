from django.urls import path
from . import views

urlpatterns = [
    #Paginas principales
    
    path('', views.pagina_principal, name='pagina_principal'),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),

    path('administracion/', views.administracion, name='administracion'),
    path('presupuesto/', views.presupuesto, name='presupuesto'),
    path('quienes_somos/', views.quienes_somos, name='quienes_somos'),
    path('ubicacion_contacto/', views.ubicacion_contacto, name='ubicacion_contacto'),
    
    #Paginas de administracion
    #Clientes
    path('administracion/clientes/', views.clientes, name='clientes'),
    path('administracion/clientes/editar/<str:dni>/', views.editar_cliente, name='editar_cliente'),
    path('administracion/clientes/eliminar/<str:dni>/', views.eliminar_cliente, name='eliminar_cliente'),

    #Vehiculos
    # Agrega estas rutas en urls.py
    path('administracion/vehiculos/', views.vehiculos, name='vehiculos'),
    path('administracion/vehiculos/editar/<str:patente>/', views.editar_vehiculo, name='editar_vehiculo'),
    path('administracion/vehiculos/eliminar/<str:patente>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
# Panel de administración: Fichas Técnicas
    path('administracion/fichas_tecnicas/', views.fichas_tecnicas, name='fichas_tecnicas'),
    path('administracion/fichas_tecnicas/editar/<int:nro_ficha>/', views.editar_ficha_tecnica, name='editar_ficha_tecnica'),
    path('administracion/fichas_tecnicas/eliminar/<int:nro_ficha>/', views.eliminar_ficha_tecnica, name='eliminar_ficha_tecnica'),
# Panel de administración: Mecánicos
    path('administracion/mecanicos/', views.mecanicos, name='mecanicos'),
    path('administracion/mecanicos/editar/<str:legajo>/', views.editar_mecanico, name='editar_mecanico'),
    path('administracion/mecanicos/eliminar/<str:legajo>/', views.eliminar_mecanico, name='eliminar_mecanico'),
# Panel de administración: Proveedores
    path('administracion/proveedores/', views.proveedores, name='proveedores'),
    path('administracion/proveedores/editar/<str:cod_prov>/', views.editar_proveedor, name='editar_proveedor'),
    path('administracion/proveedores/eliminar/<str:cod_prov>/', views.eliminar_proveedor, name='eliminar_proveedor'),
# Panel de administración: Repuestos
    path('administracion/repuestos/', views.repuestos, name='repuestos'),
    path('administracion/repuestos/editar/<str:codigo_repuesto>/', views.editar_repuesto, name='editar_repuesto'),
    path('administracion/repuestos/eliminar/<str:codigo_repuesto>/', views.eliminar_repuesto, name='eliminar_repuesto'),

]