b# Documentation REST API (detaillee)

Objectif
Ce fichier explique, ligne par ligne, les parties REST API les plus importantes
du projet. Il est volontairement detaille pour l apprentissage.
Quand un fichier documente ici change, il faut mettre a jour la section
correspondante dans ce fichier.

Portee (scope)
- Detail line-by-line: REST API et pieces Django qui l exposent.
- Pas de repetition des bases Django (modele, admin, etc.).
- Les modeles ne sont pas modifies ici; on explique seulement comment
  les API les utilisent.

--------------------------------------------------------------------------------
Cours rapide REST API (debutant)

1) C est quoi une API ?
- Une API est une porte d entree pour que d autres logiciels puissent
  parler a ton application.
- Au lieu de cliquer dans un navigateur, un client envoie des requetes
  (HTTP) et recoit des reponses (JSON).

2) C est quoi REST ?
- REST = Representational State Transfer (style d architecture).
- Idee simple: on expose des "ressources" avec des URL propres.
  Exemple: /api/examens/ represente la ressource "examens".
- On utilise des verbes HTTP standards pour dire l action:
  - GET    -> lire
  - POST   -> creer
  - PUT    -> remplacer
  - PATCH  -> modifier partiellement
  - DELETE -> supprimer
- REST est "stateless": chaque requete contient tout ce qu il faut
  (pas de memoire serveur entre requetes).

3) Pourquoi REST est utile ?
- Standard connu par tous les outils (web, mobile, scripts).
- Simple a tester avec curl/Postman.
- Les permissions, validations et erreurs sont claires.

4) Requete HTTP = 4 blocs importants
- Methode: GET/POST/PUT/PATCH/DELETE
- URL: ex: /api/soumissions/
- Headers: infos techniques (ex: Content-Type, Authorization, X-API-TOKEN)
- Body: le JSON envoye (pour POST/PUT/PATCH)

5) Reponse HTTP = 2 parties
- Status code: ex 200, 201, 400, 401, 403, 404
- Body: JSON avec les donnees ou un message d erreur

6) Codes HTTP importants (memoriser)
- 200 OK: requete reussie
- 201 Created: objet cree
- 400 Bad Request: donnees invalides
- 401 Unauthorized: pas authentifie
- 403 Forbidden: authentifie mais pas autorise
- 404 Not Found: ressource inconnue

--------------------------------------------------------------------------------
REST dans Django (DRF) : les briques

DRF (Django REST Framework) structure l API en 4 couches principales:
1) Modeles (gestion/models.py)
   - La structure des donnees (tables).
2) Serializers (gestion/serializers.py)
   - Convertit un modele en JSON et valide le JSON entrant.
3) Views/ViewSets (gestion/views.py)
   - Recoit la requete, appelle le serializer, renvoie la reponse.
4) URLs/Router (gestion/urls.py, plateforme/urls.py)
   - Associe une URL a une vue.

Raccourci mental:
Client HTTP -> URL -> View/ViewSet -> Serializer -> Modele -> DB -> JSON

--------------------------------------------------------------------------------
REST dans ce projet (idee generale)

Objectif metier du projet:
- Gerer des examens (enseignant/admin).
- Laisser les etudiants soumettre leurs travaux.
- Recevoir des resultats via webhook (CI/CD).

Ressources exposees:
- examens: creation et gestion des examens
- groupes: groupes academiques autorises
- soumissions: travail remis par etudiants
- resultats: note/feedback d une soumission
- webhook/resultats: point d entree automatique depuis la CI/CD

Raisons des regles d acces:
- Un etudiant ne doit voir que les examens publies de ses groupes.
- Un etudiant ne peut soumettre qu une seule fois par examen.
- Les resultats sont sensibles: seules les personnes autorisees
  peuvent les modifier.
- Le webhook doit etre protege par un token partage.

--------------------------------------------------------------------------------
Exemples concrets (simplifies)

1) Lister les examens (lecture)
Requete:
GET /api/examens/
Reponse possible:
200 OK
[
  {"id": 1, "titre": "...", "statut": "PUBLIE", ...},
  {"id": 2, "titre": "...", "statut": "EN_COURS", ...}
]

2) Creer un examen (enseignant/admin)
Requete:
POST /api/examens/
Body JSON (exemple):
{
  "titre": "Algo 1",
  "description": "Examen sur les graphes",
  "heure_debut": "2026-02-10T09:00:00Z",
  "heure_fin": "2026-02-10T12:00:00Z",
  "statut": "BROUILLON",
  "url_tests_git": "https://...",
  "hash_tests": "abc123",
  "groupes_autorises": [1, 2]
}
Reponse:
201 Created
{ ... objet cree ... }
Note: le champ cree_par n est pas dans le body, il est rempli par la vue.

3) Soumettre un projet (etudiant)
Requete:
POST /api/soumissions/
Body JSON:
{
  "examen": 1,
  "code_source": "print('hello')",
  "url_depot_git": "https://...",
  "hash_commit": "ff00aa"
}
Reponse:
201 Created
{ ... soumission creee ... }
Erreurs possibles:
- 400 si pas dans le groupe autorise (validation serializer)
- 400 si hors delai
- 400 si deja soumis

4) Webhook resultat (CI/CD)
Requete:
POST /api/webhook/resultats/
Headers:
X-API-TOKEN: <ton_token>
Body JSON:
{
  "soumission": 10,
  "note": "14.50",
  "feedback": "OK",
  "statut_soumission": "CORRIGE"
}
Reponse:
200 OK ou 201 Created
{
  "resultat_id": 5,
  "soumission": 10,
  "statut": "CORRIGE"
}

--------------------------------------------------------------------------------
Carte rapide des endpoints REST

Base: /api/
- /api/examens/          -> ExamenViewSet (CRUD)
- /api/groupes/          -> GroupeAcademiqueViewSet (CRUD)
- /api/soumissions/      -> SoumissionViewSet (CRUD)
- /api/resultats/        -> ResultatViewSet (CRUD)
- /api/webhook/resultats/-> ResultatWebhookAPIView (POST only)

Regles d acces (resume):
- Groupes: pas de permission explicite ici -> utilise la config DRF globale
  (AllowAny par defaut).
- Examens: authentifie + enseignant/admin pour les ecritures.
- Soumissions: authentifie.
- Resultats: authentifie + enseignant/admin pour les ecritures.
- Webhook: AllowAny mais protege par X-API-TOKEN.

--------------------------------------------------------------------------------
gestion/serializers.py (explication ligne par ligne)

L1  `from django.utils import timezone`
    Utilise pour verifier l heure courante lors d une soumission.
L2  `from rest_framework import serializers`
    Importe les classes DRF pour definir les serializers.
L3  (ligne vide)
    Separation logique des imports.
L4  `from .models import Examen, GroupeAcademique, Resultat, Soumission`
    Les serializers se basent sur ces modeles Django.

L7  `class GroupeAcademiqueSerializer(serializers.ModelSerializer):`
    Serializer automatique base sur le modele GroupeAcademique.
L8  `class Meta:`
    Configuration interne du serializer.
L9  `model = GroupeAcademique`
    Lie le serializer au modele.
L10 `fields = "__all__"`
    Expose tous les champs du modele dans l API.

L13 `class ExamenSerializer(serializers.ModelSerializer):`
    Serializer pour Examen, avec une validation metier specifique.
L14 `class Meta:`
    Meta du serializer.
L15 `model = Examen`
    Modele cible.
L16 `fields = "__all__"`
    Tous les champs sont exposes.
L17 `read_only_fields = ("cree_par",)`
    Champ cree_par en lecture seule: il est rempli automatiquement
    dans la vue (perform_create).

L19 `def validate(self, attrs):`
    Validation globale de l objet Examen.
L20 `instance = self.instance`
    Si instance existe, on est en modification (update).
L21 `if instance and instance.statut != "BROUILLON":`
    Si examen deja publie/en cours/ferme, on bloque certains champs.
L22 `url_tests_git = attrs.get("url_tests_git", instance.url_tests_git)`
    Nouveau ou ancien url des tests.
L23 `hash_tests = attrs.get("hash_tests", instance.hash_tests)`
    Nouveau ou ancien hash des tests.
L24 `if url_tests_git != instance.url_tests_git or hash_tests != instance.hash_tests:`
    Si l un des champs tests change apres publication -> erreur.
L25 `raise serializers.ValidationError(...)`
    Message clair pour l utilisateur API.
L28 `return attrs`
    Si tout est ok, on valide les donnees.

L31 `class SoumissionSerializer(serializers.ModelSerializer):`
    Serializer pour Soumission avec validation d acces.
L32 `class Me ta:`
    Meta du serializer.
L33 `model = Soumission`
    Modele cible.
L34 `fields = "__all__"`
    Tous les champs exposes.
L35 `read_only_fields = ("trace_id", "soumis_le", "etudiant")`
    Champs remplis automatiquement:
    - trace_id: UUID auto
    - soumis_le: timestamp auto
    - etudiant: rempli par la vue

L37 `def validate(self, attrs):`
    Validation globale de la soumission.
L38 `request = self.context.get("request")`
    Le serializer accede a la requete pour connaitre l utilisateur.
L39 `user = getattr(request, "user", None)`
    Recuperation safe de l utilisateur.
L40 `examen = attrs.get("examen") or getattr(self.instance, "examen", None)`
    Recupere l examen (nouveau ou existant).
L41 `if not user or not user.is_authenticated:`
    Interdit une soumission anonyme.
L42 `raise serializers.ValidationError("Authentification requise.")`
    Message d erreur clair.
L43 `code_source = (attrs.get("code_source") or "").strip()`
    Recuperation du code source (si fourni).
L44 `url_depot_git = (attrs.get("url_depot_git") or "").strip()`
    Recuperation du depot Git (si fourni).
L45 `if not code_source and not url_depot_git:`
    Exige soit un code source, soit un depot Git.
L46 `raise serializers.ValidationError(...)`
    Message d erreur si aucun contenu fourni.
L43 `if not examen:`
    Si aucun examen fourni (cas limite), on valide sans control.
L44 `return attrs`
    Retour simple.
L45 `if not examen.groupes_autorises.filter(membres=user).exists():`
    Verifie que l etudiant appartient a un groupe autorise.
L46 `raise serializers.ValidationError(...)`
    Refus si l etudiant n est pas dans les groupes autorises.
L49 `now = timezone.now()`
    Heure courante.
L50 `if now < examen.heure_debut or now > examen.heure_fin:`
    Controle de la fenetre autorisee.
L51 `raise serializers.ValidationError(...)`
    Interdit une soumission hors delai.
L54 `existing = Soumission.objects.filter(examen=examen, etudiant=user)`
    Cherche une soumission deja existante pour cet etudiant/examen.
L55 `if self.instance:`
    Si update, on evite de compter soi-meme.
L56 `existing = existing.exclude(pk=self.instance.pk)`
    Exclut la soumission courante.
L57 `if existing.exists():`
    Si deja soumis, on bloque.
L58 `raise serializers.ValidationError(...)`
    Message d erreur.
L60 `return attrs`
    Donnees validees.

L63 `class ResultatSerializer(serializers.ModelSerializer):`
    Serializer pour Resultat.
L64 `class Meta:`
    Meta du serializer.
L65 `model = Resultat`
    Modele cible.
L66 `fields = "__all__"`
    Tous les champs exposes.
L67 `read_only_fields = ("corrige_le",)`
    corrige_le est auto (timestamp).

L70 `class WebhookResultatSerializer(serializers.Serializer):`
    Serializer "manuel" pour le webhook (pas un ModelSerializer direct).
L71 `soumission = serializers.PrimaryKeyRelatedField(queryset=Soumission.objects.all())`
    Le webhook envoie l id d une soumission existante.
L73 `note = serializers.DecimalField(max_digits=5, decimal_places=2)`
    Note avec 2 decimales.
L74 `feedback = serializers.CharField(allow_blank=True, required=False)`
    Champ facultatif, accepte une chaine vide.
L75 `statut_soumission = serializers.ChoiceField(choices=["CORRIGE", "ECHEC"])`
    Statut attendu apres correction.

--------------------------------------------------------------------------------
gestion/permissions.py (explication ligne par ligne)

L1  `from rest_framework.permissions import BasePermission, SAFE_METHODS`
    BasePermission pour creer une permission custom.
    SAFE_METHODS = GET, HEAD, OPTIONS (lecture).

L4  `class IsEnseignantOrAdmin(BasePermission):`
    Permission pour autoriser uniquement enseignants/admin en ecriture.
L5  `def has_permission(self, request, view):`
    Methode appelee par DRF pour chaque requete.
L6  `if request.method in SAFE_METHODS:`
    Pour la lecture, autoriser sans restriction.
L7  `return True`
    Lecture autorisee.
L8  `profil = getattr(request.user, "profil", None)`
    Recupere le profil associe a l utilisateur.
L9  `return bool(profil and profil.role in ("ENSEIGNANT", "ADMIN"))`
    Autorise uniquement si role enseignant/admin.

L12 `class IsResultatEditor(BasePermission):`
    Permission equivalente pour les Resultats.
L13 `def has_permission(self, request, view):`
    Meme logique que ci-dessus.
L14 `if request.method in SAFE_METHODS:`
    Lecture autorisee.
L15 `return True`
    Lecture autorisee.
L16 `profil = getattr(request.user, "profil", None)`
    Profil utilisateur.
L17 `return bool(profil and profil.role in ("ENSEIGNANT", "ADMIN"))`
    Ecriture reservee enseignant/admin.

--------------------------------------------------------------------------------
gestion/views.py (explication ligne par ligne)

L1  `from django.conf import settings`
    Acces aux settings (token webhook).
L2  `from rest_framework import status, viewsets`
    status pour codes HTTP, viewsets pour CRUD automatique.
L3  `from rest_framework.permissions import AllowAny, IsAuthenticated`
    Permissions DRF pretes a l emploi.
L4  `from rest_framework.response import Response`
    Reponses JSON DRF.
L5  `from rest_framework.views import APIView`
    Vue de base pour endpoint custom (webhook).

L7  `from .models import Examen, GroupeAcademique, Resultat, Soumission`
    Modeles utilises par les API.
L8  `from .permissions import IsEnseignantOrAdmin, IsResultatEditor`
    Permissions custom.
L9  `from .serializers import (...)`
    Serializers pour convertir objets <-> JSON et valider.

L16 `class GroupeAcademiqueViewSet(viewsets.ModelViewSet):`
    CRUD complet automatiquement (list, retrieve, create, update, delete).
L17 `queryset = GroupeAcademique.objects.all()`
    Toutes les lignes GroupeAcademique.
L18 `serializer_class = GroupeAcademiqueSerializer`
    Serializer utilise pour JSON <-> modele.

L21 `class ExamenViewSet(viewsets.ModelViewSet):`
    CRUD complet pour Examen.
L22 `queryset = Examen.objects.all()`
    Base de la requete.
L23 `serializer_class = ExamenSerializer`
    Serializer Examen.
L24 `permission_classes = [IsAuthenticated, IsEnseignantOrAdmin]`
    - Auth obligatoire pour tout.
    - Ecritures reservees enseignant/admin.

L26 `def get_queryset(self):`   
    Customise les examens visibles selon le role.
L27 `queryset = super().get_queryset()`
    Commence avec la requete de base.
L28 `profil = getattr(self.request.user, "profil", None)`
    Profil de l utilisateur.
L29 `if profil and profil.role == "ETUDIANT":`
    Pour un etudiant, filtrer les examens visibles.
L30 `return queryset.filter(...).distinct()`
    Filtre: examens publies/en cours et appartenant a un groupe autorise.
L35 `return queryset`
    Pour enseignants/admin, pas de filtre supplementaire.

L37 `def perform_create(self, serializer):`
    Hook DRF appele lors de la creation.
L38 `serializer.save(cree_par=self.request.user)`
    Fixe automatiquement le createur.

L41 `class SoumissionViewSet(viewsets.ModelViewSet):`
    CRUD pour Soumission.
L42 `queryset = Soumission.objects.all()`
    Base.
L43 `serializer_class = SoumissionSerializer`
    Serializer de soumission.
L44 `permission_classes = [IsAuthenticated]`
    Auth obligatoire (pas d anon).

L46 `def perform_create(self, serializer):`
    Hook de creation.
L47 `serializer.save(etudiant=self.request.user)`
    L etudiant est force par la session, pas par le client.

L50 `class ResultatViewSet(viewsets.ModelViewSet):`
    CRUD pour Resultat.
L51 `queryset = Resultat.objects.all()`
    Base.
L52 `serializer_class = ResultatSerializer`
    Serializer Resultat.
L53 `permission_classes = [IsAuthenticated, IsResultatEditor]`
    Lecture pour tous les authentifies, ecriture enseignant/admin.

L56 `class ResultatWebhookAPIView(APIView):`
    Endpoint special pour recevoir des resultats depuis CI/CD.
L57 `permission_classes = [AllowAny]`
    Pas d auth classique, mais un token est verifie manuellement.

L59 `def post(self, request):`
    Seule methode autorisee: POST.
L60 `token = request.headers.get("X-API-TOKEN")`
    Lecture du header secret.
L61 `if token != settings.API_WEBHOOK_TOKEN:`
    Comparaison avec le token configure.
L62 `return Response(..., status=status.HTTP_403_FORBIDDEN)`
    Refus si token invalide.
L63 `serializer = WebhookResultatSerializer(data=request.data)`
    Validation des donnees recues.
L64 `serializer.is_valid(raise_exception=True)`
    En cas d erreur, DRF renvoie un 400 automatique.
L65 `soumission = serializer.validated_data["soumission"]`
    Soumission cible.
L66 `resultat, created = Resultat.objects.update_or_create(... )`
    Cree le resultat s il n existe pas, sinon met a jour la note/feedback.
L71 `soumission.statut = serializer.validated_data["statut_soumission"]`
    Mise a jour du statut de la soumission.
L72 `soumission.save(update_fields=["statut"])`
    Sauvegarde rapide (champ specifique).
L73 `return Response({...}, status=...)`
    Retourne un JSON clair avec ids et statut.
L79 `status=status.HTTP_201_CREATED if created else status.HTTP_200_OK`
    201 si creation, 200 si mise a jour.

--------------------------------------------------------------------------------
gestion/urls.py (explication ligne par ligne)

L1  `from django.urls import include, path`
    Fonctions Django pour les routes.
L2  `from rest_framework.routers import DefaultRouter`
    Routeur DRF qui genere les routes CRUD des ViewSets.

L4  `from .views import (...)`
    Import des ViewSets et de la vue webhook.

L11 `router = DefaultRouter()`
    Instance du routeur.
L12 `router.register("examens", ExamenViewSet)`
    Cree automatiquement /api/examens/ et /api/examens/<id>/.
L13 `router.register("groupes", GroupeAcademiqueViewSet)`
    Cree /api/groupes/ et /api/groupes/<id>/.
L14 `router.register("soumissions", SoumissionViewSet)`
    Cree /api/soumissions/ et /api/soumissions/<id>/.
L15 `router.register("resultats", ResultatViewSet)`
    Cree /api/resultats/ et /api/resultats/<id>/.

L17 `urlpatterns = [`
    Liste des routes de l app.
L18 `path("", include(router.urls)),`
    Ajoute toutes les routes auto generees par le routeur.
L19 `path("webhook/resultats/", ResultatWebhookAPIView.as_view()),`
    Ajoute le endpoint custom du webhook.
L20 `]`
    Fin de la liste.

--------------------------------------------------------------------------------
plateforme/urls.py (explication ligne par ligne utile pour l API)

L1-L16  Bloc de commentaire Django par defaut.
        Pas critique pour la logique REST.
L17 `from django.contrib import admin`
    Admin Django.
L18 `from django.http import HttpResponse`
    Reponse HTTP simple pour la page d accueil.
L19 `from django.urls import include, path`
    Fonctions de routing.

L22 `def accueil(request):`
    Vue simple pour la racine du site.
L23 `return HttpResponse("Bienvenue sur la plateforme.")`
    Message de test.

L25 `urlpatterns = [`
    Liste des routes principales.
L26 `path('', accueil),`
    Racine du site -> accueil.
L27 `path('admin/', admin.site.urls),`
    Admin Django.
L28 `path('api/', include('gestion.urls')),`
    Toutes les routes REST sont sous /api/.
L29 `]`
    Fin.

--------------------------------------------------------------------------------
Flux REST important (vue d ensemble)

1) Creation d un examen (enseignant/admin)
- Requete POST /api/examens/
- Permissions: IsAuthenticated + IsEnseignantOrAdmin
- Serializer Examen: cree_par est force par la vue (perform_create)

2) Soumission d un etudiant
- POST /api/soumissions/
- Permissions: IsAuthenticated
- Serializer Soumission valide:
  - utilisateur authentifie
  - appartient a un groupe autorise
  - periode autorisee
  - une seule soumission par etudiant/examen
- La vue force le champ etudiant.

3) Reception de resultats par webhook
- POST /api/webhook/resultats/ avec header X-API-TOKEN
- Validation: WebhookResultatSerializer
- Creation ou mise a jour de Resultat
- Mise a jour du statut de la Soumission

--------------------------------------------------------------------------------
Checklist de mise a jour (a garder synchronise)

Quand tu modifies:
- gestion/views.py        -> mettre a jour la section correspondante
- gestion/serializers.py  -> mettre a jour la section correspondante
- gestion/permissions.py  -> mettre a jour la section correspondante
- gestion/urls.py         -> mettre a jour la section correspondante
- plateforme/urls.py      -> mettre a jour la section correspondante
