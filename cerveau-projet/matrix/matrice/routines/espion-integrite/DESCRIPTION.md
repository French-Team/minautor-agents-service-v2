# OUTIL -- espion-integrite

> Routine espion de la Matrice : surveille l'INTEGRITE DE TOUTES LES BDD,
> a intervalle regulier. Mode tour (une passe, retour au shell) ou mode boucle
> (veille en arriere-plan, arret propre).

## Options

```
python main.py tour
python main.py boucle [--interval <secondes>]
python main.py boucle arret
```

- `tour` : une passe de surveillance (Chapitre 1 : integrite, Chapitre 2 : presence),
  journalise dans espion-log.jsonl et rend la main.
- `boucle` : tourne en arriere-plan, passe toutes les N secondes (defaut : 300),
  note son PID dans espion.pid, refuse un second lancement (zero double espion).
- `boucle arret` : pose un drapeau d'arret -- la boucle s'arrete ELLE-MEME apres
  sa passe en cours (arret cooperatif : zero processus tue, zero fantome).

## Regles respectees

- Registre des 7 BDD dans constants.py (zero valeur en dur dans la logique).
- Une BDD a-construire = INFO (presente ou pas), jamais une fausse alerte.
- Une BDD faite avec empreinte fausse = ECART (code de sortie 1).
- Journal en ajout seul (espion-log.jsonl), une ligne par passe.
- Protections ouverture/fermeture propres (regles-immuables/python-seul.md).

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| DESCRIPTION.md | la facade (ce fichier) |
| main.py | point d'entree global : DIRIGE |
| constants.py | registre des 7 BDD, valeurs de la boucle |
| commun.py | fonctions communes : empreinte, journal, PID |
| tour/ | passe de surveillance (entry + fonctions) |
| boucle/ | veille en arriere-plan + arret propre (entry + fonctions) |
