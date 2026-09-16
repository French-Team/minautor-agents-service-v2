---
identite:
  type: protocole
  appartient_a: optimus-prime
  commun: false
---

# Proto 9 -- Mini-missions + inter-round (Matrice)

> Source : inter-round v1 (modele aero : erreur hors-perimetre ->
> signalement ORACLE, pilote largue l habilite, l appelant reprend son
> round) + mission M-097. Adapte a la Matrice single-LLM : tout est
> serie, Optimus incarne chaque etape.

## MINI-MISSION (unite de travail)

- Une mission = 2 a 5 mini-missions en SERIE STRICTE.
- Une mini-mission = UN seul changement + SA preuve + SA trace BDD.
- Format : `<MISSION>.mini-<N>` (ex M-098.mini-1), objectif une phrase,
  preuve exigeable en une commande.
- Echec de preuve -> revert -> 1 retry -> 2e echec = ESCALADE createur
  (on ne boucle jamais plus de 2 fois).

## INTER-ROUND (gestion erreur sans casser le flux)

1. Erreur hors-perimetre detectee pendant mini-N : NE PAS interrompre
   la mission, NE PAS repartir de zero.
2. Signaler : noter friction BDD + mission inter-round deposee
   (entonnoir deposer --source inter-round, ou mission-creee journal).
3. Reparer : executer la mini-mission de reparation (serie, une par une).
4. Reprendre : revenir a mini-N et la REJOUER depuis son debut
   (les mini 1..N-1 restent acquises, jamais rejouees).
5. Tracer : bilan inter-round dans le bilan de la mission appelante.

## SUIVI (Optimus declare lui-meme, le pilote ne le fait pas)

- A l ouverture de chaque mission : `suivi-optimus noter --mission <ID>
  --theme <THEME> --action debut --detail "<prise en charge>"`.
- A la cloture de chaque mission : meme porte avec `--action fin` + bilan.
- Plusieurs missions = plusieurs debuts + plusieurs fins (un par mission).
- Le pilote ne note RIEN pour Optimus : pas de chemin pilote->Optimus.

## REGLES

- JAMAIS 2 mini-missions simultanees (serie stricte heritee du pilote).
- JAMAIS sauter une preuve de mini-mission (pas de preuve = pas d acquis).
- JAMAIS plus de 2 tentatives sur la meme mini-mission (escalade).
- Inter-round = reparation exclusive par mini-mission dediee, jamais
  en bricolant dans la mini-mission courante.
