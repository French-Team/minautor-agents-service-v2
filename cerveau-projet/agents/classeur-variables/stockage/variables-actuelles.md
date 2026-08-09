---
identite:
  type: classeur
  appartient_a: commun
  commun: true
---
# Stockage -- Variables Actuelles
---

## Variables
| Variable | Valeur | Source | Date | Statut |
|---|---|---|---|---|
| `donnees-brutes` | *(tableau de 5 objets)* | charger-donnees | 2026-08-04 | [OK] |
| `donnees-propres` | *(tableau nettoye)* | nettoyer-donnees | 2026-08-04 | [OK] |
| `donnees-transformees` | *(tableau transforme)* | transformer-donnees | 2026-08-04 | [OK] |
| `fichier-final` | `exports/export-2026-08-04-120000.json` | exporter-donnees | 2026-08-04 | [OK] |
| `profil-systeme` | OS: Windows / Bash: 5.2.37 / Python: 3.14.4 / Git: 2.53.0 / Node: 24.14.1 | verifier-systeme | 2026-08-07 | [OK] |
| `profil-session-llm-1` | session: session-llm-1 / id: llm-1 / agent: vulcain / date: 2026-08-09 14:23 | activer-agent-principal | 2026-08-09 | [OK] |
| `profil-session-llm-3` | session: session-llm-3 / id: kilo-llm / agent: Cerberus / date: 2026-08-08 18:17 | activer-agent-principal | 2026-08-08 | [OK] |
| `profil-session-llm-4` | session: session-llm-4 / id: llm-2 / agent: Cerberus / date: 2026-08-07 16:03 | activer-agent-principal | 2026-08-07 | [OK] |
| `profil-session-llm-5` | session: session-llm-5 / id: llm-3 / agent: Cerberus / date: 2026-08-07 16:04 | activer-agent-principal | 2026-08-07 | [OK] |
| `profil-session-llm-2` | session: session-llm-2 / agent: Cerberus / date: 2026-08-08 17:55 | activer-agent-principal | 2026-08-08 | [OK] |

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
