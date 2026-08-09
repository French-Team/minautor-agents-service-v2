# Test 004 -- combo tester-outil v0.1.0

**Testeur** : Morpheus (testeur dedie)
**Date** : 2026-08-09
**Objet** : test formel du combo `tester-outil` (Pattern 3, chemin de test encapsule)

---

## Contexte

Buffy a cree le combo `tester-outil` (v0.1.0) qui encapsule l'ancienne suite
c4-c6 du parcours morpheus :

| Case | Type | Action |
|---|---|---|
| c1 | generateur | creer-fichier (entrees fichier/contenu/forcer) -> cmd1 |
| c2 | outil | execute cmd1 : cree le fichier de test |
| c3 | controle | protections ajoutees ? OUI->c4 / NON->c5 (REGLE ABSOLUE) |
| c4 | outil | execute commande_test |
| c5 | fin | FIN PROTECTIONS MANQUANTES |
| c6 | fin | FIN chemin de test termine |

Variables attendues : `--var fichier_test` / `contenu_test` / `commande_test`.
Reponses des controles : `--reponses 'c3=OUI'` (format case=reponse).

## Points couverts

1. Structure JSON : version 0.1.0, case_depart c1, 6 cases c1-c6
2. `combos-moteur --liste` : 6 cases listees
3. Variable `fichier_test` manquante -> erreur claire (entrees de la case c1)
4. Variable `commande_test` manquante (apres c3=OUI) -> erreur claire (case c4)
5. Navigation OUI : fichier de test CREE + test EXECUTE + c6 FIN (COMBO TERMINE)
6. Navigation NON : c5 FIN PROTECTIONS MANQUANTES (REGLE ABSOLUE preservee)
7. Integration parcours morpheus v0.1.2 : case Lancer le combo tester-outil
   puis Verifier les resultats (guider-parcours)
8. `valider-cartes-decision --agent morpheus` : CONFORME
9. Nommage : bruit preexistant documente (identique aux 15 combos existants)
10. ASCII : 0 (definition combo + parcours morpheus)

## Protections

Conformement a la REGLE ABSOLUE (jamais de test sans protections), le test
s'execute dans un dossier temporaire du WORKSPACE (`.tmp-test004/`) qui est
supprime en fin de test. Aucun fichier hors workspace n'est touche.

## Execution

```bash
python3 cerveau-projet/agents/tools/tester/tests/test-004-combos-tester-outil/test-004-combos-tester-outil.py
```

## Verdict

VALIDE (tous les points passent).
