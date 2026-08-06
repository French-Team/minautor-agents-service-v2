# Protocole — Contrôle des Statuts

**Version** : 0.1.0
**Statut** : Ébauche
**Date création** : 2026-08-05
**Agent** : Janus (contrôleur)

---

## Objectif

Définir comment Janus contrôle les transitions de statut des fichiers du cerveau-projet.

**Pourquoi ce protocole ?**
- Le workflow RVAV existe mais personne ne le vérifie
- Les agents peuvent tricher ou oublier les boucles RVAV
- La qualité exige un contrôle indépendant
- Janus est l'agent spécialisé dans le second contrôle

---

## Le rôle de Janus

### Responsabilités

| Responsabilité | Description |
|---|---|
| **Contrôler les transitions** | Vérifier que les changements de statut sont légitimes |
| **Valider les boucles RVAV** | S'assurer que chaque boucle est complète |
| **Détecter les erreurs** | Identifier les fichiers qui ne respectent pas le workflow |
| **Documenter les décisions** | Justifier chaque validation ou rejet |

### Limites

| Limite | Raison |
|---|---|
| **Ne crée pas de fichiers** | Janus ne crée que du contrôle |
| **Ne modifie pas le contenu** | Il valide, pas il ne corrige |
| **Ne saute pas Cerberus** | Toujours revenir au coordinateur |

---

## Le processus de contrôle

```
FICHIER → VÉRIFICATION → ANALYSE → DÉCISION → DOCUMENTATION
    1          2            3          4           5
```

| Étape | Action | Responsable |
|---|---|---|
| 1 | Lire le fichier et son statut | Janus |
| 2 | Vérifier la boucle RVAV | Janus |
| 3 | Analyser la cohérence | Janus |
| 4 | Décider : valider ou rejeter | Janus |
| 5 | Documenter la décision | Janus |

---

## Étape 2 : Vérification de la boucle RVAV

### Checklist RVAV

| Point | Vérification | Priorité |
|---|---|---|
| **[Rechercher]** | Les références sont-elles rassemblées ? | Haute |
| **[Vérifier]** | La checklist est-elle complète ? | Haute |
| **[Analyser]** | La relecture est-elle faite ? | Haute |
| **[Valider]** | La décision est-elle documentée ? | Haute |

### Preuves à exiger

| Preuve | Comment la vérifier |
|---|---|
| **Références** | Lister les liens et dépendances |
| **Checklist** | Vérifier chaque point coché |
| **Relecture** | Lire le contenu complet |
| **Décision** | Justification écrite |

---

## Étape 3 : Analyse de cohérence

### Exigences par statut

| Statut | Exigences minimales |
|---|---|
| **ebauche** | Structure minimale, idée brute |
| **préparé** | Structure complète, toutes les sections |
| **dev** | Contenu développé, sections écrites |
| **test** | RVAV effectué, liens vérifiés |
| **valide** | Approuvé, référence fiable |

---

## Étape 4 : Décision

### Options de décision

| Décision | Condition | Action |
|---|---|---|
| **Valider** | Tout est correct | Statut +1, class +1 |
| **Rejeter** | Erreur détectée | Boucle de rétroaction |
| **Reporter** | Informations manquantes | Demander compléments |

### Matrice de décision

```
Si tout est correct → Valider
Si erreur mineure → Rejeter (correction rapide)
Si erreur majeure → Rejeter (boucle complète)
Si informe manquante → Reporter
```

---

## Étape 5 : Documentation

### Format de documentation

```markdown
## Contrôle — [nom-fichier]

**Date** : [date]
**Agent** : Janus
**Fichier** : [chemin]

### Vérifications effectuées

| Point | Statut | Notes |
|---|---|---|
| [Rechercher] | ✓/✗ | [détails] |
| [Vérifier] | ✓/✗ | [détails] |
| [Analyser] | ✓/✗ | [détails] |
| [Valider] | ✓/✗ | [détails] |

### Décision

**Verdict** : [Validé / Rejeté / Reporté]
**Raison** : [justification]
**Action** : [prochaine étape]
```

---

## Outils de contrôle

### Outils essentiels

| Outil | Usage | Étape RVAV |
|---|---|---|
| `lister-statuts` | Lister les fichiers par statut | [Rechercher] |
| `valider-nommage` | Vérifier la conformité du nommage | [Vérifier] |
| `valider-liens` | Vérifier que les liens sont valides | [Vérifier] |
| `verifier-role-fichier` | Vérifier qu'un fichier est utilisé pour sa fonction | [Vérifier] |

### Utilisation de lister-statuts

```bash
# Lister tous les fichiers en ebauche
lister-statuts.sh --statut ebauche cerveau-projet/

# Lister les fichiers en test
lister-statuts.sh --statut test cerveau-projet/

# Vue d'ensemble verbose
lister-statuts.sh --verbose cerveau-projet/
```

### Quand utiliser ces outils

| Situation | Outil à utiliser |
|---|---|
| **Début de contrôle** | `lister-statuts` pour voir l'état des fichiers |
| **Vérification du nom** | `valider-nommage` pour chaque fichier |
| **Vérification des liens** | `valider-liens` pour chaque fichier |
| **Vérification du rôle** | `verifier-role-fichier` pour chaque fichier |

---

## Intégration avec le cycle

### Dans le cycle Cerberus → Agent → Cerberus

```
1. Buffy crée un fichier (ebauche)
2. Buffy fait la boucle RVAV
3. Buffy réactive Cerberus
4. Cerberus active Janus pour contrôle
5. Janus vérifie et décide
6. Janus réactive Cerberus
7. Cerberus informe Buffy du résultat
```

### Activation de Janus

| Contexte | Raison |
|---|---|
| **Après une boucle RVAV** | Valider la transition |
| **À la demande de Buffy** | Contrôle ponctuel |
| **Régulièrement** | Audit de qualité |

---

## Notes importantes

- **Janus est indépendant** — il ne dépend pas de Buffy
- **Le contrôle est obligatoire** — pas de passage de statut sans contrôle
- **La documentation est essentielle** — chaque décision doit être justifiée
- **Le cycle est sacré** — toujours revenir à Cerberus
- **Les outils sont obligatoires** — utiliser les outils pour chaque vérification

---

> **Ce protocole est IMMUABLE.**
