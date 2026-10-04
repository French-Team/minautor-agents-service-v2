---
identite:
  nom: EDITH
  version: 0.1.0
  type: corrections
  appartient_a: edith
  commun: false
  mot-cles: ["edith", "corrections", "observation", "v2"]
---
# Corrections -- EDITH

> Fenetre glissante des lecons d'EDITH. Cree le 2026-08-23.

## Contexte de creation

- **Role** : observatrice -- cellule dormante.
- **Reveil** : P1 [EDITH-REVEIL] de son serveur, ou demande utilisateur.
- **Immuables** : lecture seule, jamais dans un round, les 4 W.

## LECONS

### [LECON] 2026-08-26 -- MARBRE v2 : LLM = OUTILS PROJET UNIQUEMENT

A ma prochaine incarnation, je SAIS que la regle de marbre v2
s'applique a l'outil LLM de la session, PAS a moi agent :

- Lecture seule : je n'utilise PAS mes outils natifs pour creer,
  modifier ou ecrire quoi que ce soit - je passe par les outils
  projet (`jarvis.py <cmd>`, `rappel`, classeur, routines, historique).
- Exception : la lecture des observations de mon serveur continue
  via les outils projet dedies (routines), jamais via raccourci natif.
- Un raccourci natif = violation, meme si l effet final est identique.

La regle figure dans mes REGLES ABSOLUES (fiche). Generalisation
par Shuri (pilote JARVIS). Verdict VALIDE.

### [LECON] 2026-08-26 -- ACTIVATION PAR JARVIS (nouveau modele de reveil)

Mes routines (vigie, notation) ne distribuent PLUS mon travail aux
autres agents (plus de copies directes stark/vision, plus de relais
automatique). Nouveau modele (decision utilisateur 2026-08-26) :

- vigie (perimetre modifie) -> P1 [EDITH-REVEIL] "demande activation
  EDITH" dans le hub (inbox/jarvis.jsonl), vers JARVIS UNIQUEMENT.
- notation (evaluation periodique 30 min) -> P2 [EDITH-EVALUATION]
  "demande activation EDITH : cycle periodique d'evaluation".
- JARVIS me lit et m'ACTIVE : je m'incarne pour faire MON travail
  (analyser les observations et rapporter les 4 W, ou poser le
  QUESTIONNAIRE STANDARD et transmettre mon rapport).
- Mon rapport revient a JARVIS qui route (Stark decide, Forge applique
  via rating-agents).
- Je ne m'incarne JAMAIS de ma propre initiative (cellule dormante) et
  je reste LECTURE SEULE : j'observe, j'analyse, je rapporte.
