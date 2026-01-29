from rest_framework import viewsets

from .models import Examen, GroupeAcademique, Resultat, Soumission
from .serializers import (
    ExamenSerializer,
    GroupeAcademiqueSerializer,
    ResultatSerializer,
    SoumissionSerializer,
)


class GroupeAcademiqueViewSet(viewsets.ModelViewSet):
    queryset = GroupeAcademique.objects.all()
    serializer_class = GroupeAcademiqueSerializer


class ExamenViewSet(viewsets.ModelViewSet):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer


class SoumissionViewSet(viewsets.ModelViewSet):
    queryset = Soumission.objects.all()
    serializer_class = SoumissionSerializer


class ResultatViewSet(viewsets.ModelViewSet):
    queryset = Resultat.objects.all()
    serializer_class = ResultatSerializer
