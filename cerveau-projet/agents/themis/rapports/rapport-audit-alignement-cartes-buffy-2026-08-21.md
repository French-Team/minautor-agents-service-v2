# Rapport d'audit - Alignement indices cartes (Buffy) - 2026-08-21

**Agent controleur** : Themis (audit-fin-mission)
**Mission auditee** : Alignement de la convention des indices de cartes - remplacement
de l'alias `corriger-symboles` par le nom canonique `corriger-accents-zones-sensibles`
dans les indices des cartes de decision (demande utilisateur : verifier pourquoi les
cartes utilisaient l'alias et aligner la convention).

---

## VERDICT : CONFORME - 0 defaut

## Points verifies

| # | Point | Resultat |
|---|---|---|
| 1 | **Plus aucun alias `corriger-symboles`** dans les 16 cartes (indices nom + catalogue) | [OK] AUCUN |
| 2 | **Nom canonique present** dans les 16 cartes | [OK] 16/16 |
| 3 | **Pattern 14** : fiche PARCOURS (vX.Y.Z) == version du parcours | [OK] 16/16 |
| 4 | **Lock cartes-lock.json** : empreintes synchronisees (fonction officielle LF + rstrip) | [OK] 0 divergence |
| 5 | **Regle texte vulcain c7** corrigee (mention canonique, plus d'alias) | [OK] OK |
| 6 | **test-055** (coherence regle/indice) | [OK] 12/12 |
| 7 | **test-035** (evaluer-processus) | [OK] 10/10 (global 0 probleme) |
| 8 | **test-096** (sync cartes <-> .mmd <-> .svg) | [OK] 11/11 (20 cartes synchronisees) |
| 9 | **test-071** (cases lecons avec outil correction) | [OK] 7/7 |
| 10 | **test-005** (generateurs-commande, pin atlas v0.5.4) | [OK] 28/28 |
| 11 | **test-013** (migration cerberus, pin v0.5.10) | [OK] 22/22 |
| 12 | **test-016** (migration buffy, pin v0.5.4) | [OK] 20/20 |
| 13 | **Marbre** (8 zones protegees) | [OK] 8/8 conforme |
| 14 | **valider-cartes-decision --tous** | [OK] 17/17 CONFORME |
| 15 | **ASCII / LF** (16 cartes + 16 fiches + 3 tests) | [OK] 0 non-ASCII, 0 CRLF |
| 16 | **Conformite d'execution** (registre usages) | [OK] editer-parcours x34, mettre-a-jour-versions, convertir-carte-mermaid, valider-cartes-decision, enregistrer-lecon, ajouter-contenu-fichier, corriger-accents-zones-sensibles |

## Detail de la verification

### 1. L'alias a disparu des cartes
- Avant : 34 indices `{nom: corriger-symboles, catalogue: corriger-symboles}` dans 16 cartes.
- Apres : 0 occurrence de `corriger-symboles` dans les 16 cartes (grep json complet).
- Chaque indice porte maintenant `nom` + `catalogue` = `corriger-accents-zones-sensibles`,
  le `chemin` et la `commande` pointaient deja vers le script canonique (inchanges).

### 2. Versions bumpees + fiches synchronisees (Pattern 14)
| Agent | Avant | Apres |
|---|---|---|
| argus | 0.2.3 | 0.2.4 |
| athena | 0.4.3 | 0.4.4 |
| atlas | 0.5.3 | 0.5.4 |
| buffy | 0.5.3 | 0.5.4 |
| cerberus | 0.5.9 | 0.5.10 |
| chiron | 0.3.3 | 0.3.4 |
| clio | 0.6.3 | 0.6.4 |
| gardien | 0.2.3 | 0.2.4 |
| hermes | 0.2.3 | 0.2.4 |
| hygie | 0.2.3 | 0.2.4 |
| janus | 0.5.5 | 0.5.6 |
| minerve | 0.4.3 | 0.4.4 |
| morpheus | 0.5.3 | 0.5.4 |
| promethee | 0.4.3 | 0.4.4 |
| themis | 0.5.5 | 0.5.6 |
| vulcain | 0.6.2 | 0.6.3 |

Toutes les fiches portent `PARCOURS (vX.Y.Z)` == version du JSON (verifie par regex).

### 3. Lock resynchronise
- `empreinte_fichier` (LF + rstrip par ligne, fonction officielle d'editer-parcours) recalcul?e
  sur les 16 cartes : 0 divergence avec cartes-lock.json.
- editer-parcours resynchronise le lock a CHAQUE ecriture : apres 34 modifications
  (--modifier-case), le lock est coherent.

### 4. La regle texte vulcain c7
- La case c7 de vulcain avait une regle texte mentionnant `(--commande corriger-symboles
  --reponses ...)`. Si l'indice avait ete renomme sans corriger la regle, test-055 aurait
  detecte un ecart regle/indice (l'outil mentionne sans indice correspondant).
- Verifie : la regle porte maintenant `corriger-accents-zones-sensibles` (0 occurrence
  d'alias dans les textes de regles des cartes).

### 5. Pins de tests adaptes (consequence directe des bumps)
- test-005 : parcours-atlas 0.5.3 -> 0.5.4 (en-tete + verif + commentaire).
- test-013 : parcours-cerberus 0.5.9 -> 0.5.10.
- test-016 : parcours-buffy 0.5.3 -> 0.5.4.
- Aucune autre reference 0.5.3/0.5.9 obsolete restante dans ces 3 tests.

### 6. Vues mermaid/SVG regenerees
- `convertir-carte-mermaid --tous` : 20 cartes regenerees (.mmd + .svg + index.md).
- test-096 : 11/11 OK (sync octet a octet, determinisme SVG).

## Conformite d'execution (registre)
- Les usages de Buffy au registre (2026-08-21 19:38-19:43) correspondent aux outils de
  sa carte pour la branche modifier-carte : editer-parcours (34 usages), mettre-a-jour-versions,
  convertir-carte-mermaid, valider-cartes-decision, enregistrer-lecon, ajouter-contenu-fichier,
  corriger-accents-zones-sensibles.
- evaluer-processus global : 0 probleme de processus detecte.

## Note
- La non-regression complete (tester-lancer-non-regression) est l'outil exclusif de Janus :
  elle sera lancee au controle final de Janus (dernier maillon de la chaine).
