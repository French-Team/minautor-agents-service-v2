# Rapport Vulcain -- Integration tokens dans le cycle d'activation

**Date** : 2026-08-19
**Mission** : afficher les consommations de tokens par agent dans AGENTS-historique (comme les durees), source hybride, detail entree/sortie.
**Carte** : Cerberus -> Vulcain -> Themis -> Vulcain -> Janus -> Cerberus

## Travail realise

### 1. analyser-tokens v0.1.1 -- nouveau mode `--snapshot`
- Retourne l'etat cumulatif des compteurs en **JSON machine** : `{"envoyes": N, "recus": N, "fiable": bool}`
- Source hybride : API reelle si fournie (TOKENS_SESSION), sinon estimation locale par taille des traces
- Fonctions auxiliaires : `difference_snapshots` (conso entre deux instants), `formater_tokens` (Xk env / Yk recus)

### 2. chronometrer-duree v0.1.1 -- option `--tokens`
- `demarrer --tokens` : stocke le snapshot de debut dans le journal
- `arreter` : retourne `agent | duree | tokens_debut` (3e champ)
- Parite py/sh validee

### 3. activer-agent-principal v0.5.17 -- integration au relais
- Au relais : snapshot de fin -> difference avec le snapshot de debut -> ajout au repere
- Format : `### 2026-08-19 19:22 - morpheus (9min 11s, tokens: 13.4k env / 8.2k recus)`
- Parite py/sh validee (flux complet teste sur copie avec TOKENS_MOCK)

### 4. evaluer-processus v0.1.11 -- analyser-tokens en P0 partage
- Outil transverse (appele en subprocess par activer-agent-principal) -> ajoute a OUTILS_P0_PARTAGES
- Evite les DECLARATION_FAUTIVE pour tous les agents

### 5. Carte Vulcain (c6) -- analyser-tokens assigne (Regle 6)
- L'audit Cerberus avait montre l'outil absent de toutes les cartes (orphelin)

### 6. Pins et docs
- test-060 pinne analyser-tokens v0.1.1 (2 corrections)
- .md des 4 outils + spec activer-agent-principal mis a jour

## Bugs trouves et corriges en route

| Bug | Correction |
|---|---|
| `split("|")` recuperait les MESSAGES apres le JSON (meme piege que la duree) | prendre la 1re ligne de parties[2] |
| `echo "$tokens_prec" \| xargs` decoupait le JSON sur les espaces | passer le JSON sans xargs + `.strip()` dans le python |

## Non-regression

- test-067 (bumper) : 8/8 -- test-060 : 12/12 -- test-092 : 9/9 -- test-098 : 7/7 -- test-035 : 10/10
- test-071 : 7/7 -- test-064 : EXCELLENT -- test-095 : 8/8 -- test-002 : 37/37
- detecter-decalages-catalogue : 185 conformes / 0 decalages
- synchro mermaid : 16 cartes synchronisees
- evaluer-processus : 0 probleme -- registre : 764 lignes, 0 inversion

## Preuves

- Flux complet teste sur copie avec TOKENS_MOCK (deterministe) : conso par difference correcte
- Lecon enregistree dans la BDD + corrections.md
- Outils declares au registre : activer-agent-principal, analyser-tokens, chronometrer-duree, evaluer-processus (mode direct)

## Ajout (meme mission) : chronometrer-duree v0.1.2 -- COEXISTENCE MULTI-SESSIONS

**Demande utilisateur** : "on doit pouvoir faire coexister nos session-llm" (2 sessions en parallele : llm-1 + llm-4/opencode).
**Constat** : demarrer/arreter filtraient DEJA par session (chrono_actif(entrees, session)) -> les ecritures coexistaient. Le bug etait l AFFICHAGE `etat` : il ignorait args.session et montrait un seul chrono global.
**Correction** (py + sh parite) :
- nouvelle fonction `chronos_actifs` : un chrono actif par session
- `etat <session>` : chrono de CETTE session (ou "Aucun chrono actif pour X")
- `etat` (sans session) : TOUS les chronos actifs, une ligne par session
- doc .md + bump 0.1.2
**Verifications** : coexistence testee de bout en bout (2 sessions demarrees en parallele, arret de l une ne touche pas l autre), test-092 9/9, test-098 7/7, bumper PROPRE, ASCII/LF purs, evaluateur 0 probleme.
**Residu note** : le chrono orphelin session-llm-4/Vulcain (20:22:52, jamais ferme) est la trace de la session opencode interrompue -- visible desormais dans `etat` (liste les 2 sessions), a fermer par llm-4 a sa reprise ou par Hygie.
