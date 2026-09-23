#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""poser-template-pilote.py -- LA PORTE DES GABARITS INVISIBLES (T3 de PB-003/SP-003/TD-003).

POURQUOI (EO-273, exigence createur 4) : < des TEMPLATES de ce qu on met en place, sur le
patron des templates du cameleon dans la Matrice > -- et, Optimus etant INVISIBLE, le
dossier des gabarits vit sous `_operateur/optimus-prime/` et JAMAIS dans la zone visible.
L-016 : un moule invisible ne sert QUE de l invisible.

CE QU'IL FAIT : il lit un MOULE (jamais un artefact vivant), remplace ses JETONS en
memoire, valide le contenu, puis pose l'artefact par la PORTE ECRIRE. Rien n'est ecrit
si un seul controle tombe : un moule a moitie pose serait une copie morte.

LA REGLE QUI FAIT UN MOULE, PAS UNE COPIE (axe 4 de la contre-analyse du 2026-09-19) :
UN MOULE SANS TROU EST REFUSE. Sans jeton a remplacer il ne fabrique pas un artefact
NEUF -- il fabrique la COPIE d'un existant, donc une divergence de plus (L-055). Le
refus est NOMME et il dit quoi poser a la place.

GARANTIES (le meme contrat que `dupliquer-template`, applique a l'invisible) :
  1. le moule EXISTE et son extension est connue (.json, .py, .md) ;
  2. au moins UN jeton `__NOM__` : sinon REFUS (copie morte) ;
  3. chaque jeton RECU correspond a un jeton du moule (un jeton recu qui n existe pas
     est une faute de frappe qui poserait un artefact faux, en silence) ;
  4. AUCUN jeton residuel apres substitution ;
  5. le contenu est VALIDE avant d'ecrire : `.json` par json.load, `.py` par py_compile
     (dans un cheque temporaire), `.md` par la regle ASCII de la porte ;
  6. la CIBLE n'existe pas encore (creer) : une pose n'ecrase JAMAIS un artefact ;
  7. publication par la PORTE ECRIRE, jamais a la main (L-007).

Usage:
  python poser-template-pilote.py lister [--racine <chemin>]
  python poser-template-pilote.py poser --moule <nom.moule> --cible <chemin> \
         --jeton CLE=VALEUR [--jeton CLE=VALEUR ...] [--racine <chemin>]
  python poser-template-pilote.py --auto-test
  code 0 = pose (ou liste), 1 = refus NOMME, 2 = racine ou moule illisible.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

DOSSIER_PILOTE = Path("_operateur") / "optimus-prime" / "pilote"
DOSSIER_MOULES = Path("_operateur") / "optimus-prime" / "suivi-pilote" / "templates"
DOSSIER_COMMUN = Path("matrice") / "data" / "commun"
NOM_SERVICE_RESOLUTION = "resolution_outils.py"
NOM_PORTE_ECRIRE = "ecrire"
MOTIF_JETON = re.compile(r"__[A-Z0-9_]+__")
EXTENSIONS_VALIDES = (".json", ".py", ".md")


def trouver_racine(depart):
    for candidat in [depart, depart / "cerveau-projet" / "matrix", depart / "matrix"]:
        if (candidat / DOSSIER_PILOTE / "commun.py").is_file():
            return candidat
    return None


def lister_moules(racine):
    """Les moules disponibles : (nom relatif, jetons). Un dossier vide se DIT."""
    dossier = racine / DOSSIER_MOULES
    trouves = []
    if not dossier.is_dir():
        return trouves
    for chemin in sorted(dossier.rglob("*.moule")):
        trouves.append((str(chemin.relative_to(dossier)).replace("\\", "/"),
                        sorted(set(MOTIF_JETON.findall(chemin.read_text(encoding="utf-8",
                                                                       errors="replace"))))))
    return trouves


def resoudre_porte(racine):
    commun = racine / DOSSIER_COMMUN
    if not (commun / NOM_SERVICE_RESOLUTION).is_file():
        return None
    if str(commun) not in sys.path:
        sys.path.insert(0, str(commun))
    try:
        import resolution_outils
        return Path(resolution_outils.chemin_outil(NOM_PORTE_ECRIRE))
    except Exception:  # noqa: BLE001
        return None


def suffixe_artefact(nom_moule, cible):
    """L'extension de l ARTEFACT : le moule la porte avant son propre `.moule`
    (`declaration.json.moule` fabrique un `.json`) -- mesurer l extension du MOULE
    refusait tous les moules legitimes (mesure du 2026-09-22, auto-test)."""
    sans = Path(nom_moule).with_suffix("")
    return (sans.suffix or Path(cible).suffix).lower()


def valider(contenu, chemin, suffixe=None):
    """(Vrai, '') ou (Faux, motif) -- le contenu est eprouve AVANT la publication."""
    suffixe = suffixe or chemin.suffix.lower()
    if suffixe == ".json":
        try:
            json.loads(contenu)
            return True, ""
        except json.JSONDecodeError as erreur:
            return False, "json invalide (" + str(erreur)[:60] + ")"
    if suffixe == ".py":
        with tempfile.TemporaryDirectory() as temporaire:
            essai = Path(temporaire) / "essai.py"
            essai.write_text(contenu, encoding="utf-8", newline="\n")
            resultat = subprocess.run([sys.executable, "-m", "py_compile", str(essai)],
                                      capture_output=True, text=True)
            if resultat.returncode != 0:
                return False, "py_compile refuse (" + (resultat.stderr or "").strip()[-120:] + ")"
    return True, ""


def resoudre_cible(racine, cible):
    """Le chemin RESOLU de la cible, s il tombe DANS la racine, sinon None.

    Mesure du 2026-09-22 : la premiere version joignait toujours la racine -- une cible
    donnee avec le prefixe du depot (`cerveau-projet/matrix/...`) etait alors DOUBLEE et
    l artefact se posait dans un arbre parasite. Un chemin qui se double se REFUSE, il ne
    s ecrit pas.
    """
    texte = str(cible).replace("\\", "/")
    prefixe = "cerveau-projet/matrix/"
    if texte.startswith(prefixe):
        texte = texte[len(prefixe):]
    essais = [Path(texte), racine / texte]
    for essai in essais:
        chemin = essai if essai.is_absolute() else (Path.cwd() / essai)
        try:
            chemin.resolve().relative_to(racine.resolve())
            return chemin if essai.is_absolute() else (Path.cwd() / essai)
        except ValueError:
            continue
    return None


def poser(racine, nom_moule, cible, jetons):
    """Pose l'artefact. Rend (code, sortie) -- et n'ecrit RIEN si un controle tombe."""
    dossier = racine / DOSSIER_MOULES
    chemin_moule = dossier / nom_moule
    if not chemin_moule.is_file():
        proches = [n for n, _ in lister_moules(racine)]
        return 1, ("REFUS : moule introuvable : " + nom_moule
                   + (" -- moules disponibles : " + ", ".join(proches) if proches
                      else " -- aucun moule dans " + str(dossier)))
    suffixe = suffixe_artefact(nom_moule, cible)
    if suffixe not in EXTENSIONS_VALIDES:
        return 1, ("REFUS : extension d artefact inconnue pour " + chemin_moule.name
                   + " -> " + (suffixe or "(aucune)")
                   + " (permises : " + ", ".join(EXTENSIONS_VALIDES) + ")")
    source = chemin_moule.read_text(encoding="utf-8")
    attendus = set(MOTIF_JETON.findall(source))
    if not attendus:
        return 1, ("REFUS : le moule " + nom_moule + " n a AUCUN jeton a remplacer -- "
                   "un moule sans trou ne fabrique pas un artefact NEUF, il fabrique une "
                   "COPIE morte (L-055). Ajoute un jeton (__NOM__) ou n utilise pas de moule.")
    # Un jeton RECU se nomme SANS ses doubles soulignes (__NOM__ dans le moule).
    recus = {"__" + cle.strip("_") + "__" for cle in jetons}
    inconnus = sorted(recus - attendus)
    if inconnus:
        return 1, ("REFUS : jeton(s) recu(s) que le moule ne porte PAS : " + ", ".join(inconnus)
                   + " -- jetons attendus : " + ", ".join(sorted(attendus)))
    contenu = source
    for cle, valeur in jetons.items():
        contenu = contenu.replace("__" + cle.strip("_") + "__", valeur)
    residuels = sorted(set(MOTIF_JETON.findall(contenu)))
    if residuels:
        return 1, ("REFUS : jeton(s) NON remplace(s) : " + ", ".join(residuels)
                   + " -- un artefact a trous se lirait comme un artefact fini.")
    valide, motif = valider(contenu, cible, suffixe)
    if not valide:
        return 1, "REFUS : le contenu pose serait invalide -- " + motif
    chemin_cible = resoudre_cible(racine, cible)
    if chemin_cible is None:
        return 1, ("REFUS : la cible sort de la racine " + str(racine) + " : " + str(cible)
                   + " -- la cible est RELATIVE a la racine (ex. "
                   + "_operateur/optimus-prime/suivi-pilote/mon-suivi.md).")
    if chemin_cible.exists():
        return 1, ("REFUS : la cible existe deja : " + str(chemin_cible)
                   + " -- une pose n ecrase JAMAIS un artefact.")
    chemin_cible.parent.mkdir(parents=True, exist_ok=True)
    porte = resoudre_porte(racine)
    if porte is None:
        return 2, "REFUS : la porte '" + NOM_PORTE_ECRIRE + "' est introuvable."
    resultat = subprocess.run([sys.executable, str(porte), "ecrire", "--fichier",
                               str(chemin_cible), "--contenu", contenu, "--mode", "creer"],
                              capture_output=True, text=True, encoding="utf-8", errors="replace")
    sortie = ((resultat.stdout or "") + (resultat.stderr or "")).strip()
    if resultat.returncode != 0:
        return 1, "REFUS de la porte : " + sortie[-300:]
    return 0, ("POSE : " + str(chemin_cible) + " depuis " + nom_moule
               + " (" + str(len(jetons)) + " jeton(s) remplace(s))")


def auto_test(racine):
    """Le cobaye EPROUVE le refus : un moule sans trou, un jeton inconnu, une cible prise."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)

    moules = lister_moules(racine)
    controler("des moules sont DECLARES, avec leurs jetons", len(moules) > 0,
              str(len(moules)) + " moule(s) : " + ", ".join(nom for nom, _ in moules))
    sans_jeton = [nom for nom, jetons in moules if not jetons]
    controler("AUCUN moule sans trou (une copie morte est refusee)",
              not sans_jeton, "moules sans jeton : " + (", ".join(sans_jeton) or "aucun"))
    if moules:
        nom, jetons = moules[0]
        code, sortie = poser(racine, nom, "_operateur/optimus-prime/tmp-interdit.md", {})
        controler("un moule dont les jetons ne sont PAS remplaces est REFUSE",
                  code == 1 and "NON remplace" in sortie, sortie[:90])
        code, sortie = poser(racine, nom, "_operateur/optimus-prime/tmp-interdit.md",
                             {"JETON_QUI_N_EXISTE_PAS": "x"})
        controler("un jeton RECU que le moule ne porte pas est REFUSE",
                  code == 1 and "ne porte PAS" in sortie, sortie[:90])
    return 0 if all(resultats) else 1


def principal(arguments):
    parseur = argparse.ArgumentParser(description="Porte des gabarits invisibles du pilote.")
    parseur.add_argument("verbe", nargs="?", default="lister", choices=("lister", "poser"))
    parseur.add_argument("--moule", default="")
    parseur.add_argument("--cible", default="")
    parseur.add_argument("--jeton", action="append", default=[])
    parseur.add_argument("--racine", default=".")
    parseur.add_argument("--auto-test", action="store_true")
    options = parseur.parse_args(arguments)
    racine = trouver_racine(Path(options.racine).resolve())
    if racine is None:
        print("REFUS : racine introuvable (aucun _operateur/optimus-prime/pilote/commun.py).")
        return 2
    if options.auto_test:
        return auto_test(racine)
    if options.verbe == "lister":
        moules = lister_moules(racine)
        if not moules:
            print("Aucun moule dans " + str(racine / DOSSIER_MOULES) + " -- rien a poser.")
            return 0
        print("MOULE -- gabarits invisibles (" + str(len(moules)) + ")")
        for nom, jetons in moules:
            print("  " + nom + " | jetons : " + (", ".join(jetons) if jetons else "AUCUN"))
        return 0
    if not options.moule or not options.cible:
        print("REFUS : poser exige --moule <nom.moule> et --cible <chemin>.")
        return 1
    jetons = {}
    for morceau in options.jeton:
        if "=" not in morceau:
            print("REFUS : --jeton attend CLE=VALEUR, recu : " + morceau)
            return 1
        cle, valeur = morceau.split("=", 1)
        jetons[cle] = valeur
    code, sortie = poser(racine, options.moule, options.cible, jetons)
    print(sortie)
    return code


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
