"""Parseur d options PARTAGE de la Matrice -- DOMICILE (EO-158, MO-171).

Le motif est PARTAGE, jamais recopie (M-076 ; meme famille que data/commun/
cible.py de MO-166). Mesure MO-169 : 40 copies VIVANTES du meme parseur, en 22
textes differents -- et la variante majoritaire AVALAIT l option suivante comme
valeur (un --fichier sans valeur posait fichier = "--mode" et sautait --mode :
une option disparaissait en silence, jamais dite). Les copies s alignent en
CONSOMMANT ce domicile.

CONTRAT (identiquement celui de la porte ecrire, EO-156) :
  1. une VALEUR peut commencer par des tirets : un document a carte d identite
     COMMENCE par ---, et un texte peut citer une option ;
  2. seul un NOM D OPTION CONNU arrete la valeur : le morceau suivant n est pris
     pour une option que s il en est une ;
  3. une option PRIVEE de valeur n est jamais avalee en silence : elle est
     INSCRITE sous CLE_SANS_VALEUR, a charge pour l appelant de la DIRE ;
  4. les DRAPEAUX (options sans valeur par nature : json, recursif, prive,
     verbose, integration, etat...) sont DECLARES par l appelant, valent "1" et
     restent PRESENTS -- un drapeau reste une option presente, c est la valeur
     qui manque ;
  5. un morceau qui a la FORME d une option (--xxx) SANS en etre une n est
     JAMAIS avale en silence : il est INSCRIT sous CLE_INCONNUES, a charge pour
     l appelant de le DIRE (EO-179). Avant, il etait simplement SAUTE : l appel
     obtenait le resultat du DEFAUT, indiscernable d un resultat correct -- et
     une limite muette se lit comme un FAIT (L-055, friction 77).
     LIMITE DITE : seuls les morceaux qui COMMENCENT par -- sont retenus -- un
     argument nu peut etre du texte libre legitime, et le declarer inconnu
     fabriquerait des faux positifs. Le parseur ne devine pas, il SIGNALE.

MODE sans_tirets (mesure MO-171 : deux outils nomment leurs options sans tirets
de tete, un autre les prefixe) : le nom est reconnu par lstrip("-"), et c est la
MEME normalisation qui decide si le morceau suivant est une option. Limite DITE :
dans ce mode, une valeur qui serait exactement un nom d option connu reste
ambigue -- hors mode, une valeur a tirets inconnue reste une valeur, toujours.

6. LE REFUS EST LE DEFAUT (T1 de la chaine PB-002, 2026-09-20). Mesure de la
   sonde sc-004 : 32 des 35 outils rendaient un refus MUET -- l option fautive
   n etait jamais NOMMEE. La cause : le parseur RETENAIT l inconnue depuis EO-179
   (CLE_INCONNUES), mais c est l APPELANT qui devait la DIRE, et 107 appelants
   sur 110 ne le faisaient pas. Le domicile refuse donc LUI-MEME : l inconnue est
   NOMMEE, les options reconnues et le remede sont dits, et l appel s ARRETE en
   code 2 (`raise SystemExit`). Un appel qui accepte des arguments LIBRES le
   DECLARE (`refuser=False`) : l inconnue est alors DITE sans arreter l appel --
   jamais taire. Le texte du refus vit ICI, en UN seul exemplaire (M-076), et
   sert les DEUX chemins : une option inconnue dans les arguments
   (`extraire_options`) et une option EN TETE, la ou un VERBE est attendu
   (`refuser_option_en_tete`, appele par le point commun des outils).
"""

import sys
from pathlib import Path

# Sentinelle des options privees de valeur : le parseur ne pose JAMAIS "" a la
# place de l appelant -- une option videe en silence se lit "pas de contenu".
CLE_SANS_VALEUR = "__sans_valeur__"
# LE MARQUEUR du refus directionnel : c est lui que cherchent les lecteurs (la
# sonde sc-004, les cobayes) pour savoir que le refus NOMME l option fautive.
# Un seul exemplaire du texte (M-076) : le message vit dans dire_option_inconnue.
MARQUEUR_OPTION_INCONNUE = "OPTION INCONNUE"
# Sentinelle des morceaux qui ONT LA FORME d une option SANS en etre une
# (EO-179, 2026-09-19) : le parseur ne les avale plus en silence -- c est
# l APPELANT qui decide de les DIRE (les ignorer en le disant, ou REFUSER).
CLE_INCONNUES = "__inconnues__"
VALEUR_DRAPEAU = "1"
# Encodage des textes lus par ce module -- LOCAL, comme chez ses voisins
# (fragment.py, lancement.py, rotation_journal.py) : chaque module de
# data/commun le declare, aucun ne l importe d un autre.
ENCODAGE = "utf-8"


def _nom_option(morceau, noms_connus, sans_tirets):
    """Nom d option reconnu, ou None si le morceau n en est pas un."""
    if sans_tirets:
        nom = morceau.lstrip("-")
        return nom if nom in noms_connus else None
    if morceau.startswith("--") and morceau[2:] in noms_connus:
        return morceau[2:]
    return None


def extraire_options(arguments, noms_connus, drapeaux=(), sans_tirets=False,
                     outil="", usage="", refuser=True):
    """Extrait les options d une liste d arguments (contrat ci-dessus).

    Ne valide pas le CONTENU des valeurs, seulement leur FORME : ce que
    l appelant fait d une valeur absente lui appartient, mais il l APPREND
    (CLE_SANS_VALEUR) au lieu de la lire "pas de contenu".

    REFUS PAR DEFAUT (point 6 du contrat) : une option qui a la FORME d une
    option sans en etre une est NOMMEE et l appel s ARRETE en code 2. Un appel
    qui accepte des arguments libres passe `refuser=False`.
    """
    options = {}
    sans_valeur = []
    inconnues = []
    index = 0
    while index < len(arguments):
        nom = _nom_option(arguments[index], noms_connus, sans_tirets)
        if nom is None:
            # EO-179 : un morceau qui a la FORME d une option sans en etre une
            # est RETENU, jamais avale en silence. Un argument NU ne l est pas :
            # il peut etre du texte libre legitime -- le parseur ne devine pas,
            # il signale, et l appelant decide (signaler_inconnues).
            if arguments[index].startswith("--"):
                inconnues.append(arguments[index])
            index += 1
            continue
        if nom in drapeaux:
            options[nom] = VALEUR_DRAPEAU
            index += 1
            continue
        suivant = arguments[index + 1] if index + 1 < len(arguments) else None
        suit_une_option = suivant is not None and _nom_option(suivant, noms_connus, sans_tirets) is not None
        if suivant is not None and not suit_une_option:
            options[nom] = suivant
            index += 2
        else:
            sans_valeur.append(nom)
            index += 1
    if sans_valeur:
        options[CLE_SANS_VALEUR] = sans_valeur
    if inconnues:
        options[CLE_INCONNUES] = inconnues
        code = dire_option_inconnue(inconnues, outil or nom_de_l_outil(),
                                    noms_connus, usage, refus=refuser)
        if code:
            # ARRET FORCE : le refus doit rester VISIBLE meme chez un appelant qui
            # capture la sortie -- sac_a_dos.envelopper la re-emet (T1).
            raise SystemExit(code)
    return options


def dire_option_inconnue(inconnues, outil, noms_connus=(), usage="", refus=True):
    """LE message du domicile : il NOMME l option, dit ce qui est connu, et le remede.

    Un seul exemplaire de ce texte (M-076) : les DEUX chemins du refus passent
    par ici -- une option inconnue DANS les arguments (`extraire_options`) et une
    option EN TETE, la ou un verbe est attendu (`refuser_option_en_tete`).
    Rend 2 quand il refuse, 0 quand l appel DECLARE accepter des arguments libres.
    """
    print(MARQUEUR_OPTION_INCONNUE + " : " + ", ".join(inconnues)
          + "  (outil : " + (outil or "?") + ")")
    if noms_connus:
        print("  options reconnues : " + ", ".join(sorted(noms_connus)))
    else:
        print("  cet outil ne declare AUCUNE option a cette place"
              " (le VERBE vient en tete).")
    if usage:
        print("  " + usage)
    if refus:
        print("  REFUS : une option inconnue n est jamais ignoree en silence --"
              " sans ce refus, l appel obtenait le resultat du DEFAUT,"
              " indiscernable d un resultat correct (EO-179, friction 77).")
        return 2
    print("  (l option est IGNOREE, et c est DIT : cet appel accepte des"
          " arguments libres)")
    return 0


def signaler_inconnues(options, outil, noms_connus, usage="", refuser=True):
    """DIT les morceaux qui ont la FORME d une option sans en etre une (EO-179).

    Conserve pour les appelants qui nommaient deja l inconnue AVANT le refus par
    defaut (rechercher, benchmark, maintenir) : c est le MEME message, jamais un
    second (M-076). Rend 2 quand il y a des inconnues et que le refus est
    demande, 0 sinon : l appelant retourne ce code tel quel.
    """
    inconnues = list(options.get(CLE_INCONNUES) or [])
    if not inconnues:
        return 0
    return dire_option_inconnue(inconnues, outil, noms_connus, usage, refus=refuser)


# Options de SERVICE : demander l aide n est pas une faute (le doc s affiche).
OPTIONS_DE_SERVICE = ("--help", "--aide")


def refuser_option_en_tete(arguments, outil="", usage="", commandes=None):
    """Un premier morceau qui a la FORME d une option, la ou un VERBE est attendu.

    Mesure T1 (2026-09-20) : la sonde pose l option inconnue EN PREMIER ; 28
    outils imprimaient alors leur doc et rendaient code 2 SANS la NOMMER -- le
    domicile n etait meme pas atteint (le routeur de verbe s arretait avant).

    GARDE-FOU DE PORTEE (faux positif MESURE, 2026-09-20) : 6 outils
    (benchmark, rechercher, dialoguer, signaler, executer, maintenir) acceptent
    une option EN TETE, sans verbe -- un refus aveugle les CASSERAIT. Le refus ne
    frappe donc QUE les outils qui DECLARENT leurs verbes (`commandes`) et dont
    le premier morceau n en est pas un : la declaration de l outil decide, jamais
    une liste tenue ici (et un outil qui ne declare rien n est jamais accuse a
    tort). Rend 0 ou 2 apres avoir NOMME l option, par le MEME message.
    """
    if not arguments or not str(arguments[0]).startswith("--"):
        return 0
    if commandes is None:
        return 0
    if str(arguments[0]) in OPTIONS_DE_SERVICE or str(arguments[0]) in commandes:
        return 0
    return dire_option_inconnue([str(arguments[0])], outil or nom_de_l_outil(),
                                commandes, usage)


def nom_de_l_outil():
    """Le nom de l outil qui parle : deduit de sys.argv, jamais une constante."""
    try:
        return Path(sys.argv[0]).resolve().parent.name or "?"
    except (IndexError, OSError):
        return "?"


# --- LE TRANSPORT @fichier (corvees C-004 / C-013, MO-469) --------------------
# LE PROBLEME RESOLU : un TEXTE passe en argument traverse le SHELL -- ses
# backticks sont EXECUTES et DISPARAISSENT. Mesure du 2026-09-25 : l objectif
# d un item est ne TROUE, DEUX fois le meme jour (corvees C-004 puis C-013). La
# porte ecrire repond depuis longtemps par `--contenu @fichier` : ce resolveur
# lui donne UN SEUL DOMICILE, car mesure du meme jour TROIS copies vivaient deja
# (ecrire/commun.py, executer/commun.py, fragment.py) -- une M-076 de plus.
#
# SEMANTIQUE, celle de la porte ecrire, choisie pour ne RIEN CASSER : un `@`
# n est regarde que s il est suivi d une reference qui RESSEMBLE a un chemin
# (elle porte un separateur ou un point) ; un chemin INTROUVABLE est REFUSE en
# le NOMMANT ; tout autre `@...` reste du TEXTE LITTERAL, exactement comme avant
# (la compatibilite arriere passe avant l elegance).


def valeur_ou_fichier(valeur, etiquette, depart):
    """(texte, refus) : la valeur, ou le CONTENU du fichier qu elle designe en @.

    `depart` est la base des references RELATIVES : elle est EXIGEE, jamais le
    cwd (CV-007 : un chemin ne se resout pas contre le dossier courant), et une
    reference absolue l ignore. Le refus NOMME le chemin REELLEMENT cherche --
    un refus qui ne dit pas OU il a cherche coute trois essais (fragment.py).
    """
    texte = "" if valeur is None else str(valeur)
    if not texte.startswith("@"):
        return texte, ""
    reference = texte[1:].strip()
    if not reference:
        return None, ("REFUS : " + etiquette + " ne porte RIEN apres @ -- pour un"
                      " texte qui commence par @, donnez-le autrement.")
    if "/" not in reference and "\\" not in reference and "." not in reference:
        return texte, ""
    chemin = Path(reference)
    if not chemin.is_absolute():
        chemin = Path(depart) / chemin
    if not chemin.is_file():
        return None, ("REFUS : " + etiquette + " @fichier INTROUVABLE : " + reference
                      + " (cherche en " + str(chemin) + ")")
    try:
        return chemin.read_text(encoding=ENCODAGE), ""
    except OSError as erreur:
        return None, ("REFUS : " + etiquette + " @fichier ILLISIBLE : " + str(chemin)
                      + " (" + str(erreur) + ")")


# --- LE RECIT : INLINE ou PAR FICHIER, EXCLUSIFS (MO-425) --------------------
# MEME FAMILLE que `valeur_ou_fichier` ci-dessus : un RECIT passe en ARGUMENT
# traverse le SHELL avant d atteindre la porte -- ses ACCENTS GRAVES sont
# EXECUTES et le texte arrive TROUE (mesure MO-363 ; lecon L-166, payee en MO-387
# puis MO-388). La porte ne peut PAS voir ce que le shell a deja avale : le
# remede est un TRANSPORT par FICHIER, jamais un controle. Le contrat est celui de
# `lire_bilan` du pilote (EO-132), tenu ici en UN SEUL exemplaire (M-076).


def lire_texte_ou_fichier(options, cle, cle_fichier, bases):
    """(code, texte, message) : la valeur INLINE ou le CONTENU DU FICHIER, exclusifs.

    - les DEUX formes donnees ENSEMBLE sont REFUSEES (un melange silencieux ferait
      gagner l une des deux sans le dire) ;
    - le fichier est cherche sous `bases` DANS L ORDRE ; un chemin ABSOLU ignore
      ces bases ;
    - un chemin INTROUVABLE est REFUSE en nommant TOUS les chemins essayes -- un
      chemin ne se devine jamais (meme discipline que `resoudre_chemin_bilan`).

    BIT-EXACT : le contenu du fichier est rendu TEL QUEL (aucun `strip`, sauts de
    ligne PRESERVES) -- c est ce qui rend la preuve mesurable : l empreinte SHA-256
    du FICHIER egale celle du TEXTE LU (MO-425). Toute normalisation ici rouvrirait
    le trou (un strip changerait l empreinte et ferait mentir le controle).
    """
    texte_direct = options.get(cle) or ""
    reference = (options.get(cle_fichier) or "").strip()
    if texte_direct and reference:
        return 2, "", ("REFUS : --" + cle + " et --" + cle_fichier
                       + " sont EXCLUSIFS : donne l un OU l autre, jamais les deux.")
    if not reference:
        return 0, texte_direct, ""
    chemin = Path(reference)
    if chemin.is_absolute():
        candidats = [chemin]
    else:
        candidats = [Path(base) / chemin for base in bases]
    for candidat in candidats:
        try:
            with open(candidat, "r", encoding=ENCODAGE, newline="") as flux:
                return 0, flux.read(), ""
        except OSError:
            continue
    return 2, "", ("REFUS : --" + cle_fichier + " INTROUVABLE : " + reference
                   + " (cherche en : " + " ; ".join(str(c) for c in candidats) + ")")
