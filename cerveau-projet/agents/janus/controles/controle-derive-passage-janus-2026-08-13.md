# Controle croise -- Derive du passage par Janus (Morpheus)

**Date** : 2026-08-13
**Controleur** : Janus (mission Cerberus, demande utilisateur)
**Objet** : comprendre pourquoi Morpheus ne lance plus Janus en fin de mission
**Verdict** : **VALIDE avec cause racine identifiee** (J1-J6 verts) + recommandation de renforcement

---

## J1 - Pool de workers v0.2.0 (round 3 etapes, jamais controle)

- test-032-pool-workers : **10 OK / 0 KO**
- Pool de workers par defaut, garde-fous globaux en serie finale, anti-deadlock fichier temp : confirmes par le garde-fou
- Verdict : **CONFORME**

## J2 - Goulot test-028 v0.2.1 (round goulot, jamais controle)

- test-028-coherence-documentaire : **8 OK / 0 KO**
- detecter-decalages-catalogue v0.2.1 : pool de threads + cache (interpreteur, script)
- **Stabilite du verdict prouvee** : 2 runs consecutifs IDENTIQUES
  - run 1 : 141 conformes / 0 decalage / 6 non testables / 0 alerte / combos 14
  - run 2 : 141 conformes / 0 decalage / 6 non testables / 0 alerte / combos 14
- Verdict : **CONFORME** (le parallelisme ne change pas le verdict)

## J3 - Non-regression complete

- **32 OK / 0 KO** en 54.8 s (pool-16) - conforme a la reference (52.3 s, +5%)

## J4 - Normes ASCII/LF

- Fichiers modifies des 2 rounds (detecter-decalages-catalogue.py/.md/spec,
  test-028, test-032, lanceur non-regression) : **0 non-ASCII / 0 CRLF**

## J5 - CONSTAT DE LA DERIVE (cause racine)

Comparaison des consignes de fin des missions donnees a Morpheus :

| Date | Mission | Fin ecrite dans la consigne |
|---|---|---|
| 2026-08-12 21:09 | round 10 (series) | activer JANUS pour le controle croise |
| 2026-08-12 21:28 | round 10b (parallele defaut) | activer JANUS pour le controle croise |
| 2026-08-12 21:47 | round 10c (serie D allegee) | activer JANUS pour le controle croise |
| 2026-08-12 22:15 | round 11 (coherence doc) | activer JANUS pour le controle croise |
| 2026-08-12 22:39 | audit template | activer JANUS pour le controle croise |
| 2026-08-12 23:01 | protections importees | activer JANUS pour le controle croise |
| **2026-08-13 00:08** | **chrono + reference** | **reactiver Cerberus** (BAScule) |
| **2026-08-13 00:56** | **pool workers** | **reactiver Cerberus** |
| **2026-08-13 07:23** | **goulot test-028** | **reactiver Cerberus** |

**Cause racine** : a partir de la mission chrono (2026-08-13 00:08), les consignes
ont ete redigees avec `reactiver Cerberus` au lieu de `activer JANUS pour le
controle croise`. Morpheus a suivi la consigne ecrite au lieu de relire SA carte
(c10/c14 = FIN - Activer Janus, meme en activation directe). Derive analogue a
celle du template : Morpheus cale sur ce qu on lui donne plutot que sur sa carte.

**Consequence** : 2 controles croises Janus n ont jamais eu lieu (pool workers
v0.2.0 + goulot test-028 v0.2.1). Le present rapport les controle retroactivement.

## J6 - Carte Morpheus conforme au test-018

- test-018-fins-reactivation : **13 OK / 0 KO**
- La seule fin REACTIVER legitime est janus (dernier maillon)
- La carte morpheus c10/c14 porte bien `FIN - Activer Janus` avec la commande
  exacte `activer session-llm-1 janus <raison>` (PAS reactiver)

---

## Recommandation : renforcer le passage par Janus (garde-fou)

1. **Fiche morpheus.md** : ajouter une REGLE ABSOLUE - apres TOUTE mission, meme
   active directement par Cerberus, Morpheus ACTIVE JANUS (jamais reactiver
   Cerberus directement ; la fin suit SA carte c10/c14).
2. **Garde-fou test-033** (serie D) : verifie que
   - la carte morpheus c10/c14 = FIN - Activer Janus avec la commande
     `activer session-llm-1 janus` (et pas `reactiver` dans le message de fin) ;
   - la fiche morpheus.md porte la REGLE ABSOLUE de passage par Janus ;
   - les consignes de mission recentes ne demandent plus `reactiver Cerberus`
     pour morpheus (echantillon AGENTS-historique).
3. **Lecon Janus** : la fin de mission suit TOUJOURS la carte, jamais la consigne
   (la carte est la reference, la consigne un declencheur).

---

Rapport redige par Janus - reactiver Cerberus avec le bilan consolide.
