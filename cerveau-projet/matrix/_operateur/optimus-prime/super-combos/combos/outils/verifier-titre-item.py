#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier-titre-item.py -- Garde : le TITRE d'un item n'est pas une ETIQUETTE.

POURQUOI (mesure 2026-09-23) : sur les 29 items de l'entonnoir d'Optimus, DEUX
portaient un NOM DU VIVIER dans `theme` -- le TITRE de la demande. La file
affichait donc `OUTIL` la ou on attend une phrase. Les deux items ont ete RE-TITRES
par le verbe `corriger` (identifiant conserve, correction tracee), et les DEUX
portes de depot refusent desormais un `--theme` qui est un nom du vivier.

LES DEUX ARBRES SONT JUGES PAR LE MEME GARDE, mais chacun par SON garde local (un
seul domicile cote code : `titre.py` pour la Matrice, `roles.py` pour l'operateur --
les deux entonnoirs sont deux arbres, heritage v1/v2) :
  - Matrice   : matrice/pilote/entonnoir/                    (famille E-)
  - operateur : _operateur/optimus-prime/pilote/entonnoir/   (famille EO-)

CE QU'IL VERIFIE :
  1. PASSIF : aucun item des deux entonnoirs ne porte une etiquette du vivier dans
     son `theme` -- la lecture du vivier passe par le GARDE DE CHAQUE ARBRE (sa
     porte, M-042), JAMAIS par une liste recopiee ici ;
  2. ACTIF : les DEUX portes de depot REFUSENT ce theme (code 2) en nommant le bon
     geste, et l'item NE NAIT PAS (compteur d'items inchange). Si une porte
     l'acceptait, ce cobaye RETIRE l'item ne et le DIT : jamais de residu muet ;
  3. AUTO-TEST : le detecteur est VU mordre (L-032/L-060) sur un theme fabrique, et
     passer sur un titre libre -- sur les DEUX arbres.

CE QU'IL NE FAIT PAS : il n'ecrit jamais dans un entonnoir (sauf pour RETIRER un
item qu'une porte fautive aurait laisse naitre).

Usage : python verifier-titre-item.py [--racine <path>] [--auto-test]
  code 0 = sain, 1 = ecart (nomme), 2 = racine introuvable.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-414, vague 3 du lot) -----------------
# Cet outil lancait a nu. Le motif est LU au domicile de la Matrice ; la racine se
# DETECTE par marqueur (MO-088 : aucun parents[N] nu) et on REFUSE plutot que de
# deviner (garde-foi L-006).
RACINE_MATRICE_LANCEMENT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
if RACINE_MATRICE_LANCEMENT.name != "matrix":
    raise RuntimeError("Structure inattendue : " + str(RACINE_MATRICE_LANCEMENT)
                       + " n est pas la racine `matrix` (garde-foi L-006)")
REPERTOIRE_COMMUN_LANCEMENT = RACINE_MATRICE_LANCEMENT / "matrice" / "data" / "commun"
if not (REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())
import sys
from pathlib import Path

BORNES_REMONTEE = 30
MARQUEUR_MATRICE = Path("matrice") / "data" / "commun" / "racine.py"
DELAI = 180
NOM_LANCEUR = "lancer.py"
DICTIONNAIRE_VIVIER = Path("matrice") / "data" / "vivier-themes.json"
TITRE_LIBRE = "Verifier que la file affiche un titre"

# (etiquette, dossier de l'entonnoir, module de SON garde, fichier d'etat des items)
ENTONNOIRS = (
    ("matrice", Path("matrice") / "pilote" / "entonnoir", "titre", "entonnoir-files.json"),
    ("operateur", Path("_operateur") / "optimus-prime" / "pilote" / "entonnoir",
     "roles", "entonnoir-files-optimus.json"),
)

RESULTATS = []


def trouver_racine(depart):
    """Le dossier qui PORTE la Matrice, ou None (meme resolution que le garde des cartes).

    La racine donnee peut etre le dossier qui contient `< cerveau-projet/matrix >`,
    le dossier `< matrix >` lui-meme, ou la Matrice : les trois se resolvent, et un
    marqueur introuvable se DIT (jamais un chemin suppose).
    """
    base = Path(depart).resolve()
    if base.name == "matrix":
        candidats = [base]
    else:
        candidats = [base / "cerveau-projet" / "matrix", base / "matrix", base]
    for candidat in candidats:
        for courant in [candidat] + list(candidat.parents):
            if (courant / MARQUEUR_MATRICE).is_file():
                return courant
    return None


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def lire_json(chemin):
    try:
        return json.loads(chemin.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def items_de(etat):
    """Tous les items d'un entonnoir (vrac + files), ou liste vide."""
    if not isinstance(etat, dict):
        return []
    items = list(etat.get("vrac", []))
    files = etat.get("files", {})
    if isinstance(files, dict):
        for missions in files.values():
            if isinstance(missions, list):
                items.extend(missions)
    return items


def nom_du_vivier(racine):
    """Un nom REELLEMENT present au vivier partage (aucune valeur en dur)."""
    donnees = lire_json(racine / DICTIONNAIRE_VIVIER)
    if not isinstance(donnees, dict):
        return ""
    for theme in donnees.get("themes", []):
        nom = str(theme.get("nom", "")).strip()
        if nom:
            return nom
    return ""


def garde_local(racine, dossier, module, themes):
    """Interroge le GARDE DE CET ARBRE (sa porte) sur des textes donnes.

    Le garde vit dans l'arbre juge : on l'importe comme le fait sa porte (son
    dossier en tete), jamais une seconde lecture du vivier ici (M-042).
    """
    lignes = [
        "import json, sys",
        "sys.path.insert(0, " + repr(str(racine / dossier)) + ")",
        "import " + module + " as garde",
        "print(json.dumps({t: bool(garde.est_theme_du_vivier(t)) for t in "
        + repr(list(themes)) + "}))",
    ]
    fini = lancer_enfant([sys.executable, "-c", "\n".join(lignes)],
                          capture_output=True, text=True, timeout=DELAI)
    if fini.returncode != 0:
        return None, (fini.stdout + fini.stderr).strip()[-200:]
    for ligne in reversed((fini.stdout or "").strip().splitlines()):
        try:
            return json.loads(ligne), ""
        except ValueError:
            continue
    return None, "aucune reponse JSON du garde"


def ids_de(chemin_etat):
    """Les identifiants des items d'un entonnoir -- lus dans SON etat, jamais
    parses dans une sortie texte : le format d'un identifiant n'a pas a etre
    recopie ici (chaque arbre a le sien, cf. `listes.PREFIXE_ITEM`)."""
    return {str(item.get("id", "")) for item in items_de(lire_json(chemin_etat)) if item.get("id")}


def controler_poser(racine, etiquette, dossier, module, chemin_etat, vivier):
    """ACTIF : la porte de depot REFUSE une etiquette -- et l'item ne nait pas."""
    avant = ids_de(chemin_etat)
    cible = racine / dossier / "main.py"
    fini = lancer_enfant(
        [sys.executable, str(racine / NOM_LANCEUR), str(cible), "deposer",
         "--theme", vivier, "--objectif", "SONDE DU GARDE : cet item ne doit pas naitre"],
        capture_output=True, text=True, cwd=str(racine), timeout=DELAI)
    sortie = (fini.stdout or "") + (fini.stderr or "")
    refuse = fini.returncode == 2 and "REFUS" in sortie and "THEME DU VIVIER" in sortie
    nes = sorted(ids_de(chemin_etat) - avant)
    detail = ("porte " + etiquette + " : code " + str(fini.returncode)
              + ", refus " + ("nomme" if refuse else "ABSENT"))
    if nes:
        # Une porte fautive a laisse naitre l'item : on le RETIRE et on le DIT.
        for nait in nes:
            lancer_enfant([sys.executable, str(racine / NOM_LANCEUR), str(cible),
                            "retirer", "--id", nait],
                           capture_output=True, text=True, cwd=str(racine),
                           timeout=DELAI)
            detail += " | item ne RETIRE : " + nait
    if not nes:
        detail += " | items " + str(len(avant))
    return controler("porte-" + etiquette + "-refuse-l-etiquette", refuse and not nes, detail)


def controler_autotest(racine, vivier):
    """Le detecteur est VU mordre et passer, sur les DEUX arbres (L-032/L-060)."""
    epreuves = []
    for etiquette, dossier, module, _ in ENTONNOIRS:
        avis, erreur = garde_local(racine, dossier, module, (vivier, TITRE_LIBRE))
        if avis is None:
            epreuves.append((etiquette + " : garde joignable", False, erreur))
            continue
        epreuves.append((etiquette + " : etiquette MORD", avis.get(vivier) is True, vivier))
        epreuves.append((etiquette + " : titre libre PASSE",
                         avis.get(TITRE_LIBRE) is False, TITRE_LIBRE))
    for nom, ok, detail in epreuves:
        print("[--] cobaye " + ("ACCEPTE" if ok else "NON REPERE") + " : " + nom + " (" + detail + ")")
    reussies = sum(1 for _, ok, _ in epreuves if ok)
    return reussies == len(epreuves), reussies, len(epreuves)


def main():
    parser = argparse.ArgumentParser(description="Garde : le titre d'un item n'est pas une etiquette")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    parser.add_argument("--auto-test", action="store_true", help="Rejoue les cobayes")
    arguments = parser.parse_args()

    racine = trouver_racine(Path(arguments.racine))
    if racine is None:
        print("Marqueur " + str(MARQUEUR_MATRICE) + " introuvable sous " + str(arguments.racine))
        return 2
    vivier = nom_du_vivier(racine)
    if not vivier:
        print("ECART : vivier partage illisible ou vide (" + str(racine / DICTIONNAIRE_VIVIER)
              + ") -- le garde ne peut pas nommer une etiquette sans lui (a reparer).")
        return 1

    ecarts = []
    for etiquette, dossier, module, nom_etat in ENTONNOIRS:
        chemin_etat = racine / dossier.parent / nom_etat
        items = items_de(lire_json(chemin_etat))
        etiquettes = [str(m.get("theme", "")) for m in items]
        avis, erreur = garde_local(racine, dossier, module, etiquettes) if etiquettes else ({}, "")
        coupes = sorted(mid for mid, m in zip([m.get("id") for m in items], etiquettes)
                        if avis.get(m))
        controler("items-" + etiquette + "-sans-etiquette", not coupes,
                  (str(len(items)) + " item(s), aucun ne porte une etiquette du vivier")
                  if not coupes else "ETIQUETTE EN GUISE DE TITRE : " + ", ".join(coupes[:8]))
        if coupes:
            ecarts.append("items " + etiquette + " a re-titrer : " + ", ".join(coupes))
        if erreur:
            ecarts.append("garde " + etiquette + " muet : " + erreur)
        if not controler_poser(racine, etiquette, dossier, module, chemin_etat, vivier):
            ecarts.append("porte " + etiquette + " : l'etiquette n'est pas refusee")

    # L'AUTO-TEST juge les DEUX arbres d'un coup : UNE fois, jamais une par
    # entonnoir (defaut vu a l'usage : appele dans la boucle, il imprimait huit
    # cobayes pour quatre epreuves -- un cobaye bruyant se lit mal).
    if arguments.auto_test:
        ok, reussies, total = controler_autotest(racine, vivier)
        if not ok:
            ecarts.append("autotest : " + str(reussies) + "/" + str(total))

    print("VERIFIER TITRE D'ITEM -- un titre n'est pas un mot du vivier")
    if ecarts:
        print("\nVERDICT KO : " + " ; ".join(ecarts))
        return 1
    print("\nVERDICT OK : le titre des items est un titre, et les deux portes le tiennent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
