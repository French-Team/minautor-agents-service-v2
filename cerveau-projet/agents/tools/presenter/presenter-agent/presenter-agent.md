# presenter-agent.py

## Description

**Presentateur COMMUN** d un agent - **presentation HUMAINE**. Outil
generique reutilisable : il lit la **fiche** de l agent (frontmatter YAML :
role, specialites, forces, style) ET son **arbre v2** (`arbre-<agent>.json` :
racine -> themes -> fins) et produit une presentation en **langage naturel**,
comme un humain se presenterait : qui je suis, ce que je peux faire pour toi,
comment je travaille, mes points forts, mon style.

Utilise pour Socrate (point de depart des super-combos) et reutilisable
pour tous les agents qui veulent se presenter a l ouverture d un round.

## Principe de fiabilite

La presentation est **GENErEE depuis la fiche + l arbre** : aucun texte
fige. Si la fiche est absente (sans role ni specialites) ou l arbre
illisible (aucune branche), l outil **REFUSE** d afficher une presentation
mensongere (code 1). `--dry-run` verifie uniquement que l arbre existe.

## Emplacement

`cerveau-projet/agents/tools/presenter/presenter-agent/`

## Utilisation

Lire cette documentation puis confirmer pour le mode reel :

```bash
python3 cerveau-projet/agents/tools/presenter/presenter-agent/presenter-agent.py socrate --confirme-doc
```

Options :

| Option | Description |
|---|---|
| `<agent>` | Nom de l agent dont on presente les possibilites (ex: socrate, morpheus) |
| `--detail` | Ajouter les buts (besoins) de chaque branche |
| `--lister-agents` | Lister tous les agents disposant d un arbre v2 |
| `--dry-run` | Verifier que l arbre existe sans rien afficher |
| `--doc` | Afficher cette documentation et sortir |
| `--confirme-doc` | Confirmer la lecture de cette doc (requis en mode reel) |
| `--verbose` | Afficher les details |
| `--chrono` | Mesurer la duree d execution |

## Sortie

Une presentation humaine generee depuis la fiche + l arbre :

```
Bonjour ! Je suis SOCRATE.
<mon role>

Ce que je peux faire pour toi :
  - <specialite 1>
  - <specialite 2>

Comment je travaille, concretement :
  1) REVISION
     <description>
  2) SYNTHESE
     <description>

Mes points forts :
  * <force 1>
  * <force 2>

Mon style : <style> ; <ton>.

Je t'ecoute : dis-moi ce qui t'amene.
```

## REGLE D AFFICHAGE (importante)

L agent qui lance cette presentation doit **AFFICHER la sortie COMPLETE**
a l utilisateur (via Pilote -> Oracle -> Cerberus -> USER). Une
presentation generee mais non transmise n existe pas pour l utilisateur.

## Notes techniques

- **100% stdlib Python** : aucune dependance externe (mini-parseur YAML
  integre pour le frontmatter de fiche).
- **ASCII strict** : aucun accent ni caractere Unicode.
- La fiche est cherchee dans `cerveau-projet/agents/<agent>/<agent>.md` ;
  l arbre dans `cerveau-projet/agents/<agent>/parcours/arbre-<agent>.json`
  puis `cerveau-projet/agents/<agent>/arbre-<agent>.json`.
- La presentation ne contient **aucun texte fige** : tout (role,
  specialites, forces, branches) est lu dans la fiche + l arbre.

## Maintenance

Proprietaire : Buffy (developpeur principal, outils communs).
En cas de modification de la fiche ou de l arbre d un agent, relancer :
`presenter-agent <agent> --confirme-doc` pour verifier la synchronisation.