# Controle croise -- Audit Morpheus : le template est LA reference

- Date : 2026-08-12
- Controleur : Janus (session-llm-1)
- Objet : verifier la mission d audit des fichiers de tests de Morpheus
  (demande utilisateur : pourquoi le template de test n est pas utilise)

## Contexte

L utilisateur a demande un audit des fichiers de tests : Morpheus ne suivait
pas le template de test mais les tests precedents. Constat de l audit :
template-test.md v0.1.0 obsolete (format bash avec protections) alors que les
tests reels sont des .py Python purs avec [OK]/[KO], et aucune case de la carte
de Morpheus ne reference le template. Derive prouvee : test-001/002/003 en
coding utf-8 + marqueur [ECHEC] invisible pour le lanceur de non-regression
(qui compte les [KO]).

## Corrections (Vulcain + Morpheus)

| Element | Changement |
|---|---|
| template-test.md | v0.1.0 (bash/protections) -> v0.2.0 (format Python canonique : shebang, coding ascii, NB_POINTS/NB_OK/NB_KO, verifier(), run(), ascii_count/crlf_count, main() + bilan RESULTAT) |
| test-001/002/003 | migres : utf-8 + [ECHEC] -> ascii + [OK]/[KO] + structure template (10/10, 37/37, 91/91 points) |
| fiche morpheus.md | section Structure des tests reecrite (Python + template) + checklist |
| carte morpheus | v0.4.1 -> v0.4.2 ; case c3 : indice OBLIGATOIRE LIRE template-test.md en tete des indices |
| garde-fou test-029 | cree : conformite-template (14 points) : pour CHAQUE test-0XX : shebang, coding ascii jamais utf-8, def verifier/check, marqueurs [OK]/[KO], bilan RESULTAT/VERDICT/BILAN, exit fiable, aucun [ECHEC], normes ASCII/LF + template v0.2.0 + carte reference + lanceur compte les [KO] |
| test-004 | adapte : parcours morpheus 0.4.1 -> 0.4.2 |

## Verifications (J1-J7)

| Verif | Resultat |
|---|---|
| J1 : template v0.2.0 present et conforme | VALIDE (Version : 0.2.0) |
| J2 : garde-fou test-029 | VALIDE (14 OK / 0 KO) |
| J3 : carte morpheus reference template + version 0.4.2 | VALIDE (c3 : template-test.md en premier indice) |
| J4 : test-004 adapte | VALIDE (COMBO TESTER-OUTIL : VALIDE) |
| J5 : non-regression complete | VALIDE (29 OK / 0 KO sur 29 tests) |
| J6 : normes ASCII + LF | VALIDE (0 KO sur 10 fichiers) |
| J7 : registre des usages | VALIDE (3 declarations Morpheus dans l historique) |

## Verdict

**VALIDE (J1-J7)**. L audit Morpheus est complet : le template v0.2.0 est LA
reference, la carte l impose (case c3), le garde-fou test-029 empeche toute
derive future (anti-recurrence), les 3 tests deviants sont migres, la
non-regression est 29/29.

## Lecons Janus

1. UNE REFERENCE OBSOLETE EST PIRE QU ABSENTE : le template v0.1.0 decrivait
   un monde (bash/protections) qui n existait plus - les agents se calent sur
   ce qu ils voient (les tests precedents) quand la reference officielle ment.
   Mettre a jour la reference AVANT d exiger la conformite.
2. UNE DERIVE DE TEST EST INVISIBLE SANS GARDE-FOU : test-001/002/003
   derivent depuis longtemps sans que personne le voie - le garde-fou test-029
   verifie desormais les invariants de CHAQUE test a chaque non-regression.
3. UN BUMP DE PARCOURS CASCADE : morpheus 0.4.1 -> 0.4.2 a casse test-004
   (verifiait la version) - un test d integration doit etre adapte a chaque
   bump de la carte qu il reference.
