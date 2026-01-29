from rest_framework import serializers

from .models import Examen, GroupeAcademique, Resultat, Soumission


class GroupeAcademiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupeAcademique
        fields = "__all__"


class ExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examen
        fields = "__all__"


class SoumissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soumission
        fields = "__all__"
        read_only_fields = ("trace_id", "soumis_le")


class ResultatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultat
        fields = "__all__"
        read_only_fields = ("corrige_le",)
