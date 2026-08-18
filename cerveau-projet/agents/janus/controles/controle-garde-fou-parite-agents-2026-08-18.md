---
identite:
  type: rapport
  appartient_a: commun
  commun: true
---
# Rapport de controle Janus -- garde-fou parite agents (test-092)

**Date** : 2026-08-18
**Mission** : controle de fin de chaine (Pattern 17) sur la creation du
garde-fou de parite agents <-> dictionnaire AGENTS de activer-agent-principal.
Chaine : Cerberus -> Morpheus (test-092) -> Vulcain (correction .sh) ->
Morpheus (re-verification) -> Themis (audit) -> Janus (controle).

## Perimetre

1. **test-092 cree par Morpheus** : garde-fou de parite (source de verite
   AGENTS.md, parite py, parite sh, reciproques, parite py/sh, preuve
   negative, normes).
2. **Correction .sh par Vulcain** : argus + gardien ajoutes aux 3 case
   statements (role, fiche, corrections), bump 0.5.12 -> 0.5.13 (py, sh, md,
   spec + entree versionning).
3. **Audit Themis** : rapport CONFORME 0 defaut
   (`themis/rapports/rapport-audit-parite-agents-test092-2026-08-18.md`).

## Verifications independantes

| Verification | Resultat |
|---|---|
| Combo controle-modification (nommage, liens, sante, tableaux, traces) | [OK] |
| Evaluateur : aucune ERREUR nouvelle (seuls artefacts preexistants) | [OK] |
| Bumper --tous : 0 outil incoherent | [OK] |
| Residus : 0 residu au total | [OK] |
| test-092 : 9 OK / 0 KO | [OK] |
| test-005 : 28/28 OK (reverdi sous session janus habilitee) | [OK] |
| test-057 (marbre/cartes-lock) : 24/24 CONFORME | [OK] |
| Normes : ASCII 0 non-ascii, LF 0 CRLF (5 fichiers du perimetre) | [OK] |
| JSONL registre : 371/371 lignes valides | [OK] |
| Perimetre git : 4 fichiers sources de verite + test-092 (nouveau) + rapport | [OK] |
| Syntaxe : bash -n OK, py_compile OK (verifie par Vulcain) | [OK] |

## Points verifies en detail

1. **Parite complete** : les 16 agents d AGENTS.md sont presents dans le
   dictionnaire AGENTS du .py ET dans les 3 fonctions du .sh (argus, gardien
   desormais presents - lignes 47-48, 71-72, 95-96 du .sh). Aucun agent mort.
2. **Preuve negative** : le test-092 a bien DETECTE le defaut avant la
   correction (argus/gardien absents du .sh = le signalement Janus de la
   mission branchement-chiron jamais corrige) et reverdit apres correction.
   La detection dans les deux sens est operationnelle.
3. **Versions** : 0.5.13 coherente partout (py en-tete + constante, sh
   variable, md en-tete + entree versionning, spec).

## Verdict

**VALIDE** -- chaine conforme, 0 defaut.

Le 3e oubli de branchement (agent cree mais absent de l outil d activation)
est desormais impossible : le garde-fou test-092 verifie la parite
py/sh/AGENTS.md dans les deux sens + la parite py/sh + une preuve negative,
a chaque execution. La chaine a demontre son fonctionnement en conditions
reelles : detection du vrai defaut -> signalement a l agent d origine ->
correction -> verdissement -> audit CONFORME.
