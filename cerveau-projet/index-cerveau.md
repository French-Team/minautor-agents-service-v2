# Index du Cerveau -- projet analyste-in-console

**Version** : v0.3.0
**Statut** : ebauche

---

## Point d'entree

Ceci est le point d'entree unique du cerveau-projet. Tout ce qui ne concerne
pas le demarrage de session (demarrer.md) se trouve ici, par la navigation.

---

## Navigation

- [pense-betes/](pense-betes/index-pense-bete.md) -- idees developpees, travail en cours
- [conventions/](pense-betes/conventions/index-conventions.md) -- renommage, structures, liens
- [specs/](pense-betes/specs/index-spec.md) -- definitions techniques et fonctionnelles
- [regles-immuables/](pense-betes/regles-immuables/index-regles-immuables.md) -- process, hierarchie, RVAV
- [recherches-web/](recherches-web/index-recherches-web.md) -- recherches web
- [classeur-variables/](classeur-variables/index-classeur.md) -- stockage partage des variables
- [agents/tools/](agents/tools/index-tools.md) -- outils partages (explorer, valider, analyser, corriger)
- [agents/](agents/index-agents.md) -- systeme d'agents avec parcours (jeu de piste)

---

## Protocoles cles

| Protocole | Role |
|---|---|
| [protocole-identification](pense-betes/regles-immuables/general/protocole-identification/) | Identification du LLM (MODE ID multi-session) |
| [protocole-carte-decision](pense-betes/regles-immuables/general/protocole-carte-decision/) | Parcours (jeu de piste) -- methode actuelle de guidage |
| [protocole-demarrer-projet](pense-betes/regles-immuables/general/protocole-demarrer-projet/) | Demarrer un nouveau projet |
| [protocole-reprendre-projet](pense-betes/regles-immuables/general/protocole-reprendre-projet/) | Reprendre un projet existant |
| [protocole-activation](pense-betes/regles-immuables/general/protocole-activation/) | Activer / reactiver les agents |
| [protocole-auto-correction](pense-betes/regles-immuables/general/protocole-auto-correction/) | Auto-correction des agents |
| [protocole-installer-regles](pense-betes/regles-immuables/general/protocole-installer-regles/) | Installer les regles immuables |

Liste complete des regles et protocoles : [pense-betes/regles-immuables/index-regles-immuables.md](pense-betes/regles-immuables/index-regles-immuables.md).

---

## Fichiers cles

| Fichier | Role |
|---|---|
| `AGENTS.md` (racine) | Agent principal actuel de chaque session (dynamique) |
| `demarrer.md` (racine) | Porte d'entree de session (identification + parcours) |
| `agents/index-agents.md` | Point d'entree du systeme d'agents |
| `agents/<agent>/<agent>.md` | Fiche de l'agent |
| `agents/<agent>/corrections.md` | Corrections de l'agent |
| `agents/<agent>/parcours/parcours-<agent>.json` | Parcours (jeu de piste) de l'agent -- source de verite du guidage |
| `agents/tools/guider/guider-parcours/` | Outil qui fait avancer dans le parcours (spec, py, sh, md) |
| `classeur-variables/index-classeur.md` | Point d'entree du classeur de variables |

---

## Liens

- [demarrer.md](../demarrer.md) -- porte d'entree de session
- [AGENTS.md](../AGENTS.md) -- agent principal actuel
