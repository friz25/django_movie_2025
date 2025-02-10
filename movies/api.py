"""
ViewSet - позволяет описывать методы, и к этим методам описывать http запросы с клиентской стороны
"""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Actor

from .serializers import (
    ActorListSelializer,
    ActorDetailSelializer,
)


class ActorViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Actor.objeects.all()
        serializer = ActorListSelializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Actor.objects.all()
        actor = get_object_or_404(queryset, pk=pk)
        serializer = ActorDetailSelializer(actor)
        return Response(serializer.data)