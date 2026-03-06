# Guide Git Local + GitHub (simple et fiable)

Ce guide est adapte a ton projet `pfe1.0_26`.

## Pourquoi c est utile

- Tu gardes un historique propre de ton code.
- Tu peux revenir en arriere si une modification casse le systeme.
- Tu evites les pertes de travail.
- Tu travailles par fonctionnalite (branches) sans casser la base stable.

## Ce qui a ete configure dans ton depot

Configuration locale deja appliquee:
- push par defaut vers `origin` (GitHub perso)
- branche `master` suit `origin/master`
- nettoyage auto des references distantes supprimees (`fetch.prune=true`)
- `git pull` en mode `fast-forward only` (evite les merges automatiques surprises)

## Strategie conseillee

- `master`: branche stable.
- `feature/...`: une branche par fonctionnalite ou correction.

Exemples de noms:
- `feature/rapport-models`
- `feature/webhook-timeout`
- `fix/login-oauth`

## Routine quotidienne (5 commandes)

1. Mettre a jour la branche stable:
```bash
git switch master
git pull origin master
```

2. Creer une branche de travail:
```bash
git switch -c feature/nom-fonctionnalite
```

3. Commiter proprement:
```bash
git add -A
git commit -m "feat: description courte"
```

4. Envoyer sur GitHub:
```bash
git push -u origin feature/nom-fonctionnalite
```

5. Fin de travail (apres merge):
```bash
git switch master
git pull origin master
git branch -d feature/nom-fonctionnalite
```

## Messages de commit recommandes

- `feat: ...` nouvelle fonctionnalite
- `fix: ...` correction
- `docs: ...` documentation
- `refactor: ...` reorganisation interne
- `test: ...` ajout/modification de tests

Exemples:
- `feat: add rapport_models diagrams`
- `fix: reject expired oauth link`
- `docs: update webhook setup guide`

## Commandes de securite tres utiles

Voir rapidement l etat:
```bash
git status -sb
```

Voir l historique compact:
```bash
git log --oneline --graph --decorate -20
```

Annuler un fichier non commit:
```bash
git restore chemin/fichier
```

Annuler une zone staged:
```bash
git restore --staged chemin/fichier
```

## Regles simples a respecter

- Ne code pas directement sur `master`.
- Fais de petits commits frequents.
- Teste avant push (`python manage.py test` au minimum avant merge).
- Utilise des messages de commit explicites.

## Si tu veux passer de master vers main (optionnel)

Ce n est pas obligatoire. Ton depot fonctionne deja sur `master`.
Si tu veux standardiser sur `main`, fais-le plus tard quand l equipe est alignee.
