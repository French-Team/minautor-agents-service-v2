# ROUTINE veille-flux

> Routine de la Matrice (M-012, doctrine du createur) : surveille les fichiers
> modifies et sauvegardes, declenche les combos de verification/correction en
> ARRIERE-PLAN, sans interrompre le travail du LLM.

## Deux etats possibles

| Etat | Commande | Ce qui tourne |
|---|---|---|
| RELAX (defaut) | `python main.py veille` | corriger-ascii (scan+correction) + py_compile global |
| VIGILE (apres modifications) | `python main.py veille --vigile` | RELAX + les 3 verifier-marbre + verifications cibles |

## Ce que fait chaque passe

1. Purge des morts (M-051/M-052) : les signatures `python-compile` dont la
   cible n'existe plus sont retirees de `alertes-emises.json` (une signature
   morte bloquerait la future alerte si la cible etait recreee) ET les
   alertes-grave fantomes de la boite Matrice (`intercom/matrice/inbox.jsonl`)
   sont retirees (fichier cible supprime = incident resolu). Les cibles
   non-fichier (comme l'etiquette `py_compile`) ne sont JAMAIS declarees
   mortes. Les autres messages de la boite (fin-mission, retour-lot,
   incident...) sont INTOUCHABLES. Jamais bloquant (incident journalise),
   resultats dans le journal (`purge-signatures`, `purge-boite`).
2. corriger-ascii : scan + correction auto (BDD empreintees intouchables,
   caracteres inconnus laisses et signales = probleme plus grave).
3. py_compile global (syntaxe Python cassee = probleme plus grave).
4. [VIGILE seulement] verifier-conventions / -regles / -protocoles +
   verification des cibles de la Matrice (DESCRIPTION.md, main.py, entry.py,
   fonctions.py des outils et routines ; DESCRIPTION + main du pilote).

## Etats de sortie (definition stricte)

- `RELAX` : aucune detection. Sortie 0.
- `VIGILE` : au moins une detection. Sortie 1.
- Chaque passe ecrit une ligne dans le journal (ajout seul).
- Etat VIGILE = retour RELAX : la re-veille a RESTAURE le probleme
  (correction/reparation) et la passe s'est terminee proprement.

## Problemes graves (PAS d'auto-correction -> alerte intercom)

- Caractere non convertible laisse en place.
- Fichier Python qui ne compile pas.
- Ecart de marbre (conventions/regles/protocoles) en mode VIGILE.

Grave -> message dans `matrice/intercom/matrice/inbox.jsonl` (type
`alerte-grave`, avec fichier et raison) -> la Matrice peut redonner une
mission via le pilote.

## Arriere-plan et arret cooperatif

    python main.py veille            (une passe)
    python main.py veille --boucle   (surveillance continue, refus de double lancement via PID)
    python main.py veille --boucle --vigile
    python main.py veille arret      (drapeau d'arret cooperatif, zero processus tue)

## Frontiere absolue

- Un fichier sous etalon .sha256 n'est JAMAIS reecrit.
- L'histoire (.jsonl) n'est jamais reecrite.
- La reparation d'un probleme grave reste une MISSION, jamais une routine silencieuse.
