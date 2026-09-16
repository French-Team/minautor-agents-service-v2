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
  aucun resultat) ; affiche le DETAIL (raison de protection) quand il existe.
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

## Audit sac-a-dos (2026-09-10)

### Total usages
3060 usages enregistres.

### Repartition par outil
| Outil | Usages | % |
|---|---|---|
| veille-flux | 1058 | 34.6% |
| corriger-ascii | 734 | 24.0% |
| bdd-activites | 731 | 23.9% |
| suivi-optimus | 322 | 10.5% |
| bdd-modifications | 69 | 2.3% |
| autres | 146 | 4.8% |

### Repartition par code
| Code | Count | Signification |
|---|---|---|
| 0 | 2242 | Succes (73.3%) |
| 1 | 786 | Refus (25.7%) - detection veille, probleme corriger-ascii, etc. |
| 2 | 32 | Refus technique (1.0%) - commande inconnue, etc. |

### Refus (code != 0)
- Total refus : 818 (26.7% des usages)
- Principaux types de refus :
  - veille-flux/passe-relax : code 1, "1 detection(s)" - detection d'ecart par veille-flux
  - corriger-ascii/corriger : code 1, "Probleme plus grave -> decision du createur (aucune perte de donnees)" - probleme non-auto-correctible
