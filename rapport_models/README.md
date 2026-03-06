# Rapport Models - Kit pret pour rapport de stage

Ce dossier contient des diagrammes coherents avec le code actuel du projet Django.
Les fichiers sont en format Mermaid (`.mmd`) pour faciliter l export en SVG/PNG.

## Contenu du dossier

| Fichier | Objectif | Section conseillee dans le rapport |
|---|---|---|
| `mcd.mmd` | Modele conceptuel de donnees (vision metier) | Analyse et conception |
| `mld.mmd` | Modele logique de donnees (tables/cles) | Conception base de donnees |
| `use_cases.mmd` | Cas d utilisation (acteurs + services) | Analyse fonctionnelle |
| `class_diagram.mmd` | Vue classes metier + API + UI | Conception technique |
| `sequence_exam_lifecycle.mmd` | Sequence creation/publication examen | Conception dynamique |
| `sequence_submission_correction.mmd` | Sequence soumission + correction CI/CD | Conception dynamique |
| `modeles_avec_dessins.md` | Modeles + dessins sous chaque modele (pret a coller) | Redaction finale |
| `texte_rapport_pret_a_copier.md` | Texte deja redige pour integrer les figures | Redaction finale |

## Ordre recommande dans le rapport

1. Cas d utilisation (`use_cases.mmd`)
2. MCD (`mcd.mmd`)
3. MLD (`mld.mmd`)
4. Diagramme de classes (`class_diagram.mmd`)
5. Sequence cycle examen (`sequence_exam_lifecycle.mmd`)
6. Sequence soumission/correction (`sequence_submission_correction.mmd`)

## Legende rapide

- `BROUILLON`, `PUBLIE`, `EN_COURS`, `FERME` = statuts d un examen.
- `EN_ATTENTE`, `EN_TEST`, `CORRIGE`, `ECHEC` = statuts d une soumission.
- `0..1` = relation optionnelle.
- `1..N` = relation obligatoire multiple.

## Export en SVG/PNG pour Word

Option simple:
1. Ouvrir https://mermaid.live
2. Coller le contenu du fichier `.mmd`
3. Exporter en `SVG` (recommande pour qualite)

Option locale (si `mmdc` est installe):
```bash
mmdc -i mcd.mmd -o mcd.svg
mmdc -i mld.mmd -o mld.svg
mmdc -i use_cases.mmd -o use_cases.svg
mmdc -i class_diagram.mmd -o class_diagram.svg
mmdc -i sequence_exam_lifecycle.mmd -o sequence_exam_lifecycle.svg
mmdc -i sequence_submission_correction.mmd -o sequence_submission_correction.svg
```

## Point de coherence avec le code

Ces diagrammes sont alignes avec:
- `gestion/models.py`
- `gestion/serializers.py`
- `gestion/views.py`
- `ui/views.py`

Si tu modifies ces fichiers, pense a mettre a jour ce dossier pour garder ton rapport synchronise.
