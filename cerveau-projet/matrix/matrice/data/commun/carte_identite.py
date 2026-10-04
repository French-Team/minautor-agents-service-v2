"""DOMICILE de la CARTE D'IDENTITE -- grammaire des en-tetes de documents.

POURQUOI CE FICHIER EXISTE (M-076, L-029 ; mesure 2026-09-21) : la grammaire de
la carte vivait dans UN SEUL endroit -- le garde `verifier-cartes-identite.py`
(marqueur de front-matter, ligne `identite:`, cles obligatoires, vocabulaire
FERME des types). Un consommateur de plus (le moteur de recherche, qui doit
savoir chercher par COMBINAISON de champs) aurait du la RECOPIER : deux copies
d'une meme regle divergent toujours en silence (mesure L-100/L-102 : trois
copies du contrat d invisibilite, la troisieme etait morte).

Ici : la GRAMMAIRE, une fois. Le garde la CONSOMME (il ne la recopie plus), le
moteur la CONSOMME (il peut chercher par carte). Une regle, un domicile.

CE QU'UNE CARTE EST : un front-matter borne par deux `---` en TETE du document,
portant la ligne `identite:` et des couples `cle: valeur`. Les trois cles
obligatoires disent QUOI est le document (`type`), A QUI il appartient
(`appartient_a` -- un NOM, jamais un chemin) et s'il est COMMUN aux deux
sessions (`commun`).

DEUX VOCABULAIRES, DEUX NATURES -- mesure du 2026-09-21 sur les cartes reelles :
- `type` est un vocabulaire FERME (TYPES_RECONNUS ci-dessous) : un type neuf se
  DECLARE, il ne s'invente pas (c'est ainsi que `preparation-readme` et
  `outil-pilote-optimus` sont nes) ;
- les AUTRES cles sont LIBRES (mesure : `version` 21 cartes, `statut` 16, `date`
  12, `tags` 3 ...). Une liste fermee y serait un mensonge : elle refuserait des
  cartes conformes. Une faute de frappe y est donc detectee par LE CORPUS
  (`cle_inconnue_du_corpus`) : une cle que AUCUNE carte du corpus ne porte est
  une faute, et l appelant la REFUSE en nommant les cles vues -- jamais un
  `0 resultat` muet.

L IMPORTANCE (EO-457, demande createur 2026-09-27) : deux cles LIBRES de plus,
`gravite` (vocabulaire FERME a 5 valeurs) et `niveau` (entier 1..10), disent le
DEGRE D IMPORTANCE d un document -- GRAVITE d abord, puis NIVEAU. `valider_carte`
les juge QUAND elles sont la (une carte sans importance reste conforme) et
`importance_de_carte` en rend la cle de comparaison.

CE QUE CE FICHIER NE FAIT PAS : il ne juge pas la CONFORMITE (le garde le fait),
il ne lit aucun corpus (il lit un TEXTE ou un CHEMIN qu'on lui donne).
"""

from pathlib import Path

# La CONFORMITE d une carte se JUGE ICI, avec la grammaire (MO-430) : la
# FORME des liens vient de cible.py -- un seul domicile par regle (M-076).
from cible import forme_canonique, racine_matrice  # noqa: E402

# Bornes du front-matter : la carte vit ENTRE deux marqueurs, en tete de fichier.
MARQUEUR_FRONT = "---"
# La ligne qui declare la carte. Un front-matter d'un autre genre (une regle
# horizontale en tete, un en-tete d'outil) n'est PAS une carte.
CLE_IDENTITE = "identite:"
# Les trois cles que toute carte DOIT porter (le garde les exige).
CLES_OBLIGATOIRES = ("type", "appartient_a", "commun")
# Un nom d'appartenance ne contient NI separateur de dossier NI antislash.
SEPARATEURS_INTERDITS = ("/", "\\")
EXTENSION = ".md"

# Vocabulaire FERME des types de document. Ajouter un type = une decision,
# tracee ici -- pas un litteral invente dans un fichier.
TYPE_OUTIL = "outil"

TYPES_RECONNUS = (
    "analyse",
    "carte-mission",
    "chaine",
    "convention",
    "fiche",
    "fiche-agent",
    "index",
    "index-parcours",
    "index-themes",
    "journal",
    "mots-cles",
    "outil",
    # MO-492 / MO-504 : la PASSERELLE USER (`user-demandes/`) est un type de document
    # a part entiere -- un CANAL de communication ecrit par le user, dont le HEAD
    # porte la carte d identite et le mode d emploi (patternes de delimitation,
    # crochets d entree, cycle de vie de l extraction). Une demande extraite est
    # RETIREE du canal : ce qui reste est le head + les demandes non extraites. Un
    # type neuf se DECLARE (il ne s invente pas) : voici la declaration.
    "passerelle",
    "pattern",
    "plan-preparation-conservation",
    "processus",
    "protocole",
    "readme",
    "regle-immuable",
    "role",
    "routine",
    "segment",
    "theme",
)

# --- L IMPORTANCE D UN DOCUMENT (EO-457, demande createur 2026-09-27) --------
# Le createur a demande que la carte d identite porte DEUX champs de plus, qui
# servent a DIRE l importance d un document et, en plus de l urgence de
# l entonnoir, a DECIDER quel travail passe devant : `gravite` (la BANDE
# principale) et `niveau` (le RAFFINEMENT dans la bande). Ce sont des cles LIBRES
# au sens du corpus -- une carte sans elles reste conforme -- mais leur VALEUR est
# FERMEE : une gravite hors liste, un niveau hors bornes sont des ECARTS.
CLE_GRAVITE = "gravite"
CLE_NIVEAU = "niveau"
# De la PLUS grave a la MOINS grave : l ORDRE EST SIGNIFICATIF (rang 0 = plus
# important). Un seul vocabulaire d importance pour tout le flux (M-076) -- c est
# LUI que l entonnoir et le pilote CONSOMMENT, jamais un second.
GRAVITES = ("tres-urgent", "urgent", "important", "normal", "optionnel")
# La forme ecrite par le createur (`tres urgent`, avec une espace) est ACCEPTEE et
# RAMENEE a la forme CANONIQUE `tres-urgent` : un champ, un sens, aucune saisie
# perdue. Un alias ne JOUE jamais le role d une gravite NOUVELLE.
GRAVITE_ALIAS = {"tres urgent": "tres-urgent"}
GRAVITE_DEFAUT = "normal"
# Le niveau est un ENTIER de 1 a 10 ; PLUS HAUT = PLUS IMPORTANT.
NIVEAU_MIN = 1
NIVEAU_MAX = 10
NIVEAU_DEFAUT = 5

# --- Grammaire d'une DEMANDE de combinaison (le moteur de recherche) ---------
# Separateur de plusieurs demandes dans UNE valeur d'option. Pourquoi un seul
# argument et non une option repetee : le parseur PARTAGE (data/commun/options.py)
# garde UNE valeur par nom d'option -- une option repetee serait ECRASEE en
# silence (mesure 2026-09-21). Une demande par `;` DIT sa forme d'un coup, et le
# moteur REFUSE une option repetee au lieu de la perdre (entry.py).
SEPARATEUR_DEMANDES = ";"
# Deux ecritures acceptees pour un couple : `=` (syntaxe d'option) et `:`
# (syntaxe de la carte elle-meme). Les deux disent la meme chose.
SEPARATEURS_CLE_VALEUR = ("=", ":")

# --- LES LIENS D'UN DOCUMENT (EO-347, demande du createur ; audit MO-349) -----
# La carte peut porter les LIENS des fichiers qui lui sont CONNECTES, pour
# retrouver les fichiers connexes a modifier. La REGLE vit ICI, une seule fois
# (M-076), et le garde la CONSOMME.
#   - la CLE est `liens` ;
#   - les liens sont separes par des VIRGULES (une valeur de carte est une
#     CHAINE, `cle: valeur` : un seul separateur, celui des listes deja utilise
#     par les tags de la BDD des modifications) ;
#   - chaque lien est un chemin RELATIF A LA RACINE DE LA MATRICE, CANONIQUE --
#     la MEME forme que les cles de la BDD (EO-363), et la MEME fonction
#     (`cible.forme_canonique`). Un chemin absolu, un prefixe
#     < cerveau-projet/matrix/ >, un < ./ > ou un antislash ne sont donc PAS
#     canoniques : une forme qui depend de qui l'ecrit ne se mesure ni ne se compare.
# POURQUOI UN CHEMIN ICI, ET PAS UN NOM : `appartient_a` est deja un NOM (jamais
# un chemin). Le contrat fondamental (2) interdit le chemin coupe pour UTILISER
# un composant ; un lien de carte n'UTILISE rien, il POINTE -- c'est le seul
# endroit ou un chemin est la bonne reponse, et il n'a donc qu'UNE forme.
# POURQUOI PAS DANS LES CLES OBLIGATOIRES : une carte sans lien est NORMALE (tout
# document n'a pas de voisin). La cle est LIBRE ; c'est le CORPUS qui detecte une
# faute de frappe, et le GARDE qui juge la FORME quand la cle est la.
CLE_LIENS = "liens"
SEPARATEUR_LIENS = ","


def lire_carte(texte):
    """Dictionnaire de la carte, ou None (aucun front-matter `identite:`).

    Le front-matter est BORNE par deux `---` : hors de ces bornes, ce n'est pas
    une carte. La carte elle-meme est une suite de `cle: valeur` -- les valeurs
    restent des CHAINES brutes (ce module ne convertit ni ne devine : `commun`
    vaut "true" ou "false" tels qu'ecrits).
    """
    if not isinstance(texte, str) or not texte:
        return None
    lignes = texte.splitlines()
    if not lignes or lignes[0].strip() != MARQUEUR_FRONT:
        return None
    bloc = []
    ferme = False
    for ligne in lignes[1:]:
        if ligne.strip() == MARQUEUR_FRONT:
            ferme = True
            break
        bloc.append(ligne)
    if not ferme:
        return None
    if not any(ligne.strip() == CLE_IDENTITE for ligne in bloc):
        return None
    carte = {}
    for ligne in bloc:
        propre = ligne.strip()
        if propre == CLE_IDENTITE or propre.startswith("#"):
            continue
        if ":" in propre:
            cle, valeur = propre.split(":", 1)
            carte[cle.strip()] = valeur.strip()
    return carte


def carte_de_fichier(chemin):
    """Carte d'un fichier lu en UTF-8 (jamais devinee), ou None.

    Un chemin illisible n'est PAS une carte : le fichier est absent du resultat,
    et l'appelant qui veut le DIRE compte les `None` (un document sans carte ne
    peut pas repondre a une combinaison de champs -- le taire serait un mensonge
    par omission).
    """
    try:
        with open(chemin, "r", encoding="utf-8", errors="replace") as fichier:
            return lire_carte(fichier.read())
    except OSError:
        return None


def demandes(texte):
    """Decoupe une demande de combinaison en (liste de couples, erreurs).

    Forme : `cle=valeur[;cle=valeur]` (le `:` vaut le `=`). Rend les couples
    NORMALISES (cle et valeur sans espaces superflus) et la liste des demandes
    ILLISIBLES, nommees telles quelles : une demande qu'on ne comprend pas ne
    doit jamais devenir un filtre qui ne filtre rien.
    """
    couples = []
    erreurs = []
    for morceau in str(texte or "").split(SEPARATEUR_DEMANDES):
        brut = morceau.strip()
        if not brut:
            continue
        position = -1
        for separateur in SEPARATEURS_CLE_VALEUR:
            ou = brut.find(separateur)
            if ou > 0 and (position == -1 or ou < position):
                position = ou
        if position <= 0:
            erreurs.append(brut)
            continue
        cle = brut[:position].strip()
        valeur = brut[position + 1:].strip()
        if not cle or not valeur:
            erreurs.append(brut)
            continue
        couples.append((cle, valeur))
    if not couples and not erreurs:
        erreurs.append("(demande vide)")
    return couples, erreurs


def correspond(carte, couples):
    """Vrai si la carte porte TOUS les couples demandes (ET, compare sans casse).

    Comparaison sans casse : une carte ecrit `optimus-prime`, l'appelant peut
    ecrire `OPTIMUS-PRIME` -- les deux disent la meme appartenance. Une carte
    ABSENTE (None) ne correspond jamais : un document sans carte ne peut pas
    repondre a une combinaison de champs.
    """
    if not carte:
        return False
    basses = {str(cle).lower(): str(valeur).lower() for cle, valeur in carte.items()}
    for cle, valeur in couples:
        if basses.get(cle.lower()) != valeur.lower():
            return False
    return True


def resume(carte, ordre=None):
    """Resume lisible d'une carte : `type=... appartient_a=... commun=...`.

    L'ordre des trois cles obligatoires est STABLE (l'appelant peut en imposer
    un) : un resume dont l'ordre change d'un document a l'autre ne se compare
    pas d'un coup d'oeil.
    """
    if not carte:
        return ""
    cles = list(ordre) if ordre else list(CLES_OBLIGATOIRES)
    for cle in carte:
        if cle not in cles:
            cles.append(cle)
    return " ".join(cle + "=" + str(carte[cle]) for cle in cles if cle in carte)


def liens_de_carte(carte):
    """Les liens declares par une carte, nettoyes (liste vide si aucun).

    `liens: a, b` rend [a, b]. Un lien VIDE est ignore : `liens:` sans valeur ne
    dit pas < aucun lien >, il ne dit RIEN -- et l'appelant qui veut l'exiger
    compte les cartes SANS la cle, il ne devine pas une valeur vide.
    """
    if not carte:
        return []
    brut = str(carte.get(CLE_LIENS, "") or "")
    return [lien.strip() for lien in brut.split(SEPARATEUR_LIENS) if lien.strip()]


def cles_du_corpus(cartes):
    """Vocabulaire REEL des cles : celles que les cartes du corpus portent.

    C'est LUI qui detecte une faute de frappe (et non une liste tenue a la main,
    qui refuserait des cles conformes) : une cle qu'aucune carte ne porte est
    une faute -- mesure 2026-09-21 : les cartes reelles portent `type`,
    `appartient_a`, `commun`, puis des cles LIBRES (`version`, `statut`,
    `date`, `tags`, ...).
    """
    vues = set()
    for carte in cartes:
        if carte:
            vues.update(str(cle) for cle in carte)
    return vues


def valeurs_vues(cartes, cle):
    """Valeurs reellement portees pour cette cle, triees (aide au refus nomme).

    Sert a ne jamais rendre un `0 resultat` muet : quand une combinaison ne
    trouve rien, l'appelant peut DIRE quelles valeurs existent pour cette cle.
    """
    cible = str(cle).lower()
    vues = set()
    for carte in cartes:
        if not carte:
            continue
        for nom, valeur in carte.items():
            if str(nom).lower() == cible:
                vues.add(str(valeur))
    return sorted(vues)


def valeur_dans_champ_multiple(cartes, cle, valeur):
    """Vrai si la valeur figure comme ELEMENT d un champ a VALEURS MULTIPLES.

    Un champ dont une valeur porte le SEPARATEUR_LIENS declare est une LISTE :
    `--champ cle=valeur` compare la valeur ENTIERE, donc une demande qui vise un
    SEUL element ne peut structurellement pas correspondre (mesure 2026-09-23 :
    `liens` porte 33 liens sur 11 cartes, et `--champ liens=<un de ces liens>`
    rendait 0). Ce predicat sert a NE PAS rendre un 0 muet : l appelant peut
    nommer le mode DEDIE (--lien pour le graphe des liens) au lieu de laisser
    croire a une absence (famille MO-055).
    """
    cible = str(cle).lower()
    voulue = str(valeur).strip().lower()
    if not voulue:
        return False
    for carte in cartes:
        if not carte:
            continue
        for nom, val in carte.items():
            if str(nom).lower() != cible:
                continue
            elements = [element.strip().lower()
                        for element in str(val).split(SEPARATEUR_LIENS)
                        if element.strip()]
            if len(elements) > 1 and voulue in elements:
                return True
    return False


# --- L IMPORTANCE D UN DOCUMENT, EN FONCTION (EO-457) -----------------------
# La comparaison est TOTALE et DETERMINISTE : GRAVITE d abord (la bande), puis
# NIVEAU (le raffinement DANS la bande). Un tuple PLUS PETIT est PLUS important :
# le niveau est rendu INVERSE pour que l ordre croissant des tuples soit l ordre
# d importance.
def gravite_canonique(valeur):
    """La forme CANONIQUE d une gravite, ou "" si inconnue (jamais devinee)."""
    texte = " ".join(str(valeur or "").split()).lower()
    if texte in GRAVITES:
        return texte
    return GRAVITE_ALIAS.get(texte, "")


def rang_gravite(gravite):
    """Le rang d une gravite (0 = plus grave), ou len(GRAVITES) si inconnue."""
    canonique = gravite_canonique(gravite)
    return GRAVITES.index(canonique) if canonique else len(GRAVITES)


def niveau_valide(valeur):
    """Le niveau ENTIER de NIVEAU_MIN a NIVEAU_MAX, ou 0 si ce n est pas un niveau."""
    try:
        entier = int(str(valeur).strip())
    except (TypeError, ValueError):
        return 0
    return entier if NIVEAU_MIN <= entier <= NIVEAU_MAX else 0


def importance_de_carte(carte):
    """La CLE D IMPORTANCE d une carte ou d un item : (rang_gravite, niveau inverse).

    Une cle PLUS PETITE est PLUS importante. Une cle d importance ABSENTE ou
    INVALIDE prend sa valeur par DEFAUT (gravite normale, niveau 5) -- c est a
    l appelant de DIRE une absence, jamais a cette fonction d inventer une gravite.
    """
    est_dict = isinstance(carte, dict)
    gravite = carte.get(CLE_GRAVITE, "") if est_dict else ""
    rang = rang_gravite(gravite)
    if rang >= len(GRAVITES):
        rang = GRAVITES.index(GRAVITE_DEFAUT)
    niveau = niveau_valide(carte.get(CLE_NIVEAU, "") if est_dict else "")
    return (rang, NIVEAU_MAX + 1 - (niveau or NIVEAU_DEFAUT))


def plus_important(cle_importance, cle_reference):
    """Vrai si la cle d importance A est STRICTEMENT plus importante que B."""
    return tuple(cle_importance) < tuple(cle_reference)


def valider_importance(carte):
    """Les ECARTS de gravite/niveau d une carte (vide = conforme).

    Les deux cles sont LIBRES : leur ABSENCE n est pas un ecart (une carte sans
    importance declaree est normale). C est leur VALEUR, QUAND ELLE EST PRESENTE,
    qui est jugee -- un critere invente serait pire qu une absence (EO-457).
    """
    ecarts = []
    if not carte:
        return ecarts
    gravite = str(carte.get(CLE_GRAVITE, "")).strip()
    if gravite and not gravite_canonique(gravite):
        ecarts.append("gravite hors vocabulaire ferme : " + gravite
                      + " (valeurs : " + ", ".join(GRAVITES) + ")")
    niveau = str(carte.get(CLE_NIVEAU, "")).strip()
    if niveau and not niveau_valide(niveau):
        ecarts.append("niveau hors bornes " + str(NIVEAU_MIN) + "-" + str(NIVEAU_MAX)
                      + " : " + niveau)
    return ecarts


# --- LA CONFORMITE D UNE CARTE (MO-430, demande du createur) ----------------
# Comparer une carte a son MODELE, c est juger ses champs : la suite d outils
# (carte-creer, carte-editer, carte-modifier, carte-comparer) consomme CE
# jugement au lieu de le recopier (M-076). Le garde verifier-cartes-identite
# garde le sien : lui mesure le corpus entier, la suite juge UNE carte sur
# demande -- deux postures, une seule reponse a < cette carte est-elle conforme ? >.
COMMUN_OUI = "true"
COMMUN_NON = "false"


MOTS_REPETITIFS = ("outil", "outils", "la", "le", "les", "un", "une", "des", "de", "du")


def titre_d_une_carte(texte):
    """Le TITRE d une carte : son premier titre de niveau 1 du corps, ou vide."""
    if not isinstance(texte, str):
        return ""
    vu_ferme = False
    for ligne in texte.splitlines():
        if ligne.strip() == MARQUEUR_FRONT:
            vu_ferme = True
            continue
        if not vu_ferme:
            continue
        # La localisation se fait par COMPARAISON sur le second caractere, sans
        # aucun litteral de filtre : le garde des extractions refuse une chaine
        # qui ressemble a une extraction sans producteur (mesure 2026-09-30,
        # meme piege que la tete de l outil lire).
        if ligne[:1] == "#" and ligne[1:2] != "#":
            return ligne[2:].strip()
    return ""


def information_du_titre(titre, nom):
    """Les mots du titre qui n apportent RIEN de plus que le nom de l outil.

    On retire le titre generique (`OUTIL`), le nom lui-meme et les mots de
    liaison. Ce qui reste est l information : c est elle qui doit etre non
    vide. Mesure du 2026-09-30 : 26 titres sur 45 ne laissaient RIEN (`OUTIL --
    lire`) et 7 cartes n avaient aucun titre -- le chemin ne les decrivait donc
    pas davantage.
    """
    if not titre:
        return []
    reste = []
    for mot in titre.replace("--", " ").replace(":", " ").split():
        propre = mot.strip(".,;:!?()[]").lower()
        if not propre or propre in MOTS_REPETITIFS:
            continue
        if nom and propre == nom.lower():
            continue
        reste.append(mot)
    return reste


def juger_titre(carte, titre, chemin):
    """Les ecarts de TITRE d une carte d OUTIL (vide = le titre informe).

    Le jugement ne porte que sur les cartes `type: outil` : une carte de role ou
    de protocole a le droit d avoir un titre qui ne fait qu annoncer le nom,
    parce que ce n est pas un outil qu on doit pouvoir distinguer de ses voisins
    a la lecture du chemin. Pour un outil, l inverse est vrai : plusieurs
    `verifier-*` ne se distinguent que par ce que leur carte dit.
    """
    if str(carte.get("type", "")).strip() != TYPE_OUTIL:
        return []
    nom = Path(str(chemin)).parent.name
    if not titre:
        return ["carte d outil SANS TITRE : le nom " + nom
                + " ne dit pas ce que l outil fait"]
    if not information_du_titre(titre, nom):
        return ["titre sans information : " + repr(titre)
                + " -- il ne fait que repeter le nom (" + nom
                + ") ; dire ce que l outil FAIT"]
    return []

def valider_carte(carte, chemin, depart):
    """Liste des ECARTS de la carte (vide = conforme), jugee sur SES regles.

    Les memes jugements que le garde : trois cles obligatoires presentes, type
    du vocabulaire ferme, commun qui dit true ou false, appartient_a en NOM
    (jamais un chemin), et pour chaque lien declare : forme canonique, jamais
    vers soi-meme, cible vivante. `chemin` est le document qui porte la carte
    (l auto-reference se mesure a lui) ; `depart` ancre la racine de la Matrice.
    Une carte ABSENTE n est pas un ecart de forme : c est l appelant qui la
    cherche -- ici, la seule reponse est < ce texte n est pas une carte >.
    """
    if not carte:
        return ["ce texte n'est pas une carte (front-matter `identite:` absent)"]
    ecarts = []
    for cle in CLES_OBLIGATOIRES:
        if not str(carte.get(cle, "")).strip():
            ecarts.append("cle obligatoire absente ou vide : " + cle)
    type_doc = carte.get("type", "")
    if type_doc and type_doc not in TYPES_RECONNUS:
        ecarts.append("type hors vocabulaire ferme : " + type_doc
                      + " (types connus : " + str(len(TYPES_RECONNUS)) + ")")
    commun_valeur = carte.get("commun", "")
    if commun_valeur and commun_valeur not in (COMMUN_OUI, COMMUN_NON):
        ecarts.append("commun doit dire " + COMMUN_OUI + " ou " + COMMUN_NON
                      + " : " + commun_valeur)
    appartenance = carte.get("appartient_a", "")
    if any(separateur in appartenance for separateur in SEPARATEURS_INTERDITS):
        ecarts.append("appartient_a doit etre un NOM, pas un chemin : " + appartenance)
    racine = racine_matrice(depart)
    canonique = ""
    try:
        canonique = Path(chemin).resolve().relative_to(racine.resolve()).as_posix()
    except (OSError, ValueError):
        canonique = ""
    for lien in liens_de_carte(carte):
        if forme_canonique(lien, chemin) != lien:
            ecarts.append("lien non canonique : " + lien
                          + " (forme attendue : relative a la racine de la Matrice)")
        elif canonique and lien == canonique:
            ecarts.append("lien vers soi-meme : " + lien)
        elif not (racine / lien).is_file():
            ecarts.append("lien mort : " + lien)
    # L IMPORTANCE (EO-457) : QUAND les deux cles sont la, leur VALEUR est jugee.
    # Le jugement vit dans valider_importance (un seul domicile, M-076).
    ecarts.extend(valider_importance(carte))
    return ecarts
