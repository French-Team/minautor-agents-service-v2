# Rapport Chiron : education d'Atlas aux ARBRES de decision v2

- **Date** : 2026-08-24
- **Mission** : eduquer Atlas pour creer le dossier .md + .svg des agents v2
  (qui ont des ARBRES de decision, pas des cartes v1)
- **Outil disponible** : convertir-carte-mermaid v0.3.0 (mode `--arbres`) --
  genere .mmd + .svg + index.md des 9 arbres v2 dans cartes-vues/arbres/
  (test-101 11/11 OK, verrouille par Morpheus)

## Diagnostic pedagogique

**Constat** : Atlas est structurellement SAIN (fiche CONFORME, carte PROPRE,
METHODE RIGOUREUSE v0.5.6 en place : dossier dedie par exploration, un .md
par dossier, rapport complet doublon de structure) mais PEDAGOGIQUEMENT NON
PREPARE pour la v2 : SA carte n a AUCUNE branche pour generer les VUES des
arbres v2 (`.mmd` + `.svg`). Les branches actuelles de c1 : explorer / web /
documenter / analyser / cartographier / cartographier-agent. Aucune ne
mentionne les ARBRES v2 ni l outil convertir-carte-mermaid.

## Incoherences (corrections proposees)

| # | TYPE | GRAVITE | FICHIER | CORRECTION PROPOSEE |
|---|---|---|---|---|
| 1 | parcours | HAUTE | parcours-atlas.json c1 | Ajouter la branche `vues-v2` -> nouvelle case c35 |
| 2 | parcours | HAUTE | parcours-atlas.json | Creer la case c35 (action) : generer les vues v2 avec `convertir-carte-mermaid --arbres` (9 .mmd + 9 .svg + index.md dans cartes-vues/arbres/), documenter dans LE DOSSIER DEDIE atlas/rapports/vues-v2-<AAAAMMJJ>/ |
| 3 | fiche | MOYENNE | atlas.md PARCOURS | Documenter la mission vues-v2 dans la fiche (PARCOURS v0.5.7) + rappeler la difference ARBRE v2 vs CARTE v1 |
| 4 | fiche | MOYENNE | atlas.md REGLE METHODE | Etendre la REGLE METHODE RIGOUREUSE : pour les vues v2, le dossier dedie contient les .md par dossier + les .mmd/.svg generes par l outil |

## Difference ARBRE v2 vs CARTE v1 (a enseigner a Atlas)

- **Carte v1** : `parcours-<agent>.json` -- structure `cases` (case_depart,
  cases avec suivant/branches, fins). Vue generee par `convertir-carte-mermaid`
  (sans `--arbres`) dans cartes-vues/mermaid/.
- **Arbre v2** : `arbre-<agent>.json` -- structure `racine` (question +
  branches vers `theme-*.json`) -> themes (redirects: besoin -> action/
  procedure + fin vers `fins.json`) -> fins centralisees. Vue generee par
  `convertir-carte-mermaid --arbres` dans cartes-vues/arbres/.
- Les 9 agents v2 : stark, shuri, forge, rogers, parker, jarvis, vision,
  fury, edith (chacun a son arbre-<agent>.json + theme-*.json + fins.json).

## Verifications Chiron

- verifier-conformite-fiche atlas : CONFORME (fiche saine, seule l education
  manque).
- grep : zero mention de "vues-v2" / "arbres" dans la carte ou la fiche
  d'Atlas (a l exception de la METHODE RIGOUREUSE qui parle du dossier
  freelance).
- Verrou habilitation : editer-parcours --agent atlas BLOQUE pour chiron
  (cartes exclusives a Buffy) -> Buffy doit appliquer les corrections.

## Corrections proposees a Buffy (seule habilitee sur la carte d'Atlas)

1. `editer-parcours --agent atlas --branche c1 --reponse vues-v2 --vers c35`
   (ajouter la branche dans c1).
2. `editer-parcours --agent atlas --inserer-case c35` : case action
   "Generer les vues v2 (arbres de decision)" avec indices outil
   convertir-carte-mermaid (commande `--arbres`), regle METHODE RIGOUREUSE
   (dossier dedie atlas/rapports/vues-v2-<AAAAMMJJ>/), suivant -> c10
   (lecons et retour).
3. Mettre a jour la fiche atlas.md : PARCOURS v0.5.7 (branche vues-v2) +
   REGLE METHODE RIGOUREUSE (vues v2 = .md par dossier + .mmd/.svg generes).
4. Bumper la version de la carte (v0.5.6 -> v0.5.7).
