---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# detecter-divergences-version

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** Detecter
**Chemin :** `agents/tools/detecter/detecter-divergences-version/`

## Description

Detecter les `spec/` dont la version declaree diverge de celle du `.py`
associe dans le meme dossier outil (regle des 5 fichiers : py, sh, md,
spec doivent etre alignes en VERSION/STATUT apres toute modification de
version d'un outil).

**Pourquoi cet outil ?**
- La lecon Vulcain (controle Janus 2026-08-09) : la spec est le fichier
  le plus souvent oublie lors d'un changement de version d'un outil.
- Le scan manuel est long (11+ spec) et les formats de version varient :
  en-tete, tableau frontmatter, versionning, tableau historique.
- Cet outil automatise la question : **"quelle spec diverge de son .py ?"**

## Utilisation

```bash
# Scan complet (racine par defaut : cerveau-projet)
python3 detecter-divergences-version.py

# Avec une racine explicite
python3 detecter-divergences-version.py --racine cerveau-projet/agents/tools

# Lister les spec trouvees sans croiser
python3 detecter-divergences-version.py --liste

# Exporter le rapport en markdown
python3 detecter-divergences-version.py --export rapport-divergences.md

# Version
python3 detecter-divergences-version.py --version
```

## Verdicts

| Verdict | Signification |
|---|---|
| `ALIGNE` | version spec == version py (ou meme base et suffixe) |
| `DIVERGENT (base)` | version spec != version py (base differente) |
| `DIVERGENT (suffixe)` | meme base (X.Y.Z) mais suffixe different (ex: -ebauche vs -beta) |
| `SANS VERSION` | version non trouvee dans la spec ou le py |
| `SANS PY` | aucun .py dans le dossier outil |

## Formats de version supportes (lecon Janus)

1. **En-tete** : `**Version :** 0.2.0` / `**Version** : 0.2.0` / `Version: X`
2. **Tableau frontmatter** : `| **Version** | 0.2.2 |`
3. **Section Versionning** : `| Version | Date | Changements |` puis `| 0.1.0 | ... |`
4. **Titre** : `# Spec -- ... v0.2.20`
5. **Tableau historique** : `| Date | Version | Auteur |` (derniere ligne)

> La version d'**EN-TETE prime** sur le tableau d'historique (lecon Janus :
> un premier scan avait pris la mauvaise version pour migrer-identite).

## Cas particulier

`guider-parcours` : la spec-guider-parcours versionne les **PATTERNS**
(v0.2.x) distincts de la version de l'outil guider-parcours.py (0.3.1).
Cet outil la rapporte comme DIVERGENTE, mais une DECISION documentee est
necessaire avant tout alignement (spec de reference des parcours, pas de
l'outil).

> **CAS LEGITIME ASSUME (decision Cerberus 2026-08-09)** : la spec
guider-parcours est la spec de reference des PARCOURS (patterns 1 a 11,
historique v0.2.0 -> v0.2.20) et ne doit PAS etre alignee sur la version
de l'outil guider-parcours.py (0.3.1). La divergence signalee est un cas
legitime : NE PAS aligner, NE PAS bloquer.

`activer-agent-principal` : la spec a une ligne d'historique MALFORMEE
(2 colonnes sans date, `| 0.5.0 | Vulcain | ...`) qui induit l'extraction
en erreur (0.3.4 vs 0.5.0). A nettoyer dans la spec (hors perimetre de
l'outil : a traiter par l'editeur de la spec).
