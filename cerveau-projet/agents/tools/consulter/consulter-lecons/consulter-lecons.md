# consulter-lecons

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** consulter

## Description

Consulte la BDD portable des lecons (SQLite, fichier unique et partage :
`cerveau-projet/agents/lecons/lecons.db`).

Permet la **pollinisation croisee** : chaque agent peut lire les lecons des
autres (evolution entre eux grace aux experiences des autres).

## Pourquoi cet outil ?

- Une lecon apprise par un agent peut etre utile a un autre pour etablir un
  constat dans ses reflexions.
- La lecture est **verrouillee** (verrou d habilitation) et **journalisee**
  (controle d activite : qui a consulte quoi).

## Regles

- **Verrou** : l usage passe par le verrou d habilitation
  (`proteger-verrou-habilitation`, auto-journalise).
- **Journalisation d activite** : chaque consultation est tracee dans le
  registre (`registre-usages-outils.jsonl`, mode `direct`) avec le filtre
  utilise.

## Utilisation

```
python3 consulter-lecons.py --agent <lecteur> [FILTRES]
```

### Options

| Option | Description |
|---|---|
| `--agent <lecteur>` | Agent qui consulte (obligatoire) |
| `--toutes` | Lister toutes les lecons |
| `--auteur <agent>` | Filtrer par auteur |
| `--domaine <d>` | Filtrer par domaine |
| `--tags <t>` | Filtrer par tag (LIKE) |
| `--recent <N>` | N lecons les plus recentes |
| `--recherche <motif>` | Recherche dans titre/lecon/mission |
| `--rapport <fichier>` | Ecrire un rapport markdown |
| `--version` | Affiche la version |
| `--aide` | Affiche l aide |

### Exemple

```
python3 consulter-lecons.py --agent buffy --domaine outil
python3 consulter-lecons.py --agent buffy --recherche "verrou" --rapport lecons.md
```

## Lecon compagnon

Pour ecrire une lecon : `enregistrer-lecon` (anti-usurpation : chaque agent
n ecrit que ses lecons).
