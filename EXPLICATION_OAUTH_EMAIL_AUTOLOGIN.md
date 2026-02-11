# Explication de la fonctionnalite OAuth + connexion automatique par email

## Objectif
Permettre a un utilisateur de se connecter automatiquement avec son email deja enregistre dans Django, sans saisir son mot de passe apres le retour OAuth.

## Fichiers modifies
- `ui/forms.py`
- `ui/views.py`
- `ui/urls.py`
- `ui/templates/ui/login.html`
- `plateforme/settings.py`
- `.env.example`
- `ui/tests.py`
- `README.md`

## Comment ca marche

### 1) Connexion classique amelioree (email ou username)
Dans `ui/forms.py`, un formulaire custom (`EmailOrUsernameAuthenticationForm`) accepte:
- un username classique
- ou un email

Si l utilisateur saisit un email:
- le systeme cherche un compte actif avec cet email
- si un seul compte est trouve, il convertit l email en username interne
- puis utilise l authentification Django normale

Resultat: la page `/connexion/` accepte maintenant email + mot de passe.

### 2) Endpoint d auto-login OAuth
Dans `ui/urls.py`, nouvelle route:
- `/connexion/oauth-email/`

Cette route appelle `OAuthEmailAutoLoginView` (dans `ui/views.py`).

Parametres attendus:
- `email` : email utilisateur
- `ts` : timestamp Unix
- `sig` : signature HMAC
- `next` (optionnel) : URL de redirection apres connexion

### 3) Verification de securite
Avant de connecter l utilisateur, `ui/views.py` verifie:
- que tous les parametres existent
- que le lien n est pas expire (`OAUTH_EMAIL_MAX_AGE_SECONDS`)
- que la signature est valide

Formule de signature:
- `sig = HMAC_SHA256_HEX(f"{email}:{ts}", OAUTH_EMAIL_AUTOLOGIN_SECRET)`

Si une verification echoue:
- pas de connexion
- message d erreur et redirection vers `/connexion/`

### 4) Connexion automatique
Si la signature est correcte:
- recherche d un utilisateur actif par email
- s il y a exactement 1 compte, `login()` Django est execute
- redirection vers `next` (si sur le meme host) ou vers `LOGIN_REDIRECT_URL`

Cas refuses:
- 0 compte pour cet email
- plus d un compte avec le meme email

### 5) Configuration requise
Dans `plateforme/settings.py` et `.env.example`:
- `OAUTH_EMAIL_AUTOLOGIN_SECRET` (obligatoire en production)
- `OAUTH_EMAIL_MAX_AGE_SECONDS` (defaut 300 secondes)

### 6) Tests ajoutes
`ui/tests.py` couvre:
- connexion classique avec email
- auto-login OAuth valide
- signature invalide
- lien expire

## Niveau de complexite
- Complexite globale: **moyenne**
- Pourquoi:
  - pas de migration DB necessaire
  - integration propre dans le flux Django existant
  - ajout de securite (HMAC + expiration + validation `next`)
  - tests automatises inclus

## Exemple de callback
Exemple URL:
`/connexion/oauth-email/?email=etudiant1@example.com&ts=1739300000&sig=<signature>`

Le service OAuth externe doit calculer `sig` avec le meme secret partage que ton application Django.
