---
identite:
  type: outil-executer
  appartient_a: matrice-data-outils
  version: 1.0.0
---

# Outil EXECUTER -- Execution Python seule

## Porte unique

Cet outil est la porte unique pour toute execution de commande.
Il remplace `run_terminal_command` (bash) par un execution **Python seule**.

## Verbes

| Verbe | Usage | Codes retour |
|---|---|---|
| `executer` | Execute une commande Python | 0=succes, 1=echec commande, 2=refus |

## Options executer

| Option | Defaut | Description |
|---|---|---|
| `--cmd` | (requis) | Commande a executer |
| `--timeout` | 60 | Timeout en secondes |
| `--contenu-chemin` | (aucun) | Anti-heredoc : @file ou chemin direct |
| `--json` | (non) | Sortie machine JSON |

## Regles absolues

1. **Python seul** : pas de bash/sh/cmd/powershell
2. **Pas de pipe** : chaque commande separee
3. **Pas de redirection** : utilisation des outils ecrire/lire
4. **Pas de 2>/dev/null** (L-003) : les erreurs doivent etre visibles
5. **Pas de heredoc** : utilisation de --contenu-chemin @file
6. **Pas de curl/wget** : utilisation des outils dedies

## Architecture

```
executer/
  constants.py     -- Chemins, commandes interdites, timeout
  commun.py        -- Validation, parse, lancement Python seul
  executer/
    entry.py       -- Verbe executer (dispatch)
  main.py          -- Point d'entree (sac a dos + dispatch)
```

## Garanties

- Zero zombie L-012 (start_new_session)
- CREATE_NO_WINDOW (win) / start_new_session (posix)
- Collecte stdout + stderr + code + duree
- Compatible win/linux
- BDD modifications tracee
