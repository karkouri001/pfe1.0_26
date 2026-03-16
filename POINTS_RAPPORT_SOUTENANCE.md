# Points cles a citer dans le rapport (version finale)

Date de reference: 2026-03-16

## 1) Problematique et objectif

- Les examens de programmation etaient geres de maniere manuelle.
- Objectif: centraliser la gestion des examens, soumissions et corrections.
- Solution: plateforme web Django avec API REST, UI par role, et correction automatisable via webhook.

## 2) Choix techniques justifies

- Framework backend: Django + Django REST Framework.
- Auth sociale: `django-allauth` (Google).
- Base de donnees:
  - local equipe: MariaDB dans Docker
  - mode dev possible en SQLite selon `DEBUG`
- Administration BD: phpMyAdmin en conteneur.
- Separation claire:
  - `gestion` pour logique metier/API
  - `ui` pour interface web
  - `plateforme` pour configuration/projet

## 3) Architecture fonctionnelle

- Roles: `ETUDIANT`, `ENSEIGNANT`, `ADMIN`.
- Entites principales: `Profil`, `GroupeAcademique`, `Examen`, `Soumission`, `Resultat`.
- Relation critique:
  - 1 etudiant -> plusieurs soumissions
  - 1 soumission -> 1 resultat max
  - unicite `(examen, etudiant)` pour eviter double soumission

## 4) Regles metier importantes

- Examen:
  - PDF obligatoire si statut != `BROUILLON`
  - tests (`url_tests_git`, `hash_tests`) verrouilles apres publication
- Soumission:
  - code source ou depot Git obligatoire
  - etudiant doit etre dans un groupe autorise
  - soumission seulement dans la fenetre horaire
  - une seule soumission par etudiant/examen
- Resultat:
  - cree/mis a jour via webhook avec token

## 5) API REST (a mentionner)

Endpoints:

- `/api/examens/`
- `/api/groupes/`
- `/api/soumissions/`
- `/api/resultats/`
- `/api/webhook/resultats/`

Webhook:

- Header `X-API-TOKEN` obligatoire
- upsert du resultat + mise a jour statut de la soumission

## 6) OAuth Google (point sensible du projet)

- OAuth configure via `.env` (`GOOGLE_OAUTH_CLIENT_ID/SECRET`).
- Callback local:
  - `http://127.0.0.1:8000/accounts/google/login/callback/`
- Securisation appliquee:
  - connexion autorisee uniquement pour emails deja existants localement
  - creation sociale automatique bloquee (`SOCIALACCOUNT_AUTO_SIGNUP=False`)
- Si un utilisateur existe mais sans profil:
  - creation automatique d un profil `ETUDIANT`

## 7) Docker et administration BD

- Docker Compose lance:
  - `mariadb:11` (conteneur `pfe_db`)
  - `phpmyadmin/phpmyadmin` (conteneur `pfe_phpmyadmin`)
- Avantages cites:
  - environnement reproductible
  - pas d installation manuelle MySQL sur chaque poste
  - facilite travail en equipe
- Ports utilises:
  - BD: `3307` (hote) -> `3306` (conteneur)
  - phpMyAdmin: `8081`

## 8) Qualite, tests, validation

- Tests automatises Django executes et passes.
- Checks executes:
  - `manage.py check`
  - `manage.py makemigrations --check --dry-run`
  - `manage.py test --noinput`
- Securite basique ajoutee sur les entrees utilisateur:
  - rejet simple des balises HTML/JavaScript dans les champs texte affiches (`titre`, `description`, `feedback`, nom de groupe)
  - nettoyage des champs de recherche/filtres pour ne garder qu une saisie simple
  - taille maximale sur certains inputs web pour limiter les abus simples
- Securite HTTP basique activee dans Django:
  - cookies de session et CSRF en `HttpOnly`
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Referrer-Policy: same-origin`
- A mentionner comme limite connue:
  - warning MariaDB `models.W036` (non bloquant, specifique contraintes conditionnelles allauth)

## 9) Limites actuelles (a dire clairement)

- Certaines permissions API sont larges et meritent un durcissement fin (objet par objet) pour production stricte.
- `SERVE_STATIC_INSECURE=True` est utile localement, mais pas recommande en production.
- Dependance a des services externes (Google OAuth, GitHub) a surveiller.
- La protection XSS ajoutee reste volontairement basique: elle bloque surtout les cas evidents, sans moteur avance de sanitization HTML.

## 10) Pistes d amelioration

- Ajouter permissions objet plus strictes sur soumissions/resultats.
- Ajouter logs/audit plus detailles par action critique.
- Ajouter monitoring et alerting sur webhook de correction.
- Ajouter pipeline CI/CD backend (tests + lint) obligatoire avant merge.
- En production, ajouter une Content Security Policy plus stricte et un serveur web dedie (Nginx/Apache).

## 11) Mini script oral (structure de presentation)

- Contexte et probleme (30s)
- Architecture technique (1 min)
- Regles metier qui garantissent integrite et securite (1 min)
- Demo rapide du flux complet:
  - creation examen -> soumission -> webhook -> resultat (2 min)
- Qualite/validation/tests (30s)
- Limites + ameliorations (30s)

## 12) Questions probables du jury (et angle de reponse)

- Pourquoi Docker pour la BD?
  - reproductibilite, portabilite, onboarding rapide.
- Comment vous securisez OAuth?
  - emails locaux uniquement + pas d auto-signup social.
- Comment vous limitez SQL injection et XSS?
  - ORM Django donc pas de SQL brut dans les vues principales, validation simple des champs texte, echappement automatique des templates Django et quelques en-tetes HTTP.
- Comment eviter les doubles soumissions?
  - contrainte DB + validation serializer.
- Que se passe-t-il si le webhook est appele plusieurs fois?
  - `update_or_create` sur `Resultat` (idempotence fonctionnelle).
- Votre solution est-elle scalable?
  - oui avec durcissement permissions, cache, et externalisation service de correction.
