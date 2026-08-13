# Audit : registre des usages vs cartes des agents

**Date** : 2026-08-13
**Evaluatrice** : Themis
**Objet** : verifier que TOUS les outils reellement utilises par les agents
sont assignes aux cartes (demande utilisateur).

## Methode

- Source des usages : `registre-usages-outils.jsonl` (21 lignes courantes)
  + `registre-usages-outils.historique.jsonl` (75 lignes) - le registre est
  la source fiable des usages reels (lecon Vulcain 2026-08-13).
- Croisement : usages declares vs (indices outil des cartes + outils P0 des
  fiches + outils transverses activer-agent-principal / enregistrer-usage-outil).
- Scan automatique `evaluer-processus` : 0 probleme (ne lit que le registre
  courant) - l audit manuel complet (courant + historique) revele les ecarts
  ci-dessous.

## Resultat par agent

### Cerberus : AUCUNE correction (etat voulu)

Les 5 outils declares hors carte sont des DERIVES HISTORIQUES DEJA CORRIGEES :
`tester-lancer-non-regression`, `generateurs-carte`, `generateurs-case`,
`generateurs-commande`, `detecter-usage-scripts-temporaires`. Le garde-fou
test-034 (cerberus-sans-outils-tests) les interdit explicitement : les
re-assigner annulerait la correction. C est l etat VOULU, pas une lacune.

### Janus : 5 ecarts dont 1 reference morte

| Outil declare | Statut | Verdict |
|---|---|---|
| `valider-case` | EXISTE, hors carte | Lacune reelle (controle croise round 7) |
| `detecter-decalages-catalogue` | EXISTE, hors carte | Lacune reelle (controles croises) |
| `detecter-divergences-version` | EXISTE, hors carte | Lacune reelle (controles croises) |
| `generateurs-regenerer-catalogue` | EXISTE, hors carte | Lacune reelle (dry-run controles) |
| `verifier-cartes-decision` | **INTROUVABLE** | **Reference morte** : typo probable pour `valider-cartes-decision` (ligne 2026-08-12 23:48:15) |

### Morpheus : 4 lacunes reelles

| Outil declare | Statut | Verdict |
|---|---|---|
| `detecter-divergences-version` | EXISTE, hors carte | Lacune (verification coherence) |
| `generateurs-regenerer-catalogue` | EXISTE, hors carte | Lacune (dry-run) |
| `tester-protections` | EXISTE, hors carte | Lacune : carte reference `tester-protection-*` (wildcard ne matchant pas le nom reel) |
| `valider-cartes-decision` | EXISTE, hors carte | Lacune (validation) |

### Vulcain : 6 lacunes reelles

| Outil declare | Statut | Verdict |
|---|---|---|
| `detecter-divergences-version` | EXISTE, hors carte | Lacune (round 11 coherence) |
| `detecter-usage-scripts-temporaires` | EXISTE, hors carte | Lacune (round 8 registre) |
| `generateurs-carte` | EXISTE, hors carte | Lacune (round 9 guidage) |
| `generateurs-case` | EXISTE, hors carte | Lacune (round 9 guidage) |
| `generateurs-regenerer-catalogue` | EXISTE, hors carte | Lacune (dry-run) |
| `guider-parcours` | EXISTE, hors carte | Lacune (guidage) |

## Synthese

- **1 reference morte** : `verifier-cartes-decision` (janus, registre historique)
- **15 usages legitimes hors carte** a corriger : janus 4, morpheus 4, vulcain 6
  (outils existants, utilises dans le cadre du role, absents des indices)
- **Cerberus : 0 correction** (derives corrigees, garde-fou test-034 en vigueur)

## Recommandations de correction (a executer par l agent habilite)

1. **Janus** : ajouter `valider-case`, `detecter-decalages-catalogue`,
   `detecter-divergences-version`, `generateurs-regenerer-catalogue` aux
   indices outil de la case c4 (Verifier les tests) ou c22 (controle
   modification) + corriger la typo du registre (`verifier-cartes-decision`
   -> `valider-cartes-decision`).
2. **Morpheus** : ajouter `detecter-divergences-version`,
   `generateurs-regenerer-catalogue`, `valider-cartes-decision` (c11/c12) +
   corriger le wildcard `tester-protection-*` -> `tester-protections`.
3. **Vulcain** : ajouter `detecter-divergences-version`,
   `detecter-usage-scripts-temporaires`, `generateurs-carte`, `generateurs-case`,
   `generateurs-regenerer-catalogue`, `guider-parcours` (c10 ou c6/c12).

## Lecon

L audit manuel complet (registre courant + historique) revele plus que le
scan automatique (registre courant seul) : le lanceur de non-regression
archive les declarations dans l historique, et evaluer-processus ne lit que
le registre courant. Pour un audit complet, lire les DEUX sources. Et les
derives corrigees restent dans l historique : les ecarts qu elles creent
sont VOLUS, pas des lacunes - il faut qualifier avant de corriger.
