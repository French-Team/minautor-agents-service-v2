---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# AUDIT -- LE PERIMETRE DE LA RECHERCHE PAR CHAMP ET LA CLE liens (EO-369 / MO-404)

> Consigne (EO-369, constat du CADRAGE des liens des fichiers connectes) : mesurer si
> les cartes qui portent les LIENS sont visibles au moteur PAR DEFAUT, et poser la
> question a trancher par la suite du CADRAGE.
> AUDIT = LECTURE SEULE : aucun fichier de service modifie. Chaque point porte la
> commande qui le VERIFIE (a rejouer telle quelle) et l EMPREINTE SHA-256 des fichiers lus.

## 1. LE MEME CHAMP, DEUX PERIMETRES : 1 OU 106 SELON LE DRAPEAU

Commande (a rejouer) :
    python3 cerveau-projet/matrix/lancer.py rechercher rechercher --champ "appartient_a=optimus-prime" --dans fichiers

Mesure SANS --prive :
    Documents a carte : 52 / 56 lus | sans carte : 4
    Exclus invisibles L-016 : 119 document(s) (28 zones declarees, dont _operateur, tmp-optimus, suivi-optimus)
    Trouves : 1  ->  matrice/docs/heritage-v1-v2-AGENTS.md

Mesure AVEC --prive (MEME requete) :
    Documents a carte : 169 / 175 lus | sans carte : 6
    Trouves : 106  (Retournes : 50, plafond d affichage)

CONSEQUENCE MESUREE : la MEME requete rend 1 ou 106. Les 105 documents d ecart
portent l essentiel des cartes de l operateur et des outils -- exactement les
cartes qui disent les fichiers CONNEXES a modifier. Un lien pose sur une carte
d operateur n est donc PAS trouvable par un rechercher ordinaire : il faut savoir
qu il faut --prive.

## 2. LA CLE liens EST ACCEPTEE, MAIS PORTEE PAR 0 CARTE

Commande (a rejouer) :
    python3 cerveau-projet/matrix/lancer.py rechercher rechercher --champ "liens=outil" --dans fichiers --prive

Mesure :
    Documents a carte : 169 / 175 lus
    Trouves : 0 | Retournes : 0

MESURE DU DISQUE (169 cartes lues, en-tetes type: + appartient_a:) : 0 carte porte
la cle liens. La cle n est donc PAS inconnue du moteur : elle est ACCEPTEE et rend
0. LA PREMISSE DE EO-369 (rechercher REFUSE EN NOMMANT la cle inconnue) est PERIMEE
depuis que la grammaire a admis la cle (section 3 de la grammaire : les cles hors
type/appartient_a/commun sont LIBRES).

## 3. LA QUESTION A TRANCHER (suite du CADRAGE)

Le perimetre de la recherche par CHAMP doit-il suivre le perimetre de L-016 (un lien
pose dans une carte invisible reste invisible), ou le lien doit-il vivre dans le
document VISIBLE qui POINTE l invisible ? Tant que ce n est pas tranche, le fait
mesure est : les cartes les plus utiles au createur sont invisibles par defaut.

## 4. DOMICILES ET EMPREINTES (fichiers lus)

- matrice/data/classeur-variables.json (cle V-003 perimetre-cameleon, qui nomme les
  28 zones) -- SHA-256 (16 premiers) 5f80da6810db8f5a
- matrice/data/commun/invisibilite.py (le domicile du contrat L-016) : lire ses zones
- matrice/data/outils/rechercher/main.py (le moteur) -- SHA-256 (16 premiers) 2adc7a4e2fd8232b

VERDICT : les cartes qui portent les liens sont INVISIBLES au moteur par defaut des
que la carte appartient a l operateur ou a un outil. Mesure rejouable ; aucune
ecriture de service.
