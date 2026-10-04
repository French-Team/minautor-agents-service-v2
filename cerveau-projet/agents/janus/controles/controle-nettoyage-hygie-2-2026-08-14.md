# Controle Janus : 2e nettoyage Hygie (suppression des 2 residus commites)

**Date** : 2026-08-14 | **Controleur** : Janus | **Mission controlee** : Hygie (suppression des 2 residus anciens commites)

## Verdict : VALIDE (12/12, avec 1 decouverte a traiter)

| # | Verification | Resultat |
|---|---|---|
| J1 | Snapshot du jour (2026-08-14, 2173 fichiers) | OK |
| J1b | Snapshot inventorie (nb_fichiers > 2000) | OK |
| J2 | Commit 49e966e (suppression 2 residus) | OK |
| J2b | 0 occurrence des 2 fichiers cibles dans HEAD | OK (faux KO initial : un 3e rapport du 12/08 matche - voir Decouverte) |
| J2c | 2 fichiers absents du disque | OK |
| J2d | Commit errone 6c64ae5 defait (reset soft + git rm -f) | OK |
| J3 | detecter-residus : PROPRE (hors tmp-janus auto) | OK |
| J4 | Rapport NON VIDE (2075 octets) + reference snapshot + commit | OK |
| J4b/J4c | Rapport reference + normes 0/0 | OK |
| J5 | Lecon Hygie (2e mission) + gap detecter-residus signale | OK |
| J5b | Usages Hygie au registre (4) | OK |
| J6 | Discipline tmp (0 dossier de mission restant) | OK |

## DECOUVERTE : 3e residu commite non identifie (a traiter)
En verifiant J2b, le controle a detecte un 3e fichier de la meme famille encore dans HEAD :
- **rapport-detecter-decalages-catalogue-2026-08-12.md** (du 12/08)
- Etat : ABSENT du disque (supprime par Hygie lors de la 1re mission le 13/08) mais TOUJOURS dans HEAD
  avec un statut git `D` (suppression jamais COMMITEE)
- Ce n etait PAS dans le perimetre de la mission Hygie (2 residus cibles) -> signale pour une mission dediee :
  commiter la suppression du rapport du 12/08 (git rm --cached ou git commit de la suppression en attente).

## Recommandation
- Mission dediee (Buffy ou Hygie) : commit la suppression en attente du rapport-detecter-decalages-catalogue-2026-08-12.md (statut D).
- Gap detecter-residus (signale par Hygie) : le pattern TEMP ne couvre pas les noms maches avec prefixe projet
  (ex. analyste-in-console.tmp-test004x.sh) - a elargir par Vulcain.
