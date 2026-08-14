# evaluer-processus

Detecte les DERIVES DE PROCESSUS dans le cerveau-projet : un agent qui
utilise un outil hors de sa carte, une mission qui finit par reactiver
Cerberus alors que la carte impose Activer Janus, ou une regle de fiche qui
contredit la carte.

## Contexte

Lecons du 2026-08-13 : trois derives successives ont ete corrigees.

1. **Morpheus (consignes vs carte)** : les consignes des missions portaient
   reactiver Cerberus au lieu de activer JANUS -- l'agent a suivi la consigne
   au lieu de SA carte.
2. **Cerberus (outils hors carte)** : le gardien a lance lui-meme la
   non-regression (domaine Morpheus) -- outil hors carte par reflexe.
3. **Regle de fiche contradictoire** : la REGLE DELEGATION de Morpheus
   legitimait la derive.

evaluer-processus croise les SOURCES FIABLES (cartes JSON, fiches agents,
AGENTS.md / AGENTS-historique.md, registre des usages) pour rendre ces
derives detectables a chaque audit, sans attendre le prochain incident.

## Detections

| Type | Source | Description |
|---|---|---|
| FIN_MISSION_ERRONEE | AGENTS.md + AGENTS-historique.md | La carte impose une fin Activer Janus mais la derniere mission ecrite porte reactiver Cerberus en fin de consigne |
| OUTIL_HORS_CARTE | registre-usages-outils.jsonl | Un usage declare au registre est absent des indices outil de la carte ET des outils P0 de la fiche |
| COHERENCE_FICHE_CARTE | fiche agent | Une regle de fiche ordonne reactiver Cerberus directement alors que la carte impose Activer Janus |

## Source des usages : le registre (pas les lecons)

Les lecons (corrections.md) NE sont PAS une source fiable : elles mentionnent
les outils des autres agents et les outils audites (faux positifs massifs).
La source fiable des outils reellement utilises par chaque agent est le
registre `cerveau-projet/agents/traces/registre-usages-outils.jsonl`
(alimente par enregistrer-usage-outil).

Sont considerees autorisees : les outils assignes aux cases de la carte
(indices type=outil), les outils P0 declares dans la section "Outils de base"
de la fiche, et les outils transverses (activer-agent-principal,
enregistrer-usage-outil) qui servent au cycle Cerberus et a la trace.

## Usage

    python3 cerveau-projet/agents/tools/evaluer/evaluer-processus/evaluer-processus.py
    python3 cerveau-projet/agents/tools/evaluer/evaluer-processus/evaluer-processus.py --agent morpheus
    python3 cerveau-projet/agents/tools/evaluer/evaluer-processus/evaluer-processus.py --rapport rapport.md
    python3 cerveau-projet/agents/tools/evaluer/evaluer-processus/evaluer-processus.py --verbose

## Options

| Option | Description |
|---|---|
| `--agent <nom>` | Restreindre l'analyse a un agent |
| `--rapport <fichier>` | Ecrire le rapport markdown |
| `--verbose` | Detail complet des problemes |
| `--version` | Afficher la version |

## Sortie

Par type de probleme : liste des problemes (agent, source, detail) + compteur.
Synthese finale : 0 probleme = OK, sinon nombre de problemes.
Code de retour : 0 si aucun probleme, 1 sinon (utilisable en garde-fou).

## Version

- v0.1.1 : creation (2026-08-13). Detection sur lecons (faux positifs).
- v0.2.0 : detection OUTIL_HORS_CARTE basee sur le REGISTRE (source
  fiable), outils P0 de la fiche et transverses exclus. Corrections des
  lacunes de cartes revelees (morpheus c12/c7, vulcain c8, janus c4).
