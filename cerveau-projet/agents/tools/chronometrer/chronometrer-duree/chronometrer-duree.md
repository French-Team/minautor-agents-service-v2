---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# chronometrer-duree

**Categorie** : Chronometrer
**Version** : 0.1.2
**Statut** : ebauche
**Chemin** : `agents/tools/chronometrer/chronometrer-duree/`
**Proprietaire** : Vulcain (constructeur d'outils)

---

## Description

Mesure la **duree d une intervention d agent** : le chrono demarre quand un
agent est active (debut de mission) et s arrete au passage du relais
(activation de l agent suivant, ou reactivation de Cerberus). L etat est un
**journal JSONL** (`cerveau-projet/agents/traces/chronos.jsonl`) : une
entree ouverte (sans `date_fin`) = chrono actif.

`activer-agent-principal` appelle cet outil automatiquement a chaque
activation : `arreter` (ferme le chrono de l agent precedent) puis
`demarrer` (ouvre celui du nouvel agent). La duree est ensuite ajoutee au
**repere `###`** de l entree de l agent dans `AGENTS-historique.md` :
`### 2026-08-19 18:20 - vulcain (12min 30s)`.

---

## Utilisation

```bash
# Demarrer le chrono d un agent (fait automatiquement par activer-agent-principal)
python3 chronometrer-duree.py demarrer session-llm-1 vulcain --confirme-doc

# Arreter le chrono de la session (retourne : agent | duree)
python3 chronometrer-duree.py arreter session-llm-1 --confirme-doc

# Afficher TOUS les chronos actifs (une ligne par session, coexistence multi-sessions)
python3 chronometrer-duree.py etat --confirme-doc

# Afficher le chrono actif d UNE session precise
python3 chronometrer-duree.py etat session-llm-1 --confirme-doc

# Afficher la documentation
python3 chronometrer-duree.py --doc

# Simuler sans rien modifier
python3 chronometrer-duree.py demarrer session-llm-1 vulcain --dry-run
```

## Options

| Option | Description |
|---|---|
| `--dry-run` | Simuler sans rien modifier |
| `--verbose` | Afficher les details |
| `--version` | Afficher la version |
| `--chrono` | Mesurer la duree d execution de l outil lui-meme |
| `--doc` | Afficher le .md complet et sortir |
| `--confirme-doc` | Confirmer la lecture de la doc (requis en mode reel) |

---

## Format du journal (`traces/chronos.jsonl`)

Une ligne JSON par chrono :

```json
{"date_debut": "2026-08-19 18:25:30", "session": "session-llm-1",
 "agent": "vulcain", "date_fin": "2026-08-19 18:37:45",
 "duree_secondes": 735}
```

- `date_fin` null = chrono **ouvert** (agent en mission)
- `arreter` ferme le dernier chrono ouvert de la session et calcule la duree

---

## Regles

1. Le chrono couvre la mission COMPLETE de l agent : du `activer` au
   passage du relais (activer suivant / reactiver Cerberus).
2. La duree est ajoutee au repere `###` de l entree de l agent dans
   `AGENTS-historique.md` : `(Xmin Ys)`.
3. Un chrono deja ouvert pour une session est ferme automatiquement au
   `demarrer` suivant (passage de relais sans arret explicite) - avec
   avertissement.
4. Le journal est une TRACE (append logique) : il ne remplace aucun autre
   registre, il documente les durees d intervention.

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.1 | 2026-08-19 | TOKENS INTEGRES : demarrer accepte --tokens (snapshot cumulatif JSON) stocke en tokens_debut ; arreter retourne 'agent | duree | tokens_debut' (3e champ) pour la conso par difference. |
| 0.1.2 | 2026-08-19 | COEXISTENCE MULTI-SESSIONS : etat <session> affiche le chrono de CETTE session ; etat (sans session) affiche TOUS les chronos actifs (une ligne par session). Les sessions LLM paralleles ne se melangent plus : demarrer/arreter filtrent deja par session (chrono_actif), seul l'affichage etat etait global. |
| 0.1.0 | 2026-08-19 | Creation : journal JSONL traces/chronos.jsonl, commandes demarrer/arreter/etat, integration dans activer-agent-principal (ajout de la duree au repere ### de l historique) |

---

## Notes

- Le .sh et le .py coexistent dans le meme dossier (aucun ne remplace l autre).
- Version bash : `chronometrer-duree.sh` (meme comportement).
- Voir aussi : `activer-agent-principal` (integration automatique).
