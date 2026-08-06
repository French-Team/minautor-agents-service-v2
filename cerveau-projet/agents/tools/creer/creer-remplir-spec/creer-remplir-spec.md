# creer-remplir-spec

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Creer
**Chemin :** `agents/tools/creer/creer-remplir-spec/`
**Proprietaire :** outil partage

## Description

Remplit les sections d'une spec **sans ouvrir le fichier**. L'agent donne la section et le contenu en arguments, l'outil insere le contenu a la bonne place. Complement de `generateurs-squelette-spec` (qui genere la structure) : cet outil cree le contenu.

## Utilisation

```bash
# Remplir le titre
creer-remplir-spec.sh spec-pipeline.001.01.ebauche.md titre "Spec du pipeline"

# Remplir le lien du pense-bete source
creer-remplir-spec.sh spec-pipeline.001.01.ebauche.md parent "pense-bete-pipeline.001.01.ebauche.md"

# Remplir l'objectif
creer-remplir-spec.sh spec-pipeline.001.01.ebauche.md objectif "Definir comment les pipelines fonctionnent"

# Remplir le contexte (multiligne avec \n)
creer-remplir-spec.sh spec-pipeline.001.01.ebauche.md contexte "Origine : le besoin de decouplage\nPerimetre : les pipelines de traitement"

# Remplir les exigences
creer-remplir-spec.sh spec-pipeline.001.01.ebauche.md exigences "Exigence 1 : communication via classeur"

# Apercu sans modifier
creer-remplir-spec.sh spec-pipeline.001.01.ebauche.md objectif "Mon objectif" --dry-run
```

## Arguments

| Argument | Description |
|---|---|
| `fichier` | Chemin de la spec a remplir |
| `section` | Section a remplir (voir liste) |
| `contenu` | Contenu a inserer (entre guillemets) |

## Sections disponibles

| Section | Cible | Marqueur |
|---|---|---|
| `titre` | Titre de la spec | `# Spec` |
| `parent` | Lien pense-bete source (header) | `**Pense-bete source :**` |
| `objectif` | Section 1. Objectif | `## 1. Objectif` |
| `contexte` | Section 2. Contexte | `## 2. Contexte` |
| `exigences` | Section 3. Exigences Fonctionnelles | `## 3. Exigences Fonctionnelles` |
| `architecture` | Section 5. Architecture | `## 5. Architecture / Structure Technique` |
| `risques` | Section 6. Contraintes et Risques | `## 6. Contraintes et Risques` |
| `livrables` | Section 7. Livrables attendus | `## 7. Livrables attendus` |
| `validation` | Section 8. Plan de validation | `## 8. Plan de validation` |
| `liens` | Section 9. Liens et References | `## 9. Liens et References` |
| `rvav` | Section 10. RVAV | `## 10. RVAV de la spec` |

## Ce que l'outil fait

1. **Valide** - La section est connue, le fichier existe
2. **Localise** - Trouve le marqueur de la section dans le fichier
3. **Detecte** - La prochaine section (pour delimiter le remplacement)
4. **Remplace** - Insere le contenu entre la section et la suivante
5. **Protege** - Ne modifie que la section visee, le reste est intact

## Exemples de sortie

```bash
$ creer-remplir-spec.sh spec-pipeline.001.01.ebauche.md objectif "Definir les pipelines"
[OK] Section 'objectif' remplie dans spec-pipeline.001.01.ebauche.md
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Passage spec -> contenu** | Remplir les sections apres generation du squelette |
| **Remplir une section** | Sans ouvrir le fichier, en une commande |
| **Correction d'une section** | Re-remplir une section avec le nouveau contenu |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `generateurs-squelette-spec` | Genere le squelette avant de remplir |
| `remplir-pense-bete` | Meme logique pour les pense-betes |
| `remplir-todo` | Meme logique pour les todos |
| `valider-pense-bete` | Modele pour creer un validateur de spec |
