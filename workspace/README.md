---
identite:
  type: dossier
  appartient_a: commun
  commun: true
---
# workspace/ -- Futur dossier des projets

Ce dossier est le **futur espace de travail des projets** du cerveau-projet.
Il vit a la racine, a cote de `cerveau-projet/`, et accueillera les
applications et projets qui seront developpes par la future equipe codeur
(issue des pense-betes, specs et todos du trio Athena / Promethee / Minerve).

---

## Compartimentation (agent Hygie)

Le scan des residus (`detecter-residus`) compartimente STRICTEMENT les deux
zones :

| Zone | Dossier scanne |
|---|---|
| `cerveau-projet` | `cerveau-projet/` uniquement |
| `workspace` | `workspace/` + la racine du projet, SANS `cerveau-projet/` |
| `tous` | les deux zones (sans double comptage) |

Chaque zone ne voit que SES residus : un fichier temp pose dans `workspace/`
n est JAMAIS signale par le scan de la zone `cerveau-projet`, et inversement.

---

## Regle

- Ce dossier est reserve aux PROJETS futurs : rien de temporaire, rien de
  jetable ici (les scripts temporaires des missions vivent dans `tmp-<agent>/`
  a la racine, supprimes en fin de mission - protocole-creation-scripts-
  temporaires).
- Hygie (agent de nettoyage) scanne cette zone comme les autres : tout residu
  pose ici (temp, rapport egare, fichier de version) est detecte et nettoye.
