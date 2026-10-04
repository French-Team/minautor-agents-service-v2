# proteger-verrou-habilitation

**Version :** 0.6.0
**Statut :** ebauche
**Categorie :** Proteger

## Pourquoi cet outil ?

Les regles de gouvernance exclusives (regles-groupes-agents.md) interdisent a
un agent d utiliser un outil reserve a un autre (seul janus lance la
non-regression, seul hygie supprime, seul morpheus ecrit les tests, seul clio
met a jour le README). Les garde-fous (test-035, test-037, test-045)
verifient ces regles APRES coup (au moment du controle). Le verrou les
applique AVANT coup : au moment ou l agent appelle l outil.

Un agent qui n est pas habilite est bloque des la demande, avec le nom de
l agent habilite et la commande exacte pour l activer (cycle Cerberus ->
agent habilite -> retour).

## Fonctionnement

1. L agent appelle le verrou avec son nom (`--agent`) et l outil souhaite
   (`--outil`) :
   `python3 proteger-verrou-habilitation.py --agent janus --outil tester-lancer-non-regression`
2. Le verrou lit la source de verite : les cartes de decision
   (`cerveau-projet/agents/*/parcours/parcours-*.json`), c est-a-dire les
   indices de type `outil` de chaque case.
3. IDENTITE REELLE (v0.2.0) : le verrou verifie en plus que l agent DECLARE
   est bien l agent REEL de la session (colonne Agent actif de la table
   '## Sessions connues' d AGENTS.md). Un script lance par Cerberus qui se
   fait passer pour janus est BLOQUE : la session porte Cerberus, pas janus.
4. Verdict :
   - l agent declare est l agent reel de la session ET l outil est dans sa
     carte -> **OK** (verrou ouvert, code 0) ;
   - sinon -> **BLOQUE** (verrou ferme, code 1) avec la liste des agents
     habilites et la commande d activation ;
   - l outil n est assigne a aucune carte -> BLOQUE (code 1) avec alerte de
     declaration manquante.

## Liste blanche developpeur (v0.2.2)

Regle utilisateur 2026-08-16 : le CONSTRUCTEUR de l outil
`tester-lancer-non-regression` (vulcain) doit pouvoir VALIDER ses
modifications sans attendre janus. Il est donc autorise DIRECTEMENT dans le
verrou, comme janus (qui est habilite via sa carte) :

- couverture STRICTE : outil `tester-lancer-non-regression` + agent `vulcain`
  uniquement. Tous les autres agents restent BLOQUES (carte = regle) ;
- les essais de validation sont journalises au mode `verrou-dev` dans
  registre-usages-outils.jsonl (trace distincte, ignoree par
evaluer-processus, autorisee par test-037).

## Auto-journalisation (espionnage, v0.2.0)

Le verrou journalise lui-meme chaque appel, sans attendre la declaration de
l agent :

- usage AUTORISE -> `cerveau-projet/agents/traces/registre-usages-outils.jsonl`
  (mode `verrou-auto` : qui a utilise quoi, quand) ;
- tentative BLOQUEE -> `cerveau-projet/agents/traces/registre-tentatives-bloquees.jsonl`
  (espionnage : qui a essaye d utiliser quoi, et quel agent reel etait actif).

Ainsi, pour les outils passes au verrou, l outil signale son propre usage :
l agent n a plus besoin de se declarer lui-meme.

## Source de verite (aucune liste en dur)

La table outil -> agents habilites est construite DYNAMIQUEMENT depuis les
parcours des agents. Aucune liste en dur dans le script : si une carte
evolue, le verrou suit automatiquement. C est la meme philosophie que les
garde-fous test-035/037/045 (la carte EST la regle).

## Usage

```
python3 proteger-verrou-habilitation.py --agent <nom> --outil <nom>
python3 proteger-verrou-habilitation.py --agent janus --outil tester-lancer-non-regression
python3 proteger-verrou-habilitation.py --agent janus --outil tester-lancer-non-regression --audit
python3 proteger-verrou-habilitation.py --liste
```

## Options

| Option | Description |
|---|---|
| `--agent <nom>` | Nom de l agent appelant (OBLIGATOIRE pour verrouiller) |
| `--outil <nom>` | Nom de l outil a utiliser (OBLIGATOIRE pour verrouiller) |
| `--audit` | Mode audit/tests : verifie la table d habilitation SANS verifier l identite reelle de la session (reserve aux preuves formelles) |
| `--verrou-interne` | Verrou bleu (v0.5.0) : croise ET EXIGE une mission oracle EN_ATTENTE/PRISE pour l agent declare (source de verite du round, pas la seule reecriture d AGENTS.md) |
| `--liste` | Affiche la table complete outil -> agents habilites |
| `--verbose` | Detail du verdict (liste des habilites, source) |
| `--version` | Affiche la version |

## Codes de sortie

| Code | Signification |
|---|---|
| 0 | OK - l agent declare est l agent reel de la session ET habilite (verrou ouvert) |
| 1 | BLOQUE - l agent n est pas habilite, usurpation d identite, ou l outil n est assigne a aucune carte |
| 2 | Erreur d utilisation (agent/outil manquant, agent inconnu, identite de session indeterminable) |

## Exemples

Verrou ouvert (janus est habilite pour la non-regression) :

```
$ python3 proteger-verrou-habilitation.py --agent janus --outil tester-lancer-non-regression
OK : l agent 'janus' est habilite pour l outil 'tester-lancer-non-regression' (verrou ouvert).
```

Usurpation d identite (un script lance par la session Cerberus se fait
passer pour janus) :

```
$ python3 proteger-verrou-habilitation.py --agent janus --outil tester-lancer-non-regression
BLOQUE : usurpation d identite - la session est sur l agent 'Cerberus', pas 'janus'. Activez d abord l agent habilite (activer-agent-principal).
```

Verrou ferme (cerberus n est pas habilite pour la non-regression, mode audit) :

```
$ python3 proteger-verrou-habilitation.py --agent cerberus --outil tester-lancer-non-regression
BLOQUE : l agent 'cerberus' n est PAS habilite pour l outil 'tester-lancer-non-regression' (verrou ferme).
  Agent(s) habilite(s) : janus
  Action requise : activez l agent habilite puis redemandez l outil.
  Commande : python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py activer <session> janus 'activation par le verrou'
  # v0.4.1 (D6) : <session> = la session de l appelant (SESSION_LLM ou classeur), plus de session-llm-1 figee
```

## Integration dans la chaine

Le verrou se place AVANT tout outil critique dans les combos et les scripts
temporaires : l agent doit prouver son habilitation avant d agir. Un garde-fou
de non-regression verifie que le verrou existe, se compile, et bloque
correctement les agents non habilites (preuve negative).

## Verrou interne (v0.5.0, Verrou bleu)

La faille historique : l identite etait AUTO-DECLAREE dans AGENTS.md (colonne
"Agent actif" de la table '## Sessions connues'), un fichier que la session
modifie directement. Un LLM qui sortait du flux pouvait y reecrire le nom de
l agent habilite pour deverrouiller un outil dedie.

Le Verrou bleu elimine cette autorite auto-declaree : l option
`--verrou-interne` exige en PLUS qu une mission oracle (EN_ATTENTE ou PRISE)
soit reellement relayee pour l agent declare (`oracle.py mission-lister
--statut EN_ATTENTE --agent <X>`). Seule la presence dans AGENTS.md ne sert
plus d autorite : il faut que le round ait passe par oracle.

Usage :

```
python3 proteger-verrou-habilitation.py --agent <X> --outil <O> --verrou-interne
```

En mode hybride (recommandation Buffy, blueprint-verrou-bleu.md), ce
croisement est le signal le plus fiable d une incarnation reelle : une
reecriture a la main du nom sans DEBUT/FIN oracle coherent est bloquee.
