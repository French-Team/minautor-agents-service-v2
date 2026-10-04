# Controle Marbre - Reparation Gardien (2026-08-20)

**Agent controleur** : Janus
**Mission controlee** : Reparation par le Gardien de la dette preexistante marbre
`cerberus.c10` (re-empreinte) + retrait de la cle corrompue "2" du manifeste.
**Autorisation utilisateur** : OUI - re-empreinter c10 (ask_user 2026-08-20)

---

## Points a verifier (E1-E10)

1. **Integrite du marbre** : `proteger-verrou-marbre --tous --verbose` ->
   8 zones conformes, exit 0, aucun crash (KeyError fichier disparu).
2. **Re-empreinte journalisee** : marbre-log.jsonl contient l entree
   `cerberus.c10` (ancienne 197d59... -> nouvelle 90f47b..., autorisation
   UTILISATEUR-OUI-2026-08-20-re-empreinte-c10, date 2026-08-20 22:00).
3. **Cle corrompue "2"** : absente du manifeste (zones sans cle numerique).
4. **Empreinte c10 correcte** : celle du manifeste = empreinte reelle calculee
   sur la carte (90f47b...), identique au HEAD (contenu carte inchange).
5. **cartes-lock resynchronise** : empreinte lock = empreinte reelle du fichier
   parcours-cerberus.json.
6. **Perimetre** : seuls marbre.json, marbre-log.jsonl, cartes-lock.json,
   gardien/corrections.md et les traces ont ete modifies (aucun fichier hors
   mission).
7. **Normes** : ASCII 0 sur les fichiers modifies, LF pur.
8. **Lecon Gardien** : ajoutee dans gardien/corrections.md (ASCII 0).

---

## Verdict

- [X] VALIDE (tout conforme)
- [ ] A REVOIR (problemes mineurs)
- [ ] REJETE (problemes majeurs)

**Observations** :

1. Marbre 8/8 conforme (exit 0, aucun crash - le KeyError fichier a disparu).
2. Re-empreinte journalisee : 197d59... -> 90f47b..., autorisation
   UTILISATEUR-OUI-2026-08-20-re-empreinte-c10, date 2026-08-20 22:00:24.
3. Cle corrompue "2" absente du manifeste (aucune cle numerique dans zones).
4. Empreinte c10 du manifeste = empreinte reelle calculee (90f47b...).
5. cartes-lock en phase avec le fichier parcours-cerberus.json
   (84822039... = reel).
6. Perimetre propre : marbre.json, marbre-log.jsonl, cartes-lock.json,
   gardien/corrections.md + traces (chronos, registre-usages) - aucun
   fichier hors mission.
7. ASCII 0 et CRLF 0 sur tous les fichiers modifies.
8. Lecon Gardien presente dans gardien/corrections.md (1 entree 2026-08-20).
