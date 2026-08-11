---
# Mission de controle -- Budget pondere des indices (valider-case v1.1.0, generateurs-case v0.4.2)

agent:
  nom: "janus"
  type_controle: "controle-croise"
  date: "2026-08-11"
  cible:
    - "cerveau-projet/agents/tools/valider/valider-case/valider-case.py"
    - "cerveau-projet/agents/tools/generateurs/generateurs-case/generateurs-case.py"
    - "cerveau-projet/agents/tools/valider/valider-case/spec/spec-valider-case.001.01.ebauche.md"
    - "cerveau-projet/agents/tools/guider/guider-parcours/spec/spec-guider-parcours.001.01.ebauche.md"
---

# Rapport de controle -- Budget pondere des indices par case

**Origine** : demande utilisateur (2026-08-11) -- rendre les cartes plus
flexibles sur le NOMBRE d'indices par case : delimiter la taille d'un indice
COURT pour que 2 indices courts valent 1 indice long. Choix utilisateur :
seuil court = 100 caracteres, budget = 3 unites, portee complete.

**Chaine** : Cerberus -> Vulcain (implementation) -> Morpheus (tests 7/7
independants + non-regression) -> Janus (controle croise).

# Verification

## J1. Coherence du modele (valider-case / generateurs-case)

| Outil | SEUIL_COURT | BUDGET_INDICES | fonction poids_indices |
|---|---|---|---|
| valider-case.py | 100 | 3.0 | OUI |
| generateurs-case.py | 100 | 3.0 | OUI |

- Modele IDENTIQUE dans les 2 outils : court (<= 100 car. ou sans texte)
  = 0,5 ; long (> 100 car.) = 1 ; budget 3,0. : OK

## J2. Parite py/sh

- valider-case.py --version = valider-case v1.1.0
- valider-case.sh --version = valider-case v1.1.0 : OK

## J3. Tests (adaptes par Vulcain, verifies par Morpheus)

- test-009-valider-case : 23/23 OK (dont cas budget 3f/3g : 6 courts CONFORME,
  4 longs A ALLEGER)
- test-010-generateurs-case : 25/25 OK
- test-015-valider-case-garde-fou : 10/10 OK : OK

## J4. Versions coherentes

- valider-case.py / .md / spec : 1.1.0
- generateurs-case.py / .md / catalogue generateurs-commande : 0.4.2 : OK

## J5. Specs documentees

- spec-valider-case v1.1.0 : section 3 documente le budget pondere
  (3 mentions) : OK
- spec-guider-parcours : principe une place pour chaque chose mis a jour
  (<= 100 car. + budget 3,0) : OK

## J6. Normes

- 9 fichiers touches : 0 non-ASCII, 0 CRLF : OK

## J7. Non-regression complete

- Suite complete (test-001 a test-021) : 21/21 OK : OK

# Verdict

**VALIDE** -- le modele pondere est coherent entre valider-case et
generateurs-case, la parite py/sh est maintenue, les tests sont verts
(dont les cas budget), les versions sont alignees (1.1.0 / 0.4.2), les specs
sont documentees, les normes sont propres et la non-regression est complete
(21/21). Aucun ecart a signaler.
