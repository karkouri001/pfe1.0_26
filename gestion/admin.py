from django.contrib import admin

from .models import (
    Examen,
    GroupeAcademique,
    JournalAudit,
    Profil,
    Resultat,
    Soumission,
)


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "role")
    search_fields = ("utilisateur__username",)


@admin.register(GroupeAcademique)
class GroupeAcademiqueAdmin(admin.ModelAdmin):
    list_display = ("nom", "annee_academique")
    search_fields = ("nom", "annee_academique")
    filter_horizontal = ("membres",)


@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    list_display = ("titre", "statut", "heure_debut", "heure_fin", "cree_par")
    list_filter = ("statut",)
    search_fields = ("titre", "cree_par__username")
    filter_horizontal = ("groupes_autorises",)


@admin.register(Soumission)
class SoumissionAdmin(admin.ModelAdmin):
    list_display = ("trace_id", "examen", "etudiant", "statut", "soumis_le")
    list_filter = ("statut",)
    search_fields = ("trace_id", "examen__titre", "etudiant__username")


@admin.register(Resultat)
class ResultatAdmin(admin.ModelAdmin):
    list_display = ("soumission", "note", "corrige_le")
    search_fields = ("soumission__trace_id",)


@admin.register(JournalAudit)
class JournalAuditAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "action", "horodatage")
    search_fields = ("utilisateur__username", "action")
