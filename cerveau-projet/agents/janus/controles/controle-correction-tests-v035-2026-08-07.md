# Controle -- Correction des tests obsoletes (Morpheus) 2026-08-07

**Outil concerne** : activer-agent-principal (v0.3.5)
**Mission controlee** : alignement des tests test-001/002/003 sur la semantique
MODE ID (sidentifier <id-llm>) pour une regression complete verte (001 a 005).
**Agent auteur** : Morpheus
**Date du controle** : 2026-08-07

---

## Mission de controle

Verifier independamment (je ne fais pas confiance) les points suivants :

| # | Point a verifier | Methode |
|---|---|---|
| 1 | Regression test-001 : 12/12 sans echec | execution reelle |
| 2 | Regression test-002 : 8/8 sans echec | execution reelle |
| 3 | Regression test-003 : 22/22 sans echec | execution reelle |
| 4 | Regression test-004 : 19/19 sans echec | execution reelle |
| 5 | Regression test-005 : 28/28 sans echec | execution reelle |
| 6 | test-001 : export CLASSEUR_STOCKAGE present (plus d'ecriture dans le vrai classeur) | inspection |
| 7 | test-001 : structure multi-session vide + Test 3 en MODE ID (llm-atlas) | inspection |
| 8 | test-003 : tests 3/4/7c reecrits en MODE ID (plus de regle 'session occupee' obsolete) | inspection |
| 9 | Conformite ASCII des fichiers modifies | valider-conformite-ascii |
| 10 | Aucune trace d'outil externe (CRLF, non-ASCII, BOM) | detecter-usage-outils-externes |

---

## Verdict

(rempli apres le controle)

- **Verdict** : **VALIDE (10/10)**
- **Points valides** : 10/10
- **Problemes detectes** : aucun

### Detail des points

| # | Point | Resultat |
|---|---|---|
| 1 | Regression test-001 | 12/12 VALIDE |
| 2 | Regression test-002 | 8/8 VALIDE |
| 3 | Regression test-003 | 22/22 VALIDE |
| 4 | Regression test-004 | 19/19 VALIDE |
| 5 | Regression test-005 | 28/28 VALIDE |
| 6 | test-001 : export CLASSEUR_STOCKAGE (ligne 24) + creation fichier (ligne 58) | CONFORME |
| 7 | test-001 : structure multi-session vide + Test 3 MODE ID (llm-atlas) | CONFORME |
| 8 | test-003 : tests 3/4/7c en MODE ID, plus de 'deja attribuee a un autre LLM' | CONFORME |
| 9 | ASCII : 0 non-conforme | CONFORME |
| 10 | detecter-usage-outils-externes : 0 suspect (10 fichiers + corrections) | CONFORME |

## Lecons

1. La correction des tests 001/002/003 etait NECESSAIRE : les echecs pre-existants venaient de structures/semantiques OBSOLETES dans les tests (ancienne regle 'session occupee -> message', nom de session comme argument), pas d'un bug v0.3.5
2. test-001 ecrivait dans le VRAI classeur (absence d'export CLASSEUR_STOCKAGE) : effet de bord dangereux detecte et corrige par Morpheus -- verifier TOUJOURS que chaque test isole son environnement
3. test-002 n'a demande AUCUNE modification : son seul echec etait la cascade de test-001 -- toujours re-executer la chaine complete avant de conclure
4. Bug latent decouvert (hors perimetre test) : sidentifier seul ne PERSISTE pas la migration d'une structure mono-session ancienne (le bloc cree par migration existe deja dans le contenu en memoire -> pas d'ecriture). A traiter par Vulcain en v0.3.6
