# OUTIL -- suivi-optimus

> Outil Python dedie a la trace `data/suivi-optimus.jsonl` (M-084, GO createur).
> La trace note L'AGENT (optimus-prime), jamais les outils : decisions, portes,
> missions -- le POURQUOI. Le sac-a-dos note les OUTILS (invocations, codes,
> durees) : les deux ne se recouvrent pas.

## Options

```
python3 cerveau-projet/matrix/lancer.py suivi-optimus noter --mission MO-XXX --theme SUIVI --action <action> --detail "..." (Optimus : MO- ; M- = cameleon)
                     [--fichiers "a,b"] [--portes "a,b"] [--duree-s N]
python3 cerveau-projet/matrix/lancer.py suivi-optimus lire [--mission M] [--action <action>] [--n N]
python3 cerveau-projet/matrix/lancer.py suivi-optimus verifier
python3 cerveau-projet/matrix/lancer.py suivi-optimus coherence [--racine <matrix>] (croise la file du pilote et le journal)
python3 cerveau-projet/matrix/lancer.py suivi-optimus archiver [--racine <matrix>] [--doublons] (sort du journal les hors
                                               perimetre OPTIMUS, en les ARCHIVANT)
python3 cerveau-projet/matrix/lancer.py suivi-optimus corriger [--mission MO-XXX] --motif "..." [--simuler oui] [--racine <matrix>]
                                               (corrige EN PLACE une duree_s DECLAREE qui CONTREDIT la mesure des
                                               bornes ; la valeur honnete est VIDE, l'ancienne reste relisible
                                               dans `corrections`)
python3 cerveau-projet/matrix/lancer.py suivi-optimus vue (genere la vue markdown dediee _operateur/optimus-prime/suivi-optimus.md)
```

- `--action` : action fermee (enum, voir constants.py) -- obligatoire.
- `--detail` : le contenu de l'evenement (obligatoire).
- `--mission` / `--theme` : contexte de la mission (facultatif).
- `--fichiers` / `--portes` : listes separees par des virgules (facultatif).
- `--duree-s` : duree en secondes (facultatif).
- **DEUX BORNES IDENTIQUES = DUREE INCONNUE** (decision createur du 2026-09-21) : le
  recap affiche `inconnue`, jamais `0`. Mesure : 59 missions portent un `debut` a la
  seconde exacte de leur `fin` -- un debut POSE APRES COUP par le garde
  anti-fin-orphelin, pas une mission de zero seconde. Un zero seconde n'est pas une
  mesure : c'est un artefact, et il se lisait comme un fait (L-055).
- `lire --n N` : les N derniers evenements (tous si absent).
- `coherence` : croise les DEUX traces d'optimus -- la FILE DU PILOTE
  (`_operateur/optimus-prime/pilote/file-missions-optimus.json`, + son archive)
  et CE JOURNAL. Ecart = divergence a reparer (code 1) ; dette = etat transitoire
  legitime ou residu hors perimetre (signale, code 0). `--racine <matrix>` cible
  un autre arbre (sert aux cobayes).

- `corriger` : corrige EN PLACE une **duree_s DECLAREE** qui CONTREDIT la mesure des bornes (EO-269, decision operateur du 2026-09-19). Le journal est en AJOUT SEUL : on ne supprime rien, on corrige, donc la date, l'action et le detail SURVIVENT. L'ancienne valeur est GARDEE DANS l'entree (`corrections` : date, motif, duree_s_avant, duree_s_apres, mesure). La VALEUR HONNETE EST VIDE, PAS LA DUREE MESUREE : le pilote n'a pas mesure, c'est la VUE qui calcule. `--simuler oui` montre sans ecrire ; `--racine <matrix>` cible un cobaye.

## Ce que `coherence` attrape (et pourquoi il existe)

Le pilote ecrit la FILE ; c'est l'AGENT qui declare au JOURNAL (marbre L-020 :
le pilote ne note RIEN). Deux traces separees ne se comparent pas toutes seules :

| Fautes (ECART, bloquant) | Cas reel |
|---|---|
| terminee dans la file, SANS fin au journal | MO-043 restee `en-cours` 40 min apres sa fin declaree |
| fin au journal, mais pas terminee dans la file | -- |
| declaree commencee au journal, mais `en-attente` dans la file | -- |
| declaree au journal, INCONNUE de la file (ni active, ni archivee) | MO-045/MO-046 menees hors file |
| plus d'une mission en cours (serie stricte) | -- |
| compteur du pilote en retard sur le plus grand id utilise | compteur 44 alors que MO-045 et MO-046 existaient : la charge suivante aurait repris MO-045 |

| Dettes (signalees, non bloquantes) |
|---|
| `en-cours` dans la file sans debut au journal (fenetre d'injection, ou declaration oubliee) |
| identifiants hors perimetre au journal (prefixe autre que MO-, residus du cameleon) |

Un ECART est une divergence entre les deux traces ; une dette ne bloque pas le
flux (on ne bloque pas une chaine parce qu'un agent est en train de declarer).

## Actions fermees (declencheurs d'entree)

| Action | Declencheur |
|---|---|
| `debut` | debut de mission |
| `fin` | fin de mission avec bilan |
| `porte` | porte officielle utilisee (pilote, lot, tresse, defcon, pause/reprise) |
| `depot` | mission deposee au vrac de l'entonnoir (E-XXX) |
| `decision` | GO / arbitrage du createur |
| `decouverte` | constat d'audit interne (ex : angle mort detecte) |
| `intervention` | INTERVENTION du createur sur la mission EN COURS (crochet `[si]`, 2026-09-21) : mini-reflexion de remise en question, tenue pendant le round et morte avec lui. Le mot vit dans la liste fermee `CROCHETS` du pilote (`filtrer/entry.py`) ; c'est le routeur qui pose cette ligne, sur la mission COURANTE -- et il DIT quand il n'y a aucune mission ou la poser. |
| `bilan` | bilan-periode demande et rendu |

PAS d'entree par fichier edite : bdd-modifications couvre ce niveau (doublon interdit).

## Format de la BDD

Une ligne JSON par evenement (journal en AJOUT SEUL, jamais reecrit) :
`{"date", "mission", "theme", "action", "detail", "fichiers[]", "portes[]", "duree_s"}`
Plus un etalon `suivi-optimus.jsonl.sha256` (empreinte recalculee a chaque ajout).

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| DESCRIPTION.md | la facade (ce fichier) |
| main.py | point d'entree global : DIRIGE |
| constants.py | chemins, enum fermee des actions |
| commun.py | fonctions communes : lire, ajouter (atomique, LF), empreinte, options |
| noter/ | noter un evenement (action fermee) |
| lire/ | lister (tout ou par mission/action, n derniers) |
| vue/ | generer la vue markdown dediee (_operateur/optimus-prime/suivi-optimus.md) |
| verifier/ | integrite SHA-256 (etalon-or) |
| coherence/ | croiser la file du pilote et le journal (verbe `coherence`) |
| archiver/ | sortir du journal actif ce qui ne doit pas y etre : evenements HORS PERIMETRE, ou DOUBLONS debut/fin (verbe `archiver`, option `--doublons`) |
| corriger/ | corriger EN PLACE une declaration qui CONTREDIT la mesure (verbe `corriger`, champ `duree_s`) |

## Ce que fait `archiver` (et pourquoi il existe)

Le journal est la trace d'OPTMUS ; il a recemporte le 2026-09-12 les missions du
CAMELEON (M-XXX) et des libelles d'entonnoir (`E-089`, `AUDIT-NEMESIS`) : **184
evenements hors perimetre** qui faussaient la vue et le croisement file <-> journal.

On ne SUPPRIME pas : on **ARCHIVE** dans `suivi-optimus-hors-perimetre.jsonl`
(append), le journal actif est reecrit sans eux et l'empreinte SHA-256 est
recalculee. Meme discipline que MO-023 (fins orphelines archivees) et MO-029
(rotation avec plafond).

Ordre de securite : **archiver d'abord, reecrire ensuite, resceller en dernier**.
Si l'archive echoue, le journal n'est pas touche ; si la reecriture echoue,
l'archive contient deja tout. Deuxieme passage = < rien a archiver > (idempotent).

### `--doublons` : reparer un ECART de `verifier` (2026-09-13)

Une mission a **UN debut et UNE fin** : `verifier` remonte tout autre compte en
ECART. Le 2026-09-13, le verbe `enregistrer` du pilote a **double MO-061**
(2 debuts, 2 fins) en notant un debut qui existait deja -- `verifier` le criait,
mais aucun verbe ne savait reparer, donc l'ecart restait.

`archiver --doublons` sort du journal les 2e debut / 2e fin de la MEME mission et
les **ARCHIVE** dans `suivi-optimus-doublons.jsonl` (jamais de suppression).
**Le premier evenement fait foi** : c'est le fait d'origine, le suivant est la
copie accidentelle. Les autres actions (`porte`, `depot`, `decision`,
`decouverte`, `bilan`) se repetent legitimement et ne sont jamais touchees.

## Ce que fait `corriger` (et pourquoi il existe)

Decision operateur du 2026-09-19 (suite d'EO-267/EO-268) : le pilote declarait
`duree_s = 0` a chaque cloture -- un PLACEHOLDER, jamais une mesure. EO-267 a
repare la SOURCE (la vue CALCULE la duree des deux bornes) ; il restait
l'HISTOIRE : 146 ecarts mesures par `verifier-placeholders` dans le journal, et
AUCUNE porte pour les corriger. Une duree fausse se lit comme un fait (L-055) :
le mensonge etait dans la DONNEE, pas dans l'affichage.

`corriger` ne fait qu'UNE chose, et il ne la devine jamais : un evenement qui
DECLARE une duree NON VIDE differente de la mesure des bornes de SA mission est
corrige EN PLACE (date, action et detail conserves ; ancienne valeur GARDEE dans
`corrections`). Tout le reste est laisse INTACT :

| Cas | Verdict |
|---|---|
| declaration egale a la mesure (zero legitime compris) | FAIT -- jamais touchee |
| valeur vide (silence) | pas une declaration -- jamais accusee |
| mission sans les deux bornes | aucune mesure possible -- laissee intacte |
| ligne illisible au journal | REFUS, journal INTACT (aucune ligne perdue) |
| mission inconnue, ou `--motif` absent | REFUS, aucune ecriture |

Ordonnancement : mesurer, refuser si une ligne serait perdue, reecrire (atomique),
resceller l'empreinte. Deuxieme passage = < rien a corriger > (idempotent). Mesure
du 2026-09-20 : 377 declarations corrigees, 866 -> 866 lignes, et le garde
`verifier-placeholders` repasse de 146 ecarts a 0.

## Protections

- Journal append-only : ajout atomique (tmp + remplacement), LF forcees.
- Empreinte SHA-256 recalculee A CHAQUE ajout, etalon surveille par l'espion.
- Action fermee : toute action hors enum refusee (code 2).
- Etancheite : le cameleon n'accede JAMAIS a cette trace (zone exclue de son perimetre).
