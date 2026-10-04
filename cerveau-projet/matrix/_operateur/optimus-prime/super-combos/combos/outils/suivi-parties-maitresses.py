#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
suivi-parties-maitresses -- LA PORTE DES SIX PARTIES MAITRESSES (MO-565).

POURQUOI. Le createur a nomme SIX parties maitresses du travail d Optimus. Deux
etaient deja servies -- le PILOTE par `suivi-pilote.py`, le CAMELEON par
`suivi-cameleon.py`. Les QUATRE autres n avaient AUCUN suivi : la Matrice (ses
BDD et leur age), les ROUTINES (mode, cadence, vivant ou mort), les ESPIONS
(ce qu ils surveillent, et les fichiers disparus) et les OUTILS (le parc, ses
briques, celles qui sont declarees et introuvables). Un travail dont personne
ne suit les parties ne se verifie pas.

CE QU ELLE EST : une VUE DERIVEE. Elle ne recopie aucun fait -- elle LIT les
sources et les RASSEMBLE sous quatre angles. Elle n ecrit qu elle-meme, et elle
pose chaque fichier par la PORTE ECRIRE comme le font ses jumelles.

LES DEUX PARTIES DEJA SERVIES NE SONT PAS RECOPIEES (L-055). Elles recoivent dans
l index un POINTEUR et leur AGE. Une deuxieme vue de la meme partie serait deux
vrais qui divergent.

LA LOI DES COLONNES (exigence createur, identique a ses jumelles) : une colonne
se garde si elle VARIE ou si elle PORTE UN VERDICT. Une colonne qui vaut `--`
pour tout le monde est un placeholder qui ment : elle est OMISE, et la vue DIT
lesquelles elle a omises.

UN AGE QUI NE SE LIT PAS SE DIT. Aucun age illisible n est rendu 0 : une BDD sans
date de generation n a pas un age de zero seconde, elle a un age INCONNU.

CE QU ELLE REFUSE, ET C EST CHOISI :
- elle ne REGENERE pas une partie deja servie, elle ne fait qu la pointer ;
- elle n INVENTE aucun fait : une source illisible est ACCUSEE et nommee, elle
  ne se remplace pas par une ligne vide ;
- elle n ecrit JAMAIS dans `matrice/data` : ses vues vivent a cote d elle.

Usage:
  python suivi-parties-maitresses.py            regenere les 4 vues + l index
  python suivi-parties-maitresses.py --json     les mesures, sans ecrire
  python suivi-parties-maitresses.py --partie <nom>   une seule partie
  python suivi-parties-maitresses.py --auto-test   eprouve les extracteurs
  code 0 = vues regenerees et lisibles ; 1 = au moins une source illisible ;
  2 = racine matrix/ introuvable.
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# --- LA RACINE, par MARQUEUR --------------------------------------------------
# Aucun `parents[N]` nu : un nombre de niveaux compte a la main devient faux des
# que l objet change de place, et il se TAIT en devenant faux (MO-088).
RACINE = None
RACINE_INTROUVABLE = ''
_courant = Path(__file__).resolve().parent
BORNES_REMONTEE = 30
for _ in range(BORNES_REMONTEE):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        RACINE = _courant
        break
    _courant = _courant.parent
if RACINE is None:
    RACINE_INTROUVABLE = ("Racine matrix/ introuvable en remontant depuis "
                          + str(Path(__file__).resolve().parent))

# --- DOMICILES ----------------------------------------------------------------
if RACINE is not None:
    DOSSIER_VUES = RACINE / "_operateur" / "optimus-prime" / "suivi-parties"
    CHEMIN_PLANNING = RACINE / "matrice" / "routines" / "vie" / "planning.json"
    DOSSIER_DATA = RACINE / "matrice" / "data"
    CHEMIN_ESPIONS = (RACINE / "_operateur" / "optimus-prime" / "espions"
                      / "registre" / "registre.json")
    CHEMIN_OUTILS = DOSSIER_DATA / "registre-outils.json"
    # Les chemins sont relatifs a `matrix/`, comme ceux du registre des outils.
    # Ils sont MESURES, pas supposes : la vue du cameleon vit dans
    # `matrice/data/`, pas dans un dossier `suivi-cameleon/` -- un chemin
    # suppose faisait dire ABSENTE a une vue qui existe.
    VUES_SERVIES = (
        ("pilote", "_operateur/optimus-prime/suivi-pilote/suivi-pilote.md",
         "suivi-pilote.py"),
        ("cameleon", "matrice/data/suivi-cameleon.md",
         "suivi-cameleon.py"),
    )
    # Les quatre parties SANS suivi : leur source, une fois chacune.
    PARTIES = (
        ("matrice", "suivi-matrice.md",
         "les BDD de la Matrice et leur age"),
        ("routines", "suivi-routines.md",
         "les routines declarees, leur mode et leur cadence"),
        ("espions", "suivi-espions.md",
         "ce que les espions surveillent, et les fichiers disparus"),
        ("outils", "suivi-outils.md",
         "le parc des outils : briques, servies, declarees et introuvables"),
    )
    NOM_INDEX = "suivi-parties-maitresses.md"

    # LES VUES QUE CETTE PORTE ECRIT (MO-576). Une vue se RECALCULE a chaque passe
    # : elle ne peut donc pas porter une note attestant son contenu AVANT l ecriture
    # -- une note d avant la passe est perimee des la passe suivante, et une note
    # d apres ne peut pas exister. Le controle d attribution les lisait comme des
    # sources, et les accusait a chaque rafraichissement.
    # La liste est DERIVEE des declarations ci-dessus (DOSSIER_VUES, NOM_INDEX,
    # PARTIES), jamais recopiee (L-029).
    VUES_PRODUITES = tuple(str(DOSSIER_VUES / nom).replace(chr(92), "/")
                          for nom in (NOM_INDEX,) + tuple(nom for _, nom, _ in PARTIES))

NL = chr(10)  # le retour a la ligne, par LE CODE : une barre oblique
#dans un litteral est une echappement, pas un retour a la ligne.

FORMAT_DATE = "%Y-%m-%d %H:%M:%S"  # UN SEUL format de date dans la porte :
#deux formats divergents produiraient deux vues qui se contredisent sans que
#rien ne le dise.


def maintenant():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def age_de(secondes):
    """Un age en texte, ou INCONNU -- jamais 0 pour ce qu on ne sait pas."""
    if secondes is None:
        return "inconnu"
    if secondes < 60:
        return str(int(secondes)) + " s"
    if secondes < 3600:
        return str(int(secondes // 60)) + " min"
    if secondes < 86400:
        return str(int(secondes // 3600)) + " h"
    return str(int(secondes // 86400)) + " j"


def _lire_json(chemin, defaut=None):
    """Lecture JSON qui DIT l echec au lieu de le renvoyer silencieusement."""
    try:
        return json.loads(chemin.read_text(encoding="utf-8")), ""
    except (OSError, ValueError) as erreur:
        return defaut, (str(chemin) + " ILLISIBLE : " + type(erreur).__name__)


def _date_fichier(chemin):
    """La date de MODIFICATION du fichier, ou None. Jamais 0 pour un inconnu."""
    try:
        return datetime.fromtimestamp(chemin.stat().st_mtime)
    except OSError:
        return None


# --- LES QUATRE PARTIES --------------------------------------------------------

def partie_matrice(dossier_data, maintenant_dt=None):
    """Les BDD de la Matrice : nom, type, date de generation, age."""
    maintenant_dt = maintenant_dt or datetime.now()
    lignes = []
    echecs = []
    if dossier_data is None or not dossier_data.is_dir():
        return [], ["dossier data INTROUVABLE : " + str(dossier_data)]
    for chemin in sorted(dossier_data.glob("*.json*")):
        if chemin.name.endswith(".sha256") or chemin.name.endswith(".tmp"):
            continue
        nature = "jsonl" if chemin.suffix == ".jsonl" else "json"
        modifie = _date_fichier(chemin)
        lignes.append({
            "fichier": chemin.name,
            "nature": nature,
            "octets": chemin.stat().st_size,
            "modifie_le": modifie.strftime(FORMAT_DATE) if modifie else "inconnu",
            "age": age_de((maintenant_dt - modifie).total_seconds()) if modifie else None,
        })
        if modifie is None:
            echecs.append(chemin.name + " : date de modification ILLISIBLE")
    return lignes, echecs


def partie_routines(chemin_planning, racine=None):
    """Les routines declarees : nom, mode, cadence, priorite, vivant ou mort.

    Le PID se LIT DANS LE SYSTEME : une cadence declaree ne prouve pas que la
    routine tourne, et une vue qui recopierait la declaration seulement dirait
    un fait qui peut etre vieux.
    """
    donnees, echec = _lire_json(chemin_planning, {})
    if echec:
        return [], [echec]
    routines = donnees.get("routines", []) if isinstance(donnees, dict) else []
    lignes = []
    for routine in routines:
        if not isinstance(routine, dict):
            continue
        nom = str(routine.get("nom", "?"))
        vivant, pourquoi = _routine_vivante(nom, racine)
        lignes.append({
            "nom": nom,
            "mode": str(routine.get("mode", "inconnu")),
            "cadence": str(routine.get("cadence_secondes", "inconnu")) + " s",
            "priorite": str(routine.get("priorite", "inconnu")),
            "vivant": vivant,
            "etat": pourquoi,
        })
    return lignes, []


def _routine_vivante(nom, racine=None):
    """Le vivant ou le mort se lit PAR LA SONDE IMPORTEE, sur le PID PUBLIE.

    Le nom du FICHIRE d etat n est pas le nom de la routine : la routine
    `espion-integrite` publie son pid dans `espion-etat.json`. Deviner le
    fichier par le nom de la routine eut rendu `non publie` pour tout le parc
    alors que le pid existe -- un controle qui rate sa source rend un fait
    faux, ce qui est pire que de ne rien dire. On BALAIE donc le dossier de la
    routine, et l on DIT quel fichier a porte le pid.
    """
    if racine is None:
        return "non publie", "racine indisponible"
    dossier = racine / "matrice" / "routines" / nom
    if not dossier.is_dir():
        return "inconnue", "dossier de routine INTROUVABLE"
    for chemin in sorted(dossier.iterdir()):
        if chemin.name.endswith(".sha256") or chemin.name.endswith(".tmp"):
            continue
        if chemin.suffix == ".pid":
            try:
                pid = int(chemin.read_text(encoding="utf-8").strip())
            except (OSError, ValueError):
                continue
            if pid > 0:
                vivant, _raison = _interroger_sonde(pid)
                return vivant, ("pid " + str(pid) + " (lu dans " + chemin.name + ")")
        elif chemin.suffix == ".json":
            donnees, echec = _lire_json(chemin, {})
            if echec or not isinstance(donnees, dict):
                continue
            pid = donnees.get("pid")
            if isinstance(pid, int) and pid > 0:
                vivant, _raison = _interroger_sonde(pid)
                return vivant, ("pid " + str(pid) + " (lu dans " + chemin.name + ")")
    return "non publie", "aucun etat du dossier ne porte de pid"


def _interroger_sonde(pid):
    """La sonde de vivacite est IMPORTEE du motif partage, jamais recopiee."""
    racine = racine_de_test()
    chemin_commun = str(racine / "matrice" / "data" / "commun")
    if chemin_commun not in sys.path:
        sys.path.insert(0, chemin_commun)
    try:
        from vivacite import processus_vivant
    except (OSError, ImportError) as erreur:
        return "inconnu", "sonde INDISPONIBLE : " + type(erreur).__name__
    try:
        vivant = bool(processus_vivant(pid))
    except Exception as erreur:  # la sonde peut lever : on ne l avale pas
        return "inconnu", "sonde MUETTE : " + type(erreur).__name__
    return ("vivant" if vivant else "mort"), ""


def partie_espions(chemin_espions):
    """Ce que les espions surveillent : nombre d empreintes, disparus, date."""
    donnees, echec = _lire_json(chemin_espions, {})
    if echec:
        return [], [echec]
    empreintes = donnees.get("empreintes", {})
    if not isinstance(empreintes, dict):
        return [], [str(chemin_espions) + " : cle `empreintes` absente ou malformee"]
    date = str(donnees.get("date", "inconnu"))
    return [{
        "fichiers_surveilles": len(empreintes),
        "registre_le": date,
    }], []


def _chemin_present(chemin, racine=None):
    """Le chemin du registre est relatif a `matrix/` : on le RESOUT, on ne le
    devine pas. Un registre non resolu accuse des outils qui existent -- c est
    la faute la plusfacile a commettre, et la moins visible."""
    racine = racine if racine is not None else racine_de_test()
    relatif = str(chemin).replace(chr(92), "/")
    return (racine / relatif).exists()


def partie_outils(chemin_outils):
    """Le parc des outils : briques, servies a l injection, declarees-introuvables."""
    donnees, echec = _lire_json(chemin_outils, {})
    if echec:
        return [], [echec]
    outils = donnees.get("outils", []) if isinstance(donnees, dict) else []
    if not isinstance(outils, list) or not outils:
        return [], [str(chemin_outils) + " ne porte AUCUNE brique"]
    servies = [o for o in outils if isinstance(o, dict) and o.get("servi_a_l_injection")]
    # `exists`, PAS `is_file` : la plupart des outils de la Matrice sont des
    # DOSSIERS, et un `is_file` les declarait disparus a lui seul (mesure du
    # 2026-10-04 : 77 faux positifs sur 191 briques, la porte `registre-outils`
    # n en accuse que 4).
    introuvables = [o for o in outils
                    if isinstance(o, dict) and str(o.get("chemin", ""))
                    and not _chemin_present(o.get("chemin"))]
    par_domicile = {}
    for outil in outils:
        if not isinstance(outil, dict):
            continue
        domicile = str(outil.get("domicile", "?"))
        compte = par_domicile.setdefault(domicile, {"briques": 0, "servies": 0})
        compte["briques"] += 1
        if outil.get("servi_a_l_injection"):
            compte["servies"] += 1
    return [{
        "briques": len(outils),
        "servies": len(servies),
        "declarees_introuvables": len(introuvables),
        "par_domicile": par_domicile,
        "introuvables": sorted(str(o.get("nom")) for o in introuvables),
    }], []


# --- LE RENDU DES VUES ---------------------------------------------------------

def _carte(type_carte, titre, description):
    """La carte d identite, puis le titre, puis la description en CITATION.

    Chaque ligne de la description est prefixee par `>` : une description dont
    seules les premieres lignes sont citees se lit comme un fait qui compte et
    une suite qui non -- c est la mise en page de ses jumelles.
    """
    lignes = [l for l in str(description).splitlines()]
    corps = ("---" + NL
             + "identite:" + NL
             + "  type: " + type_carte + NL
             + "  appartient_a: optimus-prime" + NL
             + "  commun: false" + NL
             + "---" + NL + NL
             + "# " + titre + NL + NL)
    for ligne in lignes:
        corps += ("> " + ligne).rstrip() + NL
    corps += (">" + NL
              + "> Vue DERIVEE, REGENERABLE : " + maintenant() + " par" + NL
              + "> `suivi-parties-maitresses.py`. Aucun fait n est ecrit deux fois --" + NL
              + "> la source reste la source (L-055)." + NL + NL)
    return corps


def rendre_matrice(lignes, echecs):
    corps = _carte("analyse", "SUIVI DE LA MATRICE",
                   "Les BDD de la Matrice et leur age. L age se LIT dans la date de\n"
                   "modification du fichier : une BDD dont la date ne se lit pas a un age\n"
                   "INCONNU, jamais zero.")
    corps += "## BDD\n\n| Fichier | Nature | Octets | Modifie le | Age |\n|---|---|---|---|---|\n"
    for ligne in lignes:
        corps += ("| `%s` | %s | %d | %s | %s |\n"
                  % (ligne["fichier"], ligne["nature"], ligne["octets"],
                     ligne["modifie_le"], ligne["age"]))
    corps += "\n%d BDD mesuree(s).\n" % len(lignes)
    return corps + _pied_echecs(echecs)


def rendre_routines(lignes, echecs):
    corps = _carte("analyse", "SUIVI DES ROUTINES",
                   "Les routines declarees, leur mode et leur cadence. Le vivant ou mort se\n"
                   "lit DANS LE SYSTEME (le PID de l etat court), pas dans la declaration :\n"
                   "une cadence declaree ne prouve pas que la routine tourne.")
    corps += "## Routines\n\n| Routine | Mode | Cadence | Priorite | Etat | Temoin |\n|---|---|---|---|---|---|\n"
    for ligne in lignes:
        corps += ("| `%s` | %s | %s | %s | %s | %s |\n"
                  % (ligne["nom"], ligne["mode"], ligne["cadence"],
                     ligne["priorite"], ligne["vivant"], ligne["etat"]))
    corps += "\n%d routine(s) declaree(s).\n" % len(lignes)
    return corps + _pied_echecs(echecs)


def rendre_espions(lignes, echecs):
    corps = _carte("analyse", "SUIVI DES ESPIONS",
                   "Ce que les espions surveillent. L empreinte d un fichier disparu est un\n"
                   "fait, pas un bruit : c est le seul temoin qu il a ete la.")
    corps += "## Espions\n\n| Ce qui est mesure | Valeur |\n|---|---|\n"
    for ligne in lignes:
        corps += "| Fichiers surveilles | %d |\n" % ligne["fichiers_surveilles"]
        corps += "| Registre pose le | %s |\n" % ligne["registre_le"]
    return corps + _pied_echecs(echecs)


def rendre_outils(lignes, echecs):
    corps = _carte("analyse", "SUIVI DES OUTILS",
                   "Le parc des outils : briques declarees, celles que l injection sait\n"
                   "servir, et celles qui sont DECLAREES mais introuvables sur disque -- ces\n"
                   "dernieres sont accusees, jamais rayees en silence.")
    corps += "## Parc\n\n| Ce qui est mesure | Valeur |\n|---|---|\n"
    for ligne in lignes:
        corps += "| Briques au registre | %d |\n" % ligne["briques"]
        corps += "| Servies a l injection | %d |\n" % ligne["servies"]
        corps += "| Declarees et introuvables | %d |\n" % ligne["declarees_introuvables"]
    corps += "\n## Par domicile\n\n| Domicile | Briques | Servies |\n|---|---|---|\n"
    for ligne in lignes:
        for domicile in sorted(ligne["par_domicile"]):
            compte = ligne["par_domicile"][domicile]
            corps += "| `%s` | %d | %d |\n" % (domicile, compte["briques"], compte["servies"])
    introuvables = lignes[0]["introuvables"] if lignes else []
    if introuvables:
        corps += "\n## Declarees et introuvables\n\n"
        for nom in introuvables:
            corps += "- `%s` -- declare au registre, absent du disque.\n" % nom
    return corps + _pied_echecs(echecs)


def rendre_index(mesures, racine):
    """L INDEX des six : ou les suivre. Jamais une deuxieme vue."""
    corps = _carte("index", "LES SIX PARTIES MAITRESSES",
                   "Ou suivre chacune des six parties nommees par le createur. Les deux\n"
                   "parties deja servies y recoivent un POINTEUR et leur age, jamais une\n"
                   "deuxieme vue (L-055).")
    corps += "## Les six\n\n| Partie | Vue | Etat de la vue |\n|---|---|---|\n"
    for nom, fichier, description in PARTIES:
        age = _age_de_vue(racine / "_operateur" / "optimus-prime" / "suivi-parties" / fichier)
        corps += "| %s | `%s` | %s |\n" % (nom, "suivi-parties/" + fichier, age)
    corps += "\n## Les deux deja servies (pointeur, pas de deuxieme vue)\n\n"
    corps += "| Partie | Vue | Porte | Etat de la vue |\n|---|---|---|---|\n"
    for nom, chemin, porte in VUES_SERVIES:
        age = _age_de_vue(racine / chemin)
        corps += "| %s | `%s` | `%s` | %s |\n" % (nom, chemin, porte, age)
    corps += "\nLES QUATRE DERNIERES N AVAIENT AUCUN SUIVI. Les deux premieres en avaient\n"
    corps += "chacun un, depuis le 2026-09-21 et le 2026-10-03 respectivement.\n"
    return corps


def _age_de_vue(chemin):
    modifie = _date_fichier(chemin)
    if modifie is None:
        return "ABSENTE"
    return age_de((datetime.now() - modifie).total_seconds()) + " (mesure le " \
        + modifie.strftime(FORMAT_DATE) + ")"


def _pied_echecs(echecs):
    if not echecs:
        return "\nSources illisibles : aucune.\n"
    corps = "\n## Sources ILLISIBLES (accusees, jamais remplacees)\n\n"
    for echec in echecs:
        corps += "- " + echec + "\n"
    return corps

# --- L ECRITURE, par la PORTE ECRIRE ------------------------------------------

def ecrire_par_la_porte(chemin_vue, contenu, racine):
    """La vue est posee par la PORTE ECRIRE, jamais par une ecriture directe.

    Le tampon est pose A COTE de la vue et supprime DANS TOUS LES CAS : un
    tampon laisse dans la Matrice serait lui-meme une vue sans carte, et il
    remplacerait la source d une ligne.
    """
    lanceur = racine / "lancer.py"
    if not lanceur.is_file():
        return "lanceur INTROUVABLE : " + str(lanceur)
    temporaire = chemin_vue.with_suffix(chemin_vue.suffix + ".tmp")
    try:
        temporaire.write_text(contenu, encoding="utf-8", newline="\n")
        commande = [sys.executable, str(lanceur), "--appelant", "operateur",
                    "ecrire", "ecrire", "--fichier",
                    str(chemin_vue.relative_to(racine.parent.parent)),
                    "--contenu-fichier", str(temporaire.relative_to(racine.parent.parent)),
                    "--mode", "remplacer"]
        resultat = subprocess.run(commande, capture_output=True, cwd=str(racine.parent.parent),
                                  timeout=180)
    except (OSError, subprocess.TimeoutExpired) as erreur:
        return "ECRITURE IMPOSSIBLE : " + type(erreur).__name__
    finally:
        if temporaire.is_file():
            try:
                temporaire.unlink()
            except OSError:
                pass
    sortie = ((resultat.stdout or b"") + (resultat.stderr or b"")).decode(
        "utf-8", errors="replace").encode("ascii", "ignore").decode("ascii")
    if resultat.returncode != 0:
        return "la porte ECRIRE a refuse " + chemin_vue.name + " : " + sortie.strip()[:200]
    return ""


# --- L AUTO-TEST ---------------------------------------------------------------

def _cobayes():
    """Trois jeux de faits FABRIQUES, un par extracteur : la preuve vient du jeu."""
    return {
        "bdd": [
            {"fichier": "cobaye.json", "nature": "json", "octets": 10,
             "modifie_le": "2026-10-04 04:00:00", "age": "1 h"},
        ],
        "routines": [
            {"nom": "cobaye-vivante", "mode": "boucle", "cadence": "20 s",
             "priorite": "80", "vivant": "vivant", "etat": "pid 1"},
            {"nom": "cobaye-sans-pid", "mode": "passe", "cadence": "60 s",
             "priorite": "1", "vivant": "inconnu", "etat": "PID INTROUVABLE"},
        ],
        "espions": [{"fichiers_surveilles": 3, "registre_le": "2026-10-04 04:00:00"}],
        "outils": [{"briques": 5, "servies": 2, "declarees_introuvables": 1,
                    "par_domicile": {"d1": {"briques": 5, "servies": 2}},
                    "introuvables": ["absent.py"]}],
    }


def auto_test():
    """Les extracteurs sont eprouves sur des faits FABRIQUES.

    On ne teste pas la porte entiere sur la zone reelle : un test qui lit la
    zone reelle ne peut pas distinguer un extracteur faux d une source fausse.
    """
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append((nom, bool(condition), detail))

    cobayes = _cobayes()

    # 1. UN AGE ILLISIBLE N EST JAMAIS RENDU ZERO.
    controler("un age illisible vaut inconnu, jamais 0",
              age_de(None) == "inconnu", age_de(None))

    # 2. LE RENDU D UNE DATE IMPOSSIBLE NE FABRIQUE PAS UNE DATE.
    controler("un fichier sans date de modification rend inconnu",
              _date_fichier(Path(chemin_inexistant_du_cobaye())) is None)

    # 3. LE LECTEUR JSON DIT SON ECHEC AU LIEU DE LE RENVOYER SILENCIEUX.
    donnees, echec = _lire_json(Path(chemin_inexistant_du_cobaye()), {})
    controler("une source absente est ACCUSEE, pas rendue vide",
              bool(echec) and donnees == {}, echec)

    # 4. LA VUE D OUTILS NOME CHAQUE BRIQUE DECLAREE ET INTROUVABLE.
    corps = rendre_outils(cobayes["outils"], [])
    controler("la vue nomme la brique declaree et introuvable",
              "absent.py" in corps and "Declarees et introuvables" in corps)

    # 5. LA VUE D OUTILS DIT LE NOMBRE PAR DOMICILE.
    controler("la vue des outils compte par domicile", "d1" in corps)

    # 6. UNE SOURCE ILLISIBLE EST ACCUSEE DANS LA VUE, PAS DISSIMULEE.
    corps_bdd = rendre_matrice([], ["cobaye.json : ILLISIBLE"])
    controler("une source illisible est accusee dans la vue",
              "ILLISIBLE" in corps_bdd and "Sources illisibles : aucune" not in corps_bdd)

    # 7. UNE MESURE VIDE EST DITE, PAS PASSEE SOUS SILENCE.
    controler("une liste vide se dit", "0 BDD mesuree(s)" in rendre_matrice([], []))

    # 8. LA CARTE EST PRESENTE ET SON TYPE EST DU VOCABULAIRE FERME.
    for type_carte, _f, _d in (("analyse", None, None), ("index", None, None)):
        entete = _carte(type_carte, "T", "D")
        controler("la carte porte le type " + type_carte,
                  "type: " + type_carte in entete and "appartient_a: optimus-prime" in entete)

    # 9. L INDEX NE RECOPIE AUCUNE DES DEUX VUES DEJA SERVIES : il les POINTE.
    racine_fictive = racine_de_test()
    index = rendre_index({}, racine_fictive)
    controler("l index POINTE les deux vues deja servies",
              "suivi-pilote.py" in index and "suivi-cameleon.py" in index)
    controler("l index annonce les quatre parties sans suivi",
              all(nom in index for nom, _f, _d in PARTIES))

    # 10. L INDEX DIT L AGE D UNE VUE ABSENTE, ET NE LA DECRIT PAS.
    controler("une vue absente a pour age ABSENTE, pas 0",
              "ABSENTE" in _age_de_vue(racine_fictive / "jamais" / "vu.md"))

    # 11. LE CONTRE-TEMOIN : une vue VIDE ne doit pas ressembler a une vue pleine.
    vide = rendre_espions([], [])
    pleine = rendre_espions(cobayes["espions"], [])
    controler("le contre-temoin : une vue sans mesure ne dit pas la meme chose",
              vide != pleine and "Valeur" in pleine)

    # 12. LE RENDU DES ROUTINES DIT LE MODE ET LA CADENCE.
    corps_r = rendre_routines(cobayes["routines"], [])
    controler("la vue des routines dit le mode et la cadence",
              "boucle" in corps_r and "20 s" in corps_r)

    reussis = sum(1 for _n, ok, _d in resultats if ok)
    for nom, ok, detail in resultats:
        print(("  [OK] " if ok else "  [KO] ") + nom
              + ("" if ok else " : " + str(detail)[:160]))
    print("AUTO-TEST : " + str(reussis) + "/" + str(len(resultats)) + ".")
    return 0 if reussis == len(resultats) else 1


def chemin_inexistant_du_cobaye():
    """Un chemin SUREMENT absent : un test qui lit le reel ne prouve rien."""
    return str(Path(__file__).resolve().parent / "cobaye-jamais-cree.json")


def racine_de_test():
    """La racine du parc, ou le dossier courant si la porte est copiee ailleurs."""
    return RACINE if RACINE is not None else Path.cwd()


# --- LE MAIN -------------------------------------------------------------------

def mesurer(racine):
    """Les quatre parties, mesurees. Rend (mesures, echecs)."""
    mesures = {}
    echecs = []
    lignes, rattrapages = partie_matrice(racine / "matrice" / "data")
    mesures["matrice"] = lignes
    echecs += [(nom + " (matrice)") for nom in rattrapages]
    lignes, rattrapages = partie_routines(racine / "matrice" / "routines" / "vie" / "planning.json", racine)
    mesures["routines"] = lignes
    echecs += rattrapages
    lignes, rattrapages = partie_espions(racine / "_operateur" / "optimus-prime" / "espions"
                                         / "registre" / "registre.json")
    mesures["espions"] = lignes
    echecs += rattrapages
    lignes, rattrapages = partie_outils(racine / "matrice" / "data" / "registre-outils.json")
    mesures["outils"] = lignes
    echecs += rattrapages
    return mesures, echecs


def main(argv=None):
    analyseur = argparse.ArgumentParser(description="Les six parties maitresses (MO-565).")
    analyseur.add_argument("--json", action="store_true",
                            help="les mesures, sans ecrire")
    analyseur.add_argument("--partie", default="",
                            help="une seule partie (matrice, routines, espions, outils, index)")
    analyseur.add_argument("--auto-test", action="store_true",
                            help="eprouve les extracteurs")
    arguments = analyseur.parse_args(argv)
    if RACINE is None:
        print(RACINE_INTROUVABLE)
        return 2
    if arguments.auto_test:
        return auto_test()
    racine = RACINE
    mesures, echecs = mesurer(racine)
    rendus = {
        "matrice": rendre_matrice,
        "routines": rendre_routines,
        "espions": rendre_espions,
        "outils": rendre_outils,
    }
    if arguments.json:
        print(json.dumps({"mesures": mesures, "sources_illisibles": echecs},
                         ensure_ascii=True, indent=2, sort_keys=True))
        return 1 if echecs else 0
    dossier = racine / "_operateur" / "optimus-prime" / "suivi-parties"
    dossier.mkdir(parents=True, exist_ok=True)
    cibles = ([arguments.partie] if arguments.partie else
              list(rendus) + ["index"])
    inconnues = [nom for nom in cibles if nom not in list(rendus) + ["index"]]
    if inconnues:
        print("REFUS : partie INCONNUE : " + ", ".join(inconnues)
              + " -- les quatre parties sans suivi sont "
              + ", ".join(sorted(rendus)) + ", plus l index.")
        return 2
    poses = 0
    refus = []
    for nom in cibles:
        if nom == "index":
            chemin = dossier / NOM_INDEX
            contenu = rendre_index(mesures, racine)
        else:
            chemin = dossier / dict((n, f) for n, f, _d in PARTIES)[nom]
            contenu = rendus[nom](mesures.get(nom, []), [])
        echec = ecrire_par_la_porte(chemin, contenu, racine)
        if echec:
            refus.append(echec)
        else:
            poses += 1
            print("posee : " + str(chemin.relative_to(racine)))
    for refus_ in refus:
        print("REFUS : " + refus_)
    for echec in echecs:
        print("SOURCE ILLISIBLE : " + echec)
    return 1 if (refus or echecs) else 0


if __name__ == "__main__":
    sys.exit(main())
