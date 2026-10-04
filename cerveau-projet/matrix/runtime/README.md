# Runtime Python embarque de la Matrice (3.14.8)

> Interpreteur Python **dans la Matrice** : la Matrice ne depend plus du
> Python installe sur la machine. Ce dossier est son runtime.

## Pourquoi un runtime embarque

La Matrice est un systeme de fichiers ET de programmes :669+ fichiers `.py` et
des routines de fond. Si elle s appuie sur le Python de l utilisateur (ici
`C:\Program Files\PyManager\python.exe`, alias de
`C:\Users\Optimus\AppData\Local\Programs\Python\Python314`), alors :

- **desinstaller** ou mettre a jour ce Python casse la Matrice, silencieusement ;
- la Matrice tourne sur une version qu elle n a pas choisie, et qu elle ne
  controle pas.

Le runtime embarque rend la Matrice **autonome** : elle embarque l interpreteur
qu elle a mesure, et elle declare lequel (cf. `V-004 interpreteur-python` dans
`matrice/data/classeur-variables.json`, consomme par
`matrice/data/commun/interpreteur.py`).

## Ce que contient ce dossier

Archive officielle python.org, version **embeddable** (12,6 Mo) :
`python-3.14.8-embed-amd64.zip`.

<!-- DEBUT-DECISION-MACHINE (lu par installer.py : version, URL, empreinte.
     Ne pas deplacer ni reformater ces lignes : c est le DOMICILE de la
     decision de version, et installer.py REFUSE s il ne les trouve plus.) -->

- Runtime Python embarque de la Matrice (3.14.8)
- Source officielle : https://www.python.org/ftp/python/3.14.8/python-3.14.8-embed-amd64.zip
- sha256 : a93abe456ab01bd96d7a085b3cdb6566b3063f4241360d114142fbdb07f0a310

<!-- FIN-DECISION-MACHINE -->

Ces trois lignes sont le SEUL endroit ou la version, l URL et l empreinte sont
ecrites. `installer.py` les LIT (jamais de recopie) : c est lui qui decide quoi
telecharger et quoi verifier.

| Fichier | Role |
|---|---|
| `python.exe` / `pythonw.exe` | lanceur |
| `python314.dll` / `python3.dll` | bibliotheque de l interpreteur |
| `python314.zip` | **toute la stdlib** (zippée) |
| `python314._pth` | configuration des chemins de recherche |
| `site-packages/sitecustomize.py` | **correction propre a la Matrice** (ci-dessous) |
| `*.pyd`, `*.dll` | extensions natives (`sqlite3`, `ssl`, `hashlib`, ...) |

**Choix : la version `embeddable`, pas l installeur `.exe`.** L installeur
ecrit dans le registre et `%APPDATA%`, donc il sort du perimetre de la Matrice et
reste un deuxieme domicile. L embeddable est **un dossier** : il se copie, se
supprime, se versionne. Le depot reste alors la seule maison.

## La correction : `site-packages/sitecustomize.py`

Le runtime embeddable a une particularite qui casse les briques de la Matrice :

1. il n ajoute **pas** le repertoire du script a `sys.path` ;
2. son `python314._pth` n accepte **que des chemins** — aucune ligne de code
   (`unsupported 'import' line in ._pth file`).

Or la Matrice lance ses briques par leur **nom** : le lanceur resout
`editer-agents-md` vers son `main.py`, et chaque brique fait
`from <verbe>.entry import ...` (`definir`, `verifier`, `etat`...).

**Mesure reelle (le trou n est visible qu a l usage) :**

| Epreuve | Resultat |
|---|---|
| compilation des 672 `.py` du depot | **672 OK / 0 KO** |
| `lancer.py --auto-test` | **13/13 VERDICT OK** |
| 1er appel d outil (`editer-agents-md verifier`) | **`ModuleNotFoundError: No module named 'definir'`** |

La compilation passe, le lanceur passe, et l outil casse. Seule l epreuve
d EXECUTION revelait le defaut.

Le correctif est donc `sitecustomize.py` (appele par `import site`, declare dans
le `_pth`) : il ajoute en tete de `sys.path` le repertoire du script puis le
repertoire courant. Il ne fait **rien d autre** — pas de variable, pas de
monkey-patch, pas d import de la Matrice (une dependance circulaire Python ->
Matrice -> Python serait la pire des corrections).

Apres correction :

| Epreuve | Resultat |
|---|---|
| `editer-agents-md verifier` | **OK** — empreinte `fe1111352...` |
| `selecteur-flux actuel` | **OK** — `FLUX ACTIF: FLUX2` |
| `lancer.py --appelant operateur editer-agents-md verifier` | **exit 0** |
| `registre-outils lister` | aide affichee, exit 2 (comportement correct) |

## Utilisation

```bash
# Au lieu de :
python3 cerveau-projet/matrix/lancer.py <porte> <verbe>
# Ecrire (chemin absolu) :
cerveau-projet/matrix/runtime/python.exe cerveau-projet/matrix/lancer.py <porte> <verbe>
```

## Mettre a jour le runtime

La version installee est **3.14.8** (stable au 2026-09-30). La machine hote
tourne en 3.14.4 : le runtime embarque est donc deja plus recent que le Python du
systeme — c est tout l interet.

Pour monter d une version : telecharger
`https://www.python.org/ftp/python/<VERSION>/python-<VERSION>-embed-amd64.zip`,
extraire par-dessus, puis **rejouer les deux corrections** (le `._pth` et le
`sitecustomize.py` ne viennent pas du zip pour le second) et repasser les epreuves
ci-dessus. La declaration reste au meme endroit : `V-004`.

## Ce que ce dossier n'est PAS

- **Pas un second domicile de la decision** : l interpreteur *utilise* est declare
  dans la BDD des variables (`V-004`), pas choisi ici. Ce dossier fournit le
  binaire ; la BDD porte le choix.
- **Pas un binaire versionne** : `runtime/` est ignore par git (voir `.gitignore`).
  Il se reinstalle par l archive officielle, dont l URL et la version sont
  inscrites ici — le depot reste un depot de sources.