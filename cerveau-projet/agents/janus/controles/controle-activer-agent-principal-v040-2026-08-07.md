# Controle -- Evolution v0.4.0 activer-agent-principal (Vulcain) 2026-08-07

**Outil concerne** : activer-agent-principal (v0.4.0)
**Mission controlee** : REGLE ALIGNEMENT (id llm-N -> session-llm-N), champ Id LLM dans
les blocs AGENTS.md (source double AGENTS.md + classeur), conflit gere, absorption d'une
session orpheline, demarrer.md revu, migration des donnees (ma session = session-llm-1).
**Agent auteur** : Vulcain
**Date du controle** : 2026-08-07

---

## Mission de controle

Verifier independamment (je ne fais pas confiance) :

| # | Point a verifier | Methode |
|---|---|---|
| 1 | Version 0.4.0 dans py + sh + doc | inspection |
| 2 | Regle alignement dans le code (py + sh) : sidentifier llm-1 -> session-llm-1 | inspection |
| 3 | Champ **Id LLM** cree dans les blocs (py + sh) | inspection |
| 4 | Conflit gere (session-llm-N liee a un autre id -> ATTENTION + prochaine libre) | inspection |
| 5 | Absorption session orpheline (bloc sans Id LLM) | inspection |
| 6 | demarrer.md : demarrage 'bonjour llm-1' -> verifier AGENTS.md pour SON bloc | inspection |
| 7 | Migration : AGENTS.md bloc session-llm-1 = Id LLM llm-1 ; classeur profil-session-llm-1 = id: llm-1 ; pas de doublon session-llm-2 | inspection |
| 8 | Regression 001-006 complete verte | execution reelle |
| 9 | Conformite ASCII des fichiers modifies | valider-conformite-ascii |
| 10 | Aucune trace d'outil externe | detecter-usage-outils-externes |

---

## Verdict

(rempli apres le controle)

- **Verdict** : **VALIDE**
- **Points valides** : 10/10
- **Problemes detectes** : 1 (corrige pendant le controle -- guillemets francais U+00AB/U+00BB introduits dans la doc .md par Vulcain, detectes par detecter-usage-outils-externes, corriges avant cloture ; 0 caractere non-ASCII restant)

## Detail des points

| # | Point | Resultat |
|---|---|---|
| 1 | Version 0.4.0 dans py + sh + md | OK (grep VERSION + Version 0.4.0) |
| 2 | Regle alignement py + sh | OK (session_cible_pour_id) |
| 3 | Champ Id LLM dans les blocs py + sh | OK (poser_id_llm_bloc) |
| 4 | Conflit gere (ATTENTION + prochaine libre) | OK |
| 5 | Absorption session orpheline | OK |
| 6 | demarrer.md : 'bonjour llm-1, lire demarrer.md' | OK (flux revisionne) |
| 7 | Migration AGENTS.md + classeur (session-llm-1 = llm-1, pas de session-llm-2) | OK (0 occurrence session-llm-2) |
| 8 | Regression 001-006 verte | OK : 12/12 + 8/8 + 22/22 + 19/19 + 28/28 + 26/26 = 115 cas, 0 echec (execution reelle) |
| 9 | ASCII des fichiers modifies | OK (0 non-conforme) |
| 10 | Traces d'outil externe | OK apres correction (0 suspect) |

---

## Lecons

1. detecter-usage-outils-externes detecte les guillemets francais guillemets-ouvrant/fermant (U+00AB/U+00BB) que valider-conformite-ascii ne signale PAS -- les deux outils ont des logiques differentes, il faut TOUJOURS lancer les deux.
2. La regression en boucle sur 6 tests depasse 30s -- prevoir un timeout >= 150s pour la regression complete d'activer-agent-principal.
3. test-001 et test-002 n'affichent pas de ligne VERDICT mais leur rapport Total/Reussis/Echecs est lisible -- verifier les 3 lignes du rapport, pas seulement VERDICT.
4. La migration a bien ete executee : aucun doublon session-llm-2, la session est alignee sur l'id (session-llm-1 = llm-1).
