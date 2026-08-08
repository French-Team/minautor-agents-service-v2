---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# verifier-role-fichier

**Version :** 0.2.0-py
**Statut :** prepare
**Categorie :** verifier
**Chemin :** `agents/tools/verifier/verifier-role-fichier/`
**Proprietaire :** Janus (outil partage)

## Description

Verifier qu'un fichier est utilise uniquement pour sa fonction prevue. Chaque type de fichier du cerveau-projet a un role unique (index = navigation, convention = regles, protocole = processus, spec = specification, template = modele). Cet outil detecte les sections interdites qui detournent un fichier de son role (suivi, TODO, historique, prochaines etapes).

## Utilisation

```bash
# Verifier un fichier
verifier-role-fichier.sh cerveau-projet/index-cerveau.md

# Verifier un index
verifier-role-fichier.sh cerveau-projet/pense-betes/index-pense-bete.md

# Verifier un protocole
verifier-role-fichier.sh cerveau-projet/pense-betes/regles-immuables/general/protocole-outils/protocole-outils.001.01.ebauche.md
```

## Roles et sections interdites

| Type de fichier | Role | Sections interdites |
|---|---|---|
| `index-*.md` | Navigation | Prochaines etapes, TODO, A faire, Statut du, Corrections recentes, Notes de session, Lecons apprises |
| `convention-*.md` | Conventions | Prochaines etapes, TODO, A faire, Historique (sauf definition) |
| `protocole-*.md` | Processus | Prochaines etapes, TODO, A faire, Statut, Historique (sauf description) |
| `spec-*.md` | Specification | Prochaines etapes, TODO, A faire |
| `*-template.md` | Modele | Prochaines etapes, TODO, A faire |

## Ce que l'outil fait

1. **Identifie** - Le type de fichier selon son nom (index, convention, protocole, spec, template)
2. **Cherche** - Les sections interdites selon le role
3. **Analyse** - Pour les conventions et protocoles, distingue une definition d'un detournement
4. **Verifie** - La taille du fichier (seuil : 200 lignes)
5. **Rapporte** - Les erreurs trouvees, retourne 0 si conforme, 1 sinon

## Exemples de sortie

```bash
$ verifier-role-fichier.sh cerveau-projet/index-cerveau.md
[OK] cerveau-projet/index-cerveau.md est conforme a son role

$ verifier-role-fichier.sh fichier-index-avec-todo.md
[ERREUR] fichier-index-avec-todo.md est un INDEX et contient une section interdite :
3:## Prochaines etapes
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Apres modification d'un fichier** | Verifier que le fichier reste dans son role |
| **Audit du cerveau** | Detourer les fichiers mal utilises |
| **Purification** | Identifier les sections a retirer d'un fichier |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `verifier-separation-preoccupations` | Verifie sur tous les fichiers du projet (version globale) |
| `nettoyer-fichier` | Purifie les fichiers apres detection |
| `valider-conventions` | Verifie que les conventions sont respectees |

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |

---
