from django.utils import timezone
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
        read_only_fields = ("cree_par",)

    def validate(self, attrs):
        instance = self.instance
        if instance and instance.statut != "BROUILLON":
            url_tests_git = attrs.get("url_tests_git", instance.url_tests_git)
            hash_tests = attrs.get("hash_tests", instance.hash_tests)
            if url_tests_git != instance.url_tests_git or hash_tests != instance.hash_tests:
                raise serializers.ValidationError(
                    "Les tests ne peuvent plus etre modifies apres publication."
                )
        return attrs


class SoumissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soumission
        fields = "__all__"
        read_only_fields = ("trace_id", "soumis_le", "etudiant")

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        examen = attrs.get("examen") or getattr(self.instance, "examen", None)
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Authentification requise.")
        if not examen:
            return attrs
        if not examen.groupes_autorises.filter(membres=user).exists():
            raise serializers.ValidationError(
                "Vous n'appartenez a aucun groupe autorise pour cet examen."
            )
        now = timezone.now()
        if now < examen.heure_debut or now > examen.heure_fin:
            raise serializers.ValidationError(
                "La soumission est autorisee uniquement pendant la plage horaire."
            )
        existing = Soumission.objects.filter(examen=examen, etudiant=user)
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise serializers.ValidationError(
                "Vous avez deja soumis pour cet examen."
            )
        return attrs


class ResultatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultat
        fields = "__all__"
        read_only_fields = ("corrige_le",)


class WebhookResultatSerializer(serializers.Serializer):
    soumission = serializers.PrimaryKeyRelatedField(
        queryset=Soumission.objects.all()
    )
    note = serializers.DecimalField(max_digits=5, decimal_places=2)
    feedback = serializers.CharField(allow_blank=True, required=False)
    statut_soumission = serializers.ChoiceField(choices=["CORRIGE", "ECHEC"])
