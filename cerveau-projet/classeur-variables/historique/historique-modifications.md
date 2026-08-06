# Historique — Modifications
---

## Entrées récentes
## 2026-08-04T12:00:00Z — Écriture

- **Variable** : donnees-brutes
- **Ancienne valeur** : *(aucune)*
- **Nouvelle valeur** : *(tableau de 5 objets)*
- **Source** : charger-donnees
- **Raison** : Initialisation des données brutes pour le pipeline exemple

## 2026-08-04T12:00:01Z — Écriture

- **Variable** : donnees-propres
- **Ancienne valeur** : *(aucune)*
- **Nouvelle valeur** : *(tableau nettoyé)*
- **Source** : nettoyer-donnees
- **Raison** : Nettoyage des données brutes

## 2026-08-04T12:00:02Z — Écriture

- **Variable** : donnees-transformees
- **Ancienne valeur** : *(aucune)*
- **Nouvelle valeur** : *(tableau transformé)*
- **Source** : transformer-donnees
- **Raison** : Transformation des données nettoyées

## 2026-08-04T12:00:03Z — Écriture

- **Variable** : fichier-final
- **Ancienne valeur** : *(aucune)*
- **Nouvelle valeur** : `exports/export-2026-08-04-120000.json`
- **Source** : exporter-donnees
- **Raison** : Export des données transformées

---

## Comment ajouter une entrée

### Après une écriture

```markdown
## [DATE] — Écriture

- **Variable** : [nom-variable]
- **Ancienne valeur** : [ancienne valeur ou "nouvelle"]
- **Nouvelle valeur** : [nouvelle valeur]
- **Source** : [nom-fonction]
- **Raison** : [description]
```

### Après une suppression

```markdown
## [DATE] — Suppression

- **Variable** : [nom-variable]
- **Valeur supprimée** : [valeur]
- **Source** : [nom-fonction]
- **Raison** : [description]
```

### Après une lecture (optionnel, pour audit)

```markdown
## [DATE] — Lecture

- **Variable** : [nom-variable]
- **Valeur lue** : [valeur]
- **Source** : [nom-fonction]
- **Raison** : [description]
```

---

## Format d'entrée

Chaque entrée doit contenir :

| Champ | Obligatoire | Description |
|---|---|---|
| Date | [OK] | Date et heure de l'opération |
| Type | [OK] | Écriture, Suppression, ou Lecture |
| Variable | [OK] | Nom de la variable concernée |
| Valeur | [OK] | Nouvelle valeur ou valeur supprimée |
| Source | [OK] | Fonction qui a effectué l'opération |
| Raison | [OK] | Description de l'opération |

---

## Règles

| Règle | Description |
|---|---|
| **Ordre chronologique** | Les entrées les plus récentes en premier |
| **Pas de suppression** | L'historique est immuable |
| **Traçabilité complète** | Chaque opération doit être documentée |
| **Rétention** | Garder au moins les 100 dernières entrées |

---

## Navigation

- **Parent** : [index-classeur.md](../index-classeur.md)
- **Stockage** : [../stockage/variables-actuelles.md](../stockage/variables-actuelles.md)
- **Schéma** : [../schema/variables-definition.md](../schema/variables-definition.md)
