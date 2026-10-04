---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Specification -- lister-flags

**Statut :** prepare
**Version :** 0.1.1
**ID :** 001
**Class :** 01
**Cree :** 2026-09-03
**Theme :** lister-flags
**Proprietaire :** Vulcain

## 1. Objectif

Fournir un inventaire fiable des flags et arguments des outils et combos du
cerveau-projet afin que les agents puissent preparer une invocation ou
comparer plusieurs interfaces.

## 2. Perimetre

**Couvert** : lecture du catalogue des commandes, lecture des definitions de
combos, extraction AST des appels `argparse`, fusion des declarations,
selection par nom ou categorie, filtre par flag partage et sortie table/JSON.

**Hors perimetre** : execution des scripts trouves, modification des sources,
validation semantique de chaque commande ou execution du moteur de combo.

## 3. Exigences fonctionnelles

### 3.1 Inventaire des outils

Le script doit lire `catalogue-commandes.json` et produire les parametres
avec nom, type, statut obligatoire, description et source catalogue.

### 3.2 Inventaire des combos

Le script doit parcourir les `definition-combo.json`, identifier chaque
combo et inclure les parametres des commandes catalogue et les flags presents
dans les commandes de ses cases.

### 3.3 Complement argparse

Pour chaque script Python reference dans le catalogue, le script doit lire
les appels `add_argument` avec `ast` sans executer le fichier.

### 3.4 Filtres

Le script doit accepter plusieurs cibles, `--outil`, `--combo`, `--tous`,
`--categorie`, `--source` et `--flag-partage`.

### 3.5 Formats

Le format table doit etre lisible par un agent. Le format JSON doit etre
parseable et contenir `version`, `flags_partages` et `entites`.

## 4. Exigences non fonctionnelles

| Categorie | Exigence | Critere |
|---|---|---|
| Portabilite | Git Bash Windows et Linux | bibliotheque standard uniquement |
| Securite | Lecture seule | aucun script decouvert execute |
| Robustesse | Sources manquantes ou invalides | erreur claire et code non-zero |
| Performance | Inventaire local | execution interactive courte |
| Encodage | Compatibilite outils | code et JSON ASCII |

## 5. Modele de donnees

```json
{
  "nom": "--verbose",
  "flag": "--verbose",
  "type": "flag",
  "obligatoire": false,
  "description": "Afficher les details",
  "source": "catalogue, argparse",
  "positionnel": false
}
```

Une entite contient `nom`, `categorie`, `description`, `source`, `chemin` et
`flags`. Les flags sont dedoubles par nom normalise.

## 6. Interface

```bash
lister-flags.py [CIBLES...] [OPTIONS]
```

Exemples :

```bash
lister-flags.py --dry-run --tous --format json
lister-flags.py --dry-run --outil lister-outils --verbose
lister-flags.py --dry-run --combo combo-corriger-ascii --flag-partage version
```

## 7. Contraintes et risques

| Risque | Impact | Mitigation |
|---|---|---|
| argparse dynamique | details incomplets | catalogue prioritaire + indication source |
| commande de combo composee | provenance partielle | associer la case et conserver la source |
| catalogue obsolete | inventaire divergent | fusionner avec AST sans executer |
| nom inconnu | resultat vide | message et code 1 |

## 8. Livrables

| Livrable | Destination |
|---|---|
| Python | `lister/lister-flags/lister-flags.py` |
| Bash | `lister/lister-flags/lister-flags.sh` |
| Documentation | `lister/lister-flags/lister-flags.md` |
| Specification | `lister/lister-flags/spec/` |
| Catalogue | `generateurs/generateurs-commande/catalogue-commandes.json` |
| Index | `tools/index-tools.md` |

## 9. Validation

- [ ] `python3 -m py_compile lister-flags.py`
- [ ] `--dry-run --tous` retourne des entites
- [ ] une cible outil retourne ses flags
- [ ] une cible combo retourne ses flags
- [ ] `--format json` est parseable
- [ ] `--flag-partage` filtre les entites concernees
- [ ] aucune execution de script decouvert
- [ ] ASCII et fins de ligne valides
- [ ] tests reels a ecrire et executer par Morpheus

## 10. RVAV

- [rechercher] -- sources catalogue, combos et argparse inspectees
- [verifier] -- contrat des champs et filtres explicite
- [analyser] -- fusion catalogue/AST et limites documentees
- [valider] -- validation technique a executer avant promotion

## Historique des modifications

| Date | Version | Auteur | Description |
|---|---|---|---|
| 2026-09-03 | 0.1.0 | Vulcain | Creation initiale |
