---
# Mission de controle -- synchronisation des listes apres parcours-atlas
# Second controle (Buffy + Vulcain) -- serie jeu de piste, 11e parcours

agent:
  nom: "janus"
  type_controle: "second-controle"
  date: "2026-08-07"
  cible:
    - "cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.md"
    - "demarrer.md"
---

# Mission de controle -- Sync listes (parcours-atlas)

**Origine** : Buffy + Vulcain (synchronisation des 2 listes apres la creation du 11e parcours).

## Verdict attendu

1. **Atlas present** dans les 2 listes (guider-parcours.md + demarrer.md)
2. **Versionning** : doc guider-parcours.md en v0.2.6, demarrer.md note v0.2.6
3. **Compteurs** : 11 parcours (tableau doc + Parcours disponibles (11) dans demarrer.md)
4. **Diff mecanique** : les 11 noms parcours-[a-z]*.json identiques entre les 2 fichiers
5. **ASCII** : 0 non-conforme dans les 2 fichiers

---

## RESULTAT DU CONTROLE

**VERDICT : VALIDE (5/5)**

| Point | Verification | Resultat |
|---|---|---|
| 1 | Atlas present dans les 2 listes | guider-parcours.md : 1, demarrer.md : 1 | OK |
| 2 | Versionning 0.2.6 | doc : 1, demarrer.md : 1 | OK |
| 3 | Compteurs 11 | Parcours disponibles (11) : 1, 11 parcours doc : 1 | OK |
| 4 | Diff mecanique | 11 noms identiques entre les 2 fichiers (SYNC OK) | OK |
| 5 | ASCII | 0 non-conforme dans les 2 fichiers | OK |

**Outils utilises pour le controle** : activer-agent-principal, valider-conformite-ascii, lire-fichier, editer-fichier
