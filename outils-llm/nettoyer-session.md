# nettoyer-session.py

## Utilisation

Nettoyage normal :

```bash
python3 outils-llm/nettoyer-session.py glm5 admin
```

Zero total session-admin :

```bash
python3 outils-llm/nettoyer-session.py glm5 admin --zero-total
```

## Mode `--zero-total`

Le mode zero-total purge les donnees runtime de `session-admin` :

- `AGENTS-historique.md` et `AGENTS-activite-recente.md` ;
- inbox et outbox Oracle v1 ;
- etats de cartes Oracle ;
- etat d execution des routines et donnees de routines ;
- PID files des serveurs v1 ;
- marqueur d inactivite session-admin.

Les dossiers necessaires sont recrees vides apres la purge.

Le mode ne supprime pas :

- `AGENTS.md` ;
- les fiches et corrections des agents ;
- les arbres et parcours ;
- le manifest des routines ;
- les configurations Oracle ;
- le classeur de variables permanent.

Le classeur reste volontairement preserve : il contient la configuration
structurelle de la session. Le retour a Cerberus est ensuite effectue par
`activer-agent-principal`, afin de conserver la coherence des trois sources.

Avant de vider les donnees, `--zero-total` cree une sauvegarde horodatee :

```text
backup-AAAAMMJJ-HHMMSS-session-admin/
```

Cette sauvegarde contient les files (`asap.jsonl`, `normale.jsonl`,
`plus-tard.jsonl`), les inbox/outbox, les historiques, les etats runtime et
le classeur. Un `manifest.json` indique la session, la date et le nombre de
fichiers sauvegardes.

Apres la sauvegarde, les trois files sont explicitement recreees vides :
`asap.jsonl`, `normale.jsonl` et `plus-tard.jsonl`. Le prochain demarrage
produit les premieres nouvelles traces sans recharger les anciennes missions.

Le mode `--dry-run` affiche la sauvegarde et le vidage prevus sans modifier
aucun fichier.
