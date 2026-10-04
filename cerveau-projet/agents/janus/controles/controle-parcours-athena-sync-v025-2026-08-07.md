# Controle -- Parcours Athena + synchronisation listes (2026-08-07)

**Controleur** : Janus (second controle)
**Mission controlee** : construction du parcours Athena (Buffy) + synchronisation des listes (Buffy + Vulcain)
**Fichiers concernes** :
- `cerveau-projet/agents/athena/parcours/parcours-athena.json` (21 cases, 3 chemins)
- `cerveau-projet/agents/athena/athena.md` (fiche allegee v0.2.0)
- `cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.md` (v0.2.5)
- `demarrer.md` (liste 10 parcours)

**Mission de controle** :
1. Case Mission avec 3 branches (creer, completer, autre)
2. Chemin creer complet : les 9 etapes (rechercher-pense-betes anti-doublon, lire demande, generateurs-squelette-pense-bete, creer-remplir-pense-bete sections, valider-conformite-ascii, valider-pense-bete, RVAV, lecons, ACTIVER PROMETHEE)
3. Chemin completer : les 7 etapes
4. STATUT EBAUCHE + SOUS-FICHIERS SUR DEMANDE en indices des cases RVAV (c8, c15)
5. CHAIN PROMETHEE : la case FIN active Promethee pour la spec
6. Rappel ASCII x4 dans les cases d'ecriture (Pattern 2)
7. ANTI-DOUBLON : rechercher-pense-betes en premiere case de chaque chemin (c2, c11)
8. Navigation des 3 chemins jusqu'a PARCOURS TERMINE
9. --liste OK + fiche allegee 0 mission + ASCII 0
10. 10 parcours listes dans guider-parcours.md (v0.2.5) dont athena + 10 parcours dans demarrer.md (Parcours disponibles (10)) + chemins synchronises + ASCII 0

**Verdict** : a determiner

---

## Resultat du controle

**Verdict** : VALIDE (10/10)

| Point | Verification | Resultat |
|---|---|---|
| 1 | 3 branches Mission | OK |
| 2 | Chemin creer 9 etapes | OK |
| 3 | Chemin completer 7 etapes | OK |
| 4 | STATUT EBAUCHE + SOUS-FICHIERS | OK |
| 5 | CHAIN PROMETHEE en case FIN | OK |
| 6 | Rappel ASCII x4 (Pattern 2) | OK |
| 7 | ANTI-DOUBLON en c2/c11 | OK |
| 8 | Navigation 3 chemins -> TERMINE | OK |
| 9 | --liste OK + fiche + ASCII | OK |
| 10 | 10 parcours synchronises + ASCII 0 | OK |

**Lecons** :
1. Le 10e parcours (athena) confirme le pattern de synchronisation : la creation d'un parcours declenche la maj des 2 listes (demarrer.md + guider-parcours.md)
2. Le parcours d'Athena porte la CHAIN PROMETHEE (activer Promethee pour la spec en fin de mission) -- le flux Athena -> Promethee -> Minerve est incarne dans la structure
3. Verification mecanique : diff des noms parcours-[a-z]*.json entre doc et demarrer.md -> identiques (10)
4. 10 parcours sur 10 agents avec fiches : il ne reste que Atlas
