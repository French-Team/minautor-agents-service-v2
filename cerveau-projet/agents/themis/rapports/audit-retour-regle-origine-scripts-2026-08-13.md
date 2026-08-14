# Audit Themis - Retour a la regle d origine des scripts temporaires (v0.2.4)

**Date** : 2026-08-13
**Mission auditee** : Buffy -> Morpheus (demande utilisateur : revenir a la regle d origine)
**Verdict** : **VALIDE** (15/15)

## T1. Protocole v0.2.4 (3/3)

- version 0.2.4 + regle d origine enoncee (dossier tmp-<agent> cree a la
  racine, rm -rf tmp-<agent> en fin de mission)
- 0 mention .agents-tmp (rewrite complet)

## T2. test-024 adapte (4/4)

- point 2b present (aucun dossier tmp-* residuel) + lecture du profil classeur
  (agent courant exclu)
- 14/14 positif + preuve negative (tmp-zz -> KO 2b detecte)

## T3. Gitignore + dossier (3/3)

- tmp-*/ present, .agents-tmp/ absent du gitignore, dossier .agents-tmp/ supprime

## T4. Normes et residus (3/3)

- ASCII strict 0/0 + LF pur 0/0 (protocole + gitignore + test-024 + lecons)
- 0 dossier tmp-* residuel (hors tmp-themis, dossier de la mission courante)

## T5. Conformite (2/2)

- test-029 : 14/14 (44 tests) + test-030 : 10/10

## Decouverte majeure (lecons vivantes)

Le garde-fou 2b a detecte DEUX residus reels en cascade pendant l audit :
tmp-buffy (mission precedente) puis tmp-morpheus (mission Morpheus terminee,
active Themis sans supprimer son dossier). Les agents n appliquent pas encore
automatiquement la discipline rm -rf tmp-<agent> avant de passer la main :
le garde-fou la surveille desormais en permanence.

## Synthese

La regle d origine est restauree et SURVEILLEE : dossier tmp-<agent>/ cree a
la racine, supprime en fin de mission (rm -rf), garde-fou test-024 point 2b
(0 dossier residuel hors agent courant). Retour a la simplicite.
