# Controle croise Janus -- Correction des 5 ecarts pre-existants (Buffy)

**Date** : 2026-08-12
**Objet** : verifier la correction des 5 ecarts pre-existants (signales depuis plusieurs missions sans correction) par Buffy
**Verdict** : **VALIDE**

## Controles effectues

| Controle | Resultat |
|---|---|
| J1 valider-case vulcain | CONFORME (0 erreur, 0 a alleger) |
| J1 valider-case clio | CONFORME (0 erreur, 0 a alleger) |
| J2 recablage vulcain | c22->c9b, c9b.OUI->c9c / NON->c9 ; c23->c15b, c15b.OUI->c15c / NON->c15 |
| J2 indices c6c/c12c | CREATION LIMITEE 198 -> 125 car (OK < 160) |
| J3 clio c6c | PATTERN 3 175 -> 130 car (OK < 160) |
| J4 versions + fiches | vulcain v0.4.2 / clio v0.5.2, fiches alignees |
| J5a test-018-fins-reactivation | 13 OK / 0 KO |
| J5b navigations reelles | c9b NON->c9, c9b OUI->c9e, c15b NON->c15 (fins atteintes) |
| J6a normes ASCII/LF | 5 fichiers modifies : 0 non-ASCII, 0 CRLF |
| J6b registre | 5 declarations Buffy presentes |
| J6c non-regression (Buffy) | 24 OK / 0 KO (outil lancer-non-regression) |

## Cause racine (lecons)

1. **Pattern 17 mal cable** : les questions c9b/c15b (Ameliorations possibles) etaient orphelines
   (c22.suivant pointait la fin c9 directement, et c9b.NON pointait c22 -> boucle).
   Le recablage suit le modele morpheus c8->c8b->c9.
2. **Le cycle vicieux est termine** : les ecarts signales dans les rapports sont desormais
   corriges a la mission suivante au lieu d'etre accumules.
3. **Plafond 160 car** : les indices regle doivent rester concis, l'info detaillee va dans le protocole.

## Fichiers verifies

- cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json (v0.4.2)
- cerveau-projet/agents/clio/parcours/parcours-clio.json (v0.5.2)
- cerveau-projet/agents/vulcain/vulcain.md, cerveau-projet/agents/clio/clio.md
- cerveau-projet/agents/buffy/corrections.md (lecon ajoutee)

## Transmission a Cerberus

Plus aucun ecart pre-existant ouvert sur les parcours. valider-cartes-decision 11/11 CONFORME.
