# proteger-modifier-marbre
**Version :** 0.1.3
**Statut :** ebauche
**Categorie :** Proteger
## Pourquoi cet outil ?
Le marbre (voir proteger-verrou-marbre.md) rend immuables certaines zones du
noyau. Mais un systeme immuable a 100% serait inerte : il faut une PORTE de
modification legitime, etroitement controlee. Cet outil EST cette porte.
Il met a jour l empreinte d une zone dans `marbre.json` ET journalise la
modification dans `marbre-log.jsonl` (date, zone, raison, autorisation).
## La regle d or : l autorisation est HUMAINE
Un agent ne peut JAMAIS modifier le marbre seul. Le flux impose :
1. L agent a besoin de modifier une zone protegee -> il s ARRETE et signale
   le besoin (regle : jamais de modification directe).
2. Le GARDIEN du marbre propose la modification (zone, raison, impact).
3. L UTILISATEUR valide explicitement.
4. Le gardien execute la commande avec l autorisation.
Sans `--autorisation`, l outil refuse (code 1) : le marbre est immuable pour
les agents.

## Relecture OBLIGATOIRE avant gravure (v0.1.3, demande utilisateur 2026-08-16)
Toute modification ou ajout d une zone de REGLES (fichier dans
`regles-immuables/`) exige EN PLUS une relecture automatique : la porte lance
`detecter-contradictions --regles` (audit Argus : doublons de titres,
references cassees, concordance source/protocole) AVANT d accepter
l autorisation. Si l audit n est pas PROPRE, la modification est REFUSEE
(code 1) MEME avec `--autorisation` : il faut corriger les contradictions,
relancer l audit, puis repasser la porte.

Le champ `relecture: Argus PROPRE` est journalise dans `marbre-log.jsonl`.
`--no-audit` existe pour les zones NON-regles (cartes, cases) - jamais pour
une zone regles.
## Usage
```
python3 proteger-modifier-marbre.py --zone <nom> --raison <texte> --autorisation <cle>
python3 proteger-modifier-marbre.py --ajouter <nom> --fichier <chemin> --type <type> --raison <texte> --autorisation <cle>
python3 proteger-modifier-marbre.py --log
```
## Options
| Option | Description |
|---|---|
| `--zone <nom>` | Zone a re-empreinter (ex : `cerberus.c0`) |
| `--ajouter <nom>` | AJOUTER une nouvelle zone au marbre (v0.1.2) |
| `--fichier <chemin>` | Chemin relatif du fichier protege (avec --ajouter, type fichier) |
| `--type <type>` | Type de zone (avec --ajouter) : `fichier` (defaut), `case`, `marqueurs` |
| `--raison <texte>` | Justification de la modification (OBLIGATOIRE) |
| `--autorisation <cle>` | Preuve d autorisation de l utilisateur (OBLIGATOIRE) |
| `--log` | Affiche l historique des modifications du marbre |
| `--no-audit` | Desactive l audit Argus (zones NON-regles uniquement, jamais une zone regles) |
| `--version` | Affiche la version |

## Ajouter une nouvelle zone (v0.1.2)
Pour protege un NOUVEAU fichier de regles dans le marbre (ex :
`regles-general-global`) :
```
python3 proteger-modifier-marbre.py --ajouter regles-general-global \
  --fichier cerveau-projet/agents/regles-immuables/general/regles-general-global.md \
  --type fichier --raison "..." --autorisation ADMIN
```
La zone est creee avec son empreinte SHA-256, ajoutee au manifeste et
journalisee (action `ajout`). L autorisation utilisateur reste obligatoire.
## Codes de sortie
| Code | Signification |
|---|---|
| 0 | OK - marbre mis a jour et journalise (ou contenu inchange) |
| 1 | BLOQUE - autorisation utilisateur manquante |
| 2 | Erreur d utilisation (zone inconnue, parametres manquants) |
## Journal
Chaque modification approuvee est ajoutee a `marbre-log.jsonl` :
date, zone, raison, autorise_par, ancienne empreinte, nouvelle empreinte.
Le journal est l historique de confiance : il prouve QUE la modification a
ete autorisee, PAR QUI, et POURQUOI.
