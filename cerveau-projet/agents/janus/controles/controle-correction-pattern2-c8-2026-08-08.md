---
# Mission de controle -- Correction Pattern 2 (minerve c8 + promethee c8)
# Second controle (Buffy) -- suite audit Themis serie 11 parcours

agent:
  nom: "janus"
  type_controle: "second-controle"
  date: "2026-08-08"
  cible:
    - "cerveau-projet/agents/minerve/parcours/parcours-minerve.json"
    - "cerveau-projet/agents/promethee/parcours/parcours-promethee.json"
---

# Mission de controle -- Correction des 2 ecarts Pattern 2

**Origine** : Themis (audit serie 11 parcours) a signale 2 ecarts MINEURS au
Pattern 2 de la spec v0.2.0 : les cases minerve c8 et promethee c8 (mise a jour
d'index via editer-fichier) n'avaient pas le rappel ASCII en tete de leurs
indices. Buffy a corrige. Verifier la correction.

## Verdict attendu

1. **JSON valide** : json.load OK sur les 2 parcours
2. **Premier indice de c8** : type regle avec texte REGLE IMMUABLE ASCII (Pattern 2 conforme) dans les 2 cas
3. **REGLE INDEX en position 2** : toujours presente (la correction n'a rien supprime)
4. **Navigation inchangee** : --liste OK (22 lignes) + --reponses creer/completer -> PARCOURS TERMINE (4 chemins)
5. **ASCII strict** : 0 non-conforme sur les 2 parcours

---

## RESULTAT DU CONTROLE

**VERDICT : VALIDE (5/5)**

| Point | Verification | Resultat |
|---|---|---|
| 1 | JSON valide | json.load OK sur les 2 parcours | OK |
| 2 | Premier indice de c8 = regle ASCII | minerve : pos1 regle ASCII True / promethee : pos1 regle ASCII True | OK |
| 3 | REGLE INDEX en position 2 | minerve : pos2 regle INDEX True / promethee : pos2 regle INDEX True | OK |
| 4 | Navigation inchangee | --liste 22 + 4 chemins (creer/completer x2) -> PARCOURS TERMINE | OK |
| 5 | ASCII strict | 0 non-conforme sur les 2 parcours | OK |

**Outils utilises pour le controle** : activer-agent-principal, guider-parcours, valider-conformite-ascii, lire-fichier, editer-fichier
