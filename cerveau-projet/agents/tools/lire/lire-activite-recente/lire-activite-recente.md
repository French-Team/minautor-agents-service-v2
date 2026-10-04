---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# lire-activite-recente

**Version :** 0.1.2
**Statut :** prepare
**Categorie :** lire
**Chemin :** `agents/tools/lire/lire-activite-recente/`
**Proprietaire :** Vulcain (outil partage)

## Description

Lire les N dernieres interventions des agents depuis l'historique
(`AGENTS-historique.md`) au format condense : `date | session | agent | action`.
C'est le FIL D'ACTUALITE du cerveau : chaque agent qui demarre lit les 15 dernieres
interventions (des autres comme des siennes) pour savoir ce qui se passe en temps
reel, notamment quand plusieurs LLM travaillent en parallele.

Complements :
- `lire-fichier` / `lire-lignes` : lecture brute d'un fichier
- `lire-activite-recente` : lecture SEMANTIQUE de l'historique (les plus recentes en premier)

## Utilisation

```bash
# 15 dernieres interventions (defaut)
python3 lire-activite-recente.py

# 25 dernieres
python3 lire-activite-recente.py --nombre 25

# Action tronquee a 60 caracteres
python3 lire-activite-recente.py --longueur 60

# Fichier historique surcharge (tests)
AGENTS_HISTORIQUE=/tmp/AGENTS-historique.md python3 lire-activite-recente.py

# Avec details
python3 lire-activite-recente.py --verbose
```

Version bash equivalente : `lire-activite-recente.sh` (meme logique, meme sortie).

## Options

| Option | Description | Defaut |
|---|---|---|
| `--nombre N` | Nombre d'entrees a afficher | 15 |
| `--longueur L` | Longueur max de l'action en caracteres | 100 |
| `--verbose` | Afficher les details (fichier, nombre) | false |
| `--version` | Afficher la version | - |
| `--aide, -h` | Afficher l'aide | - |

Argument positionnel : `[fichier]` (defaut : env `AGENTS_HISTORIQUE`, sinon `AGENTS-historique.md`).

## Ce que l'outil fait

1. Lit le fichier historique (les entrees les plus recentes sont EN HAUT)
2. Extrait les N premieres lignes d'interventions (format `| date | session | agent | raison |`)
3. Tronque la raison a L caracteres (action)
4. Affiche `date | session | agent | action`

## Integration

- **Parcours des agents** : la relecture de l'historique devient une lecture obligatoire
  en case c0/c0b (contexte temps reel) -- l'agent lance cet outil pour voir les 15
  dernieres interventions avant de continuer.
- **Multi-LLM** : chaque LLM qui demarre voit l'activite des autres sessions en live
  (avec la section `## Sessions connues` maintenue par activer-agent-principal v0.4.1).
