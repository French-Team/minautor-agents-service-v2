"""Categorie vrac : l'echelon 0 -- deposer une mission brute, proposer son type.

Interface entre main.py et les fonctions simples (vrac/fonctions.py).
"""
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

from classer.fonctions import classer_mission
from listes import (CHAMP_TYPE_SOURCE, MOT_CLE_DECLARE, NOM_EVALUATEUR, SOURCES,
                    SOURCE_TYPE_DECLARATION, SOURCE_TYPE_DEFAUT, SOURCE_TYPE_MOT_CLE,
                    TYPES, URGENCES, VERDICT_NON)
# L IMPORTANCE (EO-457) : le DOMICILE de la carte d identite est CONSOMME ici
# (M-076). Le bloc _REPERTOIRE_COMMUN_LANCEMENT ci-dessus a deja pose son dossier
# sur le chemin -- c est LUI qui fait foi, jamais une seconde copie du vocabulaire.
from carte_identite import (CLE_GRAVITE, CLE_NIVEAU, GRAVITES, GRAVITE_DEFAUT,
                            NIVEAU_DEFAUT, NIVEAU_MAX, NIVEAU_MIN,
                            gravite_canonique, lire_carte, niveau_valide)
from roles import CHAMP_ROLE, est_theme_du_vivier, valider_role
from stockage import charger_entonnoir, enregistrer_entonnoir
from vrac.fonctions import deposer_vrac, proposer_type, proposer_urgence


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus)


def texte_ou_fichier(valeur, etiquette):
    """Un texte libre, ou le CONTENU du fichier qu il designe en @ (C-004/C-013).

    POURQUOI (mesure du 2026-09-25, MO-469) : un texte passe en ARGUMENT traverse
    le SHELL -- ses backticks sont EXECUTES et le texte arrive TROUE (l objectif
    de EO-437 est ne troue, deux fois le meme jour). `--objectif @fichier` lit le
    texte DANS le fichier. Le resolveur vit au domicile PARTAGE des options
    (M-076) : il n est pas recopie ici, et il est appele avec la racine de la
    Matrice comme base (jamais le cwd).
    """
    from options import valeur_ou_fichier as resoudre  # domicile partage (M-076)
    return resoudre(valeur, etiquette, _RACINE_LANCEMENT)


NOMS_OPTIONS = ("theme", "objectif", "urgence", "source", "trace", "role", "type",
                "gravite", "niveau")

# L avis multi-axes est un SUPER-COMBO de l operateur (hors pilote). Le chemin se
# resout par le MARQUEUR PARTAGE (L-013 / MO-088) : AUCUN parents[N] compte a la
# main, et un marqueur introuvable le DIT (jamais un chemin faux et silencieux).
BORNES_REMONTEE = 30
MARQUEUR_MATRICE = Path("matrice") / "data" / "commun" / "racine.py"
# ATTENTION (EO-168 / MO-175 jambe 3) : le marqueur PARTAGE designe le dossier
# QUI PORTE `matrice/` (soit .../cerveau-projet/matrix) -- le chemin relatif
# part DONC de `_operateur/...`. L ancienne valeur commencait par `matrix/`, ce
# qui DOUBLAIT le segment (`.../matrix/matrix/_operateur/...`) : l evaluateur
# etait INTROUVABLE, et l avis tombait a NON avec un motif qui parlait de JSON.
CHEMIN_EVALUATEUR_REL = (Path("_operateur") / "optimus-prime" / "super-combos"
                         / "combos" / "outils" / NOM_EVALUATEUR)


def trouver_racine_matrice(depart):
    """Remonte jusqu au dossier qui PORTE le marqueur partage ; l echec se DIT."""
    courant = Path(depart).resolve()
    for _ in range(BORNES_REMONTEE):
        if (courant / MARQUEUR_MATRICE).is_file():
            return courant
        if courant.parent == courant:
            break
        courant = courant.parent
    raise RuntimeError("Racine matrix introuvable (marqueur " + str(MARQUEUR_MATRICE)
                       + " absent en remontant).")


CHEMIN_EVALUATEUR = trouver_racine_matrice(Path(__file__).resolve().parent) / CHEMIN_EVALUATEUR_REL


def avis_auto_validation(theme, objectif, type_propose, source):
    """Rend (verdict, axes) par l AVIS MULTI-AXES sur l auto-validation.

    Un moteur INJOIGNABLE se DIT : il rend NON (l item rend la main) et l axe
    `moteur` porte la raison -- jamais un repli muet (l absence d un champ doit
    se dire, lecon MO-167).
    """
    if not CHEMIN_EVALUATEUR.is_file():
        return VERDICT_NON, [{"axe": "moteur", "vote": "contre",
                              "motif": "evaluateur INTROUVABLE : " + str(CHEMIN_EVALUATEUR)}]
    sortie = lancer_enfant(
        [sys.executable, str(CHEMIN_EVALUATEUR), "--theme", theme,
         "--objectif", objectif, "--type", type_propose, "--source", source,
         "--json"], capture_output=True, text=True)
    try:
        avis = json.loads(sortie.stdout)
    except Exception as erreur:
        # Le motif NOMME la cause reelle : code de sortie + ce que le moteur a DIT
        # (l ancien motif parlait de JSON et cachait un chemin introuvable).
        motif = ("evaluateur injoignable (code " + str(sortie.returncode) + ") : "
                 + str(erreur)[:60] + " -- " + (sortie.stderr or "").strip()[:140])
        return VERDICT_NON, [{"axe": "moteur", "vote": "contre", "motif": motif}]
    return avis.get("verdict", VERDICT_NON), avis.get("axes", [])


def carte_du_document(valeur):
    """La carte d identite du document designe par `@fichier`, ou None.

    Le createur a tranche (EO-457) : la CARTE D IDENTITE est la source PREMIERE de
    l importance, l item la RECOPIE. Ne s applique qu a un `@fichier` REEL (un `@`
    nu reste du TEXTE LITTERAL, comme partout dans la Matrice) ; un document SANS
    carte ne fait pas echouer le depot -- il n apporte simplement rien.
    """
    if not str(valeur or "").startswith("@"):
        return None
    reference = str(valeur)[1:].strip()
    if not reference or not ("/" in reference or "\\" in reference or "." in reference):
        return None
    chemin = Path(reference)
    if not chemin.is_absolute():
        chemin = _RACINE_LANCEMENT / chemin
    if not chemin.is_file():
        return None
    try:
        return lire_carte(chemin.read_text(encoding="utf-8", errors="replace"))
    except OSError:
        return None


def executer(arguments):
    options = extraire_options(arguments, NOMS_OPTIONS)
    # LES TEXTES LIBRES ACCEPTENT @fichier (corvees C-004 / C-013) : un chemin
    # INTROUVABLE est REFUSE en le nommant, et RIEN n est depose.
    theme, refus_theme = texte_ou_fichier(options.get("theme", ""), "--theme")
    if refus_theme:
        print(refus_theme)
        return 2
    objectif, refus_objectif = texte_ou_fichier(options.get("objectif", ""), "--objectif")
    if refus_objectif:
        print(refus_objectif)
        return 2
    urgence = proposer_urgence(options.get("urgence", ""))
    # L IMPORTANCE (EO-457) : DEUX champs FERMES, portes par l item des sa
    # naissance. Ils se DECLARENT (--gravite / --niveau), sinon ils se RECOPIENT
    # depuis la CARTE DU DOCUMENT SOURCE (@fichier), sinon les DEFAUTS du domicile.
    # Une valeur hors liste est REFUSEE en la nommant -- jamais repliee en silence.
    gravite_declaree = options.get("gravite", "")
    niveau_declare = options.get("niveau", "")
    if gravite_declaree and not gravite_canonique(gravite_declaree):
        print("Gravite inconnue : " + repr(gravite_declaree)
              + " (gravites fermees : " + ", ".join(GRAVITES) + ")")
        return 2
    if niveau_declare and not niveau_valide(niveau_declare):
        print("Niveau inconnu : " + repr(niveau_declare)
              + " (entier de " + str(NIVEAU_MIN) + " a " + str(NIVEAU_MAX) + ")")
        return 2
    carte_source = (carte_du_document(options.get("objectif", ""))
                    or carte_du_document(options.get("theme", "")) or {})
    gravite = (gravite_canonique(gravite_declaree)
               or gravite_canonique(carte_source.get(CLE_GRAVITE, ""))
               or GRAVITE_DEFAUT)
    niveau = (niveau_valide(niveau_declare)
              or niveau_valide(carte_source.get(CLE_NIVEAU, ""))
              or NIVEAU_DEFAUT)
    # PROVENANCE FERMEE (F1, 2026-09-19) : `source` n est plus un texte libre.
    # La trace (date, motif) va dans --trace, JAMAIS ici -- un champ, un sens.
    # Un refus DIRECTIONNEL : il nomme la liste fermee ET le bon geste.
    source = (options.get("source") or SOURCES[0]).strip()
    trace, refus_trace = texte_ou_fichier(options.get("trace") or "", "--trace")
    if refus_trace:
        print(refus_trace)
        return 2
    trace = trace.strip()
    if source not in SOURCES:
        print("Source inconnue : " + repr(source) + " -- sources fermees : "
              + ", ".join(SOURCES) + ".")
        print("  La trace libre (date, motif) se met dans --trace :  --source "
              + SOURCES[0] + ' --trace "2026-09-19 (audit par la suite)"')
        return 2

    if not theme or not objectif:
        print('Usage : python main.py deposer --theme "..." --objectif "..."'
              ' [--urgence bloquante|haute|normale|basse] [--source '
              + "|".join(SOURCES) + '] [--trace "..."] [--role THEME]'
              ' [--type dev|reparation|doc|audit|revision]')
        return 2
    if urgence not in URGENCES:
        print("Urgence inconnue : " + urgence + " (urgences fermees : " + ", ".join(URGENCES) + ")")
        return 2

    # LE TITRE N'EST PAS UNE ETIQUETTE (mesure 2026-09-23, deux items reels) : un
    # `--theme` qui EST un nom du vivier est une CONFUSION DE CHAMPS -- le titre de
    # la demande etait perdu et la file affichait l etiquette a la place de la
    # phrase. Refus DIRECTIONNEL, AVANT toute ecriture, et le role a son champ.
    if est_theme_du_vivier(theme):
        print("REFUS : --theme est le TITRE de la demande (texte libre), pas une etiquette.")
        print("  " + repr(theme) + " est un THEME DU VIVIER : c'est le ROLE qui le porte.")
        print('  Titre attendu, par exemple : --theme "Reparer la file qui affiche une etiquette"')
        print("  Le role se pose AU DEPOT par --role " + theme
              + " (ou au classement, propose par la table type/categorie).")
        return 2

    # `theme` = TITRE (libre) ; `role` = ROLE de la mission, valide contre le
    # VIVIER. Facultatif au depot : le classement le pose (L-061/MO-076).
    role = ""
    role_brut = options.get("role", "")
    if role_brut:
        code, canonical, ecart = valider_role(role_brut)
        if code != 0:
            return code
        if ecart:
            print(ecart)
        role = canonical

    # Le TYPE declare (crochet `[outil]`, `[audit]`...) est valide contre la
    # liste FERMEE avant toute ecriture : un type inconnu se REFUSE, il ne
    # se replie pas en silence sur une proposition.
    type_declare = (options.get("type") or "").strip()
    if type_declare and type_declare not in TYPES:
        print("Type inconnu : " + type_declare + " (types fermes : "
              + ", ".join(TYPES) + ")")
        return 2
    etat = charger_entonnoir()
    type_propose, mot_cle = proposer_type(theme, objectif, type_declare)
    # L ORIGINE du type (EO-192) : c est elle qui arme -- ou non -- le declencheur.
    origine = (SOURCE_TYPE_DECLARATION if mot_cle == MOT_CLE_DECLARE
               else SOURCE_TYPE_DEFAUT if not mot_cle else SOURCE_TYPE_MOT_CLE)
    # L AVIS est rendu AVANT l ecriture : le verdict part avec l item (MO-175).
    verdict, axes = avis_auto_validation(theme, objectif, type_propose, source)
    identifiant = deposer_vrac(etat, theme, objectif, urgence, source, role,
                               verdict, axes, type_propose, trace, origine,
                               gravite, niveau)
    # DECLENCHEUR DE NAISSANCE (EO-192, decision createur 2026-09-19) : un item
    # dont le type est DECLARE (le crochet du createur -- SOUVERAIN) est CLASSE A
    # LA SECONDE : il entre dans SA file avec sa categorie et son role, poses par
    # les tables et IMPRIMES (donc corrigeables). Une PROPOSITION par mot-cle ne
    # classe PAS : une devinette n ouvre pas un domicile. Le vrac ne garde donc
    # que ce qu aucune souverainete n a nomme -- et le depot DIT alors le geste
    # exact qui le sort.
    classe, message_classement = False, ""
    if origine == SOURCE_TYPE_DECLARATION:
        code_classement, message_classement = classer_mission(
            etat, identifiant, type_propose, "", "")
        classe = code_classement == 0
    enregistrer_entonnoir(etat)
    if classe:
        print("Mission " + identifiant + " : type DECLARE (" + type_propose
              + ") -- CLASSEE A LA NAISSANCE.")
        print("  " + message_classement)
        print("  Corriger le ROLE si besoin : retiqueter --id " + identifiant
              + " --role <THEME du vivier>")
        return 0
    print(
        "Mission " + identifiant + " deposee au vrac (urgence " + urgence
        + ", source " + source
        + ("" if not trace else " -- trace : " + trace)
        + ") -- type propose : " + type_propose
        + ("" if not mot_cle else " (mot-cle : " + mot_cle + ")")
        + (" -- role : " + role if role else " -- role : (pose au classement)")
    )
    print("  ATTENTION : un item du vrac n est PAS executable -- aucun type ne le"
          " nomme. Sors-le :  python main.py classer --id " + identifiant
          + " [--type <" + "|".join(TYPES) + ">]")
    return 0
