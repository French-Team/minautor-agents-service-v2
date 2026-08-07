# Stockage -- Variables Actuelles
---

## Variables
| Variable | Valeur | Source | Date | Statut |
|---|---|---|---|---|
| `donnees-brutes` | *(tableau de 5 objets)* | charger-donnees | 2026-08-04 | [OK] |
| `donnees-propres` | *(tableau nettoye)* | nettoyer-donnees | 2026-08-04 | [OK] |
| `donnees-transformees` | *(tableau transforme)* | transformer-donnees | 2026-08-04 | [OK] |
| `fichier-final` | `exports/export-2026-08-04-120000.json` | exporter-donnees | 2026-08-04 | [OK] |
| `profil-systeme` | OS: Windows 10 / Bash: 5.2 / Python: 3.14 / Git: 2.53 | verifier-systeme | 2026-08-07 | [OK] |

---

## Comment mettre a jour

### Lire une variable

```
1. Chercher dans ce tableau
2. Verifier que la variable existe
3. Retourner la valeur
```

### Ecrire une variable

```
1. Verifier que le schema est respecte (voir schema/variables-definition.md)
2. Ajouter ou mettre a jour la ligne dans ce tableau
3. Ajouter une entree dans historique/historique-modifications.md
4. Noter la source (quelle fonction a ecrit)
```

### Supprimer une variable

```
1. Deplacer la variable dans l'historique
2. Supprimer la ligne de ce tableau
3. Ajouter une entree de suppression dans historique/historique-modifications.md
```

---

## Regles

| Regle | Description |
|---|---|
| **Pas de modification directe** | Modifier uniquement via les fonctions dediees |
| **Tracabilite** | Chaque modification doit etre documentee |
| **Schema** | Chaque variable doit respecter son schema |
| **Expiration** | Les variables peuvent avoir une date d'expiration |

---

## Navigation

- **Parent** : [index-classeur.md](../index-classeur.md)
- **Schema** : [../schema/variables-definition.md](../schema/variables-definition.md)
- **Historique** : [../historique/historique-modifications.md](../historique/historique-modifications.md)
