---
identite:
  type: rapport-controle
  appartient_a: janus
  commun: false
---
# Rapport de controle -- 2 regles permanentes (reprise + single-llm)

**Date** : 2026-09-02
**Mission asap** : 1dd85ee9
**Perimetre** : demarrer.md + AGENTS.md (decision utilisateur 2026-09-02)
**Verificateur** : Janus (controleur des statuts)

---

## VERDICT : VALIDE -- 0 defaut

## Verifications effectuees (reelles, jamais supposees)

| # | Verification | Resultat |
|---|---|---|
| 1 | ORDRE 4 present dans demarrer.md (reprise apres redemarrage : traiter les bloquants -> continuer l arbre -> reprendre les missions) | OK |
| 2 | ORDRE 5 present dans demarrer.md (mode single-llm : incarner tous les maillons) | OK |
| 3 | Regles permanentes 1 et 2 presentes dans AGENTS.md (Configuration Active) | OK |
| 4 | Croisement d ancrage : AGENTS.md reference demarrer.md ET demarrer.md reference AGENTS.md (double ancrage, a l origine unilateral apres ajout -> complete pendant le controle) | OK |
| 5 | ASCII strict + LF pur sur les 2 fichiers | OK (0 non-ASCII, 0 CRLF) |
| 6 | Fiche Cerberus conforme (verifier-conformite-fiche --agent cerberus : 1 CONFORME / 0 ECART) | OK |
| 7 | Aucune fin passive restante (les 2 fichiers sont des documents, pas des cartes : sans objet, mais les regles referencees aux fins aero des cartes) | OK |

## Point d attention (non bloquant)

1. La regle single-llm est le MIROIR de la regle Pattern 15 de la spec
   (guider-parcours v0.2.26/27 : mode mono-LLM, jamais d arret apres
   activation) : les 2 formulations se renforcent - l une porte par le
   protocole de demarrage (demarrer.md + AGENTS.md), l autre par la spec
   des parcours. Une seule source de verite serait preferable a terme
   (spec-guider-parcours devrait pointer vers demarrer.md au lieu de
   la repeter), mais la presente double formulation n est pas une
   contradiction.

## Conclusion

Les 2 regles permanentes demandees par l utilisateur sont gravees aux 2
endroits toujours lus (demarrer.md = protocole d entree obligatoire,
AGENTS.md = fichier racine charge en permanence), le croisement d ancrage
est bilateral, l ASCII est strict. Le controle est VALIDE et la mission
peut etre close.