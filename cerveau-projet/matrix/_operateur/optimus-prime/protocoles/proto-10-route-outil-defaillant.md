---
identite:
  type: protocole
  appartient_a: optimus-prime
  commun: false
---

# PROTOCOLE 10 -- ROUTE OUTIL DEFAILLANT (de la seance au retour vert)

> Source : regle immuable `regles-immuables/defaut-outil-repare-sur-place.md`
> (GO createur 2026-09-18, EO-162 / MO-174) et audit
> `audits/audit-pilote-erreurs-travail.md` (les 8 devoirs D1..D8). Cette route est
> celle du defaut trouve **PENDANT** que je travaille -- par opposition a `proto-8`,
> qui traite une mission bloquante deposee par la VEILLE.

## La route (8 temps, D1..D8)

1. **D1 DETECTER** : le defaut se voit a l usage (sortie fausse, refus injustifie,
   plantage, silence). Je l annonce AVANT de le reparer : c est un fait de seance,
   pas une opinion.
2. **D2 REPRODUIRE** : je relance le MEME appel, sur la MEME entree, et je confirme
   le meme ecart. Non reproduit = constate : je ne "repare" jamais a l aveugle.
3. **D3 QUALIFIER** : MINEURE (coquille de sortie, message), MOYENNE (refus
   injustifie, garde trop large), GRAVE (perte de donnees, ecriture partielle,
   silence sur une erreur). Un defaut d OUTIL n est PAS une erreur de DONNEES :
   la cible est l outil.
4. **D4 METTRE LA MISSION EN PAUSE** : serie stricte -- on ne continue pas sur un
   outil douteux. La pause est nommee dans le bilan ; la mission n est jamais
   perdue (elle reprend au temps 8).
5. **D5 REPARER DANS L OUTIL** : un changement minimum, la CAUSE et non le
   symptome, par la porte officielle (point de restauration `.bak`). Jamais un
   geste manuel qui esquive l outil, jamais un correctif A COTE.
6. **D6 PROUVER** : un cobaye rejoue l ANCIENNE regle et l ACCUSE, et le cas
   nominal passe. La preuve est un RESULTAT lu, pas une attente.
7. **D7 TRACER** : BDD modifications (le fichier repare) + marbre (l evenement :
   quel outil, quelle cause, quelle preuve). Une reparation non tracee est
   invisible.
8. **D8 REPRENDRE / ALERTER** : je reprends la mission la ou elle s est arretee
   (`proto-1-reprise-mission.md`, ETAPE 0). Si la reparation sort de mon
   perimetre : INTER-ROUND -- je SIGNALE au pilote (`[alerte]` -> machine-defcon)
   et je ne l improvise jamais (`proto-9-mini-missions-inter-round.md`).

## Quand l utiliser

- Un outil refuse un appel qui DEVRAIT passer (faux refus) ;
- un outil accepte un appel qui DEVRAIT etre refuse (garde trop large) ;
- un outil annonce un echec alors qu il a REUSSI (faux echec) ;
- un outil se tait sur une erreur (silence = defaut, jamais un confort) ;
- deux textes se CONTREDISENT (le defaut est la contradiction, pas l un des deux).

## Interdits

- Ecrire la sortie a la main "pour ne pas perdre de temps" (regle immuable).
- Reparer l appelant pour contourner l outil (le prochain appelant retombe dessus).
- "Reparer" la donnee pour faire taire un outil a tort.
- Continuer la mission sur un outil douteux (serie stricte).
- Deux reparations d outils en meme temps, ou deux outils dans la meme reparation.

## Rappel du pilote

Le pilote porte la ROUTE (crochet `[outil]`, `fin --defauts <fiche>`) : le defaut
repare et prouve est consigne AVEC la mission, pas seulement raconte dans un bilan
en texte libre.
