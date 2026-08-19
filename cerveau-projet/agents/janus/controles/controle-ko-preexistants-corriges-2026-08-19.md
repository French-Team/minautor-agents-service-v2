# Controle Janus -- 7 KO preexistants corriges (non-regression 92/92)

**Date** : 2026-08-19
**Mission** : Corriger les 7 KO preexistants de la non-regression (demande utilisateur)

## Les 7 KO et leur correction (4 volets)

| KO | Cause | Correctif (agent) |
|---|---|---|
| test-085 | 1 processus residuel reel (bash -x /tmp/vt-test2.sh, orphelin de diagnostic heredoc) | **Hygie** : snapshot + kill 1/1 + re-detection PROPRE |
| test-030 | test-093 sans bloc protections + subprocess.run bruts | **Morpheus** : bloc PROTECTIONS + lancer_protege |
| test-024 | pin editer-parcours v0.1.6 obsolete | **Morpheus** : pin -> v0.1.7 |
| test-063 | test-092/093 orphelins dans profils-tests.json | **Morpheus** : ajoutes au profil tests |
| test-087 | tags test-092/093 hors taxonomie | **Morpheus** : garde-fou-agent + preuve-negative |
| test-055 | 10 cartes mentionnaient editer-parcours dans une regle sans indice | **Buffy** : reformulation du texte (sans nommer l'outil exclusif) |
| test-079 | 32 entrees registre avec noms non canoniques | **Vulcain** : noms canoniques du catalogue |

## Incident decouvert en cours de route (conflit test-055 / test-058)

La 1re approche (ajouter un indice OUTIL editer-parcours dans les 10 cartes)
reverdissait test-055 mais cassait test-058 (outil exclusif interdit hors
buffy/chiron) ET creait 4 artefacts verrou-auto dans le registre (le verrou
lisait la carte de janus avec l'indice temporaire -> 'usage autorise' pendant
que test-057 appelait editer-parcours). Correctif : reformuler le TEXTE de la
regle sans nommer l'outil + retirer les 4 entrees fausses du registre.

## Non-regression finale (5 series, --agent janus)

| Serie | Avant | Apres |
|---|---|---|
| A (Fondations) | 30 OK / 5 KO | **35 OK / 0 KO** |
| B (Parcours + validateurs) | 15 OK / 1 KO | **16 OK / 0 KO** |
| C (Outils et combos) | 16 OK / 0 KO | **16 OK / 0 KO** |
| D (Registre et traces) | 11 OK / 0 KO | **11 OK / 0 KO** |
| E (Anti-recurrence) | 12 OK / 2 KO | **14 OK / 0 KO** |
| **TOTAL** | 84 OK / 8 KO | **92 OK / 0 KO** |

## Garde-fous verifies

- JSONL registre : 616 lignes VALIDE
- Aucun residu .zz
- Evaluateur coherence : 15 liens casses preexistants (protocole-X, hors mission)
- ASCII/LF : 0/0 sur tous les fichiers modifies
- Lecons BDD enregistrees (hygie, morpheus, buffy, themis, vulcain x2, janus)

## Verdict

**VALIDE** -- les 7 KO sont corriges, la non-regression est a 92/92 OK.
La lecon cle : test-055 (mention dans une regle -> indice) et test-058
(outil exclusif -> indice interdit hors buffy/chiron) se reconcilient en
reformulant le texte de la regle, jamais en ajoutant l'indice outil.
