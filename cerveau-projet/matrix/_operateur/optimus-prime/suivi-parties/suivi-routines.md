---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# SUIVI DES ROUTINES

> Les routines declarees, leur mode et leur cadence. Le vivant ou mort se
> lit DANS LE SYSTEME (le PID de l etat court), pas dans la declaration :
> une cadence declaree ne prouve pas que la routine tourne.
>
> Vue DERIVEE, REGENERABLE : 2026-10-04 18:45:38 par
> `suivi-parties-maitresses.py`. Aucun fait n est ecrit deux fois --
> la source reste la source (L-055).

## Routines

| Routine | Mode | Cadence | Priorite | Etat | Temoin |
|---|---|---|---|---|---|
| `routeur-maintenance` | passe | 30 s | 95 | non publie | aucun etat du dossier ne porte de pid |
| `suivi-sync` | passe | 60 s | 70 | non publie | aucun etat du dossier ne porte de pid |
| `veille-flux` | passe | 300 s | 60 | non publie | aucun etat du dossier ne porte de pid |
| `espion-integrite` | passe | 300 s | 55 | mort | pid 15436 (lu dans espion-etat.json) |
| `vigie-portes` | passe | 900 s | 50 | non publie | aucun etat du dossier ne porte de pid |
| `vigie-profil` | passe | 900 s | 40 | non publie | aucun etat du dossier ne porte de pid |
| `verifier-liens-cartes` | passe | 3600 s | 10 | non publie | aucun etat du dossier ne porte de pid |
| `chien` | boucle | 20 s | 80 | vivant | pid 3848 (lu dans chien.pid) |

8 routine(s) declaree(s).

Sources illisibles : aucune.
