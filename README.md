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

## Superuser local (si besoin)
- utilisateur: admin
- mot de passe: admin1234
