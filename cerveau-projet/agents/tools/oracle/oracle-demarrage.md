# oracle-demarrage

**Version :** 0.1.3
**Statut :** ebauche
**Categorie :** oracle
**Chemin :** `agents/tools/oracle/oracle-demarrage.py`

## Description

Serveur de demarrage de la v1 (session-admin) : lance, arrete et surveille
les serveurs de la session d une seule commande.

Repond a l impasse v1 identifiee le 2026-08-27 (meme nature que la v2,
mission [AT-1]) : le serveur oracle ne tournait jamais (lancement stdio
avec stdin DEVNULL = EOF immediat) et rien ne demarrait l infrastructure
au lancement de session. Ce serveur de demarrage est l equivalent v1 de
la chaine `jarvis demarrage`/`arret` de la v2, mais avec un code 100% v1
(decision utilisateur : 2 univers distincts, pas de copie de code).

Il lance :
- `oracle-server.py --boucle` : daemon resident (harnais + relais + DEFCON)
- le futur serveur de routines v1 (`routines-server.py`) s il existe
  (structure prete, lance automatiquement le jour ou il est cree)

## Utilisation

```bash
# Chaine de demarrage v1 (daemons -> DEFCON -> files -> operationnel)
python3 oracle-demarrage.py demarrage --confirme-doc

# Extinction propre des serveurs v1
python3 oracle-demarrage.py arret --confirme-doc

# Etat des serveurs v1 (oracle, routines, DEFCON, files, agents bloques)
python3 oracle-demarrage.py etat --confirme-doc

# Simulation sans rien lancer
python3 oracle-demarrage.py demarrage --dry-run
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--dry-run` | Simuler sans rien modifier | false |
| `--verbose` | Afficher les details | false |
| `--confirme-doc` | Confirmer la lecture de la documentation (requis en mode reel) | false |
| `--doc` | Afficher le .md complet et sortir | false |
| `--intervalle N` | Secondes entre deux tics du daemon | 30 |

## Ce que fait l'outil

1. **[1/4]** Lance `oracle-server.py --boucle` en daemon detache
   (DETACHED_PROCESS + CREATE_NEW_PROCESS_GROUP, log visible dans
   `observations/oracle-log.txt`, PID file `oracle-server.pid`).
   Sonde PID Windows via OpenProcess (os.kill(pid,0) TERMINERAIT le
   processus - lecon v2 hooks.py).
2. **[2/4]** Lance le futur serveur de routines v1 s il existe
   (`oracle/routines-server.py`, PID `routines-server.pid`).
3. **[3/4]** Affiche DEFCON v1 (files/defcon.jsonl), files de missions
   actives, agents bloques (P1 non lue).
4. **[4/4]** Declare ORACLE OPERATIONNEL et historise le demarrage.

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `oracle.py` | CLI de coordination v1 (envoyer/lire/activer/historiser) - l outil appelle `oracle.py historiser` pour tracer le demarrage |
| `oracle-server.py` | Serveur de la v1 - mode `--boucle` ajoute (daemon resident) |
| `activer-agent-principal` | Activation des agents - consomme le mode `--snapshot` d analyser-tokens |

## Notes de creation

- [x] L'outil affiche ses MESSAGES INFORMATIONNELS en fin d action reussie
- [x] L'outil embarque le bloc DOC OBLIGATOIRE (--doc / --confirme-doc)
- [x] L'outil est conforme ASCII
- [ ] L'outil est reference dans index-tools.md (categorie oracle)
- [ ] Le statut passe de `ebauche` a `prepare` apres validation RVAV

## Historique

| Version | Date | Description |
|---|---|---|
| 0.1.3 | 2026-08-29 | INCIDENT CORRUPTION HUB RESOLU : le relais (fonctions/relais.py) re-echappait les lignes brutes du hub a chaque tic (json.dumps sur un brut deja serialise) -> inbox/cerberus.jsonl a atteint 1 Go de guillemets imbriques. Fix : _ecrire_jsonl ecrit un str TEL QUEL, un dict serialize une seule fois. Reconstruction du hub (55 messages valides extraits, 41 alertes [FANTOMES] spammees purgees, 14 messages legitimes conserves). Faux positif SERVEUR MORT corrige (auto-exclusion os.getpid() retirait le daemon lui-meme - 18 alertes [FANTOMES] spammees). Garde-fous : test-108 (controle processus), test-109 (relais + audit hub). Routines v1 transposes des v2 : flux, sante, encart, live, notation, vigie-perimetre, compter-entree/sortie (manifest v0.1.3, grades G3). |
| 0.1.2 | 2026-08-29 | Controle processus fantomes : nouveau module fonctions/controle_processus.py liste les processus reels par ligne de commande (PowerShell sur Windows) et verifie UNE seule instance par serveur (oracle-server, routines-server v1). Detection automatique au tic du daemon (alerte cerberus) + commande `oracle.py controle-processus`. Correctifs fenetres cmd : CREATE_NO_WINDOW sur le lancement des routines v1 et _historiser. |
| 0.1.1 | 2026-08-27 | Correctifs robustesse : dry-run ne lance plus les serveurs, tolerance JSON double-encode dans inbox (cerberus.jsonl) pour agents bloques + relais du daemon. |
| 0.1.0 | 2026-08-27 | Creation : serveur de demarrage v1 (demarrage/arret/etat), lance oracle-server --boucle + futur routines-server v1, DEFCON/files/agents bloques, sonde PID Windows OpenProcess |
