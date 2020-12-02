from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from optometria.models import  *
from pprint import pprint 

# Create your views here.

def index(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse("login"))		
	return render(request, "index.html")

def lista_pedidos(request):
	return render(request, 'pedidos/lista_pedidos.html')

def lista_turno(request):
	if not request.user.has_related_object('secretaria') or request.user.has_related_object('gerente'):
		return render(request, 'index.html')
	turnos = Turno.objects.all()
	return render(request, 'turnos/lista_turnos.html', {'turnos': turnos})

def nuevo_turno(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse("login"))
	elif request.method == "POST":
		usuario = Usuario.objects.get(pk=request.user.email)
		secretaria = usuario.secretaria
		paciente = Paciente.objects.get(dni=request.POST['paciente'])
		fecha = request.POST['fecha_turno']
		hora = request.POST['hora_turno']
		date_time_str = fecha+hora
		momento = datetime.datetime.strptime(date_time_str, '%Y-%m-%d%H:%M')
		turno = Turno(paciente=paciente, fechaDeTurno=momento, secretaria=secretaria)
		turno.save()
		turnos = Turno.objects.all()
		return render(request, 'turnos/lista_turnos.html', {'turnos': turnos})

	pacientes = Paciente.objects.all()
	return render(request, "turnos/nuevo_turno.html", {'pacientes': pacientes})

def eliminar_turno(request, id):
	turno = Turno.objects.get(id=id)
	turno.delete()
	turnos = Turno.objects.all()
	return render(request, "turnos/lista_turnos.html", {'turnos': turnos})

def modificar_turno(request, id):
	if request.method == "POST":
		fecha = request.POST['fecha_turno']
		hora = request.POST['hora_turno']
		date_time_str = fecha+hora
		momento = datetime.datetime.strptime(date_time_str, '%Y-%m-%d%H:%M')
		turno = Turno.objects.get(id=id)
		turno.__setattr__('fechaDeTurno', momento)
		turno.save(force_update=True)
		turnos = Turno.objects.all()
		return render(request, 'turnos/lista_turnos.html', {'turnos': turnos})
	else:
		turno = Turno.objects.get(id=id)
		return render(request, "turnos/editar_turno.html", {'turno': turno})

def register(request):
	if request.method == "POST":
		email = request.POST['email']
		password = request.POST['password']
		secondpass = request.POST['repeat_pass']
		nombre = request.POST['nombre']
		apellido = request.POST['apellido']
		telefono = request.POST['telefono']
		fecha_nac = request.POST['fecha_nac']
		rol = request.POST['rol']	
		if password == secondpass:
			user = Usuario(nombre=nombre, email=email, telefono=telefono, apellido=apellido, fecha_nac=fecha_nac)
			user.set_password(password)
			user.save()

			if rol == "Secretaria":
				user_rol = Secretaria(user.email)
			elif rol == "Profesional_medico":
				user_rol = PersonalMedico(user.email)
			elif rol == "Ventas":
				user_rol = Vendedor(user.email)
			elif rol == "Taller":
				user_rol = Tecnico(user.email)
			elif rol == "Gerencia":
				user_rol = Gerente(user.email)
			
			user_rol.save()

			return HttpResponseRedirect(reverse("index")) 
	else:
		return render(request, "usuarios/register.html")

def login_view(request):
	if request.method == "POST":
		email = request.POST.get('email')
		password = request.POST.get('password')

		usuario = authenticate(request, email=email, password=password)
		

		if usuario:
			login(request, usuario)
			return HttpResponseRedirect(reverse('index'))
		else:
			return render(request, 'usuarios/login.html', 
			{
				"mensaje": "Credenciales inválidas"
			})
	return render(request, 'usuarios/login.html')

def logout_view(request):
	logout(request)
	return render(request, "usuarios/login.html", {"mensaje": "Ud. se ha desconectado."})