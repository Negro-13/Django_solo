from django.urls import path
from . import views

urlpatterns = [
    #Paginas principales
    
    path('', views.pagina_principal, name='pagina_principal'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
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
]