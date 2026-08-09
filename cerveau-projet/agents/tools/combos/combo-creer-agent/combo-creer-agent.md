# combo-creer-agent

**Version** : 0.2.0
**Type** : definition de combo (fichier du cerveau -- domaine Buffy)
**Emplacement** : `cerveau-projet/agents/tools/combos/combo-creer-agent/`

## Role

Enchaine la creation d'un agent : verifier le nom, creer le dossier, copier
le template de fiche, creer les corrections. Le combo encapsule la SUITE D
OUTILS du chemin agent de la carte de Buffy (Pattern 3, spec-guider-parcours
v0.2.4) en gardant un CONTROLE de guidance intermediaire (la question OUI/NON
sur la validite du nom).

Les commandes ne sont plus ecrites en dur : chaque etape est une case
`generateur` qui demande la commande a `generateurs-commande` (catalogue),
puis une case `outil` qui l'execute.

## Cases

| Case | Type | Action |
|---|---|---|
| c1 | generateur | Composer valider-nommage (`valider-nommage --type outil cerveau-projet/agents/{agent}`) |
| c2 | outil | Executer valider-nommage |
| c3 | controle | CONTROLE : nom valide ? (OUI -> c4 / NON -> c10) |
| c4 | generateur | Composer copier-dossier (`copier-dossier cerveau-projet/agents cerveau-projet/agents/{agent}`) |
| c5 | outil | Executer copier-dossier |
| c6 | generateur | Composer copier-fichier (template -> `{agent}/{agent}.md`) |
| c7 | outil | Executer copier-fichier |
| c8 | generateur | Composer creer-fichier (`corrections.md`) |
| c9 | outil | Executer creer-fichier |
| c10 | fin | FIN - agent cree ou nom invalide |

## Variables

| Variable | Role |
|---|---|
| `{agent}` | Nom de l'agent a creer (ex: `clio`) |

## Utilisation

```bash
python3 cerveau-projet/agents/tools/combos/combos-moteur/combos-moteur.py \
  cerveau-projet/agents/tools/combos/combo-creer-agent/definition-combo.json \
  --var agent=<nom-agent> --reponses 'c3=OUI'
```

## Guidance preservee

Le controle intermediaire (c3) reste dans le combo pour guider l'agent ; les
etapes MANUELLES du chemin (mettre a jour AGENTS.md) restent des cases de la
carte de Buffy (guidance de la carte).
