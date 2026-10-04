---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# AUDIT MO-522 / EO-534 -- TOUTES LES APPELLATIONS D IDENTIFIANTS (M-, MO-, EO-, ...)

Question du createur : "quelles sont les differentes appellations comme M-xxx,
MO-xxx, EO-xxx ? Je veux la liste de toutes ces appellations et une breve
description de chacune."

Posture AUDITEUR : lecture seule. La source de verite est la convention
CV-011 (table des prefixes en service) et ses amendements ; cette carte en est
la lecture lisibilisee, completee des familles plus recentes.

## LA TABLE DES PREFIXES

| Prefixe | Signification | Qui l emet / ou |
|---|---|---|
| M- | mission du CAMELEON (Flux 1) | matrice/pilote/entonnoir-files.json |
| E- | item d entonnoir du CAMELEON (Flux 1) | matrice/pilote/entonnoir-files.json |
| EO- | item d entonnoir d OPTIMUS (Flux 2) | _operateur/optimus-prime/pilote/entonnoir-files-optimus.json |
| MO- | mission d OPTIMUS | _operateur/optimus-prime/pilote/file-missions-optimus.json |
| L- | lecon (savoir-faire acquis, reutilisable) | matrice/data/lecons.json |
| TH- | theme / posture du VIVIER | matrice/data/vivier-themes.json |
| CV- | convention de la Matrice | matrice/data/conventions-matrice.json |
| CT- | constat | (migre depuis C- nu le 2026-09-13) |
| P- | protocole | _operateur/optimus-prime/protocoles/ |
| R- | regle | _operateur/optimus-prime/regles-immuables/ |
| H- | entree d historique-bdd | (historique) |
| N- | item numerote de la revue createur | (revue) |
| V- | variable | matrice/data/classeur-variables.json |
| c- | combo (minuscule) | super-combos/combos/ (registre des combos) |
| sc- | super-combo (minuscule) | super-combos/ (registre des super-combos) |
| PB- | etape PENSE-BETE d une chaine | preparation/ (chaine-pense-bete) |
| SP- | etape SPEC d une chaine | preparation/ (chaine-pense-bete) |
| TD- | etape TODO d'une chaine | preparation/ (chaine-pense-bete) |

## FAUX POSITIFS A NE JAMAIS PRENDRE POUR DES IDS
- SHA-256, UTF-8 : ce sont des formats/algorithmes, pas des familles d ids.
- C- (nu) : famille MORTE, migree en CT- le 2026-09-13 (chaque valeur garde sa trace dans constat_legacy).

## L ECART SIGNE (posture audit)

La table CV-011 date du 2026-09-13. Or la convention CV-008 a ete AMENDEE le
2026-09-19 pour ajouter les familles PB-, SP- et TD- (la chaine
pense-bete -> spec -> todolist). CV-011 n a pas ete revisee pour les nommer :
sa table ne porte donc pas ces trois familles. Cette carte les ajoute (mesure
par la presence reelle des compteurs chaine-compteurs.json), et l ecart est
SIGNE -- une table de prefixes qui ne suit pas ses amendements finit par
interdire une famille deja en service.

## VERDICT

La liste existe (CV-011) et elle est mesuree sur disque ; cette carte la rend
lisible et complete des trois familles plus recentes (PB/SP/TD) que CV-011
n avait pas encore integrees. Ecart signale, non corrige (posture audit) : la
table de reference CV-011 est en retard sur l amendement CV-008.
