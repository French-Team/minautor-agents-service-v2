---
identite:
  type: outil
  appartient_a: commun
  commun: true
  combos:
    - combos-maj-readme-massive
---
# editer-fichier

**Version :** 0.5.2
**Statut :** prepare
**Categorie :** Editer
**Chemin :** `agents/tools/editer/editer-fichier/`
**Proprietaire :** outil partage

## Description

Remplacer une chaine par une autre dans un fichier. Version generique de corriger-liens et corriger-nommage.

**Echec explicite** : si AUCUNE occurrence n'est trouvee, l'outil retourne un code non nul (1) avec un message clair - jamais 0 silencieux. L'agent ne continue jamais en croyant a tort que l'edition a eu lieu.

## Utilisation

**MODE ANTI-HEREDOC (v0.5.2)** : plusieurs remplacements depuis un fichier JSON :
`python3 editer-fichier.py cible.md --remplacements-chemin specs.json` avec specs.json =
`[{"ancien": "...", "nouveau": "..."}, {"ancien": "...", "nouveau": "...", "premier": true}]`
(jamais de ligne bash geante - decision D6/D7 2026-08-21).

```bash
# Remplacer la premiere occurrence
editer-fichier.sh fichier.md "ancien" "nouveau"

# Remplacer toutes les occurrences
editer-fichier.sh --global fichier.md "texte" "remplacement"
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--global` | Remplacer toutes les occurrences | false (premiere seule) |
| `--backup` | Creer une sauvegarde .bak | false |
| `--dry-run` | Simuler sans modifier | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie que le fichier existe
2. Compte les occurrences
3. Remplace selon le mode (premiere ou global)

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Corriger un mot | `editer-fichier.sh f.md "faux" "vrai"` |
| Tout remplacer | `editer-fichier.sh --global f.md "X" "Y"` |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.5.2 | 2026-09-02 | MODE ANTI-HEREDOC : option `--remplacements-chemin <json>` applique plusieurs remplacements depuis un fichier JSON `[{"ancien":..,"nouveau":..,"premier": bool?}]` (jamais de ligne bash geante, decision D6/D7 2026-08-21). Parite .sh : non concerne (le .sh ne porte pas le mode anti-heredoc - exemption bumper v0.5.0). Numerotation corrigee : le 0.5.1 (2026-08-22, protection combos) avait ete loggue au changelog sans bump des champs - l anti-heredoc passe donc en 0.5.2 |
| 0.4.3 | 2026-08-17 | MESSAGES INFORMATIONNELS : messages contextuels selon le type de fichier modifie (.py/.sh -> bumper+tests, parcours -> valider-cartes+fiche, .md -> coherence index/README) - regle immuable v0.3.0 |
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels (premiere occurrence, --global, --dry-run, fichier inexistant), promotion prepare |
| 0.3.0 | 2026-08-12 | Qualite pro : echec explicite (0 occurrence -> code 1, jamais 0 silencieux), protection nommage, message d'aide enrichi |
| 0.4.0 | 2026-08-12 | PERFORMANCE (round 2) : une seule passe (test d'existence + replace, plus de double scan count puis replace) |
| 0.4.1 | 2026-08-12 | SECURITE (round 3) : refus de modifier a travers un lien symbolique, refus octet nul, lecture robuste utf-8-sig + fallback latin-1 (plus de crash sur BOM/latin-1) |
| 0.4.2 | 2026-08-16 | VERROU CIBLE (cle exclusive morpheus) : option --agent obligatoire, appel du verrou proteger-verrou-habilitation avec --cible (tester/tests/ = exclusif morpheus) |

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md
- [x] Le statut est passe de `ebauche` a `prepare`
| 0.4.4 | 2026-08-22 | VERROU CIBLE TOOLS (decision utilisateur, correctif structurel) : toute cible sous agents/tools/ exige un agent HABILITE - vulcain = tout tools/, morpheus = tester/tests/, buffy = index-tools.md + outil-template*. Le controle s'applique MEME sans --agent (breche fermee) et REMPLACE le verrou-carte pour ces cibles (sinon vulcain etait bloque par sa propre exclusivite). Preuves : buffy BLOQUE, vulcain autorise, sans agent BLOQUE. |
| 0.5.0 | 2026-08-22 | PERIMETRE PAR AGENT (decision utilisateur) : si cerveau-projet/agents/<agent>/perimetre.json existe, toute cible doit matcher au moins un motif (glob relatif racine, ** supporte via fnmatch). PRIME sur tout le reste. Perimetre absent = regles anterieures. Pilotes crees : vulcain (tools/**), morpheus (tester/tests/** + son dossier), buffy (fiches/corrections/cartes/regles-immuables/AGENTS.md/readmes). Preuves : buffy hors perimetre BLOQUE, vulcain OK, morpheus test OK, morpheus fiche themis BLOQUE. |
| 0.5.1 | 2026-08-22 | PROTECTION DES COMBOS (decision utilisateur - les combos sont plus puissants que les outils) : toute definition sous cerveau-projet/combos exige VULCAIN exclusivement (marqueur /cerveau-projet/combos/ ajoute au verrou cible). Les definitions vivant aujourd hui sous agents/tools/combos etaient deja couvertes par le marqueur tools. Le VERROU D EXECUTION des combos (qui peut lancer quel combo) reste a implementer. |
