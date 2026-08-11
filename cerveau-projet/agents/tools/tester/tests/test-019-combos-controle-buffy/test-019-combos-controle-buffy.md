# test-019-combos-controle-buffy

Test formel du combo **combo-controle-buffy v0.1.0** (Pattern 3).

## Objet du test

Le combo `combo-controle-buffy` encapsule la preparation d'une mission de
controle du travail de Buffy. Il a ete cree pour ALLEGER les cases c11/c18 du
parcours janus (Pattern 16 - ALLEGEMENT : 4 indices -> 1 indice combo).

## Structure du combo

| Case | Type | Contenu |
|---|---|---|
| c1 | controle | Rappel pattern-2 (REGLE ASCII) - OUI -> c2 / NON -> c5 |
| c2 | controle | Rappel pattern-12 (CREATION LIMITEE) - OUI -> c3 / NON -> c5 |
| c3 | outil | Lire protocole-controle-buffy (E1-E10) |
| c4 | outil | Creer le fichier de controle (`--var fichier_controle`) |
| c5 | fin | REGLES NON RESPECTEES |
| c6 | fin | CONTROLE PREPARE |

## Cas couverts

1. JSON valide + version 0.1.0 + case_depart c1 + 6 cases
2. `combos-moteur --liste` affiche les 6 cases
3. Variable `fichier_controle` manquante -> erreur claire (case c4)
4. Navigation OUI/OUI -> c6 FIN + fichier de controle cree (forward slashes)
5. Navigation c1=NON -> c5 FIN REGLES NON RESPECTEES (garde-fou pattern-2)
6. Navigation c1=OUI;c2=NON -> c5 FIN REGLES NON RESPECTEES (garde-fou pattern-12)
7. ASCII 0 (definition combo)
8. Nommage definition-combo.json : bruit preexistant documente (non bloquant)

## Execution

```bash
python3 cerveau-projet/agents/tools/tester/tests/test-019-combos-controle-buffy/test-019-combos-controle-buffy.py
```

## Regle

Le test-019 fait partie de la suite re-scannee completement (test-009 a
test-018) apres chaque refonte d'outil ou de parcours (regle RE-SCAN COMPLET
du protocole-tests). Avec ce test, la suite s'etend a test-019.
