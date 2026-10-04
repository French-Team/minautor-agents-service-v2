# Controle -- Parcours Minerve + synchronisation listes (2026-08-07)

**Controleur** : Janus (second controle)
**Mission controlee** : construction du parcours Minerve (Buffy) + synchronisation des listes (Buffy + Vulcain)
**Fichiers concernes** :
- `cerveau-projet/agents/minerve/parcours/parcours-minerve.json` (21 cases, 3 chemins)
- `cerveau-projet/agents/minerve/minerve.md` (fiche allegee v0.2.0)
- `cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.md` (v0.2.3)
- `demarrer.md` (liste 8 parcours)

**Mission de controle** :
1. Case Mission avec 3 branches (creer, completer, autre)
2. Chemin creer complet : les 9 etapes (rechercher-todos anti-doublon, lire spec, generateurs-squelette-todo, creer-remplir-todo phases 0-9, valider-conformite-ascii, valider-todo, index-todo, lecons, reactiver)
3. Chemin completer : les 7 etapes
4. PHASE 0 (activation agent adapte) + PHASE 9 (reactiver Cerberus) en indices
5. Rappel ASCII x4 dans les cases d'ecriture (Pattern 2)
6. ANTI-DOUBLON : rechercher-todos en premiere case de chaque chemin (c2, c11)
7. Navigation des 3 chemins jusqu'a PARCOURS TERMINE
8. --liste OK
9. Fiche allegee : 0 mission detaillee, PARCOURS present
10. 8 parcours listes dans guider-parcours.md (v0.2.3) dont minerve + 8 parcours dans demarrer.md (Parcours disponibles (8)) + chemins synchronises + ASCII 0

**Verdict** : a determiner

---

## Resultat du controle

**Verdict** : VALIDE (10/10)

| Point | Verification | Resultat |
|---|---|---|
| 1 | 3 branches Mission | OK |
| 2 | Chemin creer 9 etapes | OK |
| 3 | Chemin completer 7 etapes | OK |
| 4 | PHASE 0 + PHASE 9 en indices | OK |
| 5 | Rappel ASCII x4 (Pattern 2) | OK |
| 6 | ANTI-DOUBLON en c2/c11 | OK |
| 7 | Navigation 3 chemins -> TERMINE | OK |
| 8 | --liste OK | OK |
| 9 | Fiche allegee 0 mission | OK |
| 10 | 8 parcours synchronises + ASCII 0 | OK |

**Lecons** :
1. Le 8e parcours (minerve) confirme le pattern de synchronisation : la creation d'un parcours declenche la maj des 2 listes (demarrer.md + guider-parcours.md)
2. Le parcours de la redactrice de todos couvre 2 missions (creer, completer) avec Pattern 1 + PHASE 0/9 + ANTI-DOUBLON en indices
3. Rappel ASCII x4 (Pattern 2) proportionnel a l'ecriture de l'agent
4. Verification mecanique : diff des noms parcours-[a-z]*.json entre doc et demarrer.md -> identiques (8)
5. Le parcours couvre les 9 etapes de creation et les 7 etapes de completion avec 13 references d'outils (rechercher-todos x2, creer-remplir-todo x2, valider-todo x2, generateurs-squelette-todo, valider-conformite-ascii, editer-fichier, lire-fichier, ajouter-contenu-fichier, activer-agent-principal x2)
6. Verdict VALIDE (10/10) : controle termine le 2026-08-07 apres navigation reelle des 3 chemins
