# Rapport -- Chronometre des interventions d agents

**Date** : 2026-08-19
**Agent** : Vulcain (construction)
**Mission** : creer l outil chronometrer-duree + l integrer au cycle
d activation (demande utilisateur : "ajouter la duree de l intervention
d un agent dans AGENTS-historique").

## Livrables

1. **Nouvel outil** `chronometrer/chronometrer-duree/` (v0.1.0) :
   - .py + .sh conformes au template (protections DOC --confirme-doc,
     --dry-run, --chrono, messages info)
   - commandes : demarrer <session> <agent> | arreter <session> |
     etat <session> | --version | --aide
   - journal JSONL `traces/chronos.jsonl` (entree ouverte = chrono actif)
2. **Integration activer-agent-principal v0.5.16** (py + sh) :
   - `activer` : arreter le chrono de l agent precedent (ajout de la
     duree au repere ### de SON entree) PUIS demarrer celui du nouvel agent
   - `reactiver` : arreter le dernier chrono (duree de l agent precedent)
3. **Duree dans AGENTS-historique** : le repere devient
   `### 2026-08-19 18:20 - vulcain (2min 5s)`
4. **Carte Vulcain** : c6 + chronometrer-duree (parcours v0.4.17)
5. **Registres** : index-tools.md + catalogue-commandes.json (185 commandes,
   ordre alphabetique respecte)

## Preuves

- Cycle complet teste de bout en bout sur copie : morpheus (2s) puis
  janus (3s) -> durees ajoutees aux reperes au passage de relais
- Parite py/sh : sorties identiques (demarrer py -> etat sh -> arreter sh)
- Parsers inertes verifies : lire-activite-recente et evaluer-processus
  lisent la table (pas le repere) -> la duree ne les casse pas

## Tests (garde-fou Morpheus)

- test-098 : 7/7 (format historique)
- test-048 : 8/8, test-035 : 10/10, test-065 : 8/8, test-078 : 7/7
- test-092 : 9/9 (parite agents), test-067 : 8/8 (bumper)
- test-060 : 12/12, test-079 : 15/15, test-007 : 15/15, test-040 : 5/5
- test-023 : 26/26, test-041 : 22/22, test-028 : 8/8, test-005 : 28/28
- test-095 : 8/8, test-096 : 11/11
- Pins catalogue 184 -> 185 bumpees (test-007, test-024, test-060, test-079)

## Non-regression / preexistants

- test-024 : 16/17 (KO preexistant tmp-janus, residu de la mission Janus
  precedente - hors perimetre)
- test-032 : verrou d habilitation (exclusif Janus) - attendu pour Vulcain

## Chaine

Vulcain (construction) -> Morpheus (garde-fou) -> Janus (controle) ->
Cerberus (bilan consolide)
