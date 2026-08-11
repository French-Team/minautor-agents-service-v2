# Controle croise -- valider-case.md aligne budget pondere (Janus)

**Date** : 2026-08-11
**Mission** : controle croise de l'alignement du .md de valider-case sur le budget pondere (correction par Vulcain)
**Verdict** : **VALIDE** (6 points J1-J6 verts, non-regression 22/22)

## Points controles

| # | Controle | Resultat |
|---|---|---|
| J1 | Ancienne regle ("> 3 indices" / "plus de 3 indices") : 0 dans valider-case.md ET 0 dans tous les .md de tools/ (hors spec, deja propres) | OK |
| J2 | Budget pondere dans valider-case.md : 2 mentions (historique l.13 + tableau Allegement l.55) | OK |
| J3 | Normes : non-ASCII 0, CRLF 0 | OK |
| J4 | Tests : test-009 23/23, test-015 10/10 | OK |
| J5 | Non-regression complete : 22/22 OK | OK |
| J6 | Coherence des seuils : 100 / 0,5 / 1 / 3,0 / 160 identiques dans valider-case.md + 3 specs (refonte v0.1.3, valider-case v1.1.0, guider-parcours v0.6.2) | OK |

## Corrections validees

| Element | Correction |
|---|---|
| valider-case.md l.55 (tableau Allegement) | "case avec > 3 indices OU texte de regle > 160 caracteres" -> "budget pondere des indices : COURT (<= 100 car. ou sans texte) = 0,5 unite, LONG (> 100 car.) = 1 unite, budget 3,0 par case (6 courts = 3,0 OK) ; texte de regle > 160 caracteres = SIGNALEE avec proposition de reference" |

## Observations

- **guider-parcours.md v0.5.0** : aucune mention de surcharge/allègement. C'est CORRECT : la doc d'usage du navigateur ne couvre pas la surcharge (domaine de valider-case). Rien a corriger.
- La version du .md guider-parcours (0.5.0) est alignee sur le py (0.5.0) ; la spec est en 0.6.2 (cas inverse connu : py en retard, observation pour une mission Vulcain).

## Lecons

1. Le .md d'un outil peut etre incoherent INTERNEment : historique v1.1.0 (budget pondere) OK mais tableau Allegement avec l'ancienne regle. Verifier toutes les sections, pas seulement la version.
2. Le scan complet (grep "> 3 indices" sur tous les .md de tools/) confirme l'absence totale de residue : le budget pondere est desormais documente partout (3 specs + .md valider-case + code + tests).
3. Une doc d'outil qui ne mentionne pas la surcharge (guider-parcours.md) n'est PAS un ecart si le sujet est hors de son perimetre : verifier la pertinence avant de corriger.
