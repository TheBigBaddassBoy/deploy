from django.shortcuts import render, redirect, get_object_or_404
from .forms import TareaForm, SubirTareaForm, CalificarTareaForm
from .models import Tareacreada, TareadelAlumno, TareaCalificada
from django.http import HttpResponse
import os
from django.contrib.auth.decorators import login_required

# Vista para que los profesores creen tareas
def subir_tarea(request):
    if request.user.is_superuser:  # Solo los profesores pueden crear tareas
        if request.method == 'POST':
            form = TareaForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()  # Guarda la tarea creada
                return redirect('tareas:lista_tareas')  # Redirigir a la lista de tareas
        else:
            form = TareaForm()  # Si no es un POST, muestra el formulario vacío
        return render(request, 'tareas/subir_archivo.html', {'form': form})
    else:
        return redirect('tareas:lista_tareas')  # Si no es un profesor, redirige a la lista de tareas

# Vista para que los alumnos suban sus tareas
def subir_tarea_alumno(request):
    if request.method == 'POST':
        form = SubirTareaForm(request.POST, request.FILES)
        if form.is_valid():
            tarea_subida = form.save(commit=False)
            tarea_subida.usuario = request.user  # Asocia la tarea al usuario actual
            tarea_subida.save()
            return redirect('tareas:lista_tareas')  # Redirigir a la lista de tareas
    else:
        form = SubirTareaForm()  # Si no es un POST, muestra el formulario vacío
    
    return render(request, 'tareas/subir_tarea.html', {'form': form})

# Vista para mostrar las tareas creadas y subidas (según el tipo de usuario)
def lista_tareas(request):
    if request.user.is_superuser:
        # Si es profesor (superusuario), muestra todas las tareas creadas y las tareas subidas
        tareas_creadas = Tareacreada.objects.all()
        tareas_alumnos = TareadelAlumno.objects.all()  # Ver todas las tareas subidas por los alumnos
    else:
        # Si es alumno, solo muestra las tareas que ha subido
        tareas_creadas = Tareacreada.objects.all()
        tareas_alumnos = TareadelAlumno.objects.filter(usuario=request.user)  # Filtrar tareas subidas por el usuario

    return render(request, 'tareas/lista_archivos.html', {
        'tareas_creadas': tareas_creadas,
        'tareas_alumnos': tareas_alumnos,
        'es_superuser': request.user.is_superuser
    })

# Vista para descargar los archivos de las tareas creadas por los profesores
def descargar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareacreada, id=tarea_id)
    
    if not tarea.archivo:
        return HttpResponse("Archivo no encontrado", status=404)

    file_path = tarea.archivo.path  # Obtiene la ruta del archivo en el sistema de archivos
    if os.path.exists(file_path):
        with open(file_path, 'rb') as archivo:
            response = HttpResponse(archivo.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    else:
        return HttpResponse("Archivo no encontrado", status=404)


@login_required
def calificar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareacreada, id=tarea_id)
    tareas_alumnos = TareadelAlumno.objects.filter(tarea=tarea)

    if request.method == 'POST':
        form = CalificarTareaForm(request.POST)
        if form.is_valid():
            tarea_alumno = get_object_or_404(TareadelAlumno, id=form.cleaned_data['tarea_id'])
            calificacion = form.cleaned_data['calificacion']

            # Guardar la calificación en el modelo de tareas de alumnos
            tarea_alumno.calificacion = calificacion
            tarea_alumno.save()

            return redirect('tareas:calificar_tarea', tarea_id=tarea.id)
    else:
        form = CalificarTareaForm()

    return render(request, 'tareas/calificar_tarea.html', {
        'tarea': tarea,
        'tareas_alumnos': tareas_alumnos,
        'form': form
    })


def mis_calificaciones(request):
    tareas_alumnos_usuario = TareadelAlumno.objects.filter(usuario=request.user)
    for tarea_alumno in tareas_alumnos_usuario:
        print(f'Tarea: {tarea_alumno.tarea.nombre}, Calificación: {tarea_alumno.calificacion}')
    context = {
        'tareas_alumnos_usuario': tareas_alumnos_usuario,
        'es_superuser': request.user.is_superuser,
    }
    return render(request, 'tareas/mis_calificaciones.html', context)
