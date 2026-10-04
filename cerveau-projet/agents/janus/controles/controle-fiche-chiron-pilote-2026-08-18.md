# Controle Janus -- Mise a jour fiche chiron.md (capacite pilote)

**Date** : 2026-08-18
**Controleur** : Janus (controleur des statuts, session habilitee)
**Cible** : `cerveau-projet/agents/chiron/chiron.md`
**Contexte** : demande utilisateur "Mettre a jour la fiche de Chiron avec sa nouvelle capacite pilote d auto-correction". Chaine : Cerberus -> Buffy (application) -> Themis (audit CONFORME) -> Janus (controle final).

## Perimetre controle

La fiche chiron.md devait reflete la carte v0.3.0 (cycle d auto-correction c11b/c15-c18, exception pilote marbre) :
- Vue d ensemble : version du parcours + nombre de cases exact
- Liste des cases alignee sur le JSON (23 cases)
- EXCEPTION PILOTE documentee dans les regles absolues, workflow, faiblesses, limites
- Cycle CHIRON -> THEMIS -> CHIRON documente
- Aucune contradiction avec l ancienne formulation "je ne modifie jamais"

## Verifications sous session habilitee (Janus)

| Verification | Resultat |
|---|---|
| valider-cartes-decision --agent chiron | **CONFORME** (dont point 10 : coherence fiche/parcours v0.3.0) |
| test-058 (SEUL BUFFY + exception pilote) | 6/6 CONFORME |
| test-006 (cartographie parcours) | 19/19 VALIDE |
| test-027 (series-garde-fou) | 11/11 OK |
| Bumper --tous | 0/0 coherent |
| Verrou marbre --tous | 8/8 zones conformes |
| Evaluateur coherence | 15 liens preexistants (0 nouveau, 0 chiron) |
| Registre JSONL | 747/747 lignes valides |
| Normes fiche chiron | ASCII 0, LF 0 |
| Perimetre git | chiron.md + rapport audit (rien d autre) |
| Residus (.bak, .zz) | 0 |

## Verdict

**VALIDE** -- la fiche chiron.md reflete fidelement la carte v0.3.0 et la capacite pilote d auto-correction. La chaine complete (Buffy applique, Themis audite, Janus controle) est coherente et tous les garde-fous sont verts.

## Lecons (Janus)

1. LA COHERENCE FICHE/PARCOURS EST UN POINT DE CONTROLE AUTOMATISE : valider-cartes-decision point 10 verifie que la ligne PARCOURS (vX) de la fiche == version du JSON. Une fiche mise a jour a la main doit passer ce point AVANT le controle manuel.
2. UNE FICHE D AGENT EST A JOUR QUAND L EXCEPTION EST DOCUMENTEE PARTOUT : version, liste des cases, regles absolues, workflow, faiblesses, limites. L audit Themis verifie l absence de formulation absolue non nuancee ; le controle Janus reverifie sous session habilitee.
3. LE CONTROLE FINAL RESTE SOUS LA SESSION HABILITEE : les verrous (valider-cartes, test-027) ne s appliquent qu a la session Janus. Ce qui etait bloque sous Themis (valider-cartes) est vert ici.
