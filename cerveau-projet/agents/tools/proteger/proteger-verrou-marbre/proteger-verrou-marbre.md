# proteger-verrou-marbre
**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** Proteger
## Pourquoi cet outil ?
Certaines regles du cerveau-projet doivent etre GRAVEES DANS LE MARBRE :
elles ne peuvent plus etre modifiees sans passer par un protocole de
securite du code (protocole-securite-marbre.md) qui exige une autorisation
explicite de l utilisateur. Ce sont la Constitution (Configuration Active +
cycle fondamental dans AGENTS.md), les regles immuables (regles-groupes-
agents.md) et les cases critiques des cartes (ex : relecture c0, activation
c10, chaine c14, fin c20 de Cerberus).
Le verrou du marbre verifie l INTEGRITE de ces zones : l empreinte SHA-256
du contenu actuel doit etre identique a celle enregistree dans le manifeste
`marbre.json`. Toute divergence = une modification NON autorisee = le marbre
est brise.
## Les deux temps du marbre
- **AVANT (ce verrou, blocage a la source)** : les outils du noyau qui
  ecrivent dans les fichiers proteges (activer-agent-principal,
  editer-parcours) verifient le marbre avant d ecrire. Zone divisee = ecriture
  refusee, la chaine s arrete.
- **APRES (garde-fou test-057)** : la non-regression verifie le marbre
  integral (`--tous`) a chaque lancement. Toute divergence = KO.
## Fonctionnement
1. Le manifeste `marbre.json` liste les zones protegees avec leur empreinte :
   - `case` : une case d un parcours JSON (cid) ;
   - `marqueurs` : le texte entre deux marqueurs d un fichier
     (`<!-- MARBRE:DEBUT ... -->` / `<!-- MARBRE:FIN ... -->`) ;
   - `fichier` : le fichier entier.
2. Le verrou recalcule l empreinte du contenu reel et la compare au manifeste.
3. Verdict : conforme (code 0) ou BLOQUE (code 1) avec la liste des zones
   divisees et la commande du protocole pour les re-empreinter legalement.
## Usage
```
python3 proteger-verrou-marbre.py --tous
python3 proteger-verrou-marbre.py --zone <nom>
python3 proteger-verrou-marbre.py --agent <nom>
python3 proteger-verrou-marbre.py --empreinte <nom>
python3 proteger-verrou-marbre.py --liste
```
## Options
| Option | Description |
|---|---|
| `--tous` | Verifie toutes les zones du manifeste |
| `--zone <nom>` | Verifie une zone precise (ex : `cerberus.c0`) |
| `--agent <nom>` | Verifie toutes les zones d un agent (prefixe `<agent>.`) |
| `--empreinte <nom>` | Affiche l empreinte actuelle d une zone (lecture seule) |
| `--liste` | Liste les zones protegees et leur raison |
| `--verbose` | Detail du verdict (empreintes attendue/actuelle) |
| `--version` | Affiche la version |
## Codes de sortie
| Code | Signification |
|---|---|
| 0 | OK - toutes les zones demandees sont conformes (marbre intact) |
| 1 | BLOQUE - au moins une zone diverge (marbre brise, modification sans protocole) |
| 2 | Erreur d utilisation |
## Modification legitime
Modifier une zone protegee n est possible QUE via
`proteger-modifier-marbre --zone <nom> --raison <...> --autorisation <cle>`
(autorisation utilisateur explicite, journalisee dans marbre-log.jsonl).
Sans cette porte, toute ecriture dans une zone du marbre est une violation.
