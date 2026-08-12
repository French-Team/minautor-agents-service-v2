# Controle croise -- Round 10b : parallele par defaut du lanceur de non-regression

**Date** : 2026-08-12
**Controleur** : Janus (session-llm-1)
**Objet** : tester-lancer-non-regression v0.1.3 (--parallele par defaut + --serial + heritage du filtre --tests)
**Verdict** : VALIDE (J1-J7 verts)

---

## Verifications

| # | Verification | Resultat |
|---|---|---|
| J1 | Defaut = parallele : sans option, sortie en structure Serie A/B/C/D | VALIDE |
| J2 | --serial = ancien mode serie : RESULTAT : 27 OK / 0 KO | VALIDE |
| J3 | Filtre herite : --tests test-003 sans option -> 1 OK / 0 KO (sur 1 tests) | VALIDE |
| J4 | test-024 13/13 (v0.1.3) + test-027 11/11 (defaut=parallele + --serial testes) | VALIDE |
| J5 | Non-regression 27/27 en mode defaut ET en --serial (parite) | VALIDE |
| J6 | Catalogue : 0 a ajouter (dry-run) | VALIDE |
| J7 | Normes ASCII 0 + LF 0 (lanceur .py/.md, test-024, test-027, lecons) | VALIDE |

## Bilan

Le round 10b est conforme : le mode parallele est desormais le DEFAut de la
non-regression (une commande sans option = A/B/C en parallele puis D en
serie), l'ancien mode reste accessible via --serial, et le filtre --tests est
herite par les sous-processus (un filtre cible ne lance jamais une serie
complete). Les deux modes donnent 27/27. Le gain de temps est automatique
sans aucun changement de commande pour les agents.
