---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Protocole -- Controle des Statuts

**Version** : 0.1.0
**Statut** : Ebauche
**Date creation** : 2026-08-05
**Agent** : Janus (controleur)

---

## Objectif

Definir comment Janus controle les transitions de statut des fichiers du cerveau-projet.

**Pourquoi ce protocole ?**
- Le workflow RVAV existe mais personne ne le verifie
- Les agents peuvent tricher ou oublier les boucles RVAV
- La qualite exige un controle independant
- Janus est l'agent specialise dans le second controle

---

## Le role de Janus

### Responsabilites

| Responsabilite | Description |
|---|---|
| **Controler les transitions** | Verifier que les changements de statut sont legitimes |
| **Valider les boucles RVAV** | S'assurer que chaque boucle est complete |
| **Detecter les erreurs** | Identifier les fichiers qui ne respectent pas le workflow |
| **Documenter les decisions** | Justifier chaque validation ou rejet |

### Limites

| Limite | Raison |
|---|---|
| **Ne cree pas de fichiers** | Janus ne cree que du controle |
| **Ne modifie pas le contenu** | Il valide, pas il ne corrige |
| **Ne saute pas Cerberus** | Toujours revenir au coordinateur |

---

## Le processus de controle

```
FICHIER -> VERIFICATION -> ANALYSE -> DECISION -> DOCUMENTATION
    1          2            3          4           5
```

| Etape | Action | Responsable |
|---|---|---|
| 1 | Lire le fichier et son statut | Janus |
| 2 | Verifier la boucle RVAV | Janus |
| 3 | Analyser la coherence | Janus |
| 4 | Decider : valider ou rejeter | Janus |
| 5 | Documenter la decision | Janus |

---

## Etape 2 : Verification de la boucle RVAV

### Checklist RVAV

| Point | Verification | Priorite |
|---|---|---|
| **[Rechercher]** | Les references sont-elles rassemblees ? | Haute |
| **[Verifier]** | La checklist est-elle complete ? | Haute |
| **[Analyser]** | La relecture est-elle faite ? | Haute |
| **[Valider]** | La decision est-elle documentee ? | Haute |

### Preuves a exiger

| Preuve | Comment la verifier |
|---|---|
| **References** | Lister les liens et dependances |
| **Checklist** | Verifier chaque point coche |
| **Relecture** | Lire le contenu complet |
| **Regle de relecture des agents** | `valider-relecture` -- chaque agent porte la regle dans sa fiche et ses corrections |
| **Decision** | Justification ecrite |

---

## Etape 3 : Analyse de coherence

### Exigences par statut

Les statuts reels du projet sont : `ebauche`, `prepare`, `stable`.

| Statut | Exigences minimales |
|---|---|
| **ebauche** | Structure minimale, idee brute (premier statut) |
| **prepare** | Structure complete, toutes les sections remplies |
| **stable** | Approuve, reference fiable (exceptions : les dictionnaires fonctionnels) |

---

## Etape 4 : Decision

### Options de decision

| Decision | Condition | Action |
|---|---|---|
| **Valider** | Tout est correct | Statut +1, class +1 |
| **Rejeter** | Erreur detectee | Boucle de retroaction |
| **Reporter** | Informations manquantes | Demander complements |

### Matrice de decision

```
Si tout est correct -> Valider
Si erreur mineure -> Rejeter (correction rapide)
Si erreur majeure -> Rejeter (boucle complete)
Si informe manquante -> Reporter
```

---

## Etape 5 : Documentation

### Format de documentation

```markdown
## Controle -- [nom-fichier]

**Date** : [date]
**Agent** : Janus
**Fichier** : [chemin]

### Verifications effectuees

| Point | Statut | Notes |
|---|---|---|
| [Rechercher] | [OK]/[ERREUR] | [details] |
| [Verifier] | [OK]/[ERREUR] | [details] |
| [Analyser] | [OK]/[ERREUR] | [details] |
| [Valider] | [OK]/[ERREUR] | [details] |

### Decision

**Verdict** : [Valide / Rejete / Reporte]
**Raison** : [justification]
**Action** : [prochaine etape]
```

---

## Outils de controle

### Outils essentiels

| Outil | Usage | Etape RVAV |
|---|---|---|
| `lister-statuts` | Lister les fichiers par statut | [Rechercher] |
| `lister-prepares` | Lister les fichiers 'prepare' et verifier leurs specs | [Rechercher] |
| `detecter-erreur-statut` | Detecter les fichiers dont le statut ne correspond pas au contenu | [Verifier] |
| `valider-nommage` | Verifier la conformite du nommage | [Verifier] |
| `valider-liens` | Verifier que les liens sont valides | [Verifier] |
| `valider-relecture` | **SYSTEMATIQUE** : verifier que chaque fiche agent + corrections contient la regle de relecture | [Verifier] |
| `verifier-role-fichier` | Verifier qu'un fichier est utilise pour sa fonction | [Verifier] |
| `changer-statut` | Changer le statut d'un fichier en le renommant | [Valider] |

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

| Situation | Outil a utiliser |
|---|---|
| **Debut de controle** | `lister-statuts` pour voir l'etat des fichiers |
| **Verification du nom** | `valider-nommage` pour chaque fichier |
| **Verification des liens** | `valider-liens` pour chaque fichier |
| **Verification de la regle de relecture** | `valider-relecture` pour TOUS les agents (obligatoire a chaque controle) |
| **Verification du role** | `verifier-role-fichier` pour chaque fichier |

---

## Integration avec le cycle

### Dans le cycle Cerberus -> Agent -> Cerberus

```
1. Buffy cree un fichier (ebauche)
2. Buffy fait la boucle RVAV
3. Buffy reactive Cerberus
4. Cerberus active Janus pour controle
5. Janus verifie et decide
6. Janus reactive Cerberus
7. Cerberus informe Buffy du resultat
```

### Activation de Janus

| Contexte | Raison |
|---|---|
| **Apres une boucle RVAV** | Valider la transition |
| **A la demande de Buffy** | Controle ponctuel |
| **Regulierement** | Audit de qualite |

---

## Notes importantes

- **Janus est independant** -- il ne depend pas de Buffy
- **Le controle est obligatoire** -- pas de passage de statut sans controle
- **La documentation est essentielle** -- chaque decision doit etre justifiee
- **Le cycle est sacre** -- la fin de mission suit SA carte : reactiver Cerberus (activation directe ou dernier maillon) ou activer le suivant selon la carte
- **Les outils sont obligatoires** -- utiliser les outils pour chaque verification
- **`valider-relecture` est SYSTEMATIQUE** -- a chaque controle, verifier que tous les agents portent la regle de relecture (garde-fou du cycle d'activation)

---

> **Ce protocole est IMMUABLE.**
