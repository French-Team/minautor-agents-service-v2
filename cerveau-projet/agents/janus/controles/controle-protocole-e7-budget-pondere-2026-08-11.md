# Controle croise : protocole-verification-coherence v0.2.0 (E7) + docstring valider-case.py

**Date** : 2026-08-11
**Controleur** : Janus (second controle, chaine Cerberus -> Vulcain -> Janus)
**Objet** : verification du travail Vulcain (docstring budget pondere corrige) + du protocole-verification-coherence v0.2.0 (etape E7 : grep croise des seuils budget pondere)

---

## Verdict : VALIDE

## Controles J1-J6

| # | Controle | Resultat |
|---|---|---|
| J1 | Anti-recurrence : ancienne regle "> 3 indices"/"plus de 3 indices" ABSENTE des 6 fichiers | OK (0 fichier) |
| J2 | Grep croise des 5 valeurs dans les 4 fichiers textes (100car / 0,5 / 3,0 / 160) | OK (spec-refonte 6/4/6/5, spec-valider-case 3/3/5/3, spec-guider-parcours 4/2/5/4, valider-case.md 2/2/2/2) |
| J3 | Constantes code : valider-case.py SEUIL_COURT=100 / BUDGET_INDICES=3.0 / SEUIL_TEXTE=160 ; generateurs-case.py SEUIL_COURT=100 / BUDGET_INDICES=3.0 / SEUIL_REGLE_DEFAUT=160 | OK (lignes 32-34 et 689-693) |
| J4 | Normes des 2 fichiers modifies (protocole + valider-case.py) : 0 non-ASCII, 0 CRLF | OK |
| J5 | Non-regression complete (test-001 a test-022) | OK (22/22) |
| J6 | Structure protocole : 7 sections + version 0.2.0 + historique + 10 mentions E7 | OK |

## Detail du travail verifie

1. **protocole-verification-coherence v0.2.0** : nouvelle etape E7 (grep croise
   des seuils budget pondere sur 6 fichiers) ajoutee par Cerberus -- perimetre
   etendu documente dans l'Objectif, prerequis 5 (6 fichiers), flux 8 etapes,
   RVAV mis a jour, Exemple 3 (seuil divergent), 3 pieges (seuil divergent .md,
   virgule vs point, valeur a plusieurs usages), liens vers les 6 fichiers.
2. **valider-case.py** : docstring (lignes 11-15) corrige par Vulcain --
   l'ancienne regle "> 3 indices ou texte > 160 caracteres" remplacee par le
   budget pondere (COURT <= 100 car. = 0,5 unite, LONG > 100 = 1 unite, budget
   3,0 par case, texte > 160 car. = SIGNALEE). C'etait la SEULE occurrence
   residue dans les 6 fichiers couverts par E7.
3. Le test reel du grep croise E7 a fonctionne des sa premiere utilisation : il
   a detecte l'ecart du docstring que les verifications precedentes (specs, .md)
   avaient laisse passer.

## Lecons Janus

1. Le grep croise E7 du protocole-verification-coherence v0.2.0 est operationnel
   et a prouve son efficacite (ecart reel detecte + verifie corrige).
2. La coherence budget pondere est desormais couverte sur les 6 fichiers
   (3 specs + .md + 2 codes) : plus aucun residue de l'ancienne regle "> 3 indices".
3. Les docstrings/en-tetes des .py font partie du perimetre de coherence a
   verifier lors des changements de regles.

## Fichiers verifies

- cerveau-projet/agents/regles-immuables/general/protocole-verification-coherence/protocole-verification-coherence.001.01.ebauche.md (v0.2.0)
- cerveau-projet/agents/tools/valider/valider-case/valider-case.py (v1.1.0)
- cerveau-projet/docs-dev-cerveau-projet/spec-refonte-cartes-decision.001.01.ebauche.md
- cerveau-projet/agents/tools/valider/valider-case/spec/spec-valider-case.001.01.ebauche.md
- cerveau-projet/agents/tools/guider/guider-parcours/spec/spec-guider-parcours.001.01.ebauche.md
- cerveau-projet/agents/tools/valider/valider-case/valider-case.md
- cerveau-projet/agents/tools/generateurs/generateurs-case/generateurs-case.py
