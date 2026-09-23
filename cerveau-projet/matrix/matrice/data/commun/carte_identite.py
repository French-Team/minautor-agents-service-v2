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

CE QUE CE FICHIER NE FAIT PAS : il ne juge pas la CONFORMITE (le garde le fait),
il ne lit aucun corpus (il lit un TEXTE ou un CHEMIN qu'on lui donne).
"""

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
    "plan-preparation-conservation",
    "protocole",
    "readme",
    "regle-immuable",
    "role",
    "theme",
)

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
