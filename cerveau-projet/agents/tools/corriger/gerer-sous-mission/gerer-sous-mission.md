---
# Outil — gerer-sous-mission
# Gérer les sorties et retrées du flux principal

outil:
  nom: "gerer-sous-mission"
  version: "0.1.0"
  statut: "beta"
  cree: "2026-08-05"
  auteur: "Buffy"
  categorie: "corriger"
---

# gerer-sous-mission
---

## Objectif

Permettre à un agent de :
1. **Sauvegarder** sa position dans la mission principale
2. **Sortir** pour accomplir une sous-mission
3. **Revenir** au flux principal une fois la sous-mission terminée

---

## Commandes

### Script bash

```bash
./gerer-sous-mission.sh COMMANDE [OPTIONS]
```

### `sauvegarder`

**Usage** : `./gerer-sous-mission.sh sauvegarder --mission "description" --etape "numéro" --donnees "ce qui a été collecté"`

**Description** : Sauvegarde la position actuelle dans la mission principale.

**Sortie** :
```
[OK] Position sauvegardée
- Mission : [description]
- Étape : [numéro]
- Données : [ce qui a été collecté]
- Fichier : [chemin-vers-fichier-sauvegarde]
```

---

### `sortir`

**Usage** : `./gerer-sous-mission.sh sortir --raison "pourquoi" --outil "nom-outil"`

**Description** : Marque la sortie du flux principal pour une sous-mission.

**Sortie** :
```
[ROTATION] Sortie du flux principal
- Raison : [pourquoi]
- Outil nécessaire : [nom-outil]
- Sous-mission : [description]
```

---

### `revenir`

**Usage** : `./gerer-sous-mission.sh revenir --resultat "succès/échec" --outil-créé "oui/non"`

**Description** : Marque le retour au flux principal après une sous-mission.

**Sortie** :
```
[OK] Retour au flux principal
- Sous-mission : [description]
- Résultat : [succès/échec]
- Outil créé : [oui/non]
- On reprend à l'étape : [numéro]
```

---

### `lister`

**Usage** : `./gerer-sous-mission.sh lister`

**Description** : Liste les sous-missions en cours et les positions sauvegardées.

**Sortie** :
```
[CHECKLIST] Sous-missions en cours
1. [description] - Étape [numéro]
2. [description] - Étape [numéro]

[CHECKLIST] Positions sauvegardées
1. [mission] - Étape [numéro]
2. [mission] - Étape [numéro]
```

---

## Exemple d'utilisation

### Scénario : Vulcain crée un outil

```bash
# 1. Vulcain est en train de créer modifier-agents-md
# Il est à l'étape 1 : Vérifier le système

# 2. Il détecte que verifier-systeme n'existe pas
gerer-sous-mission sauvegarder \
  --mission "Créer modifier-agents-md" \
  --etape "1" \
  --donnees "Outil demandé par Cerberus"

# 3. Il sort du flux pour créer verifier-systeme
gerer-sous-mission sortir \
  --raison "verifier-systeme n'existe pas" \
  --outil "verifier-systeme"

# 4. Il crée verifier-systeme
# ... développement ...

# 5. Il revient au flux principal
gerer-sous-mission revenir \
  --resultat "succès" \
  --outil-créé "oui"

# 6. Il reprend à l'étape 1
# verifier-systeme existe maintenant !
```

---

## Fichier de sauvegarde

### Format

```json
{
  "mission": "Créer modifier-agents-md",
  "etape": "1",
  "donnees": "Outil demandé par Cerberus",
  "date_sauvegarde": "2026-08-05T10:00:00",
  "sous_missions": [
    {
      "raison": "verifier-systeme n'existe pas",
      "outil": "verifier-systeme",
      "statut": "terminée",
      "resultat": "succès"
    }
  ]
}
```

### Emplacement

```
cerveau-projet/agents/[agent]/sauvegardes/[mission]-[date].json
```

---

## Règles

1. **Toujours sauvegarder avant de sortir** — Sinon, impossible de revenir
2. **Toujours revenir après une sous-mission** — La sous-mission n'est pas une fin
3. **Documenter chaque sortie/retrée** — Pour l'historique et le débogage
4. **Une sous-mission à la fois** — Pas d'imbrication sauf si nécessaire

---

## Dépendances

| Outil | Usage | Statut |
|---|---|---|
| `lister-outils` | Vérifier si un outil existe | Créé |
| `verifier-systeme` | Vérifier le système | À créer |

---

