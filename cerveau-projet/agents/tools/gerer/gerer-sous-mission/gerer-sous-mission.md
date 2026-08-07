# gerer-sous-mission

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** gerer
**Chemin :** `agents/tools/gerer/gerer-sous-mission/`
**Proprietaire :** Buffy (outil partage)

---

## Objectif

Permettre a un agent de :
1. **Sauvegarder** sa position dans la mission principale
2. **Sortir** pour accomplir une sous-mission
3. **Revenir** au flux principal une fois la sous-mission terminee

---

## Commandes

### Script bash

```bash
./gerer-sous-mission.sh COMMANDE [OPTIONS]
# Version Python (recommandee)
python3 gerer-sous-mission.py COMMANDE [OPTIONS]
```

### `sauvegarder`

**Usage** : `./gerer-sous-mission.sh sauvegarder --mission "description" --etape "numero" --donnees "ce qui a ete collecte"`

**Description** : Sauvegarde la position actuelle dans la mission principale.

**Sortie** :
```
[OK] Position sauvegardee
- Mission : [description]
- Etape : [numero]
- Donnees : [ce qui a ete collecte]
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
- Outil necessaire : [nom-outil]
- Sous-mission : [description]
```

---

### `revenir`

**Usage** : `./gerer-sous-mission.sh revenir --resultat "succes/echec" --outil-cree "oui/non"`

**Description** : Marque le retour au flux principal apres une sous-mission.

**Sortie** :
```
[OK] Retour au flux principal
- Sous-mission : [description]
- Resultat : [succes/echec]
- Outil cree : [oui/non]
- On reprend a l'etape : [numero]
```

---

### `lister`

**Usage** : `./gerer-sous-mission.sh lister`

**Description** : Liste les sous-missions en cours et les positions sauvegardees.

**Sortie** :
```
[CHECKLIST] Sous-missions en cours
1. [description] - Etape [numero]
2. [description] - Etape [numero]

[CHECKLIST] Positions sauvegardees
1. [mission] - Etape [numero]
2. [mission] - Etape [numero]
```

---

## Exemple d'utilisation

### Scenario : Vulcain cree un outil

```bash
# 1. Vulcain est en train de creer activer-agent-principal
# Il est a l'etape 1 : Verifier le systeme

# 2. Il detecte que verifier-systeme n'existe pas
gerer-sous-mission sauvegarder \
  --mission "Creer activer-agent-principal" \
  --etape "1" \
  --donnees "Outil demande par Cerberus"

# 3. Il sort du flux pour creer verifier-systeme
gerer-sous-mission sortir \
  --raison "verifier-systeme n'existe pas" \
  --outil "verifier-systeme"

# 4. Il cree verifier-systeme
# ... developpement ...

# 5. Il revient au flux principal
gerer-sous-mission revenir \
  --resultat "succes" \
  --outil-cree "oui"

# 6. Il reprend a l'etape 1
# verifier-systeme existe maintenant !
```

---

## Fichier de sauvegarde

### Format

```json
{
  "mission": "Creer activer-agent-principal",
  "etape": "1",
  "donnees": "Outil demande par Cerberus",
  "date_sauvegarde": "2026-08-05T10:00:00",
  "sous_missions": [
    {
      "raison": "verifier-systeme n'existe pas",
      "outil": "verifier-systeme",
      "statut": "terminee",
      "resultat": "succes"
    }
  ]
}
```

### Emplacement

```
cerveau-projet/agents/[agent]/sauvegardes/[mission]-[date].json
```

---

## Regles

1. **Toujours sauvegarder avant de sortir** -- Sinon, impossible de revenir
2. **Toujours revenir apres une sous-mission** -- La sous-mission n'est pas une fin
3. **Documenter chaque sortie/retree** -- Pour l'historique et le debogage
4. **Une sous-mission a la fois** -- Pas d'imbrication sauf si necessaire

---

## Dependances

| Outil | Usage | Statut |
|---|---|---|
| `lister-outils` | Verifier si un outil existe | Cree |
| `verifier-systeme` | Verifier le systeme | A creer |

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-05 | Creation initiale (frontmatter YAML) |
| 0.2.0 | 2026-08-07 | Conversion format v2 : frontmatter markdown, statut prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (4 commandes, JSON gere en natif, --version) |
