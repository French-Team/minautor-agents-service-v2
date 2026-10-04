#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
injecter.py -- Moteur du CATALOGUE d'injections (porte `injection/`)

Rend le contenu des sources du catalogue `config.json` : injections de DEMARRAGE
et de PHASE. L'injection de MISSION (ordonnee, filtree L-016, pesee en tokens)
est faite par `injection/fonctions.py` -- les deux vivent dans la MEME porte.

Usage:
  python injecter.py <categorie> [--format texte|json|markdown]
  python injecter.py <categorie> --peser
  python injecter.py --categories
  python injecter.py fiche <categorie>    # la FICHE TECHNIQUE DE TRAVAIL (moule a jetons)

Les CATEGORIES viennent du CATALOGUE (aucune liste en dur ici) ; `mission` sert
les trois phases de mission d'un coup.

MESURE (MO-314, demande createur du 2026-09-20) : `--peser` rend le POIDS EN TOKENS
de chaque source servie, puis le TOTAL -- avec le peseur du DOMICILE PARTAGE
(matrice/data/commun/tokens.py), jamais une formule recopiee ici (M-076). C est la
mesure REJOUABLE qui a chiffre l injection avant-mission a 7435 tokens, dont 1792
pour les quatre cartes de modes d emploi (2373 si elles etaient completes : le
plafond de la carte en economise 581). Un peseur ABSENT = REFUS NOMME, jamais un 0
muet (une mesure qui se tait se lit comme une mesure a zero).

FICHE TECHNIQUE (MO-471, decisions D1 et D5) : le moule a jetons d'une CATEGORIE
vit a SON domicile (templates/<categorie>/fiche.moule) et le verbe `fiche` le REND
avec les metadonnees du catalogue. Un jeton que le moteur ne connait pas est un
REFUS nomme -- un moule a trou qui sortirait sans le dire se lirait comme une fiche
complete (L-055).

Doctrine "jamais de degradation silencieuse" (2026-09-13) :
  source absente + obligatoire: true   -> REFUS nomme   (code 2)
  source absente + obligatoire: false  -> ALERTE nommee (code 0, on continue)
  `obligatoire` non declare            -> traite comme OBLIGATOIRE (prudence) + alerte
  `type` inconnu du moteur             -> REFUS nomme   (code 2)
  `section` demandee et introuvable    -> REFUS nomme   (code 2)
Aucune cle du catalogue n'est ignoree : elle est SERVIE, ou SIGNALEE.
"""

import importlib.util
import sys
import json
import re
from pathlib import Path
from datetime import datetime

PILOTE = "optimus-prime"               # cachet de sortie (nomme l'agent servi)

BASE = Path(__file__).resolve().parent
RACINE = BASE.parent                    # le pilote : ancrage des sources du catalogue
CONFIG_PATH = BASE / "config.json"

TYPES_FICHIER = ("fichier",)
TYPES_JSON = ("json", "bdd")
TYPES_DOSSIER = ("dossier",)
TYPES_OUTIL = ("outil",)                # fichier -> lu, dossier -> liste
# MODES D EMPLOI (revision createur du 2026-09-20, MO-313) : le catalogue servait un
# `os.listdir` -- des NOMS, `__pycache__` et `.bak` compris, et AUCUN usage. Un outil
# se livre AVEC son mode d emploi. La source est un DOSSIER DE BRIQUES, servi par
# l extracteur de SON domicile (`injection/modes_emploi.py`), jamais une fiche
# recopiee ici : une fiche a cote deriverait en silence (M-076 / L-032).
TYPES_MODES_EMPLOI = ("modes-emploi",)
# LE PROFIL DE L UTILISATEUR (EO-480 / MO-507, decision createur 2026-09-30) : la fiche
# `matrix/USER-PROFIL.md` est remplie, et son bloc voyageait avec la mission -- mais
# comme AJUSTABLE, donc invisible par defaut : un agent qui ne demande pas `--complet`
# n a jamais le pseudo sous les yeux. Le createur tranche : le profil se sert EN FIN,
# juste avant que le pilote rende la main et que l agent fasse son compte-rendu -- c est
# le seul moment ou s adresser a l utilisateur avec SON pseudo et SON style a du sens.
#
# LA LECTURE N EST PAS REECRITE ICI : ce type appelle `charger_profil_utile`, qui
# consomme le MOTIF PARTAGE (matrice/data/commun/fiche_profil.py) -- la liste des
# champs attendus, le chemin de la fiche et la borne de poids y vivent, et le bloc
# dit deja ce qui manque, ce qui est coupe et ce qui n a pas pu etre lu. Relire la
# fiche a cote deriverait en silence : c est le defaut que le projet paie le plus
# cher (M-076 / L-032). Un profil ne se declare donc pas par un `source` de catalogue :
# son domicile EST le motif, et un second chemin serait deux verites.
TYPES_PROFIL = ("profil",)
CHEMIN_MODES_EMPLOI = BASE / "modes_emploi.py"
# Le PESEUR de tokens vit au DOMICILE partage (matrice/data/commun/tokens.py) : la
# mesure du catalogue le CONSOMME, elle ne recopie aucune formule (M-076). Forme du
# chemin : RELATIVE AU PILOTE, comme les `source` du catalogue.
CHEMIN_TOKENS = RACINE / "../../../matrice/data/commun/tokens.py"
FORMATS = ("texte", "json", "markdown")
CODE_OK = 0
CODE_REFUS = 2
CATEGORIE_MISSION = "mission"
PHASES_MISSION = ("avant-mission", "pendant-mission", "apres-mission")
# FICHE TECHNIQUE (MO-471) : les moules a jetons vivent par CATEGORIE, a leur
# domicile (templates/<categorie>/fiche.moule). Le moteur les REND avec les
# metadonnees du catalogue ; un jeton INCONNU du moteur est un REFUS nomme.
CHEMIN_TEMPLATES = BASE / "templates"
MOTIF_JETON = re.compile(r"__([A-Z_]+)__")
JETONS_FICHE = ("CATEGORIE", "DATE", "NB_SOURCES", "SOURCES")


def charger_catalogue():
    """Lit le catalogue. Absent ou mal forme = REFUS nomme, jamais un vide muet."""
    if not CONFIG_PATH.is_file():
        return None, "catalogue absent : " + str(CONFIG_PATH)
    try:
        donnees = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError) as erreur:
        return None, "catalogue illisible : " + str(CONFIG_PATH) + " (" + str(erreur) + ")"
    injections = donnees.get("injections")
    if not isinstance(injections, dict) or not injections:
        return None, "catalogue vide ou mal forme : " + str(CONFIG_PATH)
    return injections, None


def lire_fichier(chemin):
    return chemin.read_text(encoding="utf-8")


def lire_dossier(chemin):
    return sorted(p.name for p in chemin.iterdir())


def lire_json(chemin):
    return json.loads(chemin.read_text(encoding="utf-8"))


def charger_extracteur():
    """Charge l extracteur de modes d emploi depuis SON domicile. Rend (module, refus).

    Absent ou casse = REFUS NOMME (doctrine : aucune degradation silencieuse) : un
    catalogue qui ne sert plus les modes d emploi doit le CRIER, pas servir une
    carte vide que l agent lirait comme un parc sans outils.
    """
    if not CHEMIN_MODES_EMPLOI.is_file():
        return None, "extracteur de modes d emploi absent : " + str(CHEMIN_MODES_EMPLOI)
    try:
        specification = importlib.util.spec_from_file_location(
            "modes_emploi_catalogue", str(CHEMIN_MODES_EMPLOI))
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except (ImportError, OSError, SyntaxError, AttributeError) as erreur:
        return None, ("extracteur de modes d emploi ILLISIBLE : " + str(CHEMIN_MODES_EMPLOI)
                      + " (" + type(erreur).__name__ + " : " + str(erreur) + ")")
    return module, ""


def servir_modes_emploi(source):
    """Le texte d une source de type `modes-emploi` : la carte des briques du dossier."""
    module, refus = charger_extracteur()
    if module is None:
        raise ValueError(refus)
    return module.servir(source)


def servir_profil():
    """Le bloc PROFIL, rendu par SON motif (jamais la fiche relue ici).

    L import est PAResseux et a l EPROUVEMENT du motif : `fonctions.py` est le gros
    module de l injection, et ce catalogue doit rester lisible sans le charger. Il ne
    l importe pas lui-meme -- l aller-retour est sans cycle -- mais il a besoin que la
    racine du PILOTE soit dans le chemin, ce que le pilote fait deja et qu un appel
    isole (le catalogue rejoue a la main) ne fait pas. On le dit plutot que de le
    decouvrir dans un traceback.
    """
    try:
        from fonctions import charger_profil_utile
    except ImportError:
        for racine in (BASE, RACINE):
            if str(racine) not in sys.path:
                sys.path.insert(0, str(racine))
        try:
            from fonctions import charger_profil_utile
        except ImportError as erreur:
            return ("PROFIL NON SERVI (le module de l injection ne s importe pas : "
                    + str(erreur)[:70] + ") -- le pseudo n est pas lu, donc pas "
                    "employe. Le motif partage est "
                    "matrice/data/commun/fiche_profil.py : a reparer.")
    bloc = charger_profil_utile()
    if not isinstance(bloc, dict):
        return "PROFIL NON SERVI : le motif n a pas rendu un bloc ("
        + type(bloc).__name__ + ")"
    lignes = []
    champs = bloc.get("champs") or {}
    if champs:
        lignes.append("Les champs REMPLIS de la fiche utilisateur, a employer tels quels :")
        for nom in sorted(champs):
            lignes.append("- " + str(nom) + " : " + str(champs[nom]))
    else:
        lignes.append("Aucun champ rempli dans la fiche utilisateur.")
    a_remplir = bloc.get("a_remplir") or []
    if a_remplir:
        lignes.append("Champs VIDES (ils guiding : `profil --guider`) : "
                      + ", ".join(str(c) for c in a_remplir))
    ecartes = bloc.get("ecartes_par_plafond") or []
    if ecartes:
        lignes.append("Coupes par le plafond de poids : "
                      + ", ".join(str(c) for c in ecartes))
    avertissement = bloc.get("avertissement")
    if avertissement:
        lignes.append("AVERTISSEMENT : " + str(avertissement))
    if bloc.get("source"):
        lignes.append("Source : " + str(bloc["source"]))
    # LA CONSIGNE D EMPLOI, ici et pas ailleurs (decision createur, EO-480) : le bloc
    # QUIET ne demandait rien de lui-meme. Elle dit QUI, QUAND et POUR QUOI.
    lignes.append("")
    lignes.append("EMPLOI : au COMPTE-RENDU de fin de mission, adresse-toi a "
                  "l utilisateur avec le pseudo et le style ci-dessus -- c est le "
                  "seul moment ou cela a du sens. Ailleurs, ils sont ton contexte, "
                  "pas une consigne.")
    return "\n".join(lignes)


def filtrer_par_categorie(donnee, categorie):
    """Filtre un registre {"themes": [...]} sur le champ `categorie` des items."""
    if isinstance(donnee, dict) and "themes" in donnee:
        retenus = [t for t in donnee["themes"] if t.get("categorie") == categorie]
        return {"themes": retenus}
    return donnee


def extraire_section(texte, nom):
    """Extrait la section markdown `nom` : de son titre au titre de niveau <= au sien.

    Rend None si la section est introuvable (l'appelant en fait un REFUS).
    """
    lignes = texte.splitlines()
    cible = nom.strip().lower()
    debut = None
    niveau = 0
    for i, ligne in enumerate(lignes):
        if not ligne.startswith("#"):
            continue
        titre = ligne.lstrip("#").strip().lower()
        profondeur = len(ligne) - len(ligne.lstrip("#"))
        if debut is None:
            if cible in titre:
                debut = i
                niveau = profondeur
        elif profondeur <= niveau:
            return "\n".join(lignes[debut:i]).rstrip()
    if debut is None:
        return None
    return "\n".join(lignes[debut:]).rstrip()


def formater(entree, contenu, format_sortie):
    titre = entree["description"]
    if format_sortie == "markdown":
        if isinstance(contenu, (dict, list)):
            contenu = json.dumps(contenu, ensure_ascii=False, indent=2)
        return "## " + titre + "\n\n" + contenu + "\n"
    if format_sortie == "json":
        if isinstance(contenu, str):
            contenu = {"contenu": contenu}
        return json.dumps({
            "id": entree["id"],
            "description": titre,
            "donnees": contenu,
        }, ensure_ascii=False, indent=2)
    if isinstance(contenu, (dict, list)):
        contenu = json.dumps(contenu, ensure_ascii=False, indent=2)
    return "=== " + titre + " ===\n" + contenu + "\n"


def servir(entree, format_sortie):
    """Rend (texte, alertes, refus) pour UNE entree du catalogue."""
    alertes = []
    refus = []
    # `source` est exigee pour tout type QUI LIT UN CHEMIN. Le type `profil` n en a pas :
    # son domicile est le MOTIF partage, qui dit lui-meme si la fiche est la. Exiger une
    # source ici obligerait a declarer un second chemin vers la fiche -- deux verites
    # qui divergent en silence (M-076).
    type_declare = entree.get("type")
    cles = ("id", "description", "type")
    if type_declare not in TYPES_PROFIL:
        cles = cles + ("source",)
    for cle in cles:
        if not entree.get(cle):
            refus.append("entree mal formee : cle `" + cle + "` absente")
    if refus:
        return "", alertes, refus

    identifiant = entree["id"]
    if "obligatoire" not in entree:
        alertes.append(identifiant + " : `obligatoire` non declare -> traite comme OBLIGATOIRE")
        obligatoire = True
    else:
        obligatoire = bool(entree["obligatoire"])

    type_ = entree["type"]
    if type_ not in (TYPES_FICHIER + TYPES_JSON + TYPES_DOSSIER + TYPES_OUTIL
                     + TYPES_MODES_EMPLOI + TYPES_PROFIL):
        return "", alertes, [identifiant + " : type inconnu du moteur -> `" + str(type_) + "`"]

    # LE PROFIL N A PAS DE SOURCE DE CATALOGUE : son domicile est le MOTIF partage, qui
    # dit lui-meme si la fiche est la. Un `source` declare ici serait un second chemin
    # vers la fiche -- deux verites qui divergent en silence (M-076).
    if type_ in TYPES_PROFIL:
        try:
            contenu = servir_profil()
        except (OSError, ValueError) as erreur:
            return "", alertes, [identifiant + " : profil illisible ("
                                + type(erreur).__name__ + " : " + str(erreur)[:60] + ")"]
        return formater(entree, contenu, format_sortie), alertes, refus

    source = (RACINE / entree["source"]).resolve()
    if type_ in TYPES_DOSSIER:
        present = source.is_dir()
    elif type_ in TYPES_OUTIL or type_ in TYPES_MODES_EMPLOI:
        present = source.is_file() or source.is_dir()
    else:
        present = source.is_file()

    if not present:
        message = (identifiant + " : source " + ("OBLIGATOIRE" if obligatoire else "optionnelle")
                   + " absente -> " + str(source))
        if obligatoire:
            refus.append(message)
        else:
            alertes.append(message)
        return "", alertes, refus

    try:
        if type_ in TYPES_FICHIER:
            contenu = lire_fichier(source)
        elif type_ in TYPES_JSON:
            contenu = lire_json(source)
            if entree.get("categorie"):
                contenu = filtrer_par_categorie(contenu, entree["categorie"])
                items = contenu.get("themes") if isinstance(contenu, dict) else None
                if isinstance(items, list) and not items:
                    alertes.append(identifiant + " : filtre `" + str(entree["categorie"])
                                   + "` -> 0 item servi (contenu VIDE)")
        elif type_ in TYPES_DOSSIER:
            contenu = lire_dossier(source)
        elif type_ in TYPES_MODES_EMPLOI:
            contenu = servir_modes_emploi(source)
        else:                                   # outil : fichier -> lu, dossier -> liste
            contenu = lire_fichier(source) if source.is_file() else lire_dossier(source)
    except (OSError, ValueError) as erreur:
        return "", alertes, [identifiant + " : lecture impossible (" + str(erreur) + ")"]

    if "section" in entree:
        if not isinstance(contenu, str):
            return "", alertes, [identifiant + " : `section` declaree sur une source non textuelle"]
        extrait = extraire_section(contenu, entree["section"])
        if extrait is None:
            return "", alertes, [identifiant + " : section `" + str(entree["section"])
                                 + "` introuvable dans " + source.name]
        contenu = extrait

    return formater(entree, contenu, format_sortie), alertes, refus


def charger_peseur():
    """Le peseur de tokens du DOMICILE partage, ou None (le refus est alors NOMME)."""
    if not CHEMIN_TOKENS.is_file():
        return None
    specification = importlib.util.spec_from_file_location("tokens_catalogue", str(CHEMIN_TOKENS))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module.estimer_tokens


def peser(categorie, format_sortie):
    """MESURE REJOUABLE (demande createur 2026-09-20, MO-314) : le poids de chaque source.

    "Mesurer ce que l injection avant-mission coute en tokens MAINTENANT, et borner la
    carte." La mesure est donc un VERBE du catalogue, pas un script jetable : elle se
    rejoue apres chaque changement de contenu, et c est elle qui a montre que les QUATRE
    cartes pesaient 2452 tokens sur un total de 8004 avant la pose du plafond.
    """
    catalogue, refus_catalogue = charger_catalogue()
    if catalogue is None:
        print("REFUS : " + str(refus_catalogue))
        return CODE_REFUS
    estimer = charger_peseur()
    if estimer is None:
        print("REFUS : peseur de tokens ABSENT : " + str(CHEMIN_TOKENS)
              + " -- la mesure ne peut pas etre faite (jamais un 0 muet).")
        return CODE_REFUS
    if categorie == CATEGORIE_MISSION:
        entrees = [(phase, entree) for phase in PHASES_MISSION
                   for entree in catalogue.get(phase, [])]
    else:
        entrees = [(categorie, entree) for entree in catalogue.get(categorie, [])]
    if not entrees:
        print("REFUS : categorie `" + categorie + "` absente du catalogue.")
        return CODE_REFUS
    print("=== POIDS TOKENS -- " + categorie.upper() + " (estimation du domicile tokens.py) ===")
    total = 0
    for phase, entree in entrees:
        texte, _alertes, _refus = servir(entree, format_sortie)
        poids = estimer(texte)
        total += poids
        print("  " + str(poids).rjust(6) + "  " + str(entree.get("id", "?")))
    print("  " + str(total).rjust(6) + "  TOTAL " + categorie.upper())
    return CODE_OK


def injecter(categorie, format_sortie):
    """Sert une categorie entiere. Rend CODE_OK ou CODE_REFUS."""
    catalogue, refus_catalogue = charger_catalogue()
    if catalogue is None:
        print("REFUS : " + str(refus_catalogue))
        return CODE_REFUS

    if categorie == CATEGORIE_MISSION:
        entrees = [(phase, entree) for phase in PHASES_MISSION
                   for entree in catalogue.get(phase, [])]
    else:
        entrees = [(categorie, entree) for entree in catalogue.get(categorie, [])]

    if not entrees:
        print("REFUS : categorie `" + categorie + "` absente du catalogue (" + CONFIG_PATH.name + ")")
        print("(categories : " + ", ".join(sorted(catalogue)) + ", " + CATEGORIE_MISSION + ")")
        return CODE_REFUS

    print("=== INJECTIONS " + PILOTE.upper() + " - " + categorie.upper() + " ===")
    print("Horodatage: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Format: " + format_sortie)
    print()

    alertes = []
    refus = []
    servies = 0
    phase_courante = None
    for phase, entree in entrees:
        if phase != categorie and phase != phase_courante:
            print("--- phase : " + phase + " ---")
            phase_courante = phase
        texte, ses_alertes, ses_refus = servir(entree, format_sortie)
        for message in ses_alertes:
            alertes.append(message)
            print("  ALERTE : " + message)
        for message in ses_refus:
            refus.append(message)
            print("  REFUS  : " + message)
        if texte:
            servies += 1
            print(texte)
            print()

    print("--- " + str(servies) + " source(s) servie(s), " + str(len(alertes))
          + " alerte(s), " + str(len(refus)) + " refus ---")
    if refus:
        print("REFUS : le catalogue n'est pas entier -- reparer la source avant de continuer.")
        return CODE_REFUS
    return CODE_OK


def sources_fiche(catalogue, categorie):
    """Les sources d'une CATEGORIE, et leur obligation DITE (jamais supposee).

    `obligatoire` non declare est traite comme OBLIGATOIRE (doctrine du moteur)
    et la ligne le DIT : une fiche qui annoncerait moins qu'elle ne livre se
    lirait comme un chiffre faux (meme defaut que MO-314).
    """
    if categorie == CATEGORIE_MISSION:
        entrees = [(phase, entree) for phase in PHASES_MISSION
                   for entree in catalogue.get(phase, [])]
    else:
        entrees = [(categorie, entree) for entree in catalogue.get(categorie, [])]
    lignes = []
    for _phase, entree in entrees:
        declare = entree.get("obligatoire", None)
        if declare is None:
            marque = "obligatoire NON DECLARE (traite comme obligatoire)"
        else:
            marque = "obligatoire" if declare else "optionnelle"
        lignes.append("- " + str(entree.get("id", "?")) + " : "
                      + str(entree.get("description", "")) + " [" + marque + "]")
    return entrees, lignes


def rendre_moule(texte, jetons):
    """Rend un MOULE a jetons. Rend (rendu, jetons_inconnus).

    Aucun remplacement muet : un jeton que le moteur ne connait pas est RENDU
    TEL QUEL et NOMME a l'appelant, qui en fait un REFUS. Un moule a trou qui
    sortirait sans le dire se lirait comme une fiche complete (L-055).
    """
    inconnus = []

    def remplacer(correspondance):
        nom = correspondance.group(1)
        if nom not in jetons:
            inconnus.append(nom)
            return correspondance.group(0)
        return str(jetons[nom])

    return MOTIF_JETON.sub(remplacer, texte), inconnus


def fiche(categorie):
    """La FICHE TECHNIQUE DE TRAVAIL d'une CATEGORIE (moule a jetons, D1/D5).

    Le moule vit a SON domicile (templates/<categorie>/fiche.moule). La fiche
    BORNE : elle DIT les sources de la phase et leur obligation, elle ne
    REMPLACE jamais leur contenu. Refus NOMMES : catalogue absent, categorie
    inconnue, moule absent ou illisible, jeton inconnu -- jamais une fiche muette.
    """
    catalogue, refus_catalogue = charger_catalogue()
    if catalogue is None:
        print("REFUS : " + str(refus_catalogue))
        return CODE_REFUS
    if categorie == CATEGORIE_MISSION:
        print("REFUS : la fiche de `mission` est servie par l'injection de mission"
              " (injection/fonctions.py, verbe `pilote ordres`).")
        return CODE_REFUS
    if categorie not in catalogue:
        print("REFUS : categorie inconnue `" + categorie + "` pour `fiche`")
        print("(categories du catalogue : " + ", ".join(sorted(catalogue)) + ")")
        return CODE_REFUS
    chemin = CHEMIN_TEMPLATES / categorie / "fiche.moule"
    if not chemin.is_file():
        print("REFUS : moule de fiche ABSENT : " + str(chemin))
        return CODE_REFUS
    try:
        texte = chemin.read_text(encoding="utf-8")
    except OSError as erreur:
        print("REFUS : moule de fiche ILLISIBLE : " + str(chemin)
              + " (" + str(erreur) + ")")
        return CODE_REFUS
    entrees, lignes = sources_fiche(catalogue, categorie)
    if not entrees:
        print("REFUS : categorie `" + categorie + "` sans source -- rien a ficher.")
        return CODE_REFUS
    jetons = {
        "CATEGORIE": categorie,
        "DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "NB_SOURCES": len(entrees),
        "SOURCES": "\n".join(lignes),
    }
    rendu, inconnus = rendre_moule(texte, jetons)
    if inconnus:
        print("REFUS : jeton(s) INCONNU(S) du moteur de fiche : "
              + ", ".join(sorted(set(inconnus))))
        print("(jetons servis : " + ", ".join(JETONS_FICHE) + ")")
        return CODE_REFUS
    print(rendu)
    return CODE_OK


def main():
    arguments = sys.argv[1:]
    catalogue, refus_catalogue = charger_catalogue()
    if catalogue is None:
        print("REFUS : " + str(refus_catalogue))
        return CODE_REFUS

    categories = sorted(catalogue)
    if not arguments:
        print(__doc__)
        print("Categories du catalogue : " + ", ".join(categories) + " (+ " + CATEGORIE_MISSION + ")")
        return CODE_REFUS
    if arguments[0] == "--categories":
        for nom in categories:
            print(nom + " : " + str(len(catalogue[nom])) + " injection(s)")
        print(CATEGORIE_MISSION + " : les 3 phases de mission d'un coup")
        return CODE_OK
    if arguments[0] == "fiche":
        if len(arguments) < 2:
            print("REFUS : `fiche` attend une categorie (ex : fiche avant-mission).")
            return CODE_REFUS
        if len(arguments) > 2:
            print("REFUS : option inconnue pour `fiche` : " + " ".join(arguments[2:]))
            return CODE_REFUS
        return fiche(arguments[1])

    categorie = arguments[0]
    format_sortie = "texte"
    if "--format" in arguments:
        position = arguments.index("--format")
        if position + 1 >= len(arguments):
            print("REFUS : --format attend une valeur (" + "|".join(FORMATS) + ")")
            return CODE_REFUS
        format_sortie = arguments[position + 1]
    if format_sortie not in FORMATS:
        print("REFUS : format inconnu `" + format_sortie + "` (" + "|".join(FORMATS) + ")")
        return CODE_REFUS
    if categorie != CATEGORIE_MISSION and categorie not in categories:
        print("REFUS : categorie inconnue `" + categorie + "`")
        print("(categories du catalogue : " + ", ".join(categories) + ", " + CATEGORIE_MISSION + ")")
        return CODE_REFUS
    if "--peser" in arguments:
        return peser(categorie, format_sortie)
    return injecter(categorie, format_sortie)


if __name__ == "__main__":
    sys.exit(main())
