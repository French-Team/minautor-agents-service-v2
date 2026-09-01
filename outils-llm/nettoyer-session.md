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

Le mode zero-total ne laisse aucune trace dans l historique qu il vient de
vider. Le prochain demarrage produit les premieres nouvelles traces.
