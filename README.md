# Plateforme d'examens (Django)

## Prerequis
- Python 3.x
- PowerShell

## Installation rapide
1. python -m venv .venv
2. .\.venv\Scripts\pip install -r requirements.txt
3. .\.venv\Scripts\python manage.py migrate
4. .\.venv\Scripts\python manage.py createsuperuser
5. .\.venv\Scripts\python manage.py runserver

## Acces
- Admin: http://127.0.0.1:8000/admin/
- API: http://127.0.0.1:8000/api/

## Endpoints REST
- /api/examens/
- /api/groupes/
- /api/soumissions/
- /api/resultats/
- /api/webhook/resultats/

## Superuser local (si besoin)
- utilisateur: admin
- mot de passe: admin1234

## Tests unitaires et CI/CD (resume)
- Tests BACKEND: dans `gestion/tests.py`, executes par `python manage.py test`.
- Tests de correction: par examen, fournis par l enseignant via `url_tests_git` (+ `hash_tests` optionnel).
- Flux: examen + url_tests_git -> soumission -> CI clone depot etudiant + repo tests -> execute -> webhook.

## Webhook CI/CD
Configurer le token via variable d environnement:
- PowerShell: `$env:API_WEBHOOK_TOKEN="mon-token"`

Exemple d appel:
```bash
curl -X POST http://127.0.0.1:8000/api/webhook/resultats/ \
  -H "Content-Type: application/json" \
  -H "X-API-TOKEN: mon-token" \
  -d "{\"soumission\": 1, \"note\": \"14.50\", \"feedback\": \"OK\", \"statut_soumission\": \"CORRIGE\"}"
```
