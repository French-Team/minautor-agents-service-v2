# classeur-v2

> Classeur de la v2 : BDD SQLite (freelance/classeur/classeur.db), parite
> fonctionnelle avec le classeur v1 mais stockage et consultation PLUS
> RAPIDES (requetes SQL au lieu d un fichier markdown lu/reecrit en entier).
>
> Decision utilisateur 2026-08-25 : la v2 a SON propre classeur, separe du
> classeur v1 (agents/classeur-variables/) -- la v2 n ecrit JAMAIS dans le
> classeur v1 (frontiere v1/v2).

| Version | 0.1.0 | Proprietaire | Vision (JARVIS) / ferrari (couche superieure) |

## Contenu (4 tables)

| Table | Contenu |
|---|---|
| `variables` | Variables cle/valeur (nom, valeur, source, date, statut) -- parite v1 |
| `sessions` | Profil des sessions v2 (session, id_llm, agent, date) -- parite profil-session-* v1 |
| `agents` | Etat des agents v2 (nom, statut, derniere_activite, mission) |
| `utilisateur` | Carte d identite de l utilisateur (RESERVE -- structure prete, a remplir) |

## Interface

### Via jarvis.py (interface recommandee, agents v2)

```
python3 cerveau-projet/freelance/tools-commun/jarvis/jarvis.py classeur variable-set <nom> <valeur> [--source S]
python3 cerveau-projet/freelance/tools-commun/jarvis/jarvis.py classeur variable-get <nom>
python3 cerveau-projet/freelance/tools-commun/jarvis/jarvis.py classeur variable-list
python3 cerveau-projet/freelance/tools-commun/jarvis/jarvis.py classeur session-set <session> [--id ID] [--agent AGENT]
python3 cerveau-projet/freelance/tools-commun/jarvis/jarvis.py classeur session-get <session>
python3 cerveau-projet/freelance/tools-commun/jarvis/jarvis.py classeur session-list
python3 cerveau-projet/freelance/tools-commun/jarvis/jarvis.py classeur agent-set <nom> [--statut S] [--mission M]
python3 cerveau-projet/freelance/tools-commun/jarvis/jarvis.py classeur agent-get <nom>
python3 cerveau-projet/freelance/tools-commun/jarvis/jarvis.py classeur agent-list
python3 cerveau-projet/freelance/tools-commun/jarvis/jarvis.py classeur utilisateur-set <champ> <valeur>
python3 cerveau-projet/freelance/tools-commun/jarvis/jarvis.py classeur utilisateur-list
python3 cerveau-projet/freelance/tools-commun/jarvis/jarvis.py classeur etat
python3 cerveau-projet/freelance/tools-commun/jarvis/jarvis.py classeur exporter
```

### Via CLI directe (outil autonome)

```
python3 cerveau-projet/freelance/classeur/entry.py <sous-commande> [args]
```

## Regles

| Regle | Description |
|---|---|
| **BDD unique** | Le classeur v2 EST la BDD SQLite (pas de fichier markdown a maintenir) |
| **Frontiere v1/v2** | La v2 n ecrit jamais dans le classeur v1 ; la v1 ne lit pas le classeur v2 (sauf outil dedie a venir) |
| **Tracabilite** | Chaque variable a une source et une date |
| **Carte identite** | Table utilisateur reservee : a remplir quand la carte d identite utilisateur sera definie |
| **Conventions v2** | UTF-8, CRLF, emojis autorises (D4) |

## Emplacement

```
cerveau-projet/freelance/classeur/
  classeur.db          <- la BDD SQLite (source de verite)
  classeur.md          <- ce document
  entry.py             <- CLI directe
  fonctions/classeur.py <- logique (tables, requetes)
```