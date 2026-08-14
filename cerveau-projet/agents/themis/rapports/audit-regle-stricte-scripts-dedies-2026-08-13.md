# Audit Themis - Regle stricte scripts dedies (.agents-tmp)

**Date** : 2026-08-13
**Mission auditee** : Buffy (demande utilisateur : les .tmp continuent d etre crees a la racine)
**Verdict** : **VALIDE** (15/15)

## T1. Protocole v0.2.3 (6/6)

- version 0.2.3 + dossier dedie .agents-tmp/ documente
- AUCUNE mention de tolerance racine residuelle (autorisee/tolere/exception)
- regle stricte enoncee (JAMAIS de script temporaire a la racine)
- section Deux usages distincts : jetable cree dans `.agents-tmp/.tmp-*.py`
- section spawn_agents : ECRIRE dans `.agents-tmp/.tmp-<agent>-<sujet>.py`

## T2. Dossier dedie + garde-fou (2/2)

- .gitignore : .agents-tmp/ present
- test-024 : 13/13 OK (dossier present, scan racine uniquement - invisible)

## T3. Normes (3/3)

- ASCII strict 0/0 + LF pur 0/0 (protocole + gitignore)
- lecon Buffy : normes 0/0

## T4. Residus

- 0 residu a la racine (commande directe) + .agents-tmp/ vide apres suppression
  du script d audit (l unique KO initial etait le script d audit lui-meme)

## T5. Garde-fous impactes (2/2)

- test-039 (residus version racine) vert
- test-041 (outils critiques anti-residus) vert

## Synthese

La regle stricte est restauree : JAMAIS de script temporaire a la racine,
tout passe par `.agents-tmp/` (dossier dedie gitignore, invisible pour
test-024). Le point de bascule (v0.2.0 2026-08-13 20:44) et l officialisation
de la tolerance (v0.2.2 21:18) sont documentes dans la lecon Buffy.
