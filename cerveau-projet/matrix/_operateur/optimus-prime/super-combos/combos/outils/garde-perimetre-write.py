#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
garde-perimetre-write.py -- Garde WRITE=matrix/ (M-098)

Signale tout fichier hors perimetre d ecriture d Optimus.
Perimetre : cerveau-projet/matrix/ (+ la declaration de la PORTE ECRIRE pour la racine).

DEUX DEFAUTS DE PARCOURS REPARES (MO-495, mesure du 2026-09-27/29).

(1) LES FICHIERS DE LA RACINE N ETAIENT JAMAIS EXAMINES. Le walk elaguait la branche
    qui mene au perimetre, puis faisait `continue` -- ce `continue` sautait la boucle
    des fichiers du dossier COURANT. Or le dossier courant, quand il est un ANCETRE du
    perimetre, c est la RACINE du workspace (et cerveau-projet/) : leurs fichiers
    n etaient donc JAMAIS juges. L ALLOWLIST racine etait du CODE MORT (jamais
    atteinte), et le garde rendait < perimetre sain > quoi qu on pose a la racine.
    Mesure : un fichier cobaye pose a la racine rendait exit 0 ; le MEME fichier dans
    un sous-dossier etait accuse. Le garde juge desormais les fichiers du dossier qu il
    elargue : on elague une DESCENTE, pas un JUGEMENT.

(2) LA BRANCHE ELARGUEE CONTENAIT TOUT LE CERVEAU v1/v2. L elagage retirait le PREMIER
    morceau du chemin vers le perimetre (cerveau-projet), donc le cerveau v1/v2 entier
    -- ou la regle immuable interdit d ecrire -- n etait ni parcouru ni juge. Le seul
    dossier retire de la descente est desormais le PERIMETRE LUI-MEME (matrix/).
    DECISION MESUREE du 2026-09-29 : `cerveau-projet/` hors matrix EST surveille, parce
    que la regle < Je ne modifie JAMAIS le cerveau v1/v2 > ne se garde que si on le
    regarde ; mesure de la fenetre 7 j : AUCUN fichier n y a ete ecrit (le corpus v1/v2
    est dormant depuis le 2026-09-05), donc cette surveillance ne coute aucun faux rouge
    aujourd hui. Si une session v1/v2 reprend, le remede est une exemption DECLAREE et
    VISIBLE (famille EO-408, artefacts exterieurs), jamais un elagage muet.

LA DECLARATION DE LA PORTE ECRIRE EST CONSOMMEE, JAMAIS RECOPIEE (M-076, L-207/L-211).
Deux instruments de la meme maison declaraient le perimetre de la racine et ne disaient
pas la MEME chose : ce garde portait sa liste ecrite a la main (2 demarrages) tandis que
la porte ECRIRE -- l instrument qui ECRIT reellement -- en autorisait davantage
(`AGENTS.md`, que la v3 met a jour par sa porte dediee `editer-agents-md`). Un fichier
ecrit par la porte et accuse par le garde serait un rouge que personne ne peut reparer
(L-210). L allowlist racine et la FORME du point de restauration sont donc LUES chez
elle (`matrice/data/outils/ecrire/constants.py`), comme le font deja cinq autres
lecteurs ; le garde ne recopie plus ni la liste, ni le motif.

CE QU IL MET DE COTE, ET LE DIT (exemptions visibles, MO-075) :
  - les ARBRES d un OUTIL ETRANGER (`.kilo/worktrees`, domicile partage
    matrice/data/commun/artefacts_externes.py) : comptes A PART, NOMMES avec leur date
    de naissance (EO-408). La portee est MESUREE avant tout refus (L-286) ;
  - le FILET DE LA PORTE (un `X.bak.<horodatage>` dont le nom de BASE est autorise par
    la porte) : c est la sauvegarde que la porte cree ELLE-MEME a chaque ecriture, pas
    un fichier pose a la main. Une sauvegarde d un fichier NON autorise, elle, reste une
    ecriture interdite : elle s ACCUSE.

REPLIS, TOUS DU COTE QUI ACCUSE (jamais une exemption muette) : une declaration de porte
ABSENTE ou ILLISIBLE n accorde AUCUNE exemption racine (et le garde le DIT), et aucun
filet n est reconnu.

Usage: python garde-perimetre-write.py [--jours N] [--racine <path>] [--lister-artefacts]
  code 0 = perimetre sain, code 1 = ecritures suspectes hors perimetre.
"""

import sys
import argparse
import importlib.util
import os
import re
from datetime import datetime, timedelta
from pathlib import Path


# Dossiers techniques exclus (activite git/python, jamais ecritures Optimus).
EXCLUS_DIRS = {".git", "__pycache__"}
EXCLUS_EXT = {".pyc", ".pid"}

# La zone JETABLE du cameleon est une exception NOMMEE a ce perimetre : elle vit
# HORS de la Matrice (workspace/tmp-cameleon) parce que le cameleon CONSTRUIT
# dans workspace/ (regle R-005, MO-189). Son domicile se CITE -- il est declare
# une seule fois dans le moteur partage des zones (data/commun/zone_tmp.py).
_MATRICE = Path(__file__).resolve()
while _MATRICE.name != 'matrix' and _MATRICE.parent != _MATRICE:
    _MATRICE = _MATRICE.parent
sys.path.insert(0, str(_MATRICE / 'matrice' / 'data' / 'commun'))
from zone_tmp import est_dans_zone_cameleon  # noqa: E402
from artefacts_externes import artefact_de, date_de_naissance  # noqa: E402

# --- LA DECLARATION DE LA PORTE ECRIRE (son domicile, jamais une copie) --------
DOMICILE_PORTE_ECRIRE = (_MATRICE / "matrice" / "data" / "outils" / "ecrire"
                         / "constants.py")
CONSTANTE_ALLOWLIST_RACINE = "ALLOWLIST_RACINE"
CONSTANTE_ALLOWLIST_PREFIXES = "ALLOWLIST_PREFIXES"
CONSTANTE_MOTIF_BAK = "MOTIF_BAK_HORODATE"


def charger_declaration_porte(domicile=None):
    """(allowlist racine, prefixes, motif du point de restauration) LUS chez la porte.

    AUCUNE recopie (M-076) : la porte ECRIRE est l instrument qui decide ce qui peut
    etre ecrit hors de la Matrice, et c est ELLE qui produit la forme du point de
    restauration (commun.chemin_bak) -- nulle part ailleurs. Un consommateur qui
    redevine l une ou l autre derive en silence (L-100/L-102).

    REPLI DU COTE QUI ACCUSE : un domicile absent, illisible ou invalide rend
    (None, None, None). Le garde n accorde alors AUCUNE exemption racine et ne
    reconnait AUCUN filet -- il accuse davantage, et il le DIT. Une exemption qui
    echoue en silence serait exactement l angle mort que ce garde surveille.
    """
    domicile = Path(domicile or DOMICILE_PORTE_ECRIRE)
    if not domicile.is_file():
        return None, None, None
    dossier = str(domicile.parent)
    ajoute = dossier not in sys.path
    if ajoute:
        sys.path.insert(0, dossier)
    try:
        specification = importlib.util.spec_from_file_location(
            "domicile_porte_ecrire", str(domicile))
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except (ImportError, OSError, SyntaxError, AttributeError):
        return None, None, None
    finally:
        if ajoute and dossier in sys.path:
            sys.path.remove(dossier)
    allowlist = getattr(module, CONSTANTE_ALLOWLIST_RACINE, None)
    prefixes = getattr(module, CONSTANTE_ALLOWLIST_PREFIXES, None)
    motif_brut = getattr(module, CONSTANTE_MOTIF_BAK, None)
    if not isinstance(allowlist, (tuple, list)) or not isinstance(prefixes, (tuple, list)):
        return None, None, None
    motif = None
    if isinstance(motif_brut, str) and motif_brut:
        try:
            motif = re.compile(motif_brut)
        except re.error:
            motif = None
    return tuple(allowlist), tuple(prefixes), motif


def autorise_par_la_porte(nom, allowlist, prefixes):
    """Vrai si la PORTE peut ecrire ce nom de fichier a la RACINE du workspace."""
    return nom in allowlist or any(nom.startswith(prefixe) for prefixe in prefixes)


def est_filet_de_la_porte(nom, allowlist, prefixes, motif):
    """Vrai si le nom est la SAUVEGARDE d un fichier que la porte peut ecrire.

    Le nom de BASE compte autant que la forme : `demarrer-optimus-prime.md.bak.<date>`
    est le filet de la porte, tandis que `README.md.bak.<date>` serait la trace d une
    ecriture que la porte refuse -- la seconde s ACCUSE, la premiere se DIT.
    """
    if not motif:
        return False
    trouve = motif.search(nom)
    if trouve is None:
        return False
    return autorise_par_la_porte(nom[:trouve.start()], allowlist, prefixes)


def main():
    parser = argparse.ArgumentParser(description="Garde perimetre WRITE=matrix/")
    parser.add_argument("--jours", type=int, default=7, help="Fenetre de suspicion en jours (defaut: 7)")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    parser.add_argument("--lister-artefacts", action="store_true",
                        help="Liste aussi les fichiers des artefacts externes declares (exemption VISIBLE)")
    args = parser.parse_args()

    racine = Path(args.racine).resolve()
    # Perimetre = le dossier matrix/ : cerveau-projet/matrix prefere (sinon racine/matrix)
    # Priorite a cerveau-projet/matrix car c'est le vrai perimetre de la Matrice.
    candidats = [racine / "cerveau-projet" / "matrix", racine / "matrix"]
    if racine.name == "matrix":
        candidats.insert(0, racine)
    perimetre = next((c for c in candidats if c.is_dir()), None)
    if perimetre is None:
        print(f"Dossier matrix/ introuvable sous {racine}")
        return 2
    perimetre = perimetre.resolve()
    seuil = datetime.now() - timedelta(days=args.jours)
    suspects = []
    # EO-408 : les fichiers d un ARTEFACT EXTERIEUR declare sont comptes A PART. Ils
    # ne sont pas des ecritures de la v3 -- les melanger faisait rendre 4550 fichiers
    # non a la v3, et un rouge qui repartait tout seul a la disparition du worktree.
    artefacts = {}
    filets = []

    # LA DECLARATION DE LA PORTE EST LUE UNE FOIS, AVANT LE PARCOURS : sans elle, le
    # garde n accorderait aucune exemption de racine (et il le DIT plus bas).
    allowlist, prefixes, motif_bak = charger_declaration_porte()
    declaration_lue = allowlist is not None
    if not declaration_lue:
        allowlist, prefixes = (), ()

    # Elagage du PERIMETRE SEUL : le sous-arbre matrix/ est sain par definition, mais
    # la branche qui y mene (cerveau-projet/) est PARCOURUE -- c est le cerveau v1/v2,
    # et la regle qui interdit de l ecrire ne se garde que si on le regarde (MO-495).
    for dirpath, dirnames, filenames in os.walk(racine):
        # Elagage : ne jamais descendre dans les dossiers techniques
        dirnames[:] = [d for d in dirnames if d not in EXCLUS_DIRS]
        cur = Path(dirpath).resolve()
        try:
            cur.relative_to(perimetre)
            # cur est DANS le perimetre : tout son sous-arbre l est aussi
            dirnames.clear()
            continue
        except ValueError:
            pass
        # cur est un ANCETRE du perimetre (la RACINE, puis cerveau-projet/) : on retire
        # de la DESCENTE le seul dossier qui y mene, et on EXAMINE QUAND MEME les
        # fichiers de cur. L ancien `continue` sautait ce jugement : les fichiers de la
        # RACINE n etaient jamais vus (l allowlist racine etait du code mort, MO-495).
        for nom_dossier in list(dirnames):
            if (cur / nom_dossier).resolve() == perimetre:
                dirnames.remove(nom_dossier)
        for name in filenames:
            p = Path(dirpath) / name
            if not p.is_file():
                continue
            try:
                rel = p.relative_to(racine)
            except ValueError:
                continue
            # Dans le perimetre : sous matrix/ ou allowlist racine
            try:
                p.relative_to(perimetre)
                continue
            except ValueError:
                pass
            # ZONE DECLAREE du cameleon (R-005) : elle vit HORS de la Matrice,
            # donc elle serait suspecte ici a chaque mission du cameleon.
            # L exemption est NOMMEE (exemptions visibles, MO-075), jamais muette.
            if est_dans_zone_cameleon(p, racine):
                continue
            # LA DECLARATION DE LA PORTE ECRIRE (M-076), appliquee A LA RACINE SEULE :
            # la porte n autorise des noms hors Matrice que sans separateur de dossier
            # (son propre contrat) ; ailleurs, hors perimetre, rien n est autorise.
            if len(rel.parts) == 1:
                # LE FILET DE LA PORTE, JUGE AVANT L ALLOWLIST : sa sauvegarde se
                # reconnait a la FORME (lue chez la porte) ET a son nom de BASE
                # (autorise). Juge apres la liste, il serait epargne en SILENCE par
                # le prefixe `demarrer-` -- et une exemption muette se lit comme un
                # angle mort (MO-075). Ici il est NOMME, comme les artefacts.
                if est_filet_de_la_porte(p.name, allowlist, prefixes, motif_bak):
                    filets.append((str(rel), p.stat().st_mtime))
                    continue
                if autorise_par_la_porte(rel.parts[0], allowlist, prefixes):
                    continue
            # Bruit technique exclu (.pyc, .pid ; dossiers deja elagues au walk)
            if p.suffix in EXCLUS_EXT:
                continue
            # Hors perimetre : suspect si modifie dans la fenetre
            try:
                mtime = datetime.fromtimestamp(p.stat().st_mtime)
            except OSError:
                continue
            if mtime >= seuil:
                date = mtime.strftime("%Y-%m-%d %H:%M:%S")
                # La portee se MESURE avant de refuser (L-286) : le fichier tombe-t-il
                # dans un artefact EXTERIEUR declare ? Si oui, il est COMPTE, NOMME et
                # mis de cote ; sinon il est une violation a part entiere.
                artefact = artefact_de(p, racine)
                if artefact is not None:
                    artefacts.setdefault(str(artefact), []).append((str(rel), date))
                    continue
                suspects.append((str(rel), date))

    if not declaration_lue:
        print("DECLARATION DE LA PORTE ILLISIBLE (" + str(DOMICILE_PORTE_ECRIRE)
              + ") : aucune exemption racine n est accordee -- le garde accuse du cote"
              " qui accuse (M-076).")
    # L'ARTEFACT EXTERIEUR EST NOMME AVANT LE VERDICT : un perimetre qui met de cote
    # doit DIRE ce qu'il met de cote (exemptions visibles, MO-075), COMBIEN de
    # fichiers, et de QUAND date l'artefact -- il est nommable : chemin, naissance.
    total_artefacts = 0
    if artefacts:
        print("ARTEFACT(S) EXTERNE(S) declare(s) -- hors de la v3, comptes A PART :")
        for chemin, fichiers in sorted(artefacts.items()):
            total_artefacts += len(fichiers)
            naissance = date_de_naissance(chemin)
            print("  - " + chemin + " | " + str(len(fichiers)) + " fichier(s) | ne le "
                  + (naissance if naissance else "date ILLISIBLE"))
            if args.lister_artefacts:
                for rel, date in sorted(fichiers):
                    print("      " + rel + " (" + date + ")")

    # LE FILET DE LA PORTE EST NOMME AVANT LE VERDICT, lui aussi : c est une exemption
    # VISIBLE (MO-075) -- la sauvegarde que la porte cree elle-meme n est pas une
    # ecriture d agent, et le lecteur doit pouvoir le verifier.
    if filets:
        print("FILET(S) DE LA PORTE ECRIRE (point de restauration de la porte, pas une"
              " ecriture d agent) :")
        for rel, horodatage in sorted(filets):
            stamp = datetime.fromtimestamp(horodatage).strftime("%Y-%m-%d %H:%M:%S")
            print("  - " + rel + " (" + stamp + ")")

    if suspects:
        complement = ("" if not total_artefacts else
                      " (hors " + str(total_artefacts) + " fichier(s) d'artefact(s) externe(s) declare(s))")
        print(f"PERIMETRE VIOLE : {len(suspects)} fichier(s) hors matrix/ modifies"
              f" (fenetre {args.jours}j){complement} :")
        for rel, date in sorted(suspects):
            print(f"  - {rel} ({date})")
        # MO-463 : le createur a tranche (2026-09-27) -- le dossier .freebuff/
        # N A PAS LIEU D ETRE. Le garde ne l EXEME PAS (aucune exemption muette) :
        # il accuse et NOMME le remede -- un rouge qui ne dirait pas comment obeir
        # resterait muet. Le nettoyage a l OUVERTURE de session vit en ORDRE 0 BIS
        # des fichiers demarrer-optimus-prime.md / demarrer-cameleon.md.
        if any(Path(r).parts[:1] == (".freebuff",) for r, _ in suspects):
            print("  DECISION CREATEUR (MO-463, 2026-09-27) : .freebuff/ N A PAS LIEU D ETRE.")
            print("    REMEDE (et non exemption) : supprimer le dossier -- il est reecrit par le")
            print("    harnais du client a chaque ouverture, et nettoye en ORDRE 0 BIS")
            print("    (demarrer-optimus-prime.md / demarrer-cameleon.md).")
        return 1

    complement = ""
    if total_artefacts:
        complement = (f" ; {total_artefacts} fichier(s) d'artefact(s) externe(s) declare(s)"
                      f" mis de cote et NOMMES ci-dessus")
    if filets:
        complement += (f" ; {len(filets)} filet(s) de la porte ECRIRE reconnu(s) et"
                       f" NOMME(s) ci-dessus")
    print(f"Perimetre sain : aucune ecriture de la V3 hors matrix/ (fenetre {args.jours}j)"
          f"{complement}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
