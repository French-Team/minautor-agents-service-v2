# Specification -- lister-agents

**Statut :** prepare
**ID :** 001
**Class :** 01
**Cree :** 2026-08-05
**Theme :** lister-agents
**Pense-bete source :** Spec directe (pas de pense-bete parent)

---

## 1. Objectif

Fournir une interface standardisee pour interroger la base d'agents du cerveau-projet et produire une liste lisible (table, liste ou JSON) des agents avec leur role et leur statut.

---

## 2. Contexte

### 2.1 Origine

Le cerveau-projet gere plusieurs agents (Cerberus, Buffy, Atlas, Janus, etc.) decrits dans `index-agents.md`. Un agent a besoin de connaitre la liste des agents disponibles, leur role et leur statut pour prendre des decisions (qui activer, qui consulter). Sans outil dedie, chaque agent devait lire et parser manuellement le fichier, avec des risques d'erreur.

### 2.2 Perimetre

**Couvert** : lecture de `index-agents.md`, extraction des agents, filtrage par statut, formatage table/liste/JSON.

**Hors perimetre** : modification des agents, creation de fiches, gestion des corrections.

### 2.3 Public cible

Tous les agents du cerveau-projet (Cerberus, Buffy, Atlas, Janus, et les agents dedies).

---

## 3. Exigences Fonctionnelles

### 3.1 Exigence 01 -- Lister tous les agents

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Retourne la liste complete des agents avec nom, role et statut |
| **Critere d'acceptation** | La liste contient tous les agents presents dans `index-agents.md` |
| **Dependances** | Fichier `index-agents.md` lisible |

### 3.2 Exigence 02 -- Filtrer par statut

| Champ | Description |
|---|---|
| **Priorite** | Moyenne |
| **Description** | Retourne uniquement les agents correspondant au statut demande (disponible, principal, en attente) |
| **Critere d'acceptation** | Seuls les agents du statut demande sont retournes |
| **Dependances** | Exigence 01 |

### 3.3 Exigence 03 -- Formater en JSON

| Champ | Description |
|---|---|
| **Priorite** | Moyenne |
| **Description** | Produit un tableau JSON valide au lieu d'une table markdown |
| **Critere d'acceptation** | La sortie est parseable par un decodeur JSON |
| **Dependances** | Exigence 01 |

---

## 4. Exigences Non-Fonctionnelles

| Categorie | Exigence | Critere de mesure |
|---|---|---|
| **Performance** | Reponse en moins de 2 secondes | Chronometrage sur un fichier standard |
| **Fiabilite** | Fichier source introuvable gere | Message d'erreur clair, code de retour non-zero |
| **Maintenabilite** | Script lisible et commente | Revue par l'agent proprietaire |
| **Portabilite** | Compatible Git Bash Windows, Linux, Mac | Aucune commande specifique a un OS |

---

## 5. Architecture / Structure Technique

### 5.1 Vue d'ensemble

Le script lit le fichier `index-agents.md`, extrait les lignes du tableau des agents, applique le filtre optionnel, puis formate le resultat selon le parametre demande.

### 5.2 Composants

| Composant | Role | Dependances |
|---|---|---|
| Lecteur | Lire `index-agents.md` | Fichier source |
| Extracteur | Parser les lignes du tableau | Lecteur |
| Filtre | Appliquer le filtre par statut | Extracteur |
| Formateur | Produire table, liste ou JSON | Filtre |

### 5.3 Modele de donnees

```markdown
| Agent | Fiche | Corrections | Role | Statut |
|---|---|---|---|---|
| [Cerberus](cerberus/cerberus.md) | ... | ... | Gardien de l'entree | Disponible (principal) |
```

### 5.4 Interfaces / API

```bash
lister-agents.sh [--format table|liste|json] [--filtre statut:VALEUR]
```

### 5.5 Flux / Workflows

```
1. Lire index-agents.md
2. Trouver la section "Agents existants"
3. Extraire les lignes du tableau
4. Pour chaque ligne : nom, role, statut
5. Appliquer le filtre si present
6. Formater selon --format
7. Retourner le resultat
```

---

## 6. Contraintes et Risques

### 6.1 Contraintes

| Contrainte | Impact | Mitigation |
|---|---|---|
| Format variable du tableau source | Extraction fragile | Parser tolerant aux colonnes vides |

### 6.2 Risques

| Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|
| Fichier source renomme | Faible | Moyen | Chemin configure en constante |
| Accents dans les noms | Faible | Faible | Normalisation ASCII a la lecture |

---

## 7. Livrables attendus

| Livrable | Format | Destination |
|---|---|---|
| Script | Bash | `agents/tools/lister/lister-agents/lister-agents.sh` |
| Documentation | Markdown | `agents/tools/lister/lister-agents/lister-agents.md` |
| Specification | Markdown | `agents/tools/lister/lister-agents/spec/` |

---

## 8. Plan de validation

### 8.1 Criteres de succes globaux

- [ ] La liste complete contient tous les agents
- [ ] Le filtre par statut fonctionne
- [ ] Le format JSON est valide

### 8.2 Methode de validation

Tests manuels sur le dossier `exemples/` avec des fichiers de test.

### 8.3 Responsables

| Role | Responsable |
|---|---|
| Redaction | Promethee |
| Validation technique | Buffy |

---

## 9. Liens et References

### 9.1 Pense-bete source

- Spec directe (pas de pense-bete parent)

### 9.2 Specs connexes

- `spec-lister-outils.001.01`

### 9.3 Conventions applicables

- `convention-renommage.md`

### 9.4 Regles immuables

- `regles-emojis-ascii.md`

### 9.5 References externes

- Aucune

---

## 10. RVAV de la spec

- [rechercher] -- references rassemblees (index-agents, conventions)
- [verifier] -- structure complete (sections 1-10 presentes)
- [analyser] -- coherent avec l'outil existant (v0.2.0)
- [valider] -- pret pour le statut prepare

---

## Historique des modifications

| Date | Version | Auteur | Description |
|---|---|---|---|
| 2026-08-05 | 0.1.0 | Vulcain | Creation initiale |
| 2026-08-07 | 0.2.0 | Promethee | Refonte selon spec-template, version outil 0.2.0 |
