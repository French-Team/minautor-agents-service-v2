---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
  flux: 2
  role: surveillance de la zone Optimus (les espions signalent, ils ne reparent jamais)
---

# ESPIONS-OPTIMUS -- carte d'identite

> Le `README.md` de ce dossier explique le **pourquoi** de la zone (pourquoi la
> zone `_operateur/optimus-prime/` est surveillee, et par quoi). Cette carte
> repond a la seule question du lanceur : **quoi est ce dossier, qui y ecrit**.
> Les deux ne se recopient pas.

## Ce que le lanceur juge ici

Les quatre espions de ce dossier lisent la zone et **signalent** ; ils ne
reparent jamais (la reparation passe par Optimus). Sans carte, le lanceur ne
pouvait pas juger et le disait (`[SANS CARTE]`) : chaque ecriture partie de
cette zone sortait non attribuee.

## Les quatre espions

| Espion | Ce qu il surveille |
|---|---|
| `espion-integrite-optimus.py` | empreintes SHA de la zone (detection d une modification hors BDD) |
| `espion-activite-optimus.py` | file de missions, frictions actives, verrous BDD non liberes |
| `espion-sondes-optimus.py` | sondes de vivacite des processus |
| `espion-tracebacks-optimus.py` | tracebacks d'outils, conserves pour diagnostic |

## Le registre

`registre/` porte ce que les espions **possedent** (et non ce qu'ils lisent) :
`registre.json` (empreintes de zone), `sondes.jsonl`, `tracebacks-historique.jsonl`.
Chaque espion declare (`PRODUCTIONS`) ce qu il ecrit ; une case vide y signifie
`je n'ecris rien`, ce qui est vrai pour un espion qui ne fait que lire et
signaler.

## Codes de sortie

0 : rien a signaler ; 1 : ecart nomme ; 2 : zone introuvable.

## Ce que ces outils ne font pas

Ils ne reparent pas. Un ecart detecte est un **signalement**, jamais une
correction : la zone surveillee appartient a Optimus, et l'outil qui la
reparerait se surveillerait lui-meme.