---
identite:
  type: index
  appartient_a: optimus-prime
  commun: false
---

# INDICES -- _operateur/optimus-prime/

> Tete de lecture : lire CECI avant les fichiers. L'indice pointe, le contrat fait foi.

| Besoin | Lire (fichier, section) |
|---|---|
| Verifier la Matrice comme serveur distant (Flux 2) | `cockpit/README.md` + `cockpit/cockpit-matrice.py --route complet` (routes privees verrouillees, lecture seule, M-129) |
| Qui je suis, regles absolues, mission | `optimus-prime.md` (fiche, tout) |
| Reprendre une session | `protocoles/proto-1-reprise-mission.md` |
| Friction -> evolution reversible | `protocoles/proto-2-auto-evolution.md` |
| Un probleme avant de creer | `protocoles/proto-3-debug-dag.md` |
| Avant toute livraison | `protocoles/proto-4-auto-audit-3-axes.md` |
| Galere outil natif -> creer l'outil | `protocoles/proto-5-auto-amelioration.md` |
| Forme et style des fichiers | `conventions/` (index : conventions-readme.md) |
| Problemes fondamentaux (chemin, lien, nom, flag) | `conventions/convention-chemins-liens-noms-flags.md` (contrat CV-007) + controle : `super-combos/combos/outils/verifier-contrat-fondamental.py tout` |
| Combos et super-combos (numerotes sc-NNN / c-NNN) | `conventions/convention-nommage-numerote.md` (contrat CV-008) + registre `super-combos/combos/registry.json` + controle : `super-combos/combos/outils/creer-combo.py lister` |
| Themes de travail (arbre) | `parcours/themes/index-themes.json` |
| Commandes de mes outils | `matrice/data/manuel-outils.md` (sections operateur) + `super-combos/combos/outils/outils-readme.md` |
| Routes privees (cockpit) | `cockpit/routes-privees.json` (mapping /etat /sante /flux1 /flux2 /chercher /metriques) |
| Chercher une mission, une lecon, un fichier | `matrice/data/outils/rechercher/main.py rechercher --requete <texte> --dans tous` (porte unique) ou `cockpit-matrice.py --route chercher --requete <texte>` |

## Regles de lecture (economy)

- Un protocole se lit QUAND sa situation arrive (index : protocoles-readme.md),
  pas tous d'un coup.
- L'indice se lit avant les fichiers de la zone : il dit quoi lire, jamais tout.
- Les lecons vivent en BDD (matrice/data/lecons.json via outil bdd-lecons) --
  il n'existe AUCUN fichier de lecons a relire.
