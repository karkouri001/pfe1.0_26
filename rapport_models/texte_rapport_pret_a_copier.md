# Texte pret a copier dans le rapport

## 1) Figure - Cas d utilisation

**Titre conseille:** "Diagramme des cas d utilisation de la plateforme d examens de programmation"

Le diagramme des cas d utilisation presente les interactions entre les acteurs (Etudiant, Enseignant, Admin) et le systeme.  
L etudiant consulte ses examens autorises, soumet son code et suit ses resultats.  
L enseignant cree, configure et publie les examens, puis suit soumissions et resultats.  
L admin dispose des memes capacites de gestion que l enseignant.  
Des services externes interviennent dans le flux: OAuth pour la connexion, GitHub pour le depot de solution et CI/CD pour la correction automatique via webhook.

## 2) Figure - MCD

**Titre conseille:** "MCD de la plateforme d examens"

Le MCD decrit les entites metier principales: Utilisateur, Profil, GroupeAcademique, Examen, Soumission, Resultat et JournalAudit.  
Les relations importantes sont: appartenance d un utilisateur a des groupes, association des groupes autorises a un examen, soumission d un etudiant a un examen, puis production eventuelle d un resultat.  
Ce modele met en evidence la regle centrale du systeme: une soumission unique par etudiant et par examen.

## 3) Figure - MLD

**Titre conseille:** "MLD relationnel de la plateforme"

Le MLD traduit le modele conceptuel en tables relationnelles avec cles primaires et etrangeres.  
Les tables de jointure `GROUPE_ACADEMIQUE_MEMBRES` et `EXAMEN_GROUPES_AUTORISES` implementent les relations plusieurs-a-plusieurs.  
Les contraintes d unicite principales sont: `profil.utilisateur_id`, `resultat.soumission_id`, `soumission.trace_id` et le couple `(soumission.examen_id, soumission.etudiant_id)`.

## 4) Figure - Diagramme de classes

**Titre conseille:** "Diagramme de classes metier et applicatif"

Le diagramme de classes montre la coherence entre la couche metier (models), la couche API (serializers/viewsets) et la couche UI (forms).  
Les classes `ExamenSerializer` et `SoumissionSerializer` portent les validations metier critiques (fenetre horaire, appartenance groupe, verrouillage des tests apres publication).  
La classe `ResultatWebhookAPIView` represente l integration avec la correction automatique.

## 5) Figure - Sequence cycle de vie examen

**Titre conseille:** "Sequence de creation et publication d un examen"

Cette sequence decrit la creation d un examen depuis l interface enseignant, la validation via `ExamenForm`, puis la publication via l API REST.  
Le diagramme montre explicitement la regle de blocage: les champs de tests ne sont plus modifiables apres la phase brouillon.

## 6) Figure - Sequence soumission et correction

**Titre conseille:** "Sequence de soumission et correction CI/CD"

Cette sequence couvre le flux de bout en bout: soumission etudiant, validations metier, push vers GitHub, execution des tests CI/CD, puis retour du resultat via webhook securise par token.  
La mise a jour finale cree ou met a jour `Resultat` et positionne le statut de `Soumission` a `CORRIGE` ou `ECHEC`.

## 7) Conclusion courte (optionnelle)

Ces modeles confirment une architecture separee en trois couches: donnees, logique applicative et presentation.  
Ils facilitent la maintenance du projet et permettent d expliquer clairement les regles metier dans un contexte academique.
