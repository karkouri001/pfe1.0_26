# Pourquoi ces tables "Comptes" et "Comptes sociaux" existent

Ce document explique pourquoi tu vois dans `/admin/` les sections:
- `Adresses e-mail`
- `Applications sociales`
- `Comptes sociaux`
- `Jetons de l'application sociale`

et d ou viennent les tables SQL associees.

## 1) Origine des tables

Ces tables viennent de la librairie `django-allauth` (pas de tes modeles `gestion`).

Dans ton projet, `allauth` est active dans `INSTALLED_APPS`:
- `allauth`
- `allauth.account`
- `allauth.socialaccount`
- `allauth.socialaccount.providers.google`

Donc quand tu fais `migrate`, Django cree automatiquement les tables `account_*` et `socialaccount_*`.

## 2) Correspondance Admin -> Modeles -> Tables

### A. Adresses e-mail
- Admin: `Adresses e-mail`
- Modele: `account.EmailAddress`
- Table: `account_emailaddress`
- Role:
  - lie un utilisateur Django a une adresse email
  - stocke si l email est verifie (`verified`)
  - stocke si c est l email principal (`primary`)

Champs principaux:
- `id`
- `user_id` (FK vers `auth_user`)
- `email`
- `verified`
- `primary`

Contraintes utiles:
- unicite `(user_id, email)` (pas 2 fois le meme email pour le meme user)
- unicite de l email verifie (selon migration allauth de ta version)

### B. (Interne) Confirmation email
- Admin: souvent pas central dans l usage courant
- Modele: `account.EmailConfirmation`
- Table: `account_emailconfirmation`
- Role:
  - stocke les confirmations email en attente / envoyees
  - permet de valider un email via une cle de confirmation

Champs principaux:
- `email_address_id` (FK vers `account_emailaddress`)
- `key` (cle de confirmation)
- `created`
- `sent`

### C. Applications sociales
- Admin: `Applications sociales`
- Modele: `socialaccount.SocialApp`
- Table: `socialaccount_socialapp`
- Role:
  - configuration OAuth du provider (Google, etc.)
  - contient `client_id`, `secret`, provider, settings
  - associee a un ou plusieurs sites Django (`django.contrib.sites`)

Champs principaux:
- `provider` (ex: `google`)
- `provider_id`
- `name`
- `client_id`
- `secret`
- `key`
- `settings` (JSON)

### D. Comptes sociaux
- Admin: `Comptes sociaux`
- Modele: `socialaccount.SocialAccount`
- Table: `socialaccount_socialaccount`
- Role:
  - lie un utilisateur local (`auth_user`) a un compte provider externe
  - ex: user Django <-> compte Google

Champs principaux:
- `user_id` (FK vers `auth_user`)
- `provider` (google, github, ...)
- `uid` (identifiant externe unique chez le provider)
- `last_login`
- `date_joined`
- `extra_data` (JSON profil provider)

Contrainte cle:
- unicite `(provider, uid)` (un compte provider ne peut pas etre lie 2 fois)

### E. Jetons de l'application sociale
- Admin: `Jetons de l'application sociale`
- Modele: `socialaccount.SocialToken`
- Table: `socialaccount_socialtoken`
- Role:
  - stocke token d acces OAuth (et parfois refresh/token_secret selon provider)
  - utilise pour appels API provider apres login (selon configuration)

Champs principaux:
- `app_id` (FK vers `socialaccount_socialapp`)
- `account_id` (FK vers `socialaccount_socialaccount`)
- `token`
- `token_secret`
- `expires_at`

### F. Table de liaison SocialApp <-> Site
- Modele technique M2M
- Table: `socialaccount_socialapp_sites`
- Role:
  - associe une app OAuth a un site Django (`site_id`)
  - important si plusieurs domaines/sites dans la meme base

## 3) A quoi ca sert concretement dans TON projet

Ton projet a:
- une connexion classique (`username` / `email` + mot de passe)
- un flux OAuth/auto-login email explique dans `EXPLICATION_OAUTH_EMAIL_AUTOLOGIN.md`
- un provider Google active dans settings

Donc ces tables servent a:
1. memoriser les emails et leur statut de verification
2. stocker la config OAuth Google (client ID / secret)
3. relier un user local a un compte Google
4. conserver les tokens OAuth necessaires selon les usages

## 4) Pourquoi elles apparaissent dans l admin Django

`django-allauth` enregistre ses modeles dans l admin.
Resultat: tu vois automatiquement les sections "Comptes" et "Comptes sociaux".

Ce comportement est normal et attendu.

## 5) Est-ce que c est obligatoire ?

Obligatoire si tu veux garder:
- login social (Google)
- gestion email/verification via allauth

Pas obligatoire si tu retires completement `allauth` du projet.

Attention: retirer `allauth` implique de:
- enlever les apps allauth de `INSTALLED_APPS`
- enlever backend/middleware allauth
- revoir les vues/templates qui en dependent
- gerer les migrations/tables existantes proprement

## 6) Commandes utiles de verification

Voir les migrations allauth appliquees:

```powershell
.\.venv\Scripts\python manage.py showmigrations account socialaccount
```

Lister les tables allauth presentes:

```powershell
.\.venv\Scripts\python manage.py shell -c "from django.db import connection; print('\n'.join([t for t in connection.introspection.table_names() if 'account' in t or 'social' in t]))"
```

## 7) Resume court

- Ces tables ne viennent pas de `gestion/models.py`.
- Elles viennent de `django-allauth`.
- Elles servent a la gestion email + OAuth social (Google).
- Leur presence dans l admin est normale.
