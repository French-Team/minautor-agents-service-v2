# OUTIL -- vie (activateur de la Matrice)

> Premier outil de la famille `routines/vie/` : DEMARRE et ARRETE la vie
> de fond de la Matrice. La veille-flux et l'espion-integrite ont chacune
> leur boucle ; cet activateur les lance EN DETACHE (elles survivent a la
> session) au demarrage de la Matrice -- c'est le raccord du statut
> "Auto-activation de la veille" (E-019 -> M-046).

## Options

```
python main.py etat                        -> etat des boucles (ARRET / ACTIVE / fantome nettoye)
python main.py activer                     -> lance veille-flux + espion-integrite en detache
python main.py activer --intervalle <s>    -> lancement avec intervalle personnalise
```

## Garanties

- LANCEMENT DETACHE : DETACHED_PROCESS + CREATE_NEW_PROCESS_GROUP -- la boucle
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
reste le point d'entree du createur : il y ajoutera une ligne
`python cerveau-projet/matrix/matrice/routines/vie/main.py activer` quand il voudra.
