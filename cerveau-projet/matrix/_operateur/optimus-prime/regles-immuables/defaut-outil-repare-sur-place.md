---
identite:
  type: regle-immuable
  appartient_a: optimus-prime
  commun: false
  decide_par: createur
  date: 2026-09-18
---

# REGLE IMMUABLE -- UN DEFAUT D OUTIL SE REPARE DANS L OUTIL

> Gravee le 2026-09-18 (GO createur, EO-162 / MO-174, audit
> `audits/audit-pilote-erreurs-travail.md`). Avant elle, la garantie n existait
> NULLE PART : ni dans les regles immuables, ni dans la fiche, ni dans un
> protocole. La mesure qui l a rendue necessaire : la reparation de la porte
> `ecrire` (MO-173) n avait laisse qu un RECIT dans un bilan de fin de mission --
> aucun fait structure, aucun texte interdisant le contournement.

## La regle

Quand un OUTIL se comporte mal PENDANT que je travaille (mauvaise sortie, refus
injustifie, plantage, silence), je NE contourne JAMAIS par un geste manuel :

1. **REPRODUIRE** le defaut avant de decider (meme entree, meme sortie fausse).
   Un defaut non reproduit n est pas repare : il est seulement constate.
2. **REPARER DANS L OUTIL** -- la cible est l outil, jamais l appelant, jamais la
   donnee. Un correctif qui vit A COTE de l outil est INTERDIT : c est le defaut
   meme, deplace.
3. **PROUVER** : un cobaye rejoue l ANCIENNE regle et l ACCUSE (`verifier-*`,
   super-combos). Une reparation sans preuve est une opinion.
4. **TRACER** : BDD modifications pour le fichier + marbre pour l evenement. Une
   reparation non tracee est invisible : la prochaine session la refera.
5. **REPRENDRE** la mission la ou elle s est arretee (`proto-1-reprise-mission.md`,
   ETAPE 0) : la reparation ne coute pas la mission.
6. **HORS PERIMETRE -> INTER-ROUND** : si la reparation sort de mon perimetre, je
   la SIGNALE au pilote et je ne l improvise jamais (`proto-9-mini-missions-inter-round.md`).

Route complete en 8 temps : `protocoles/proto-10-route-outil-defaillant.md`.
Case de theme : `parcours/themes/theme-auto-correction.json` (case OUTIL).

## Ce qui est INTERDIT (les contournements, tous)

| Geste | Pourquoi c est le defaut, pas la solution |
|---|---|
| Retaper a la main ce que la porte devait ecrire | le prochain appelant retombe sur le defaut, et personne ne le sait |
| Detourner la porte (mode degrade, option de secours) | le defaut reste, il est seulement moins visible |
| Contourner par un autre outil | deux verites pour une seule chose (L-029/L-102) |
| "Reparer" la donnee pour faire taire l outil | l outil accusera la prochaine donnee valide |
| Noter le defaut puis continuer | un defaut signale mais non repare revient au prochain round |

## Ce que la regle N EXIGE PAS

- Elle n exige PAS la reparation immediate quand la mission est critique ET que le
  defaut est HORS PERIMETRE : elle exige de le DIRE (inter-round) puis de reprendre.
- Elle n autorise PAS a reparer un outil CRITIQUE sans le createur : le risque
  CRITIQUE reste au createur (`proto-2-auto-evolution.md`).

Source : consigne du createur du 2026-09-18 -- "il faut les corriger avant de
continuer et ne pas esquiver en codant a la main si c est le code qui devait le
faire (le but etant de reparer nos process en temps reel)".
