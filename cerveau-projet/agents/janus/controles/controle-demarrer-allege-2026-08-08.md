# Controle -- Allegement demarrer.md + enrichissement des destinations (Buffy)

**Date** : 2026-08-08
**Agent controle** : Buffy
**Session** : session-llm-1 (id: llm-1)

## Mission de controle (ecrite AVANT de controler -- Regle 1 Janus)

Controle du second controle apres la mission : alleger demarrer.md (porte d'entree
~45 lignes) + enrichir protocole-identification (MODE ID v0.4.0) + index-cerveau.md
(v0.3.0) + aligner convention-sous-protocoles.

## Points a verifier

| # | Point | Methode |
|---|---|---|
| 1 | demarrer.md allege : identification MODE ID condensee + devenir Cerberus + attendre mission + lancer le parcours (CASE 0) + pointer vers index-cerveau.md | inspection |
| 2 | Regle "Reactiver Cerberus SANS lire = inutile" conservee (citee par parcours-cerberus c11) | grep |
| 3 | Liste des 11 parcours + sections 1-7 retirees (contenu absorbe par guider-parcours.md + protocoles + index) | inspection + grep negatif |
| 4 | protocole-identification v0.2.0 : MODE ID multi-session (v0.4.0) en tete (sidentifier, alignement id llm-N -> session-llm-N, source double Id LLM, conflit, 2 LLM jamais une session) | inspection |
| 5 | index-cerveau.md v0.3.0 : Protocoles cles (7) + Fichiers cles (8) | inspection |
| 6 | convention-sous-protocoles : exemple reoriente vers protocole-demarrer-projet | inspection |
| 7 | ASCII 0 sur les 5 fichiers (demarrer, index, protocole, convention, corrections buffy) | valider-conformite-ascii |
| 8 | Liens cites (protocole-identification, index-cerveau, guider-parcours.md) existants | verification fichiers |

## Verdict

**VERDICT : VALIDE (8/8)**

| # | Point | Resultat |
|---|---|---|
| 1 | demarrer.md allege : 5 sections (S identifier MODE ID, Devenir Cerberus, Attendre la mission, Lancer le parcours CASE 0, Pour tout le reste) | OK |
| 2 | Regle Reactiver Cerberus SANS lire = inutile conservee (citee par parcours-cerberus c11) | OK (x1) |
| 3 | Liste des 11 parcours + sections 1-7 retirees (Nouveau projet 0, Carte de Decision 0, Auto-correction 0, Fichiers cles 0, parcours-vulcain.json 0) | OK |
| 4 | protocole-identification : MODE ID MULTI-SESSION en tete (sidentifier x1, session-llm-N x3, Id LLM x2, NE PARTAGENT JAMAIS UNE SESSION x1) | OK |
| 5 | index-cerveau v0.3.0 : Protocoles cles (7 protocoles) + Fichiers cles | OK |
| 6 | convention-sous-protocoles : exemple reoriente vers protocole-demarrer-projet + note porte d entree | OK |
| 7 | ASCII 0 sur les 5 fichiers (demarrer, index, protocole, convention, corrections buffy) | OK |
| 8 | Liens cites existants (protocole-identification, index-cerveau, guider-parcours.md, cerberus fiche + corrections) | OK |

**Lecon** :
1. Un grep case-sensitive peut donner un faux negatif sur une phrase en MAJUSCULES (DEUX LLM DIFFERENTS NE PARTAGENT JAMAIS UNE SESSION) : verifier avec -i
2. Un grep avec backtick dans la chaine (protocole-demarrer-projet) echoue aussi : relire le texte reel avec grep -A avant de conclure
3. L allegement de demarrer.md est coherent : le MODE ID (le contenu vraiment critique au demarrage) a ete absorbe par protocole-identification, pas perdu
