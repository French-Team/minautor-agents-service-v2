# Controle -- Parcours Themis + synchronisation listes (2026-08-07)

**Controleur** : Janus (second controle)
**Mission controlee** : construction du parcours Themis (Buffy) + synchronisation des listes (Buffy + Vulcain)
**Fichiers concernes** :
- `cerveau-projet/agents/themis/parcours/parcours-themis.json` (24 cases, 4 chemins)
- `cerveau-projet/agents/themis/themis.md` (fiche allegee v0.2.0)
- `cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.md` (v0.2.2)
- `demarrer.md` (liste 7 parcours)

**Mission de controle** :
1. Case Mission avec 4 branches (audit, doute, rvav, autre)
2. Chemin audit complet : les 10 etapes d'outils (combos-audit-general, valider-relecture, combos-valider-cerveau, valider-tableaux, detecteurs, rapport, lecons, reactiver)
3. NON-EXECUTION en indices (Themis ne modifie jamais)
4. Rappel ASCII x2 dans les cases d'ecriture (rapport, lecons -- Pattern 2)
5. Navigation des 4 chemins jusqu'a PARCOURS TERMINE
6. --liste OK
7. Fiche allegee : 0 mission detaillee, PARCOURS present
8. 7 parcours listes dans guider-parcours.md (v0.2.2) dont themis
9. 7 parcours listes dans demarrer.md (Parcours disponibles (7)) dont themis
10. Chemins synchronises entre les 2 listes + ASCII 0 non-conforme partout

**Verdict** : a determiner

---

## Resultat du controle

**Verdict** : VALIDE (10/10)

| Point | Verification | Resultat |
|---|---|---|
| 1 | 4 branches Mission | OK |
| 2 | Chemin audit 10 etapes | OK |
| 3 | NON-EXECUTION en indices | OK |
| 4 | Rappel ASCII x2 (Pattern 2) | OK |
| 5 | Navigation 4 chemins -> TERMINE | OK |
| 6 | --liste OK | OK |
| 7 | Fiche allegee 0 mission | OK |
| 8 | 7 parcours dans guider-parcours.md (v0.2.2) | OK |
| 9 | 7 parcours dans demarrer.md | OK |
| 10 | Synchronisation + ASCII 0 | OK |

**Lecons** :
1. La creation d'un parcours (7e : themis) declenche la synchronisation des 2 listes (demarrer.md + guider-parcours.md) -- la source de verite partagee est maintenue a chaque parcours
2. Le parcours de l'evaluatrice croisee est un parcours de NON-EXECUTION : seule la case rapport + lecons ecrivent
3. Pattern 1 (multi-missions) + Pattern 2 (rappel ASCII) respectes sur le 7e parcours
4. Le chemin audit couvre les 10 etapes avec 12 references d'outils (combos-audit-general x2, valider-relecture x2, valider-tableaux x2, combos-valider-cerveau, detecteurs, rapport, lecons, reactiver)
5. Verification croisee des listes : diff des noms parcours-[a-z]*.json entre doc et demarrer.md -> identiques (7) -- la synchronisation est verifiee mecaniquement, pas par lecture seule
6. Verdict VALIDE (10/10) : controle termine le 2026-08-07, navigation reelle des 4 chemins confirmee
