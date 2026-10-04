#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fichiers-travail.py -- LA PORTE DES FICHIERS DE TRAVAIL D UNE MISSION (MO-374).

LA QUESTION A LAQUELLE RIEN NE REPONDAIT : ou vivent les fichiers de travail d une
mission, QUI les a poses, et QUAND disparaissent-ils ? Mesure MO-371 : la zone
jetable d Optimus portait 20 fichiers + 1 dossier issus d un travail NON pilote,
donc sans cloture et sans purge ; et les fichiers de travail naissaient a la main,
par la porte ECRIRE, sous des noms libres (paires/*.ancien, *.nouveau) que RIEN
ne reliait a une mission.

CETTE PORTE REND L INVISIBLE VISIBLE. Elle NOMME (un nom canonique PAR MISSION),
elle LISTE (ce que la zone porte, canonique ou residu), elle MONTRE (le contenu
d un fichier), elle VIDE (le solde de la zone), et elle JOURNALISE (ce qui a ete
cree, par qui, quand c est purge). Le createur ne voit pas ce qui se passe : ce
journal est aussi pour CA.

UN NOM CANONIQUE, POUR QUOI FAIRE ? Tout element de travail d une mission s appelle
<mission minuscule>-<libelle>.<extension>, par exemple mo-374-bilan.txt. Le nom
PORTE la mission, donc la lecture et la purge n ont plus besoin d une liste tenue
a la main ; et un element qui ne porte pas cette forme est un RESIDU -- VU, NOMME,
jamais silencieux.

ELLE CONSOMME LES DOMICILES PARTAGES, ELLE NE LES RECOPIE PAS (M-076) :
matrice/data/commun/zone_tmp.py fournit le chemin DECLARE de la zone, la liste de
son contenu et sa purge ; matrice/data/commun/cobayes_jetables.py fournit le
dossier de fixtures de l auto-test. Le nom de la zone n est JAMAIS redevine ici.

Usage (par le lanceur, jamais par un chemin de brique recopie) :
  python3 cerveau-projet/matrix/lancer.py fichiers-travail nommer --mission MO-374 --libelle bilan
  python3 cerveau-projet/matrix/lancer.py fichiers-travail lister [--mission MO-374] [--strict] [--json]
  python3 cerveau-projet/matrix/lancer.py fichiers-travail montrer mo-374-bilan.txt
  python3 cerveau-projet/matrix/lancer.py fichiers-travail vider [--mission MO-374] [--par <qui>]
  python3 cerveau-projet/matrix/lancer.py fichiers-travail journal [--n 20]
  python3 cerveau-projet/matrix/lancer.py fichiers-travail --auto-test

CODES DE SORTIE : 0 ok ; 1 ecart (purge partielle, ou --strict devant un residu) ;
2 refus.
"""

import sys
import re
import json
import shutil
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).resolve().parent

# Racine matrix/ DETECTEE par le marqueur partage (matrice/data/commun/racine.py),
# jamais comptee a la main (L-013).
BORNES_REMONTEE = 30
_courant = BASE
for _ in range(BORNES_REMONTEE):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        break
    _courant = _courant.parent
else:
    raise RuntimeError("Racine matrix/ introuvable en remontant depuis " + str(BASE))
RACINE_MATRIX = _courant
REPERTOIRE_COMMUN = RACINE_MATRIX / "matrice" / "data" / "commun"
if str(REPERTOIRE_COMMUN) not in sys.path:
    sys.path.insert(0, str(REPERTOIRE_COMMUN))

# DOMICILES PARTAGES (M-076) : CONSOMMES, jamais recopies.
from zone_tmp import contenu as contenu_zone, vider as vider_zone, chemin_zone_optimus  # noqa: E402
from cobayes_jetables import fixtures  # noqa: E402

# La ZONE de ce flux, par son domicile DECLARE (zone_tmp.chemin_zone_optimus).
ZONE_DEFAUT = chemin_zone_optimus(RACINE_MATRIX)

# LE JOURNAL VIT A COTE DE LA PORTE (un etat, pas une source) : en AJOUT SEUL
# (.jsonl). La forme est declaree comme etat par la remorque, donc le journal
# n est pas compte comme equipement ; et aucune de ses lignes n est reecrite.
JOURNAL_DEFAUT = BASE / "fichiers-travail-journal.jsonl"

# NOM CANONIQUE : <mission minuscule>-<libelle>.<extension>. Un nom qui porte
# cette forme EST canonique ; la mission s y relit sans liste tenue a la main.
MOTIF_MISSION = re.compile(r"^(mo|m)-([0-9]+)$")
MOTIF_CANONIQUE = re.compile(r"^(mo|m)-([0-9]+)-([a-z0-9][a-z0-9-]*)\.([a-z0-9]+)$")
MOTIF_LIBELLE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
# `jsonl` (reprise MO-500) : le segment de raisonnement que la LOI DU ROUND fait
# deposer a la cloture est un fichier d OBJETS JSON PAR LIGNE -- la liste des
# extensions de travail l ignorait, donc la porte REFUSAIT de poser un nom que la loi
# prescrit (mo-XXX-segment.jsonl) ; le nom etait alors cree par la porte ECRIRE, et le
# journal accusait ensuite < PURGE MENTIE > (declare purge, encore present). Le format
# .jsonl est deja celui des traces du projet (defauts, verdicts).
EXTENSIONS = ("txt", "md", "json", "jsonl", "py", "log", "base64")
ACTION_CREE = "cree"
ACTION_PURGE = "purge"
LIGNES_MONTREES = 200
PAR_DEFAUT = "optimus-prime"


def maintenant():
    """L horodatage du journal, seconde : la forme commune des traces du projet."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def chemin_relatif(chemin):
    """Le chemin RELATIF a la racine de la Matrice, en barres obliques."""
    try:
        return Path(chemin).resolve().relative_to(RACINE_MATRIX.resolve()).as_posix()
    except (ValueError, OSError):
        return str(chemin).replace(chr(92), "/")


def nom_canonique(mission, libelle, extension):
    """Le NOM CANONIQUE d un fichier de travail, ou (None, refus NOMME).

    Trois champs, trois refus DISTINCTS et nommes : une mission hors forme, un
    libelle hors forme, une extension hors liste. Le nom rendu porte la mission
    en minuscules (convention des objets de la Matrice : minuscules a tirets).
    """
    mission = (mission or "").strip().lower()
    libelle = (libelle or "").strip().lower()
    extension = (extension or "").strip().lower().lstrip(".")
    if not MOTIF_MISSION.match(mission):
        return None, ("REFUS : identifiant de mission invalide (< " + str(mission)
                      + " >) -- forme attendue MO-<numero>, par exemple MO-374.")
    if not MOTIF_LIBELLE.match(libelle):
        return None, ("REFUS : libelle invalide (< " + str(libelle)
                      + " >) -- minuscules, chiffres et tirets : par exemple bilan.")
    if extension not in EXTENSIONS:
        return None, ("REFUS : extension < " + str(extension) + " > hors liste -- "
                      + ", ".join(EXTENSIONS) + ".")
    return mission + "-" + libelle + "." + extension, None


def mission_du_nom(nom):
    """L identifiant de mission PORTE par un nom canonique, ou None."""
    trouve = MOTIF_CANONIQUE.match(nom or "")
    if not trouve:
        return None
    return trouve.group(1) + "-" + trouve.group(2)


def est_canonique(nom):
    """Vrai si le nom porte la forme canonique (la porte l a nomme ou non)."""
    return MOTIF_CANONIQUE.match(nom or "") is not None


def journal_lire(chemin_journal=None):
    """Les entrees du journal, dans l ORDRE, ligne par ligne.

    Une ligne ILLISIBLE n est pas avalee : elle est rendue sous l action
    `illisible` avec son texte brut -- un journal qui cache une ligne qu il ne
    comprend pas se lirait comme un journal complet.
    """
    chemin = Path(chemin_journal or JOURNAL_DEFAUT)
    entrees = []
    if not chemin.is_file():
        return entrees
    try:
        lignes = chemin.read_text(encoding="utf-8").splitlines()
    except OSError:
        return entrees
    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            entrees.append(json.loads(ligne))
        except ValueError:
            entrees.append({"action": "illisible", "brut": ligne})
    return entrees


def journal_noter(entree, chemin_journal=None):
    """Ajoute UNE entree horodatee au journal (ajout seul, jamais de reecriture)."""
    chemin = Path(chemin_journal or JOURNAL_DEFAUT)
    entree = dict(entree)
    entree["date"] = maintenant()
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(str(chemin), "a", encoding="utf-8", newline="\n") as flux:
        flux.write(json.dumps(entree, ensure_ascii=True) + "\n")
    return entree


def noms_journalises(chemin_journal=None):
    """{nom: entree} des noms POSES par la porte (au moins une ligne `cree`)."""
    poses = {}
    for entree in journal_lire(chemin_journal):
        if entree.get("action") == ACTION_CREE and entree.get("nom"):
            poses[entree["nom"]] = entree
    return poses


def elements_zone(zone, chemin_journal=None):
    """La zone, element par element, avec sa CLASSE -- aucun element tu.

    Trois classes, DITES :
      - `canonique` : le nom porte <mission>-<libelle>.<ext> ET la porte l a pose
        (une ligne `cree` de son journal) ;
      - `canonique-non-journalise` : la forme est canonique, mais la porte ne l a
        jamais pose -- un fichier ne hors de la porte, ce qui se DIT ;
      - `residu` : le nom ne porte AUCUNE forme canonique -- le cas d un fichier
        pose a la main, que cette porte REND VISIBLE.
    """
    journalises = noms_journalises(chemin_journal)
    elements = []
    for element in contenu_zone(zone):
        nom = element.name
        try:
            stat = element.stat()
            taille = stat.st_size if element.is_file() else -1
            modifie = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        except OSError:
            taille, modifie = -1, ""
        canonique = est_canonique(nom)
        if canonique and nom in journalises:
            classe = "canonique"
        elif canonique:
            classe = "canonique-non-journalise"
        else:
            classe = "residu"
        elements.append({"nom": nom, "dossier": element.is_dir(), "taille": taille,
                         "modifie": modifie, "canonique": canonique,
                         "mission": mission_du_nom(nom) or "", "classe": classe})
    return elements


def nommer(zone, mission, libelle, extension, par, chemin_journal=None):
    """Pose le fichier de travail d une mission sous son NOM CANONIQUE.

    Une pose n ECRASE JAMAIS un fichier existant : elle le DIT et laisse le
    contenu intact (meme regle que poser-template-pilote). L acte est journalise
    dans les DEUX cas, avec son resultat -- un `deja-pose` est un fait, pas rien.
    Rend (code, message, chemin).
    """
    zone = Path(zone)
    nom, refus = nom_canonique(mission, libelle, extension)
    if refus:
        return 2, refus, None
    if not zone.is_dir():
        return 2, ("REFUS : la zone " + str(zone) + " n existe pas -- elle est creee"
                   " par le pilote de son flux (regle R-005)."), None
    cible = zone / nom
    if cible.exists():
        journal_noter({"action": ACTION_CREE, "resultat": "deja-pose", "nom": nom,
                       "mission": mission.strip().lower(), "par": par}, chemin_journal)
        return 0, ("DEJA POSE : " + nom + " existe -- rien n a ete ecrit, contenu intact."), cible
    try:
        with open(str(cible), "w", encoding="utf-8", newline="\n") as flux:
            flux.write("")
    except OSError as erreur:
        return 1, ("ECHEC : pose impossible (" + str(erreur) + ")."), None
    journal_noter({"action": ACTION_CREE, "resultat": "pose", "nom": nom,
                   "mission": mission.strip().lower(), "par": par,
                   "chemin": chemin_relatif(cible)}, chemin_journal)
    return 0, ("POSE : " + nom + " (" + chemin_relatif(cible) + ")"), cible


def montrer(zone, nom):
    """Le CONTENU d un element de la zone, par son SEUL nom.

    Le nom est un NOM, jamais un chemin (un separateur est un REFUS) : la porte
    ne sert pas un fichier hors de sa zone. Un nom absent est refuse en NOMMANT
    ce que la zone porte -- un vide muet se lirait comme une zone vide.
    Rend (code, texte).
    """
    zone = Path(zone)
    if not nom or nom in (".", "..") or "/" in nom or chr(92) in nom:
        return 2, ("REFUS : < montrer > prend un NOM, jamais un chemin (recu : "
                   + str(nom) + ").")
    cible = zone / nom
    if not cible.is_file():
        presents = ", ".join(element["nom"] for element in elements_zone(zone)) or "aucun"
        return 2, ("REFUS : " + nom + " absent de " + chemin_relatif(zone)
                   + " -- presents : " + presents)
    try:
        lignes = cible.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as erreur:
        return 2, "REFUS : lecture impossible (" + str(erreur) + ")."
    bloc = ["# " + nom + " (" + str(len(lignes)) + " ligne(s))"]
    if len(lignes) > LIGNES_MONTREES:
        bloc.append("... " + str(len(lignes) - LIGNES_MONTREES) + " ligne(s) non affichee(s) ...")
        lignes = lignes[:LIGNES_MONTREES]
    bloc.extend(lignes)
    return 0, "\n".join(bloc)


def vider(zone, mission, par, chemin_journal=None):
    """VIDE la zone (ou les elements d UNE mission) et journalise chaque retrait.

    La purge de TOUTE la zone passe par le moteur PARTAGE (zone_tmp.vider) : ce
    n est pas la logique de cette porte, c est celle des deux flux, et elle rend
    ses echecs au lieu de les avaler. La purge CIBLEE ne traite que les elements
    dont le nom porte la mission (forme canonique) ou commence par son prefixe.
    Rend (code, rapport) : le rapport porte `supprimes`, `echecs` et `restants`,
    et le SOLDE est journalise avec chaque retrait.
    """
    zone = Path(zone)
    if not zone.is_dir():
        return 0, {"supprimes": [], "echecs": [], "restants": []}
    mission = (mission or "").strip().lower()
    if mission:
        prefixe = mission + "-"
        supprimes, echecs = [], []
        for element in contenu_zone(zone):
            nom = element.name
            if mission_du_nom(nom) != mission and not nom.startswith(prefixe):
                continue
            try:
                if element.is_dir():
                    shutil.rmtree(str(element))
                else:
                    element.unlink()
                supprimes.append(nom)
            except OSError:
                echecs.append(nom)
    else:
        supprimes, echecs = vider_zone(zone)
    restants = [element["nom"] for element in elements_zone(zone, chemin_journal)]
    for nom in supprimes:
        journal_noter({"action": ACTION_PURGE, "nom": nom,
                       "mission": mission_du_nom(nom) or "", "par": par,
                       "solde": len(restants)}, chemin_journal)
    rapport = {"supprimes": supprimes, "echecs": echecs, "restants": restants}
    return (1 if echecs else 0), rapport


def afficher_lister(zone, elements, mission_filtre=None):
    """La VUE de la zone : chaque element, sa classe, et le compte par classe."""
    lignes = ["ZONE : " + chemin_relatif(zone)]
    vus = elements
    hors_filtre = []
    if mission_filtre:
        mission_filtre = mission_filtre.strip().lower()
        vus = [element for element in elements if element["mission"] == mission_filtre]
        hors_filtre = [element for element in elements if element["mission"] != mission_filtre]
    if not elements:
        lignes.append("  (zone vide : aucun fichier de travail, aucun residu)")
        return lignes
    for element in vus:
        marque = "dossier" if element["dossier"] else str(element["taille"]) + " o"
        lignes.append("  [" + element["classe"].upper() + "] " + element["nom"]
                      + "  (" + marque + ", " + element["modifie"] + ")")
    comptes = {}
    for element in elements:
        comptes[element["classe"]] = comptes.get(element["classe"], 0) + 1
    lignes.append("  TOTAL : " + str(len(elements)) + " element(s) -- "
                  + ", ".join(cle + " " + str(valeur) for cle, valeur in sorted(comptes.items())))
    if mission_filtre is not None:
        lignes.append("  HORS FILTRE (" + str(mission_filtre) + ") : " + str(len(hors_filtre))
                      + " element(s) -- aucun n est cache")
    return lignes


def _options(arguments, connues, drapeaux=()):
    """Rend (options, positionnels, refus) -- une option INCONNUE est un REFUS NOMME."""
    options = {}
    positionnels = []
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument.startswith("--"):
            nom = argument[2:]
            if nom not in connues:
                return None, None, ("REFUS : option inconnue < " + argument + " > -- connues : "
                                    + ", ".join("--" + connu for connu in connues) + ".")
            if nom in drapeaux:
                options[nom] = True
                index += 1
                continue
            if index + 1 >= len(arguments):
                return None, None, "REFUS : option sans valeur < " + argument + " >."
            options[nom] = arguments[index + 1]
            index += 2
            continue
        positionnels.append(argument)
        index += 1
    return options, positionnels, None


CONNUES = {
    "nommer": ("mission", "libelle", "extension", "par", "zone", "journal"),
    "lister": ("mission", "zone", "journal", "strict", "json"),
    "montrer": ("zone",),
    "vider": ("mission", "par", "zone", "journal"),
    "journal": ("n", "journal", "json"),
}
DRAPEAUX = ("strict", "json")


def principal(arguments):
    """Route le verbe et rend le code de sortie (0 ok, 1 ecart, 2 refus)."""
    if not arguments or arguments[0] in ("-h", "--help", "--aide"):
        print(__doc__)
        return 2
    if arguments[0] == "--auto-test":
        return auto_test()
    verbe = arguments[0]
    if verbe not in CONNUES:
        print("REFUS : verbe inconnu < " + verbe + " > -- connus : "
              + ", ".join(sorted(CONNUES)) + ".")
        return 2
    options, positionnels, refus = _options(arguments[1:], CONNUES[verbe], DRAPEAUX)
    if refus:
        print(refus)
        return 2
    zone = Path(options.get("zone") or ZONE_DEFAUT)
    chemin_journal = Path(options.get("journal") or JOURNAL_DEFAUT)
    par = options.get("par") or PAR_DEFAUT

    if verbe == "nommer":
        if not options.get("mission") or not options.get("libelle"):
            print("REFUS : nommer exige --mission et --libelle.")
            return 2
        code, message, _ = nommer(zone, options["mission"], options["libelle"],
                                  options.get("extension") or "txt", par, chemin_journal)
        print(message)
        return code

    if verbe == "lister":
        elements = elements_zone(zone, chemin_journal)
        if options.get("json"):
            print(json.dumps({"zone": chemin_relatif(zone), "elements": elements},
                             ensure_ascii=True))
        else:
            for ligne in afficher_lister(zone, elements, options.get("mission")):
                print(ligne)
            entrees = journal_lire(chemin_journal)
            poses = len([e for e in entrees if e.get("action") == ACTION_CREE])
            purges = len([e for e in entrees if e.get("action") == ACTION_PURGE])
            print("  JOURNAL : " + str(len(entrees)) + " entree(s) -- " + str(poses)
                  + " cree(s), " + str(purges) + " purge(s)")
        ecarts = [element for element in elements if element["classe"] != "canonique"]
        if options.get("strict") and ecarts:
            print("ECART : " + str(len(ecarts)) + " element(s) hors forme canonique"
                  " (residu ou non journalise) -- la porte les a NOMMES.")
            return 1
        return 0

    if verbe == "montrer":
        if len(positionnels) != 1:
            print("REFUS : montrer exige UN nom, par exemple montrer mo-374-bilan.txt.")
            return 2
        code, texte = montrer(zone, positionnels[0])
        print(texte)
        return code

    if verbe == "vider":
        code, rapport = vider(zone, options.get("mission"), par, chemin_journal)
        print("PURGE : " + str(len(rapport["supprimes"])) + " retire(s) -- solde "
              + str(len(rapport["restants"])) + " element(s) dans la zone.")
        for nom in rapport["supprimes"]:
            print("  - retire : " + nom)
        for nom in rapport["echecs"]:
            print("  ! ECHEC  : " + nom + " (non retire -- la purge partielle se DIT)")
        for nom in rapport["restants"]:
            print("  = reste  : " + nom)
        if not rapport["supprimes"] and not rapport["restants"]:
            print("  (la zone etait deja vide)")
        return code

    # journal : les derniers actes, dans l ORDRE
    entrees = journal_lire(chemin_journal)
    try:
        limite = int(options.get("n") or 20)
    except (TypeError, ValueError):
        print("REFUS : --n attend un nombre.")
        return 2
    tranche = entrees[-limite:]
    if options.get("json"):
        print(json.dumps(tranche, ensure_ascii=True))
        return 0
    print("JOURNAL : " + chemin_relatif(chemin_journal) + " -- " + str(len(entrees))
          + " entree(s), " + str(len(tranche)) + " affichee(s)")
    for entree in tranche:
        detail = entree.get("nom", entree.get("brut", ""))
        complement = ""
        if entree.get("action") == ACTION_PURGE:
            complement = " (solde " + str(entree.get("solde", "?")) + ")"
        elif entree.get("resultat"):
            complement = " [" + str(entree["resultat"]) + "]"
        print("  " + str(entree.get("date", "")) + " " + str(entree.get("action", ""))
              + " " + str(detail) + " par " + str(entree.get("par", "")) + complement)
    return 0


def auto_test():
    """Le cobaye MORD, le contre-temoin EPARGNE (L-032) -- sur un dossier JETABLE.

    Le dossier de fixtures est FOURNI par la fabrique PARTAGEE
    (cobayes_jetables.fixtures) : elle le retire TOUJOURS, meme si une epreuve
    leve. Aucune epreuve ne touche la zone reelle.
    """
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)

    with fixtures("cobaye-fichiers-travail-") as dossier:
        zone = dossier / "tmp-cobaye"
        zone.mkdir(parents=True, exist_ok=True)
        journal = dossier / "cobaye-journal.jsonl"

        nom, _ = nom_canonique("MO-374", "bilan", "txt")
        controler("le nom canonique se compose", nom == "mo-374-bilan.txt", str(nom))
        _, refus_mission = nom_canonique("374", "bilan", "txt")
        controler("une mission hors forme est REFUSEE", refus_mission is not None,
                  str(refus_mission)[:70])
        _, refus_extension = nom_canonique("MO-374", "bilan", "exe")
        controler("une extension hors liste est REFUSEE", refus_extension is not None,
                  str(refus_extension)[:70])
        controler("le nom canonique se RELIT en mission",
                  mission_du_nom(nom) == "mo-374", str(mission_du_nom(nom)))

        controler("la zone est VIDE avant la pose",
                  not elements_zone(zone, journal), "0 element")
        code, message, _ = nommer(zone, "MO-374", "bilan", "txt", "optimus-prime", journal)
        apres = elements_zone(zone, journal)
        controler("la pose reussit", code == 0, message)
        controler("lister VOIT le fichier pose par la porte",
                  [element["nom"] for element in apres] == ["mo-374-bilan.txt"],
                  str([element["nom"] for element in apres]))
        controler("il est classe CANONIQUE et porte sa mission",
                  bool(apres) and apres[0]["classe"] == "canonique"
                  and apres[0]["mission"] == "mo-374",
                  apres[0]["classe"] if apres else "")

        (zone / "paires").mkdir()
        (zone / "paires" / "routeur.ancien").write_text("x", encoding="utf-8")
        (zone / "residu-a-la-main.txt").write_text("x", encoding="utf-8")
        classes = {element["nom"]: element["classe"] for element in elements_zone(zone, journal)}
        controler("un FICHIER pose a la main est VU comme RESIDU",
                  classes.get("residu-a-la-main.txt") == "residu",
                  str(classes.get("residu-a-la-main.txt")))
        controler("un DOSSIER pose a la main est VU comme RESIDU",
                  classes.get("paires") == "residu", str(classes.get("paires")))
        controler("le fichier de la porte n est PAS un residu (contre-temoin)",
                  classes.get("mo-374-bilan.txt") == "canonique",
                  str(classes.get("mo-374-bilan.txt")))

        code, rapport = vider(zone, None, "optimus-prime", journal)
        restants = elements_zone(zone, journal)
        controler("vider SOLDE la zone", not restants, str(len(restants)))
        controler("vider NOMME les trois elements retires",
                  sorted(rapport["supprimes"]) == ["mo-374-bilan.txt", "paires",
                                                   "residu-a-la-main.txt"],
                  str(sorted(rapport["supprimes"])))
        actes = [(entree.get("action"), entree.get("nom")) for entree in journal_lire(journal)]
        controler("le journal DIT la pose",
                  (ACTION_CREE, "mo-374-bilan.txt") in actes, str(actes))
        controler("le journal DIT CHAQUE purge",
                  all((ACTION_PURGE, element) in actes for element in rapport["supprimes"]),
                  str(actes))
        controler("le contre-temoin est AVEUGLE : sans la porte, aucun acte n est trace",
                  journal_lire(dossier / "cobaye-journal-absent.jsonl") == [], "0 entree")

    print("AUTO-TEST : " + str(sum(resultats)) + "/" + str(len(resultats)) + " epreuves vertes")
    return 0 if all(resultats) else 1


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
