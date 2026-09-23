#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-profil-injection.py -- Garde : le profil utilisateur est INJECTE, et BORNE.

Pourquoi (demande createur du 2026-09-21) : la fiche `matrix/USER-PROFIL.md` est
remplie AVEC le createur (pseudo, style, interets, niveau technique...) mais AUCUN
agent ne la lisait. Mesure du jour : le pilote ne l'ouvrait qu'au DEMARRAGE
(`injection/cycle.py`), pour tester si la ligne `**Pseudo**` etait remplie, puis
jetait le contenu -- les 8 champs n'atteignaient donc aucune mission, alors que la
fiche annonce elle-meme etre lue par Optimus.

CE QU'IL EXIGE :
  1. UN SEUL DOMICILE : les champs ATTENDUS et la lecture des valeurs vivent dans
     le module PARTAGE (data/commun/fiche_profil.py) -- deux copies divergeraient,
     et l'une des deux pointerait un fichier mythique (c'est arrive : MO-043).
  2. CHAMP PESE : `profil` appartient a CHAMPS_PESES -- un champ livre sans poids
     est du contexte en franchise (le defaut exact de MO-314, modes d emploi).
  3. DEUX CHEMINS : l'injection SIMPLE et l'injection de LOT portent le profil --
     deux copies d'un mecanisme = un chemin protege et l'autre non.
  4. RIEN DANS L'OMBRE : chaque champ ATTENDU est SOIT injecte, SOIT dit
     (`a_remplir`), SOIT dit ecarte (`ecartes_par_plafond`). Un champ qui
     disparaitrait sans le dire est le vrai risque d'un ecretage silencieux.
  5. BORNE REELLE : sur une fiche OBESE, le bloc est ECRETE et les champs ecartes
     sont DITS ; sous un plafond enorme, le MEME cobaye passe ENTIER -- preuve que
     l'ecretage vient du plafond, et de rien d'autre.
  6. AUCUN SILENCE : fiche absente ou illisible -> un AVERTISSEMENT NOMME dans le
     bloc (un bloc vide se lirait comme "profil complet").

L'AUTOTEST le PIEGE (lecon L-032) : le cobaye obese est ecrete, le meme cobaye
passe entier sous un plafond enorme, et le premier champ passe toujours seul sous
un plafond minuscule -- un detecteur jamais vu crier ne prouve rien.

CE QU'IL NE FAIT PAS : AUCUNE ecriture dans la zone reelle. Le seul fichier qu'il
cree est son cobaye, dans la zone JETABLE de son flux (declaree au domicile
partage `data/commun/zone_tmp.py`), et il le supprime dans tous les cas. Il ne
lance aucune mission et ne touche aucune porte.

Usage: python verifier-profil-injection.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = zone introuvable.
"""

import argparse
import sys
from pathlib import Path

# Les domiciles : declares UNE fois, jamais recopies dans la logique.
FICHIER_MOTIF = Path("matrice") / "data" / "commun" / "fiche_profil.py"
FICHIER_COMMUN = Path("matrice") / "data" / "commun"
FICHIER_INJECTION = (Path("_operateur") / "optimus-prime" / "pilote"
                     / "injection" / "fonctions.py")

# Le marqueur du champ dans l'injection : le texte EXACT que la logique ecrit.
# DEUX chemins (mission simple + lot) : c'est le trou qu'on ferme.
MARQUEUR_CHAMP = "CHAMP_PROFIL: charger_profil_utile(),"
CHEMINS_ATTENDUS = 2
# La declaration des champs ATTENDUS : UNE seule (le motif partage).
MARQUEUR_MOTIF = "CHAMPS_ATTENDUS = ("
DOMICILES_ATTENDUS = 1
# Zones jetables et caches : hors champ -- un cobaye pose un exemplaire du motif
# pour l'eprouver, et le compter comme une COPIE rendrait le garde fou (meme
# regle que verifier-recherche, L-029).
PREFIXE_ZONE_JETABLE = "tmp-"
DOSSIERS_IGNORES = ("__pycache__",)

# Le cobaye : une fiche OBESE (un champ colle de 4000 caracteres) et deux plafonds
# extremes -- c'est la seule facon de voir l'ecretage a l'oeuvre sans jamais
# toucher la fiche du createur.
VALEUR_OBESE = "x" * 4000
PLAFOND_ENORME = 10 ** 6
PLAFOND_MINUSCULE = 1
NOM_COBAYE = "profil-cobaye.md"

RESULTATS = []


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def trouver_racine(racine):
    """Retourne le dossier matrix/ (celui qui porte `matrice` et `_operateur`), ou None."""
    candidats = [
        racine,
        racine / "cerveau-projet" / "matrix",
        racine / "matrix",
    ]
    for candidat in candidats:
        if (candidat / FICHIER_MOTIF).is_file():
            return candidat
    return None


def charger_pilote(racine):
    """Importe la porte d'injection du pilote. -> (module, erreur)."""
    pilote = str(racine / "_operateur" / "optimus-prime" / "pilote")
    if pilote not in sys.path:
        sys.path.insert(0, pilote)
    try:
        import injection.fonctions as fonctions
    except Exception as erreur:  # un module qui ne se charge pas est DEJA un ecart
        return None, repr(erreur)
    return fonctions, None


def charger_zone(racine):
    """Le chemin de la zone jetable du flux, LU au domicile partage. -> (chemin, erreur)."""
    commun = str(racine / FICHIER_COMMUN)
    if commun not in sys.path:
        sys.path.insert(0, commun)
    try:
        from zone_tmp import chemin_zone_optimus
    except Exception as erreur:
        return None, repr(erreur)
    return chemin_zone_optimus(racine), None


def est_en_champ(chemin, racine):
    """Vrai si le fichier est du CODE de la zone (hors garde, zones jetables, caches)."""
    try:
        parties = chemin.relative_to(racine).parts
    except ValueError:
        return False
    if parties[-1] == Path(__file__).name:
        return False
    for partie in parties[:-1]:
        if partie in DOSSIERS_IGNORES or partie.startswith(PREFIXE_ZONE_JETABLE):
            return False
    return True


def fabriquer_cobaye(zone, motif):
    """Une fiche de cobaye OBESE, batie avec le FORMAT DECLARE par le motif.

    La ligne de tableau n'est pas inventee ici : elle est COMPOSEE avec les
    constantes du motif (separateur, rang des colonnes) -- recopier le format
    ferait un second domicile, et le cobaye passerait le jour ou la fiche change
    de forme. Le champ obese est le DERNIER declare : c'est le cas reel (une
    valeur longue ajoutee a la fin) et il laisse les autres champs passer.
    """
    lignes = []
    dernier = motif.CHAMPS_ATTENDUS[-1]
    for libelle in motif.CHAMPS_ATTENDUS:
        valeur = VALEUR_OBESE if libelle == dernier else "valeur de " + libelle
        colonnes = [""] * (motif.COLONNES_MINIMUM + 1)
        colonnes[motif.COLONNE_LIBELLE] = " **" + libelle + "** "
        colonnes[motif.COLONNE_VALEUR] = " " + valeur + " "
        colonnes[motif.COLONNE_STATUT] = " Rempli "
        lignes.append(motif.SEPARATEUR_TABLEAU.join(colonnes))
    chemin = zone / NOM_COBAYE
    chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8", newline="\n")
    return chemin, dernier


def couverture(bloc, attendus):
    """Les champs ATTENDUS qui ne sont NI injectes, NI dits, NI ecartes (detecteur PUR)."""
    couverts = set(bloc.get("champs", {}))
    couverts |= set(bloc.get("a_remplir", []))
    couverts |= set(bloc.get("ecartes_par_plafond", []))
    return sorted(set(attendus) - couverts)


def verifier_domicile(racine):
    """1. UN SEUL DOMICILE : les champs attendus ne sont declares qu'une fois."""
    domiciles = [chemin for chemin in racine.rglob("*.py")
                 if est_en_champ(chemin, racine)
                 and MARQUEUR_MOTIF in chemin.read_text(encoding="utf-8", errors="replace")]
    detail = (str(len(domiciles)) + " fichier(s) declarent les champs attendus (attendu : "
              + str(DOMICILES_ATTENDUS) + ")")
    if len(domiciles) != DOMICILES_ATTENDUS:
        detail = "COPIES : " + ", ".join(str(c) for c in domiciles)
    if controler("domicile-unique", len(domiciles) == DOMICILES_ATTENDUS, detail):
        return []
    return ["champs attendus declares dans " + str(len(domiciles)) + " fichier(s)"]


def verifier_champ_pese(fonctions):
    """2. CHAMP PESE : un champ livre sans poids est du contexte en franchise."""
    champ = getattr(fonctions, "CHAMP_PROFIL", "")
    pese = bool(champ) and champ in getattr(fonctions, "CHAMPS_PESES", ())
    detail = ("`" + str(champ) + "` est pese avec le sac-a-dos" if pese
              else "`" + str(champ) + "` MANQUE de CHAMPS_PESES")
    if controler("champ-pese", pese, detail):
        return []
    return ["le champ du profil n'est pas pese"]


def verifier_deux_chemins(racine):
    """3. DEUX CHEMINS : l'injection SIMPLE et celle du LOT portent le profil."""
    source = (racine / FICHIER_INJECTION).read_text(encoding="utf-8", errors="replace")
    occurrences = source.count(MARQUEUR_CHAMP)
    detail = (str(occurrences) + " chemin(s) d'injection portent le profil"
              if occurrences >= CHEMINS_ATTENDUS
              else "SEULEMENT " + str(occurrences) + " sur " + str(CHEMINS_ATTENDUS)
              + " -- un chemin sans profil est une mission ou l'agent improvise")
    if controler("deux-chemins", occurrences >= CHEMINS_ATTENDUS, detail):
        return []
    return ["chemins d'injection sans profil : " + str(occurrences) + "/" + str(CHEMINS_ATTENDUS)]


def verifier_plafond(fonctions):
    """4. PLAFOND DECLARE : le plafond vit chez le proprietaire du contrat."""
    plafond = getattr(fonctions, "PLAFOND_PROFIL_TOKENS", None)
    declare = isinstance(plafond, int) and plafond > 0
    detail = (("plafond " + str(plafond) + " tokens") if declare
              else "PLAFOND absent ou nul dans les constantes du pilote")
    if controler("plafond-declare", declare, detail):
        return [], plafond
    return ["plafond du profil absent ou nul"], plafond


def verifier_fiche(fonctions, motif):
    """5. LA FICHE REELLE : injectee, et RIEN dans l'ombre (chaque champ a un etat)."""
    ecarts = []
    bloc = fonctions.charger_profil_utile()
    injecte = bool(bloc.get("present")) and bool(bloc.get("champs"))
    detail = ("AUCUN profil injecte -- " + str(bloc.get("avertissement", "raison non dite")))
    if injecte:
        detail = (str(len(bloc.get("champs", {}))) + " champ(s) injectes sur "
                  + str(len(motif.CHAMPS_ATTENDUS)) + " attendus (complet : "
                  + str(bool(bloc.get("complet"))) + ")")
    if not controler("fiche-reelle", injecte, detail):
        ecarts.append("le profil reel n'est pas injecte")
    manquants = couverture(bloc, motif.CHAMPS_ATTENDUS)
    if not controler("rien-dans-l-ombre", not manquants,
                     "chaque champ attendu est injecte, dit ou ecarte" if not manquants
                     else "CHAMPS SILENCIEUX : " + ", ".join(manquants)):
        ecarts.append("champs attendus sans etat (ni injecte, ni dit)")
    return ecarts


def verifier_borne(zone, fonctions, motif, plafond):
    """6, 7, 8. Le COBAYE : la borne MORD et elle le DIT, rien ne se tait.

    Le cobaye vit dans la zone JETABLE de son flux et il est supprime dans TOUS
    les cas (finally) : la zone doit rester vide, sinon la non-regression
    laisserait derriere elle exactement ce que la regle perimetre-tmp interdit.
    """
    ecarts = []
    epreuves = []
    cobaye = None
    try:
        zone.mkdir(exist_ok=True)
        cobaye, obese = fabriquer_cobaye(zone, motif)

        bloc_obese = fonctions.charger_profil_utile(chemin=cobaye)
        ecartes = bloc_obese.get("ecartes_par_plafond", [])
        poids_retenu = bloc_obese.get("poids_champs_tokens", 0)
        mord = obese in ecartes and poids_retenu <= plafond
        detail = ("la borne n'a PAS mordu : ecartes=" + str(ecartes)
                  + ", poids=" + str(poids_retenu) + " / plafond " + str(plafond))
        if mord:
            detail = ("champ obese (" + obese + ") ECARTE ET DIT ; poids retenu "
                      + str(poids_retenu) + " <= plafond " + str(plafond))
        if not controler("borne-obese", mord, detail):
            ecarts.append("une fiche obese n'est pas ecretee, ou l'ecretage se tait")

        manquants = couverture(bloc_obese, motif.CHAMPS_ATTENDUS)
        if not controler("rien-dans-l-ombre-obese", not manquants,
                         "l'ecretage ne perd aucun champ : chacun est injecte ou DIT ecarte"
                         if not manquants else "CHAMPS SILENCIEUX : " + ", ".join(manquants)):
            ecarts.append("l'ecretage perd un champ sans le dire")

        bloc_absent = fonctions.charger_profil_utile(chemin=zone / ("absent-" + NOM_COBAYE))
        muet = not bloc_absent.get("present") and bool(bloc_absent.get("avertissement"))
        detail = "fiche introuvable -> bloc MUET (il se lirait comme complet)"
        if muet:
            detail = ("fiche introuvable -> avertissement nomme : "
                      + str(bloc_absent.get("avertissement", ""))[:70])
        if not controler("aucun-silence", muet, detail):
            ecarts.append("une fiche introuvable ne se dit pas")

        bloc_enorme = fonctions.charger_profil_utile(chemin=cobaye, plafond_tokens=PLAFOND_ENORME)
        epreuves.append(("plafond enorme -> le MEME cobaye passe ENTIER",
                         not bloc_enorme.get("ecartes_par_plafond")
                         and len(bloc_enorme.get("champs", {})) == len(motif.CHAMPS_ATTENDUS)))
        bloc_minuscule = fonctions.charger_profil_utile(chemin=cobaye,
                                                        plafond_tokens=PLAFOND_MINUSCULE)
        epreuves.append(("plafond minuscule -> le PREMIER champ passe quand meme",
                         list(bloc_minuscule.get("champs", {})) == [motif.CHAMPS_ATTENDUS[0]]
                         and len(bloc_minuscule.get("ecartes_par_plafond", []))
                         == len(motif.CHAMPS_ATTENDUS) - 1))
        reussies = sum(1 for _, ok in epreuves if ok)
        detail = "rate : " + ", ".join(nom for nom, ok in epreuves if not ok)
        if reussies == len(epreuves):
            detail = "piege (" + str(reussies) + "/" + str(len(epreuves)) + ")"
        if not controler("autotest-borne", reussies == len(epreuves), detail):
            ecarts.append("autotest de la borne du profil rate")
    finally:
        if cobaye is not None:
            try:
                Path(cobaye).unlink()
            except OSError:
                pass
    print("cobaye : " + str(len(epreuves)) + " epreuve(s) rejouee(s) en zone jetable")
    return ecarts


def main():
    parser = argparse.ArgumentParser(description="Garde : profil utilisateur injecte et borne")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = parser.parse_args()

    racine = trouver_racine(Path(arguments.racine).resolve())
    if racine is None:
        print("Zone matrix/ introuvable sous " + str(arguments.racine))
        return 2

    fonctions, erreur = charger_pilote(racine)
    if fonctions is None:
        print("REFUS : la porte d'injection du pilote ne se charge pas -- " + str(erreur))
        return 1
    motif = getattr(fonctions, "motif_profil", None)
    if motif is None:
        print("REFUS : le motif partage de la fiche profil ne se charge pas (fiche_profil.py)")
        return 1
    zone, erreur = charger_zone(racine)
    if zone is None:
        print("REFUS : le domicile de la zone jetable ne se charge pas -- " + str(erreur))
        return 1

    ecarts = []
    ecarts += verifier_domicile(racine)
    ecarts += verifier_champ_pese(fonctions)
    ecarts += verifier_deux_chemins(racine)
    ecarts_plafond, plafond = verifier_plafond(fonctions)
    ecarts += ecarts_plafond
    if isinstance(plafond, int) and plafond > 0:
        ecarts += verifier_fiche(fonctions, motif)
        ecarts += verifier_borne(zone, fonctions, motif, plafond)

    print("VERIFIER PROFIL INJECTION -- un profil qui n'arrive pas jusqu'a la mission ne personnalise rien")
    if ecarts or any(not ok for _, ok, _ in RESULTATS):
        print("")
        print("VERDICT KO : le profil n'est pas injecte, borne ou dit (voir les ecarts nommes).")
        return 1
    print("")
    print("VERDICT OK : le profil voyage avec la mission, borne et DIT, par les deux chemins.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
