# Controle Janus -- Cycle pilote Chiron reel (verification bout en bout)

**Date** : 2026-08-18
**Controleur** : Janus (controleur des statuts, session habilitee)
**Cible** : carte chiron (parcours-chiron.json v0.3.0, case c18 corrigee)
**Contexte** : demande utilisateur "Verifier que Chiron peut reellement executer son cycle d auto-correction de bout en bout". Chaine : Cerberus -> Chiron (detecte + corrige SA carte) -> Themis (audit CONFORME) -> Chiron (reprend) -> Janus (controle final).

## L incoherence reelle detectee et corrigee par Chiron

- **c18 (Retour de Themis recu ?)** : le texte de la regle annoncait "A REVOIR -> NON (retour c15)" mais la branche JSON NON allait vers c18 (attente) -- le cas A REVOIR n avait AUCUNE branche. Texte : 168 caracteres (> 160).
- **Correction (editer-parcours --modifier-case, verrou pilote SA carte OK)** : 3 branches explicites :
  - OUI (CONFORME) -> c12 (reprendre)
  - A REVOIR -> c15 (retour corriger)
  - NON (pas revenue) -> c18 (attendre, re-essai legitime)
  - Texte aligne : 151 caracteres. Lock resynchronise automatiquement par editer-parcours.

## Preuves du cycle bout en bout

| Etape du cycle | Preuve |
|---|---|
| c11b (MA carte ?) | OUI -> c15 (navigation verifiee) |
| c15 (se re-eduquer) | lecon BDD id 58 (Chiron, domaine auto-correction) |
| c16 (corriger SA carte) | editer-parcours --modifier-case c18, verrou pilote a AUTORISE (SA carte) |
| c17 (activer Themis) | activation reelle, audit CONFORME (rapport + lecon 59) |
| c18 (reprendre) | CONFORME -> c12 -> c13 -> c14 FIN ; A REVOIR -> c15 ; NON -> c18 |

## Verifications sous session habilitee (Janus)

| Verification | Resultat |
|---|---|
| valider-cartes-decision --agent chiron | **CONFORME** (dont point 10 : coherence fiche/parcours) |
| c18 branches | 3 (CONFORME/A REVOIR/NON), texte 151 car |
| Lock marbre | MATCH (hash resynchronise) |
| Navigation c18 | A REVOIR -> c15, OUI -> PARCOURS TERMINE, NON -> c18 |
| test-006 (cartographie) | 19/19 VALIDE |
| test-027 (series-garde-fou) | 11/11 OK |
| Bumper --tous | 0/0 coherent |
| Marbre --tous | 8/8 zones conformes |
| Evaluateur coherence | 0 lien chiron |
| Registre JSONL | 774/774 lignes valides |
| Normes | ASCII 0, LF 0 |

## Point d attention : pin test-058 (a adapter par Morpheus)

**test-058 point 2b : KO** -- la boucle REGISTRE n a pas l exception pilote chiron (contrairement aux boucles indices OUTIL et texte, adaptees en v0.2.3). Elle signale les 3 declarations legitimes `chiron/editer-parcours` (tracage du cycle pilote reel du 2026-08-18) comme des violations. Ce n est PAS un defaut de la mission : Chiron a fait exactement ce que l exception pilote autorise (editer-parcours sur SA carte uniquement, verrou pilote l a confirme). Adaptation : ajouter l exception chiron dans la boucle 2b, comme les 2 autres boucles.

## Verdict

**VALIDE** -- le cycle pilote d auto-correction de Chiron fonctionne de bout en bout : detecter (c11b) -> se re-eduquer (c15) -> corriger SA carte (c16, verrou pilote) -> verifier par Themis (c17) -> reprendre (c18). La preuve est reelle : une incoherence veritable (cas A REVOIR sans branche) a ete detectee et corrigee par Chiron seul, sans intervention de Buffy.

## Lecons (Janus)

1. LA VERIFICATION D UN PILOTE = LE LAISSER TOURNER SUR UN VRAI DEFAUT : le cycle a prouve son fonctionnement en corrigeant une incoherence reelle (c18), pas en simulation. Le verrou pilote a autorise l ecriture sur SA carte, le lock s est resynchronise, Themis a verifie, Chiron a repris.
2. UN TEXTE DE REGLE DOIT ANNONCER DES BRANCHES QUI EXISTENT : le defaut c18 etait exactement ca -- le texte promettait 'A REVOIR -> c15' mais aucune branche ne menait a c15. Les controles futurs des cartes doivent verifier texte vs branches.
3. L EXCEPTION PILOTE DOIT COUVRIR CHAQUE BOUCLE DE CHAQUE GARDE-FOU : test-058 a l exception dans 2 boucles sur 3 (indices, texte) mais pas la registre (2b). Le pin est a adapter par Morpheus -- domaine tests.
