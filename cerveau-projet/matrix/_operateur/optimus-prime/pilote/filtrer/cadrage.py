"""CADRAGE AUTONOME -- [???] constitue la suite de missions de bout en bout.

DEMANDE CREATEUR (2026-09-21, crochet [corriger]) : "quand j'utilise [???] tout le
process doit se faire de bout en bout sans intervention de user jusqu'a la
transformation en la suite de missions. Ce process doit etre automatise a son
maximum. Je ne veux pas devoir intervenir : chaque litige doit etre resolu par le
process."

CE QUI SE PASSAIT AVANT (mesure du meme jour) : le routeur IMPRIMAIT
`cadrage/ouvrir` ("ROUTE IMPRIMEE, PAS JOUEE") et c'etait l'AGENT qui devait jouer
le parcours. Mesure : il s'est arrete au premier geste (un item au vrac), et le
createur a du redemander. Cinq litiges rendaient la main au createur :
  1. le parcours n'etait PAS joue ;
  2. "ATTENTION DOUBLON POSSIBLE ... si c'est le meme travail, REUNIR les items ;
     sinon continuer" -- une decision rendue au LECTEUR ;
  3. "un item du vrac n'est PAS executable" -- un SECOND geste manuel (classer) ;
  4. "auto-validation non" -- un GO attendu ;
  5. la CHAINE n'existait nulle part : c'etait de la prose, pas une liste.

CE QUE CE MODULE FAIT : il joue le parcours ENTIER et rend l'unite a deposer.

LES REGLES NE SONT PAS RECOPIEES (M-076) : elles sont LUES dans le domicile du
theme (`parcours/themes/theme-cadrage.json`, champ `redirects`). Six cases, six
regles, et ce module les CONSOMME au lieu de les re-dicter :
  [manques]  une demande sans manque nommable SORT PAR LA PREMIERE CASE -- c'est un
             RESULTAT, jamais un echec (le module le DIT et s'arrete la) ;
  [memoire]  la memoire se lit AVANT toute question -- et ici, la lecture est une
             MISSION (le moteur de recherche est dans les outils de toute mission
             depuis le 2026-09-21), jamais une question au createur ;
  [audit]    lecture seule, ce que le disque dit prime ;
  [nemesis]  un avis qui ne retire rien le DIT ;
  [chaine]   aucun maillon sans PREUVE attendue ni TYPE declare, et jamais sans sa
             derniere ligne : LA MISSION ;
  [depot]    aucun depot ne contourne la porte.

LE PRINCIPE QUI RESOUT TOUS LES LITIGES (demande du createur) : une incertitude ne
remonte JAMAIS au createur -- elle devient un MAILLON MESURABLE. Le doute est le
travail de la chaine, pas une question. Et un doublon se resout par une REGLE
declaree (ci-dessous), jamais par un "si c'est le meme travail" rendu au lecteur.
"""
import base64
import json
import subprocess

import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-414, vague 4 du lot) -----------------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu) : on remonte
# jusqu au dossier `matrix`, et on REFUSE plutot que de deviner (garde-foi L-006).
_RACINE_LANCEMENT = Path(__file__).resolve().parent
while _RACINE_LANCEMENT.name != "matrix":
    if _RACINE_LANCEMENT.parent == _RACINE_LANCEMENT:
        raise RuntimeError("racine `matrix` introuvable en remontant depuis " + __file__)
    _RACINE_LANCEMENT = _RACINE_LANCEMENT.parent
_REPERTOIRE_COMMUN_LANCEMENT = _RACINE_LANCEMENT / "matrice" / "data" / "commun"
if not (_REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(_REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(_REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(_REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())

import sys
from pathlib import Path

# Le domicile des regles : le theme CADRAGE lui-meme (M-076 -- jamais une copie).
# Le chemin est DETECTE, jamais suppose (L-013) : la mesure du 2026-09-21 a montre
# que le supposer (`pilote/parcours/...`) rendait ZERO case -- et la chaine se
# reduisait a sa derniere ligne SANS QUE RIEN NE LE DISE. Un chemin faux et muet
# fabrique une chaine fausse qui a l'air complete.
NOM_THEME_CADRAGE = "theme-cadrage.json"
# Le prefixe des items : il vient de SON domicile (entonnoir/listes.py), comme le
# fait deja filtrer/entry.py pour TYPES. Recopie ici, il compilait et changeait le
# SENS de ce module sans un bruit le jour ou la famille d'ids change (M-076).
from entonnoir.listes import PREFIXE_ITEM  # noqa: E402
DOSSIER_THEMES = ("parcours", "themes")


def trouver_theme():
    """Le chemin REEL du theme CADRAGE, ou None (jamais une supposition)."""
    for parent in [Path(__file__).resolve()] + list(Path(__file__).resolve().parents):
        candidat = parent / DOSSIER_THEMES[0] / DOSSIER_THEMES[1] / NOM_THEME_CADRAGE
        if candidat.is_file():
            return candidat
    return None

# --- LA REGLE DE DOUBLON (declaree, mesuree, automatique) --------------------
# Pourquoi >= 2 : la mesure du 2026-09-21 a montre une alerte declenchee par UN SEUL
# mot commun ("fichiers") entre deux travaux sans rapport. Un seul mot est du bruit.
# Pourquoi un mot LONG : un mot de 6 caracteres et plus porte du sens ("cadrage",
# "identite", "moteur") ; les mots courts ("item", "type") sont partout.
MOTS_COMMUNS_POUR_DOUBLON = 2
LONGUEUR_MOT_SIGNIFICATIF = 6
# Mots trop generaux pour fonder un doublon (liste COURTE et declaree : elle ne
# juge que la ressemblance des TITRES, jamais le fond).
MOTS_GENERIQUES = ("fichier", "fichiers", "mission", "missions", "outil", "outils",
                   "projet", "matrice", "optimus", "systeme", "donnees")

# --- LA TABLE DES MAILLONS (ce que chaque case DEVIENT) ----------------------
# Chaque case du theme produit UNE mission : son type DECLARE (regle de [chaine]),
# la PREUVE attendue (regle de [chaine]) et la forme de son objectif. La derniere
# ligne est LA MISSION -- elle n'est jamais oubliee (regle de [chaine]).
# Les types viennent du vocabulaire ferme de l'entonnoir (dev, reparation, doc,
# LIMITE DECLAREE (2026-09-21) : ce moteur verse les maillons TYPES et AUTO-VALIDES
# par la regle, mais il ne porte PAS leur ordre dans le brin -- le brin est tisse par
# urgence puis round-robin entre les files (tresse/fonctions.py, tresser). Mesure :
# apres versement de la chaine EO-341..347, ses positions dans le brin etaient
# [20, 22, 24, 26, 6, 27, 15] -- ni ordonnees ni contigues. Consequence DITE : le
# pilote peut servir LA MISSION avant ses audits. Le maillon [depot] porte desormais
# cette exigence ; la limite reste, et elle se dit ici plutot que de se cacher.
#
# audit, revision) : aucun type invente.
MAILLONS_DECLARES = (
    ("manques", "audit",
     "Nommer CE QUI MANQUE dans la demande, en le MESURANT dans le depot : ce qui"
     " est deja ecrit (dans les fichiers, les OUTILS, les BDD) est lu, ce qui est"
     " absent est nomme. Aucune question au createur : un manque se mesure ou se"
     " declare, jamais il ne se demande.",
     "la liste des manques nommes, chacun avec sa MESURE et la commande qui la"
     " REJOUE (a rejouer telle quelle) ; s'il n'y a aucun manque nommable, la"
     " chaine s'arrete la et le DIT"),
    ("memoire", "audit",
     "Reprendre ce que le projet SAIT DEJA sur le sujet, avec le MOTEUR DE RECHERCHE"
     " du projet (cartes d'identite, BDD, fichiers) : chaque manque qui y est deja"
     " ecrit est une faute de recherche, pas un manque.",
     "les reponses trouvees, citees par leur chemin, la commande de recherche"
     " REJOUEE telle quelle, et les manques REELLEMENT absents apres ce TEST"),
    ("audit", "audit",
     "Constater l'etat REEL du perimetre (lecture seule) : ce que le disque dit des"
     " fichiers py/json et des BDD du perimetre, jamais ce qu'on croit savoir.",
     "l'etat constate, et pour chaque point la commande qui le VERIFIE (a"
     " REJOUER) avec l'EMPREINTE SHA du fichier lu"),
    ("nemesis", "audit",
     "Avis CONTRADICTOIRE sur la chaine envisagee : attaquer les maillons, les cas"
     " limites et ce que la liste ne couvre pas, en nommant pour chaque objection"
     " l'OUTIL ou le GARDE du projet qui la tranche. Si l'attaque ne retire rien, le"
     " DIRE (un avis qui ne change rien et se tait fait croire qu'il a servi).",
     "les objections, celles qui ont change la liste (et comment), celles qui"
     " n'ont rien change (dites telles quelles), chacune tranchee par un TEST ou"
     " un CONTRE-TEMOIN"),
    # LES TROIS CASES EXIGEES (EO-464, demande createur 2026-09-28) : elles vivent
    # dans le theme CADRAGE (parcours/themes/theme-cadrage.json) et DOIVENT etre
    # DECLAREES ici, sinon le garde des maillons les dit < CASE NON DECLAREE dans la
    # table > -- mesure du 2026-09-28 : le moteur les a VERSEES non declarees, et il
    # l'a ECRIT dans chaque objectif plutot que de sauter la case en silence. Leur
    # ordre (apres [nemesis], avant [chaine]) est celui du parcours : expertise et
    # contre-expertise d'abord, l'objection nommee ensuite, ce que voudrait l'user
    # en DERNIER filtre -- AVANT que la chaine ne devienne la mission finale.
    ("expertise", "audit",
     "EXPERTISE puis CONTRE-EXPERTISE : dire ce que le projet SAIT FAIRE de mieux"
     " sur ce sujet (etat de l'art INTERNE : outils, BDD, parcours, portes deja"
     " presentes), chaque affirmation portee par un temoin fichier:ligne ou"
     " porte/verbe ; puis ATTAQUER cette expertise -- ce qui est FAUX, INUTILE ou"
     " DEJA RESOLU, et le cas limite qui la rendrait inutile. Ne rien decider :"
     " cette case CONSTATE et ATTAQUE, elle ne tranche pas.",
     "deux blocs SEPARES (expertise, puis contre-expertise) et ce qui a SURVECU a"
     " l'attaque, cite par son temoin ; si l'attaque ne retire rien, le DIRE"),
    ("oui, mais...", "audit",
     "NOMMER l'objection AVANT d'agir : ecrire OUI, <ce qui est JUSTE dans la"
     " demande> MAIS <ce qui gene, manque ou coute> -- le OUI n'est pas une"
     " politesse, il NOMME ce qu'on accepte ; chaque MAIS est un FAIT mesure ou une"
     " CONSEQUENCE, jamais un gout, et il est suivi soit de la CONSEQUENCE (ce"
     " qu'on fera differemment) soit de la DECISION demandee au createur. Un MAIS"
     " qui ne peut pas se trancher seul est le POINT D'ARRET du parcours : on ne"
     " fabrique pas une mission sur une objection non tranchee.",
     "la forme OUI/MAIS ecrite, chaque MAIS suivi de sa consequence ou de sa"
     " decision, et les MAIS RETIRES (sans temoin ni consequence) dits tels quels"),
    ("si j'etais user", "audit",
     "DERNIER FILTRE avant la mission : LIRE la brique du projet sans la recopier"
     " (pilote/injection/si_j_etais_user.py -- c'est ELLE qui est injectee, une"
     " copie divergerait en silence, L-029/L-106) ; ecrire UNE phrase -- 'si"
     " j'etais user, je demanderais : ...' -- du point de vue de celui qui SUBIT le"
     " resultat ; la CONFRONTER a la chaine ENVISAGEE, et REECRIRE la chaine si"
     " elle n'y repond pas (cette case peut renvoyer a [chaine]).",
     "la phrase ecrite, la CONFRONTATION avec la chaine, et la reecriture si elle"
     " a eu lieu ; une case qui ne POUVAIT pas changer la chaine se DIT"),
    ("depot", "audit",
     "Verifier que la chaine est versee ET injectee comme UN seul ensemble : aucun"
     " maillon contourne la porte, aucun n'est orphelin, et l'ensemble se lit d'un"
     " bloc DANS L'ORDRE de la chaine (mesures du 2026-09-21 : le LOT existe -- EO-148"
     " verse le brin entier d'un geste -- mais le brin est TISSE par urgence puis"
     " round-robin entre les files, donc il NE PORTE PAS l'ordre des maillons ;"
     " l'ordre doit etre porte par la chaine elle-meme, jamais suppose).",
     "le versement VERIFIE : une ligne par maillon avec l'id rendu par la porte,"
     " et l'ensemble injecte comme un bloc"),
    ("chaine", "doc",
     "CONSTITUER LA LISTE : la suite ordonnee des missions, chacune avec son TYPE"
     " declare et sa PREUVE attendue, terminee par LA MISSION reelle -- la liste"
     " devient un fichier de pilotage (json) ecrit par un OUTIL, jamais un texte"
     " libre.",
     "la liste ecrite, ordonnee, chaque maillon type et prouvable, a VERIFIER par le"
     " garde des maillons (type + preuve nommes), avec sa derniere ligne (la"
     " mission)"),
)
# LA DERNIERE LIGNE (jamais oubliee) : la mission reelle. Son type est celui que la
# PORTE de depot PROPOSE (sa table a mots-cles) -- un type DECLARE par la porte,
# jamais devine par ce module. Le repli est declare ici, en un seul endroit.
TYPE_MISSION_DEFAUT = "reparation"
ACTION_DIRECTE = "a determiner par les maillons precedents (chaque maillon les"
ACTION_DIRECTE_SUITE = " reduit)"


def charger_cases(cas_du_theme=None):
    """Les cases du theme CADRAGE, ou None si le theme est INTROUVABLE.

    None n'est PAS une liste vide : une liste vide dirait "le theme n'a aucune
    case" (donc une chaine d'un seul maillon, qui a l'air complete), alors que None
    dit "je n'ai pas trouve le domicile des regles" -- et l'appelant le DIT.
    """
    if cas_du_theme is not None:
        return list(cas_du_theme)
    chemin = trouver_theme()
    if chemin is None or not chemin.is_file():
        return None
    try:
        with open(chemin, "r", encoding="utf-8") as flux:
            return list(json.load(flux).get("theme", {}).get("redirects", []))
    except (OSError, ValueError):
        return None


def mots_significatifs(texte):
    """Les mots qui peuvent fonder un doublon : longs, hors mots generiques."""
    propres = []
    for brut in str(texte or "").lower().replace("'", " ").split():
        mot = "".join(c for c in brut if c.isalnum() or c in "-_")
        if len(mot) >= LONGUEUR_MOT_SIGNIFICATIF and mot not in MOTS_GENERIQUES:
            if mot not in propres:
                propres.append(mot)
    return propres


def doublon_avec(titre, titres_existants):
    """Le titre existant qui fait DOUBLON avec celui-ci, ou None (REGLE, pas avis).

    La regle est DECLAREE et MESUREE : au moins MOTS_COMMUNS_POUR_DOUBLON mots
    significatifs communs. Un jumeau trouve n'arrete PAS le travail -- il l'evite :
    le module dit quel item porte deja le sujet et ne depose pas un doublon.
    """
    mes_mots = set(mots_significatifs(titre))
    for existant in titres_existants:
        communs = mes_mots & set(mots_significatifs(existant))
        if len(communs) >= MOTS_COMMUNS_POUR_DOUBLON:
            return existant, sorted(communs)
    return None, []


def constituer_la_chaine(titre, demande, cas_du_theme=None, type_mission=""):
    """La SUITE ORDONNEE des missions pour cette demande -- sans aucune question.

    Rend une liste de maillons : {"case", "type", "objectif", "preuve", "ordre"}.
    Les cases viennent du THEME (son domicile) ; la table ci-dessus dit ce que
    chacune devient. Un cas du theme sans entree dans la table est DIT (jamais
    silencieusement saute : la chaine doit couvrir ses propres cases).
    """
    maillons = []
    cases = charger_cases(cas_du_theme)
    if cases is None:
        # LE THEME INTROUVABLE EST UN MAILLON, PAS UN SILENCE : sans lui la chaine
        # n'aurait qu'une ligne (la mission) et se lirait comme complete.
        maillons.append({
            "case": "theme-introuvable", "ordre": 1, "type": "reparation",
            "objectif": ("[THEME-INTROUVABLE] Le domicile des regles du cadrage"
                         " (" + NOM_THEME_CADRAGE + ") n'a pas ete trouve depuis "
                         + str(Path(__file__).resolve().parent) + " : les cases du"
                         " parcours ne peuvent pas etre lues, donc la chaine serait"
                         " incomplete. Reparer le chemin AVANT tout cadrage."),
            "preuve": ("le theme lu, et ses cases servies : le VERIFIER par la"
                       " commande qui l'a trouve (a REJOUER)"),
            "regle": "un domicile illisible se DIT : une chaine qui n'a pas pu lire"
                     " ses regles ne peut pas se declarer complete"})
        cases = []
    case_par_nom = {nom: (typ, obj, preuve) for nom, typ, obj, preuve in MAILLONS_DECLARES}
    for indice, cas in enumerate(cases):
        besoin = str(cas.get("besoin", ""))
        # Le NOM de la case est ce qui vit ENTRE les crochets (`[manques] -- dire ce
        # qu'on sait`). Mesure du 2026-09-21 : `strip("[] ")` laissait le crochet
        # fermant colle au nom ("depot]"), donc AUCUNE case ne retrouvait sa ligne
        # dans la table et les six tombaient en "case non declaree" -- avec l'air
        # d'une chaine complete.
        nom = ""
        debut = besoin.find("[")
        fin = besoin.find("]", debut + 1) if debut >= 0 else -1
        if debut >= 0 and fin > debut:
            nom = besoin[debut + 1:fin].strip()
        declare = case_par_nom.get(nom)
        if declare is None:
            maillons.append({
                "case": nom, "ordre": indice + 1, "type": "audit",
                "objectif": ("CASE NON DECLAREE dans la table des maillons ("
                             + besoin + ") : a declarer dans cadrage.py -- jamais"
                             " sautee en silence."),
                "preuve": ("la declaration de cette case dans la table, VERIFIEE"
                           " par le garde des maillons"),
                "regle": str(cas.get("regle", ""))})
            continue
        type_case, objectif, preuve = declare
        maillons.append({
            "case": nom, "ordre": indice + 1, "type": type_case,
            "objectif": ("[" + nom.upper() + "] " + objectif + "\n\nDEMANDE DU"
                         " CREATEUR : " + titre + ("\n\n" + demande if demande else "")),
            "preuve": preuve,
            "regle": str(cas.get("regle", ""))})
    # LES TROIS CASES EXIGEES, PRESENCE ET ORDRE (EO-475, 2026-09-30). Le miroir
    # ci-dessus verifie l ACCORD entre le theme et la table ; il ne verifie ni que
    # les trois cases exigees SOIENT la, ni qu elles soient DANS L ORDRE.
    # MESURE (le trou, avant la reparation) : [expertise]-retiree des DEUX cotes
    # (le theme ET la table) rend un miroir VERT -- accuses vide, chaine de 9
    # maillons au lieu de 10, et la demande du createur disparait sans un mot. Le
    # miroir est de plus UNIDIRECTIONNEL : il parcourt les cases du THEME, donc une
    # case que le THEME perd et que la TABLE garde passe aussi sans etre accusee.
    # C est le meme defaut des deux cotes, et il se ferme sur les NOMS servis.
    for ecart in controler_cases_exigees([maillon["case"] for maillon in maillons]):
        maillons.append({
            "case": "cases-exigees", "ordre": len(maillons) + 1,
            "type": "reparation",
            "objectif": ("[" + ecart + "] Les TROIS cases que le createur a exigees"
                         " avant la mission finale (expertise et sa contre-expertise,"
                         " oui-mais, si j etais user) ne sont pas toutes presentes, ou"
                         " ne sont pas dans l ordre exige. Le MIROIR theme <-> table"
                         " ne le voit pas : il verifie l ACCORD, pas l EXISTENCE, et"
                         " il est unidirectionnel. Reparer le parcours ou cette table"
                         " -- jamais sauter la case en silence."),
            "preuve": ("les trois cases du parcours relues, presence ET ordre, par la"
                       " commande qui les lit (a REJOUER)"),
            "regle": "trois cases exigees, trois cases servies : l ordre compris"})
    # LA DERNIERE LIGNE (regle de [chaine]) : la mission reelle. Elle est TOUJOURS
    # presente : une chaine sans fin n'est pas une chaine.
    maillons.append({
        "case": "mission", "ordre": len(maillons) + 1,
        "type": type_mission or TYPE_MISSION_DEFAUT,
        "objectif": ("[MISSION] " + titre + "\n\nLA MISSION REELLE, a mener apres"
                     " les maillons : " + ACTION_DIRECTE + ACTION_DIRECTE_SUITE
                     + " -- le CODE ou l'OUTIL a reparer est celui que les maillons"
                     " precedents ont nomme.\n\n" + demande),
        "preuve": ("le resultat demande, prouve : mesure avant/apres, et un COBAYE"
                   " pour le cas nouveau ; la non-regression a VERIFIER par le"
                   " lanceur de non-regression"),
        "regle": "aucune liste sans sa derniere ligne : la mission"})
    return maillons


# LES TROIS CASES QUE LE CREATEUR EXIGE (EO-464, 2026-09-28) -- et, depuis EO-475,
# leur PRESENCE et leur ORDRE sont exiges aussi. La table MAILLONS_DECLARES les
# DECLARE ; ce controle les EXIGE. Un domicile pour l idee (M-076) : la liste des
# trois vit ici, la table les sert, le controle les verifie -- jamais trois copies.
CASES_EXIGEES = ("expertise", "oui, mais...", "si j'etais user")


def controler_cases_exigees(noms_cases):
    """Rend la liste des ECARTS entre les cases exigees et celles du parcours.

    Vide = conforme. Chaque ecart est une PHRASE, jamais un booleen : un garde qui
    sait dire POURQUOI est un garde qu on peut reparer.

    Les absences sont renduES avant l ordre, et l ordre ne se juge que si les trois
    sont la : un parcours qui a perdu une case ne se repare pas en remettant les
    deux autres dans l ordre, il se repare en rendant la troisieme.
    """
    ecarts = []
    presents = [nom for nom in noms_cases if nom in CASES_EXIGEES]
    for exigee in CASES_EXIGEES:
        if exigee not in presents:
            ecarts.append("CASE EXIGEE ABSENTE : [" + exigee + "] ne figure pas dans"
                          " le parcours servi (cases presentes : "
                          + (", ".join(noms_cases) if noms_cases else "aucune") + ")")
    if not ecarts and tuple(presents) != CASES_EXIGEES:
        rendu = " -> ".join("[" + nom + "]" for nom in presents)
        attendu = " -> ".join("[" + nom + "]" for nom in CASES_EXIGEES)
        ecarts.append("CASES EXIGEES DANS LE DESORDRE : le parcours les sert dans"
                      " l ordre " + rendu + " ; l ordre exige est " + attendu)
    return ecarts


def texte_de_la_chaine(maillons, doublon=None):
    """Le rendu lisible de la chaine (ce que le createur LIT, sans intervenir)."""
    lignes = ["CHAINE CONSTITUEE -- " + str(len(maillons)) + " maillon(s),"
              " ordonnee(s), chacun TYPE et PROUVABLE"]
    if doublon:
        lignes.append("  DOUBLON RESOLU PAR REGLE : " + doublon[0]
                      + " porte deja ce sujet (mots communs : "
                      + ", ".join(doublon[1]) + ") -- aucun doublon depose.")
    for maillon in maillons:
        lignes.append("  " + str(maillon["ordre"]) + ". [" + maillon["case"] + "]"
                      " type=" + maillon["type"])
        lignes.append("     preuve attendue : " + maillon["preuve"][:150])
    lignes.append("  FIN : le dernier maillon est LA MISSION (jamais oubliee).")
    return "\n".join(lignes)


def verser(maillons, chemin_depot, theme, urgence="normale", source="createur",
           trace="", simuler=False):
    """Verse la chaine par la PORTE de depot (regle de [depot] : jamais contournee).

    Rend (deposes, refus) : chaque refus est NOMME avec le code de la porte. Le
    module ne rejoue PAS la porte et ne devine pas ses regles : il l'appelle, et il
    rapporte ce qu'elle a dit -- c'est ce qui rend le versement verifiable.

    Le CHEMIN de la porte est RECU, jamais recalcule : l'appelant en est le
    domicile (filtrer/entry.py le detecte par marqueur). Le 2026-09-21, le module
    l'a recalcule lui-meme (`pilote/main.py`) et la porte a refuse les 7 maillons en
    imprimant le docstring du PILOTE : une porte qu'on appelle au mauvais chemin ne
    dit pas < je ne suis pas la porte >, elle dit n'importe quoi -- et la chaine
    semblait versee.
    """
    commande_base = [sys.executable, str(chemin_depot), "deposer",
                     "--theme", theme, "--objectif", "", "--urgence", urgence,
                     "--source", source, "--trace", trace]
    deposes, refus = [], []
    for maillon in maillons:
        objectif = maillon["objectif"] + "\n\nPREUVE ATTENDUE : " + maillon["preuve"]
        commande = list(commande_base)
        commande[commande.index("--objectif") + 1] = objectif
        # Le TYPE est DECLARE a la naissance : c'est la regle de [chaine] (aucun
        # maillon sans type declare) ET la fin du litige 3 (item non executable).
        commande += ["--type", maillon["type"]]
        if simuler:
            deposes.append((maillon["case"], "SIMULE -- commande : "
                           + " ".join(commande[1:6])))
            continue
        try:
            termine = lancer_enfant(commande, capture_output=True, text=True,
                                     encoding="utf-8", errors="replace", timeout=60)
        except (OSError, subprocess.SubprocessError) as erreur:
            refus.append((maillon["case"], "porte injoignable : " + repr(erreur)))
            continue
        sortie = (termine.stdout or termine.stderr or "").strip()
        if termine.returncode == 0:
            # Ce qu'on RAPPORTE est la ligne de l'IDENTITE (celle qui porte l'id rendu
            # par la porte), jamais la derniere ligne : mesure du 2026-09-21, la
            # derniere ligne etait un conseil generique ("Corriger le ROLE si
            # besoin") -- la chaine paraissait donc n'avoir rien verse de nomme.
            lignes = [ligne for ligne in sortie.splitlines() if ligne.strip()]
            avec_id = [ligne for ligne in lignes if PREFIXE_ITEM in ligne]
            deposes.append((maillon["case"], (avec_id or lignes[-1:])[0].strip()))
        else:
            refus.append((maillon["case"], sortie[:200]))
    return deposes, refus
# --- LA LISTE DE PILOTAGE (regle de [chaine], MO-427) ------------------------
# La chaine existait comme TEXTE imprime : le maillon [chaine] exige qu elle
# devienne un FICHIER DE PILOTAGE (json) ecrit par un OUTIL, jamais un texte
# libre. Le fichier porte ce que le texte ne peut pas : l ORDRE relisible, le TYPE
# et la PREUVE de chaque maillon, et sa derniere ligne (la mission). Il vit dans
# le dossier des chaines (preparation/), celui qui porte deja leurs artifacts
# (index-chaine.md, chaine-compteurs.json) -- jamais un dossier invente.
DOSSIER_LISTE_PILOTAGE = ("_operateur", "optimus-prime", "preparation")
NOM_LISTE_PILOTAGE = "maillons-cadrage.json"
CLE_LISTE_MAILLONS = "maillons"
CLE_LISTE_TITRE = "titre"
CLE_LISTE_DEMANDE = "demande"
CLE_LISTE_SOURCE = "source"
CLE_LISTE_VERSION = "version"
VERSION_LISTE_PILOTAGE = 1
# La PORTE qui ecrit (regle de [depot] : aucun depot ne la contourne). Son chemin
# se RECALCULE du meme ancrage que le reste du module, jamais suppose (L-013).
CHEMIN_PORTE_ECRIRE = _RACINE_LANCEMENT / "matrice" / "data" / "outils" / "ecrire" / "main.py"


def racine_workspace():
    """La racine du WORKSPACE (celle que la porte ECRIRE attend), ou None.

    Mesure du 2026-09-26 : `_RACINE_LANCEMENT` est la Matrice elle-meme
    (`cerveau-projet/matrix`) -- l ancetre du workspace est donc DEUX crans
    au-dessus, et la porte ECRIRE a refuse la premiere pose (le chemin tombait
    sous `cerveau-projet/`, hors perimetre) au lieu de la poser ailleurs en
    silence : une porte qui refuse NOMME son perimetre.
    """
    return _RACINE_LANCEMENT.parent.parent


def chemin_liste_pilotage():
    """Le chemin ABSOLU de la liste, ou None (jamais un chemin DEVINE).

    Le dossier de la liste est relatif a la MATRICE (`_operateur/...`), pas au
    workspace : la mesure du 2026-09-26 l a paye -- jointe a l ancetre du
    workspace, la liste tombait sous `cerveau-projet/`, HORS perimetre, et la
    porte l a refusee. Une racine qui sert a DEUX choses se nomme deux fois.
    """
    base = _RACINE_LANCEMENT
    if base is None:
        return None
    return base.joinpath(*DOSSIER_LISTE_PILOTAGE).joinpath(NOM_LISTE_PILOTAGE)


def liste_de_pilotage(maillons, titre, demande, source):
    """Le CONTENU de la liste : ordre, TYPE et PREUVE NOMMES, derniere ligne incluse."""
    return {
        CLE_LISTE_VERSION: VERSION_LISTE_PILOTAGE,
        CLE_LISTE_TITRE: str(titre or ""),
        CLE_LISTE_DEMANDE: str(demande or ""),
        CLE_LISTE_SOURCE: str(source or ""),
        CLE_LISTE_MAILLONS: [
            {"ordre": int(maillon.get("ordre", 0)),
             "case": str(maillon.get("case", "")),
             "type": str(maillon.get("type", "")),
             "preuve": str(maillon.get("preuve", "")),
             "objectif": str(maillon.get("objectif", ""))}
            for maillon in maillons],
    }


def texte_de_la_liste(donnees):
    """Le TEXTE de la liste : ASCII strict (les accents sortent echappes), STABLE.

    L ASCII n est pas une coquetterie : la porte ECRIRE CORRIGE les fautes
    d encodage futiles, et un texte qui change en traversant la porte ne peut plus
    etre compare a ce qu on croyait avoir ecrit.
    """
    return json.dumps(donnees, ensure_ascii=True, indent=2) + chr(10)


def ecrire_liste_de_pilotage(maillons, titre, demande, source, chemin_demande=""):
    """ECRIT la liste par la PORTE ECRIRE. Rend (code, sortie).

    Un chemin DEMANDE (option --liste-fichier) est resolu contre la racine du
    workspace ; un chemin VIDE vise le domicile declare de la liste. La porte est
    APPELEE, jamais imitee : une liste ecrite a la main se lirait comme un artefact
    produit (regle de [depot]).
    """
    if chemin_demande:
        chemin = Path(chemin_demande)
        if not chemin.is_absolute():
            base = racine_workspace()
            chemin = (base / chemin) if base is not None else chemin.resolve()
    else:
        chemin = chemin_liste_pilotage()
    if chemin is None:
        return 2, "REFUS : racine du workspace introuvable -- la liste n est pas ecrite."
    if not CHEMIN_PORTE_ECRIRE.is_file():
        return 2, ("REFUS : porte ECRIRE introuvable (" + str(CHEMIN_PORTE_ECRIRE)
                   + ") -- la liste n est pas ecrite.")
    donnees = liste_de_pilotage(maillons, titre, demande, source)
    # Le transport est BASE64 : le texte du json ne traverse aucune couche capable
    # de le deformer (guillemets, apostrophes, accents echappes) -- EO-156/MO-173.
    blob = base64.b64encode(texte_de_la_liste(donnees).encode("utf-8")).decode("ascii")
    commande = [sys.executable, str(CHEMIN_PORTE_ECRIRE), "ecrire",
                "--fichier", str(chemin), "--mode", "remplacer",
                "--contenu-base64", blob]
    try:
        termine = lancer_enfant(commande, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=60)
    except (OSError, subprocess.SubprocessError) as erreur:
        return 2, "REFUS : porte ECRIRE injoignable : " + repr(erreur)
    return termine.returncode, ((termine.stdout or "") + (termine.stderr or "")).strip()
