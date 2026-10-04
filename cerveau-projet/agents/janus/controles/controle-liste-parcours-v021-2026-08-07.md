# Controle -- Liste des parcours mise a jour (2026-08-07)

**Controleur** : Janus (second controle)
**Mission controlee** : mise a jour de la liste des parcours (Buffy + Vulcain)
**Fichiers concernes** :
- `cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.md` (v0.2.1)
- `demarrer.md`

**Mission de controle** :
1. 6 parcours listes dans guider-parcours.md (tableau Emplacement des parcours) : vulcain, morpheus, clio, janus, cerberus, buffy
2. Versionning 0.2.1 present dans guider-parcours.md (mise a jour de liste tracee)
3. 6 parcours listes dans demarrer.md (bloc CASE 0) : memes agents
4. Chemins identiques dans les 2 fichiers (synchronisation)
5. ASCII 0 non-conforme dans les 2 fichiers
6. Les 6 fichiers JSON de parcours existent reellement

**Verdict** : a determiner

---

## Resultat du controle

**Verdict** : VALIDE (6/6)

| Point | Verification | Resultat |
|---|---|---|
| 1 | 6 parcours dans guider-parcours.md | OK |
| 2 | Versionning 0.2.1 present | OK |
| 3 | 6 parcours dans demarrer.md | OK |
| 4 | Chemins synchronises (2 fichiers) | OK |
| 5 | ASCII 0 non-conforme (2 fichiers) | OK |
| 6 | 6 JSON existent reellement | OK |

**Lecons** :
1. La liste des parcours est une source de verite partagee entre demarrer.md (case 0) et guider-parcours.md (doc de l'outil) -- toute creation de parcours doit mettre a jour les 2 fichiers
2. La doc guider-parcours.md distingue version DOC (0.2.1) et version CLI (0.1.0-py/-sh inchangee) -- une mise a jour de liste ne bumpe que la doc
3. Les fichiers du cerveau (demarrer.md, fiches) sont le domaine de Buffy, la doc d'un outil (guider-parcours.md) est le domaine de Vulcain -- 2 agents ont participe a la meme mission

## Observation hors perimetre (signalee, non corrigee -- Regle 4)

**Probleme** : `janus/corrections.md` contient 2 lignes non-ASCII PRE-EXISTANTES (hors perimetre de cette mission) :
- ligne 312 : accent `e` dans "cosmetiques" (section generateurs-commande, deja presente dans le diff git initial)
- ligne 326 : guillemets francais doubles non-ASCII (section activer-agent-principal v0.4.0)

**Impact** : mineur -- le fichier ne passe pas valider-conformite-ascii, mais aucun de ces caracteres ne provient de la presente mission (les 2 fichiers controles sont ASCII 0).
**Correction suggeree** : a traiter par Buffy lors d'une prochaine maintenance (remplacer par "cosmetiques" et guillemets ASCII) -- Janus signale sans corriger.
