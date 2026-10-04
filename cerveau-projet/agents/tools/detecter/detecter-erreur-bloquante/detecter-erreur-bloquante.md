---
identite:
  type: outil
  appartient_a: commun
  commun: true
---

# detecter-erreur-bloquante

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** Detecter

## Pourquoi cet outil ?

Une session ne demarre pas "pour rien" : un marbre divise, un daemon mort
ou un etat de carte residuel bloque silencieusement le round. C est
exactement l erreur observee au demarrage 2026-08-29 : un agent a edite la
zone `constitution` d AGENTS.md sans passer par la porte du marbre, et
`sidentifier` a refuse d ecrire (zones protegees divisees). La session
etait BLOQUEE avec un message cryptique.

Cet outil **detecte et AFFICHE clairement** ces conditions bloquantes
AVANT demarrer, pour donner immediatement le diagnostic (OU CHERCHER /
REPARER) au lieu de bloquer sans explication.

## Ce qu il detecte

| Signal | Condition | Consequence |
|---|---|---|
| **MARBRE DIVISE** | Une zone protegee (constitution, cases cerberus, regles-groupes) a une empreinte differente du manifeste `marbre.json` | `sidentifier` refuse d ecrire dans AGENTS.md -> demarrage bloque |
| **DAEMON MORT** | `oracle-server` et/ou `routines-server` ne tournent pas (pid absent/mort) | Les missions asap ne sont pas consommees -> les agents ne demarrent pas |
| **ETAT-CARTE INCOHERENT** | Un etat de carte est a `etape=fin` avec un `precedent` pose (residu de fin de round) | Risque de mauvais rebouclage precedent-aware au round suivant |

## Usage

```bash
python3 detecter-erreur-bloquante.py
python3 detecter-erreur-bloquante.py --verbose
python3 detecter-erreur-bloquante.py --status
python3 detecter-erreur-bloquante.py --marbre-seul
```

## Options

| Option | Effet |
|---|---|
| `--verbose` | Detail de chaque controle (marbre, daemons, etats) |
| `--status` | Code de sortie : 0 = aucun bloquant, 4 = un bloque |
| `--marbre-seul` | Ne verifier que le marbre (zone la plus bloquante) |
| `--version` | Affiche la version |
| `--aide` | Affiche l aide complete |

## Integration recommandee

Appeler cette routine en TETE de `outils-llm/demarrer-llm.py` (apres la
lecture de l agent actif, avant `sidentifier`) pour AFFICHER le diagnostic
debranchant avant la tentative d ecriture dans AGENTS.md. La routine est
NI bloquante (elle ne modifie rien) NI dependent d Oracle (elle lit les
fichiers d etat directement).

## Codes de sortie

- `0` : AUCUN bloquant (coordination prete)
- `4` : au moins UNE condition bloquante detectee
- `2` : erreur d utilisation

## Connexions

- `proteger-verrou-marbre` : verification d integrite du marbre (reutilise)
- `proteger-modifier-marbre` : porte de reparation LEGITIME d une zone
- `oracle.py demarrage` : relance les serveurs morts
- source de l erreur : `outils-llm/demarrer-llm.py` (pas sidentifier)