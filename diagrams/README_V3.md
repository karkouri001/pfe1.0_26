# Diagrammes V3 (version enrichie)

Cette version enrichit les anciens diagrammes avec:
- plus de cardinalites et contraintes metier,
- les flux OAuth / GitHub / CI-CD / webhook,
- la separation MCD (conceptuel) vs MLD (logique),
- une vue classes orientee code Django/DRF,
- deux sequences metier detaillees.

## Fichiers
- `diagrams/mld_v3.mmd`
- `diagrams/use_cases_v3.mmd`
- `diagrams/mcd_v3.mmd`
- `diagrams/class_diagram_v3.mmd`
- `diagrams/sequence_submission_correction_v3.mmd`
- `diagrams/sequence_exam_lifecycle_v3.mmd`

## Rendu SVG (optionnel)
Si Mermaid CLI (`mmdc`) est installe:

```bash
mmdc -i diagrams/mld_v3.mmd -o diagrams/mld_v3.svg
mmdc -i diagrams/use_cases_v3.mmd -o diagrams/use_cases_v3.svg
mmdc -i diagrams/mcd_v3.mmd -o diagrams/mcd_v3.svg
mmdc -i diagrams/class_diagram_v3.mmd -o diagrams/class_diagram_v3.svg
mmdc -i diagrams/sequence_submission_correction_v3.mmd -o diagrams/sequence_submission_correction_v3.svg
mmdc -i diagrams/sequence_exam_lifecycle_v3.mmd -o diagrams/sequence_exam_lifecycle_v3.svg
```
