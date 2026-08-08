# Controle -- Rappel ASCII dans les cases d'ecriture (Buffy) 2026-08-07

**Objet controle** : parcours-morpheus.json (c4, c8) + parcours-clio.json (c6, c8, c10) -- indice regle ASCII ajoute dans chaque case d'ecriture
**Mission controlee** : ajouter le rappel ASCII dans chaque case qui ecrit dans un fichier, pour que l'agent voie la regle juste avant d'ecrire (demande utilisateur)
**Agent auteur** : Buffy (developpeur principal -- fichiers du cerveau)
**Date du controle** : 2026-08-07

---

## Mission de controle

Verifier independamment (je ne fais pas confiance) :

| # | Point a verifier | Methode |
|---|---|---|
| 1 | Les 5 cases visees (morpheus c4/c8, clio c6/c8/c10) contiennent un indice regle ASCII en tete de la liste indices | inspection |
| 2 | Le texte du rappel est coherent : ASCII strict, aucun accent/emoji/Unicode, guillemets ASCII (pas de guillemets francais) | inspection |
| 3 | Les cases d'ecriture de vulcain (c6/c12) etaient deja couvertes avant la mission (pas de regression) | inspection |
| 4 | Les JSON restent valides (structure) | guider-parcours --liste |
| 5 | La navigation est inchangee (les branches aboutissent toujours a PARCOURS TERMINE) | guider-parcours --reponses |
| 6 | Conformite ASCII des 2 JSON modifies | valider-conformite-ascii |
| 7 | Le rappel est place AVANT l'outil d'ecriture dans la liste des indices (ordre des indices) | inspection |
| 8 | Aucune trace d'outil externe | detecter-usage-outils-externes |

---

## Verdict

- **Verdict** : VALIDE (8/8 points)
- **Points valides** : 8/8
- **Problemes detectes** : aucun
- **Detail** : les 5 cases visees (morpheus c4/c8, clio c6/c8/c10) ont l'indice
  regle ASCII en TETE de la liste indices (donc affiche avant l'outil d'ecriture),
  texte coherent (ASCII strict, guillemets ASCII), vulcain c6/c12 deja couverts
  (pas de regression), JSON valides, navigation inchangee (PARCOURS TERMINE),
  ASCII 0 non-conforme, traces externes 0.

---

## Lecons

1. La demande utilisateur (rappel ASCII juste avant d'ecrire) est bien servie par
   le modele de case existant : un indice regle en tete de la liste indices s'affiche
   avant l'outil d'ecriture -- pas besoin de nouvelle case ou de nouveau type.
2. L'audit des cases d'ecriture doit etre exhaustif : 7 cases au total (3 parcours),
   dont 2 deja couvertes (vulcain c6/c12) et 5 a completer (morpheus c4/c8,
   clio c6/c8/c10) -- verifier TOUTES les cases, pas seulement celles modifiees.
3. Le rappel ASCII est le meme texte partout (uniformite) : REGLE IMMUABLE ASCII,
   verifier avant d'ecrire, 100%% ASCII, guillemets ASCII jamais de guillemets francais.
