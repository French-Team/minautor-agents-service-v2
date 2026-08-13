# Controle croise -- Axe D : elargir la carte et les declencheurs de Themis

- **Date** : 2026-08-13
- **Controleur** : Janus (second controle, dernier maillon de la chaine)
- **Mission** : Buffy (axe D, demande utilisateur) -- Themis maillon automatique de la chaine
- **Verdict** : **VALIDE (J1-J7 verts)**

## Contexte

Themis avait une faiblesse declaree 'Depend de Cerberus pour etre activee' : les
agents avaient une case 'Activer Themis pour auditer' mais AUCUNE fin de mission ne
l activait systematiquement. L axe D rend Themis automatique en fin de mission.

## Verifications

| Point | Verification | Resultat |
|---|---|---|
| J1 | valider-case 6 parcours (buffy/vulcain/morpheus/atlas/clio/themis) | 6/6 CONFORME |
| J2 | valider-cartes-decision 6 agents | 6/6 CONFORME |
| J3 | detecter-cablages-manquants 6 parcours | PROPRE (0 cas orphelin, 0 ref morte) |
| J4 | navigation reelle buffy c22a -> c22b (OUI) -> c22 | PARCOURS TERMINE |
| J5 | test-018 (fins reactiver) + test-033 (passage Janus) | 13/13 + 9/9 OK |
| J6 | normes ASCII + LF (13 fichiers) + 0 residu temp | 0/0, 0 residu |
| J7 | fiches Pattern 14 (6 versions PARCOURS) + faiblesse Themis retiree | a jour |

## Livrables controles

1. **5 parcours modifies** (18 cases ajoutees, versions bumpees) :
   - buffy v0.4.2 : c8a/c8b, c22a/c22b, c27a/c27b
   - vulcain v0.4.5 : c9f/c9g, c15f/c15g
   - morpheus v0.4.4 : c10a/c10b, c14a/c14b
   - atlas v0.4.2 : c11a/c11b
   - clio v0.5.4 : c12a/c12b
   - Chaque fin de mission est precedee de : action 'Activer Themis pour auditer ma
     mission' (commande exacte `activer session-llm-1 themis`) -> controle
     'Retour de Themis recu ?' (OUI -> fin existante / NON -> soi-meme = attente).
2. **Carte themis v0.4.2 elargie** : branche 'audit-fin-mission' dans c1 -> c25
   (Auditer pour un agent) + message c25 enrichi (audit de fin de mission).
3. **Fiche themis** : faiblesse 'Depend de Cerberus pour etre activee' RETIREE
   (remplacee par une force : activee automatiquement en fin de mission) +
   declenchement enrichi + Pattern 14 v0.4.2.
4. **Lecon Buffy** ajoutee a corrections.md.

## Decision de conception validee

- **Point d insertion : Themis AVANT Janus** -- la REGLE IMMUABLE JANUS exige que
  Janus soit le dernier maillon qui reactive Cerberus (test-018 : seule fin
  REACTIVER-CERBERUS = janus c10). Nouvelle chaine :
  `Cerberus -> Agent -> Themis -> Agent -> Janus -> Cerberus`.
- **Mecanique de case** : impossible de mettre un 'suivant' sur une fin (garde-fou
  suivant mort) -> action + controle de re-essai (NON -> soi-meme, pattern natif).
- **janus non modifie** : sa fin c10 est REACTIVER Cerberus (il est le dernier
  maillon) -- la mission le listait par erreur.

## KO attendus (adaptations Morpheus a venir)

- test-004 : parcours morpheus v0.4.3 -> v0.4.4 (1 KO)
- test-016 : parcours buffy v0.4.1 -> v0.4.2 + compteurs (3 actions/3 controles en
  plus) (3 KO)
- Les autres tests (018, 033, etc.) restent verts : les fins 'FIN - Activer Janus'
  sont inchangees, seules les etapes Themis s y inserent avant.
