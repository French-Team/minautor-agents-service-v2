---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# AUDIT -- LE DECLENCHEMENT DEFCON EST-IL BRANCHE ? (MO-242, lecture seule)

L audit instruit affirmait : LA MONTEE EST BRANCHEE, LE DECLENCHEMENT NE L EST PAS (ZERO appelant
de machine-defcon hors son propre dossier ; le cockpit nommerait ses seuils proto-2 DECLENCHEURS).
LA MESURE REFUTE LES TROIS AFFIRMATIONS.

## 1. Le declenchement automatique EXISTE et TOURNE

- `matrice/routines/veille-flux/passe/fonctions.py` ligne 111 : la passe VIGILE appelle
  `machine-defcon surveiller` a chaque tour. La veille est VIVANTE : passe-fin a 18:57:03,
  intervalle 300 s (journal-veille.txt), et le maillon 3 de la non-regression la declare saine.
- `machine-defcon/surveiller/entry.py` : le verbe EVALUE les declencheurs declares et POSE le
  niveau -- par la PORTE `monter` (ligne 42), jamais par une ecriture directe, donc chaque
  declenchement est journalise et, a 5, met la session en pause.
- Mesure qui refute le zero appelant : 17 fichiers citent machine-defcon, dont la veille, le
  pilote (filtrer, garde session_en_pause a l injection) et le cockpit.

## 2. Les declencheurs sont DECLARES, MESURABLES et MORTELS-INTERDITS

Trois conditions dans machine-defcon/constants.py, chacune nommant le FAIT, le MESUREUR, le SEUIL
et le NIVEAU : perimetre-write (niveau 5), marbre-hors-porte (niveau 5), perimetre-tmp (niveau 4).
Les trois mesureurs existent REELLEMENT (garde-perimetre-write.py, verifier-regles/main.py,
garde-tmp.py). Le code dit lui-meme pourquoi ils sont branches : un declencheur ecrit mais jamais
branche serait un declencheur MORT -- le defaut trouve par l audit EO-181, deja repare ici.

## 3. Le cockpit separe DEJA le faux du vrai

cockpit-matrice.py : les seuils proto-2 sont affiches comme SUGGESTION (ce ne sont PAS des
declencheurs) ET une section DECLENCHEURS REELS (AUTOMATIQUES -- poses par machine-defcon/
surveiller) les lit en direct. La troisieme affirmation de l audit est donc perimee.

## 4. La trace fonctionne

defcon-historique.jsonl : 12 transitions, chacune avec sa source (machine-defcon monter /
descendre / valider). Les dernieres datent du test M-080 (2026-09-09).

## ECART RESIDUEL SIGNALE A LA MATRICE (jamais corrige ici : l auditeur ne repare pas)

La chaine est branchee de bout en bout, mais son ALLUMAGE POSITIF n a JAMAIS ete observe en
production : les passes de veille rendent detections 0 et aucune transition defcon n a eu lieu
depuis les tests du 09-09. Rien ne prouve donc, mesure a l appui, qu un mesureur qui rendrait
code 1 FERAIT monter le niveau et armerait la pause -- c est la seule case non cochee. Le remede
est un cobaye en classeur JETABLE (force un mesureur a code 1, verifie la montee et la pause),
jamais une montee sur le vivant : cela mettrait la session en pause pour de vrai.

## CE QUE CET AUDIT ENSEIGNE (a graver par la Matrice)

Troisieme fois de la journee qu une premisse ecrite depuis un etat ANCIEN est refutee par la
mesure (MO-240, MO-241, MO-242) : un audit instruit qui n est pas re-mesure avant d etre servi
transmet un verdict faux -- et un verdict faux coute plus cher qu aucun verdict.
