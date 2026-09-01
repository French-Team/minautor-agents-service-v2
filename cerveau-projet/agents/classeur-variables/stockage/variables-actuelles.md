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
| `profil-systeme` | OS: Windows / Bash: 5.2.37 / Python: 3.14.4 / Git: 2.53.0 / Node: 24.14.1 | verifier-systeme | 2026-08-31 | [OK] |
| `profil-session-admin` | session: session-admin / id: glm5 / agent: Cerberus / date: 2026-09-01 09:18:40.663 | activer-agent-principal | 2026-09-01 | [OK] |

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
| **Classeur actif** | Le classeur est une source d etat obligatoire : toute routine lit la variable ici avant de deduire un etat et ne conserve pas une copie implicite concurrente |
| **Trace entree/sortie** | Chaque lecture produit une activite recente `CLASSEUR ENTREE` (variable, source, agent, resultat) ; chaque ajout, modification ou suppression produit `CLASSEUR SORTIE` (variable, source, agent, resultat) |
| **Routine centrale** | Les lectures/ecritures passent par la routine de gestion du classeur ; aucun agent ne modifie le stockage directement |
| **Echec visible** | Une lecture/ecriture impossible produit une activite `CLASSEUR ENTREE` ou `CLASSEUR SORTIE` avec statut `ERREUR`, jamais un silence |

---

## Navigation

- **Parent** : [index-classeur.md](../index-classeur.md)
- **Schema** : [../schema/variables-definition.md](../schema/variables-definition.md)
- **Historique** : [../historique/historique-modifications.md](../historique/historique-modifications.md)
