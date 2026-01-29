# PFE — Plateforme d’examens de programmation (Django)

## Contraintes
- Utiliser l’utilisateur Django par défaut (pas de CustomUser).
- Modèles et champs en français.
- Code simple (niveau PFE), pas de trucs avancés inutiles.

## Acteurs
- Étudiant
- Enseignant
- Admin

## Règles métier
- L’enseignant crée un examen (brouillon → publié → en_cours → fermé).
- L’enseignant dépose les tests unitaires de l’examen.
- Examens autorisés par groupes académiques.
- L’étudiant soumet : url_depot_git + hash_commit.
- Le système lance les tests et met à jour le statut.
- Résultat = note + feedback, lié à une soumission.
- Journal d’audit des actions importantes.

## Modèles
Profil(utilisateur OneToOne User, role ETUDIANT/ENSEIGNANT/ADMIN)
GroupeAcademique(nom, annee_academique, membres M2M User)
Examen(titre, description, heure_debut, heure_fin, statut BROUILLON/PUBLIE/EN_COURS/FERME, cree_par FK User, groupes_autorises M2M GroupeAcademique)
Soumission(trace_id UUID, examen FK Examen, etudiant FK User, url_depot_git, hash_commit, soumis_le, statut EN_ATTENTE/EN_TEST/CORRIGE/ECHEC, unique (examen, etudiant))
Resultat(OneToOne Soumission, note, feedback, corrige_le)
JournalAudit(utilisateur FK User nullable, action, horodatage)
