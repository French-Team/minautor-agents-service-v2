# Controle Janus -- Tableau Agents disponibles de cerberus.md

**Date** : 2026-08-18
**Controleur** : Janus (controleur des statuts, session habilitee)
**Cible** : `cerveau-projet/agents/cerberus/cerberus.md` (section Agents disponibles)
**Contexte** : demande utilisateur -- le tableau "Agents disponibles" ne listait que 10 agents (Buffy -> Themis) ; 5 agents secondaires absents (Argus, Chiron, Gardien, Hermes, Hygie). Chaine : Cerberus -> Buffy (application) -> Themis (audit CONFORME) -> Janus (controle final).

## Perimetre controle

Le tableau "Agents disponibles" devait lister TOUS les agents du projet (carte d entree du routeur) : 5 lignes ajoutees (Argus, Chiron, Gardien, Hermes, Hygie) avec roles AGENTS.md + conditions d activation des fiches.

## Verifications sous session habilitee (Janus)

| Verification | Resultat |
|---|---|
| Agents listes | 15 : Buffy, Atlas, Janus, Vulcain, Morpheus, Athena, Promethee, Minerve, Clio, Themis, Argus, Chiron, Gardien, Hermes, Hygie |
| Les 5 manquants presents | OUI (Argus, Chiron, Gardien, Hermes, Hygie) |
| Completeness vs dossiers agents/ | 15/15 (seul reste "classeur-variables" = faux positif outil PREEXISTANT, dossier de donnees type classeur, pas un agent) |
| verifier-conformite-fiche cerberus | 1 CONFORME / 0 ECART |
| Bumper --tous | 0/0 coherent |
| Marbre --tous | 8/8 zones conformes |
| Evaluateur coherence | 15 liens preexistants (0 nouveau) |
| Registre JSONL | 821/821 lignes valides |
| Normes fiche | ASCII 0, LF 0 |
| Perimetre git | cerberus.md + rapport audit Themis (rien d autre) |
| Residus (.bak, .zz) | 0 |

## Verdict

**VALIDE** -- le tableau "Agents disponibles" de cerberus.md liste desormais les 15 agents du projet, y compris les 5 secondaires manquants. La carte d entree du routeur est complete et conforme.

## Point d attention (hors perimetre)

**valider-tableaux signale "classeur-variables"** : faux positif PREEXISTANT (deja signale avant cette mission). Le dossier `classeur-variables/` est un classeur de donnees de session (`type: classeur`), pas un agent. Amelioration outil possible (domaine Vulcain) : ne considerer comme agent que les dossiers dont le fichier a `type: fiche-agent` dans le frontmatter. A NE PAS ajouter au tableau (ce serait un agent fantome).

## Lecons (Janus)

1. LE TABLEAU AGENTS DISPONIBLES EST LA CARTE D ENTREE DU ROUTEUR : un agent oublie = jamais active par Cerberus. Le controle de completude (valider-tableaux) compare le tableau aux dossiers agents/ -- 15/15 apres correction.
2. UN FAUX POSITIF PREEXISTANT D OUTIL N INVALIDE PAS UNE MISSION : "classeur-variables" etait deja signale AVANT la correction. Il est documente comme point d attention (amelioration outil pour Vulcain), pas comme defaut de la mission.
3. LE CONTROLE VERIFIE LES 2 SOURCES DES LIGNES : roles (AGENTS.md) ET conditions d activation (fiches). La seule presence du nom ne suffit pas -- chaque ligne doit etre operationnelle.
