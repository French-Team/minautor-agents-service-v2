# Controle Re-controle boucle KO - Reparation carte themis (2026-08-20)

**Agent controleur** : Janus
**Mission controlee** : Reparation par Buffy du defaut OUTIL_HORS_CARTE themis ->
evaluer-processus (signale par Janus au controle precedent, rapport
controle-reparation-buffy-2026-08-20.md, lecon #179).
**Correction** : indice evaluer-processus ajoute a la case c16 de la carte
themis (parcours-themis.json), bump 0.5.2 -> 0.5.3, fiche sync (Pattern 14),
lock resync.
**Audit Themis** : CONFORME (rapport-audit-reparation-carte-themis-2026-08-20.md,
lecon #181).

---

## Points a verifier (E1-E10)

1. **Carte themis** : version 0.5.3, case c16 contient l indice
   `evaluer-processus` (nom exact), description mise a jour
2. **Fiche themis** : PARCOURS (v0.5.3) synchronisee (Pattern 14)
3. **cartes-lock** : themis present, en phase avec la carte
4. **evaluer-processus** : global + --agent themis = 0 probleme
   (le defaut OUTIL_HORS_CARTE est corrige)
5. **valider-cartes-decision themis** : CONFORME (verifie par Buffy,
   verrouille pour Themis -- verifier structurellement)
6. **valider-case** : CONFORME (0/0/0)
7. **Marbre** : 8/8 intact
8. **Normes** : ASCII 0, CRLF 0 sur les fichiers modifies
9. **Perimetre** : seuls fichiers modifies = carte themis, fiche themis,
   lock, themis/corrections + rapport (fichiers de mission)
10. **Conformite execution** : Buffy a suivi sa carte (editer-parcours ->
    valider-cartes-decision -> lecon BDD #180 avant retour, Pattern 13
    garde-fou v0.5.19 respecte)

---

## Verdict : VALIDE (tout conforme)

Le defaut OUTIL_HORS_CARTE themis -> evaluer-processus signale au controle
precedent est CORRIGE : l indice evaluer-processus est present dans la case
c16 de la carte themis (v0.5.3), la fiche est synchronisee (Pattern 14), le
lock en phase, evaluer-processus global + themis = 0 probleme,
valider-cartes-decision CONFORME, valider-case CONFORME (0/0/0), marbre
8/8, ASCII 0 CRLF 0. Perimetre propre (carte, fiche, corrections, lock -
les fichiers marbre sont de la mission Gardien anterieure, deja controlee
VALIDE). Conformite execution Buffy : trace conforme (editer-parcours ->
valider-cartes-decision -> lecon BDD #180 avant retour, Pattern 13 garde-fou
v0.5.19 respecte). Aucun defaut restant.
