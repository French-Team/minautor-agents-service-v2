# OUTIL bdd-usages

> Outil de la Matrice (M-013, plan 7 BDD : 4/7). Alimente la BDD
> `usages-outils-combos.jsonl` : UN enregistrement par appel d'un outil,
> combo ou routine de la Matrice (temps, resultat).
> Format journal : jsonl en AJOUT SEUL (l'histoire n'est jamais reecrite,
> sans empreinte -- comme historiques-missions.jsonl).

## Ce que fait chaque commande

- `noter` : ajoute UN enregistrement d'usage (outil, commande, code de sortie,
  duree optionnelle, detail optionnel, tags obligatoires).
- `lire` : lit la BDD, filtres combinables --outil / --tag (reponse vide =
  aucun resultat).
- `verifier` : controle structurel : chaque ligne est un JSON valide avec les
  cles requises et des tags non vides. Code 0/1.

## Flux d'ecriture (porte unique)

```
[1] l'appelant (espion embarque, routine, agent)
      |  python main.py noter --outil <nom> --commande <verbe> --code <n> [--duree <ms>] --tags "a,b"
      v
[2] main.py                 DIRIGE : route vers la categorie demandee
      v
[3] noter/entry.py          VALIDE (champs requis) puis orchestre
      v
[4] noter/fonctions.py      FABRIQUE l'entree {date, outil, commande, ...}
      v
[5] commun.py               AJOUTE UNE LIGNE a la BDD (ajout seul, LF forces)
```

## Regles

- Tags obligatoires (regles des BDD : lecons, modifications, USAGES).
- L'histoire (jsonl) n'est JAMAIS modifiee ni reecrite.
- Zero valeur en dur : la logique CONSOMME constants.py.
- Qui ecrit (contrat data-readme) : les espions embarques (sac a dos, M-014+),
  et pour l'instant les passes de la veille et l'agent.
