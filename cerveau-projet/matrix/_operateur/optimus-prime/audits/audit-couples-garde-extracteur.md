---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# AUDIT -- LES COUPLES GARDE-EXTRACTEUR (MO-383, lecture seule)

Question : le defaut MO-382 (l extracteur cherchait `KO]` quand le garde imprime
`[KO]`) est-il ISOLE, ou d autres couples garde-extracteur sont-ils incoherents ?

## Methode

Deux mesures STATIQUES sur tout le .py de la Matrice (zones jetables et caches
exclus) :

1. LES SITES D EXTRACTION : `splitlines()` suivi, dans une fenetre de 240
   caracteres, d un `startswith(...)` -- 66 sites dans 4 fichiers ; 26 filtres
   distincts.
2. LES PREFIXES IMPRIMES : pour chaque fichier, la convention `controler()` (qui
   imprime `[OK]` / `[KO]`) et le premier litteral de chaque `print(...)` (partie
   avant l accolade d une f-string, espaces de tete retires).

Un filtre est COHERENT si au moins un prefixe imprime COMMENCE par lui (la
lecture se fait sur `l.strip()`).

## Resultat

66 sites, 26 filtres distincts. UN SEUL ecart DE STATUT :

| Fichier:ligne | Maillon | Filtre | Producteur | Verdict |
|---|---|---|---|---|
| lanceur-non-regression.py:1116 | 34 source | `"[KO"` (corrige en MO-382) | verifier-source-item.py (`controler`) imprime `[KO]` | COHERENT |
| lanceur-non-regression.py:1140 | 35 enchainement | `"KO]"` | verifier-enchainement.py (`controler`) imprime `[KO]` | MUET -- A REPARER |

CAUSE : la MEME faute de frappe que MO-382 (crochet ouvrant manquant), dans la
forme SIMPLE `startswith("KO]")` et non la forme tuple `startswith(("KO]", ...))`
-- c est pourquoi le premier balayage ne l avait pas vue.

CONSEQUENCE : quand le maillon 35 rougit, le verdict ne nomme AUCUN controle et
renvoie `enchainement: voir verifier-enchainement.py` : le rouge muet de la lecon
L-163, au maillon voisin.

Les AUTRES sites ne sont PAS des couples garde-extracteur mais des parseurs de
DOCUMENT, dont le producteur est un fichier, pas une ligne imprimee : `#`,
les triples accents graves, `## Encart : `, `usage`, `"  "` (markdown / usage /
lignes indentees). Ils ne sont pas juges ici : les compter MUETS serait un faux
positif de la MESURE, pas un defaut du code.

## Limites dites

- La mesure des prefixes est STATIQUE : un garde qui imprime par une variable ou
  un motif compose peut etre declare MUET a tort. Les deux sites de STATUT ont ete
  verifies a la main (les deux gardes portent bien `def controler(`).
- La fenetre de 240 caracteres peut manquer un site dont le `startswith` serait
  plus loin ; elle en a trouve 66, dont les 31 du lanceur.

## CONCLUSION

Le defaut n etait PAS isole : un SECOND exemplaire vit au maillon 35 (enchainement).
Les deux sont la MEME classe (lecon L-163). Le reste des couples de statut est
coherent. La reparation du maillon 35 est DEPOSEE (cet audit est en lecture seule).
