# Plateforme d'examens (Django)

## Prerequis
- Python 3.x
- PowerShell

## Installation rapide
1. python -m venv .venv
2. .\.venv\Scripts\pip install -r requirements.txt
3. Configurer MySQL (voir section suivante)
4. .\.venv\Scripts\python manage.py makemigrations
5. .\.venv\Scripts\python manage.py migrate
6. .\.venv\Scripts\python manage.py createsuperuser
7. .\.venv\Scripts\python manage.py runserver

## Configuration MySQL
Creer la base (exemple simple) :
```sql
CREATE DATABASE plateforme_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Definir les variables d environnement (PowerShell) :
```powershell
$env:DB_NAME="plateforme_db"
$env:DB_USER="root"
$env:DB_PASSWORD=""
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
```

Vous pouvez aussi copier `.env.example` vers `.env` si vous utilisez un outil qui charge les variables d environnement.
Sur Windows, PyMySQL est utilise automatiquement si mysqlclient n est pas disponible.

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
