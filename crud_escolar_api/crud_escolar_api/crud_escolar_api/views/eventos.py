from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from crud_escolar_api.serializers import *
from crud_escolar_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
import string
import random
import json  

class EventoAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        evento = Evento.objects.filter().order_by("id")
        evento = EventoSerializer(evento, many=True).data
 
        return Response(evento, 200)

class EventoView(generics.CreateAPIView):
    #Obtener usuario por ID
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        evento = get_object_or_404(Evento, id = request.GET.get("id"))
        evento = EventoSerializer(evento, many=False).data
        evento["publico_objetivo"] = json.loads(evento["publico_objetivo"])
 
        return Response(evento, 200)
   
    #Registrar nuevo usuario
    @transaction.atomic
    def post(self,request, *args, **kwargs):
            evento = EventoSerializer(data=request.data)            
 
            evento = Evento.objects.create(
                                            nombre_evento= request.data["nombre_evento"],
                                            tipo_evento= request.data["tipo_evento"] ,          
                                            fecha_evento= request.data["fecha_evento"],
                                            hora_inicio= request.data["hora_inicio"],
                                            hora_fin= request.data["hora_fin"],
                                            lugar= request.data["lugar"],
                                            publico_objetivo = json.dumps (request.data["publico_objetivo"]),
                                            programa_educativo = request.data["programa_educativo"],
                                            responsable_evento= request.data["responsable_evento"],
                                            descripcion = request.data["descripcion"],
                                            cupo_maximo= request.data["cupo_maximo"])
            
 
            evento.save()
 
            return Response({"Evento creado": evento.id }, 201)
 
            return Response(Evento.errors, status=status.HTTP_400_BAD_REQUEST)


    
#Se agrega edicion y eliminar maestros
class EventosViewEdit(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def put(self, request, *args, **kwargs):
        try:
            evento = get_object_or_404(Evento, id=request.data.get("id"))
            
            # Validar y formatear la fecha
            fecha_evento = request.data.get("fecha_evento")
            if fecha_evento:
                try:
                    # Asegurar el formato YYYY-MM-DD
                    if isinstance(fecha_evento, str):
                        fecha_evento = datetime.strptime(fecha_evento, "%Y-%m-%d").date()
                    evento.fecha_evento = fecha_evento
                except (ValueError, TypeError) as e:
                    return Response(
                        {"error": "Formato de fecha inválido. Use YYYY-MM-DD"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Validar y formatear las horas
            hora_inicio = request.data.get("hora_inicio")
            if hora_inicio:
                # Asegurar formato HH:MM:SS
                if len(hora_inicio.split(':')) == 2:
                    hora_inicio += ":00"
                evento.hora_inicio = hora_inicio

            hora_fin = request.data.get("hora_fin")
            if hora_fin:
                # Asegurar formato HH:MM:SS
                if len(hora_fin.split(':')) == 2:
                    hora_fin += ":00"
                evento.hora_fin = hora_fin

            # Actualizar los demás campos
            evento.nombre_evento = request.data.get("nombre_evento", evento.nombre_evento)
            evento.tipo_evento = request.data.get("tipo_evento", evento.tipo_evento)
            evento.lugar = request.data.get("lugar", evento.lugar)
            
            # Manejar público objetivo (puede venir como lista o como string JSON)
            publico_objetivo = request.data.get("publico_objetivo")
            if publico_objetivo is not None:
                if isinstance(publico_objetivo, str):
                    try:
                        publico_objetivo = json.loads(publico_objetivo)
                    except json.JSONDecodeError:
                        publico_objetivo = [publico_objetivo]
                evento.publico_objetivo = json.dumps(publico_objetivo)
            
            evento.programa_educativo = request.data.get("programa_educativo", evento.programa_educativo)
            evento.responsable_evento = request.data.get("responsable_evento", evento.responsable_evento)
            evento.descripcion = request.data.get("descripcion", evento.descripcion)
            
            # Validar cupo máximo
            cupo_maximo = request.data.get("cupo_maximo")
            if cupo_maximo is not None:
                try:
                    evento.cupo_maximo = int(cupo_maximo)
                except (ValueError, TypeError):
                    return Response(
                        {"error": "El cupo máximo debe ser un número entero"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            evento.save()
            
            # Preparar respuesta
            evento_serializado = EventoSerializer(evento).data
            evento_serializado["publico_objetivo"] = json.loads(evento_serializado["publico_objetivo"])
            
            return Response(evento_serializado, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Error al actualizar el evento: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, *args, **kwargs):
        try:
            evento_id = request.GET.get("id")
            if not evento_id:
                return Response(
                    {"error": "Se requiere el parámetro 'id'"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            evento = get_object_or_404(Evento, id=evento_id)
            evento.delete()
            
            return Response(
                {"success": "Evento eliminado correctamente"},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"error": f"Error al eliminar el evento: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)