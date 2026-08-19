# Audit Themis -- Mise a jour fiche chiron.md (capacite pilote)

**Date** : 2026-08-18
**Auditeur** : Themis (evaluatrice croisee)
**Cible auditee** : `cerveau-projet/agents/chiron/chiron.md`
**Contexte** : mise a jour de la fiche par Buffy apres la mission du parcours d auto-correction (carte chiron v0.3.0, cycle c11b/c15-c18, exception pilote marbre).

## Perimetre

La fiche chiron.md devait refleter la nouvelle capacite pilote d auto-correction :
- version du parcours dans la Vue d ensemble
- liste des cases alignee sur le JSON (23 cases)
- EXCEPTION PILOTE documentee dans les regles absolues 1 et 2, le workflow RVAV, les faiblesses et les limites
- cycle pilote CHIRON -> THEMIS -> CHIRON documente
- aucune contradiction residuelle avec l ancienne formulation "je ne modifie jamais"

## Verifications independantes

| Verification | Resultat |
|---|---|
| Version parcours JSON vs fiche | JSON v0.3.0 = fiche v0.3.0 (23 cases) |
| Cases listees vs JSON | 23/23 (0 manquante, 0 en trop) |
| EXCEPTION PILOTE presente | 3 occurrences (regles absolues 1 et 2, limites) |
| Anciennes formulations absolues sans nuance | 0 residu (toutes nuancees) |
| Cycle pilote documente | CHIRON -> THEMIS -> CHIRON + tableau c11b/c15/c16/c17/c18 |
| Navigation guider-parcours | OK (v0.3.0, depart c0) |
| Lock marbre | MATCH (hash identique) |
| test-058 (SEUL BUFFY + exception pilote) | 6/6 CONFORME |
| test-006 (cartographie parcours) | 19/19 VALIDE |
| Bumper | 0/0 coherent |
| Evaluateur liens | 15 liens preexistants (0 nouveau, 0 dans chiron) |
| Normes fiche | ASCII 0, LF 0 |

## Points verifies en detail

1. **La fiche ne contredit plus la carte** : les regles absolues 1 et 2 portent maintenant l exception pilote (SEUL Chiron corrige SA carte via editer-parcours, cycle c11b->c15->c16->c17->c18, toute autre cible = Buffy).
2. **Les limites et faiblesses sont nuancees** : "je ne modifie PAS les cartes des AUTRES agents" (SA carte uniquement en auto-correction pilote, verifiee par Themis avant reprise).
3. **Le cycle pilote est visible** : section dediee sous UTILISATION DE activer-agent-principal avec le pattern CHIRON -> THEMIS -> CHIRON et le tableau des 5 etapes (c11b question, c15 re-education, c16 correction, c17 verification, c18 reprise).
4. **Le comptage des cases est exact** : 23 cases du JSON, y compris c0c/c0e qui manquaient a la liste precedente (la fiche disait 15 cases alors que le parcours en comptait deja 18).

## Verdict

**CONFORME** -- la fiche chiron.md reflete fidelement la carte v0.3.0 et la capacite pilote d auto-correction. Les garde-fous (lock, test-058, conformite) sont tous verts.

## Lecons (Themis)

1. UNE EXCEPTION DE CARTE DOIT ETRE DOCUMENTEE PARTOUT DANS LA FICHE, PAS SEULEMENT DANS LA CARTE : l agent relit SA fiche au demarrage (c0) -- si la fiche contredit la carte, il est desoriente. L audit verifie l ABSENCE de formulation absolue non nuancee, pas seulement la presence de l exception.
2. LE COMPTAGE DES CASES SE FAIT SUR LE JSON : la fiche affichait 15 cases alors que le JSON en avait 18 (c0c/c0e absents de la liste). Le reflet exact = compter les cles du dict cases et aligner la liste 1:1.
3. L AUDIT DE FICHE CROISE 3 SOURCES : carte JSON (version + cases), fiche (reflet), tests (test-058 pour l exception, test-006 pour la navigation). Les 3 doivent etre coherents entre eux.
