---
identite:
  type: outil
  appartient_a: matrice
  commun: true
  version: 1
  date: 2026-09-23
  liens: matrice/templates/routine/README.md, matrice/data/outils/dupliquer-template/DESCRIPTION.md, matrice/data/manuel-outils.md
---

# OUTIL -- ecrire -- porte unique d ecriture, atomique et reversible

> Porte unique d'ecriture (MO-002). Remplace `write_file` + `str_replace` natifs (non atomiques, LF non forces, pas de .bak, pas de validation) par une porte atomique, verifiee, reversible.

## Verbes

```
python3 cerveau-projet/matrix/lancer.py ecrire ecrire --fichier <chemin> --contenu "<texte|@fichier>" [--mode creer|remplacer|ajouter]
python3 cerveau-projet/matrix/lancer.py ecrire ecrire --fichier <chemin> --contenu-fichier <chemin-source> [--mode creer|remplacer|ajouter]
python3 cerveau-projet/matrix/lancer.py ecrire ecrire --fichier <chemin> --contenu-base64 <blob> [--mode creer|remplacer|ajouter]
python3 cerveau-projet/matrix/lancer.py ecrire editer --fichier <chemin> --ancien "<old|@fichier>" --nouveau "<new|@fichier>"
python3 cerveau-projet/matrix/lancer.py ecrire editer --fichier <chemin> --ancien-fichier <chemin> --nouveau-fichier <chemin>
python3 cerveau-projet/matrix/lancer.py ecrire editer --fichier <chemin> --ancien-base64 <blob> --nouveau-base64 <blob>
```

- `--fichier` : cible (relatif a la racine, detectee par `data/commun/racine.py`).
- `--contenu` : texte direct, ou `@chemin` (anti-heredoc, lecture du fichier source).
- `--contenu-fichier` : alias lecture fichier source (meme effet que `--contenu @...`).
- `--contenu-base64` : **transport SANS echappement (MO-173)** -- le blob ne porte ni guillemet, ni antislash, ni saut de ligne : aucune couche traversee (heredoc, shell, litteral) ne peut le deformer. Lecture STRICTE (`validate=True`), refus NOMME si le blob est invalide ou n est pas de l UTF-8. **Les trois sources de contenu sont EXCLUSIVES** et seule leur PRESENCE compte : une source videe est REFUSEE (ecrire un fichier vide est une intention, pas un oubli).
- `--mode` : `creer` (refuse si existe), `remplacer` (defaut), `ajouter` (concatene).
- `--ancien` / `--nouveau` : chaines exactes (1 occurrence unique imposee, comme `str_replace` mais validee).
- `--ancien-base64` / `--nouveau-base64` : **transport SANS echappement de CHAQUE texte (MO-376)** -- meme garantie que `--contenu-base64` (blob STRICT, refus NOMME si invalide ou non-UTF8). **UN SEUL transport par cote** : `--ancien`, `--ancien-fichier`, `--ancien-base64` sont EXCLUSIFS (code 2, le refus NOMME les options en presence). Le bit-exact est alors GARANTI : aucun `@fichier` n est relu, un NOUVEAU qui COMMENCE par `@` est ecrit TEL QUEL -- les fichiers OLD/NEW deviennent inutiles.

- **Extrait a DEUX formes (MO-173)** : `ecrire` force un LF final (L-001), donc un extrait de MILIEU de ligne ecrit par la porte ne pouvait JAMAIS correspondre. `editer` essaie la forme EXACTE, puis la forme SANS son LF final, et DIT laquelle a servi ; si la forme retenue a perdu le LF, le NOUVEAU le perd aussi (symetrie -- sinon l edition injecterait un saut de ligne DANS la ligne).
- **Rien apres la publication (MO-173)** : le compte-rendu est construit AVANT `os.replace` ; apres la publication il ne reste que le SHA et le retour. Une porte qui ecrit PUIS crie annonce un faux echec (mesure : un NameError declenche apres l ecriture).
- `--ancien-fichier` / `--nouveau-fichier` : variantes fichier pour gros blocs.
- **Valeur a tirets (EO-156)** : une valeur peut commencer par `--` -- un document a carte d'identite COMMENCE par `---` : la carte s'ecrit donc en UNE passe. Le morceau suivant n'est pris pour une option que s'il est un NOM connu (`--contenu`). Seule limite : une valeur qui serait exactement un nom d'option connu (ex. `--mode`) passe par `@fichier`.

## Preparer la paire ancien/nouveau (module fragment)

> Une recopie A LA MAIN d un fragment existant a fait entrer un bloc AUTRE que le
> fichier (MO-207 : refuse a l edition, et `py_compile` ne l a pas vu), des
> guillemets non-ASCII (MO-206) et un texte modifie par le shell (EO-192 : des
> accents graves EXECUTES). Le module PARTAGE `matrice/data/commun/fragment.py`
> compose la paire : la donnee vient du FICHIER, l unicite est PROUVEE, l ASCII
> est mesure AVANT, et rien ne passe par la ligne de commande -- la commande ne
> porte que des CHEMINS.

| Verbe | Commande |
|---|---|
| `extraire` | `python3 cerveau-projet/matrix/matrice/data/commun/fragment.py extraire --fichier <cible> ( --lignes a,b \| --ancre <texte> ) --sortie <fichier>` |
| `verifier` | `python3 cerveau-projet/matrix/matrice/data/commun/fragment.py verifier --fichier <cible> ( --fragment <fichier> \| --ancre <texte> )` |
| `poser` | `python3 cerveau-projet/matrix/matrice/data/commun/fragment.py poser --fichier <cible> --fragment <fichier> --nouveau <fichier> [--dossier <zone>]` |

- `--lignes a,b` : EXACT, bloc CONTIGU (1-based, bornes INCLUSES) ;
- `--ancre <texte>` : resiste au DEPLACEMENT ; elle doit etre UNIQUE, sinon le
  refus NOMME les lignes candidates ;
- `--sortie` est EXIGEE : le fragment va dans un FICHIER, jamais dans un
  affichage (un affichage n est PAS le fichier -- c est la panne MO-207).

`poser` ne fait que PREPARER : il ecrit la paire dans la zone jetable et REND la
commande `editer` a copier. La POSE (backup, empreinte, BDD, garde, validation)
reste a CETTE porte -- une seule maison par geste. Le module est PARTAGE (pas de
`main.py`) : le lanceur ne resout que les outils et les routines, donc il s
invoque PAR SON CHEMIN, et c est DIT ici. Dettes nommees par le GO : les octets
atomiques (I-02 `fichier.py`) et l ASCII vu avant (I-05 `texte.py`) vivent dans le
module jusqu a la naissance de ces deux modules.

## Garanties (pourquoi meilleur que le natif)

| Natif | ecrire (ameliore) |
|---|---|
| Ecriture directe non atomique | **tmp+replace** (`os.replace`) : jamais de fichier a moitie ecrit |
| LF non forces (L-001) | **LF forces** (`newline="\n"`, normalise CRLF/CR) |
| Pas de .bak (pas de revert proto-2) | **.bak horodate** si fichier existait (revert possible) -- pose AVANT la publication, JAMAIS pour une ecriture REFUSEE : un refus ne laisse aucun point derriere lui (MO-286) |
| Pas de SHA | **SHA-256 avant/apres** annonce (preuve disque) |
| Pas de validation syntaxe | **py_compile** (.py) et **json** (.json) VALIDES AVANT publication : un contenu invalide est REFUSE (code 1) et la cible reste INTACTE (EO-129) ; un `.py` qui AVERTIT (echappement INVALIDE, ce que py_compile ne dit pas) est REFUSE de meme, ligne et REMEDE nommes (MO-286) |
| Hors perimetre possible | **Refuse hors de la Matrice, chemin RESOLU d abord** (sauf allowlist `AGENTS.md`/`demarrer-*.md`), code 2, refus qui NOMME la Matrice (MO-183/EO-177) |
| str_replace fragile whitespace | **Occurrence unique imposee** (0 ou >1 = REFUS (code 2), message explicite) |
| Pas d'ASCII | **ASCII CORRIGE, puis refuse** (MO-210) : ce que la carte commune sait convertir est corrige AVANT l ecriture et DIT ; ce qu elle IGNORE = **REFUS (code 2)**, RIEN n est ecrit, caractere et ligne NOMMES |
| Heredoc casse | **@file** (anti-heredoc) |
| Zone des sources du createur (`docs/`, MO-377) | **REFUS NOMME** : la zone est **LECTURE SEULE**, la porte n y publie JAMAIS et le refus dit POURQUOI et les TROIS remedes reels (git pour un source suivie, le createur pour une source VIVANTE, un document NET ecrit A COTE). Le remede de la carte ASCII ne s applique PAS ici : il **mutilerait** la source |
| Deux textes hostiles a EDITER (MO-376) | **`--ancien-base64` / `--nouveau-base64`** : le transport sans echappement de `--contenu-base64`, applique aux DEUX textes de `editer` -- **UN SEUL transport par cote** (`--ancien`, `--ancien-fichier`, `--ancien-base64` EXCLUSIFS, refus code 2) et bit-exact de bout en bout : un NOUVEAU qui COMMENCE par `@` est ecrit TEL QUEL (aucune relecture comme chemin). Epreuve : le MEME geste par la coquille est MANGE (l accent grave s execute, le dollar se substitue) et le NOUVEAU n arrive pas |
| Contenu hostile au transport (antislash, triples guillemets imbriques) | **`--contenu-base64`** (MO-173) : le blob traverse la chaine sans qu aucune couche puisse le deformer. Epreuve : le MEME contenu, en brut, arrive CORROMPU (l antislash consomme) ; en base64 il est **BIT-EXACT** |
| ImportError invisible a la compilation | **Garde d ORDRE** (EO-159) : un import LOCAL dont le nom n est pas lie par le module fournisseur est REFUSE avant publication -- `py_compile` ne dit rien d un ImportError (mesure MO-169 : la porte est morte de son propre contenu) |

## Architecture

| Piece | Role |
|---|---|
| `main.py` | DIRIGE (parser, router) |
| `constants.py` | chemins, suffixes, modes, allowlist |
| `commun.py` | fonctions communes : perimetre, SHA, LF, .bak, validation, atomique |
| `ecrire/` | categorie ecrire : `entry.py` orchestre, `fonctions.py` fait |
| `editer/` | categorie editer : `entry.py` orchestre, `fonctions.py` fait |

## Protections

- Perimetre : le chemin RESOLU doit tomber DANS la Matrice (allowlist racine : `AGENTS.md`, `demarrer-*.md`) -- hors perimetre = code 2, refus NOMME. La forme `matrix/...` n est acceptee que si la Matrice vit sous la racine ; dans ce depot la Matrice vit sous `cerveau-projet/`, donc la forme correcte est `cerveau-projet/matrix/...` (MO-183/EO-177 : juger un PREFIXE avant la resolution a fait ecrire la porte HORS de la Matrice, arborescence parasite creee).
- Mode ferme (`creer|remplacer|ajouter`) -- inconnu = code 2.
- `creer` refuse si existe (code 2).
- Option PRIVEE de valeur = **REFUS nomme** (code 2, `REFUS : option --X sans valeur`) : le parseur n'ecrit plus `""` en silence -- une option videe en silence se lit "pas de contenu" et accuse a tort l'appelant (EO-156).
- `editer` : 0 occurrence = code 2, >1 = code 2 (unique).
- **ASCII avant publication (MO-210)** : les DEUX verbes passent par `corriger_contenu` AVANT la publication. Trois sorties : (1) rien a corriger, silence ; (2) non-ASCII couverts par la carte, corriges et DITS (`[ASCII] CORRIGE : n caractere(s) en lignes ...`) ; (3) non-ASCII HORS carte, **REFUS (code 2), RIEN n est ecrit**, avec le caractere et sa ligne (`\xB0 (U+00B0)` pour le degre) et le remede. La carte vit au **domicile unique** `matrice/data/commun/carte_ascii.py` : deux consommateurs (cette porte et le scan `corriger-ascii`), une seule carte -- recopiee, elle aurait ete deux verites (l une corrigeant ce que l autre ignorait). Le message est 100% ASCII : un caractere brut sortait en cp1252 et cassait tout appelant qui capture la sortie (mesure du cobaye MO-210).
- Validation : `.py` via `py_compile`, `.json` via `json.load`, faite sur le TEMPORAIRE **AVANT** le remplacement. Echec = code 1, RIEN n'est ecrit, la cible est INTACTE (EO-129 : avant, la porte publiait d'abord et un fichier invalide restait en place).
- Ecriture atomique : `tmp`, VALIDATION, puis `os.replace`, LF forces (le temporaire est retire si le contenu est refuse).

## Zone des sources du createur : `docs/` (MO-377)

`docs/` (a la racine de la Matrice) est la ZONE DES SOURCES du createur -- vision,
transcriptions, notes -- declaree **LECTURE SEULE** par la regle
`_operateur/optimus-prime/regles-immuables/ascii-strict.md`, ou les banks de lecture
externe sont declarees INTACTES, jamais modifiees, jamais traduites (`docs/docs-readme.md`).

DECISION (MO-377, mesure du 2026-09-24) : la Matrice n ECRIT JAMAIS dans cette zone et
cette porte le REFUSE en le DISANT. Le refus est DOUBLE, A DESSEIN : AVANT la correction
ASCII (donc le message ne propose plus d ajouter le caractere a la carte ASCII -- suivre
ce remede aurait MUTILE la source, defaut mesure) ET dans le passage oblige
(`ecrire_atomique` / `editer_atomique`), pour qu aucun appelant ne puisse l oublier.

Le refus NOMME la zone, la regle qui fait foi et les TROIS remedes reels : git pour un
source suivie par git, le createur pour une source VIVANTE (`IMPERATIF.md`), un document
NET ecrit A COTE pour ce que la Matrice doit produire.

La zone est designee par sa POSITION -- le PREMIER segment du chemin, relatif a la racine
de la Matrice : `docs/...` est la zone des sources, `matrice/docs/...` est la
documentation INTERNE de la Matrice et reste ecrite par elle. Le domicile unique de cette
declaration est `matrice/data/commun/zone_sources.py` (M-076) : la presente porte, le
garde `garde-ascii` et le scan `corriger-ascii` y lisent la MEME zone.

## Secours (EO-159)

Un garde ne suffit pas : si la porte est cassee MALGRE le garde, plus AUCUNE
ecriture n est possible -- toute ecriture du perimetre passe par elle (mesure
MO-169 : un import pose avant sa constante a rendu la porte injouable).

- **Prevention** : le garde d ORDRE refuse d ecrire un `.py` qui consomme un nom
  absent de son fournisseur local. La porte ne peut plus mourir de son propre
  contenu, et le geste fautif est DIT (jamais silencieux).
- **Cure** : le POINT DE RESTAURATION `.bak` horodate, laisse par la porte a
  chaque ecriture, EST la porte de secours. `revert-fichier.py`
  (`_operateur/optimus-prime/super-combos/combos/outils/`) rend un fichier a sa
  version d avant DEPUIS ce `.bak` -- et il ecrit SANS la porte, expres : il sert
  quand la porte est la chose cassee. Limites DITES : aucune validation, aucun
  SHA, la version courante n est pas sauvee. Mesure MO-170 : les 10 controles du
  cobaye passent, secours compris.

## Benchmark (critere GO MO-002)

- 1000 lignes : <30ms ecriture.
- Serie stricte, zero fantome.
