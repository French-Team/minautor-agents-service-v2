# detecter-erreur-statut

**Categorie** : Detecter
**Version** : 0.2.0
**Statut** : prepare
**Date creation** : 2026-08-05
**Proprietaire** : Vulcain (outil partage)

---

## Objectif

Detecter les fichiers dont le statut ne correspond pas a leur contenu.

**Pourquoi cet outil ?**
- Un fichier "ebauche" trop complet devrait etre "prepare"
- Un fichier "prepare" trop simple devrait etre "ebauche"
- Cet outil audit la coherence des statuts dans le projet

---

## Utilisation

```bash
./detecter-erreur-statut.sh [dossier] [OPTIONS]
# Version Python (recommandee)
python3 detecter-erreur-statut.py [dossier] [OPTIONS]
```

### Options

| Option | Description |
|---|---|
| `--statut <statut>` | Filtrer par statut (ebauche, prepare, dev, test, valide) |
| `--verbose` | Afficher les details |
| `--aide` | Afficher l'aide |

### Exemples

```bash
# Verifier tous les fichiers
./detecter-erreur-statut.sh

# Verifier uniquement les fichiers ebauche
./detecter-erreur-statut.sh --statut ebauche

# Verifier dans un dossier specifique
./detecter-erreur-statut.sh cerveau-projet/
```

---

## Comment ca fonctionne

### 1. Evaluation de la maturite

L'outil evalue la **maturite** de chaque fichier (score de 0 a 15) :

| Critere | Points |
|---|---|
| **Nombre de lignes** | 0-3 points |
| **Frontmatter** | 0-1 point |
| **Nombre de sections** | 0-3 points |
| **Tableaux** | 0-1 point |
| **Code** | 0-1 point |
| **Listes** | 0-1 point |
| **Liens internes** | 0-2 points |

### 2. Statut recommande

Selon la maturite, l'outil recommande un statut :

| Maturite | Statut recommande |
|---|---|
| 0-2 | ebauche |
| 3-4 | prepare |
| 5-6 | dev |
| 7-9 | test |
| 10+ | valide |

### 3. Detection des erreurs

| Situation | Erreur |
|---|---|
| Statut actuel < Statut recommande | **Sous-statut** : le fichier est trop avance pour son statut |
| Statut actuel > Statut recommande | **Sur-statut** : le fichier est trop simple pour son statut |

---

## Resultat

### Exemple de sortie

```
=== Detection des erreurs de statut ===
Dossier : cerveau-projet
Filtre : ebauche

[ERREUR] protocole-auto-correction.001.01.ebauche.md
   Statut actuel : ebauche
   Maturite : 8/15
   Statut recommande : dev
   -> Devrait etre au statut 'dev'

[ERREUR] protocole-versionning-outils.001.01.ebauche.md
   Statut actuel : ebauche
   Maturite : 6/15
   Statut recommande : dev
   -> Devrait etre au statut 'dev'

=== Resume ===
Fichiers analyses : 15
Erreurs detectees : 2

[ERREUR] 2 erreur(s) de statut detectee(s)
```

---

## Types d'erreurs

### 1. Sous-statut (le plus frequent)

**Exemple** : Un fichier "ebauche" qui contient :
- 50 lignes
- Un frontmatter
- 5 sections
- Des tableaux

**Probleme** : Ce fichier est trop structure pour etre un ebauche.

**Solution** : Passer au statut "prepare" (ou superieur).

### 2. Sur-statut (plus rare)

**Exemple** : Un fichier "valide" qui contient :
- 5 lignes
- Pas de structure

**Probleme** : Ce fichier est trop simple pour etre valide.

**Solution** : Revenir au statut "ebauche" ou "prepare".

---

## Relation avec le workflow RVAV

Cet outil est utilise a l'etape **[Rechercher]** du workflow RVAV :

```
1. [Rechercher] -> detecter-erreur-statut pour voir les incoherences
2. [Verifier]   -> valider-nommage pour chaque fichier
3. [Analyser]   -> Lire le contenu des fichiers
4. [Valider]    -> Decider du passage de statut
5. [Purifier]   -> nettoyer-fichier ou condenser-fichier
```

---

## Qui devrait utiliser cet tool ?

| Agent | Quand l'utiliser |
|---|---|
| **Janus** | Pour le controle des statuts -- verifier la coherence |
| **Cerberus** | Pour un audit rapide du projet |
| **Tout agent** | Avant de commencer une mission -- voir l'etat du projet |

---

## Notes

- Cet outil ne modifie pas les fichiers, il les analyse uniquement
- L'evaluation de la maturite est basee sur des heuristiques simples
- Les resultats sont indicatifs, pas definitifs
- Utiliser `valider-ebauche` pour une validation plus detaillee d'un fichier

---

## Liens

- **Outil similaire** : `valider-ebauche` -- validation detaillee d'un fichier ebauche
- **Workflow** : `rvav-workflow.md` -- processus de validation
- **Protocole** : `protocole-controle-statuts.md` -- controle des statuts par Janus

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels, corrections, promotion |
| 0.2.0-py | 2026-08-07 | Version Python creee (memes fonctionnalites + --version) |
