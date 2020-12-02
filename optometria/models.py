import datetime

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200)
    precio = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    LEJOS = 'LE'
    CERCA = 'CE'
    DISTANCIA_CHOICES = [
        (LEJOS, "Lejos"),
        (CERCA, "Cerca")
    ]

    IZQUIERDA = 'IQ'
    DERECHA = 'DR'
    LADO_CHOICES = [
        (IZQUIERDA, "Izquierda"),
        (DERECHA, "Derecha")
    ]

    distancia = models.CharField(
        max_length=2,
        choices=DISTANCIA_CHOICES,
        default=LEJOS
    )

    lado = models.CharField(
        max_length=2,
        choices=LADO_CHOICES,
        default=DERECHA
    )

    CON_ARMAZON = 'CA'
    SIN_ARMAZON = 'SA'
    ARMAZON_CHOICES = [
        (CON_ARMAZON, "Si"),
        (SIN_ARMAZON, "No")
    ]

    armazon = models.CharField(
        max_length=2,
        choices=ARMAZON_CHOICES,
        default=CON_ARMAZON
    )

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    fechaDePedido = models.DateTimeField()
    montoTotal = models.DecimalField(max_digits=19, decimal_places=4)
    vendedor = models.ForeignKey('Vendedor', null=True, on_delete=models.SET_NULL)
    paciente = models.ForeignKey('Paciente', null=True, on_delete=models.SET_NULL)

    CREDITO = 'CR'
    DEBITO = 'DB'
    VIRTUAL = 'VT'
    EFECTIVO = 'EF'
    MONEY_CHOICES = [
        (CREDITO, "Tarjeta de Credito"),
        (DEBITO, "Tarjeta de Debito"),
        (VIRTUAL, "Billetera Virtual"),
        (EFECTIVO, "Efectivo")
    ]

    tipoDePago = models.CharField(
        max_length=2,
        choices=MONEY_CHOICES,
        default=EFECTIVO
    )

    PENDIENTE = 'PT'
    PEDIDO = 'PD'
    TALLER = 'TL'
    FINALIZADO = 'FN'
    ESTADOS_DE_PEDIDO = [
        (PENDIENTE, "Pendiente"),
        (PEDIDO, "Pedido"),
        (TALLER, "Enviado a Taller"),
        (FINALIZADO, "Finalizado")
    ]

    estado = models.CharField(
        max_length=2,
        choices=ESTADOS_DE_PEDIDO,
        default=PENDIENTE
    )



class ProductoPedido(models.Model):
    producto = models.ForeignKey(Producto, null=True, on_delete=models.SET_NULL)
    cantidad = models.IntegerField(default=1) 
    pedido = models.ForeignKey(Pedido, null=True, on_delete=models.SET_NULL)
    
    def getSubTotal(self):
        return self.producto.precio * self.cantidad


class Paciente(models.Model):
    dni = models.BigIntegerField()
    email = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Turno(models.Model):
    fechaDeTurno = models.DateTimeField()
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    secretaria = models.ForeignKey('Secretaria', on_delete=models.CASCADE)

class HistorialMedico(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    turno = models.ForeignKey('Turno', on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=500)
    personalMedico = models.ForeignKey('PersonalMedico', on_delete=models.CASCADE)

class PersonalMedico(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.usuario.nombre + " " + self.usuario.apellido

class Secretaria(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.usuario.nombre + " " + self.usuario.apellido

class Vendedor(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.usuario.nombre + " " + self.usuario.apellido

class Tecnico(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.usuario.nombre + " " + self.usuario.apellido

class Gerente(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.usuario.nombre + " " + self.usuario.apellido


class UsuarioManager(BaseUserManager):
    def create_user(self, email, name, lastname, phone, date_of_birth, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            nombre=name,
            apellido=lastname,
            telefono=phone,
            fecha_nac=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, name, lastname, phone, date_of_birth, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.create_user(
            email=self.normalize_email(email),
            nombre=name,
            apellido=lastname,
            telefono=phone,
            fecha_nac=date_of_birth,
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(AbstractUser):
    first_name = None
    last_name = None

    username = models.CharField(max_length=32)
    nombre = models.CharField(max_length=200)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=200, unique=True, primary_key=True)
    apellido = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)
    fecha_nac = models.DateTimeField(default=None, blank=True, null=True)
    is_admin = False

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'username']

    def __str__(self):
        return self.email

    def has_related_object(self, related):
        return hasattr(self, related)


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

