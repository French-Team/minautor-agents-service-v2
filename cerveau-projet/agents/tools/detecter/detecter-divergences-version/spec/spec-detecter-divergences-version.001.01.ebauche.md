# Specification -- detecter-divergences-version

**Version :** 0.2.0
**Statut :** ebauche
**Categorie :** Detecter
**Date :** 2026-08-09
**Agent :** Vulcain
**Historique :** v0.2.0 (round 11 coherence documentaire : champ spec 'Version outil' prioritaire pour les specs de conventions dont la version documente des patterns au-dela de l outil -- ex: guider-parcours spec 0.6.2 / outil 0.5.0 ; constante VERSION ajoutee, resout le SANS VERSION de sa propre spec) -> v0.1.0 (creation, lecon Vulcain regle des 5 fichiers + controle Janus 2026-08-09)
**Pense-bete source :** lecon Vulcain regle des 5 fichiers + controle Janus 2026-08-09 (scan temporaire)

## Objectif

Detecter les spec/ dont la version declaree diverge de celle du .py
associe, pour appliquer durablement la regle des 5 fichiers (py, sh, md,
spec alignes en VERSION/STATUT apres toute modification de version d'un
outil).

## Contexte

- Le controle Janus (2026-08-09) a scanne 11 spec avec des scripts
  TEMPORAIRES (.tmp-scan-versions*.py) et detecte 6 divergences.
- Les lecons Janus : formats de version varies (la version d'en-tete
  prime sur le tableau d'historique), distinguer divergence de base vs
  de suffixe, cas particulier guider-parcours.
- Cet outil remplace les scripts temporaires par un outil durable.

## Fonctionnalites

| # | Fonctionnalite | Detail |
|---|---|---|
| 1 | Scan recursif | Parcourt les spec/ sous une racine (defaut cerveau-projet) |
| 2 | Extraction version spec | 5 formats : en-tete, tableau frontmatter, versionning, titre, tableau historique |
| 3 | Extraction version py | VERSION = dans le .py du meme dossier outil |
| 4 | Croisement | Verdict : ALIGNE / DIVERGENT (base) / DIVERGENT (suffixe) / SANS VERSION / SANS PY |
| 5 | Options | --racine, --liste, --version, --aide, --export (rapport markdown) |

## Verdicts

| Verdict | Condition |
|---|---|
| ALIGNE | v_spec == v_py |
| DIVERGENT (base) | base_version(v_spec) != base_version(v_py) |
| DIVERGENT (suffixe) | base identique, suffixe different |
| SANS VERSION | version spec ou py non trouvee |
| SANS PY | aucun .py dans le dossier outil |

## Regles de conception

1. 100% stdlib Python (aucune dependance externe).
2. 100% ASCII strict (aucun accent, emoji ou caractere Unicode).
3. Schema hybride : bloc identite dans les 12 premieres lignes du .py/.sh,
   frontmatter YAML dans le .md.
4. Parite py/sh (--version identique).
5. Preserver le style de fin de ligne du projet (CRLF sous Windows).
6. L'outil s'exclut de son propre scan (dossier spec/ detecte, mais
   s'il n'y a pas de .py dans son dossier, verdict SANS PY - pas une erreur).

## Validation

- Scan reel sur le cerveau : doit retrouver les 6 divergences de Janus
  (regenerer-catalogue, lister-agents, lister-outils, verifier-systeme,
  combos-moteur, guider-parcours).
- py_compile + bash -n OK.
- valider-nommage OK (prefixe detecter-).
- valider-conformite-ascii 0 non-ASCII.
- detecter-impacts VERDICT a jour.
- index-tools mis a jour (107 -> 108).
- catalogue generateurs-commande synchronise (entree ajoutee).

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-09 | Creation : scan spec/py, 5 formats de version, verdicts, options --racine/--liste/--export |
