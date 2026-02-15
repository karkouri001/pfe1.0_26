# Guide: mettre a jour `WEBHOOK_URL` a chaque fois

Ce guide explique:
- ou trouver la nouvelle URL webhook
- quand il faut la changer
- ou la coller dans GitHub

## Pourquoi il faut la changer

Quand tu utilises un tunnel rapide (`cloudflared tunnel --url ...`), l URL publique `https://...trycloudflare.com` change a chaque nouveau lancement.

Donc a chaque redemarrage du tunnel, il faut mettre a jour le secret GitHub `WEBHOOK_URL`.

## 1) Lancer le backend Django

Dans un terminal:

```powershell
cd c:\Users\Lenovo\Desktop\PFE_DJ\pfe1.0_26
.\.venv\Scripts\python manage.py runserver 0.0.0.0:8000
```

Laisser ce terminal ouvert.

## 2) Lancer le tunnel et recuperer l URL

Dans un 2e terminal:

```powershell
c:\Users\Lenovo\Desktop\PFE_DJ\tools\cloudflared.exe tunnel --url http://127.0.0.1:8000 --no-autoupdate
```

Dans la sortie, chercher la ligne:

`Your quick Tunnel has been created! Visit it at ...`

Exemple:

`https://specialties-triangle-epic-neighborhood.trycloudflare.com`

## 3) Construire l URL webhook complete

Prendre l URL du tunnel et ajouter le chemin API:

`https://...trycloudflare.com/api/webhook/resultats/`

https://dense-hosts-stocks-out.trycloudflare.com/api/webhook/resultats/Exemple
final:

`https://specialties-triangle-epic-neighborhood.trycloudflare.com/api/webhook/resultats/`

## 4) Mettre a jour GitHub Secrets

Dans le repo `pffe2026-prog/submission`:

1. `Settings`
2. `Secrets and variables`
3. `Actions`
4. Ouvrir le secret `WEBHOOK_URL`
5. Remplacer par la nouvelle URL complete
6. Sauvegarder

## 5) Verifier `WEBHOOK_TOKEN`

Le secret `WEBHOOK_TOKEN` doit etre identique a `API_WEBHOOK_TOKEN` dans:

`pfe1.0_26/.env`

Important:
- `WEBHOOK_TOKEN` ne change pas a chaque tunnel (sauf si tu modifies `.env`).
- `WEBHOOK_URL` change a chaque redemarrage du tunnel rapide.

## 6) Tester rapidement

Faire une nouvelle soumission depuis l application.

Puis verifier:
- GitHub Actions du repo `submission`: job lance
- dans Django: la soumission passe de `EN_TEST` a `CORRIGE` ou `ECHEC`
- un `Resultat` est cree/mis a jour

## Erreurs frequentes

### `curl: Failed to connect to 127.0.0.1:8000`
Cause: `WEBHOOK_URL` pointe encore vers localhost dans GitHub secrets.  
Fix: utiliser l URL `https://...trycloudflare.com/api/webhook/resultats/`.

### `DisallowedHost` / HTTP 400
Cause: host tunnel non autorise Django.  
Fix: en dev, verifier la config `ALLOWED_HOSTS` dans `plateforme/settings.py`.

### Rien ne se passe dans CI
Cause possible: workflow mal place.  
Fix: verifier que le fichier est bien dans `.github/workflows/`.
