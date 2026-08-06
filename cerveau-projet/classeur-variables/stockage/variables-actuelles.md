# Stockage — Variables Actuelles
---

## Variables
| Variable | Valeur | Source | Date | Statut |
|---|---|---|---|---|
| `donnees-brutes` | *(tableau de 5 objets)* | charger-donnees | 2026-08-04 | [OK] |
| `donnees-propres` | *(tableau nettoyé)* | nettoyer-donnees | 2026-08-04 | [OK] |
| `donnees-transformees` | *(tableau transformé)* | transformer-donnees | 2026-08-04 | [OK] |
| `fichier-final` | `exports/export-2026-08-04-120000.json` | exporter-donnees | 2026-08-04 | [OK] |

---

## Comment mettre à jour

### Lire une variable

```
1. Chercher dans ce tableau
2. Vérifier que la variable existe
3. Retourner la valeur
```

### Écrire une variable

```
1. Vérifier que le schéma est respecté (voir schema/variables-definition.md)
2. Ajouter ou mettre à jour la ligne dans ce tableau
3. Ajouter une entrée dans historique/historique-modifications.md
4. Noter la source (quelle fonction a écrit)
```

### Supprimer une variable

```
1. Déplacer la variable dans l'historique
2. Supprimer la ligne de ce tableau
3. Ajouter une entrée de suppression dans historique/historique-modifications.md
```

---

## Règles

| Règle | Description |
|---|---|
| **Pas de modification directe** | Modifier uniquement via les fonctions dédiées |
| **Traçabilité** | Chaque modification doit être documentée |
| **Schéma** | Chaque variable doit respecter son schéma |
| **Expiration** | Les variables peuvent avoir une date d'expiration |

---

## Navigation

- **Parent** : [index-classeur.md](../index-classeur.md)
- **Schéma** : [../schema/variables-definition.md](../schema/variables-definition.md)
- **Historique** : [../historique/historique-modifications.md](../historique/historique-modifications.md)
