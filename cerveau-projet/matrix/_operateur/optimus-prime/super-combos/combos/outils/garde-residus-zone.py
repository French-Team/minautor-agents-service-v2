#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
garde-residus-zone.py -- Garde du CONTENU des zones jetables (MO-378).

LA LACUNE QUE CE GARDE FERME. `garde-tmp.py` juge le DOMICILE des zones et leur
README, et il se tait volontairement sur leur CONTENU (pendant une mission, des
cobayes y vivent legitimement). Personne, donc, n accusait un residu RESTE DANS
une zone apres une cloture : la zone vide n etait qu une discipline, jamais un
controle.

CE QU IL ACCUSE : une PURGE MENTIEUSE (un nom declare purge par le journal et
ENCORE PRESENT), un RESIDU (un nom hors forme canonique M- ou MO-), et une zone
SANS son README. Ce qu il INFORME sans accuser : un element canonique ACTIF, et le
FILET DE LA PORTE ECRIRE (un .bak.<horodatage>, MO-462) -- la sauvegarde que la
porte cree ELLE-MEME quand elle ecrit dans la zone n est pas < un fichier pose a la
main >. Sa forme est CONSOMMEE chez son domicile (data/outils/ecrire/constants.py),
comme le font deja les quatre autres lecteurs. En mode --cloture, lui seul reste un
ECART : la zone doit etre VIDE, filet compris.

MODE --cloture : apres une cloture, la zone doit etre VIDE (le README seul
demeure). Tout element encore present est alors un ECART. C est CE mode que le
pilote appelle a la cloture ; le maillon de non-regression appelle le mode par
defaut, qui ne criminalise pas un cobaye en vol.

IL CONSOMME les domiciles partages (matrice/data/commun/zone_tmp.py). Les MOTIFS
de nom canonique sont la FORME COMMUNE des deux portes, dont les domiciles sont
cites : matrice/data/outils/fichiers-travail-cameleon/constants.py (M-) et
_operateur/optimus-prime/super-combos/combos/outils/fichiers-travail.py (MO-).

code 0 = sain, code 1 = ecart detecte.
Usage: python garde-residus-zone.py [--racine <matrix/>] [--cloture]
       [--zone-optimus <chemin>] [--zone-cameleon <chemin>]
       [--journal-optimus <chemin>] [--journal-cameleon <chemin>] [--auto-test]
"""

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

_MATRICE = Path(__file__).resolve()
while _MATRICE.name != "matrix" and _MATRICE.parent != _MATRICE:
    _MATRICE = _MATRICE.parent
sys.path.insert(0, str(_MATRICE / "matrice" / "data" / "commun"))

from racine import detecter_racine  # noqa: E402
from cobayes_jetables import fixtures  # noqa: E402
from zone_tmp import (  # noqa: E402
    NOM_README,
    NOM_ZONE_CAMELEON,
    NOM_ZONE_OPTIMUS,
    chemin_zone_cameleon,
    chemin_zone_optimus,
    contenu as contenu_zone,
)

# La FORME COMMUNE des deux portes (M- du cameleon, MO- d Optimus) : un nom hors
# de ces deux formes est un residu, que personne ne peut purger par mission.
MOTIF_CANONIQUE = re.compile(r"^(m|mo)-([0-9]+)-([a-z0-9][a-z0-9-]*)\.([a-z0-9]+)$")
# Les deux ACTES que les journaux distinguent (memes mots que les portes).
ACTION_CREE = "cree"
ACTION_PURGE = "purge"

# Les journaux des DEUX portes, a leurs domiciles respectifs.
JOURNAL_CAMELEON = (_MATRICE / "matrice" / "data" / "outils"
                    / "fichiers-travail-cameleon"
                    / "fichiers-travail-cameleon-journal.jsonl")
JOURNAL_OPTIMUS = (_MATRICE / "_operateur" / "optimus-prime" / "super-combos"
                   / "combos" / "outils" / "fichiers-travail-journal.jsonl")

# --- LE FILET DE LA PORTE ECRIRE (MO-462 / EO-434) --------------------------
# Sa FORME vit a UN seul domicile -- matrice/data/outils/ecrire/constants.py,
# MOTIF_BAK_HORODATE -- et QUATRE consommateurs la lisent deja de la :
# espion-integrite-optimus, remorque-optimus, controle-attribution et
# verifier-contrat-fondamental. Ce garde etait le CINQUIEME, et le SEUL a ne pas
# la connaitre : mesure du 2026-09-25, la zone d'Optimus a porte
# mo-409-bilan.txt.bak.20260925_211625 -- la sauvegarde que la porte ECRIRE cree
# ELLE-MEME quand elle ecrit dans la zone -- et le garde l'a accusee en RESIDU
# < un fichier pose a la main >. Deux gardes du meme depot disaient donc le
# CONTRAIRE du MEME fichier : l'attribution EXCLUT ce motif (elle sait que ce
# n'est pas une ecriture d'agent), ce garde l'accusait.
DOMICILE_MOTIF_BAK = (_MATRICE / "matrice" / "data" / "outils" / "ecrire"
                      / "constants.py")
NOM_CONSTANTE_MOTIF_BAK = "MOTIF_BAK_HORODATE"


def charger_motif_bak():
    """La forme du point de restauration, LUE chez la porte qui la PRODUIT.

    AUCUNE recopie (M-076) : le motif est CONSOMME chez son domicile, comme les
    quatre autres lecteurs. Un domicile ABSENT, illisible ou invalide rend None --
    et le garde RETOMBE alors sur son jugement d'avant (un `.bak` accuse en RESIDU).
    C'est un choix ASSUME : une exclusion muette serait exactement l'angle mort que
    ce garde surveille, donc on echoue du cote qui ACCUSE, jamais du cote qui tait.
    """
    if not DOMICILE_MOTIF_BAK.is_file():
        return None
    dossier = str(DOMICILE_MOTIF_BAK.parent)
    ajoute = dossier not in sys.path
    if ajoute:
        sys.path.insert(0, dossier)
    try:
        specification = importlib.util.spec_from_file_location(
            "domicile_motif_bak", str(DOMICILE_MOTIF_BAK))
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except (ImportError, OSError, SyntaxError, AttributeError):
        return None
    finally:
        if ajoute and dossier in sys.path:
            sys.path.remove(dossier)
    motif = getattr(module, NOM_CONSTANTE_MOTIF_BAK, None)
    if not motif:
        return None
    try:
        return re.compile(motif)
    except re.error:
        return None


# LU UNE FOIS a l'import : la forme ne change pas en cours d'execution.
MOTIF_BAK = charger_motif_bak()


def est_filet_de_la_porte(nom):
    """Vrai si le nom est la SAUVEGARDE de la porte ECRIRE -- pas un residu.

    Un nom que personne ne journalise (< mo-409-bilan.txt.bak.20260925_211625 >) et
    qu'aucune mission ne peut purger : c'est la porte qui l'a pose, a chaque ecriture,
    et c'est elle qui le remplace au coup suivant. Sans motif lu, RIEN n'est reconnu
    comme filet (repli fail-closed, voir charger_motif_bak).
    """
    if MOTIF_BAK is None:
        return False
    return MOTIF_BAK.search(nom or "") is not None


def trouver_matrix(depart):
    """Le dossier matrix/ depuis <depart>, ou None."""
    depart = Path(depart).resolve()
    if depart.name == "matrix":
        return depart
    for candidat in (depart / "matrix", depart / "cerveau-projet" / "matrix"):
        if candidat.is_dir():
            return candidat
    for parent in depart.parents:
        if parent.name == "matrix":
            return parent
    return None


def journal_lire(chemin):
    """Les entrees lisibles du journal, dans l ORDRE (une ligne cassee est sautee)."""
    chemin = Path(chemin)
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
            continue
    return entrees


def etat_noms(chemin):
    """{nom: dernier acte} du journal -- le DERNIER acte dit l etat courant."""
    etats = {}
    for entree in journal_lire(chemin):
        nom = entree.get("nom")
        if nom:
            etats[nom] = entree.get("action")
    return etats


def est_canonique(nom):
    """Vrai si le nom porte la forme canonique d UNE des deux portes."""
    return MOTIF_CANONIQUE.match(nom or "") is not None



def juger_zone(nom_zone, chemin, journal, cloture):
    """Juge le CONTENU d une zone : rend (ecarts, infos). Aucun element tu."""
    ecarts = []
    infos = []
    chemin = Path(chemin)
    if not chemin.is_dir():
        infos.append(nom_zone + " : zone ABSENTE (" + str(chemin) + ") -- elle est"
                     " creee par le pilote de son flux (R-005), pas un ecart")
        return ecarts, infos
    if not (chemin / NOM_README).is_file():
        ecarts.append(nom_zone + " : zone SANS son README (" + str(chemin) + ")")
    etats = etat_noms(journal)
    for element in contenu_zone(chemin):
        nom = element.name
        if etats.get(nom) == ACTION_PURGE:
            ecarts.append(nom_zone + " / PURGE MENTIE : " + nom + " declare purge par"
                          " le journal et ENCORE PRESENT")
            continue
        if est_filet_de_la_porte(nom):
            # LE FILET DE LA PORTE ECRIRE (MO-462) : la sauvegarde qu'elle cree
            # ELLE-MEME n'est pas < un fichier pose a la main >. L'accuser etait un
            # FAUX diagnostic -- le garde nommait une main qui n'avait rien pose.
            # En mode --cloture il RESTE un ecart, et il est NOMME pour ce qu'il est :
            # apres une cloture la zone doit etre vide, filet compris (on n'excuse pas
            # un reste a la cloture, on le dit).
            if cloture:
                ecarts.append(nom_zone + " / RESTE A LA CLOTURE : " + nom + " (la zone"
                              " doit etre vide apres une cloture, filet compris)")
            else:
                infos.append(nom_zone + " / FILET : " + nom + " (sauvegarde de la porte"
                             " ECRIRE -- pas un fichier pose a la main)")
            continue
        if not est_canonique(nom):
            ecarts.append(nom_zone + " / RESIDU : " + nom + " (aucune forme canonique"
                          " M- ou MO-) -- un fichier pose a la main")
            continue
        if cloture:
            ecarts.append(nom_zone + " / RESTE A LA CLOTURE : " + nom + " (la zone doit"
                          " etre vide apres une cloture)")
            continue
        marque = ("pose par la porte" if etats.get(nom) == ACTION_CREE
                  else "canonique NON journalise")
        infos.append(nom_zone + " / ACTIF : " + nom + " (" + marque + ")")
    return ecarts, infos


def main():
    analyseur = argparse.ArgumentParser(description="Garde du contenu des zones jetables")
    analyseur.add_argument("--racine", default=".", help="Dossier matrix/ (defaut: cwd)")
    analyseur.add_argument("--cloture", action="store_true",
                           help="Apres une cloture : tout element restant est un ecart")
    analyseur.add_argument("--zone-optimus")
    analyseur.add_argument("--zone-cameleon")
    analyseur.add_argument("--journal-optimus")
    analyseur.add_argument("--journal-cameleon")
    analyseur.add_argument("--auto-test", action="store_true")
    args = analyseur.parse_args()
    if args.auto_test:
        return auto_test()

    matrix = trouver_matrix(Path(args.racine))
    if matrix is None:
        print("Dossier matrix/ introuvable depuis " + str(args.racine))
        return 2
    racine_workspace = detecter_racine(matrix)
    zones = (
        (NOM_ZONE_OPTIMUS,
         Path(args.zone_optimus) if args.zone_optimus else chemin_zone_optimus(matrix),
         Path(args.journal_optimus) if args.journal_optimus else JOURNAL_OPTIMUS),
        (NOM_ZONE_CAMELEON,
         Path(args.zone_cameleon) if args.zone_cameleon else chemin_zone_cameleon(racine_workspace),
         Path(args.journal_cameleon) if args.journal_cameleon else JOURNAL_CAMELEON),
    )
    ecarts = []
    infos = []
    for nom_zone, zone, journal in zones:
        ecarts_zone, infos_zone = juger_zone(nom_zone, zone, journal, args.cloture)
        ecarts.extend(ecarts_zone)
        infos.extend(infos_zone)
    for info in infos:
        print("INFO   : " + info)
    if ecarts:
        print("ECARTS : " + str(len(ecarts)) + " residu(s) de zone jetable :")
        for ecart in ecarts:
            print("  - " + ecart)
        return 1
    print("Zones saines : aucun residu, aucune purge mentie"
          + (", aucun reste a la cloture" if args.cloture else "") + ".")
    return 0



def auto_test():
    """Le cobaye MORD, le contre-temoin EPARGNE -- sur des zones JETABLES."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)

    with fixtures("cobaye-garde-residus-zone-") as dossier:
        zone = dossier / "tmp-optimus"
        zone.mkdir(parents=True, exist_ok=True)
        (zone / NOM_README).write_text("readme", encoding="utf-8", newline="\n")
        journal = dossier / "journal.jsonl"

        ecarts, _ = juger_zone("zone", zone, journal, False)
        controler("CONTRE-TEMOIN : zone propre au README seul -> 0 ecart",
                  not ecarts, str(ecarts))

        (zone / "residu-a-la-main.txt").write_text("x", encoding="utf-8")
        ecarts, _ = juger_zone("zone", zone, journal, False)
        controler("le GARDE CRIE sur un residu non canonique",
                  len(ecarts) == 1, str(ecarts))

        with open(str(journal), "a", encoding="utf-8", newline="\n") as flux:
            flux.write(json.dumps({"action": ACTION_CREE, "nom": "m-378-bilan.txt"}) + "\n")
            flux.write(json.dumps({"action": ACTION_PURGE, "nom": "m-378-bilan.txt"}) + "\n")
        (zone / "m-378-bilan.txt").write_text("x", encoding="utf-8")
        ecarts, _ = juger_zone("zone", zone, journal, False)
        controler("le GARDE CRIE sur une PURGE MENTIE",
                  any("PURGE MENTIE" in ecart for ecart in ecarts), str(ecarts))

        (zone / "m-378-bilan.txt").unlink()
        with open(str(journal), "a", encoding="utf-8", newline="\n") as flux:
            flux.write(json.dumps({"action": ACTION_CREE, "nom": "mo-379-note.txt"}) + "\n")
        (zone / "mo-379-note.txt").write_text("x", encoding="utf-8")
        ecarts, infos = juger_zone("zone", zone, journal, False)
        controler("un canonique ACTIF n est PAS accuse",
                  not any("mo-379-note.txt" in ecart for ecart in ecarts), str(ecarts))
        controler("il est bien INFORME",
                  any("mo-379-note.txt" in info for info in infos), str(infos))

        ecarts, _ = juger_zone("zone", zone, journal, True)
        controler("mode --cloture : tout element restant est un ECART",
                  len(ecarts) >= 2, str(ecarts))

        ecarts, _ = juger_zone("zone", dossier / "tmp-absente", journal, True)
        controler("une zone ABSENTE est INFORME, jamais accuse", not ecarts, str(ecarts))

        (zone / "residu-a-la-main.txt").unlink()
        (zone / "mo-379-note.txt").unlink()
        ecarts, _ = juger_zone("zone", zone, journal, True)
        controler("CONTRE-TEMOIN : zone vide a la cloture -> 0 ecart",
                  not ecarts, str(ecarts))

        # LE FILET DE LA PORTE ECRIRE (MO-462 / EO-434). L'exemple porte un
        # horodatage comme la porte en pose un ; c'est la FORME qui est CONSOMMEE
        # chez son domicile (est_filet_de_la_porte), et c'est elle qui est verifiee.
        # Si la porte change un jour sa forme, cette epreuve ROUGIT : le garde ne
        # peut donc pas se mettre a ignorer des fichiers qu'elle ne produit plus.
        controler("la FORME du filet est bien LUE chez la porte (jamais recopiee)",
                  MOTIF_BAK is not None,
                  "domicile " + str(DOMICILE_MOTIF_BAK) + " -> " + repr(MOTIF_BAK))
        filet = "mo-462-bilan.txt.bak.20260925_211625"
        controler("l'exemple du cobaye porte bien la FORME lue chez la porte",
                  est_filet_de_la_porte(filet), repr(filet))
        (zone / filet).write_text("x", encoding="utf-8")
        ecarts, infos = juger_zone("zone", zone, journal, False)
        controler("un FILET de la porte n est plus un RESIDU (il est INFORME)",
                  not any(filet in ecart for ecart in ecarts)
                  and any(filet in info for info in infos),
                  "ecarts=" + str(ecarts) + " infos=" + str(infos))
        ecarts, _ = juger_zone("zone", zone, journal, True)
        controler("CONTRE-TEMOIN : a la CLOTURE le filet RESTE un ecart (zone vide)",
                  any(filet in ecart for ecart in ecarts), str(ecarts))
        (zone / filet).unlink()
        presque = "mo-463-bilan.txt.bak"
        (zone / presque).write_text("x", encoding="utf-8")
        ecarts, _ = juger_zone("zone", zone, journal, False)
        controler("CONTRE-TEMOIN : un nom qui RESSEMBLE au filet reste ACCUSE",
                  any(presque in ecart for ecart in ecarts), str(ecarts))
        (zone / presque).unlink()
        ecarts, _ = juger_zone("zone", zone, journal, True)
        controler("CONTRE-TEMOIN : filet retire, la zone est VIDE a la cloture",
                  not ecarts, str(ecarts))

    print("AUTO-TEST : " + str(sum(resultats)) + "/" + str(len(resultats)) + " epreuves vertes")
    return 0 if all(resultats) else 1


if __name__ == "__main__":
    sys.exit(main())
