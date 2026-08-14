# Rapport d'incoherences - readme-dev.md

**Date** : 2026-08-14
**Auteur du constat** : Clio (apres alerte utilisateur)
**Destinataire** : Themis (responsable des README, decision utilisateur)
**Objet** : readme-dev.md contient des affirmations fausses ou perimees.
**Demande utilisateur** : "le readme-dev raconte n'importe quoi (...) c'est
n'importe quoi puisqu'il est sur la route des agents comme dernier controle."

---

## INCOHERENCE 1 (MAJEURE) : activation de Janus

**Lieu** : `cerveau-projet/readme-dev.md` ligne 139, tableau des agents,
colonne "Quand l'activer".

**Texte actuel (FAUX)** :
> | **Janus** | Second controle - SEUL a lancer la non-regression complete |
> Par Cerberus, si la mission est dans la liste |

**Verite (21 preuves dans AGENTS-historique.md + fiche janus.md ligne 192)** :
Janus est active PAR LES AGENTS en fin de mission, comme DERNIER MAILLON de la
chaine (outil -> tests -> controle) : il reactiver Cerberus avec le bilan
consolide. Exemples : "FIN : lecon Clio + activer JANUS (second controle)",
"FIN : activer JANUS (conforme a ta carte c14)", "c13 : FIN - Activer Janus
(second controle) - ne PAS reactiver Cerberus directement".

**A corriger** : la colonne doit dire, par exemple : "Par les agents, en fin de
mission (dernier maillon de la chaine), ou par Cerberus pour une activation
directe".

## INCOHERENCE 2 : nombre de tests de non-regression

**Lieu** : `cerveau-projet/readme-dev.md` ligne 309, section 9.1.

**Texte actuel (FAUX)** :
> **44 tests** organises en series thematiques (a, b, c, d, e)...

**Verite** : il y a **46 tests** reels (compte des dossiers test-* dans
`cerveau-projet/agents/tools/tester/tests/` : 46). Le README public a ete
corrige a "46 tests" (refonte non-technicien) ; readme-dev est reste a 44.

**A corriger** : 44 -> 46.

## INCOHERENCE 3 : regle perimee dans la fiche janus.md (cause racine)

**Lieu** : `cerveau-projet/agents/janus/janus.md` lignes 239-240, section Limites.

**Texte actuel (contradictoire avec la pratique reelle)** :
> - Je n'interviens que si Cerberus m'active (liste definie) ou si un fichier
>   change de statut
> - Je suis active par Cerberus, jamais par l'agent controle (independance du
>   controle)

**Verite** : Janus est active par les agents en fin de mission (maillon de
chaine) depuis la regle "FIN : activer JANUS" appliquee sur toutes les cartes.
La ligne 240 contredit la pratique reelle et a probablement seme la confusion
lors de la redaction de readme-dev.

**A corriger** : reformuler les limites pour refleter la realite (active par
les agents en fin de mission comme dernier maillon ; l'independance du controle
reste vraie dans le sens ou Janus ne controle PAS son propre travail).

## ELEMENTS VERIFIES ET CONFORMES (pas d action)

- Table des outils (section 6) : 131 outils, compteurs par categorie conformes
  a la realite du disque. OK.
- Roles des agents dans le tableau (section 4) : conformes aux fiches
  (atlas, morpheus, athena, promethee, minerve, clio, themis, hygie). OK.
- Seul JANUS lance la non-regression complete : conforme (regle actuelle). OK.
- Section 9.1 : le principe (chrono, reference, pool parallele) est exact. OK.

---

## RECOMMANDATION

1. Corriger readme-dev.md : ligne 139 (activation de Janus) + ligne 309
   (44 -> 46 tests).
2. Corriger la cause racine : fiche janus.md lignes 239-240 (limites perimees).
3. Verifier apres correction : test-038-badge-readme-synchronise reste 7/7
   (readme-dev n est pas teste par la non-regression, mais verifier quand meme
   les normes ASCII/LF).
4. Documenter une lecon : lors de la redaction d un README (public ou dev),
   verifier les regles d activation dans les fiches ET la pratique reelle des
   missions (AGENTS-historique), pas seulement recopier les tableaux existants.
