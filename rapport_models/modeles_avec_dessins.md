# Modeles Avec Dessins

Ce document garde les modeles et ajoute directement le dessin sous chaque modele.
Tu peux copier-coller chaque section dans ton rapport.

## 1) Modele des cas d utilisation

### Description courte
Ce modele montre les acteurs (Etudiant, Enseignant, Admin) et les interactions principales avec la plateforme, GitHub, OAuth et CI/CD.

### Dessin
```mermaid
flowchart LR
    Etudiant[Acteur Etudiant]
    Enseignant[Acteur Enseignant]
    Admin[Acteur Admin]
    OAuth[Service OAuth]
    GitHub[Service GitHub]
    CICD[Service CI/CD]

    subgraph Plateforme["Systeme: Plateforme d examens de programmation"]
        UC_Login((Se connecter username/email))
        UC_OAuthLink((Auto-login via lien signe))
        UC_Logout((Se deconnecter))

        UC_ExamList((Lister examens autorises))
        UC_ExamDetail((Voir detail examen + PDF))
        UC_Submit((Soumettre code source))
        UC_Track((Suivre statut soumission))
        UC_ViewStudentResults((Consulter ses resultats))

        UC_CreateExam((Creer examen))
        UC_EditExam((Modifier examen))
        UC_AssignGroups((Associer groupes autorises))
        UC_ConfigTests((Configurer tests Git))
        UC_PublishExam((Publier examen))
        UC_CloseExam((Fermer examen))
        UC_ViewTeacherSubs((Consulter soumissions))
        UC_ViewTeacherResults((Consulter resultats))

        UC_GitPush((Pousser solution vers GitHub))
        UC_RunTests((Executer pipeline tests))
        UC_Webhook((Poster webhook resultat))
        UC_ApplyResult((MAJ Resultat + statut Soumission))
    end

    Etudiant --> UC_Login
    Etudiant --> UC_OAuthLink
    Etudiant --> UC_Logout
    Etudiant --> UC_ExamList
    Etudiant --> UC_ExamDetail
    Etudiant --> UC_Submit
    Etudiant --> UC_Track
    Etudiant --> UC_ViewStudentResults

    Enseignant --> UC_Login
    Enseignant --> UC_CreateExam
    Enseignant --> UC_EditExam
    Enseignant --> UC_AssignGroups
    Enseignant --> UC_ConfigTests
    Enseignant --> UC_PublishExam
    Enseignant --> UC_CloseExam
    Enseignant --> UC_ViewTeacherSubs
    Enseignant --> UC_ViewTeacherResults

    Admin --> UC_Login
    Admin --> UC_CreateExam
    Admin --> UC_EditExam
    Admin --> UC_AssignGroups
    Admin --> UC_ConfigTests
    Admin --> UC_PublishExam
    Admin --> UC_CloseExam
    Admin --> UC_ViewTeacherSubs
    Admin --> UC_ViewTeacherResults

    OAuth --> UC_OAuthLink
    GitHub --> UC_GitPush
    CICD --> UC_RunTests
    CICD --> UC_Webhook

    UC_OAuthLink -. include .-> UC_Login
    UC_Submit -. include .-> UC_GitPush
    UC_GitPush -. trigger .-> UC_RunTests
    UC_RunTests -. include .-> UC_Webhook
    UC_Webhook -. include .-> UC_ApplyResult
    UC_ViewStudentResults -. depend .-> UC_ApplyResult
    UC_ViewTeacherResults -. depend .-> UC_ApplyResult
    UC_CreateExam -. include .-> UC_AssignGroups
    UC_CreateExam -. include .-> UC_ConfigTests
```

**Image PNG (pret a inserer):**  
![Cas d utilisation](./use_cases.png)

**Version vectorielle:** [use_cases.svg](./use_cases.svg)

## 2) MCD (modele conceptuel de donnees)

### Description courte
Le MCD presente les entites metier et leurs relations, sans details SQL.

### Dessin
```mermaid
erDiagram
    UTILISATEUR {
        INT id
        STRING username
        STRING email
        BOOL is_active
    }

    PROFIL {
        INT id
        ENUM role "ETUDIANT|ENSEIGNANT|ADMIN"
    }

    GROUPE_ACADEMIQUE {
        INT id
        STRING nom
        STRING annee_academique
    }

    EXAMEN {
        INT id
        STRING titre
        TEXT description
        DATETIME heure_debut
        DATETIME heure_fin
        ENUM statut "BROUILLON|PUBLIE|EN_COURS|FERME"
        STRING url_tests_git
        STRING hash_tests
        STRING pdf_examen
    }

    SOUMISSION {
        INT id
        UUID trace_id
        DATETIME soumis_le
        ENUM statut "EN_ATTENTE|EN_TEST|CORRIGE|ECHEC"
        TEXT code_source
        STRING url_depot_git
        STRING hash_commit
    }

    RESULTAT {
        INT id
        DECIMAL note
        TEXT feedback
        DATETIME corrige_le
    }

    JOURNAL_AUDIT {
        INT id
        STRING action
        DATETIME horodatage
    }

    UTILISATEUR ||--o| PROFIL : "possede"
    UTILISATEUR }o--o{ GROUPE_ACADEMIQUE : "appartient_a"
    UTILISATEUR ||--o{ EXAMEN : "cree"
    EXAMEN }o--o{ GROUPE_ACADEMIQUE : "autorise_pour"
    EXAMEN ||--o{ SOUMISSION : "recoit"
    UTILISATEUR ||--o{ SOUMISSION : "depose"
    SOUMISSION ||--o| RESULTAT : "produit"
    UTILISATEUR ||--o{ JOURNAL_AUDIT : "declenche"
```

**Image PNG (pret a inserer):**  
![MCD](./mcd.png)

**Version vectorielle:** [mcd.svg](./mcd.svg)

## 3) MLD (modele logique de donnees)

### Description courte
Le MLD detaille les tables, cles primaires, cles etrangeres et contraintes.

### Dessin
```mermaid
erDiagram
    AUTH_USER {
        BIGINT id PK
        VARCHAR username UK
        VARCHAR email
        BOOLEAN is_active
        DATETIME last_login
        DATETIME date_joined
    }

    PROFIL {
        BIGINT id PK
        BIGINT utilisateur_id FK_UK
        ENUM role "ETUDIANT|ENSEIGNANT|ADMIN"
    }

    GROUPE_ACADEMIQUE {
        BIGINT id PK
        VARCHAR nom
        VARCHAR annee_academique
    }

    GROUPE_ACADEMIQUE_MEMBRES {
        BIGINT id PK
        BIGINT groupeacademique_id FK
        BIGINT user_id FK
    }

    EXAMEN {
        BIGINT id PK
        VARCHAR titre
        TEXT description
        DATETIME heure_debut
        DATETIME heure_fin
        ENUM statut "BROUILLON|PUBLIE|EN_COURS|FERME"
        BIGINT cree_par_id FK
        VARCHAR url_tests_git NULL
        CHAR hash_tests_40
        VARCHAR pdf_examen NULL
    }

    EXAMEN_GROUPES_AUTORISES {
        BIGINT id PK
        BIGINT examen_id FK
        BIGINT groupeacademique_id FK
    }

    SOUMISSION {
        BIGINT id PK
        UUID trace_id UK
        BIGINT examen_id FK
        BIGINT etudiant_id FK
        VARCHAR url_depot_git NULL
        VARCHAR hash_commit
        TEXT code_source
        DATETIME soumis_le
        ENUM statut "EN_ATTENTE|EN_TEST|CORRIGE|ECHEC"
    }

    RESULTAT {
        BIGINT id PK
        BIGINT soumission_id FK_UK
        DECIMAL note_5_2
        TEXT feedback
        DATETIME corrige_le
    }

    JOURNAL_AUDIT {
        BIGINT id PK
        BIGINT utilisateur_id FK_NULL
        VARCHAR action
        DATETIME horodatage
    }

    AUTH_USER ||--o| PROFIL : "profil applicatif"
    AUTH_USER ||--o{ GROUPE_ACADEMIQUE_MEMBRES : "membre"
    GROUPE_ACADEMIQUE ||--o{ GROUPE_ACADEMIQUE_MEMBRES : "contient"
    AUTH_USER ||--o{ EXAMEN : "cree"
    EXAMEN ||--o{ EXAMEN_GROUPES_AUTORISES : "autorise"
    GROUPE_ACADEMIQUE ||--o{ EXAMEN_GROUPES_AUTORISES : "est_cible"
    EXAMEN ||--o{ SOUMISSION : "recoit"
    AUTH_USER ||--o{ SOUMISSION : "depose"
    SOUMISSION ||--o| RESULTAT : "corrigee_par"
    AUTH_USER ||--o{ JOURNAL_AUDIT : "actions"
```

**Image PNG (pret a inserer):**  
![MLD](./mld.png)

**Version vectorielle:** [mld.svg](./mld.svg)

## 4) Diagramme de classes

### Description courte
Ce diagramme relie classes metier (models), API (serializers/viewsets) et UI (forms).

### Dessin
```mermaid
classDiagram
    direction LR

    class User {
        +id: bigint
        +username: str
        +email: str
        +is_active: bool
    }
    class Profil { +role: Role }
    class GroupeAcademique { +nom: str +annee_academique: str }
    class Examen {
        +titre: str
        +heure_debut: datetime
        +heure_fin: datetime
        +statut: StatutExamen
    }
    class Soumission {
        +trace_id: uuid
        +soumis_le: datetime
        +statut: StatutSoumission
    }
    class Resultat { +note: decimal +corrige_le: datetime }
    class JournalAudit { +action: str +horodatage: datetime }

    class ExamenSerializer { +validate(attrs) }
    class SoumissionSerializer { +validate(attrs) }
    class ResultatSerializer
    class WebhookResultatSerializer

    class ExamenViewSet { +get_queryset() +perform_create(serializer) }
    class SoumissionViewSet { +perform_create(serializer) }
    class ResultatViewSet
    class ResultatWebhookAPIView { +post(request) }

    class ExamenForm { +clean() }
    class EmailOrUsernameAuthenticationForm { +clean() }

    class Role {
        <<Enumeration>>
        ETUDIANT
        ENSEIGNANT
        ADMIN
    }
    class StatutExamen {
        <<Enumeration>>
        BROUILLON
        PUBLIE
        EN_COURS
        FERME
    }
    class StatutSoumission {
        <<Enumeration>>
        EN_ATTENTE
        EN_TEST
        CORRIGE
        ECHEC
    }

    User "1" --> "0..1" Profil
    Profil --> Role
    User "0..*" --> "0..*" GroupeAcademique
    User "1" --> "0..*" Examen : cree
    Examen --> StatutExamen
    Examen "0..*" --> "0..*" GroupeAcademique
    Examen "1" --> "0..*" Soumission
    User "1" --> "0..*" Soumission
    Soumission --> StatutSoumission
    Soumission "1" --> "0..1" Resultat
    User "0..1" --> "0..*" JournalAudit

    ExamenSerializer --> Examen
    SoumissionSerializer --> Soumission
    ResultatSerializer --> Resultat
    WebhookResultatSerializer --> Soumission
    ExamenViewSet --> ExamenSerializer
    SoumissionViewSet --> SoumissionSerializer
    ResultatViewSet --> ResultatSerializer
    ResultatWebhookAPIView --> WebhookResultatSerializer
    ExamenForm --> Examen
    EmailOrUsernameAuthenticationForm --> User
```

**Image PNG (pret a inserer):**  
![Diagramme de classes](./class_diagram.png)

**Version vectorielle:** [class_diagram.svg](./class_diagram.svg)

## 5) Diagramme de sequence - cycle examen

### Description courte
Ce diagramme montre creation, validation, publication et suivi d un examen.

### Dessin
```mermaid
sequenceDiagram
    autonumber
    actor Enseignant
    actor Admin
    participant UI as UI Django (enseignant_examen_nouveau/detail)
    participant Auth as Controle Auth/Role
    participant Form as ExamenForm
    participant API as ExamenViewSet (REST)
    participant Ser as ExamenSerializer
    participant DB as Base de donnees

    Enseignant->>UI: POST creation examen (statut BROUILLON)
    UI->>Auth: verifier role ENSEIGNANT|ADMIN
    Auth-->>UI: autorise
    UI->>Form: clean(titre, dates, pdf, tests, groupes)

    alt Form invalide
        Form-->>UI: erreurs validation
        UI-->>Enseignant: afficher erreurs
    else Form valide
        UI->>DB: create Examen + save m2m groupes
        DB-->>UI: examen cree
        UI-->>Enseignant: confirmation
    end

    Admin->>API: PATCH /api/examens/{id} statut=PUBLIE
    API->>Auth: IsAuthenticated + IsEnseignantOrAdmin
    Auth-->>API: autorise
    API->>Ser: validate(instance, attrs)

    alt changement tests apres BROUILLON
        Ser-->>API: ValidationError
        API-->>Admin: 400 tests non modifiables
    else validation OK
        API->>DB: update statut examen
        DB-->>API: examen publie
        API-->>Admin: 200 OK
    end
```

**Image PNG (pret a inserer):**  
![Sequence cycle examen](./sequence_exam_lifecycle.png)

**Version vectorielle:** [sequence_exam_lifecycle.svg](./sequence_exam_lifecycle.svg)

## 6) Diagramme de sequence - soumission et correction

### Description courte
Ce diagramme couvre le flux complet de l etudiant vers CI/CD puis retour webhook.

### Dessin
```mermaid
sequenceDiagram
    autonumber
    actor Etudiant
    actor Enseignant
    participant UI as UI Django (etudiant_examen_detail)
    participant Auth as Controle Auth/Role
    participant Ser as SoumissionSerializer
    participant DB as Base de donnees
    participant GH as GitHub API
    participant CI as Pipeline CI/CD
    participant WH as API Webhook Resultats

    Etudiant->>UI: Ouvrir examen puis POST code_source
    UI->>Auth: verifier session + role ETUDIANT
    Auth-->>UI: OK
    UI->>Ser: validate(payload, request.user)
    Ser->>DB: verifier groupe + date + unicite

    alt Validation KO
        Ser-->>UI: erreurs metier
        UI-->>Etudiant: message erreur
    else Validation OK
        UI->>DB: create Soumission(statut=EN_TEST)
        UI->>GH: upsert Main.java + metadata.json

        alt Push GitHub KO
            GH-->>UI: erreur API
            UI->>DB: delete Soumission
            UI-->>Etudiant: soumission annulee
        else Push GitHub OK
            GH-->>UI: repo_url + commit_sha
            UI->>DB: update Soumission(url_depot_git, hash_commit)
            CI->>WH: POST /api/webhook/resultats/ + X-API-TOKEN
            WH->>DB: update_or_create Resultat + update statut Soumission
            WH-->>CI: 200/201 OK
        end
    end

    Etudiant->>UI: consulter resultats
    UI->>DB: select Resultat par etudiant
    UI-->>Etudiant: note + feedback

    Enseignant->>UI: consulter resultats
    UI->>DB: select Resultat par examens enseignant
    UI-->>Enseignant: suivi corrections
```

**Image PNG (pret a inserer):**  
![Sequence soumission correction](./sequence_submission_correction.png)

**Version vectorielle:** [sequence_submission_correction.svg](./sequence_submission_correction.svg)
