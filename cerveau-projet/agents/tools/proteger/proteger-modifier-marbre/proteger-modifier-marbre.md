# proteger-modifier-marbre
**Version :** 0.1.0
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
## Usage
```
python3 proteger-modifier-marbre.py --zone <nom> --raison <texte> --autorisation <cle>
python3 proteger-modifier-marbre.py --log
```
## Options
| Option | Description |
|---|---|
| `--zone <nom>` | Zone a re-empreinter (ex : `cerberus.c0`) |
| `--raison <texte>` | Justification de la modification (OBLIGATOIRE) |
| `--autorisation <cle>` | Preuve d autorisation de l utilisateur (OBLIGATOIRE) |
| `--log` | Affiche l historique des modifications du marbre |
| `--version` | Affiche la version |
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
