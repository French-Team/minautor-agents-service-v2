# combo-creer-fichier-cerveau

**Version** : 0.2.0
**Type** : definition de combo (fichier du cerveau -- domaine Buffy)
**Emplacement** : `cerveau-projet/agents/tools/combos/combo-creer-fichier-cerveau/`

## Role

Enchaine la creation d'un fichier du cerveau : verifier le nommage, verifier
la structure, verifier l'absence du fichier, puis le creer. Le combo encapsule
la SUITE D OUTILS du chemin creer de la carte de Buffy (Pattern 3,
spec-guider-parcours v0.2.4) en gardant un CONTROLE de guidance intermediaire
(la question OUI/NON sur les verifications).

Les commandes ne sont plus ecrites en dur : chaque etape est une case
`generateur` qui demande la commande a `generateurs-commande` (catalogue),
puis une case `outil` qui l'execute. Le generateur est donc le composeur de
commandes de bout en bout (source de verite = catalogue-commandes.json).

## Cases

| Case | Type | Action |
|---|---|---|
| c1 | generateur | Composer valider-nommage (`valider-nommage --type outil {chemin}`) |
| c2 | outil | Executer valider-nommage |
| c3 | generateur | Composer valider-conventions (`valider-conventions {chemin}`) |
| c4 | outil | Executer valider-conventions |
| c5 | generateur | Composer rechercher-fichier (`rechercher-fichier {chemin}`) |
| c6 | outil | Executer rechercher-fichier |
| c7 | controle | CONTROLE : verifications OK ? (OUI -> c8 / NON -> c10) |
| c8 | generateur | Composer creer-fichier (`creer-fichier {chemin} {contenu}`) |
| c9 | outil | Executer creer-fichier |
| c10 | fin | FIN - fichier cree ou non conforme |

## Variables

| Variable | Role |
|---|---|
| `{chemin}` | Chemin du fichier a creer (ex: `cerveau-projet/agents/test/fiche.md`) |
| `{contenu}` | Contenu du fichier (si vide, fichier vide) |

## Utilisation

```bash
python3 cerveau-projet/agents/tools/combos/combos-moteur/combos-moteur.py \
  cerveau-projet/agents/tools/combos/combo-creer-fichier-cerveau/definition-combo.json \
  --var chemin=<chemin> --var contenu=<contenu> --reponses 'c7=OUI'
```

## Guidance preservee

Les verifications intermediaires (controle c7) restent dans le combo pour
guider l'agent ; les etapes MANUELLES du chemin (mettre a jour l'index, ajouter
les lecons) restent des cases de la carte de Buffy (guidance de la carte).
