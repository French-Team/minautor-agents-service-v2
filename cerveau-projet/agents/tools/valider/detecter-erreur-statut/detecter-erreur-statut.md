# Outil — Détecter les Erreurs de Statut

**Catégorie** : Valider
**Version** : 0.1.0
**Statut** : beta
**Date création** : 2026-08-05
**Propriétaire** : Vulcain (outil partagé)

---

## Objectif

Détecter les fichiers dont le statut ne correspond pas à leur contenu.

**Pourquoi cet outil ?**
- Un fichier "ebauche" trop complet devrait être "préparé"
- Un fichier "préparé" trop simple devrait être "ebauche"
- Cet outil audit la cohérence des statuts dans le projet

---

## Utilisation

```bash
./detecter-erreur-statut.sh [dossier] [OPTIONS]
```

### Options

| Option | Description |
|---|---|
| `--statut <statut>` | Filtrer par statut (ebauche, préparé, dev, test, valide) |
| `--verbose` | Afficher les détails |
| `--aide` | Afficher l'aide |

### Exemples

```bash
# Vérifier tous les fichiers
./detecter-erreur-statut.sh

# Vérifier uniquement les fichiers ebauche
./detecter-erreur-statut.sh --statut ebauche

# Vérifier dans un dossier spécifique
./detecter-erreur-statut.sh cerveau-projet/
```

---

## Comment ça fonctionne

### 1. Évaluation de la maturité

L'outil évalue la **maturité** de chaque fichier (score de 0 à 15) :

| Critère | Points |
|---|---|
| **Nombre de lignes** | 0-3 points |
| **Frontmatter** | 0-1 point |
| **Nombre de sections** | 0-3 points |
| **Tableaux** | 0-1 point |
| **Code** | 0-1 point |
| **Listes** | 0-1 point |
| **Liens internes** | 0-2 points |

### 2. Statut recommandé

Selon la maturité, l'outil recommande un statut :

| Maturité | Statut recommandé |
|---|---|
| 0-2 | ebauche |
| 3-4 | préparé |
| 5-6 | dev |
| 7-9 | test |
| 10+ | valide |

### 3. Détection des erreurs

| Situation | Erreur |
|---|---|
| Statut actuel < Statut recommandé | **Sous-statut** : le fichier est trop avancé pour son statut |
| Statut actuel > Statut recommandé | **Sur-statut** : le fichier est trop simple pour son statut |

---

## Résultat

### Exemple de sortie

```
=== Détection des erreurs de statut ===
Dossier : cerveau-projet
Filtre : ebauche

❌ protocole-auto-correction.001.01.ebauche.md
   Statut actuel : ebauche
   Maturité : 8/15
   Statut recommandé : dev
   → Devrait être au statut 'dev'

❌ protocole-versionning-outils.001.01.ebauche.md
   Statut actuel : ebauche
   Maturité : 6/15
   Statut recommandé : dev
   → Devrait être au statut 'dev'

=== Résumé ===
Fichiers analysés : 15
Erreurs détectées : 2

❌ 2 erreur(s) de statut détectée(s)
```

---

## Types d'erreurs

### 1. Sous-statut (le plus fréquent)

**Exemple** : Un fichier "ebauche" qui contient :
- 50 lignes
- Un frontmatter
- 5 sections
- Des tableaux

**Problème** : Ce fichier est trop structuré pour être un ebauche.

**Solution** : Passer au statut "préparé" (ou supérieur).

### 2. Sur-statut (plus rare)

**Exemple** : Un fichier "valide" qui contient :
- 5 lignes
- Pas de structure

**Problème** : Ce fichier est trop simple pour être validé.

**Solution** : Revenir au statut "ebauche" ou "préparé".

---

## Relation avec le workflow RVAV

Cet outil est utilisé à l'étape **[Rechercher]** du workflow RVAV :

```
1. [Rechercher] → detecter-erreur-statut pour voir les incohérences
2. [Vérifier]   → valider-nommage pour chaque fichier
3. [Analyser]   → Lire le contenu des fichiers
4. [Valider]    → Décider du passage de statut
5. [Purifier]   → purifier-fichier ou condenseur
```

---

## Qui devrait utiliser cet tool ?

| Agent | Quand l'utiliser |
|---|---|
| **Janus** | Pour le contrôle des statuts — vérifier la cohérence |
| **Cerberus** | Pour un audit rapide du projet |
| **Tout agent** | Avant de commencer une mission — voir l'état du projet |

---

## Notes

- Cet outil ne modifie pas les fichiers, il les analyse uniquement
- L'évaluation de la maturité est basée sur des heuristiques simples
- Les résultats sont indicatifs, pas définitifs
- Utiliser `valider-ebauche` pour une validation plus détaillée d'un fichier

---

## Liens

- **Outil similaire** : `valider-ebauche` — validation détaillée d'un fichier ebauche
- **Workflow** : `rvav-workflow.md` — processus de validation
- **Protocole** : `protocole-controle-statuts.md` — contrôle des statuts par Janus
