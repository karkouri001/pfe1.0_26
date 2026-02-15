# Problematique initiale et solution proposee

## Problematique initiale
- Les examens de programmation sont geres de facon manuelle (planification, autorisations par groupe, suivi des etudiants).
- Les depots des etudiants (URL Git + commit) ne sont pas centralises et la tracabilite est faible.
- La correction est lente et inegale sans automatisation des tests.
- Il manque un historique des actions (qui a fait quoi et quand).
- Les etudiants ont besoin de resultats et de feedback rapides.

## Solution proposee
- Mettre en place une plateforme web Django pour gerer tout le cycle des examens de programmation.
- Definir des roles clairs (admin, enseignant, etudiant) et des groupes academiques pour les autorisations.
- Gerer le cycle de vie d un examen (brouillon -> publie -> en_cours -> ferme).
- Centraliser les soumissions (url_depot_git + hash_commit) et associer un resultat a chaque soumission.
- Automatiser la correction via des tests fournis par l enseignant (repo de tests) executes par CI/CD.
- Recevoir les resultats via un webhook et mettre a jour la note, le feedback et le statut.
- Conserver un journal d audit des actions importantes.
- Exposer une API REST pour les operations CRUD et les integrations.
