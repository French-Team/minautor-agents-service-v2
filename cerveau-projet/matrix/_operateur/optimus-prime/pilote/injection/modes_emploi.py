#!/usr/bin/env python3
"""modes_emploi.py -- LE MODE D EMPLOI D UNE BRIQUE, extrait de SON domicile.

POURQUOI (revision createur du 2026-09-20, EO-311 / mission MO-313) : l injection
"outils-disponibles" du catalogue servait un os.listdir -- des NOMS, __pycache__ et
les points de restauration .bak compris, et AUCUN usage. Le createur : "fournir des
outils, combos, super-combos sans explication n est pas productif et genere des
actions inutiles". Or proto-6 etape 2 PROMET DEJA "les interfaces FERMEES des outils
que la mission va appeler (usage main.py, codes 0/1/2)" : le protocole disait vrai,
le CATALOGUE ne le faisait pas.

LA REGLE N EST PAS RECOPIEE (M-076 / L-032) : le mode d emploi d une brique est ce
que la BRIQUE dit d ELLE-MEME -- le docstring de son main.py, ou la premiere ligne
de son README quand il n y a pas de docstring. Une fiche ecrite a cote (une copie)
divergerait en silence : c est exactement ce que ce module refuse.

UNE BRIQUE, C EST QUOI : un .py, ou un dossier qui porte un main.py. Les points de
restauration (*.bak*), __pycache__, les documents (*.md) et les donnees (*.json) ne
sont PAS des briques -- ils polluaient la liste servie a l agent.

L API DES CONSOMMATEURS -- trois fonctions, un seul sens :
  - `trouver_brique(nom)`   : le CHEMIN de la brique nommee, ou None -- LA resolution ;
  - `noms_servables()`      : les noms servables (sert au refus ET a la preuve) ;
  - `refus_nom(nom)`        : le refus NOMME (nom fautif, proches, remede).
`mode_emploi_brique(nom)` les consomme. La porte `preparer` de l entonnoir (EO-313)
les consomme AUSSI, par le meme domicile : un nom que la porte accepte est un nom
que l injection sait servir -- jamais l inverse.

UN MODE D EMPLOI MANQUANT EST ACCUSE, JAMAIS TU : une brique sans usage lisible rend
un texte qui le DIT (le remede est de l ecrire dans la brique, son domicile).

Usage:
  python modes_emploi.py carte [--racine <racine>]
  python modes_emploi.py mode-emploi <nom>
  python modes_emploi.py --auto-test
"""
import sys
from pathlib import Path

# --- LE DOMICILE DES REGLES PARTAGEES (M-076 / MO-468) -----------------------
# La regle des noms proches vit a UN SEUL domicile (matrice/data/commun/noms_proches.py) :
# le pilote la CONSOMME, il ne la recopie pas. Ce module est lance SEUL (par l injection,
# par l entonnoir, par un garde), donc il installe lui-meme le chemin -- par MARQUEUR
# (MO-088 : aucun parents[N] nu) et il REFUSE plutot que de deviner (garde-foi L-006).
_RACINE_MATRIX = Path(__file__).resolve().parent
while _RACINE_MATRIX.name != "matrix":
    if _RACINE_MATRIX.parent == _RACINE_MATRIX:
        raise RuntimeError("racine `matrix` introuvable en remontant depuis " + __file__)
    _RACINE_MATRIX = _RACINE_MATRIX.parent
_DOMICILE_COMMUN = _RACINE_MATRIX / "matrice" / "data" / "commun"
if not (_DOMICILE_COMMUN / "noms_proches.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(_DOMICILE_COMMUN)
                       + " ne porte pas le domicile des noms proches")
if str(_DOMICILE_COMMUN) not in sys.path:
    sys.path.insert(0, str(_DOMICILE_COMMUN))
from noms_proches import NOMBRE_PROCHES, proches  # noqa: E402


# --- DOMICILES DE LA DECOUVERTE, declares une fois ---------------------------
# Ou une brique dit son usage, dans l ORDRE ou on le cherche : le docstring du
# module d entree d abord (le contrat de la porte elle-meme), puis son document.
NOMS_DOCUMENTS = ("DESCRIPTION.md", "README.md", "README-*.md")
# Un mode d emploi est MINI par construction : on borne, et la coupe est DITE.
PLAFOND_LIGNES_USAGE = 8
# PLAFOND DES BRIQUES SERVIES PAR UNE CARTE (demande createur du 2026-09-20, MO-314) :
# mesure avant de le poser -- avant-mission pesait 8004 tokens, dont 2452 pour les
# QUATRE cartes (31 pour cent de l injection). La carte est une MEMOIRE, pas le
# manuel : au-dela, le detail se demande pour la brique voulue (mode-emploi <nom>).
# La coupe est TOUJOURS DITE, et la carte complete reste accessible (--complet) :
# un plafond qui cache sans le dire serait un bandeau sur les yeux (L-055).
PLAFOND_BRIQUES_CARTE = 30
PLAFOND_LIGNES_BUT = 100
MARQUE_COUPE = " [...]"
# Non-briques : jamais servies (mesure du defaut : __pycache__ et .bak etaient dans
# la liste remise a l agent).
EXCLUSIONS = ("__pycache__",)
SUFFIXES_EXCLUS = (".bak", ".pyc", ".md", ".json", ".txt")
SUFFIXE_BRIQUE = ".py"
NOM_ENTREE = "main.py"

# Les RACINES des briques, declarees ici (un seul domicile). MEME FORME que les
# `source` du catalogue d injection : RELATIVES AU PILOTE (jamais au dossier du
# module) -- deux formes pour un meme chemin, c est deux verites.
PILOTE = Path(__file__).resolve().parent.parent
RACINES = {
    "outils": "../super-combos/combos/outils",
    "combos": "../super-combos/combos",
    "super-combos": "../super-combos",
    "outils-matrice": "../../../matrice/data/outils",
}

# LE PLANCHER DES CARTES -- les briques qu une carte ne cache JAMAIS. Le plafond
# coupe par la FIN : le plancher se place donc EN TETE, et une essentielle ne peut
# plus tomber par la seule vertu de son INITIALE.
#
# LA MESURE QUI L A RENDU NECESSAIRE (2026-09-25, journal des usages --
# matrice/data/usages-outils-combos.jsonl) : la coupe alphabetique de la carte des
# portes cachait suivi-optimus, LA BRIQUE LA PLUS APPELEE DE TOUTE LA MATRICE, et
# sept autres des plus appelees, pendant que la meme carte servait bdd-usages.
# Chaque nom porte son chiffre : ce n est pas un gout, c est le classement des
# usages REELS.
#
# DECISION DU CREATEUR (2026-09-27, MO-454) : ETENDRE le plancher d essentielles
# plutot que monter le plafond -- le plafond reste a 30 et le poids d injection ne
# bouge pas. Le critere est DECLARE, jamais un gout :
#   - la carte des OUTILS-MATRICE a un journal d usages : le plancher = le TOP du
#     classement (les plus appelees) PLUS deux roles qui ne se mesurent pas a
#     l usage (theme-vivier : la source d identite ; signaler : le geste par lequel
#     un agent declare un probleme) ;
#   - la carte des OUTILS n a AUCUNE donnee d usage (une brique lancee seule ne se
#     note pas) : le plancher = les GARDES DU PROCESS, ceux que le round lance ou
#     subit -- le critere est ecrit dans la declaration, jamais devine.
# L INVARIANT : un plancher ne peut JAMAIS depasser le plafond, sans quoi la carte
# en couperait elle-meme -- l autotest le crie (le plancher est une GARANTIE).
BRIQUES_TOUJOURS = {
    "outils-matrice": (
        "ecrire",                 # 3 710 -- la porte d ecriture : tout passe par elle
        "suivi-optimus",          # 3 178 -- la trace des missions
        "corriger-ascii",         # 2 802
        "bdd-activites",          # 2 588
        "bdd-conservation",       # 2 345
        "journal-multi-encarts",  # 2 342
        "bdd-modifications",      # 2 332
        "rechercher",             # 2 293 -- le moteur, seul chemin vers la memoire
        "bdd-sessions",           # 1 532
        "machine-defcon",         # 1 438
        "bdd-lecons",             # 1 434
        "verifier-regles",        # 1 432
        "selecteur-flux",         # 1 423 -- le flux actif
        "bdd-protocoles-matrice", # 1 417
        "verifier-protocoles",    # 1 416
        "bdd-regles-matrice",     # 1 413
        "bdd-conventions-matrice",# 1 412
        "verifier-conventions",   # 1 410
        "registre-outils",        # 1 406
        "dupliquer-template",     # 1 398
        "pause-session",          # 1 387
        "chaine-pense-bete",      # 1 381
        "bdd-variables",          # 1 378
        "lister",                 # 1 378
        "theme-vivier",           # ROLE -- la source d identite de l agent
        "signaler",               # ROLE -- declarer un probleme
    ),
    "outils": (
        "fichiers-travail.py",            # la fiche technique de travail du round
        "suivi-pilote.py",                # la vue du brin, les dormeurs
        "lanceur-non-regression.py",      # la suite du depot
        "lanceur-non-regression-flux.py", # la suite du FLUX
        "garde-ascii.py",                 # l ASCII avant publication
        "garde-flux2.py",                 # la frontiere des deux flux
        "garde-perimetre-write.py",       # le perimetre d ecriture
        "garde-residus-zone.py",          # les residus de zone jetable
        "garde-tmp.py",                   # la zone tmp
        "garde-versions.py",              # les versions des briques
        "verifier-contrat-fondamental.py",# le contrat fondamental
        "verifier-maillons.py",           # les maillons de la suite
        "verifier-commandes.py",          # les chemins ancres des commandes
        "verifier-resolution.py",         # le nom rend la brique
        "verifier-contrats-outils.py",    # les contrats des outils
        "revert-fichier.py",              # le retour arriere
        "dry-run.py",                     # la repetition avant l acte
        "creer-outil.py",                 # la fabrique d outil
        "creer-combo.py",                 # la fabrique de combo
        "poser-template-pilote.py",       # la pose de template
        "controle-attribution.py",        # qui a fait quoi
        "bdd-frictions",                  # la memoire des frictions
        "bdd-lecons-matrice",             # la memoire des lecons
        "bdd-modifs",                     # la memoire des modifications
    ),
}


def plancher_de(racine):
    """Les briques que la carte de CETTE racine ne cache jamais (plancher declare).

    Rend un tuple VIDE quand la racine n est pas une racine declaree (un arbre
    jetable n a pas de plancher) : le plancher se LIT ici, jamais recopie.
    """
    cible = Path(racine).resolve()
    for cle, relative in RACINES.items():
        if (PILOTE / relative).resolve() == cible:
            return BRIQUES_TOUJOURS.get(cle, ())
    return ()


def ordonner(briques, racine):
    """Les briques d une carte : le PLancher EN TETE, puis l ordre habituel (nom).

    Le plafond coupe par la FIN : c est ce placement qui rend une essentielle
    increvable. Aucune brique n est ajoutee ni retiree ici -- l ORDRE seul change,
    et le contenu de la carte reste la verite de la racine.
    """
    par_nom = {brique.name: brique for brique in briques}
    # DANS L ORDRE DECLARE : la priorite du plancher est une INFORMATION (pourquoi
    # suivi-optimus avant ecrire se lit dans la declaration), pas un tri a refaire.
    # Un nom declare qui n existe pas sous cette racine est ECARTE ici -- et c est le
    # GARDE qui l accuse (contrat des modes d emploi), jamais un silence : une faute de
    # frappe dans le plancher doit crier, pas proteger personne en cachette.
    premieres = [par_nom[nom] for nom in plancher_de(racine) if nom in par_nom]
    gardees = {brique.name for brique in premieres}
    autres = [brique for brique in briques if brique.name not in gardees]
    return premieres + autres


def _est_brique(chemin):
    """Un .py, ou un dossier qui porte un main.py. Sinon : jamais une brique."""
    nom = chemin.name
    if nom in EXCLUSIONS or any(motif in nom for motif in SUFFIXES_EXCLUS):
        return False
    if chemin.is_file():
        return chemin.suffix == SUFFIXE_BRIQUE
    if chemin.is_dir():
        return (chemin / NOM_ENTREE).is_file()
    return False


def lister_briques(racine):
    """Les briques d une racine, par ordre de nom. Racine absente : liste vide."""
    racine = Path(racine)
    if not racine.is_dir():
        return []
    return sorted((p for p in racine.iterdir() if _est_brique(p)),
                  key=lambda p: p.name.lower())


def chemin_brique(racine, nom):
    """Le chemin de la brique nom sous racine, ou None (jamais une devinette)."""
    candidat = Path(racine) / nom
    return candidat if _est_brique(candidat) else None


def premier_document(brique):
    """Le texte ou la brique dit ce qu elle est : son docstring, ou son document.

    Rend (texte, origine) : l ORIGINE est dite, parce qu un mode d emploi sans
    temoin se lit comme une affirmation en l air.
    """
    brique = Path(brique)
    fichiers = [brique] if brique.is_file() else [brique / NOM_ENTREE]
    for nom in NOMS_DOCUMENTS:
        fichiers.extend(sorted(brique.glob(nom)) if brique.is_dir() else [])
    for fichier in fichiers:
        if not fichier.is_file():
            continue
        try:
            texte = fichier.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if texte.strip():
            return texte, fichier.name
    return "", ""


def docstring(texte):
    """Le docstring d un module Python : le PREMIER bloc a TRIPLE GUILLEMET.

    DEUX FORMES, ET LA PREMIERE GAGNE (mesure du 2026-09-25) : le triple guillemet
    DOUBLE et le triple guillemet SIMPLE. Ne connaitre que le double rendait
    INVISIBLE le docstring d une brique ecrite avec le simple, et l extracteur allait
    lire PLUS LOIN -- chez la premiere fonction venue : le mode d emploi servi etait
    alors celui d une AUTRE chose. Cas mesure : espion-sondes-optimus.py (docstring
    en guillemet simple, 1 600 caracteres) annoncait < Le SEUL lancement de processus
    de cet outil >, le docstring d une aide locale. C est le PREMIER des deux dans le
    fichier qui gagne, parce que c est celui que Python retient comme __doc__.
    """
    marques = [position for position in (texte.find("\"\"\""), texte.find("'''"))
               if position >= 0]
    if not marques:
        return ""
    marque = min(marques)
    guillemets = texte[marque:marque + 3]
    fin = texte.find(guillemets, marque + 3)
    return texte[marque + 3:fin] if fin > 0 else ""


def but(texte):
    """La PREMIERE ligne qui dit a quoi sert la brique (le but, en une ligne)."""
    for ligne in texte.splitlines():
        ligne = ligne.strip()
        if ligne and not ligne.startswith("#") and not ligne.startswith("-"):
            return ligne[:PLAFOND_LIGNES_BUT]
    return ""


def bloc_usage(texte):
    """Les lignes du bloc Usage (bornees), ou "" : une brique peut ne pas en avoir.

    Le bloc commence a une ligne Usage et s arrete a la premiere ligne qui ne
    ressemble plus a une commande : un mode d emploi ne deverse pas la brique.
    """
    lignes = texte.splitlines()
    depart = None
    retenues = []
    for index, ligne in enumerate(lignes):
        if ligne.strip().lower().startswith("usage"):
            # DEUX FORMES MESUREES dans les briques : la commande EN LIGNE
            # (Usage: python x.py --y, forme des super-combos) et le bloc INDENTE
            # sous le label (Usage : puis 4 espaces, forme des outils de la Matrice).
            # N en lire qu une seule rendait un mode d emploi VIDE sur la moitie du
            # parc -- et c est l AUTOTEST qui l a crie, pas une relecture.
            reste = ligne.split(":", 1)[1].strip() if ":" in ligne else ""
            if reste:
                retenues.append(reste)
            depart = index + 1
            break
    if depart is None:
        return ""
    for ligne in lignes[depart:]:
        if not ligne.strip():
            if retenues:
                break
            continue
        if not (ligne.startswith((" ", "\t")) or ligne.lstrip().startswith(("python", "-", "$"))):
            break
        retenues.append(ligne.rstrip())
        if len(retenues) >= PLAFOND_LIGNES_USAGE:
            retenues.append(MARQUE_COUPE.strip())
            break
    return "\n".join(retenues)

def extrait(brique):
    """Le (BUT, USAGE, ORIGINE) d une brique -- les trois morceaux SEPARES.

    L API que consomme le REGISTRE DES OUTILS (EO-314) : le registre range le but et
    le snippet dans la BDD, avec l empreinte de leur source pour dire QUAND ils
    periment. Le mode d emploi du pilote, lui, les recolle : `mode_emploi` consomme
    CETTE fonction -- deux lectures d une meme brique divergeraient (M-076).

    Rend ("", "", "") quand la brique ne dit rien d elle-meme : l appelant en fait
    une ACCUSATION, jamais un silence.
    """
    texte, origine = premier_document(brique)
    if not texte:
        return "", "", ""
    corps = docstring(texte) if origine.endswith(".py") else texte
    if not [ligne for ligne in corps.splitlines() if ligne.strip()]:
        return "", "", origine
    return but(corps), bloc_usage(corps), origine


def mode_emploi(brique):
    """Le MINI mode d emploi d une brique : son but, puis son usage.

    Rend (texte, origine) ; texte VIDE quand la brique ne dit rien d elle-meme --
    l appelant en fait une ACCUSATION, jamais un silence.
    """
    but_brique, usage, origine = extrait(brique)
    if not but_brique and not usage:
        return "", origine
    return "\n".join([but_brique] + ([usage] if usage else [])), origine


def trouver_brique(nom):
    """Le CHEMIN de la brique nommee dans les racines declarees, ou None.

    LA RESOLUTION VIT ICI, UNE SEULE FOIS (M-076) : elle est consommee par
    `mode_emploi_brique` (l injection) ET par la porte `preparer` de l entonnoir
    (EO-313). Pourquoi la MEME : une porte qui accepterait un nom que l injection
    ne sait pas servir ferait ACCUSER par le garde une mission qu elle a prise
    elle-meme -- la porte doit valider contre ce que le consommateur sert vraiment.
    """
    for cle in sorted(RACINES):
        brique = chemin_brique((PILOTE / RACINES[cle]).resolve(), nom)
        if brique is not None:
            return brique
    return None


def noms_servables():
    """Les NOMS des briques servables (toutes racines), tries -- sert au refus.

    Une carte dit le BUT de chaque brique ; cette liste dit les NOMS que la porte
    `preparer` peut accepter, et rien de plus.
    """
    noms = []
    for cle in sorted(RACINES):
        for brique in lister_briques((PILOTE / RACINES[cle]).resolve()):
            if brique.name not in noms:
                noms.append(brique.name)
    return sorted(noms)


def refus_nom(nom):
    """Le refus NOMME d un nom non servable : le nom fautif, les proches, le remede.

    Meme discipline que le refuseur de la facade (`data/commun/resolution_outils.py`) :
    un refus qui ne dit QUE non oblige a deviner le geste juste.

    LA REGLE DES PROCHES N EST PLUS RECOPIEE (MO-468) : elle vit a UN SEUL domicile
    (`data/commun/noms_proches.py`, M-076) et les DEUX refuseurs la consomment. Cette
    copie ne cherchait que la SOUS-CHAINE : un nom fautif d UNE LETTRE ne proposait
    RIEN, la ou la facade proposait deja -- deux comportements sous un meme nom de
    regle (L-029).
    """
    trouves = proches(nom, noms_servables())[:NOMBRE_PROCHES]
    message = "nom non servable : " + repr(nom)
    if trouves:
        message += " -- proches : " + ", ".join(trouves)
    return message + " -- une brique est un .py ou un dossier a main.py des racines : " + ", ".join(sorted(RACINES))


def mode_emploi_brique(nom):
    """Le mode d emploi d une brique NOMMEE, cherchee dans les racines declarees.

    C est l API que le PILOTE consomme a l injection. Rend (texte, origine) ;
    ("", "") quand le nom ne designe AUCUNE brique -- le consommateur le DIT : une
    brique demandee et introuvable est un ECART, jamais un silence (et c est ce que
    le garde des contrats accuse).
    """
    brique = trouver_brique(nom)
    return mode_emploi(brique) if brique is not None else ("", "")


def ligne_carte(brique):
    """UNE ligne par brique pour la CARTE : le nom, son but, et le defaut s il y en a."""
    texte, origine = mode_emploi(brique)
    if not texte:
        return "  " + brique.name + " : AUCUN MODE D EMPLOI (a poser dans la brique)"
    return "  " + brique.name + " : " + texte.splitlines()[0]


# --- LE DECLENCHEUR DE L ETAT D EXECUTION (MO-577) --------------------------------
# La chaine pense-bete etait deja au PLANCHER de chaque injection -- donc l agent la
# voyait -- mais AUCUN code ne l appelait jamais : le lien entre la porte et le
# moment ou elle sert n existait pas. C est le troisieme maillon que l audit nomme.
#
# LE RAPPEL EST DIT, JAMAIS JOUE. Un declencheur qui poserait `execute` tout seul a la
# cloture de chaque mission ecrirait dans la zone du createur (l espace
# preparation) sans qu il l ait demande, et le ferait sur une PREUVE qu il n a pas
# choisie. Le rappel se contente de nommer l objet, son statut et le geste ; la
# decision, et la preuve, restent a l agent et au createur.
NOM_CHAINE = "chaine-pense-bete"
CHEMIN_CONSTANTES_CHAINE = ("matrice", "data", "outils", NOM_CHAINE, "constants.py")


def _declarations_de_la_chaine(racine):
    """Les constantes de la porte, LUES (jamais recopiees) ; {} si elle est absente.

    Le domicile de la chaine est une donnee de la PORTE : le recopier ici
    rejouerait le vice que le projet compte (un chemin dit a un endroit et vivant
    a un autre -- MO-575). On lit, et on ne devine rien.
    """

    import importlib.util
    # LA RACINE SE REMONTE PAR MARQUEUR (L-013), jamais par `parents[N]`. La
    # carte est rendue par DOMICILE (`carte(_operateur/.../pilote)`), donc un
    # `joinpath` sur la racine rendue -- premiere version de ce code : le rappel
    # disait "porte absente" sur les quatre cartes du parc.
    chemin = None
    courant = Path(racine).resolve()
    for candidat in (courant,) + tuple(courant.parents):
        essaye = candidat.joinpath(*CHEMIN_CONSTANTES_CHAINE)
        if essaye.is_file():
            chemin = essaye
            break
    if chemin is None:
        return {}
    specification = importlib.util.spec_from_file_location("chaine_pense_bete_constantes", chemin)
    if specification is None or specification.loader is None:
        return {}
    try:
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        return {"domicile": getattr(module, "REPERTOIRE_DOMICILE", None),
                "index": getattr(module, "NOM_INDEX", ""),
                "todo": getattr(module, "ETAPE_TODO", "todo")}
    except Exception:
        return {}


def rappel_chaine_pense_bete(racine):
    """Les objets de la chaine dont le travail n est pas constate, ou une ligne qui
    dit qu il n y en a pas.

    LE RAPPEL EST UN FAIT MESURE : il lit l index de la chaine et compte les lignes
    `[todo]`. Il ne devine rien, et il ne se trompe jamais de silence : une chaine
    absente donne la ligne qui le dit, pas un rappelmuet.
    """
    declarations = _declarations_de_la_chaine(racine)
    domicile = declarations.get("domicile")
    if not domicile:
        return "  chaine pense-bete : porte absente -- aucun rappel, aucun travail en attente"
    index = Path(domicile) / (declarations.get("index") or "")
    if not index.is_file():
        return "  chaine pense-bete : aucun objet dans la chaine (index absent)"
    en_attente = []
    for ligne in index.read_text(encoding="utf-8").splitlines():
        propre = ligne.strip()
        if propre.startswith("- ") and ("[" + declarations.get("todo", "todo") + "]") in propre:
            en_attente.append(propre[2:].split("[")[0].strip())
    if not en_attente:
        return ("  chaine pense-bete : aucun objet au statut todo -- tous leurs travaux"
                " sont consignes")
    return ("  chaine pense-bete : " + str(len(en_attente)) + " objet(s) au statut todo ("
            + ", ".join(en_attente) + ") -- si le travail est LIVRE, que la porte le"
            " constate : chaine-pense-bete executer --id " + en_attente[0]
            + " --preuve <le fichier qui le prouve> (la porte refuse sans preuve, et"
            " la preuve se choisit ici, pas dans l injection)")


def carte(racine, plafond=PLAFOND_BRIQUES_CARTE):
    """La CARTE d une racine : une ligne par brique, les manques NOMMES, la coupe DITE.

    Rend (texte, manquantes). Deux choses sont toujours DITES, parce qu une carte
    qui se tait se lit comme une carte complete :
      - les briques SANS mode d emploi (leur nom), pour qu elles se reparent ;
      - les briques NON AFFICHEES quand la carte depasse le plafond, avec le geste
        qui les rend (la carte complete, ou le detail d UNE brique).

    `plafond` par defaut : PLAFOND_BRIQUES_CARTE -- et c est LE MEME defaut pour le
    catalogue et pour le garde qui la juge : deux defauts differents, c est un garde
    qui juge autre chose que ce qui est servi (defaut attrape par l autotest du
    plafond, 2026-09-20). Un plafond a 0 rend TOUT (la carte complete : la voie de
    secours, jamais un blocage).
    """
    briques = ordonner(lister_briques(racine), racine)
    if not briques:
        return "", []
    retenues = briques if not plafond else briques[:plafond]
    lignes = ["CARTE DES BRIQUES -- " + str(racine) + " (" + str(len(briques)) + " brique(s))"]
    manquantes = []
    for brique in retenues:
        lignes.append(ligne_carte(brique))
        if "AUCUN MODE D EMPLOI" in lignes[-1]:
            manquantes.append(brique.name)
    lignes.append("  " + str(len(manquantes)) + " sans mode d emploi sur " + str(len(retenues))
                  + " affichee(s) : " + (", ".join(manquantes) if manquantes else "aucune"))
    restantes = len(briques) - len(retenues)
    if restantes > 0:
        lignes.append("  " + str(restantes) + " brique(s) NON AFFICHEE(S) sur "
                      + str(len(briques)) + " (plafond " + str(plafond) + ") -- detail d une"
                      " brique : python modes_emploi.py mode-emploi <nom> ; carte complete :"
                      " python modes_emploi.py carte <racine> --complet")
    if plancher_de(racine):
        lignes.append("  plancher declare : " + str(len(plancher_de(racine)))
                      + " brique(s) TOUJOURS servie(s) parmi " + str(len(briques))
                      + " (declare au domicile de l extracteur -- jamais coupees)")

    # LE DECLENCHEUR (MO-577) : la carte RAPELLE l objet de la chaine dont le
    # travail reste a constater. Il est dit, pas joue -- et il l est meme quand
    # la carte est coupee par son plafond : c est la ligne qui manque le plus.
    lignes.append(rappel_chaine_pense_bete(racine))
    return "\n".join(lignes), manquantes


def servir(racine, plafond=PLAFOND_BRIQUES_CARTE):
    """Le texte servi par le CATALOGUE pour une racine : une CARTE bornee, jamais une liste nue."""
    texte, manquantes = carte(racine, plafond)
    if not texte:
        return "REFUS : aucune brique sous " + str(racine) + " (racine absente ou vide)."
    return texte


def _epreuve_proximite(servables):
    """COBAYE de la PROXIMITE (MO-468) : une LETTRE OUBLIEE doit etre PROPOSEE.

    C est le defaut MESURE : cette copie ne cherchait que la SOUS-CHAINE, donc
    < suivi-optimu > (une lettre oubliee) ne proposait RIEN. L epreuve lit le parc
    REEL (lecture seule) : elle retire une lettre au MILIEU d un nom servable assez
    long -- le resultat n est alors plus une SOUS-CHAINE du nom, donc seule la
    PROXIMITE du domicile peut le retrouver -- et exige que le nom REEL soit propose.
    """
    for candidat in servables:
        if len(candidat) < 12:
            continue
        milieu = len(candidat) // 2
        essai = candidat[:milieu] + candidat[milieu + 1:]
        if not essai or essai in servables:
            continue
        return candidat in refus_nom(essai)
    return False


def autotest():

    """Le piege du module (L-032) : 4 epreuves sur un arbre jetable, et il nettoie.

    Un extracteur jamais vu crier ne prouve rien : on exige (1) une brique AVEC
    usage servie ; (2) une brique SANS usage ACCUSEE ; (3) un .bak et un __pycache__
    JAMAIS des briques ; (4) un nom inconnu : aucun chemin rendu.
    """
    import shutil
    import tempfile
    racine = Path(tempfile.mkdtemp(prefix="modes-emploi-"))
    try:
        (racine / "avec-usage.py").write_text(
            "\"\"\"avec-usage -- but lisible." + chr(10) + chr(10)
            + "Usage: python avec-usage.py --x" + chr(10) + "\"\"\"" + chr(10),
            encoding="utf-8")
        (racine / "sans-usage.py").write_text("", encoding="utf-8")
        (racine / "vieux.py.bak.20260101_000000").write_text("x", encoding="utf-8")
        (racine / "__pycache__").mkdir()
        # COBAYE DU PLAFOND (MO-314) : au-dela du plafond declare, la carte doit etre
        # COUPEE ET LE DIRE ; en deca, elle ne coupe RIEN. Deux arbres, deux verdicts.
        grande = racine / "grande"
        grande.mkdir()
        for numero in range(PLAFOND_BRIQUES_CARTE + 2):
            (grande / ("brique-" + str(numero).zfill(2) + ".py")).write_text(
                "\"\"\"" + "brique numero " + str(numero) + " -- but de cobaye." + chr(10)
                + "Usage: python brique.py --x" + chr(10) + "\"\"\"" + chr(10), encoding="utf-8")
        servables = noms_servables()
        # LE PLANCHER (2026-09-25) : une carte ne cache JAMAIS ses essentielles, meme
        # quand le plafond coupe. Le cobaye lit la VRAIE carte des portes : si le
        # plancher casse, suivi-optimus (la brique la plus appelee de la Matrice)
        # disparait du texte servi, et cette epreuve le crie.
        racine_portes = (PILOTE / RACINES["outils-matrice"]).resolve()
        briques_portes = lister_briques(racine_portes)
        plancher_portes = plancher_de(racine_portes)
        ordonnees_portes = [brique.name for brique in ordonner(briques_portes, racine_portes)]
        texte_portes, _absentes_portes = carte(racine_portes)
        texte_portes_complet, _ = carte(racine_portes, 0)
        texte_grand, _absentes = carte(grande)
        texte_petit, _absentes_petit = carte(racine)
        briques = [b.name for b in lister_briques(racine)]
        texte, manquantes = carte(racine)
        # La CARTE dit UNE ligne par brique ; le mode d emploi COMPLET (but + usage)
        # se demande pour la brique -- deux lectures, et l epreuve exige LES DEUX.
        complet, origine = mode_emploi(racine / "avec-usage.py")
        return [
            ("brique AVEC usage SERVIE (but + usage)",
             "avec-usage.py : avec-usage -- but lisible." in texte
             and "avec-usage -- but lisible." in complet
             and "python avec-usage.py --x" in complet),
            ("brique SANS usage ACCUSEE (jamais tue)",
             "sans-usage.py" in manquantes),
            ("point de restauration et __pycache__ JAMAIS des briques",
             "vieux.py.bak.20260101_000000" not in briques and "__pycache__" not in briques),
            ("nom inconnu : aucun chemin rendu (l appelant refuse)",
             chemin_brique(racine, "inexistant.py") is None),
            ("carte AU-DELA du plafond : coupee ET la coupe DITE",
             "2 brique(s) NON AFFICHEE(S) sur " + str(PLAFOND_BRIQUES_CARTE + 2) in texte_grand
             and "brique-" + str(PLAFOND_BRIQUES_CARTE).zfill(2) + ".py" not in texte_grand),
            ("CONTRE-TEMOIN : carte SOUS le plafond, RIEN de coupe",
             "NON AFFICHEE" not in texte_petit),
            # LE PLANCHER (2026-09-25) : le plafond coupe par la FIN, donc l ORDRE est ce
            # qui protege une essentielle. Cobaye lu sur la VRAIE carte des portes :
            # l ordre les met DEVANT, la carte SERVIE les porte TOUTES malgre la coupe,
            # et elle DIT son plancher (un lecteur doit savoir ce qui est garanti).
            ("plancher : l ordre met les essentielles DEVANT (le plafond coupe la fin)",
             bool(plancher_portes)
             and tuple(ordonnees_portes[:len(plancher_portes)]) == tuple(plancher_portes)
             and len(briques_portes) > PLAFOND_BRIQUES_CARTE),
            ("plancher : la carte SERVIE porte ses essentielles MALGRE la coupe",
             all(nom in texte_portes for nom in plancher_portes)),
            ("plancher : la carte DIT son plancher",
             "plancher declare : " + str(len(plancher_portes)) in texte_portes),
            ("CONTRE-TEMOIN : carte complete (plafond 0) rend TOUTES les briques",
             all(brique.name in texte_portes_complet for brique in briques_portes)),
            # LA RESOLUTION (EO-313) : elle est consommee par une PORTE, donc elle
            # se prouve comme une porte -- un nom servable RESOUT, un nom inconnu
            # est REFUSE en le nommant (avec ses proches), jamais rendu None en
            # silence. L epreuve lit le VRAI parc (lecture seule) : c est la seule
            # facon de prouver que la porte et l injection regardent les memes noms.
            ("un nom servable RESOUT, un nom inconnu est REFUSE en le nommant",
             bool(servables) and trouver_brique(servables[0]) is not None
             and trouver_brique("zzz-inexistant.py") is None
             and "nom non servable" in refus_nom("zzz-inexistant.py")),
            # LA PROXIMITE ELLE-MEME (MO-468) : une LETTRE OUBLIEE est PROPOSEE -- la
            # copie du pilote ne cherchait que la SOUS-CHAINE et se taisait. Le cobaye
            # (_epreuve_proximite) est joue sur le parc REEL, en lecture seule.
            ("une LETTRE OUBLIEE est PROPOSEE (la regle n est plus la sous-chaine seule)",
             _epreuve_proximite(servables)),

            # EXTRAIT (EO-314) : les trois morceaux SEPARES -- le registre les range
            # separement, le pilote les recolle. Les DEUX lectures doivent dire la
            # MEME chose (sinon le registre decrirait une autre brique que celle qui
            # est servie) : c est ce que cette epreuve tient.
            ("extrait separe (but, usage) et mode_emploi les recolle a l identique",
             extrait(racine / "avec-usage.py")[0] == "avec-usage -- but lisible."
             and "python avec-usage.py --x" in extrait(racine / "avec-usage.py")[1]
             and mode_emploi(racine / "avec-usage.py")[0]
             == ("avec-usage -- but lisible." + chr(10)
                 + extrait(racine / "avec-usage.py")[1])),
            # LA GARANTIE ELLE-MEME (MO-454) : un plancher plus long que le
            # plafond serait coupe par sa propre carte -- la promesse deviendrait
            # un mensonge. Toute carte declaree doit tenir : plancher <= plafond.
            ("plancher : aucun plancher ne depasse le plafond de sa carte",
             all(len(plancher_de((PILOTE / RACINES[cle]).resolve()))
                 <= PLAFOND_BRIQUES_CARTE for cle in sorted(RACINES))),
        ]
    finally:
        shutil.rmtree(str(racine), ignore_errors=True)


def _racine_option(arguments, defaut):
    if "--racine" in arguments:
        position = arguments.index("--racine")
        if position + 1 < len(arguments):
            return Path(arguments[position + 1])
    return Path(defaut)


def main():
    arguments = sys.argv[1:]
    if "--auto-test" in arguments:
        epreuves = autotest()
        for nom, tenu in epreuves:
            print(("  [OK] " if tenu else "  [KO] ") + nom)
        ratees = [nom for nom, tenu in epreuves if not tenu]
        print("  AUTOTEST : " + str(len(epreuves) - len(ratees)) + "/" + str(len(epreuves))
              + " epreuve(s) tenue(s)")
        return 1 if ratees else 0
    if not arguments:
        print(__doc__)
        return 2
    base = PILOTE
    nom_racine = arguments[0]
    if nom_racine in RACINES:
        racine = (base / RACINES[nom_racine]).resolve()
        # --complet : la carte ENTIERE (voie de secours, jamais un blocage).
        print(servir(racine, 0 if "--complet" in arguments else PLAFOND_BRIQUES_CARTE))
        return 0
    if nom_racine == "mode-emploi" and len(arguments) > 1:
        cible = arguments[1]
        for racine_nommee in sorted(RACINES):
            racine = (base / RACINES[racine_nommee]).resolve()
            brique = chemin_brique(racine, cible)
            if brique is not None:
                texte, origine = mode_emploi(brique)
                print("=== " + cible + " (" + (origine or "aucune source") + ") ===")
                print(texte if texte else "AUCUN MODE D EMPLOI : a poser dans la brique elle-meme.")
                return 0
        print("REFUS : brique inconnue : " + cible + " (racines : " + ", ".join(sorted(RACINES)) + ")")
        return 2
    print(__doc__)
    print("Racines connues : " + ", ".join(sorted(RACINES)))
    return 2


if __name__ == "__main__":
    sys.exit(main())
