---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# migrer-cases-relecture

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** migrer/

## Pourquoi cet outil ?

L ancienne structure de relecture des parcours (c0 question "As-tu EN MEMOIRE ?"
avec OUI -> c0c) permettait a un agent de contourner la lecture de sa fiche en
repondant OUI. La relecture de la fiche et des corrections doit etre
OBLIGATOIRE a chaque activation : on migre vers une structure ou la lecture
est TOUJOURS exigee, puis la confirmation est posee.

## Structure cible

```
c0  [action]   RELIRE OBLIGATOIRE : corrections puis fiche   -> c0b
c0b [question] Confirmation : as-tu lu et compris ?   OUI -> c0c, NON -> c0
c0c [action]   CONTEXTE obligatoire (inchange, suivant conserve)
```

## Usage

```
python3 migrer-cases-relecture.py --tous
python3 migrer-cases-relecture.py --agent buffy
python3 migrer-cases-relecture.py --agent buffy janus --dry-run
python3 migrer-cases-relecture.py --tous --rapport rapport-migration.md
```

## Options

| Option | Role |
|---|---|
| `--agent <nom>...` | Migrer un ou plusieurs parcours (chemin automatique) |
| `--tous` | Migrer les 15 parcours |
| `--dry-run` | Afficher les transformations sans ecrire |
| `--rapport <fichier>` | Ecrire un rapport markdown |
| `--verbose` | Detail par parcours |
| `--version` | Version de l outil |

## Transformations appliquees

1. **c0** : `question` -> `action`, titre "RELIRE OBLIGATOIRE : corrections
   puis fiche", indices = regle + 2 outils lire-fichier (corrections puis
   fiche), `suivant` = c0b.
2. **c0b** : `action` -> `question` confirmation, branches OUI -> c0c et
   NON -> c0 (relecture).
3. **c0c** : conserve tel quel (suivant c0d ou c1 inchange).
4. **Version** : bump du patch (+1) de chaque parcours migre.

## Contraintes

- ASCII strict, LF pur, JSON ecrit en ASCII (ensure_ascii=True).
- 100% stdlib Python.
- Idempotent : relancer ne modifie plus (la structure cible est deja en place
  : c0 action + c0b question -> skip silencieux du re-bump si conforme).
