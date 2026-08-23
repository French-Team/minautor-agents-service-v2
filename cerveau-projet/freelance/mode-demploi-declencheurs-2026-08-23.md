# Mode d'emploi -- Les 6 declencheurs (protocole 13 v2)

> Cree le 2026-08-23. Reference complete : protocoles/protocoles.md
> (PROTOCOLE 13 v2). Mecanique : tools-commun/jarvis/jarvis.py v0.8.0 +
> jarvis-server.py v0.8.0.

---

## Utilisation

Ecris ta demande en plaçant le prefixe EN TETE :

```
[attente]  la demande...
[attention] la demande...
[urgent]   la demande...
[creer]    ce qu'il faut creer...
[probleme] le probleme constate...
[stop]     la raison de l'arret...
```

## Ce que fait chaque declencheur

### [attente] -- parker sans perdre
La mission en cours est placee en `file-attente.jsonl` (statut EN_ATTENTE,
ordre normal). Ta demande sera traitee apres la file. RIEN n'est perdu :
chaque entree porte son contexte de reprise.

### [attention] -- juste apres
Ta demande est placee en `file-asap.jsonl` avec statut **SUIVANTE** :
elle sera executee DIRECTEMENT APRES la mission en cours.

### [urgent] -- prend le dessus
Ta demande est traitee IMMEDIATEMENT. La mission en cours est placee en
file-attente avec statut **PRIORITAIRE** : elle repasse avant tout le reste
des que l'urgence est reglee.

### [creer] -- routage de creation
Route vers les protocoles de creation PAR TYPE :
| Creation | Protocole |
|---|---|
| Agent v2 | PROTOCOLE 9 |
| Outil v2 | PROTOCOLE 10 |
| Autre | arbitrage Stark via JARVIS |

### [probleme] -- routage de resolution (par type de fichier)
| Fichier en cause | Habilite |
|---|---|
| jarvis.py / jarvis-server.py / files/ | Vision (exclusif) |
| *.json de donnees | Forge puis Rogers |
| regles / conventions / protocoles | Rogers |
| fiches / arbres d'agents | Shuri |
| historique / git | Hades (v1) - arbitrage Stark |

### [stop] -- DEFCON 5, gravite maximale
ROUND BRISE. Arret complet du dev : TOUTES les missions en files sont
GELEES (statut DEFCON5), l'arret est journalise dans files/defcon.jsonl.
Toute reprise exige TA decision explicite.

---

## Commandes mecaniques (jarvis.py / serveur MCP)

| Commande | Role |
|---|---|
| `mettre-en-attente --mission X --contexte Y [--niveau attente\|attention\|urgent]` | placer une mission selon le declencheur |
| `file` | lister les deux files |
| `reprendre [--file F]` | reprendre la mission la plus prioritaire (PRIORITAIRE > SUIVANTE > EN_ATTENTE) |
| `stop-dev --raison X` | [stop] DEFCON 5 |

## Ordre de reprise

`PRIORITAIRE` > `SUIVANTE` > `EN_ATTENTE`

## Exemple reel (2026-08-23)

```
Utilisateur : "[urgent] je ne vois pas 'jarvis' dans agents-historique..."
Stark       : reconnait [urgent] -> transmet a JARVIS
JARVIS      : met la philosophie en file (contexte capture) -> active Vision
Vision      : repare (v0.6.2) -> bilan -> JARVIS -> Stark
Puis        : reprendre -> la philosophie reprend avec son contexte intact
```
