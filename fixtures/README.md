# Fixtures demo (sans secrets)

Objectif
- Partager des donnees de demo entre binomes sans dump SQL ni secrets.
- Les fixtures ne contiennent PAS d utilisateurs, mots de passe ou tokens.

Workflow rapide (binome)
1) Recuperer le code:
   - git pull
2) Creer la base et appliquer les migrations:
   - python manage.py migrate
3) Charger les donnees de demo:
   - python manage.py loaddata fixtures/demo.json
4) Creer un admin local:
   - python manage.py createsuperuser

Exporter des donnees de demo
- Windows:
  - scripts\export_demo.bat
- Linux/macOS:
  - scripts/export_demo.sh

Importer des donnees de demo
- Windows:
  - scripts\import_demo.bat
- Linux/macOS:
  - scripts/import_demo.sh

Commande utilisee (reference)
python manage.py dumpdata gestion --exclude auth --exclude contenttypes --exclude admin --exclude sessions --indent 2 > fixtures/demo.json
