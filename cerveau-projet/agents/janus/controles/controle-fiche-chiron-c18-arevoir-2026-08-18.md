# Controle Janus -- Fiche chiron : branche A REVOIR de c18

**Date** : 2026-08-18
**Controleur** : Janus (controleur des statuts, session habilitee)
**Cible** : `cerveau-projet/agents/chiron/chiron.md`
**Contexte** : demande utilisateur "Documenter la nouvelle branche A REVOIR de c18 dans la fiche chiron (le cycle pilote a evolue)". Chaine : Cerberus -> Buffy (application) -> Themis (audit CONFORME) -> Janus (controle final).

## Perimetre controle

La fiche chiron.md devait documenter l evolution de c18 (3 branches dans le parcours v0.3.0, issue de la verification reelle du cycle pilote) :
- Branches de decision : c18 -> OUI (CONFORME) -> c12, A REVOIR -> c15 (retour corriger), NON (pas revenue) -> c18 (attendre)
- Tableau du cycle pilote : c18 complete avec les 3 branches

## Verifications sous session habilitee (Janus)

| Verification | Resultat |
|---|---|
| Branches JSON c18 | 3 : OUI (CONFORME)->c12, A REVOIR->c15, NON (pas revenue)->c18 |
| Fiche : A REVOIR -> c15 | PRESENT (2 mentions : branches de decision + tableau pilote) |
| Fiche : NON (pas revenue) -> c18 | PRESENT |
| valider-cartes-decision --agent chiron | **CONFORME** (point 10 : coherence fiche/parcours) |
| verifier-conformite-fiche chiron | 1 CONFORME / 0 ECART |
| test-058 (SEUL BUFFY + exception pilote) | 6/6 CONFORME |
| Bumper --tous | 0/0 coherent |
| Marbre --tous | 8/8 zones conformes |
| Evaluateur coherence | 0 lien chiron |
| Registre JSONL | 801/801 lignes valides |
| Normes fiche | ASCII 0, LF 0 |
| Perimetre git | chiron.md + rapport Themis (rien d autre) |

## Verdict

**VALIDE** -- la fiche chiron.md documente fidelement les 3 branches de c18. La branche A REVOIR (ajoutee lors de la verification reelle du cycle pilote) apparait dans les Branches de decision ET le tableau du cycle pilote. La chaine (Buffy applique, Themis audite, Janus controle) est coherente et tous les garde-fous sont verts.

## Lecons (Janus)

1. UNE EVOLUTION DE CARTE ISSUE DU CYCLE PILOTE REMONTE JUSQU A LA FICHE : Chiron a corrige c18 (verrou pilote SA carte), Themis a verifie la re-education, puis Buffy a documente la fiche (SEUL BUFFY sur les fichiers agents) et Themis a audite. Chaque evolution de carte doit etre refletee dans la fiche, sinon la fiche et le parcours divergent.
2. LA VERIFICATION DE LA DOCUMENTATION = CORRESPONDANCE BRANCHES JSON <-> MENTIONS FICHE : le controle verifie que les 3 branches du JSON apparaissent dans la fiche, pas seulement la branche nouvelle. Ici A REVOIR est present 2 fois (les 2 sections qui decrivent c18).
3. LE CYCLE PILOTE EST MAINTENANT COMPLET ET DOCUMENTE : detecter (c11b) -> se re-eduquer (c15) -> corriger (c16) -> verifier (c17) -> reprendre (c18 avec 3 branches) -- carte, fiche, tests et rapports sont tous alignes.
