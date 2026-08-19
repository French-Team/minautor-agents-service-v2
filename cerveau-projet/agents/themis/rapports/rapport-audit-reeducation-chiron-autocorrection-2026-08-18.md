# Audit Themis -- Re-education Chiron (cycle pilote reel)

**Date** : 2026-08-18
**Auditeur** : Themis (evaluatrice croisee)
**Contexte** : verification reelle du cycle pilote d auto-correction de Chiron (demande utilisateur). Chiron a detecte une incoherence reelle dans SA carte (c18), s est re-eduque, a corrige via editer-parcours (verrou pilote SA carte), et m a activee (c17) pour verifier.

## L incoherence detectee par Chiron (c18)

Avant correction :
- **Texte de la regle** : "CONFORME -> OUI -> c12 (reprendre) ; A REVOIR -> NON (retour c15) ; pas revenue -> NON (attendre)"
- **Branches JSON** : OUI -> c12, NON -> c18 (2 branches seulement)

**Defaut** : le cas A REVOIR annonce dans le texte (retour c15) n avait AUCUNE branche -> l agent ne pouvait pas executer la reprise apres un verdict A REVOIR de Themis. En plus, le texte faisait 168 caracteres (> 160).

## La correction appliquee par Chiron

c18 a maintenant **3 branches** :
- OUI (CONFORME) -> c12 (reprendre)
- A REVOIR -> c15 (retour corriger)
- NON (pas revenue) -> c18 (attendre, re-essai legitime)

Texte aligne sur les branches (151 caracteres, < 160). Applique via editer-parcours --modifier-case c18, verrou pilote autorise (SA carte), lock resynchronise automatiquement.

## Verifications independantes

| Verification | Resultat |
|---|---|
| Branches c18 | 3 (CONFORME/A REVOIR/NON) |
| Cibles texte vs branches | c12/c15/c18 coherents |
| Navigation c18 A REVOIR | -> c15 (Se re-eduquer) OK |
| Navigation c18 OUI CONFORME | -> c12 -> c13 -> c14 FIN OK |
| Navigation c18 NON | -> c18 (attente re-essai) OK |
| Branches cassees globales | 0 |
| Lock marbre | MATCH (hash resynchronise) |
| Textes cycle pilote (c11b/c15-c18) | tous < 160 |
| Fiche chiron | v0.3.0 (23 cases) synchronisee |
| ASCII / LF parcours | 0 / 0 |
| Lecon BDD | id 58 (Chiron, domaine auto-correction) |

## Verdict

**CONFORME** -- la re-education de Chiron est valide : le cycle pilote fonctionne de bout en bout (detecter -> se re-eduquer -> corriger -> verifier -> reprendre). La correction c18 est propre, le verrou pilote a autorise l ecriture sur SA carte sans intervention de Buffy, le lock est resynchronise.

## Point d attention (pin test a adapter par Morpheus)

**test-058 point 2b (registre) : KO** -- la boucle 2b ne porte pas l exception pilote chiron (contrairement aux boucles indices OUTIL et texte, deja adaptees en v0.2.3). Elle signale les declarations legitimes `chiron/editer-parcours` (tracage du cycle pilote reel) comme des violations. Adaptation necessaire : ignorer `chiron/editer-parcours` dans la boucle 2b, comme les 2 autres boucles. Domaine : tests -> Morpheus.

## Lecons (Themis)

1. LA VERIFICATION D UN PILOTE SE FAIT PAR SON ACTION REELLE, PAS PAR UN TEST : la meilleure preuve que le cycle d auto-correction fonctionne est de le laisser tourner sur une incoherence reelle (c18 : cas A REVOIR sans branche). Le pilote a detecte, corrige, verifie - tout le cycle a fonctionne sans intervention externe.
2. UN TEXTE DE REGLE QUI PROMET UNE BRANCHE INEXISTANTE EST UN VRAI DEFAUT DETECTABLE : la regle c18 annoncait 'A REVOIR -> c15' mais aucune branche ne menait a c15. L audit verifie que chaque cible annoncee dans un texte de question existe dans les branches.
3. L EXCEPTION PILOTE DOIT COUVRIR TOUTES LES BOUCLES DES GARDE-FOUS : test-058 a l exception chiron dans les boucles indices et texte mais PAS dans la boucle registre (2b). Chaque nouvelle boucle de verification du garde-fou doit porter l exception, sinon le pilote est faussement signale.
