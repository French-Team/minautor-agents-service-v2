# Rapport Themis -- Audit de la mission Vulcain (integration tokens)

**Date** : 2026-08-19
**Mission auditee** : afficher les consommations de tokens par agent dans AGENTS-historique (comme les durees), source hybride, detail entree/sortie.
**Chaine** : Cerberus -> Vulcain -> Themis -> Vulcain -> Janus -> Cerberus

## VERDICT : CONFORME (0 defaut dans le perimetre de la mission)

## 1. Conformite d'execution (c8b) -- OK

| Point | Verdict |
|---|---|
| analyser-tokens v0.1.1 : mode `--snapshot` JSON machine (envoyes/recus/fiable) | CONFORME |
| chronometrer-duree v0.1.1 : `--tokens` au demarrage, 3e champ dans arreter | CONFORME |
| activer-agent-principal v0.5.17 : conso par difference au relais | CONFORME |
| Parite py/sh des 2 outils (flux complet teste sur copie, TOKENS_MOCK) | CONFORME |
| evaluer-processus v0.1.11 : analyser-tokens en OUTILS_P0_PARTAGES | CONFORME |
| Carte Vulcain c6 : analyser-tokens assigne (Regle 6) | CONFORME |
| test-060 : pins 0.1.1 (2 corrections) | CONFORME |
| Fin selon SA carte c9f : active Themis (PAS reactiver Cerberus en milieu de chaine) | CONFORME |

## 2. Verification d'impact (c8c) -- OK sur le perimetre

- Bumper (test-067) : PROPRE (0 incoherence de version)
- ASCII/LF : 11/11 fichiers de la mission purs (0 non-ASCII, 0 CRLF)
- index-tools : analyser-tokens (l.44) + chronometrer-duree (l.66) presents
- catalogue-commandes : analyser-tokens + chronometrer-duree presents
- registre : 764 lignes, 0 inversion, usages vulcain declares
- Tests : 098 (7/7), 060 (12/12), 092 (9/9), 040 (5/5), 028 (8/8), 067 (PROPRE)
- detecter-local-hors-fonction : 0 -- detecter-usage-outils-externes : 0
- valider-cartes-decision --tous : 16/16 CONFORME -- valider-tableaux : 23/23 CONFORME
- Preuve reelle : chrono vulcain ferme (807s = 13min 27s) au repere, chrono themis ouvert avec tokens_debut (estimation)

## 3. Defauts detectes (TOUS preexistants, HORS perimetre de la mission)

### D1. Combo audit-themis mal parametre (preexistant) -- a corriger
Le combo `combo-audit-themis` a 2 cases generatrices qui produisent des commandes INVALIDES :
- **c1** : generateur audit-general avec `dossier: cerveau-projet` -> `combos-audit-general.py cerveau-projet` -> l'outil attend le WORKSPACE (il construit `dossier/cerveau-projet/...`) -> chemin `cerveau-projet/cerveau-projet` INEXISTANT -> 57 erreurs factices "MANQUANT", score 46/100 CRITIQUE (vs structure 100/100 avec le bon dossier `.`)
- **c4** : generateur combos-valider-cerveau avec `dossier: cerveau-projet/agents` -> l'outil REFUSE l'argument positionnel (usage: sans dossier) -> `unrecognized arguments`
- `echec_ok: true` sur les 2 cases -> le combo se termine "COMBO TERMINE" en masquant les echecs
- Impact : MON propre outil d'audit produit des resultats faux quand il est lance via la definition-combo.

### D2. Ma carte (c3/c25) : indice fichier vers un chemin inexistant (preexistant)
Les cases c3 et c25 pointent vers `cerveau-projet/combos/combo-audit-themis/definition-combo.json` (MANQUANT) au lieu de `cerveau-projet/agents/tools/combos/combo-audit-themis/definition-combo.json` (reel). La commande (combos-moteur) est bonne, seul l'indice fichier est faux.

### D3. readme-dev.md obsolete (preexistant -- mission precedente)
Annonce "159 outils dans 38 categories" : la categorie Chronometrer (chronometrer-duree, creee par la mission chrono) n'y figure pas. Le compteur et la liste des categories sont en retard sur index-tools.

### D4. Faux positifs connus des evaluateurs (preexistants)
- evaluer-agents (24/100) : dossiers de DONNEES (conventions, lecons, philosophie, regles-immuables, traces) pris pour des agents + tests sans .sh/.md
- evaluer-coherence : `protocole-X/` (exemples generiques dans corrections.md) et options CLI (`--etat-tests`, etc.) pris pour des liens/outils casses -- presents au HEAD
- valider-relecture : 9 manques (dossiers de donnees + chiron/gardien/hermes sans regle complete)
- valider-conformite-ascii : crashe sur l'emoji du dictionnaire-emojis.txt (documente par Janus)

### D5. Ma carte (themis) : outils d'audit absents -- DECLARATION_FAUTIVE sur mes propres usages
L'evaluateur-processus signale 2 OUTIL_HORS_CARTE pour themis : `evaluer-processus` et `valider-cartes-decision`. Ces outils sont dans les cartes de buffy/janus/vulcain/argus (outils de controle/audit legitimes) mais ABSENTS de mon parcours (21 outils assignes). Je les utilise pourtant en audit. A corriger par Buffy : ajouter ces 2 outils aux indices de ma carte (ou les passer en P0 partages si transverses).

## 4. Verdict final

**CONFORME.** La mission Vulcain est executee selon SA carte (c9f), les 4 outils sont coherents (py/sh, versions, catalogue, index), la non-regression est verte, la preuve reelle est au repere (`vulcain (13min 27s)` + chrono themis avec tokens_debut). Les 3 defauts signales (D1 combo, D2 carte themis, D3 readme-dev) sont TOUS preexistants au HEAD et a traiter hors de cette mission : D1+D2 par Buffy (SEUL a corriger les cartes/combos ? a arbitrer), D3 par le prochain passage de mise a jour du README.
