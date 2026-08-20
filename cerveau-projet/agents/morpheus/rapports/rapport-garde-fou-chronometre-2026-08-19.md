# Rapport -- Garde-fou chronometre + integration activation

**Date** : 2026-08-19
**Agent** : Morpheus (testeur dedie)
**Mission** : garde-fou de l outil chronometrer-duree (v0.1.0) et de son
integration dans activer-agent-principal (v0.5.16) -- mission Vulcain.

## Ce qui a ete teste (et passe)

- **Parite py/sh** : demarrer (py) -> etat (sh) -> arreter (sh) -> etat (py)
  : sorties identiques, journal coherent
- **Protections template** : refus sans --confirme-doc, --dry-run sans effet,
  --version, --aide
- **Cas limites** : arreter sans chrono (AUCUN_CHRONO), double demarrer
  (ferme l existant avec avertissement -- anti-orphelins), etat (actif/aucun)
- **Flux complet** (copie) : activer -> activer -> reactiver : durees
  ajoutees aux reperes ### au passage de relais (janus 2s sur copie)
- **Non-regression** : test-098 (7/7), 048 (8/8), 065 (8/8), 078 (7/7),
  092 (9/9), 067 (8/8), 060 (12/12), 079 (15/15), 007 (15/15), 040 (5/5),
  023 (26/26), 041 (22/22), 028 (8/8), 005 (27/28), 095 (8/8), 096 (11/11),
  013 (22/22), 016 (20/20), 057 (conforme), 088 (8/8), 037 (6/6),
  002 (37/37), 024 (16/17), 063 (OK)

## Bugs detectes et CORRIGES

1. **CHEMIN PARENTS[3]** (chronometrer-duree.py) : remontait a agents/ au
   lieu de cerveau-projet/ -> journal agents/agents/traces/ inexistant ->
   le chrono reel ne s ecrivait PAS (preuve : apres l activation reelle de
   Morpheus, le repere de Vulcain n avait pas de duree et chronos.jsonl
   n existait pas). Corrige : parents[4] (py) + ../../../../ (sh).
2. **TRI DU REGISTRE** (consulter-combos.journaliser) : append brut cassait
   le tri decroissant du registre-usages-outils (test-024 point 14 ->
   entrees=759 trie=False). Corrige : reutilise trier_registre
   d enregistrer-usage-outil (source de verite). Bump consulter-combos
   0.1.0 -> 0.1.1.
3. **FAUX POSITIF DECLARATION_FAUTIVE** (evaluer-processus) : chronometrer-
   duree (dans UNE carte : vulcain) declare par morpheus = juge exclusif a
   tort, alors qu il est appele en subprocess par activer-agent-principal a
   chaque activation (transverse). Corrige : ajout a OUTILS_P0_PARTAGES.
   Bump evaluer-processus 0.1.9 -> 0.1.10.

## Verrous attendus (pas des regressions)

- test-005 point 21 (valider-cartes-decision) : KO pour Morpheus
  (habilitation argus/buffy/janus/vulcain)
- test-032 (3 KO) : exclusif Janus (pool workers)
- test-024 point 2b (tmp-janus) : KO PREEXISTANT, residu de la mission
  Janus precedente (dossier temporaire non nettoye)

## Etat final

- Registre : 764 lignes, 0 inversion (trie)
- evaluer-processus : 0 probleme de processus
- chronos.jsonl : propre (entree Morpheus ouverte, en attente du relais)

## Chaine

Vulcain (construction) -> Morpheus (garde-fou) -> Janus (controle) ->
Cerberus (bilan consolide)
