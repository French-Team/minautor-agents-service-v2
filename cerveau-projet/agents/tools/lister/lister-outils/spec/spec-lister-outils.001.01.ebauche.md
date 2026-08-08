---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Specification -- lister-outils

**Statut :** prepare
**ID :** 001
**Class :** 01
**Cree :** 2026-08-05
**Theme :** lister-outils
**Pense-bete source :** Spec directe (pas de pense-bete parent)

---

## 1. Objectif

Fournir une interface standardisee pour interroger la boite a outils partagee du cerveau-projet et produire une liste lisible (table, liste ou JSON) des outils par categorie.

---

## 2. Contexte

### 2.1 Origine

Le cerveau-projet possede une boite a outils dans `tools/`, inventoriee dans `index-tools.md`. Un agent a besoin de connaitre les outils disponibles, leur description et leur categorie pour choisir le bon outil dans sa mission.

### 2.2 Perimetre

**Couvert** : lecture de `index-tools.md`, extraction des outils, filtrage par categorie, formatage table/liste/JSON.

**Hors perimetre** : creation d'outils, modification d'outils, gestion des versions.

### 2.3 Public cible

Tous les agents du cerveau-projet, en particulier Vulcain (constructeur) et Buffy (responsable du cerveau).

---

## 3. Exigences Fonctionnelles

### 3.1 Exigence 01 -- Lister tous les outils

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Retourne la liste complete des outils avec nom, description et categorie |
| **Critere d'acceptation** | La liste contient tous les outils presents dans `index-tools.md` |
| **Dependances** | Fichier `index-tools.md` lisible |

### 3.2 Exigence 02 -- Filtrer par categorie

| Champ | Description |
|---|---|
| **Priorite** | Moyenne |
| **Description** | Retourne uniquement les outils de la categorie demandee (explorer, valider, corriger, etc.) |
| **Critere d'acceptation** | Seuls les outils de la categorie demandee sont retournes |
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

Le script lit le fichier `index-tools.md`, repere les sections par categorie, extrait les lignes de chaque tableau, applique le filtre optionnel, puis formate le resultat.

### 5.2 Composants

| Composant | Role | Dependances |
|---|---|---|
| Lecteur | Lire `index-tools.md` | Fichier source |
| Extracteur | Parser les tableaux par categorie | Lecteur |
| Filtre | Appliquer le filtre par categorie | Extracteur |
| Formateur | Produire table, liste ou JSON | Filtre |

### 5.3 Modele de donnees

```markdown
| Outil | Description | Chemin |
|---|---|---|
| `lister-dossiers` | Lister les dossiers | [lister/lister-dossiers/](lister/lister-dossiers/) |
```

### 5.4 Interfaces / API

```bash
lister-outils.sh [--format table|liste|json] [--categorie NOM]
```

### 5.5 Flux / Workflows

```
1. Lire index-tools.md
2. Trouver les sections par categorie
3. Extraire les lignes de chaque tableau
4. Pour chaque ligne : nom, description, categorie
5. Appliquer le filtre si present
6. Formater selon --format
7. Retourner le resultat
```

---

## 6. Contraintes et Risques

### 6.1 Contraintes

| Contrainte | Impact | Mitigation |
|---|---|---|
| Noms de categories varies | Regroupement incertain | Normaliser les noms de sections a la lecture |

### 6.2 Risques

| Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|
| Outil ajoute sans index | Moyen | Moyen | Signalement des entrees orphelines |
| Accents dans les noms | Faible | Faible | Normalisation ASCII a la lecture |

---

## 7. Livrables attendus

| Livrable | Format | Destination |
|---|---|---|
| Script | Bash | `agents/tools/lister/lister-outils/lister-outils.sh` |
| Documentation | Markdown | `agents/tools/lister/lister-outils/lister-outils.md` |
| Specification | Markdown | `agents/tools/lister/lister-outils/spec/` |

---

## 8. Plan de validation

### 8.1 Criteres de succes globaux

- [ ] La liste complete contient tous les outils
- [ ] Le filtre par categorie fonctionne
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

- `spec-lister-agents.001.01`

### 9.3 Conventions applicables

- `convention-renommage.md`

### 9.4 Regles immuables

- `regles-emojis-ascii.md`

### 9.5 References externes

- Aucune

---

## 10. RVAV de la spec

- [rechercher] -- references rassemblees (index-tools, conventions)
- [verifier] -- structure complete (sections 1-10 presentes)
- [analyser] -- coherent avec l'outil existant (v0.2.0)
- [valider] -- pret pour le statut prepare

---

## Historique des modifications

| Date | Version | Auteur | Description |
|---|---|---|---|
| 2026-08-05 | 0.1.0 | Vulcain | Creation initiale |
| 2026-08-07 | 0.2.0 | Promethee | Refonte selon spec-template, version outil 0.2.0 |
