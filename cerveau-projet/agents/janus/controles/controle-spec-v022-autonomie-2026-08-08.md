---
# Mission de controle -- Spec-guider-parcours v0.2.2 (regle d'autonomie)
# Second controle (Vulcain) -- demande utilisateur

agent:
  nom: "janus"
  type_controle: "second-controle"
  date: "2026-08-08"
  cible:
    - "cerveau-projet/agents/tools/guider/guider-parcours/spec/spec-guider-parcours.001.01.ebauche.md"
    - "cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.md"
---

# Mission de controle -- Regle d'autonomie des parcours (spec v0.2.2)

**Origine** : demande utilisateur -- chaque parcours doit rester un fichier
individuel pour pouvoir etre complete par la suite sans incoherence. Vulcain a
ajoute la regle 8 AUTONOMIE dans la spec (v0.2.1 -> v0.2.2) + la doc (v0.2.7 ->
v0.2.8).

## Verdict attendu

1. **Spec en v0.2.2** : titre + champ Version + ligne d'historique
2. **Regle 8 AUTONOMIE** : dans les regles du format -- fichier individuel par agent, convergence uniquement intra-parcours, aucun partage de cases entre parcours, chaque parcours complet et validable independamment
3. **Sous-section Autonomie** : dans la procedure d'audit (verifier l'absence de references croisees)
4. **Doc guider-parcours.md** : versionning 0.2.8 + reference spec v0.2.2 + regle 7 AUTONOMIE dans la section Regles
5. **Autonomie reelle + ASCII** : 0 reference croisee entre les 11 parcours ; ASCII 0 sur spec + doc + corrections vulcain

---

## RESULTAT DU CONTROLE

**VERDICT : VALIDE (5/5)**

| Point | Verification | Resultat |
|---|---|---|
| 1 | Spec en v0.2.2 | 5 occurrences (titre + Version + historique) | OK |
| 2 | Regle 8 AUTONOMIE | AUTONOMIE DES PARCOURS : 1, INTRA-parcours : 2, fichier INDIVIDUEL : 1 | OK |
| 3 | Sous-section Autonomie (procedure d'audit) | Autonomie des parcours (regle 8) : 1 | OK |
| 4 | Doc guider-parcours.md | versionning 0.2.8 : 1, ref spec (v0.2.2) : 2, regle 7 AUTONOMIE : 1 | OK |
| 5 | Autonomie reelle + ASCII | 0 reference croisee entre les 11 parcours ; ASCII 0 sur spec + doc + corrections | OK |

**Outils utilises pour le controle** : activer-agent-principal, valider-conformite-ascii, lire-fichier, editer-fichier
