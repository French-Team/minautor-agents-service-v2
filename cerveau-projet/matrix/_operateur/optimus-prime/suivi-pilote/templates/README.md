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
| `raisonnement/segment.md.moule` | un SEGMENT de raisonnement (carte + ce qui est ETABLI + ce qui RESTE ouvert) | `poser-template-pilote` |
| `regles-immuables/regle-immuable.md.moule` | une REGLE IMMUABLE de la zone invisible (regle + source + contre-exemple + exception nommee) | `poser-template-pilote` |
| `conventions/convention.md.moule` | une CONVENTION de la zone invisible (regle de forme + format + source + cas limites) | `poser-template-pilote` |
| `protocoles/protocole.md.moule` | un PROTOCOLE de la zone invisible (declencheur + gestes ordonnes + arret + regle jumelle) | `poser-template-pilote` |

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
| `__TITRE__` | le sujet de la piece, en 3 a 6 mots | la loi du round |
| `__LIENS__` | les chemins canoniques lies (le readme de la zone, le jumeau) | conventions/conventions-readme.md |
| `__REGLE__` | la regle elle-meme (forme pour une convention, consigne pour une regle) | une mission a la fois |
| `__FORMAT__` | le gabarit de sortie, au point pres | le format d un indices.md |
| `__SOURCE__` | la demande ou la lecon qui a fait naitre la piece | lecon directrice du createur |
| `__MESURE__` | le fait mesure qui rend la piece necessaire, compte et date | 3 bilans ecraseS par 1 |
| `__REMPLACE__` | l usage anterieur sans forme, ou RIEN | la relecture a la main |
| `__CAS_LIMITES__` | ce qui se passe aux bornes, nomme | une zone sans indices |
| `__CONTRE_EXEMPLE__` | ce qui arrive si on n applique pas la regle | deux missions en parallele |
| `__PERIMETRE__` | ce qui est concerne, et ce qui ne l est pas | tout l operateur |
| `__EXCEPTION__` | l exception nommee, ou AUCUNE | AUCUNE |
| `__GARDE__` | l instrument qui verifie la regle | verifier-regles |
| `__NUMERO__` | le numero du protocole (jamais reutilise) | 12 |
| `__QUAND__` | le declencheur, en une ligne | au demarrage, avec le reste de la reprise |
| `__GESTES__` | la suite de gestes, numerotee, une preuve par geste | 1. lire la fiche, 2. deposer |
| `__ARRET__` | ce qui rend le protocole TERMINE, et ce qu il vaut sinon | le bilan de la mission |
| `__JUMELLE__` | la regle ou le protocole voisin, lu avec | regles-immuables/evolution-decidee.md |

> CE QUE CETTE TABLE DIT, ET CE QU ELLE NE DIT PAS. Elle dit ce qu un jeton
> **SIGNIFIE** -- la seule chose qu un moule ne peut pas dire, puisque lui ne
> contient que le trou. Elle ne dit pas quels jetons **EXISTENT** : cette liste la
> lit la porte, dans les moulES eux-memes (`lister` la publie, jeton par jeton).
> La recopier ici serait en faire une deuxieme source, et elle tairait les
> families de demain -- c est le meme argument qui fait extraire les identifiants
> par FORME (`_ids_dans`, MO-548) plutot que par une liste recopiee.

## Pourquoi ces trois moules (la mesure qui les a fait naitre)

Ce bloc est ici, et NON dans les trois moules : c est la raison d etre du PATRON.
Mesure dans le fichier, elle atterrirait dans chaque convention, chaque regle et
chaque protocole pose -- avec le risque de s y perimer en silence, ce qui est
arrive : le moule des regles citait < 23 regles >, il y en a **19**.

| Famille | Mesure au 2026-10-02 (compte reel, hors `.bak`) | Ce que le patron comble |
|---|---|---|
| regles immuables | 19 regles + 1 readme | aucune ne disait ce qui rend une regle IMMUABLE (source, contre-exemple, perimetre, exception nommee, garde) : chacune se relisait en entier pour en deduire la forme |
| conventions | 14 conventions + 1 readme | aucune ne disait ce qu une convention a le droit de dire -- et elle empietait sur la regle (quoi faire) et sur la lecon (pourquoi) |
| protocoles | 14 protocoles numerotes + 1 readme | la numerotation SILENCIEUSE : aucun ne disait ce qui distingue un protocole d une regle, donc deux protocoles de meme sujet avaient deux formes |

Le patron de la zone VISIBLE existait deja (`matrice/templates/`, consomme par
`dupliquer-template`). Celui-ci est son jumeau pour l invisible : L-016 tranche,
un moule invisible ne sert que de l invisible.

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
