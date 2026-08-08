---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# lister-agents

**Categorie** : Lister
**Version** : 0.3.0
**Statut** : prepare
**Date creation** : 2026-08-05
**Proprietaire** : Buffy (outil partage)

---

## Objectif

Lister tous les agents du cerveau-projet avec leurs informations essentielles.

**Pourquoi cet outil ?**
- Cet outil retourne exactement ce dont on a besoin
- Il est optimise pour nos projets futurs
- Il evolue avec nos besoins
- Il est concu pour nos agents et nos projets

---

## Utilisation

Version Python (recommandee) :

```bash
python3 lister-agents.py [OPTIONS]
```

### Options

| Option | Description |
|---|---|
| `--detail, -d` | Afficher le detail complet de chaque agent |
| `--verbose, -v` | Afficher les details d'execution |
| `--version` | Afficher la version |
| `--aide, -h` | Afficher l'aide |

### Exemples

```bash
python3 lister-agents.py          # Liste table des agents
python3 lister-agents.py --detail # Liste detaillee
```

Version bash equivalente : `lister-agents.sh` (meme logique, dossier source par defaut).

---

## Resultat

### Format table (defaut)

```markdown
| Agent | Role | Statut | Dossier |
|---|---|---|---|
| Cerberus | Gardien de l'entree | Disponible (principal) | cerberus/ |
| Buffy | Developpeur principal | Disponible (en attente) | buffy/ |
| Atlas | Explorateur | Disponible (en attente) | atlas/ |
| Janus | Second controle | Disponible (sur demande) | janus/ |
```

### Format liste

```markdown
- **Cerberus** : Gardien de l'entree [Disponible]
- **Buffy** : Developpeur principal [En attente]
- **Atlas** : Explorateur [En attente]
- **Janus** : Second controle [Sur demande]
```

### Format JSON

```json
[
  {"nom": "Cerberus", "role": "Gardien de l'entree", "statut": "disponible"},
  {"nom": "Buffy", "role": "Developpeur principal", "statut": "en attente"},
  {"nom": "Atlas", "role": "Explorateur", "statut": "en attente"},
  {"nom": "Janus", "role": "Second controle", "statut": "sur demande"}
]
```

---

## Exemples

### Exemple 1 -- Lister tous les agents

```
lister-agents()
```

**Resultat** : Liste complete de tous les agents.

### Exemple 2 -- Lister les agents actifs

```
lister-agents(filtre="statut:disponible")
```

**Resultat** : Uniquement les agents avec le statut "disponible".

### Exemple 3 -- Lister avec champs specifiques

```
lister-agents(champs="nom,role")
```

**Resultat** : Uniquement les noms et roles.

---

## Implementation

### Comment ca fonctionne

1. Lire `cerveau-projet/agents/index-agents.md`
2. Extraire la table des agents
3. Formater selon le parametre `format`
4. Appliquer le filtre si specifie
5. Retourner le resultat

### Ce que fait cet outil

| Capacite | Description |
|---|---|
| Format table/liste/JSON | Choisissez le format de sortie |
| Filtre par statut/role | Recuperez uniquement ce dont vous avez besoin |
| Optimise | Concus pour nos agents et nos projets |

---

## Dependances

- `cerveau-projet/agents/index-agents.md` -- source de donnees

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels, corrections, promotion |
| 0.2.0-py | 2026-08-07 | Version Python creee (lister-agents.py), basee sur outil-template.py |
| 0.3.0 | 2026-08-08 | CONVENTION IDENTIFICATION : lecture des nouveaux champs YAML des fiches -- role-agent et statut-<agent> (anciens noms role: / statut: acceptes en repli). py + sh + doc |

---

## Notes

- Cet outil est le premier d'une serie d'outils d'agent
- Il est concu pour evoluer avec nos besoins
- Chaque agent peut l'ameliorer selon ses besoins
- Il est partage entre tous les agents

---

