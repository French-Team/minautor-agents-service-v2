# Specification -- enregistrer-usage-outil

**Version :** 0.2.1
**Statut :** ebauche
**Historique :** v0.2.1 (alignement spec/outil, round 11 coherence documentaire : version de la spec synchronisee avec la version de l outil 0.2.1) -> v0.1.0 (creation, 2026-08-11)
**Categorie :** Enregistrer
**Date :** 2026-08-11
**Agent :** Vulcain
**Pense-bete source :** demande utilisateur URGENTE 2026-08-11 (constat : certains agents n utilisent pas nos outils simples et basculent sur des outils tiers ; les tests anti-regression ne detectent pas ce probleme car aucune trace d utilisation n existe)

## Objectif

Enregistrer CHAQUE utilisation d un outil du cerveau-projet dans un registre
JSONL (`registre-usages-outils.jsonl`) : une ligne JSON par usage, avec
date, agent, outil, mode, commande et contexte. Creer la source de verite
que les controles (Janus, Themis) et les tests de non-regression pourront
croiser avec les rapports de mission.

## Contexte

- Constat utilisateur : Morpheus (exemple) n utilise pas toujours nos outils
  simples, ce qui le pousse vers des outils tiers. Les tests actuels
  detectent les TRACES (CRLF/non-ASCII/BOM via detecter-usage-outils-externes)
  mais pas QUI a utilise QUOI.
- Le generateur-commande est l entree PASSE PAR LE GENERATEUR : c est le
  point d integration naturel pour la journalisation automatique.
- Decision utilisateur (2026-08-11) : mode LES DEUX -- le generateur
  journalise automatiquement + un outil dedie pour les usages directs/combos.

## Fonctionnalites

| # | Fonctionnalite | Detail |
|---|---|---|
| 1 | Append JSONL | Ajoute une ligne JSON au registre (date, agent, outil, mode, commande, contexte) |
| 2 | Mode | `generateur` / `direct` / `combo` (defaut `direct`) |
| 3 | Dry-run | `--dry-run` : affiche la ligne sans l ecrire |
| 4 | Registre fixe | Chemin par defaut : cerveau-projet/agents/traces/registre-usages-outils.jsonl |
| 5 | Creation auto | Cree le dossier/registre si absent |
| 6 | Journalisation auto generateur | generateurs-commande.py appelle cet outil apres composer_commande (mode generateur) |

## Modeles de commande

```bash
# direct
enregistrer-usage-outil.py --agent <agent> --outil <outil> --mode <mode> [--commande <cmd>] [--contexte <ctx>] [--dry-run]
```

## Format du registre

```json
{"date":"2026-08-11 18:30:00","agent":"morpheus","outil":"valider-case","mode":"direct","commande":"","contexte":""}
```

- 1 ligne = 1 usage, append, LF pur, ASCII strict
- Chaque ligne est un JSON parseable independamment (interrogeable par les tests)

## Interface (--aide / --help)

- `--agent` : obligatoire, nom de l agent
- `--outil` : obligatoire, nom de l outil
- `--mode` : generateur|direct|combo, defaut direct
- `--commande` : optionnel, commande reelle
- `--contexte` : optionnel, contexte d usage
- `--registre` : optionnel, chemin du registre
- `--dry-run` : optionnel, simulation
- `--version` : affiche la version

## Cas limites

| Cas | Comportement |
|---|---|
| Registre absent | Cree le dossier et le fichier |
| Outil inconnu du catalogue | Enregistre quand meme (usage reel) -- c est le but |
| Commandes multi-mots | Stockees telles quelles dans `commande` |
| ASCII / LF | Le registre et les fichiers de l outil respectent ASCII strict + LF pur |

## Non-regression

- L ajout de l entree catalogue passe le catalogue de 141 a 142 commandes :
  mettre a jour test-007 (compteur) et index-tools (categorie Enregistrer).
- Les tests existants (test-001 a test-023) doivent rester verts.
- Un test dedie (test-024) pourra verifier le format du registre en non-regression (mission ulterieure).
