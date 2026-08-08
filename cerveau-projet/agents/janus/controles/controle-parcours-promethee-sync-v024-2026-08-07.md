# Controle -- Parcours Promethee + synchronisation listes (2026-08-07)

**Controleur** : Janus (second controle)
**Mission controlee** : construction du parcours Promethee (Buffy) + synchronisation des listes (Buffy + Vulcain)
**Fichiers concernes** :
- `cerveau-projet/agents/promethee/parcours/parcours-promethee.json` (21 cases, 3 chemins)
- `cerveau-projet/agents/promethee/promethee.md` (fiche allegee v0.2.0)
- `cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.md` (v0.2.4)
- `demarrer.md` (liste 9 parcours)

**Mission de controle** :
1. Case Mission avec 3 branches (creer, completer, autre)
2. Chemin creer complet : les 9 etapes (rechercher-specs anti-doublon, lire pense-bete source, generateurs-squelette-spec, creer-remplir-spec sections, valider-conformite-ascii, valider-spec, index-spec, lecons, ACTIVER MINERVE)
3. Chemin completer : les 7 etapes
4. REGLE PENSE-BETE SOURCE en indice (case c3)
5. FLUX MINERVE : la case FIN active Minerve pour le todo
6. Rappel ASCII x4 dans les cases d'ecriture (Pattern 2)
7. ANTI-DOUBLON : rechercher-specs en premiere case de chaque chemin (c2, c11)
8. Navigation des 3 chemins jusqu'a PARCOURS TERMINE
9. --liste OK + fiche allegee 0 mission + ASCII 0
10. 9 parcours listes dans guider-parcours.md (v0.2.4) dont promethee + 9 parcours dans demarrer.md (Parcours disponibles (9)) + chemins synchronises + ASCII 0

**Verdict** : a determiner

---

## Resultat du controle

**Verdict** : VALIDE (10/10)

| Point | Verification | Resultat |
|---|---|---|
| 1 | 3 branches Mission | OK |
| 2 | Chemin creer 9 etapes | OK |
| 3 | Chemin completer 7 etapes | OK |
| 4 | PENSE-BETE SOURCE en indice | OK |
| 5 | FLUX MINERVE en case FIN | OK |
| 6 | Rappel ASCII x4 (Pattern 2) | OK |
| 7 | ANTI-DOUBLON en c2/c11 | OK |
| 8 | Navigation 3 chemins -> TERMINE | OK |
| 9 | --liste OK + fiche + ASCII | OK |
| 10 | 9 parcours synchronises + ASCII 0 | OK |

**Lecons** :
1. Le 9e parcours (promethee) confirme le pattern de synchronisation : la creation d'un parcours declenche la maj des 2 listes (demarrer.md + guider-parcours.md)
2. Le parcours de Promethee porte le FLUX MINERVE (activer Minerve pour le todo en fin de mission) -- difference cle avec Minerve qui reactive Cerberus
3. Verification mecanique : diff des noms parcours-[a-z]*.json entre doc et demarrer.md -> identiques (9)
4. Le processus est maintenant totalement reproductible : creation -> controle -> README -> sync -> controle
5. Verification croisee : 3 chemins naviguent jusqu au PARCOURS TERMINE, 12 outils references (rechercher-specs x2, creer-remplir-spec x2, valider-spec x2, generateurs-squelette-spec, valider-conformite-ascii, editer-fichier, lire-fichier, ajouter-contenu-fichier, activer-agent-principal) -- tous existent dans le cerveau
6. Verdict VALIDE (10/10) : controle termine le 2026-08-07
