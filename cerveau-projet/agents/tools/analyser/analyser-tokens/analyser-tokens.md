---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# analyser-tokens

**Categorie** : Analyser
**Version** : 0.1.0
**Statut** : ebauche

---

## Objectif

Mesurer la consommation de tokens de la session en cours : tokens ENVOYES,
tokens RECUS et ENCOMBREMENT de la fenetre de contexte (utilise / total).

Cet outil est le premier du volet "mesure de la fenetre de contexte" (demande
utilisateur 2026-08-15) : il sera integre aux templates des futurs fichiers
(agents, outils, tests, scripts temp) pour que chaque fichier puisse rendre
compte de sa consommation.

---

## Modele hybride (decision utilisateur)

L outil utilise DEUX sources, la plus fiable en priorite :

| Source | Quand | Fiable |
|---|---|---|
| **Compteurs API reels** | `TOKENS_SESSION` (variable d environnement, JSON) ou fichier `cerveau-projet/agents/traces/metadonnees-session-*.json` contenant `prompt_tokens` / `completion_tokens` | OUI |
| **Estimation locale** | Aucune metadonnee API -> taille des registres et traces du projet convertie en tokens (~4 caracteres par token, 60% envoyes / 40% recus) | NON (heuristique, signalee) |

La fenetre de contexte : `fenetre_tokens` des metadonnees API si fournie,
sinon `--fenetre-total` (defaut 200 000).

---

## Utilisation

```bash
# Estimation locale (aucune metadonnee API)
python3 analyser-tokens.py

# Avec compteurs API reels (metadonnees de session presentes)
python3 analyser-tokens.py --session session-llm-1

# Fenetre de contexte differente
python3 analyser-tokens.py --fenetre-total 128000

# Rapport markdown
python3 analyser-tokens.py --rapport rapport-tokens.md

# Detail des sources
python3 analyser-tokens.py --verbose

# Version
python3 analyser-tokens.py --version
```

## Options

| Option | Description |
|---|---|
| `--session <nom>` | Session analysee (defaut : lue du classeur) |
| `--fenetre-total <N>` | Taille totale de la fenetre (defaut 200000) |
| `--rapport <f>` | Ecrit le rapport markdown |
| `--verbose` | Detail des sources (registres, metadonnees) |
| `--dry-run` | Affiche sans ecrire le rapport |
| `--no-chrono` | Coupe le chrono de l outil lui-meme |
| `--version` | Affiche la version |

---

## Sortie

```
=== ANALYSE TOKENS DE LA SESSION session-llm-1 ===
Tokens ENVOYES       : 45000
Tokens RECUS         : 12000
Tokens TOTAL         : 57000
Fenetre de contexte  : 128000
ENCOMBREMENT         : 44.5%
Source : compteurs API reels
```

En estimation locale, la source est signalee jaune avec l avertissement :
la seule source fiable est l API (TOKENS_SESSION ou metadonnees-session-*.json).

---

## Integration aux templates

La consommation de tokens sera integree aux templates des futurs fichiers :
- `outil-template-python.md` / `outil-template.md` : bloc tokens dans les options
- `fiche-agent-template.md` : mention de la mesure en fin de mission
- Template test (triplet v0.3.0) : chrono + tokens par test
- `protocole-creation-scripts-temporaires` : mesure des scripts temp

La migration est PROGRESSIVE avec des pilotes par type de fichier (agent,
outil, test, script temp) - documentee dans le protocole correspondant.

---

## Historique

| Version | Date | Description |
|---|---|---|
| 0.1.0 | 2026-08-15 | Creation : modele hybride (registres locaux + compteurs API), encombrement de la fenetre |
