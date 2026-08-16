---
identite:
  type: rapport
  appartient_a: commun
  commun: true
---
# Audit : carte de Cerberus - habilitations limitees (lecture + coordination)

**Date** : 2026-08-16
**Auditrice** : Themis
**Cible** : `cerveau-projet/agents/cerberus/parcours/parcours-cerberus.json` v0.4.9 (36 cases)
**Motif** : demande utilisateur - Cerberus a fait le travail de Themis (un
diagnostic/audit de la convention des scripts temporaires) alors qu il doit
se limiter a la coordination et a la LECTURE.

## 1. Methode

Lecture exhaustive des 36 cases : titre, type, indices (outils/regles), 
branchements (`suivant` / `branches`). Verification de chaque indice outil :
outil de coordination, outil de lecture, ou outil d audit/analyse/correction
(hors habilitation).

## 2. Inventaire des outils indices par case

| Case | Outil | Type d habilitation | Verdict |
|---|---|---|---|
| c2, c3, c8 | lister-agents | LECTURE (liste les agents) | CONFORME |
| c6, c10, c14, c17, c21, c22, c12b, c15c, c19d | activer-agent-principal | COORDINATION (activer/reactiver) | CONFORME |
| c0b | lire-fichier (x2 - DOUBLON) | LECTURE (relire fiche/corrections) | CONFORME (doublon a nettoyer) |
| c0c | lire-activite-recente | LECTURE (activite des agents) | CONFORME |
| c1b, c19c | generateurs-amelioration | COORDINATION (parcours amelioration documente) | CONFORME |
| c11 | corriger-symboles (sur SON corrections.md) | CORRECTION CIBLEE (son propre fichier, regle lecons) | CONFORME |
| c24 | enregistrer-usage-outil | DECLARATION (registre) | CONFORME |
| **c10** | **combos-analyse-projet** | **ANALYSE + ECRITURE de rapport (proprietaire Clio)** | **A CORRIGER** |

## 3. Verdict global

**Carte globalement CONFORME** aux garde-fous anti-derive, avec **1 correction
majeure + 1 nettoyage mineur**.

### Points conformes (les garde-fous anti-audit sont bien la)

- **c1** : branche `autre -> c18` (toute demande hors liste -> c18).
- **c5** : `GARDE-FOU C5 : VERIF/AUDIT/ANALYSE -> Themis (c22). Execution -> activer`.
- **c18** : `Inventaire / audit ? OUI -> c22 (Themis audite, jamais moi). NON -> c23`.
- **c22** : `REGLE ABSOLUE : JE N EXECUTE JAMAIS UN INVENTAIRE OU UN AUDIT MOI-MEME` + indice activer-agent-principal vers Themis.
- **c2/c6** : `je n execute JAMAIS une mission moi-meme` (role = ecouter, choisir, activer).
- **c0d** : lire la doc de l outil avant utilisation (regle, pas d outil).

### Corrections demandees

**M1 - MAJEUR : retirer `combos-analyse-projet` de la case c10**
- `combos-analyse-projet` est un outil d ANALYSE (rapport README vs realite,
  compteurs, ecarts) qui ECRIT un rapport dans `clio/rapports/` (proprietaire
  Clio). Il donne a Cerberus une habilitation d analyse avec sortie ecrite,
  precisement ce que les garde-fous v0.4.8 interdisent
  (`ANALYSE -> Themis, jamais analyser avant activer`).
- Impact : si Cerberus a besoin de connaitre l etat du projet (ex: compteurs
  README) avant d activer un agent, il ACTIVE Themis ou Clio - il ne lance
  pas le combo lui-meme.
- Correction : editer-parcours (Buffy) - retirer l indice outil
  combos-analyse-projet de c10 (garder activer-agent-principal).

**m1 - MINEUR : dedoublonner `lire-fichier` dans c0b**
- L indice `lire-fichier` apparait deux fois dans c0b. Un seul suffit.

## 4. Tests a adapter apres correction (Morpheus)

- `test-013-cerberus-migration` : verifie la carte de Cerberus (versions,
  cases). L historique du test mentionne combos-analyse-projet (v0.4.7 dans
  c17) - verifier s il pinte la presence de l outil dans la carte et
  l adapter si le retrait le casse.
- `test-035-evaluer-processus` : verifie les OUTIL_HORS_CARTE (un outil
  utilise au registre doit etre dans la carte). Retirer combos-analyse-projet
  de la carte cerberus ne casse pas ce test SAUF si Cerberus l utilise au
  registre (a verifier - il ne doit plus l utiliser).

## 5. Cause racine de la derive

La derive du 2026-08-16 (Cerberus a fait un audit de convention) vient de :
1. La carte contenait encore un outil d ANALYSE (combos-analyse-projet en c10),
   ce qui rendait l analyse "accessible" a Cerberus ;
2. Les garde-fous v0.4.8 (c1/c5/c18/c22) existaient mais Cerberus ne les a
   pas suivis (il a pris le chemin direct de l analyse au lieu de c18 -> c22).

La correction M1 (retirer l outil) supprime la tentation ; le garde-fou c18
reste la barriere de comportement.

## 6. Recommandation de chaine

1. **Buffy** : editer-parcours sur parcours-cerberus (retirer combos-analyse-
   projet de c10, dedoublonner c0b) + bump version 0.4.9 -> 0.5.0 + fiche
   (Pattern 14).
2. **Morpheus** : adapter test-013 si necessaire.
3. **Janus** : non-regression complete.

**Verdict Themis** : AUDIT TERMINE - 1 correction majeure (M1), 1 nettoyage
mineur (m1). La carte est sinon conforme : les habilitations de Cerberus se
limitent bien a la coordination (activer-agent-principal), a la lecture
(lister-agents, lire-fichier, lire-activite-recente) et a la declaration
(enregistrer-usage-outil).
