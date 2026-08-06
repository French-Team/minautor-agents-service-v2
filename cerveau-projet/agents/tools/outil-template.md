# [nom-outil]

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** [ajouter | analyser | changer | combos | condenser | copier | corriger | creer | decomposer | deplacer | detecter | ecrire | editer | evaluer | generateurs | gerer | inserer | lire | lister | mettre-a-jour | nettoyer | rechercher | supprimer | valider | verifier]
**Chemin :** `agents/tools/[categorie]/[nom-outil]/`

## Description

[Description complete de ce que fait l'outil, pourquoi il existe et ce qu'il resout.]

## REGLE IMMUABLE : prefixe du dossier

> Le nom de l'outil DOIT commencer par le prefixe du dossier de categorie.
> C'est une regle immuable (voir `convention-renommage.md`).

| Dossier | Nom attendu | Exemple invalide |
|---|---|---|
| `lire/` | `lire-xxx` | `xxx` |
| `rechercher/` | `rechercher-xxx` | `xxx` |
| `corriger/` | `corriger-xxx` | `dictionnaire-xxx` |
| `creer/` | `creer-xxx` | `remplir-xxx` |
| `mettre-a-jour/` | `mettre-a-jour-xxx` | `modifier-xxx` |

> Cette regle s'applique a TOUS les dossiers de categorie, y compris `generateurs/`, `combos/` et `tester/` (ex: `generateurs-squelette-pense-bete`, `combos-audit-general`, `tester-protection-blocage`).

**Verification** :
1. Au demarrage du script, le bloc `verifier_nommage` controle le prefixe (ne pas le supprimer).
2. L'outil `valider-nommage` avec `--recursive` detecte toute violation.

## REGLE IMMUABLE : compatibilite Git Bash (interdiction PCRE)

> Les outils tournent sur Git Bash Windows. Les options `grep -P`, `grep -oP`,
> `grep -qP` et la syntaxe `\K` (PCRE/perl) ECHOUENT silencieusement sur Git Bash
> (code 2, "supports only unibyte and UTF-8 locales").
> C'est une regle immuable (voir `convention-outils-agents.md` Regle 5 et
> `protocole-outils` Regle 7).

| Interdit | Raison | Alternative obligatoire |
|---|---|---|
| `grep -P` / `grep -oP` / `grep -qP` | Echec silencieux sur Git Bash | Python ou `sed` (BRE) |
| `\K` (PCRE) avec `grep -oE` | Ne matche jamais sur Git Bash | `sed -n 's/.../\1/p'` (BRE) |

**Verification** :
1. Aucun `grep -[a-z]*P` ni `\K` dans le script.
2. La detection de caracteres non-ASCII se fait avec Python (comme `valider-conformite-ascii`).
3. Avant promotion, tester reellement le script sur Git Bash (les regex ne se "voient" pas a l'ecran).

## Utilisation

```bash
# [Cas d'utilisation 1]
[nom-outil].sh [argument 1]

# [Cas d'utilisation 2]
[nom-outil].sh --dry-run [argument 1]

# [Cas d'utilisation 3]
[nom-outil].sh --verbose [argument 1]
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--dry-run` | Simuler sans appliquer les modifications | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. **[Etape 1]** - [Description de l'etape 1]
2. **[Etape 2]** - [Description de l'etape 2]
3. **[Etape 3]** - [Description de l'etape 3]
4. **[Rapport]** - [Description de la sortie]

## Exemples de sortie

```bash
$ [nom-outil].sh [argument 1]

=== [nom-outil] ===
[Sortie reelle de l'outil]

=== Resume ===
[Resume des resultats]
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **[Situation 1]** | [Pourquoi utiliser l'outil ici] |
| **[Situation 2]** | [Pourquoi utiliser l'outil ici] |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `[outil-lie-1]` | [Comment il complete cet outil] |
| `[outil-lie-2]` | [Comment il complete cet outil] |

## Notes de creation

- [ ] L'outil a ete teste en `--dry-run` avant application
- [ ] L'outil est conforme ASCII (aucun accent, aucun emoji) -- valider avec `valider-conformite-ascii`
- [ ] L'outil est reference dans `index-tools.md`
- [ ] L'outil est assigne a un agent dans sa carte de decision (protocole-outils Regle 6)
- [ ] Le statut est passe de `ebauche` a `prepare` apres validation RVAV
