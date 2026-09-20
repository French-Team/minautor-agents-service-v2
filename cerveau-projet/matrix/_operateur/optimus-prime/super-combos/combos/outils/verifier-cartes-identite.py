#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-cartes-identite.py -- Garde : toute doc de la zone PORTE une carte d'identite.

Pourquoi (audit MO-089, demande createur) : sur 65 documents de la zone Optimus,
VINGT-SIX n'avaient AUCUNE carte d'identite (surtout des README et des index) et
RIEN ne s'en plaignait : les trois verificateurs du marbre (regles, protocoles,
conventions) ne regardent que `matrice/data/`, jamais la zone de l'operateur. Un
document sans carte est un document SANS TYPE : le pilote ne peut pas savoir QUOI
il injecte -- et une doctrine qui doit etre injectee au bon moment ne peut pas
etre choisie si elle ne dit pas ce qu'elle est.

Trois autres ecarts trouves le meme jour : un `appartient_a` qui contenait un
CHEMIN (`_operateur/optimus-prime/pilote`) au lieu d'un nom, et trois `type` hors
vocabulaire (`journal-preparation`, `preparation-readme`, `outil-pilote-optimus`).

CE QU'IL EXIGE, pour chaque `.md` de la zone :
  1. une carte en TETE (front-matter `---` + `identite:`) ;
  2. les trois cles : `type`, `appartient_a`, `commun` ;
  3. `appartient_a` est un NOM, jamais un chemin (ni `/` ni `\\`) ;
  4. `type` vient d'un VOCABULAIRE FERME -- un type neuf doit etre DECLARE ici,
     jamais invente au fil de l'eau (c'est ainsi que `preparation-readme` et
     `outil-pilote-optimus` sont nes).

L'AUTOTEST le PIEGE (lecon L-032) : un cobaye complet est ACCEPTE, une carte
absente est ACCUSEE, un `appartient_a` en chemin est ACCUSE, un type inconnu est
ACCUSE. Un detecteur jamais vu crier ne prouve rien.

CE QU'IL NE FAIT PAS : lecture seule -- il lit des en-tetes de fichiers.

Usage: python verifier-cartes-identite.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = racine introuvable.
"""

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

# --- REFERENCES (aucune valeur en dur dans la logique) -----------------------
ZONE = Path("_operateur") / "optimus-prime"
# ZONES EXCLUES (MO-218/EO-212) : le corpus SCANNE est le vivant. Les autres gardes
# excluent DEJA ces memes zones (verifier-vocabulaire-etat.py : EXCLUS, avec
# 'purification' ; verifier-contrat-fondamental.py : EXCLUS_DIRS, avec les zones
# jetables). Une ARCHIVE n a pas de carte a porter : elle est morte, et exiger sa
# normalisation rendait la suite ROUGE a vie.
# MO-241 : l exclusion tenait au NOM DU PARENT (purification) et non a la NATURE du
# document -- une archive posee ailleurs (tout autre dossier nomme archives) etait donc
# accusee de nouveau, alors que la regle est la meme partout : une archive est de
# l histoire, elle ne se normalise pas. archives est declare zone morte PAR NATURE,
# et le garde DIT combien de documents il met hors corpus.
ZONES_EXCLUES = ("purification", "archives", "tmp-optimus", "tmp-cameleon", "tmp-test", "__pycache__", ".git")
EXTENSION = ".md"
MARQUEUR_FRONT = "---"
CLE_IDENTITE = "identite:"
CLES_OBLIGATOIRES = ("type", "appartient_a", "commun")
# Vocabulaire FERME des types de document. Ajouter un type = une decision,
# tracee ici -- pas un litteral invente dans un fichier.
TYPES_RECONNUS = (
    "analyse",
    "carte-mission",
    "chaine",
    "convention",
    "fiche",
    "fiche-agent",
    "index",
    "index-parcours",
    "index-themes",
    "journal",
    "mots-cles",
    "outil",
    "plan-preparation-conservation",
    "protocole",
    "readme",
    "regle-immuable",
    "role",
    "theme",
)
# Un nom d'appartenance ne contient NI separateur de dossier NI antislash.
SEPARATEURS_INTERDITS = ("/", "\\")

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


def controler(nom, condition, detail="", collecteur=None, silencieux=False):
    """Enregistre et affiche un controle.

    MO-218 (EO-212) : `collecteur` et `silencieux` existent parce que l AUTOTEST
    passait par ici avec ses PROPRES cobayes : ses accusations ATTENDUES
    s imprimaient en `[KO]`, indiscernables d un ecart REEL pour qui lit la
    sortie -- et le lanceur de non-regression LIT la sortie. Trois faux ecarts
    (sans-carte.md, app-chemin.md, type-inconnu.md : des fichiers qui n existent
    NULLE PART) ont fait passer la suite pour ROUGE a chaque run. Un garde qui
    crie pour ses cobayes apprend a ne plus etre ecoute (L-055).
    """
    (RESULTATS if collecteur is None else collecteur).append((nom, bool(condition), detail))
    if not silencieux:
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def lire_texte(chemin):
    try:
        return chemin.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def carte_de(texte):
    """Dictionnaire de la carte d'identite, ou None (pas de front-matter identite).

    Le front-matter est BORNE par deux `---` : hors de ces bornes, ce n'est pas
    une carte. On exige la ligne `identite:` -- un front-matter d'un autre genre
    (une regle horizontale en tete, par exemple) ne compte pas comme une carte.
    """
    lignes = texte.splitlines()
    if not lignes or lignes[0].strip() != MARQUEUR_FRONT:
        return None
    bloc = []
    ferme = False
    for ligne in lignes[1:]:
        if ligne.strip() == MARQUEUR_FRONT:
            ferme = True
            break
        bloc.append(ligne)
    if not ferme:
        return None
    if not any(ligne.strip() == CLE_IDENTITE for ligne in bloc):
        return None
    carte = {}
    for ligne in bloc:
        propre = ligne.strip()
        if propre == CLE_IDENTITE or propre.startswith("#"):
            continue
        if ":" in propre:
            cle, valeur = propre.split(":", 1)
            carte[cle.strip()] = valeur.strip()
    return carte


def controler_zone(zone, collecteur=None, silencieux=False):
    """Chaque .md porte une carte complete, un nom d'appartenance et un type reconnu."""
    # `dire` relaie le collecteur et le silence : l autotest ne parle plus au nom
    # du corpus reel (MO-218/EO-212).
    def dire(nom, condition, detail=""):
        return controler(nom, condition, detail, collecteur, silencieux)

    if not zone.is_dir():
        return ("zone-lisible", False, "zone introuvable : " + str(zone)), ["zone introuvable"]
    # Le corpus SCANNE est le VIVANT : archives, zones jetables et caches sont hors
    # sujet (une archive ne porte pas de carte, elle est morte -- MO-218/EO-212).
    tous = sorted(zone.rglob("*" + EXTENSION))
    fichiers = [chemin for chemin in tous
                if not any(partie in ZONES_EXCLUES
                           for partie in chemin.relative_to(zone).parts)]
    morts = [chemin for chemin in tous if chemin not in fichiers]
    # Le DIT de MO-241 : une exclusion que personne ne voit redevient une absence
    # (lecon MO-218). Le silence de l autotest, lui, reste respecte.
    if not silencieux:
        print("[--] zones-mortes : " + str(len(morts)) + " document(s) hors corpus (zones declarees : "
              + ", ".join(ZONES_EXCLUES) + ")")
    if not fichiers:
        return ("zone-lisible", False, "aucun document sous " + str(zone)), ["aucun document"]

    ecarts = []
    sans_carte, app_fautif, type_inconnu, cle_manquante = [], [], [], []
    for chemin in fichiers:
        relatif = str(chemin.relative_to(zone))
        carte = carte_de(lire_texte(chemin))
        if carte is None:
            sans_carte.append(relatif)
            continue
        manquantes = [cle for cle in CLES_OBLIGATOIRES if cle not in carte]
        if manquantes:
            cle_manquante.append(relatif + " (" + ",".join(manquantes) + ")")
        appartenance = carte.get("appartient_a", "")
        if any(sep in appartenance for sep in SEPARATEURS_INTERDITS):
            app_fautif.append(relatif + " -> " + appartenance)
        type_doc = carte.get("type", "")
        if type_doc and type_doc not in TYPES_RECONNUS:
            type_inconnu.append(relatif + " -> " + type_doc)

    dire("cartes-presentes", not sans_carte,
              str(len(fichiers)) + " document(s), chacun porte une carte"
              if not sans_carte else "SANS CARTE (" + str(len(sans_carte)) + ") : "
              + ", ".join(sans_carte[:8]) + (" ..." if len(sans_carte) > 8 else ""))
    if sans_carte:
        ecarts.append("documents sans carte : " + ", ".join(sans_carte))

    dire("cles-completes", not cle_manquante,
              "les trois cles (" + ", ".join(CLES_OBLIGATOIRES) + ") sont presentes"
              if not cle_manquante else "CLES MANQUANTES : " + ", ".join(cle_manquante))
    if cle_manquante:
        ecarts.append("cles manquantes : " + ", ".join(cle_manquante))

    dire("appartenance-est-un-nom", not app_fautif,
              "aucun appartient_a n'est un CHEMIN"
              if not app_fautif else "APPARTENANCE EN CHEMIN : " + ", ".join(app_fautif))
    if app_fautif:
        ecarts.append("appartient_a en chemin : " + ", ".join(app_fautif))

    dire("type-reconnu", not type_inconnu,
              "chaque type vient du vocabulaire ferme (" + str(len(TYPES_RECONNUS)) + " types)"
              if not type_inconnu else "TYPES HORS VOCABULAIRE : " + ", ".join(type_inconnu))
    if type_inconnu:
        ecarts.append("types hors vocabulaire : " + ", ".join(type_inconnu))

    return ("cartes-presentes", not ecarts,
            str(len(fichiers)) + " document(s) verifie(s)"), ecarts


def controler_autotest():
    """Le garde se PIEGE (lecon L-032) : quatre cobayes en dossier jetable."""
    racine = Path(tempfile.mkdtemp(prefix="verifier-cartes-autotest-"))
    zone = racine / ZONE
    zone.mkdir(parents=True, exist_ok=True)

    def poser(nom, contenu):
        (zone / nom).write_text(contenu, encoding="utf-8")

    def carte(type_doc, appartenance, commun="false"):
        return ("---\nidentite:\n  type: " + type_doc + "\n  appartient_a: "
                + appartenance + "\n  commun: " + commun + "\n---\n\n# Doc\n")

    epreuves = []
    try:
        poser("doc-sain.md", carte("convention", "optimus-prime"))
        _, ecarts = controler_zone(zone, collecteur=[], silencieux=True)
        epreuves.append(("cobaye complet ACCEPTE", not ecarts))

        shutil.rmtree(zone)
        zone.mkdir(parents=True, exist_ok=True)
        poser("sans-carte.md", "# Doc sans carte\n")
        _, ecarts = controler_zone(zone, collecteur=[], silencieux=True)
        epreuves.append(("carte ABSENTE ACCUSEE", any("sans carte" in e for e in ecarts)))

        shutil.rmtree(zone)
        zone.mkdir(parents=True, exist_ok=True)
        poser("app-chemin.md", carte("convention", "_operateur/optimus-prime/pilote"))
        _, ecarts = controler_zone(zone, collecteur=[], silencieux=True)
        epreuves.append(("appartenance EN CHEMIN ACCUSEE", any("chemin" in e for e in ecarts)))

        shutil.rmtree(zone)
        zone.mkdir(parents=True, exist_ok=True)
        poser("type-inconnu.md", carte("preparation-readme", "optimus-prime"))
        _, ecarts = controler_zone(zone, collecteur=[], silencieux=True)
        epreuves.append(("type HORS VOCABULAIRE ACCUSE", any("hors vocabulaire" in e for e in ecarts)))
    finally:
        shutil.rmtree(racine, ignore_errors=True)

    for nom, ok in epreuves:
        print("[--] cobaye " + ("ACCEPTE" if ok else "NON REPERE") + " : " + nom)
    reussies = sum(1 for ok in [ok for _, ok in epreuves] if ok)
    detail = ("piege (" + str(reussies) + "/4)" if reussies == len(epreuves)
              else "rate : " + ", ".join(nom for nom, ok in epreuves if not ok))
    return ("autotest-cartes", reussies == len(epreuves), detail)


def main():
    parser = argparse.ArgumentParser(description="Garde : carte d'identite obligatoire dans la zone")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = parser.parse_args()

    matrix = trouver_matrix(Path(arguments.racine).resolve())
    if matrix is None:
        print("Dossier matrix/ introuvable sous " + str(arguments.racine))
        return 2

    resultats = []
    ecarts_nommes = []

    resultat, ecarts = controler_zone(matrix / ZONE)
    resultats.append(resultat)
    ecarts_nommes.extend(ecarts)
    autotest = controler_autotest()
    resultats.append(autotest)
    # L-032 : le PIEGE doit etre VU crier -- mais jamais en `[KO]`, sinon l humain
    # (et la suite qui lit la sortie) le prend pour un ecart reel (MO-218/EO-212).
    print("[--] " + autotest[0] + " : " + autotest[2])

    print("VERIFIER CARTES D'IDENTITE -- un document qui ne dit pas QUOI il est ne peut pas etre injecte")
    if any(not ok for _, ok, _ in resultats) or ecarts_nommes:
        print("\nVERDICT KO : une carte manque ou n'est pas normalisee (voir les ecarts nommes).")
        return 1
    print("\nVERDICT OK : tout document de la zone porte une carte complete et normalisee.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
