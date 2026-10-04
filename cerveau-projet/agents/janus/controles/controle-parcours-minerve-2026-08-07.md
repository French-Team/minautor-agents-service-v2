# Controle -- Parcours Minerve (2026-08-07)

**Controleur** : Janus (second controle)
**Mission controlee** : construction du parcours Minerve (Buffy)
**Fichiers concernes** :
- `cerveau-projet/agents/minerve/parcours/parcours-minerve.json` (21 cases)
- `cerveau-projet/agents/minerve/minerve.md` (fiche allegee v0.2.0)

**Mission de controle** :
1. Case Mission avec 3 branches (creer, completer, autre)
2. Chemin creer complet : les 9 etapes (rechercher-todos anti-doublon, lire spec, generateurs-squelette-todo, creer-remplir-todo phases 0-9, valider-conformite-ascii, valider-todo, index-todo, lecons, reactiver)
3. Chemin completer : les 7 etapes (rechercher-todos, lire-fichier, verifier conventions, creer-remplir-todo phases manquantes, valider-todo, lecons, reactiver)
4. PHASE 0 (activation agent adapte) + PHASE 9 (reactiver Cerberus) en indices des cases de remplissage + case FIN
5. Rappel ASCII x4 dans les cases d'ecriture (squelette, remplissage, completer, lecons -- Pattern 2)
6. ANTI-DOUBLON : rechercher-todos en premiere case de chaque chemin (c2, c11)
7. Navigation des 3 chemins jusqu'a PARCOURS TERMINE
8. --liste OK
9. Fiche allegee : 0 mission detaillee, PARCOURS present
10. ASCII 0 non-conforme sur les 2 fichiers

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
| 10 | ASCII 0 non-conforme | OK |

**Lecons** :
1. Le parcours de la redactrice de todos couvre 2 missions (creer, completer) avec le Pattern 1 (branches + convergence vers lecons c9, retour c10)
2. Les regles propres de Minerve sont des indices : PHASE 0 (activation), PHASE 9 (reactivation), ANTI-DOUBLON (rechercher-todos en c2/c11)
3. Rappel ASCII x4 (Pattern 2) -- Minerve ecrit des fichiers todo, le rappel est proportionnel a son volume d'ecriture
4. Les outils references (rechercher-todos, generateurs-squelette-todo, creer-remplir-todo, valider-todo) existent dans le cerveau
5. Verification croisee : 13 references d'outils dans les 2 chemins (rechercher-todos x2, creer-remplir-todo x2, valider-todo x2, generateurs-squelette-todo, valider-conformite-ascii, editer-fichier, lire-fichier, ajouter-contenu-fichier, activer-agent-principal x2)
6. Verdict VALIDE (10/10) : controle termine le 2026-08-07 apres navigation reelle des 3 chemins
