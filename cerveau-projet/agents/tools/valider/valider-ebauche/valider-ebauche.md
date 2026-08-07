# valider-ebauche

**Version :** 0.2.0-py
**Statut :** prepare
**Categorie :** valider
**Chemin :** `agents/tools/valider/valider-ebauche/`
**Proprietaire :** Vulcain (outil partage)

---

## Objectif

Verifier si un fichier ebauche respecte les **exigences minimales** d'un ebauche.

**Pourquoi cet outil ?**
- Un ebauche est une idee brute, pas un document structure
- Cet outil verifie que le fichier est bien un ebauche (et pas un prepare deguise)
- Il aide a maintenir la coherence des statuts

---

## Utilisation

```bash
./valider-ebauche.sh <fichier> [OPTIONS]
```

### Options

| Option | Description |
|---|---|
| `--verbose` | Afficher les details |
| `--aide` | Afficher l'aide |

---

## Ce que verifie l'outil

### Exigences minimales (obligatoires)

| Verification | Critere |
|---|---|
| **Statut** | Le fichier est bien un ebauche |
| **Titre** | Presence d'un titre principal (h1) |
| **Contenu** | Au moins 5 lignes |

### Verifications de coherence (avertissements)

| Verification | Critere |
|---|---|
| **Nommage** | Le nom respecte la convention |
| **Frontmatter** | Pas de frontmatter (inutile pour un ebauche) |
| **Tableaux** | Pas de tableaux (peut-etre trop structure) |
| **Sections** | Pas plus de 3 sections (peut-etre trop structure) |

---

## Resultat

### Exemple de sortie (succes)

```
=== Validation du fichier ebauche ===
Fichier : protocole-xxx.001.01.ebauche.md

--- Verification du nommage ---
--- Verification de la structure minimale ---
--- Verification du contenu minimal ---
--- Verification : pas trop complet pour un ebauche ---

=== Resume ===
Erreurs : 0
Avertissements : 1

[OK] Le fichier ebauche respecte les exigences minimales
[ATTENTION]  Cependant, il semble trop structure pour un ebauche
    Considerez passer au statut 'prepare'
```

### Exemple de sortie (echec)

```
=== Validation du fichier ebauche ===
Fichier : protocole-xxx.001.01.ebauche.md

--- Verification de la structure minimale ---
[ERREUR] Pas de titre principal (h1)

=== Resume ===
Erreurs : 1
Avertissements : 0

[ERREUR] Le fichier ebauche ne respecte pas les exigences minimales
```

---

## Logique de l'outil

| Statut | Ce que l'outil verifie |
|---|---|
| **ebauche** | Le fichier respecte les exigences **minimales** d'un ebauche |
| **ebauche** | Le fichier **n'est PAS encore** un prepare (sinon -> avertissement) |

---

## Relation avec d'autres outils

| Outil | Usage |
|---|---|
| `valider-ebauche` | Verifier les exigences minimales d'un ebauche |
| `detecter-erreur-statut` | Detecter les fichiers dont le statut ne correspond pas au contenu |
| `valider-nommage` | Verifier la conformite du nommage |

---

## Notes

- Un ebauche est une **idee brute**, pas un document structure
- Si un ebauche est "pret", c'est une **erreur de statut** (devrait etre "prepare")
- Utiliser `detecter-erreur-statut` pour verifier tous les fichiers d'un coup

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
