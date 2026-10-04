---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
  flux: 2
  role: attelage des equipements d'Optimus (inventaire et comparaison)
---

# REMORQUE-OPTIMUS -- carte d'identite

> Le `README.md` de ce dossier explique le POURQUOI (ce que porte la remorque,
> ce qu elle ne partage pas avec le sac-a-dos du cameleon). Cette carte repond
> a la seule question du lanceur : **QUOI est ce fichier, et qui l ecrit**.
> Les deux ne se recopient pas.

## Ce que le lanceur juge ici

`remorque-optimus.py` ecrit `inventaire.json`. Toute ecriture doit etre
attribuable a une porte ; sans carte, le lanceur ne peut pas juger et le DIT
(`[SANS CARTE]`) -- l'ecriture partait alors sans attribution.

## Verbes

| Verbe | Effet |
|---|---|
| `inventorier` | regenere `inventaire.json` depuis le reel |
| `etat` | compare inventaire et reel, nomme manquants et inattendus |

Usage par le lanceur (jamais par un chemin recopie) :

```
python3 cerveau-projet/matrix/lancer.py remorque-optimus inventorier
python3 cerveau-projet/matrix/lancer.py remorque-optimus etat
```

## Codes de sortie

0 : concordance ; 1 : ecart nomme ; 2 : refus.

## Ce que l outil ne fait pas

Il ne supprime rien et ne repare rien : il DECRIT l'equipement, la reparation
reste hors de la remorque (proto-8). Les points de restauration `.bak` sont
comptes comme etat de transaction, jamais comme equipement.