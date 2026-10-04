---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# detecter-fins-passives

**Categorie** : Detecter
**Version** : 0.1.0
**Statut** : prepare
**Date creation** : 2026-09-02
**Proprietaire** : Vulcain (outil partage, usage principal Buffy)

---

## Objectif

Detecter les fins PASSIVES dans les arbres v2 des agents
(`cerveau-projet/agents/*/parcours/fins.json` + `theme-*.json`).

**Pourquoi cet outil ?**
- Norme du modele aero (decision utilisateur 2026-08-30) : TOUTE fin d un
  arbre v2 doit porter `action=reactiver` + `cible=oracle` + la commande
  `reactiver-fin <agent> --cible oracle` (la fin va vers ORACLE, le pilote
  decide du suivant).
- Une fin PASSIVE (`action=procedure` sans commande, `cible=cerberus`,
  formulation "attend le retour", theme qui clot sur `fin-theme`) COUPE
  la chaine : l arbre se fige, le round ne continue pas (particulierement
  vrai en single-LLM ou rien ne repart en arriere-plan).
- Cet outil rejoue automatiquement le diagnostic qui a ete fait a la main
  sur la carte de Cerberus (2026-09-02) : il signale les fins a corriger
  AVANT qu elles ne bloquent un round.

---

## Utilisation

```bash
# Version Python (recommandee)
python3 detecter-fins-passives.py [CIBLE] [--agents A B] [--json]

# Version bash equivalente (wrapper)
bash detecter-fins-passives.sh [CIBLE] [--agents A B] [--json]
```

**Arguments :**
| Argument | Description |
|---|---|
| `CIBLE` | Dossier des agents (defaut: `cerveau-projet/agents/`) |
| `--agents A B` | Limiter l analyse aux agents listes (ex: `--agents cerberus argus`) |
| `--json` | Sortie JSON machine (champ `bloquant: true/false` par probleme) |
| `--version` | Afficher la version |

**Exit code :**
| Code | Signification |
|---|---|
| `0` | Aucune fin passive bloquante (des [INFO] de migration peuvent exister) |
| `1` | Fins PASSIVES detectees OU cible introuvable |
| `2` | Erreur (racine du projet introuvable, cible invalide) |

---

## Ce que detecte l'outil

| Type | Bloquant ? | Detail |
|---|---|---|
| `PROCEDURE_SANS_COMMANDE` | OUI | Fin `action=procedure` sans commande : elle ne fait rien, chaine coupee |
| `FIN_SANS_ACTION` | OUI | Fin sans champ `action` : coquille |
| `ACTION_INCONNUE` | OUI | Action non reconnue (ni reactiver ni delegation) |
| `CIBLE_NON_ORACLE` | OUI | Fin `reactiver` vers autre chose qu'ORACLE (ex: cerberus) |
| `COMMANDE_SANS_REACTIVER_FIN` | OUI | Fin `reactiver` dont la commande n appelle pas reactiver-fin |
| `FORMULATION_PASSIVE` | OUI | Description/titre porte "attend le retour / attends la suite..." |
| `THEME_FINIT_SUR_FIN_THEME` | OUI | Un theme clot sur `fin-theme` (retour racine passif) au lieu d une fin active |
| `THEME_FIN_INCONNUE` | OUI | Un theme pointe vers une fin absente de fins.json |
| `FIN_THEME_NON_REDIRECTION` | OUI | La fin systeme `fin-theme` n est pas une redirection |
| `REDIRECTION_SANS_CIBLE` | OUI | Redirection sans champ `vers` |
| `FINS_JSON_INVALIDE` / `STRUCTURE_FINS` / `FIN_MALFORMEE` | OUI | Fichier illisible ou structure invalide |

Les fins `action=redirection` (reprise interne) et `action=activer`
(delegation directe, ancien modele bout-en-bout) sont signalees en
**[INFO]** : elles n'orientent pas vers ORACLE mais ne coupent pas la
chaine -- a migrer vers le modele aero, non bloquantes.

---

## Exemple

```bash
# Analyser tous les agents
python3 detecter-fins-passives.py

# Analyser un agent specifique
python3 detecter-fins-passives.py --agents cerberus

# Sortie machine pour un controleur
python3 detecter-fins-passives.py --json
```

Sortie :

```
[PASSIF] oracle | CIBLE_NON_ORACLE | fin-coordination (cible=cerberus)
[PASSIF] vulcain | PROCEDURE_SANS_COMMANDE | fin-signaler-besoin

=== RESUME fins-passives ===
Agents analyses : 30
Problemes        : 2 (dont 2 PASSIFS bloquants)
VERDICT : fins PASSIVES detectees (2) - la chaine peut s arreter
Correction recommandee : action=reactiver + cible=oracle + commande reactiver-fin <agent> --cible oracle (modele aero)
```

---

## Integration

- **Buffy** l utilise en audit des cartes v2 (complement de la suite
  combo-sante-tableaux) pour verifier qu aucune fin passive ne subsiste avant
  de declarer un arbre sain.
- **Themis / Janus** l utilisent en controle croise : `detecter-fins-passives
  --json` donne le verdict machine (champ `bloquant`).
- Il complemente le garde-fou de `generateurs-case` (Pattern 5), qui ne
  couvre que les PARCOURS v1 ; celui-ci couvre les ARBRES v2 (fins.json +
  themes).

---

## Notes

- Les dossiers hors agents (tools, lecons, traces, classeur-variables,
  conventions, regles-immuables, philosophie) sont ignores.
- Un agent sans `parcours/fins.json` n est pas un arbre v2 : ignore (tolere).
- Verifier apres chaque creation/branchement d agent : `detecter-fins-passives
  --agents <nouvel-agent>` doit rendre 0.

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-09-02 | Creation initiale : scan fins.json + themes de tous les agents, classification PASSIF (bloquant) vs INFO (delegation a migrer), options --agents/--json, modele aero reactiver-fin (decision 2026-08-30). |