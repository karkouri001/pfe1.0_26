# Pack examen Java: somme des nombres pairs

Ce dossier contient un examen complet et ses tests unitaires pour valider la correction automatique.

## Contenu
- `ENONCE.md`: sujet a donner a l etudiant.
- `tests_repo/`: repo de tests unitaires JUnit (a pousser sur GitHub).
- `solutions/Main_ok.java`: exemple de solution correcte.
- `solutions/Main_ko.java`: exemple de solution incorrecte.
- `run_local_tests.ps1`: script local pour verifier passe/echec rapidement.

## Utilisation dans la plateforme
1. Pousse `tests_repo/` dans un repo GitHub dedie (ex: `karkouri001/exam-java-somme-pairs-tests`).
2. Recupere le hash commit a utiliser pour figer la version des tests.
3. Cree l examen dans la plateforme avec:
   - `url_tests_git`: URL GitHub du repo de tests (ex: `https://github.com/karkouri001/exam-java-somme-pairs-tests.git`)
   - `hash_tests`: hash commit des tests
4. Donne le sujet `ENONCE.md` aux etudiants.

## Test local rapide
Depuis ce dossier:

```powershell
.\run_local_tests.ps1 -Solution ok
.\run_local_tests.ps1 -Solution ko
```

- `ok` doit passer les tests.
- `ko` doit echouer.
