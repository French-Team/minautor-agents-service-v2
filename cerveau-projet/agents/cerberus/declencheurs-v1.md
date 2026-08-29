# Mode d'emploi -- Les declencheurs v1 (Cerberus)

> Cree le 2026-08-29. Transposition du concept v2 (mode-demploi-declencheurs
> v2, protocole 13 v2) adaptee a la v1 : **Cerberus est TOUJOURS l'agent
> avec qui tu parles**. Tu places le prefixe EN TETE de ta demande, Cerberus
> reconnait le declencheur et declenche l'evenement correspondant (case de
> detection cD de son parcours).

---

## Utilisation

Ecris ta demande en placant le prefixe EN TETE :

```
[attente]   la demande...
[attention] la demande...
[urgent]    la demande...
[question]  la question...
[creer]     ce qu'il faut creer...
[probleme]  le probleme constate...
[stop]      la raison de l'arret...
```

Sans prefixe : Cerberus traite la demande normalement (ecoute, analyse,
active l'agent habilite).

## Ce que fait chaque declencheur

### [attente] -- parker sans perdre
La demande est placee dans la file `plus-tard` (statut EN_ATTENTE) via
`oracle.py mission-ajouter --file plus-tard`. Elle sera traitee apres la
file. RIEN n'est perdu : chaque entree porte son contexte de reprise.

### [attention] -- juste apres
La demande est placee dans la file `asap` (statut SUIVANTE) via
`oracle.py mission-ajouter --file asap` : elle sera executee DIRECTEMENT
APRES la mission en cours.

### [urgent] -- prend le dessus
La demande est traitee IMMEDIATEMENT. Cerberus l'analyse en priorite et
active l'agent habilite tout de suite (la mission en cours eventuelle est
mise en attente dans la file `asap` avec statut PRIORITAIRE).

### [question] -- phase question/reponse dediee
Ouvre une phase DEDIEE entre toi et Cerberus :
1. Tu poses ta question ([question] ...)
2. Cerberus repond directement (dialogue) ou active l'agent qui detient
   l'information (Atlas pour l'exploration, Socrate pour la strategie...)
   qui lui retourne la reponse.
3. Cerberus repond avec les informations collectees.
Aucune autre tache pendant la phase.

### [creer] -- routage de creation PAR TYPE
| Creation | Agent habilite v1 |
|---|---|
| Outil (agents/tools) | Vulcain (constructeur d'outils) |
| Fichier / code / doc | Buffy (developpeur principal) |
| Pense-bete | Athena (redactrice de pense-betes) |
| Spec | Promethee (redacteur de specs) |
| Todo | Minerve (redactrice de todos) |
| Agent | Buffy (processus de creation d'agent) |

### [probleme] -- routage de resolution (par type de fichier)
| Fichier en cause | Agent habilite v1 |
|---|---|
| Outil du cerveau (agents/tools) | Vulcain puis Morpheus (tests) |
| Regles / conventions / protocoles | Buffy |
| Tests / non-regression | Morpheus (testeur) |
| Marbre / zones protegees | Gardien (l'utilisateur valide) |
| Git / historique | Hades (SEUL habilite git) |
| Langue / orthographe | Hermes |
| Workspace / nettoyage | Hygie (SEULE habilite tout le workspace) |
| Contradictions / incoherences | Argus (detecte et signale, ne corrige jamais) |
| Fichiers v2 (freelance/) | ferrari (agent v1 specialise v2) |

### [stop] -- DEFCON 5, gravite maximale
ROUND BRISE. Arret complet : Cerberus declare le DEFCON 5 via
`oracle.py defcon-declarer <raison>` (journalise dans files/defcon.jsonl,
les routines le surveillent). Toute reprise exige TA decision explicite.

---

## Mecanique (cote Cerberus)

| Declencheur | Commande oracle | Effet |
|---|---|---|
| [attente] | `oracle.py mission-ajouter "<mission>" --file plus-tard` | file plus-tard (EN_ATTENTE) |
| [attention] | `oracle.py mission-ajouter "<mission>" --file asap` | file asap (SUIVANTE) |
| [urgent] | traitement immediat + `mission-ajouter --file asap` si mission en cours | priorite absolue |
| [question] | dialogue direct ou activation de l'agent info-holder | phase Q/R dediee |
| [creer] | activer l'agent de creation par type (tableau ci-dessus) | routage creation |
| [probleme] | activer l'agent de resolution par fichier (tableau ci-dessus) | routage resolution |
| [stop] | `oracle.py defcon-declarer "<raison>"` | DEFCON 5, arret total |

## Ordre de reprise des files

`PRIORITAIRE` > `SUIVANTE` > `EN_ATTENTE` (lecture via
`oracle.py mission-lister` / `mission-prendre`).

## Exemple reel (parite v2)

```
Utilisateur : "[urgent] je ne vois pas 'activer-agent-principal' dans index-tools..."
Cerberus    : reconnait [urgent] -> traite immediatement -> identifie l'agent
              habilite (Vulcain si outil, Argus si detection...) -> l'active
Agent       : resout -> la fin suit SA carte -> reactiver Cerberus avec le bilan
```
