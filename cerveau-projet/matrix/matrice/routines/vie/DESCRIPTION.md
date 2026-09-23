# OUTIL -- vie (activateur de la Matrice)

> Premier outil de la famille `routines/vie/` : DEMARRE et ARRETE le
> server matrice, unique proprietaire de la vie de fond. Le server adopte
> ou lance les trois routines (veille-flux, espion-integrite, suivi-sync),
> les supervise et les relance sans fenetre -- c'est le raccord du statut
> "Auto-activation de la veille" (E-019 -> M-046) et du server M-081.

## Options

```
python3 cerveau-projet/matrix/lancer.py vie etat -> etat des boucles (ARRET / ACTIVE / fantome nettoye)
python3 cerveau-projet/matrix/lancer.py vie activer -> lance le server matrice (porte unique)
python3 cerveau-projet/matrix/lancer.py vie activer --intervalle <s> -> lancement du server avec intervalle personnalise
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
| constants.py | chemins des boucles, noms des PID |
| fonctions.py | sondage processus, nettoyage PID fantome, lancement detache |
| activer.py | orchestre le lancement des deux boucles |
| etat.py | affiche l'etat des boucles |

## Raccord demarrage

`demarrer-optimus-prime.md` (racine, hors perimetre d'ecriture de l'operateur)
reste le point d'entree de developpement : il pourra appeler
`python3 cerveau-projet/matrix/matrice/routines/vie/main.py activer`.
Le demarrage final de production de la Matrice et du cameleon sera defini
par le futur fichier de demarrage global ; Optimus Prime reste reveille
pendant cette construction puis sera sollicite seulement au besoin.
