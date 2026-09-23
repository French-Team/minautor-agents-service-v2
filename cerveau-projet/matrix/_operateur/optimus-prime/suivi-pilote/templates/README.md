---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# GABARITS INVISIBLES -- les moules de la zone d'Optimus

> Un moule ne s'execute JAMAIS seul : il est consomme par son unique PORTE.
> Ces moules vivent dans la zone INVISIBLE : un moule d'ici ne fabrique que de
> l'INVISIBLE (L-016 -- le visible garde `matrice/templates/`, patron `outil-bdd`).

## Quels artefacts, et qui les pose

| Moule | Fabrique | Pose par |
|---|---|---|
| `suivi-bdd/declaration.json.moule` | la DECLARATION fermee des pannes d'un suivi (un moule par suivi) | `poser-template-pilote` |
| `suivi-bdd/suivi.md.moule` | la VUE derivee d'un suivi (carte + Table 0 + tables de parties) | `poser-template-pilote` |

## Les jetons (remplaces a la pose)

| Jeton | Signification | Exemple |
|---|---|---|
| `__NOM_SUIVI__` | nom du suivi pose | suivi-pilote |
| `__APPARTIENT_A__` | nom d'appartenance de la carte | optimus-prime |
| `__DOMICILE__` | dossier de l'artefact (zone invisible) | _operateur/optimus-prime/suivi-pilote/ |
| `__PARTIE__` | partie surveillee | file |
| `__ID_PANNE__` | identifiant de la panne declaree | mission-qui-n-avance-pas |
| `__DETECTEUR__` | nom du detecteur | age_mission_en_cours |
| `__SEUIL_MINUTES__` | seuil de silence, en minutes (nombre) | 2880 |
| `__FAIT_ATTENDU__` | ce qui doit arriver | une mission en cours se termine dans la fenetre |
| `__SOURCE__` | source qui porte le fait | file-missions-optimus.json (chargee_le) |
| `__SEUIL_DECLARE__` | le seuil, dit en clair au lecteur | 2880 minutes (48 h) |
| `__GRAVITE__` | gravite | haute |
| `__VU_PAR__` | qui la voit deja, ou PERSONNE | PERSONNE |
| `__PORTE_QUI_REPARE__` | porte qui repare la panne | pilote reporter |
| `__PORTE__` | porte qui ecrit la vue | suivi-pilote |
| `__QUI_LIT__` | qui lit l'artefact | le lanceur de non-regression |
| `__COLONNE_N__` / `__VALEUR_N__` | colonnes d'une table | Mission / MO-1 |
| `__CONSTAT__` / `__SILENCE__` | la ligne de panne de la Table 0 | etat de pause ABSENT |

## La regle qui fait un MOULE, pas une copie

**Un moule SANS TROU est REFUSE** : sans jeton a remplacer, il ne fabrique pas un
artefact NEUF, il fabrique une **copie morte** -- la divergence de plus (L-055).
La porte n'ecrit rien tant qu'un jeton ne peut pas etre remplace.

## La porte unique

```
python3 cerveau-projet/matrix/lancer.py poser-template-pilote lister
python3 cerveau-projet/matrix/lancer.py poser-template-pilote poser --moule suivi-bdd/suivi.md.moule \
       --cible <chemin cible> --jeton NOM_SUIVI=mon-suivi --jeton APPARTIENT_A=optimus-prime ...
```

La porte : lit le MOULE (jamais un artefact vivant), remplace les jetons EN MEMOIRE,
REFUSE un jeton non remplace, refuse un moule sans aucun jeton, valide le contenu
(`.json` par `json.load`, `.py` par `py_compile`) AVANT d'ecrire, et publie par la
PORTE ECRIRE -- jamais a la main.
