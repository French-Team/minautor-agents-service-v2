---
identite:
  type: routine
  appartient_a: matrice-routines
  commun: true
---

# OUTIL -- vie (activateur de la Matrice)

> Premier outil de la famille `routines/vie/` : il DETIENT la vie de fond de la
> Matrice, en DEUX modes (decision du createur D1-D2, MO-429) :
> - le PLANNING (`planning.json`) est la SOURCE des cadences, des modes
>   (`boucle` | `passe`) et de la rotation d allumage (decalage initial) ;
> - le SERVER MATRICE supervise les routines en `boucle` (il les adopte ou les
>   lance, les surveille et les relance sans fenetre -- M-081) ;
> - le SERVICE (`service/`) sert les routines en `passe` : il les ALLUME
>   individuellement quand leur cadence est echue, RECOIT leur resultat (code,
>   trace de lancement, passe publiee) et TRANSFORME les ecarts en MESSAGES
>   (porte `signaler`, niveaux declares, montee defcon sur le critique -- D4b).
> Une routine en mode `passe` est ETEINTE entre deux passes par conception :
> plus de boucle residente, plus de pics des sept au demarrage.

## Options

```
python3 cerveau-projet/matrix/lancer.py vie etat -> etat des boucles (ARRET / ACTIVE / PASSE eteinte / fantome nettoye)
python3 cerveau-projet/matrix/lancer.py vie activer -> lance le server matrice (porte unique)
python3 cerveau-projet/matrix/lancer.py vie activer --intervalle <s> -> lancement du server avec intervalle personnalise
python3 cerveau-projet/matrix/lancer.py vie server arret -> arret cooperatif du server et des boucles
python3 cerveau-projet/matrix/lancer.py vie service etat -> le PLANNING lu : cadence, mode, derniere passe, DUE / pas due
python3 cerveau-projet/matrix/lancer.py vie service tour [--racine X] -> UN tour : allume la routine DUE, recoit, signale
```

## Garanties

- LANCEMENT DETACHE SANS FENETRE (E-056, M-081) : motif UNIQUE partage
  data/commun/lancement.py (Windows : CREATE_NO_WINDOW + CREATE_NEW_PROCESS_GROUP
  + startupinfo SW_HIDE ; POSIX : start_new_session) -- aucune fenetre console
  n'apparait jamais, le redemarrage d'une routine est invisible pour le createur.- SERVER MATRICE (E-056, M-081) : server_matrice.py surveille les trois boucles en
  continu et RELANCE toute routine morte (arret cooperatif : main.py server arret) ;
  chaque routine est une fille du server, jamais lancee en direct par l'activateur --
 la boucle
  survit a la session qui l'a demarree, zero processus fantome a la fermeture.
- GARDE DE DOUBLE LANCEMENT : chaque routine porte SON PID (veille-flux.pid,
  espion.pid) et refuse elle-meme un second lancement ; l'activateur
  verifie AVANT et ne contourne jamais ce garde.
- PID FANTOME NETTOYE : un fichier PID dont le processus est mort est
  supprime automatiquement (etat comme activation), la boucle repart propre.
- ARRET COOPERATIF : l'arret reste celui des routines elles-memes
  (`veille-flux/main.py veille arret`, `espion-integrite/main.py boucle arret`)
  -- zero processus tue de l'exterieur.

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| DESCRIPTION.md | la facade (ce fichier) |
| main.py | point d'entree global : DIRIGE |
| planning.json | LE PLANNING des routines (cadence, mode, decalage, priorite, commande de passe) -- source unique (D1) |
| constants.py | chemins des boucles, noms de PID, tables uniques, constantes du service |
| fonctions.py | sondage processus, nettoyage PID fantome, lancement detache, cadence declaree (renvoi au planning) |
| activer.py | orchestre le lancement des boucles en mode `boucle` |
| etat.py | affiche l'etat des boucles (et le MODE lu au planning) |
| server_matrice.py | le serveur : surveille les `boucle`, saute les `passe`, appelle le service a chaque cycle |
| service/entry.py | porte `vie service` (etat, tour) |
| service/fonctions.py | ALLUMER (drapeau retire, plafond), RECEVOIR (code, trace, passe publiee), SIGNALER (niveaux + defcon) |

## Raccord demarrage

`demarrer-optimus-prime.md` (racine, hors perimetre d'ecriture de l'operateur)
reste le point d'entree de developpement : il pourra appeler
`python3 cerveau-projet/matrix/matrice/routines/vie/main.py activer`.
Le demarrage final de production de la Matrice et du cameleon sera defini
par le futur fichier de demarrage global ; Optimus Prime reste reveille
pendant cette construction puis sera sollicite seulement au besoin.
