from django import forms
from .models import Tareacreada, TareadelAlumno, TareaCalificada

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tareacreada
        fields = ['nombre', 'descripcion','modulo', 'fecha_limite', 'archivo']

class SubirTareaForm(forms.ModelForm):
    class Meta:
        model = TareadelAlumno
        fields = ['tarea', 'archivo']


class CalificarTareaForm(forms.Form):
    tarea_id = forms.IntegerField(widget=forms.HiddenInput())
    calificacion = forms.IntegerField(
        min_value=0, 
        max_value=10, 
        label="Calificación",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

