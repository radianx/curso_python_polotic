from django import forms
from models import Secretaria

class NuevoTurnoForm(forms.form):
    secretaria = forms.ChoiceField(widget=forms.Select, choices=Secretaria.objects.all().values_list(pk, usuario.nombre), required=True, help_text="Secretaria")
    paciente = Paciente.objects.get(pk=request.POST.get('id_paciente'))
    fecha = request.POST.get('fecha_turno')
    hora = request.POST.get('hora_turno')
    momento = datetime.combine(fecha, hora)
    turno = Turno(paciente, momento, secretaria)