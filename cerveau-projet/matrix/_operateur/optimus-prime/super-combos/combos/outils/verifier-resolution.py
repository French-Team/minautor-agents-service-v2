"""Garde : la RESOLUTION des briques tient-elle son contrat ? (EO-287 / MO-293 / MO-294)

Le lanceur (matrix/lancer.py) et les appelants INTERNES resolvent une brique par son
NOM, au domicile PARTAGE `matrice/data/commun/resolution_outils.py`.

QUI est juge, et comment : AUCUNE table tenue a la main. Un appelant se DECOUVRE par le
fait qui le definit -- il IMPORTE le domicile partage (`from resolution_outils import ...`)
-- et le nom qu il donne a `chemin_outil(...)` se lit CHEZ LUI : un litteral, ou un
identifiant resolu dans son fichier puis dans le `constants.py` le plus proche. Une table
se perime en silence : le jour ou un appelant n y est pas ajoute, il n est pas juge et
personne ne le sait. Ici, adopter le domicile SUFFIT a entrer dans le jugement.

CONTRAT -- deux polarites, toujours les deux :
  CONTRE-TEMOIN : chaque nom RENDU par le domicile pointe un main.py qui EXISTE, aucun nom
    n est pris a la fois par un outil et une routine, et chaque nom DECOUVERT chez un
    appelant RESOUT une brique reelle -- une constante renommee sans que sa cible suive
    est une panne que py_compile ne voit pas.
  COBAYE : un nom INCONNU rend un REFUS NOMME -- le nom fautif, les noms PROCHES pour un
    nom qui a des sosies, le REMEDE -- et `chemin_outil` LEVE ce meme refus ; un refus
    SILENCIEUX, ou un argument ILLISIBLE (expression calculee), est ACCUSE et jamais
    ignore.

FACADE : la CLI (matrix/lancer.py) est le DEUXIEME consommateur du MEME domicile.
  `--lister` doit rendre EXACTEMENT les noms du domicile, et un nom inconnu sortir en
  code 2. Une facade qui ne lit plus la source est un lanceur qui a diverge.

PREUVE (lecon L-032) : l autotest porte SIX epreuves -- deux resolutions truquees (MUETTE
et FANTOME, qui doivent crier) et QUATRE epreuves de DECOUVERTE sur un arbre cobaye, dont
un FAUX appelant qui doit rester INVISIBLE et un appelant SAIN qui doit rester NON accuse.
Un garde qu on ne peut pas faire rougir ne prouve rien ; un garde qui accuse tout non plus.

Verdict : 0 = contrat tenu ; 1 = ecart accuse ; 2 = refus (rien a juger).
"""
import argparse
import ast
import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# Le nom que les appelants importent (le domicile partage, M-076).
DOMICILE = "resolution_outils"
MOTIF_IMPORT = re.compile(r"^\s*from\s+" + DOMICILE + r"\s+import\s", re.MULTILINE)
# Une constante DECLAREE par un litteral : `NOM = "valeur"`.
MOTIF_CONSTANTE = re.compile(r"^\s*(?P<nom>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*[\"'](?P<valeur>[^\"']+)[\"']\s*$",
                             re.MULTILINE)

# Des noms qui ne peuvent PAS exister (le suffixe porte la mission : aucun doute).
NOMS_INCONNUS = ("outil-fantome-eo293", "brique-inconnue-eo293", "bdd")
# Un nom qui A des sosies : le refus doit les NOMMER (c est le remede utile).
NOM_AVEC_PROCHES = "bdd"
# Le refus doit NOMMER la faute et le remede. `proches` est exige EN PLUS pour un nom qui
# a des sosies -- l exiger partout accuserait a tort un nom qui n en a aucun (mesure : un
# garde qui crie a tort n est jamais branche).
MOTS_DU_REMEDE = ("nom inconnu", "remede")


def trouver_matrix(racine):
    """Retourne le dossier matrix/ (celui qui porte matrice/data/outils), ou None."""
    candidats = [racine / "cerveau-projet" / "matrix", racine / "matrix"]
    if racine.name == "matrix":
        candidats.insert(0, racine)
    candidats.append(racine)
    for candidat in candidats:
        if (candidat / "matrice" / "data" / "outils").is_dir():
            return candidat
    return None


def charger_domicile(matrix):
    """Le domicile partage, charge COMME le lanceur le charge (un seul sens)."""
    commun = matrix / "matrice" / "data" / "commun"
    chemin = commun / (DOMICILE + ".py")
    if not chemin.is_file():
        return None, "domicile ABSENT : " + str(chemin)
    if str(commun) not in sys.path:
        sys.path.insert(0, str(commun))
    spec = importlib.util.spec_from_file_location(DOMICILE + "_juge", chemin)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as erreur:
        return None, "domicile ILLISIBLE : " + type(erreur).__name__ + " -- " + str(erreur)
    return module, None


def noms_du_domicile(resolution):
    return sorted({nom for _, nom, _ in resolution.entrer_outils()})


def fichiers_python(racine):
    """Les .py d un arbre, sans les caches ni les points de restauration."""
    return sorted(p for p in Path(racine).rglob("*.py")
                  if "__pycache__" not in p.parts and ".bak" not in p.name)


def constants_le_plus_proche(chemin):
    """Le `constants.py` le plus PROCHE en remontant (une categorie range les siens a sa
    racine d outil : `machine-defcon/monter/entry.py` lit `machine-defcon/constants.py`)."""
    courant = chemin.parent
    for _ in range(4):
        candidat = courant / "constants.py"
        if candidat.is_file():
            return candidat
        if courant.parent == courant:
            break
        courant = courant.parent
    return None


def valeurs_declarees(chemin):
    """Les constantes litterales du fichier, PUIS celles de son constants.py."""
    valeurs = {}
    voisins = [chemin]
    proche = constants_le_plus_proche(chemin)
    if proche is not None:
        voisins.append(proche)
    for voisin in voisins:
        try:
            texte = voisin.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for trouve in MOTIF_CONSTANTE.finditer(texte):
            valeurs.setdefault(trouve.group("nom"), trouve.group("valeur"))
    return valeurs


def noms_appeles(chemin, valeurs):
    """(appels, ecarts) : les noms passes a `chemin_outil(...)`, LUS dans l ARBRE du code.

    L arbre (ast) et non une expression reguliere : un `chemin_outil(` cite dans un
    commentaire ou un texte n est pas un appel, et une expression IMBRIQUEE
    (`chemin_outil(str(x))`) ne doit pas passer entre les mailles -- un appel manque est
    un appel non juge.
    """
    appels = []
    ecarts = []
    try:
        arbre = ast.parse(chemin.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, SyntaxError) as erreur:
        return [], ["[KO] appelant ILLISIBLE : " + str(chemin) + " (" + type(erreur).__name__ + ")"]
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Call):
            continue
        if not isinstance(noeud.func, ast.Name) or noeud.func.id != "chemin_outil":
            continue
        if not noeud.args:
            ecarts.append("[KO] argument MANQUANT : chemin_outil() dans " + str(chemin))
            continue
        premier = noeud.args[0]
        if isinstance(premier, ast.Constant) and isinstance(premier.value, str):
            appels.append((chemin, repr(premier.value), premier.value))
            continue
        if isinstance(premier, ast.Name):
            if premier.id in valeurs:
                appels.append((chemin, premier.id, valeurs[premier.id]))
            else:
                ecarts.append("[KO] nom INTROUVABLE : " + premier.id + " (" + str(chemin)
                              + ") -- declare-le dans un constants.py, ou passe un LITTERAL")
            continue
        ecarts.append("[KO] argument ILLISIBLE : chemin_outil("
                      + ast.unparse(premier) + ") dans " + str(chemin)
                      + " -- le nom doit etre un LITTERAL ou une CONSTANTE, jamais une expression")
    return appels, ecarts


def decouvrir_appelants(racine):
    """(appels, ecarts, appelants) : QUI utilise le domicile, et avec QUELS noms.

    Aucune table : l appelant se DECOUVRE par son IMPORT du domicile partage. Ce qu on ne
    recopie pas, on ne peut pas l oublier -- et adopter le domicile suffit a etre juge.
    """
    appels = []
    ecarts = []
    appelants = []
    for chemin in fichiers_python(racine):
        if chemin.name == DOMICILE + ".py":
            continue                      # le domicile ne s appelle pas lui-meme
        try:
            texte = chemin.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if not MOTIF_IMPORT.search(texte):
            continue                      # cite le domicile sans l IMPORTER : pas un appelant
        appelants.append(chemin)
        trouves, fautes = noms_appeles(chemin, valeurs_declarees(chemin))
        appels.extend(trouves)
        ecarts.extend(fautes)
    return appels, ecarts, appelants


def juger_appels(appels, resolution, muet=False):
    """CONTRE-TEMOIN : chaque nom DECOUVERT chez un appelant resout une brique reelle."""
    ecarts = []
    for chemin, expression, nom in appels:
        cible, refus = resolution.resoudre(nom)
        if refus is not None or cible is None or not Path(cible).is_file():
            ecarts.append("[KO] nom DECOUVERT qui ne resout RIEN : " + str(chemin.name)
                          + " -> " + expression + " = " + repr(nom) + " (" + str(refus) + ")")
        elif not muet:
            print("  ok  " + str(chemin.name) + " -> " + expression + " = " + nom
                  + " (" + str(Path(cible).parent.name) + ")")
    return ecarts


def controler(resolution, appels, ecarts_decouverte):
    """Les ecarts du contrat. Les appels viennent de la DECOUVERTE, jamais d une table."""
    ecarts = list(ecarts_decouverte)
    try:
        briques = resolution.entrer_outils()
    except Exception as erreur:
        return ecarts + ["[KO] entrer_outils a LEVE : " + type(erreur).__name__]
    if not briques:
        ecarts.append("[KO] aucune brique resolvable : le domicile ne rend RIEN")
    familles = {}
    for famille, nom, principal in briques:
        if not Path(principal).is_file():
            ecarts.append("[KO] brique nommee mais ABSENTE : " + nom + " -> " + str(principal))
        if nom in familles:
            ecarts.append("[KO] nom en DOUBLE (outil ET routine) : " + nom)
        familles[nom] = famille
    ecarts.extend(juger_appels(appels, resolution, muet=True))
    # COBAYE : un nom INCONNU refuse en le NOMMANT (jamais un refus silencieux).
    for nom in NOMS_INCONNUS:
        chemin, refus = resolution.resoudre(nom)
        if chemin is not None:
            ecarts.append("[KO] nom pourtant INCONNU qui a resolu : " + repr(nom))
            continue
        if not refus:
            ecarts.append("[KO] refus SILENCIEUX (aucun message) pour : " + repr(nom))
            continue
        manquants = [mot for mot in MOTS_DU_REMEDE if mot not in refus]
        if nom == NOM_AVEC_PROCHES and "proches" not in refus:
            manquants.append("proches")
        if manquants:
            ecarts.append("[KO] refus INCOMPLET pour " + repr(nom) + " : il manque "
                          + ", ".join(sorted(set(manquants))) + " -- " + str(refus))
        try:
            resolution.chemin_outil(nom)
            ecarts.append("[KO] chemin_outil n a PAS refuse un nom inconnu : " + repr(nom))
        except Exception as erreur:
            if str(refus) not in str(erreur):
                ecarts.append("[KO] chemin_outil refuse AUTRE CHOSE que le refus nomme : "
                              + repr(nom) + " (" + type(erreur).__name__ + ")")
    return ecarts


def controler_facade(lancer, noms_attendus):
    """La CLI est le DEUXIEME consommateur du MEME domicile (EO-287)."""
    if not lancer.is_file():
        return ["[KO] facade ABSENTE : " + str(lancer)]
    ecarts = []
    rendu = subprocess.run([sys.executable, str(lancer), "--lister"],
                           capture_output=True, text=True)
    if rendu.returncode != 0:
        ecarts.append("[KO] la facade --lister sort en code " + str(rendu.returncode))
    noms_cli = sorted({ligne.split()[1] for ligne in rendu.stdout.splitlines()
                       if len(ligne.split()) == 2})
    if noms_cli != noms_attendus:
        manquants = [n for n in noms_attendus if n not in noms_cli]
        en_trop = [n for n in noms_cli if n not in noms_attendus]
        ecarts.append("[KO] facade et domicile NE DISENT PAS LA MEME CHOSE : "
                      + str(len(noms_attendus)) + " attendu(s), " + str(len(noms_cli)) + " rendu(s)"
                      + (" ; manquants : " + ", ".join(manquants[:5]) if manquants else "")
                      + (" ; en trop : " + ", ".join(en_trop[:5]) if en_trop else ""))
    refus = subprocess.run([sys.executable, str(lancer), "outil-fantome-eo293"],
                           capture_output=True, text=True)
    if refus.returncode != 2:
        ecarts.append("[KO] la facade n a PAS refuse un nom inconnu (code "
                      + str(refus.returncode) + ")")
    elif "REFUS" not in (refus.stdout or ""):
        ecarts.append("[KO] facade qui refuse SANS le dire (aucun message de refus)")
    return ecarts


class ResolutionMuette:
    """LE refus silencieux -- l ecart meme que ce garde existe pour empecher."""

    def entrer_outils(self):
        return [("outil", "fantome-eo293", Path("fantome-eo293") / "main.py")]

    def resoudre(self, nom):
        return None, None

    def chemin_outil(self, nom):
        return Path("fantome-eo293") / "main.py"


class ResolutionFantome:
    """Tous les noms resolvent vers un main.py qui N EXISTE PAS."""

    def entrer_outils(self):
        return [("outil", "fantome-eo293", Path("fantome-eo293") / "main.py")]

    def resoudre(self, nom):
        return Path("fantome-eo293") / "main.py", None

    def chemin_outil(self, nom):
        return Path("fantome-eo293") / "main.py"


def arbre_cobaye(base):
    """Un arbre synthetique : un appelant SAIN, deux FAUTES, un FAUX appelant."""
    outil = Path(base) / "outil-cobaye"
    outil.mkdir(parents=True, exist_ok=True)
    (outil / "constants.py").write_text(
        "# Les deux noms que l appelant cobaye utilise.\n"
        'NOM_SAIN = "ecrire"\n'
        'NOM_CASSE = "brique-inconnue-eo294"\n', encoding="utf-8")
    (outil / "sain.py").write_text(
        "from resolution_outils import chemin_outil\n"
        "from constants import NOM_SAIN\n"
        'chemin_outil("ecrire")\n'
        "chemin_outil(NOM_SAIN)\n", encoding="utf-8")
    (outil / "casse.py").write_text(
        "from resolution_outils import chemin_outil\n"
        "from constants import NOM_CASSE\n"
        "chemin_outil(NOM_CASSE)\n", encoding="utf-8")
    (outil / "illisible.py").write_text(
        "from resolution_outils import chemin_outil\n"
        "chemin_outil(nom_calcule())\n", encoding="utf-8")
    (outil / "faux-appelant.py").write_text(
        "# Ce fichier PARLE du domicile et appelle un chemin_outil LOCAL : il n importe\n"
        "# rien, donc il n est PAS un appelant -- et il ne doit jamais etre juge.\n"
        "def chemin_outil(nom):\n"
        "    return nom\n"
        'chemin_outil("mot-qui-n-existe-pas")\n', encoding="utf-8")
    return outil


def autotest(resolution):
    """Le garde PEUT-IL dire non, et sait-il se TAIRE quand il faut ? Six epreuves."""
    reussies = []
    manquees = []
    appels_cobaye = [(Path("cobaye.py"), "NOM_COBAYE", "fantome-eo293")]
    for etiquette, truquee in (("resolution MUETTE", ResolutionMuette()),
                               ("resolution FANTOME", ResolutionFantome())):
        if controler(truquee, appels_cobaye, []):
            reussies.append(etiquette)
        else:
            manquees.append(etiquette)
    with tempfile.TemporaryDirectory() as temporaire:
        outil = arbre_cobaye(temporaire)
        appels, ecarts, appelants = decouvrir_appelants(outil)
        noms_vus = sorted(p.name for p in appelants)
        if noms_vus == ["casse.py", "illisible.py", "sain.py"]:
            reussies.append("decouverte des appelants (le faux reste INVISIBLE)")
        else:
            manquees.append("decouverte des appelants (vus : " + ", ".join(noms_vus) + ")")
        ecarts_noms = juger_appels(appels, resolution, muet=True)
        if not any("sain.py" in ecart for ecart in ecarts_noms):
            reussies.append("appelant SAIN non accuse")
        else:
            manquees.append("appelant SAIN non accuse")
        if any("casse.py" in ecart for ecart in ecarts_noms):
            reussies.append("brique inconnue ACCUSEE")
        else:
            manquees.append("brique inconnue ACCUSEE")
        if any("ILLISIBLE" in ecart for ecart in ecarts):
            reussies.append("argument ILLISIBLE accuse")
        else:
            manquees.append("argument ILLISIBLE accuse")
    return reussies, manquees


def main():
    analyseur = argparse.ArgumentParser(description="Garde : la resolution des briques tient son contrat")
    analyseur.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = analyseur.parse_args()
    matrix = trouver_matrix(Path(arguments.racine).resolve())
    if matrix is None:
        print("Dossier matrix/ introuvable sous " + str(arguments.racine))
        return 2
    resolution, motif = charger_domicile(matrix)
    if resolution is None:
        print("[KO] " + str(motif))
        print("VERDICT KO : un garde qui ne lit pas son contrat ne peut pas dire qu il est tenu.")
        return 1
    for nom_attendu in ("entrer_outils", "resoudre", "chemin_outil"):
        if not callable(getattr(resolution, nom_attendu, None)):
            print("[KO] le domicile n expose plus " + nom_attendu + "() -- contrat rompu")
            return 1
    noms = noms_du_domicile(resolution)
    appels, ecarts_decouverte, appelants = decouvrir_appelants(matrix / "matrice")
    print("DOMICILE LU : " + str(len(noms)) + " brique(s) resolvable(s)")
    print("DECOUVERTE : " + str(len(appelants)) + " appelant(s) par leur IMPORT (aucune table)")
    for appelant in appelants:
        combien = sum(1 for chemin, _, _ in appels if chemin == appelant)
        print("  appelant " + appelant.relative_to(matrix).as_posix()
              + " -- " + str(combien) + " nom(s) lu(s)")
    if not appelants:
        ecarts_decouverte.append("[KO] AUCUN appelant decouvert : plus personne n importe le"
                                 " domicile partage ? Une decouverte qui ne trouve rien ne juge rien")
    ecarts = controler(resolution, appels, ecarts_decouverte)
    ecarts += controler_facade(matrix / "lancer.py", noms)
    reussies, manquees = autotest(resolution)
    print("[--] autotest : " + str(len(reussies)) + " epreuve(s) reussie(s) sur "
          + str(len(reussies) + len(manquees))
          + ("" if not manquees else " -- MANQUEES : " + ", ".join(manquees)))
    for manquee in manquees:
        ecarts.append("[KO] autotest : le garde n a PAS su " + manquee)
    if ecarts:
        print("")
        print("VERDICT KO : un nom ne rend pas la brique, ou un nom inconnu ne refuse pas en le nommant.")
        for ecart in ecarts:
            print(ecart if ecart.startswith("[KO]") else "[KO] " + ecart)
        return 1
    print("")
    print("VERDICT OK : chaque appelant DECOUVERT rend une brique reelle, et un nom inconnu"
          " est REFUSE en le nommant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
