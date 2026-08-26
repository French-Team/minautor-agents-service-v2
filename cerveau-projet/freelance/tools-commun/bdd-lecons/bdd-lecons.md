# bdd-lecons v2 (D10) — BDD des lecons (bible)

> La BDD des lecons v2 : lecons CLASSEES, CATEGORISEES, consultables
> comme une bible au moment du besoin (decision D10, proposition-v2.md).
> Stockage SQLite (modele du classeur v2 : rapide, consultation immediate).
> Les agents n ecrivent PLUS leurs lecons dans corrections.md : ils les
> enregistrent ici via l outil.

## Emplacement

- Outil : `cerveau-projet/freelance/tools-commun/bdd-lecons/`
  (entry.py + fonctions/bdd_lecons.py + lecons.db + bdd-lecons.md)
- BDD : `lecons.db` (SQLite, creee au premier appel)

## Format d une lecon

| Champ | Detail |
|---|---|
| `id` | auto (increment) |
| `date` | auto (YYYY-MM-DD HH:MM:SS.mmm — 3 chiffres ms) |
| `agent` | obligatoire (qui a appris la lecon) |
| `categorie` | `outil` / `protocole` / `processus` / `carte` / `correction` / `technique` / `autre` (defaut : correction) |
| `titre` | auto (debut du resume, ~70 caracteres) |
| `resume` | obligatoire (la lecon, ce qui a ete appris) |
| `mots_cles` | csv libre (facilite la recherche) |
| `source` | fichier d origine (pour les lecons migrees) ou `bdd-lecons` |

## Commandes

```
bdd-lecons enregistrer "<resume>" --agent <nom> [--categorie C] [--mots-cles a,b] [--source S]
bdd-lecons lister [--n 20]                # les 20 dernieres (bible : apercu recent)
bdd-lecons chercher [--mot-cle M] [--categorie C] [--agent A]
bdd-lecons compter                        # nombre total de lecons
```

## Usage agent (PROTOCOLE 22 : commande + pourquoi)

- **ENREGISTRER une lecon** : `bdd-lecons enregistrer "<ce que j ai appris>" --agent <moi> --categorie correction`
  → l outil fait le reste (id/date/titre auto), il CONFIRME (affiche id + categorie).
- **CONSULTER avant de re-inventer** (D10) : `bdd-lecons chercher --mot-cle <sujet>`
  → consulte la bible au moment du besoin, AVANT de re-inventer (P5/P6 v1).
- **Voir les apprentissages recents** : `bdd-lecons lister --n 20`.

## Regles

- La BDD est le SEUL stockage des lecons v2 (plus de lecons dans corrections.md).
- Une lecon est enregistree par son auteur (agent), pas par un tiers.
- La consultation est une LECTURE (jamais de modification de lecon existante ;
  une lecon fausse est signalee, pas corrigee).
- HARNAIS (PROTOCOLE 21) : l outil s auto-verifie en debut de traitement.

## Migration (une fois, 2026-08-25)

Les lecons historiques des `corrections.md` (9 agents v2) ont ete importees
avec `source` = fichier d origine. Les corrections.md cessent d accueillir
de nouvelles lecons.
