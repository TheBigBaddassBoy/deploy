from django.urls import path
from . import views

app_name = 'tareas'  # Definir el espacio de nombres de la aplicación

urlpatterns = [
    path('lista/', views.lista_tareas, name='lista_tareas'),
    path('subir/', views.subir_tarea, name='subir_tarea'),  # Profesores suben tareas
    path('subir_alumno/', views.subir_tarea_alumno, name='subir_tarea_alumno'),  # Alumnos suben tareas
    path('descargar/<int:tarea_id>/', views.descargar_tarea, name='descargar_tarea'),
    path('calificar/<int:tarea_id>/', views.calificar_tarea, name='calificar_tarea'),  # Calificación de tareas
    path('mis-calificaciones/', views.mis_calificaciones, name='mis_calificaciones'),
]
