# enregistrer-lecon

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** enregistrer

## Description

Enregistre une lecon dans la BDD portable des lecons (SQLite, fichier unique
et partage : `cerveau-projet/agents/lecons/lecons.db`).

La BDD est la **memoire longue** des lecons des agents. Les `corrections.md`
restent la **memoire courte** (fenetre glissante des missions proches).

## Pourquoi cet outil ?

- Les `corrections.md` sont devenus illisibles (plusieurs milliers de lignes
  par agent) : ce sont des archives, plus une memoire de travail.
- Une BDD unique et partagee permet la **pollinisation croisee** : chaque
  agent peut consulter les lecons des autres.
- C est aussi le **beta-test** de la future BDD du projet.

## Regles

- **Anti-usurpation** : chaque agent n ecrit QUE ses propres lecons
  (`--agent` doit etre l agent actif de la session, sinon refus code 1).
- **Verrou** : l usage passe par le verrou d habilitation
  (`proteger-verrou-habilitation`, auto-journalise).
- **ASCII strict** : tout caractere non-ASCII est refuse.
- **Anti-doublon** : meme agent + titre + corps deja present = signale, rien
  n est re-ecrit.

## Utilisation

```
python3 enregistrer-lecon.py --agent <auteur> --titre <titre> --lecon <texte> [OPTIONS]
```

### Options

| Option | Description |
|---|---|
| `--agent <auteur>` | Auteur de la lecon (obligatoire = agent actif) |
| `--domaine <d>` | Domaine/theme (outil, test, carte, protocole...) |
| `--tags <t1,t2>` | Tags separes par des virgules |
| `--titre <titre>` | Titre court de la lecon |
| `--lecon <texte>` | Corps de la lecon (ou `--lecon-fichier`) |
| `--lecon-fichier <f>` | Fichier contenant le corps de la lecon |
| `--mission <contexte>` | Contexte de la mission |
| `--outils <o1,o2>` | Outils concernes |
| `--verdict <v>` | Verdict associe |
| `--version` | Affiche la version |
| `--aide` | Affiche l aide |

### Exemple

```
python3 enregistrer-lecon.py --agent vulcain --domaine outil \
  --tags "bdd,outil" --titre "BDD lecons = memoire longue" \
  --lecon "La BDD est la memoire longue, corrections.md la memoire courte." \
  --verdict OK
```

## Lecon compagnon

Apres l ecriture, la lecon est consultable via `consulter-lecons`.
