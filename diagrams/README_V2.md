# Diagrammes V2

Ces diagrammes remplacent les versions trop minimales et couvrent :
- structure relationnelle detaillee (MLD),
- cas d usage metier et flux CI/CD,
- modele conceptuel de donnees (MCD),
- vue classes (modele + API + permissions + formulaire),
- sequences metier (soumission/correction + cycle de vie examen).

## Fichiers
- `diagrams/mld_v2.mmd`
- `diagrams/mld_v2.svg`
- `diagrams/use_cases_v2.mmd`
- `diagrams/use_cases_v2.svg`
- `diagrams/mcd_v2.mmd`
- `diagrams/mcd_v2.svg`
- `diagrams/class_diagram_v2.mmd`
- `diagrams/class_diagram_v2.svg`
- `diagrams/sequence_submission_correction_v2.mmd`
- `diagrams/sequence_submission_correction_v2.svg`
- `diagrams/sequence_exam_lifecycle_v2.mmd`
- `diagrams/sequence_exam_lifecycle_v2.svg`

## Rendu (optionnel)
Si `mmdc` (Mermaid CLI) est installe :

```bash
mmdc -i diagrams/mld_v2.mmd -o diagrams/mld_v2.svg
mmdc -i diagrams/use_cases_v2.mmd -o diagrams/use_cases_v2.svg
mmdc -i diagrams/mcd_v2.mmd -o diagrams/mcd_v2.svg
mmdc -i diagrams/class_diagram_v2.mmd -o diagrams/class_diagram_v2.svg
mmdc -i diagrams/sequence_submission_correction_v2.mmd -o diagrams/sequence_submission_correction_v2.svg
mmdc -i diagrams/sequence_exam_lifecycle_v2.mmd -o diagrams/sequence_exam_lifecycle_v2.svg
```
