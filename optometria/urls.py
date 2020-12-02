from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),

	#turno
	path('nuevo_turno', views.nuevo_turno, name='nuevo_turno'),
	path('modificar_turno/<int:id>', views.modificar_turno, name='modificar_turno'),
	path('eliminar_turno/<int:id>', views.eliminar_turno, name='eliminar_turno'),
	path('lista_turno', views.lista_turno, name='lista_turno'),

	#usuario
	path('register', views.register, name='register'),
	path('login', views.login_view, name='login'),
	path('logout', views.logout_view, name='logout'),

	#pedidos
	path('lista_pedidos', views.lista_pedidos, name='lista_pedidos'),
	path('nuevo_pedido', views.nuevo_pedido, name='nuevo_pedido'),
	path('ver_pedido/<id>', views.ver_pedido, name='ver_pedido')
]
