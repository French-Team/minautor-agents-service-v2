# Audit Themis -- Fiche chiron : branche A REVOIR de c18

**Date** : 2026-08-18
**Auditeur** : Themis (evaluatrice croisee)
**Cible auditee** : `cerveau-projet/agents/chiron/chiron.md`
**Contexte** : documentation de la nouvelle branche A REVOIR de c18 (le cycle pilote a evolue lors de la verification reelle : c18 a maintenant 3 branches dans le parcours v0.3.0).

## Perimetre

La fiche chiron.md devait refleter l evolution de c18 :
- Branches de decision : c18 a 3 branches (OUI CONFORME -> c12, A REVOIR -> c15, NON pas revenue -> c18)
- Tableau du cycle pilote : c18 complete avec les 3 branches
- Coherence globale avec le parcours JSON (qui a ete corrige par Chiron lui-meme, verrou pilote)

## Verifications independantes

| Verification | Resultat |
|---|---|
| Branches JSON c18 | 3 : OUI (CONFORME)->c12, A REVOIR->c15, NON (pas revenue)->c18 |
| Fiche : branche A REVOIR -> c15 | PRESENT (2 mentions : branches de decision + tableau pilote) |
| Fiche : NON (pas revenue) -> c18 | PRESENT |
| verifier-conformite-fiche chiron | 1 CONFORME / 0 ECART |
| valider-cartes-decision chiron (point 10) | CONFORME (coherence fiche/parcours, verifie par Buffy) |
| Lock marbre | MATCH |
| test-058 (SEUL BUFFY + exception pilote) | 6/6 CONFORME |
| Bumper | 0/0 coherent |
| Evaluateur coherence | 0 lien chiron |
| Normes fiche | ASCII 0, LF 0 |

## Verdict

**CONFORME** -- la fiche chiron.md reflete fidelement les 3 branches de c18 du parcours v0.3.0. La branche A REVOIR (issue de la verification reelle du cycle pilote) est documentee dans les 2 sections qui la mentionnent (branches de decision et tableau du cycle pilote). Les garde-fous (conformite, lock, test-058, bumper) sont tous verts.

## Lecons (Themis)

1. LA FICHE SUIT LE PARCOURS : une evolution de case (c18 : A REVOIR -> c15) doit etre refletee dans TOUTES les sections de la fiche qui decrivent cette case. L audit verifie la correspondance branches JSON <-> mentions fiche, section par section.
2. LE CYCLE PILOTE EVOLUE LA CARTE, BUFFY EVOLUE LA FICHE : Chiron a corrige c18 (verrou pilote SA carte), Themis a verifie la re-education (CONFORME), puis Buffy a documente la fiche (SEUL BUFFY sur les fichiers agents) et Themis audite de nouveau. La separation des pouvoirs est respectee a chaque etape.
3. L AUDIT DE FICHE APRES UNE EVOLUTION DE CARTE = verifier que les 3 branches du JSON apparaissent dans la fiche, pas seulement la branche nouvelle.
