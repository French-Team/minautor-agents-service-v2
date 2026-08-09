# Rapport d'audit -- Garde-fou restauration (lecon incident piste B)

**Date** : 2026-08-08
**Auditrice** : Themis (evaluatrice croisee)
**Contexte** : apres l incident piste B (git checkout de restauration ayant ecrase les modifs non commitees), Buffy a inscrit un garde-fou a 2 niveaux. Audit de coherence et de conformite demande par l utilisateur.

## Verdict global : CONFORME (5/5 criteres)

## Criteres d'audit

| # | Critere | Resultat |
|---|---|---|
| C1 | PRESENCE : le garde-fou est present dans les 2 fichiers | CONFORME -- regles-general-global.md ligne 21 (tableau regles globales) + protocole-gestion-defaillances.001.01.ebauche.md lignes 67-73 (Etape 3 Corriger la defaillance) |
| C2 | COHERENCE INTER-FICHIERS : pas de contradiction entre la regle courte et la procedure | CONFORME -- memes commandes interdites (git checkout / git restore / git reset --hard), meme condition (fichiers non commites), memes alternatives (git status, sauvegarde cp, git stash). Casse differente de la condition (NON COMMITES majuscules dans le tableau vs non commites minuscules dans le protocole) = variante de style (emphase vs texte courant), PAS une contradiction |
| C3 | CONFORMITE FORMAT : tableaux coherents, ASCII 0, position correcte | CONFORME -- valider-tableaux : 1 analyse / 1 conforme / 0 probleme ; ASCII 0 sur les 2 fichiers ; position correcte (tableau des regles globales / Etape 3 Corriger la defaillance) |
| C4 | NON-REGRESSION : diff minimal, pas de reformatage global | CONFORME -- 2 fichiers modifies, 9 insertions, 0 suppression (8 lignes protocole + 1 ligne tableau) |
| C5 | HIERARCHIE : regle globale > protocole, index a jour | CONFORME -- index-regles-general.md reference les 2 fichiers (1 + 1) ; la hierarchie regle immuable > protocole est respectee |

## Verifications independantes realisees

1. grep du texte exact dans les 2 fichiers (presence + numeros de ligne)
2. Comparaison automatique des formulations (commandes interdites, condition, alternatives)
3. valider-conformite-ascii sur les 2 fichiers
4. valider-tableaux sur regles-general-global.md
5. git diff --stat (diff minimal)
6. grep index-regles-general.md (references)

## Lecons

1. Le garde-fou restauration est coherent a tous les niveaux : la regle courte du tableau global et la procedure detaillee du protocole disent la meme chose avec le meme perimetre (checkout/restore/reset --hard interdits sur fichiers non commites).
2. La difference de casse (NON COMMITES vs non commites) est une variation stylistique legitime : le tableau utilise des majuscules d emphase, le protocole du texte courant. Ce n est pas un ecart.
3. Le choix de Buffy (regle courte globale + procedure dans protocole-gestion-defaillances Etape 3) est conforme a la hierarchie du cerveau : la regle immuable gagne en cas de conflit, le protocole donne la procedure.
4. Aucun ecart detecte : le garde-fou est operationnel pour tous les agents.
