# Audit Themis -- Tableau Agents disponibles de cerberus.md

**Date** : 2026-08-18
**Auditeur** : Themis (evaluatrice croisee)
**Cible auditee** : `cerveau-projet/agents/cerberus/cerberus.md` (section Agents disponibles)
**Contexte** : demande utilisateur -- le tableau "Agents disponibles" ne listait que 10 agents (Buffy -> Themis), 5 agents secondaires absents (Argus, Chiron, Gardien, Hermes, Hygie).

## Perimetre

Le tableau "Agents disponibles" de cerberus.md devait lister TOUS les agents du projet (la carte d entree du routeur) : les 5 manquants ont ete ajoutes par Buffy avec leurs roles (AGENTS.md) et conditions d activation (fiches).

## Verifications independantes

| Verification | Resultat |
|---|---|
| Agents listes dans le tableau | 15 : Buffy, Atlas, Janus, Vulcain, Morpheus, Athena, Promethee, Minerve, Clio, Themis, **Argus, Chiron, Gardien, Hermes, Hygie** |
| Completeness vs dossiers agents/ | OK (15/15 agents ; seul reste "classeur-variables" = faux positif, dossier de donnees type classeur, pas un agent) |
| Roles du tableau | conformes AGENTS.md (Detecteur de contradictions, Educateur, Gardien du marbre, Agent de la langue, Nettoyage) |
| "Quand l'activer" | operationnel (conditions d activation des fiches : incoherences a signaler, re-education, zone protegee, fautes, nettoyage) |
| verifier-conformite-fiche cerberus | 1 CONFORME / 0 ECART |
| Bumper --tous | 0/0 coherent |
| Evaluateur coherence | 15 liens preexistants (0 nouveau) |
| Normes fiche | ASCII 0, LF 0 |
| Perimetre git | seul cerberus.md modifie (5 lignes ajoutees) |

## Point d attention (hors perimetre de la mission)

**valider-tableaux signale "classeur-variables"** comme agent absent : c est un faux positif PREEXISTANT (signale avant cette mission aussi). `classeur-variables/` est un dossier de DONNEES de session (identite `type: classeur`, fichier classeur-variables.md), pas une fiche agent. L outil detecte tout dossier contenant `<dossier>.md` comme agent. Amelioration possible de l outil (domaine Vulcain) : ne considerer comme agent que les dossiers dont le fichier a `type: fiche-agent` dans le frontmatter.

## Verdict

**CONFORME** -- le tableau "Agents disponibles" de cerberus.md liste desormais les 15 agents du projet. La carte d entree du routeur est complete : chaque agent (y compris les 5 secondaires) est reference avec son role et sa condition d activation.

## Lecons (Themis)

1. LE TABLEAU AGENTS DISPONIBLES EST LA CARTE D ENTREE DU ROUTEUR : un agent oublie ne sera jamais active par Cerberus. L audit de completude (valider-tableaux) compare le tableau aux dossiers agents/ -- 15/15 apres correction.
2. UN FAUX POSITIF D OUTIL N EST PAS UN DEFAUT DE MISSION : "classeur-variables" (dossier de donnees, pas un agent) est signale par valider-tableaux de facon preexistante. Il ne faut PAS l ajouter au tableau (ce serait un agent fantome) -- c est l outil qui devrait distinguer `type: fiche-agent` de `type: classeur`.
3. LES ROLES ET CONDITIONS D ACTIVATION VIENNENT DE 2 SOURCES : AGENTS.md (roles) + fiches (conditions operationnelles). L audit verifie les 2, pas seulement la presence du nom.
