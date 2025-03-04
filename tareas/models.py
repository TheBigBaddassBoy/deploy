from django.db import models
from django.contrib.auth.models import User

class Tareacreada(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField()
    estado = models.BooleanField(default=False)
    modulo = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='archivos', null=True, blank=True)

    def __str__(self):
        return self.nombre

class TareadelAlumno(models.Model):
    tarea = models.ForeignKey(Tareacreada, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Alumno que subió la tarea
    archivo = models.FileField(upload_to='tareas_alumnos/')
    fecha_entrega = models.DateTimeField(auto_now_add=True)
    calificacion = models.IntegerField(null=True, blank=True)  # Asegúrate de permitir valores nulos

    def __str__(self):
        return self.tarea.nombre

class TareaCalificada(models.Model):
    tarea_alumno = models.OneToOneField(TareadelAlumno, on_delete=models.CASCADE)
    calificacion = models.FloatField()
    fecha_calificacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tarea_alumno.usuario.get_full_name} - {self.calificacion}"

