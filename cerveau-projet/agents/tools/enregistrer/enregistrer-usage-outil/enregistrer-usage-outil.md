# enregistrer-usage-outil

**Categorie** : Enregistrer
**Version** : 0.2.1
**Statut** : ebauche
**Agent** : Vulcain
**Date** : 2026-08-11

Enregistre l'utilisation d'un outil du cerveau-projet dans le **registre
d'usage** (`cerveau-projet/agents/traces/registre-usages-outils.jsonl`) :
une ligne JSON par usage, en append.

---

## Objectif

Creer une **source de verite** sur QUI utilise QUEL outil, QUAND et COMMENT.
Cette trace permet aux controles (Janus, Themis) et aux tests de
non-regression de detecter :
- un agent qui n'utilise PAS nos outils (absence de traces alors que sa
  mission mentionne des commandes),
- un agent qui passe par des outils TIERS (commande non enregistree),
- les usages reellement conformes au catalogue (mode `generateur`).

## Utilisation

```bash
# Usage direct (mode par defaut : direct)
python3 enregistrer-usage-outil.py --agent morpheus --outil valider-case

# Usage genere via le catalogue
python3 enregistrer-usage-outil.py --agent vulcain --outil test-023-grep-budget-pondere \
    --mode generateur --commande "python3 ...py" --contexte "refonte spec"

# Usages d'un combo
python3 enregistrer-usage-outil.py --agent themis --outil combo-audit-themis --mode combo

# Simuler sans ecrire
python3 enregistrer-usage-outil.py --agent morpheus --outil valider-case --dry-run
```

## Parametres

| Parametre | Obligatoire | Defaut | Description |
|---|---|---|---|
| `--agent` | OUI | - | Nom de l'agent (ex : morpheus) |
| `--outil` | OUI | - | Nom de l'outil utilise |
| `--mode` | NON | `direct` | `generateur` / `direct` / `combo` / `script-temporaire` |
| `--commande` | NON | vide | Commande reelle lancee |
| `--contexte` | NON | vide | Contexte de l'usage (mission, etape) |
| `--registre` | NON | chemin fixe | Chemin du registre JSONL |
| `--dry-run` | NON | - | Affiche la ligne sans l'ecrire |
| `--version` | NON | - | Affiche la version |

## Registre (format JSONL)

Chaque ligne du registre est un objet JSON :
```json
{"date":"2026-08-11 18:30:00","agent":"morpheus","outil":"valider-case","mode":"direct","commande":"","contexte":""}
```

- 1 ligne = 1 usage
- Append en fin de fichier (creation si absent)
- ASCII strict + LF pur (chaque ligne se termine par `\n`)
- Le registre vit dans `cerveau-projet/agents/traces/registre-usages-outils.jsonl`
- Depuis v0.2.1 : garde-fous de fiabilite - `--agent`/`--outil` vides
  refuses (code 1), doublons signales en avertissement, lignes non-JSON
  du registre signalees avant ajout

## Garde-fous (v0.2.1)

- `--agent` vide ou `--outil` vide : `[ERREUR]` + code 1 (une entree sans
  agent ni outil est inexploitable)
- Entree identique deja presente (agent+outil+mode+commande+contexte) :
  `[AVERTISSEMENT]` (l'usage peut etre legitiment rejoue, on ne bloque pas)
- Registre cible avec des lignes non-JSON : `[AVERTISSEMENT]` avant l'ajout
  (le fichier est probablement corrompu, on ne l'ecrase jamais)

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.2.1 | 2026-08-12 | Round 8 : garde-fous de fiabilite (champs vides refuses, doublons et registre corrompu signales) |
| 0.2.0 | 2026-08-11 | Mode script-temporaire : declaration des scripts jetables .zz-*/.tmp-* pour le croisement du detecteur |
| 0.1.0 | 2026-08-11 | Creation : registre JSONL des usages d'outils |

## Integration avec le generateur-commande

Le `generateurs-commande.py` journalise AUTOMATIQUEMENT chaque commande
generee (mode `generateur`) : il appelle cet outil apres avoir compose la
commande. L'agent n'a donc rien a faire quand il passe par le generateur.

Pour les usages directs (sans generateur) ou les combos, l'agent doit
appeler cet outil lui-meme (ou son parcours le lui rappelle).

## Pourquoi ne pas valider l'outil ?

Cet outil enregistre l'usage REEL, meme si l'outil n'existe pas au
catalogue : c'est justement ce qui permet de detecter les commandes en dur
ou les outils hors catalogue. La validation se fait A POSTERIORI par les
controles (croisement registre vs catalogue).

## Normes

- ASCII strict : 0 non-ASCII
- LF pur : 0 CRLF
- Stdlib Python uniquement (json, datetime, argparse, io, os, sys)
