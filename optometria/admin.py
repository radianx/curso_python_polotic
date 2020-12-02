from django.contrib import admin
from .models import *

admin.site.register(Usuario)
admin.site.register(PersonalMedico)
admin.site.register(Pedido)
admin.site.register(Vendedor)
admin.site.register(Secretaria)
admin.site.register(Gerente)
admin.site.register(Tecnico)
admin.site.register(Producto)
admin.site.register(ProductoPedido)
admin.site.register(Turno)
admin.site.register(Paciente)
admin.site.register(HistorialMedico)

# Register your models here.
