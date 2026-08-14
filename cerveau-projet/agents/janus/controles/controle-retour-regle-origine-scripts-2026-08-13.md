# Controle Janus - Retour a la regle d origine des scripts temporaires (v0.2.4)

**Date** : 2026-08-13
**Mission controlee** : Buffy -> Morpheus -> Themis (demande utilisateur)
**Verdict** : **VALIDE** (J1-J5)

## J1. Protocole + gitignore (4/4)

- protocole v0.2.4 : regle d origine (dossier tmp-<agent>/ cree a la racine,
  rm -rf en fin de mission) + 0 mention .agents-tmp
- .gitignore : tmp-*/ present, dossier .agents-tmp/ supprime du disque

## J2. test-024 (3/3)

- point 2b (0 dossier tmp-* residuel hors agent courant) + lecture profil classeur
- 14/14 positif + preuve negative (tmp-zz -> KO 2b detecte)

## J3. Normes (2/2)

- ASCII strict 0/0 + LF pur 0/0 sur 6 fichiers (protocole, gitignore, test-024,
  lecons Buffy/Morpheus/Themis)

## J4. Residus (2/2)

- 0 dossier tmp-* residuel (hors tmp-janus) + 0 script .tmp-*/.zz-* a la racine
- la discipline est respectee : tmp-themis supprime par Janus au debut

## J5. Non-regression complete

- **44/44 OK** -- 44.1s, meilleur que la reference (44.3s -> mise a jour)

## Synthese

La regle d origine est restauree, SIMPLE et SURVEILLEE : dossier tmp-<agent>/
cree a la racine par l agent, supprime en fin de mission (rm -rf), garde-fou
test-024 point 2b (0 dossier residuel hors agent courant). Les 3 residus reels
detectes pendant la chaine (tmp-buffy, tmp-morpheus, tmp-themis) prouvent que
le garde-fou fonctionne ET que la discipline s installe : chaque agent
supprime SON dossier avant de passer la main.
