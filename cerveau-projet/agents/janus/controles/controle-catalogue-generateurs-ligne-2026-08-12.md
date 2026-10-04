# Controle croise : correction catalogue generateurs-ligne (regenerer-catalogue debloque)

**Date** : 2026-08-12
**Controleur** : Janus
**Chaine** : Cerberus -> Vulcain (catalogue + README) -> Morpheus (non-regression) -> Janus

---

## Verdict : VALIDE (J1-J6 verts)

| # | Verification | Resultat |
|---|---|---|
| J1 | Catalogue-commandes.json : 0 cle dupliquee sur 146 entrees, generateurs-ligne a 13 parametres | CONFORME (scan complet, doublon source/mode/branche retire) |
| J2 | regenerer-catalogue --dry-run : GARDE-FOU 0 cle dupliquee (OK), 0 a ajouter ; generateurs-commande --commande generateurs-ligne compose correctement | CONFORME (regeneration debloquee) |
| J3 | README : combos-analyse-projet verdict README A JOUR (badge Outils 126 == 126, categorie enregistrer ajoutee, 0 ecart) | CONFORME |
| J4 | Non-regression 26/26 OK, registre 0 ligne (test-005/007/017/024 verts + garde-fous 025 11/11 et 026 10/10) | CONFORME |
| J5 | Lecons Vulcain + Morpheus documentees, registre usages complet | CONFORME |
| J6 | Delegation respectee (Vulcain n a touche a aucun fichier de test) + **lecon Cerberus c15b/c15c appliquee** : cette correction a ete declenchee par l activation immediate de l agent habilite (carte cerberus v0.4.2, garde-fou c15b en place) | CONFORME |

## Details

### J1 - Le bug corrige

L'entree `generateurs-ligne` du catalogue contenait un **bloc de parametres
duplique** (source/mode/branche apparaissaient 2 fois : index 8/9/10 identiques
a 11/12/13). Le garde-fou de regenerer-catalogue detectait les cles dupliquees
et **refusait toute regeneration** (blocage pre-existant, decouvert lors de la
mission detecter-cablages-manquants). Correction : retrait du bloc duplique
(16 -> 13 parametres). Scan complet : **0 doublon restant**.

### J6 - La lecon Cerberus appliquee

Cette mission est la **preuve de la lecon c15b/c15c** : le rapport Janus de la
mission detecter-cablages-manquants signalait le blocage regenerer-catalogue ;
au lieu d attendre la prochaine mission utilisateur, Cerberus a **active
immediatement l agent habilite** (Vulcain) -- conformement a la carte cerberus
v0.4.2 (indice GARDE-FOU C15B ajoute : "TOUT probleme signale (meme hors
perimetre) -> OUI -> activer l agent habilite TOUT DE SUITE").

---

**Fin de controle** : Janus reactive Cerberus avec le bilan consolide.
