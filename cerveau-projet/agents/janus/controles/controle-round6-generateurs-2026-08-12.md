---
identite:
  type: rapport-controle
  appartient_a: janus
  commun: false
---
# Controle croise -- Round 6 : Generateurs (2026-08-12)

**Controleur** : Janus
**Objet** : controle croise des corrections Vulcain sur les 3 generateurs
(generateurs-commande, generateurs-regenerer-catalogue, generateurs-amelioration),
validees par Morpheus (non-regression 26/26).

---

## Corrections controles

| Faille | Avant | Apres |
|---|---|---|
| A. Flag orphelin (`generateurs-commande` 0.2.3) | un parametre texte optionnel du MODELE (`--commande {commande}`) sans champ `flag` declare : valeur vide -> le placeholder etait retire mais le flag `--commande` restait seul, absorbant l option suivante (`--commande --contexte test`) | v0.2.4 : branche `else` retire `--flag {cle}` quand la valeur est vide (parite py/sh). 95 entrees du catalogue (sur 146) portent ce motif |
| B. Traceback brut (`generateurs-regenerer-catalogue` 1.1.0) | catalogue introuvable ou JSON invalide -> traceback Python brut (`FileNotFoundError` / `JSONDecodeError`) | v1.1.1 : `charger_catalogue` -> message `ERREUR: catalogue illisible/invalide (chemin + cause)` + code 1. Dry-run sur catalogue sain inchange (0 a ajouter) |
| C. Divergence outil/donnees (`generateurs-amelioration` 2.0.0) | l outil affichait v2.0.0 alors que themes-amelioration.json etait en 2.2.0 (11 themes) - divergence silencieuse | v2.1.0 : `--version` et `--liste` affichent la version des themes lue du JSON (`themes v2.2.0`) |

## Verifications (J1-J7)

| # | Verification | Resultat |
|---|---|---|
| J1 | Versions alignees py/sh/md : gc 0.2.4, regen 1.1.1, amelio 2.1.0 (8/8) | OK |
| J2 | Correction A re-mesuree : enregistrer-usage-outil commande= vide -> pas de `--commande` orphelin (py + sh) ; flags booleens inverse=oui/non intacts | OK |
| J3 | Correction B re-mesuree : JSON casse -> ERREUR + rc 1 (pas de Traceback) ; absent -> idem ; sain -> 0 a ajouter | OK |
| J4 | Correction C re-mesuree : --version v2.1.0 + themes v2.2.0 ; --liste 11 themes + themes v2.2.0 | OK |
| J5 | Non-regression complete 26/26 (test-005 v0.2.4 et test-008 v2.1.0 adaptes par Morpheus, verts) | OK |
| J6 | Catalogue : dry-run 0 a ajouter, garde-fou 0 cle dupliquee, 146 entrees intactes | OK |
| J7 | Normes ASCII strict + LF : 0/0 sur 12 fichiers ; lecons ROUND 6 (vulcain) + APRES ROUND 6 (morpheus) presentes | OK |

## Fait marquant

Le bug A n est PAS un cas isole : **95 entrees du catalogue sur 146** portent le
motif `--flag {cle}` avec un parametre texte optionnel (sans champ `flag` declare).
La correction du generateur corrige la FAMILLE entiere, pas une entree. Le
controleur a re-cree le cas (J2) sur py ET sh et a verifie que les flags
booleens declares (gestion preexistante) n etaient pas casses.

## VERDICT

**VALIDE** -- J1-J7 tous verts. Aucun ecart ouvert.

Lecons : controle re-mesure (J2/J3/J4 creent les cas, ne relisent pas le rapport) ;
la regle du flag s applique au MODELE, pas au champ declare ; un outil qui lit des
donnees avec leur propre version doit l afficher (jamais de divergence silencieuse).
