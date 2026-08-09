# combo-creer-protocole

**Version** : 0.2.0
**Type** : definition de combo (fichier du cerveau -- domaine Buffy)
**Emplacement** : `cerveau-projet/agents/tools/combos/combo-creer-protocole/`

## Role

Enchaine la creation d'un protocole : verifier la convention, creer le
dossier, creer le protocole. Le combo encapsule la SUITE D OUTILS du chemin
protocole de la carte de Buffy (Pattern 3, spec-guider-parcours v0.2.4) en
gardant un CONTROLE de guidance intermediaire (la question OUI/NON sur le
respect de la convention).

Les commandes ne sont plus ecrites en dur : chaque etape est une case
`generateur` qui demande la commande a `generateurs-commande` (catalogue),
puis une case `outil` qui l'execute.

## Cases

| Case | Type | Action |
|---|---|---|
| c1 | generateur | Composer valider-conventions (`valider-conventions {chemin}`) |
| c2 | outil | Executer valider-conventions |
| c3 | controle | CONTROLE : convention respectee ? (OUI -> c4 / NON -> c8) |
| c4 | generateur | Composer copier-dossier (`copier-dossier cerveau-projet/agents cerveau-projet/agents/{chemin}`) |
| c5 | outil | Executer copier-dossier |
| c6 | generateur | Composer creer-fichier (`creer-fichier {chemin} {contenu}`) |
| c7 | outil | Executer creer-fichier |
| c8 | fin | FIN - protocole cree ou convention non respectee |

## Variables

| Variable | Role |
|---|---|
| `{chemin}` | Chemin du protocole a creer (ex: `cerveau-projet/agents/regles-immuables/general/mon-protocole.001.01.ebauche.md`) |
| `{contenu}` | Contenu du protocole (si vide, fichier vide) |

## Utilisation

```bash
python3 cerveau-projet/agents/tools/combos/combos-moteur/combos-moteur.py \
  cerveau-projet/agents/tools/combos/combo-creer-protocole/definition-combo.json \
  --var chemin=<chemin> --var contenu=<contenu> --reponses 'c3=OUI'
```

## Guidance preservee

Le controle intermediaire (c3) reste dans le combo pour guider l'agent ; les
etapes MANUELLES du chemin (RVAV final) restent des cases de la carte de Buffy
(guidance de la carte).
