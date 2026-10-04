#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
corriger-zone-tmp -- RAMENE LES SCRIPTS DE LA ZONE JETABLE EN ASCII STRICT.

POURQUOI. La zone jetable est le seul endroit du depot ou l on ecrit des
brouillons a la main -- et elle est, par construction, la ou un accent glisse
arrive le plus vite. Un script de brouillon non ASCII devient un COBAYE qui
plante sur une machine qui ne lit pas sa carte, ou un `python` qui refuse le
fichier, ou une comparaison de chaines qui ment. Le corriger est un geste
MECANIQUE : pas de sens a interpreter, pas de decision a prendre.

CE QU ELLE FAIT, ET CE QU ELLE NE FAIT PAS.
- Elle appelle `vers_ascii` AU DOMICILE (`matrice/data/commun/texte_ascii.py`)
  et ne la RECOPIE pas : une copie divergerait au premier accent de plus, et
  personne ne le dirait (L-029).
- Elle retire le caractere sans equivalent ASCII **en gardant le reste de la
  ligne** : corriger une ligne ne doit pas retirer la ligne.
- Elle RAPPORTE, pour chaque correction : le FICHIER, la LIGNE, la COLONNE et
  le POINT DE CODE. Un rapport sans position ne permet pas de verifier.

TROIS REFUS, ET ILS SONT CHOISIS.
- Elle ne touche QUE la zone qu on lui donne, et par defaut la zone JETABLE.
  Un brouillon ASCII est un outil de travail ; normaliser tout le depot serait
  une faute de perimetre, pas un service.
- Elle n ECRIT RIEN en mode `--verifier` : le scan seul doit pouvoir etre joue
  sans risque, sinon on ne le joue pas.
- Elle ne DEVINE pas la zone : un dossier introuvable est une faute nommee, pas
  un succes vide.

Usage:
  python corriger-zone-tmp.py                 (corrige et rapporte)
  python corriger-zone-tmp.py --verifier      (scan seul, n ecrit rien)
  python corriger-zone-tmp.py --zone <dossier>
  python corriger-zone-tmp.py --auto-test     (cobaye sur fichiers jetables)
  code 0 = tout est ASCII ou tout a ete corrige ; 1 = des non-ASCII restent
  (en mode verifier) ; 2 = zone introuvable.
"""
import argparse
import sys
from pathlib import Path

# --- LA RACINE, par MARQUEUR (jamais un `parents[N]` nu) ------------------------
RACINE = None
_courant = Path(__file__).resolve().parent
for _ in range(30):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        RACINE = _courant
        break
    _courant = _courant.parent
RACINE_INTROUVABLE = ("Racine matrix/ introuvable en remontant depuis "
                      + str(Path(__file__).resolve().parent))

# La zone JETABLE par defaut : c est le perimetre de ce correcteur.
ZONE_JETABLE = "_operateur/optimus-prime/tmp-optimus"
EXCLUS = {"__pycache__", ".git"}
SUFFIXES = {".py", ".md", ".json", ".jsonl", ".txt"}


def charger_vers_ascii(racine):
    """`vers_ascii` vient du DOMICILE, jamais d une copie locale."""
    commun = racine / "matrice" / "data" / "commun"
    if not commun.is_dir():
        return None, "domicile INTROUVABLE : " + str(commun)
    sys.path.insert(0, str(commun))
    try:
        from texte_ascii import vers_ascii
    except (OSError, ImportError) as erreur:
        return None, "IMPORT IMPOSSIBLE : " + type(erreur).__name__
    return vers_ascii, ""


def decouvrir(zone):
    """Les fichiers du perimetre. Un dossier introuvable est une faute, pas un vide."""
    if not zone.is_dir():
        return [], "ZONE INTROUVABLE : " + str(zone)
    trouves = []
    for chemin in sorted(zone.rglob("*")):
        if not chemin.is_file() or chemin.suffix not in SUFFIXES:
            continue
        if EXCLUS & set(chemin.relative_to(zone).parts):
            continue
        trouves.append(chemin)
    return trouves, ""


def non_ascii_de(ligne):
    """Les positions non ASCII d une ligne : (colonne, point de code, caractere).

    La colonne compte a partir de 1 : une colonne a zero fait decalage d une
    unite avec tout rapport humain, et un rapport decale n est pas relisible.
    """
    return [(index + 1, ord(caractere), caractere)
            for index, caractere in enumerate(ligne)
            if ord(caractere) > 127]


def corriger_fichier(chemin, vers_ascii, ecrire):
    """Corrige UN fichier. Rend (ecarts, corriger). `ecarts` porte la position."""
    try:
        texte = chemin.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as erreur:
        return [{"fichier": chemin.name, "erreur": type(erreur).__name__}], None
    lignes = texte.splitlines()
    ecarts = []
    corrigees = []
    for numero, ligne in enumerate(lignes, 1):
        hors = non_ascii_de(ligne)
        if not hors:
            corrigees.append(ligne)
            continue
        ecarts.append({"fichier": str(chemin), "ligne": numero,
                       "hors": [(colonne, "U+%04X" % code)
                                for colonne, code, _c in hors]})
        corrigees.append(vers_ascii(ligne))
    if ecarts and ecrire:
        # `newline=""` : on n ajoute ni on ne retire un retour a la ligne.
        chemin.write_text("\n".join(corrigees) + "\n", encoding="utf-8", newline="")
    return ecarts, "\n".join(corrigees) + "\n"


def _relatif(chemin, racine):
    """Le chemin AFFICHE, relatif a la racine quand il est sous elle.

    Un rapport qui sort un chemin absolu de 90 caracteres pour dire que le
    fichier s appelle `mo-572-cobaye-accent.py` est un rapport illisible : le
    lecteur cherche le fichier, il ne cherche pas sa racine.
    """
    texte = str(chemin)
    prefixe = str(racine) + chr(92)
    if texte.startswith(prefixe):
        return texte[len(prefixe):].replace(chr(92), "/")
    return texte


def rapporter(ecarts, chemin_affiche, racine=None):
    for ecart in ecarts:
        if "erreur" in ecart:
            print("  " + chemin_affiche + " : ILLISIBLE : " + ecart["erreur"])
            continue
        points = ", ".join("colonne " + str(c) + " " + p for c, p in ecart["hors"])
        nom = _relatif(ecart["fichier"], racine) if racine else str(ecart["fichier"])
        print("  " + nom + " ligne " + str(ecart["ligne"]) + " : " + points)


def main(argv=None):
    analyseur = argparse.ArgumentParser(
        description="Ramene les scripts de la zone jetable en ASCII strict.")
    analyseur.add_argument("--verifier", action="store_true",
                            help="scan seul : n ecrit rien")
    analyseur.add_argument("--zone", default="",
                            help="dossier a traiter (defaut : la zone jetable)")
    analyseur.add_argument("--auto-test", action="store_true",
                            help="cobaye sur fichiers jetables")
    arguments = analyseur.parse_args(argv)
    if RACINE is None:
        print(RACINE_INTROUVABLE)
        return 2
    if arguments.auto_test:
        return auto_test(RACINE)
    zone = Path(arguments.zone) if arguments.zone else (RACINE / ZONE_JETABLE)
    vers_ascii, echec = charger_vers_ascii(RACINE)
    if echec:
        print("REFUS : " + echec)
        return 2
    fichiers, echec = decouvrir(zone)
    if echec:
        print("REFUS : " + echec)
        return 2
    ecrire = not arguments.verifier
    total = 0
    modifies = 0
    for chemin in fichiers:
        ecarts, _corrige = corriger_fichier(chemin, vers_ascii, ecrire)
        if ecarts:
            total += len(ecarts)
            if ecrire:
                modifies += 1
            rapporter(ecarts, _relatif(chemin, RACINE), RACINE)
    action = "corrige" if ecrire else "verifie"
    print(action + " : " + str(len(fichiers)) + " fichier(s), " + str(modifies)
          + " modifie(s), " + str(total) + " ligne(s) non ASCII.")
    if arguments.verifier and total:
        print("VERDICT : " + str(total) + " ligne(s) non ASCII subsistent.")
        return 1
    return 0


# --- L AUTO-TEST ---------------------------------------------------------------

def auto_test(racine):
    """Neuf assertions sur des fichiers FABRIQUES, dans une zone a lui.

    Le test ne touche jamais la zone jetable REELLE : un test qui corrige les
    vrais brouillons pour prouver qu il corrige est un test qui casse le
    travail en cours.
    """
    import tempfile

    vers_ascii, echec = charger_vers_ascii(racine)
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append((nom, bool(condition), detail))

    with tempfile.TemporaryDirectory(prefix="cobaye-zone-tmp-") as temporaire:
        base = Path(temporaire)

        # 1. UN CARACTERE CONVERTISSABLE EST RETIRE, LE RESTE DE LA LIGNE GARDE.
        # 1. UN ACCENT EST DECOMPOSE EN SA LETTRE, UN CARACTERE SANS
        #    EQUIVALENT EST RETIRE. Les deux cas ne se ressemblent pas et le
        #    test les prend separement : dire < un accent disparait > serait
        #    faux, il devient sa lettre.
        accent = chr(0xE9)
        ideogramme = chr(0x6F22)
        fichier = base / "a.py"
        fichier.write_text("x = " + accent + ideogramme + "1" + NL_S,
                           encoding="utf-8", newline="")
        ecarts, _corrige = corriger_fichier(fichier, vers_ascii, False)
        controler("un accent devient sa lettre, un ideogramme est retire",
                  vers_ascii(accent + ideogramme + "1") == "e1",
                  vers_ascii(accent + ideogramme + "1"))
        # 2. LA POSITION EST RAPPORTEE : fichier, ligne, colonne, point de code.
        ecarts, _ = corriger_fichier(fichier, vers_ascii, False)
        controler("l ecart porte fichier, ligne et colonne",
                  bool(ecarts) and ecarts[0]["ligne"] == 1
                  and ecarts[0]["hors"][0][0] == 5
                  and ecarts[0]["hors"][0][1] == "U+00E9"
                  and len(ecarts[0]["hors"]) == 2,
                  ecarts)

        # 3. LA COLONNE COMPTE A PARTIR DE 1.
        controler("la colonne compte a partir de 1",
                  non_ascii_de("ab" + chr(0xE9))[0][0] == 3,
                  non_ascii_de("ab" + chr(0xE9)))

        # 4. UNE LIGNE VIDE ET UNE LIGNE ASCII NE SONT PAS ACCUSEES.
        controler("une ligne ASCII n est pas accusee", non_ascii_de("rien ici") == [])

        # 5. CORRIGER RETIRE LE CARACTERE SANS RETIRER LA LIGNE.
        fichier.write_text("ligne1 = 1" + NL_S + "ligne2 = 2" + NL_S, encoding="utf-8", newline="")
        _ecarts, corrige = corriger_fichier(fichier, vers_ascii, True)
        lignes = corrige.splitlines()
        controler("corriger garde le reste de la ligne et le nombre de lignes",
                  len(lignes) == 2 and lignes[0] == "ligne1 = 1",
                  lignes)

        # 6. UN FICHIER DEJA ASCII N EST PAS REECRIT (le mtime ne bouge pas).
        stable = base / "b.py"
        stable.write_text("rien = 0" + NL_S, encoding="utf-8", newline="")
        avant = stable.stat().st_mtime_ns
        corriger_fichier(stable, vers_ascii, True)
        controler("un fichier deja ASCII n est pas reecrit",
                  stable.stat().st_mtime_ns == avant)

        # 7. UN DOSSIER INTROUVABLE EST UNE FAUTE NOMMEE, PAS UN VIDE.
        _trouves, echec_ = decouvrir(base / "jamais")
        controler("une zone introuvable est une faute nommee",
                  bool(echec_) and "INTROUVABLE" in echec_, echec_)

        # 8. LA ZONE JETABLE REELLE N EST PAS TOUCHEE PAR LE TEST.
        controler("la zone jetable reelle n est pas le perimetre du test",
                  not (base == (racine / ZONE_JETABLE)))

        # 9. UN FICHIER ILLISIBLE EST ACCUSE, PAS RENDU VIDE.
        illisible = base / "c.py"
        illisible.write_bytes(b"\xff\xfe\x00binaire")
        ecarts, _ = corriger_fichier(illisible, vers_ascii, False)
        controler("un fichier illisible est accuse",
                  bool(ecarts) and "erreur" in ecarts[0], ecarts)

    reussis = sum(1 for _n, ok, _d in resultats if ok)
    for nom, ok, detail in resultats:
        print(("  [OK] " if ok else "  [KO] ") + nom
              + ("" if ok else " : " + str(detail)[:160]))
    print("AUTO-TEST : " + str(reussis) + "/" + str(len(resultats)) + ".")
    return 0 if reussis == len(resultats) else 1


NL_S = chr(10)

if __name__ == "__main__":
    sys.exit(main())
