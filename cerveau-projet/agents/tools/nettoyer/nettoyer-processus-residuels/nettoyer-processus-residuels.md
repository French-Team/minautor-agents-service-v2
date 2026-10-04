---
identite:
  type: outil
  appartient_a: commun
  commun: true
---

# nettoyer-processus-residuels

**Version :** 0.1.1
**Statut :** ebauche
**Categorie :** Nettoyer

## Pourquoi cet outil ?

Completer `detecter-processus-residuels` : une fois les processus residuels
identifies, cet outil les **termine**. Conforme a la regle immuable
`regles-groupes-agents.md` : **seul Hygie supprime** - le verrou
`proteger-verrou-habilitation` bloque tout autre agent.

## Exclusivite

L'outil appelle `proteger-verrou-habilitation --agent <nom> --outil
nettoyer-processus-residuels` **AVANT toute action**. Seul `hygie` (qui
aura l'outil en carte) passe. Tout autre agent est BLOQUE avec la commande
d'activation de Hygie.

## Securites

| Securite | Detail |
|---|---|
| **Dry-run par defaut** | Sans `--kill` ni `--tous`, liste seulement ce qui serait tue |
| **Liste blanche** | `freebuff`, `unsloth`, `codebuff` : jamais tues (refus explicite) |
| **Verification d'existence** | Le PID est re-verifie avant le kill (evite les erreurs sur PID recycle) |
| **Confirmation** | Sans `--force`, une confirmation est demandee |

## Usage

```bash
# Dry-run (ne tue rien)
python3 nettoyer-processus-residuels.py --agent hygie

# Tuer des PID precis
python3 nettoyer-processus-residuels.py --agent hygie --kill 1234,5678 --force

# Tuer tous les residuels detectes
python3 nettoyer-processus-residuels.py --agent hygie --tous --force
```

## Options

| Option | Effet |
|---|---|
| `--agent <nom>` | Nom de l'agent appelant (obligatoire, verrou) |
| `--kill <pids>` | Pids a tuer (separes par des virgules) |
| `--tous` | Tuer tous les residuels detectes |
| `--force` | Confirmer sans relance |
| `--verbose` | Affiche les details |
| `--version` | Affiche la version |
| `--aide` | Affiche l'aide complete |

## Compatibilite

- Windows : `taskkill /PID <pid> /F`
- Linux/macOS : `os.kill(pid, SIGKILL)`

## Connexions

- `detecter-processus-residuels` : detection (tous les agents)
- `proteger-verrou-habilitation` : verrou d'exclusivite (Hygie seul)
- `detecter-residus` : residus fichiers (Hygie)
