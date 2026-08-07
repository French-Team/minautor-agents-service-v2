# Specification -- verifier-systeme

**Statut :** prepare
**ID :** 001
**Class :** 01
**Cree :** 2026-08-05
**Theme :** verifier-systeme
**Pense-bete source :** Spec directe (pas de pense-bete parent)

---

## 1. Objectif

Verifier le systeme de l'utilisateur (OS, shells, langages, outils) et produire un rapport structure (table, json ou resume) pour permettre aux agents de choisir les bonnes commandes sans supposer ce qui est installe.

---

## 2. Contexte

### 2.1 Origine

Les agents du cerveau-projet executaient des commandes en supposant ce qui est installe sur le systeme (bash, python, git, etc.), ce qui violait les protocoles (ne pas supposer). Un outil de verification systeme est necessaire pour collecter l'etat reel de la machine avant toute decision.

### 2.2 Perimetre

**Couvert** : detection de l'OS, verification des shells, des langages de programmation et des outils disponibles, formats de sortie multiples.

**Hors perimetre** : installation de logiciels, configuration du systeme, benchmark de performance.

### 2.3 Public cible

Tous les agents du cerveau-projet, en particulier Vulcain (constructeur d'outils) avant d'utiliser une technologie.

---

## 3. Exigences Fonctionnelles

### 3.1 Exigence 01 -- Detecter le systeme

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Retourne l'OS, la version et l'architecture de la machine |
| **Critere d'acceptation** | Objet contenant os, version, arch |
| **Dependances** | Module `platform` disponible |

### 3.2 Exigence 02 -- Verifier les shells

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Liste les shells disponibles (bash, powershell, etc.) avec leur version |
| **Critere d'acceptation** | Chaque shell installe est detecte avec sa version |
| **Dependances** | Commandes systeme `which`/`where` |

### 3.3 Exigence 03 -- Verifier les langages

| Champ | Description |
|---|---|
| **Priorite** | Moyenne |
| **Description** | Liste les langages de programmation installes (python, node, etc.) avec leur version |
| **Critere d'acceptation** | Chaque langage installe est detecte avec sa version |
| **Dependances** | Commandes de version des langages |

### 3.4 Exigence 04 -- Produire un rapport formate

| Champ | Description |
|---|---|
| **Priorite** | Moyenne |
| **Description** | Produit le rapport en table, JSON ou resume selon le parametre format |
| **Critere d'acceptation** | Le format JSON est parseable, le resume est lisible |
| **Dependances** | Exigences 01 a 03 |

---

## 4. Exigences Non-Fonctionnelles

| Categorie | Exigence | Critere de mesure |
|---|---|---|
| **Performance** | Execution en moins de 5 secondes | Chronometrage |
| **Fiabilite** | Outil absent gere sans erreur | Absence signalee, pas de crash |
| **Portabilite** | Compatible Windows, Linux, Mac | Commandes `which`/`where` selon l'OS |
| **Maintenabilite** | Script lisible et commente | Revue par l'agent proprietaire |
| **Non-intrusif** | Aucune installation effectuee | Verification en lecture seule |

---

## 5. Architecture / Structure Technique

### 5.1 Vue d'ensemble

Le script detecte le systeme via le module `platform`, verifie la presence des shells, langages et outils via les commandes systeme, puis assemble un rapport formate selon le parametre demande.

### 5.2 Composants

| Composant | Role | Dependances |
|---|---|---|
| Detecteur OS | Collecter os, version, arch | Module `platform` |
| Verificateur shells | Tester bash, powershell, etc. | `which` / `where` |
| Verificateur langages | Tester python, node, etc. | Commandes de version |
| Verificateur outils | Tester git, npm, etc. | Commandes de version |
| Formateur | Produire table, JSON ou resume | Composants precedents |

### 5.3 Modele de donnees

```json
{
  "systeme": { "os": "...", "version": "...", "arch": "..." },
  "shells": ["bash 5.x"],
  "langages": ["python 3.x"],
  "outils": ["git 2.x"]
}
```

### 5.4 Interfaces / API

```bash
verifier-systeme.sh [--format table|json|resume] [--detail standard|complet]
```

### 5.5 Flux / Workflows

```
1. Detecter l'OS (platform)
2. Verifier les shells (bash, powershell)
3. Verifier les langages (python, node)
4. Verifier les outils (git, npm)
5. Assembler le rapport
6. Formater selon --format
7. Retourner le resultat
```

---

## 6. Contraintes et Risques

### 6.1 Contraintes

| Contrainte | Impact | Mitigation |
|---|---|---|
| Commandes differentes selon l'OS | Detection incomplete | Branchement `which` (Unix) / `where` (Windows) |

### 6.2 Risques

| Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|
| Commande de version lente | Faible | Moyen | Timeout sur chaque commande |
| Outil present mais sans version | Faible | Faible | Presence = detection simple |

---

## 7. Livrables attendus

| Livrable | Format | Destination |
|---|---|---|
| Script | Bash | `agents/tools/verifier/verifier-systeme/verifier-systeme.sh` |
| Documentation | Markdown | `agents/tools/verifier/verifier-systeme/verifier-systeme.md` |
| Specification | Markdown | `agents/tools/verifier/verifier-systeme/spec/` |

---

## 8. Plan de validation

### 8.1 Criteres de succes globaux

- [ ] La detection du systeme fonctionne sur la machine courante
- [ ] Les shells, langages et outils sont detectes correctement
- [ ] Le format JSON est valide

### 8.2 Methode de validation

Execution reelle sur le systeme de l'utilisateur + fichiers de test dans `exemples/`.

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

- Aucune

### 9.3 Conventions applicables

- `convention-renommage.md`

### 9.4 Regles immuables

- `regles-emojis-ascii.md`

### 9.5 References externes

- Documentation Python `platform`

---

## 10. RVAV de la spec

- [rechercher] -- references rassemblees (platform, commandes systeme, conventions)
- [verifier] -- structure complete (sections 1-10 presentes)
- [analyser] -- coherent avec l'outil existant (v0.2.0)
- [valider] -- pret pour le statut prepare

---

## Historique des modifications

| Date | Version | Auteur | Description |
|---|---|---|---|
| 2026-08-05 | 0.1.0 | Vulcain | Creation initiale |
| 2026-08-07 | 0.2.0 | Promethee | Refonte selon spec-template, version outil 0.2.0 |
