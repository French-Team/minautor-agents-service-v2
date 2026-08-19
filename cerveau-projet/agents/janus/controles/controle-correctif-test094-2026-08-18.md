# Controle Janus -- Correctif test-094 (tags taxonomie + profil)

**Date** : 2026-08-18
**Mission** : Boucle KO -- Morpheus corrige test-094 (defauts detectes par Janus)

## Defauts initiaux detectes par Janus

1. **test-087** : tags du test-094 hors taxonomie (`valider-tableaux`, `fiche-agent`,
   `faux-positif`, `wrapper`, `stdin-windows` non autorises dans
   categories-tests.json + TAGS_SPECIFIQUES).
2. **test-063** : test-094 orphelin (non reference dans profils-tests.json, point 5).

## Correctif applique par Morpheus

| Fichier | Correction |
|---|---|
| test-094-valider-tableaux-fiche-agent.py | Tags remplaces par la taxonomie : `outils, valider, garde-fou, anti-recurrence` |
| profils-tests.json | test-094 ajoute au profil `tests` |

## Re-controle (verdict)

| Test | Avant | Apres |
|---|---|---|
| test-094 | 7/7 OK | **7/7 OK** |
| test-087 (tags) | KO (dont test-094) | **test-094 plus signale** (reste test-092/093 preexistants) |
| test-063 (profils) | KO (dont test-094) | **test-094 plus orphelin** (reste test-092/093 preexistants) |

## Non-regression complete (5 series, --agent janus)

| Serie | Resultat |
|---|---|
| A (Fondations) | 30 OK / 5 KO (tous preexistants : test-030, 055, 063, 079, 085) |
| B (Parcours + validateurs) | **16 OK / 0 KO** (test-094 inclus) |
| C (Outils et combos) | **16 OK / 0 KO** |
| D (Registre et traces) | **11 OK / 0 KO** |
| E (Anti-recurrence) | 12 OK / 2 KO (tous preexistants : test-024, 087) |
| **TOTAL** | **85 OK / 7 KO -- aucun lie a la mission** |

Les 7 KO residuels sont des pins de session preexistants (test-092/093 sans
protections ni tags taxonomie, verrou habilitation janus, editer-parcours
v0.1.7, etc.) -- aucun n'est cause par le correctif test-094.

## Garde-fous

- ASCII / LF : 0 / 0 sur test-094.py et profils-tests.json
- JSONL registre : 602 lignes VALIDE
- Aucun residu .zz
- Evaluateur coherence : 15 liens casses preexistants (protocole-X dans
  corrections.md buffy/janus), aucun dans les fichiers de la mission

## Verdict

**VALIDE** -- le correctif est conforme, test-094 reverdi et integre au profil.
La boucle KO Janus -> Morpheus -> Janus fonctionne : signalement, correction
par l'agent habilite, re-controle.

**Lecon** : tout nouveau test doit (1) porter des tags de la taxonomie
(categories-tests.json + TAGS_SPECIFIQUES) et (2) etre reference dans le bon
profil de profils-tests.json -- sinon test-087 et test-063 font KO.
