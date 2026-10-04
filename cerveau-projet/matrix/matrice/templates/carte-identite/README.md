---
identite:
  type: readme
  appartient_a: matrice
  commun: true
  version: 1
  date: 2026-09-23
  liens: matrice/data/commun/carte_identite.py, matrice/data/commun/cible.py, matrice/data/outils/rechercher/DESCRIPTION.md, matrice/routines/verifier-liens-cartes/DESCRIPTION.md, _operateur/optimus-prime/super-combos/combos/outils/verifier-cartes-identite.py, matrice/templates/carte-identite/INVENTAIRE-CLES.md, matrice/data/outils/carte-comparer/DESCRIPTION.md
---

# MODELE -- carte d identite (le front-matter qui rend un document TROUVABLE)

## LE MODELE EN 4 PIECES (les quatre fichiers de ce dossier)

| piece | role |
|---|---|
| `README.md` | ce document : le POURQUOI du modele, les cles, les pieges mesures, l usage par le moteur |
| `carte.modele` | le squelette MINIMAL a copier (l essentiel pour commencer) |
| `carte-complete.modele` | la carte TRES detaillee : les 3 cles obligatoires commentees, les cles libres mesurees, la cle `liens` et ses 5 regles |
| `INVENTAIRE-CLES.md` | la MESURE du modele : l inventaire reel des cles sur 14 cartes, les 3 pieges mesures, ce que le moteur sait chercher |

> Un modele que nul document ne nomme est un modele invisible : les quatre pieces
> ci-dessus sont nommees ici, et deux d entre elles portent une carte que le moteur
> retrouve (`--champ "type=readme"`).

> Ce dossier n est PAS un moule a jetons : `dupliquer-template` sert des OUTILS et
> des ROUTINES, pas des cartes. C est le MODELE de reference d une carte.
> La GRAMMAIRE vit dans `matrice/data/commun/carte_identite.py` (domicile unique),
> la FORME des chemins de la Matrice dans `matrice/data/commun/cible.py`, le garde
> `verifier-cartes-identite.py` juge la conformite, et le moteur
> `rechercher --champ` retrouve les documents PAR leur carte.

## La SUITE d outils qui sert ce modele (MO-430)

Le modele donne les CHAMPS ; quatre outils les POSSENT, les CHANGENT et les
MESURENT. Fiches dans `matrice/data/manuel-outils.md` (sections 37 a 40) :

| outil | ce qu il fait |
|---|---|
| `matrice/data/outils/carte-creer/` | pose la carte d un document qui n en a pas (modele complet ou minimal) |
| `matrice/data/outils/carte-editer/` | remplace la carte ENTIERE par un nouveau bloc |
| `matrice/data/outils/carte-modifier/` | change UN champ (remplacer, inserer ou retirer) |
| `matrice/data/outils/carte-comparer/` | dit si les champs du modele sont PRESENTS et si la carte est CONFORME |

Toute ecriture passe PAR LA PORTE `ecrire` (decision createur MO-430) :
fragments puis cible, donc validation, point de restauration et refus a
occurrence unique. `carte-comparer` est le seul des quatre en LECTURE SEULE --
c est lui qui repond a la question "je suis conforme ?", face a CE modele.
Le combo `c-008-cartes` (CV-008) rend l inventaire du corpus sur la meme
reference.

## Pourquoi ce modele existe (mesure du 2026-09-23)

167 documents sous `matrix/`, **113 portent une carte**, et **ZERO n utilise la cle
`liens`** : le mecanisme existait deja (EO-347), personne ne s en servait. Une carte
SANS `liens` est normale (tout document n a pas de voisin) -- mais un corpus qui ne
declare aucun lien ne permet pas de retrouver les fichiers CONNECTES a celui qu on
doit modifier. Ce modele rend la ligne uniforme ; la routine
`verifier-liens-cartes` mesure ce qu elle vaut.

## La forme : front-matter en TETE du document, entre deux `---`

```text
---
identite:
  type: outil
  appartient_a: optimus-prime
  commun: false
  version: 1
  date: 2026-09-23
  liens: matrice/data/commun/carte_identite.py, matrice/data/commun/cible.py
---
```

## Les cles

| cle | obligatoire | ce qu elle dit |
|---|---|---|
| `type` | OUI | nature du document, VOCABULAIRE FERME (18 types reconnus) -- un type neuf se DECLARE dans le domicile, il ne s invente pas |
| `appartient_a` | OUI | a qui le document appartient : un NOM, jamais un chemin |
| `commun` | OUI | `true` si le document est commun aux deux sessions |
| `liens` | NON | les documents CONNECTES : chemins canoniques, separes par des virgules |
| `version`, `statut`, `date`, `tags`, ... | NON | cles LIBRES -- c est le CORPUS qui detecte une faute de frappe (une cle qu aucune carte ne porte) |
| `gravite` | NON | le DEGRE D IMPORTANCE, VOCABULAIRE FERME : `tres-urgent`, `urgent`, `important`, `normal`, `optionnel` (EO-457) |
| `niveau` | NON | l entier 1-10 qui RAFFINE la gravite DANS sa bande ; plus haut = plus important (EO-457) |

## La regle des LIENS (ce qui rend un voisin retrouvable)

1. un lien est un CHEMIN depuis la racine des documents de la Matrice
   (ex. `matrice/data/outils/rechercher/main.py`) -- jamais un nom seul, jamais un
   chemin absolu, jamais un < voir aussi > perdu dans la prose ;
2. jamais un lien vers SOI-MEME (le garde le nomme : egocentrique) ;
3. la cible doit EXISTER (le garde le nomme : lien mort) ;
4. le lien se DECLARE DES DEUX COTES : si A nomme B, B nomme A. C est ce RETOUR que
   la routine `verifier-liens-cartes` mesure -- le garde, lui, juge la forme, la mort
   et l egocentrisme (EO-347) ;
5. garder la ligne lisible : au-dela de six liens, preferer un document `index` qui
   porte la carte, et nommer l index.

## Ce que le moteur de recherche en fait

```text
# --requete et --champ sont DEUX modes DISTINCTS : les combiner est REFUSE (le filtre serait muet).
python3 cerveau-projet/matrix/lancer.py rechercher rechercher --champ "type=outil;appartient_a=optimus-prime"

Et pour remonter le GRAPHE DES LIENS -- qui pointe vers ce fichier ?

# la CIBLE se donne en forme CANONIQUE depuis la racine des documents : matrice/...
python3 cerveau-projet/matrix/lancer.py rechercher rechercher --lien <chemin canonique>

# exemple MESURE : une carte qui declare matrice/data/commun/cible.py est retrouvee
# par --lien cible.py -- < cible.py > est une FIN de chemin, la tolerance est DITE.

`--lien` rend les DOCUMENTS dont la carte DECLARE ce chemin. La comparaison
accepte la forme CANONIQUE exacte ou une FIN de chemin (`cible.py`) : la
tolerance est DITE, jamais silencieuse. Un 0 resultat NOMME la demande et dit
combien de liens sont declares dans le corpus lu (jamais un 0 muet).
```

`--champ` rend les DOCUMENTS qui portent la carte, pas des lignes : les cles de carte
SONT l index du corpus. Une carte remplie rend un document trouvable ; une carte
absente ou vide le rend invisible (L-016). Les zones invisibles ne sont pas
cherchees : d ou l importance d une carte VRAIE plutot que d un document muet.
