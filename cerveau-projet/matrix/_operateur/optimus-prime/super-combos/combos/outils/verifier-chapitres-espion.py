#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-chapitres-espion.py -- Garde : les chapitres ANNONCES sont ceux PRODUITS

Pourquoi (2026-09-13, MO-072 / EO-102) : la passe de `espion-integrite` annoncait
`"chapitres": [1, 2]` ECRIT EN DUR, alors que le chapitre 2 (presence) ne peut
produire une ligne que pour une BDD marquee a-construire au registre -- et le
registre n'avait plus que des True depuis le 2026-09-06 (mesure : 81 lignes
chapitre 2 sur 504 008 observations, la derniere le 2026-09-06 16:22:16). Un canal
DECLARE mais structurellement vide fait croire a une surveillance qui n'existe
pas : c'est pire que pas de canal, car le lecteur du journal compte dessus.

Ce garde exige que l'annonce soit CALCULEE du registre (fonction
`chapitres_produits`), et que l'annonce soit EGALE a ce que la passe produit
reellement. Il s'AUTOTESTE en rejouant l'ancienne annonce STATIQUE : si la
reparation etait annulee, le garde doit la refuser.

CE QU'IL NE FAIT PAS : il n'ecrit JAMAIS dans le journal reel de la routine (la
sortie est redirigee vers un fichier temporaire du garde), ne touche ni le
registre ni l'etat, et n'execute aucun depot.

Usage: python verifier-chapitres-espion.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = racine introuvable.
"""

import argparse
import json
import sys
import tempfile
from pathlib import Path

# --- REFERENCES (aucune valeur en dur ailleurs que dans cette table) ---------
ROUTINE = "espion-integrite"
CHAPITRE_INTEGRITE = 1
CHAPITRE_PRESENCE = 2
# L'annonce STATIQUE d'avant la reparation : c'est ELLE que le garde doit
# accuser si elle revenait (auto-test, lecon L-032 : un controle qu'on ne peut
# pas pieger ne prouve rien).
ANCIENNE_ANNONCE = [CHAPITRE_INTEGRITE, CHAPITRE_PRESENCE]

RESULTATS = []


def trouver_matrix(racine):
    """Retourne le dossier matrix/, ou None."""
    candidats = [racine / "cerveau-projet" / "matrix", racine / "matrix"]
    if racine.name == "matrix":
        candidats.insert(0, racine)
    for candidat in candidats:
        if (candidat / "matrice").is_dir():
            return candidat
    return None


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)


def passer(tour_entry, commun, registre, journal_tmp, etat_tmp):
    """Fait UNE passe COMPLETE sur un registre donne, journal et ETAT rediriges.

    Depuis MO-081 les observations ne sont journalisees que si le TABLEAU DES BDD
    change : une passe dont l'etat de controle est INCONNU est donc une passe
    complete (le tableau part a la premiere passe). Chaque passe du cobaye repart
    d'un ETAT NEUF -- sinon la 2e passe d'un meme registre serait absorbee, et ce
    garde mesurerait une production vide au lieu de l'annonce (il deviendrait
    aveugle a ce qu'il surveille). L'etat du SERVICE n'est jamais touche.
    """
    ancien_journal = commun.CHEMIN_JOURNAL
    ancien_etat = commun.CHEMIN_ETAT_BDDS
    ancien_registre = tour_entry.BDDS
    commun.CHEMIN_JOURNAL = journal_tmp
    commun.CHEMIN_ETAT_BDDS = etat_tmp
    tour_entry.BDDS = dict(registre)
    try:
        journal_tmp.write_text("", encoding="utf-8")
        if etat_tmp.exists():
            etat_tmp.unlink()
        code = tour_entry.executer([])
    finally:
        commun.CHEMIN_JOURNAL = ancien_journal
        commun.CHEMIN_ETAT_BDDS = ancien_etat
        tour_entry.BDDS = ancien_registre
    lignes = []
    for brute in journal_tmp.read_text(encoding="utf-8").splitlines():
        brute = brute.strip()
        if brute:
            lignes.append(json.loads(brute))
    return code, lignes


def annonces(lignes):
    """Les chapitres portes par l'evenement `passe` (l'ANNONCE)."""
    for ligne in lignes:
        if ligne.get("type") == "passe":
            return ligne.get("chapitres")
    return None


def produits(lignes):
    """Les chapitres REELLEMENT journalises par les observations."""
    return sorted({l.get("chapitre") for l in lignes if "chapitre" in l})


def attendus(bdds):
    """L'annonce HONNETE d'un registre : chaque chapitre, s'il est produisible."""
    chapitres = []
    if any(bool(f) for f in bdds.values()):
        chapitres.append(CHAPITRE_INTEGRITE)
    if any(not bool(f) for f in bdds.values()):
        chapitres.append(CHAPITRE_PRESENCE)
    return chapitres


def main():
    parser = argparse.ArgumentParser(description="Garde : chapitres annonces == chapitres produits")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = parser.parse_args()

    matrix = trouver_matrix(Path(arguments.racine).resolve())
    if matrix is None:
        print("Dossier matrix/ introuvable sous " + str(arguments.racine))
        return 2
    dossier = matrix / "matrice" / "routines" / ROUTINE
    if not dossier.is_dir():
        print("Routine introuvable : " + str(dossier))
        return 2

    print("VERIFIER CHAPITRES ESPION -- l'annonce est celle qui est produite")

    sys.path.insert(0, str(dossier))
    try:
        import constants as constantes
        import commun
        from tour import entry as tour_entry
    except Exception as erreur:  # noqa: BLE001 -- on AVOUE l'echec, on ne plante pas
        print("ECART : routine illisible (" + ROUTINE + ") : " + str(erreur))
        return 1

    # 0. L'annonce est CALCULEE du registre (une fonction), pas ecrite en dur.
    calcul = getattr(tour_entry, "chapitres_produits", None)
    controler("annonce-calculee", callable(calcul),
              "chapitres_produits presente" if callable(calcul) else "chapitres_produits ABSENTE")
    if not callable(calcul):
        return 1

    registre_reel = dict(constantes.BDDS)
    temporaire = Path(tempfile.mkdtemp(prefix="garde-chapitres-"))
    journal_tmp = temporaire / "journal.jsonl"
    etat_tmp = temporaire / "etat-bdds.json"
    ecarts = []
    try:
        # 1. Registre REEL : annonce calculee == ce que la passe produit.
        annonce = calcul(registre_reel)
        _, lignes = passer(tour_entry, commun, registre_reel, journal_tmp, etat_tmp)
        annonce_passe = annonces(lignes)
        produits_reels = produits(lignes)
        controler(
            "reel-annonce",
            annonce == annonce_passe == attendus(registre_reel),
            "calcule=" + str(annonce) + " passe=" + str(annonce_passe)
            + " attendu=" + str(attendus(registre_reel)),
        )
        if annonce != annonce_passe:
            ecarts.append("l'annonce de la passe differe de l'annonce calculee")
        controler(
            "reel-production",
            set(produits_reels).issubset(set(annonce)) and set(annonce).issubset(set(produits_reels)),
            "produits=" + str(produits_reels) + " annonces=" + str(annonce),
        )
        if not set(produits_reels).issubset(set(annonce)):
            ecarts.append("un chapitre journalise n'est pas annonce : " + str(produits_reels))

        # 2. AUTOTEST : l'ancienne annonce STATIQUE doit etre ACCUSEE.
        #    Rejouee sur le registre reel, elle annonce un chapitre que la passe
        #    ne peut pas produire -- le garde doit s'en plaindre (lecon L-032).
        controler(
            "autotest-statique",
            ANCIENNE_ANNONCE != attendus(registre_reel)
            and ANCIENNE_ANNONCE != produits_reels,
            "ancienne=" + str(ANCIENNE_ANNONCE) + " produite=" + str(produits_reels),
        )
        if ANCIENNE_ANNONCE == produits_reels:
            ecarts.append("le garde ne saurait pas accuser l'ancienne annonce statique")

        # 3. Une BDD a-construire RALLUME le chapitre 2 (et il est annonce).
        registre_avenir = dict(registre_reel)
        registre_avenir["bdd-en-construction.json"] = False
        annonce_avenir = calcul(registre_avenir)
        code_avenir, lignes_avenir = passer(tour_entry, commun, registre_avenir, journal_tmp, etat_tmp)
        chap2 = [l for l in lignes_avenir if l.get("chapitre") == CHAPITRE_PRESENCE]
        controler(
            "a-construire-rallume",
            annonce_avenir == attendus(registre_avenir) == ANCIENNE_ANNONCE
            and annonces(lignes_avenir) == ANCIENNE_ANNONCE
            and len(chap2) >= 1
            and all(l.get("bdd") == "bdd-en-construction.json" for l in chap2)
            and code_avenir == 0,
            "annonce=" + str(annonces(lignes_avenir)) + " lignes chapitre 2=" + str(len(chap2)),
        )
        if len(chap2) < 1:
            ecarts.append("une BDD a-construire n'allume pas le chapitre 2")

        # 4. Registre ENTIEREMENT a-construire : le chapitre 1 n'est pas annonce
        #    (aucune BDD faite a verifier) -- l'annonce reste honnete.
        registre_vierge = {nom: False for nom in registre_reel}
        annonce_vierge = calcul(registre_vierge)
        _, lignes_vierges = passer(tour_entry, commun, registre_vierge, journal_tmp, etat_tmp)
        produits_vierges = produits(lignes_vierges)
        controler(
            "registre-vierge",
            annonce_vierge == [CHAPITRE_PRESENCE]
            and set(produits_vierges).issubset(set(annonce_vierge)),
            "annonce=" + str(annonce_vierge) + " produits=" + str(produits_vierges),
        )
        if annonce_vierge != [CHAPITRE_PRESENCE]:
            ecarts.append("un registre entierement a-construire annonce mal ses chapitres")
    finally:
        for reste in temporaire.glob("*"):
            reste.unlink()
        temporaire.rmdir()

    for ecart in ecarts:
        print("ECART : " + ecart)
    echecs = [nom for nom, ok, _ in RESULTATS if not ok]
    if ecarts or echecs:
        print("")
        print("VERDICT KO : l'annonce des chapitres n'est plus celle qui est produite.")
        return 1
    print("")
    print("VERDICT OK : les chapitres annonces sont ceux qui sont produits.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
