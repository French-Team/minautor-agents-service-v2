# Controle croise Janus - Mission Vulcain (activer-agent-principal v0.5.4)

**Date** : 2026-08-14
**Mission controlee** : automatiser l instruction de demarrage des agents
(anti-bug d arret a c0) + fix bug latent Raison multiligne (decision
utilisateur : automatiser).

## Verdict : VALIDE (18/18)

| Point | Resultat |
|---|---|
| J1. .py : instruction_demarrage + appel (agent != cerberus) + version 0.5.4 | OK |
| J2. .py : fix multiligne (capture + recollement + reemission) | OK |
| J3. .sh : parite (raison_finale + emettre_bloc v_suite + emission multiligne) | OK |
| J4. Doc .md : version 0.5.4 + changelog | OK |
| J5. Test reel sur copie : demarrage ajoute, multiligne survit, cerberus sans demarrage | OK |
| J6. Normes 0/0 + bash -n + py_compile | OK |

## Detail

- Les 2 bugs sont corriges dans le .py ET le .sh (parite).
- Test reel sur copie (AGENTS_FILE surcharge) : activer clio ajoute
  DEMARRAGE OBLIGATOIRE, reactiver preserve la Raison multiligne, la raison
  de Cerberus ne contient pas l instruction.
- Tests internes de l outil (7 scripts) tous VALIDES ; test-025 11/11,
  test-013 22/22, test-018 13/13, test-034 6/6.
- Le bug latent (perte de la Raison multiligne a la reactivation) etait plus
  grave que le bug demande : il tronquait la mission et injectait une ligne
  parasite. Desormais corrige.
