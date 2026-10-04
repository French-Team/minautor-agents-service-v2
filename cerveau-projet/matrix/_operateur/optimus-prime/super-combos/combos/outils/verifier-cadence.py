#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-cadence.py -- Garde : une routine tient-elle la cadence qu'elle DECLARE ?

Pourquoi (friction 28, 2026-09-14) : `veille-flux` a tourne a 6,0 s d'ecart median
contre 300 s declarees, les 09-11 (10 494 passes) et 09-12 (8 960) -- 20 219 passes
en trop, ~5,6 h de CPU, ~39 000 lignes de journal, 19 500 appels a `corriger-ascii`,
et PERSONNE ne l'a vu pendant 3 jours. Le seul temoin fut la TAILLE du journal,
constatee trois jours plus tard (MO-078). La cause n'etait pas la routine : sa
cadence etait DECLAREE dans ses constantes et PUBLIEE dans un etat court, mais
RIEN ne MESURAIT son battement reel. Ce garde est la troisieme jambe.

LE PIEGE QUE CE GARDE A PAYE, ET QUI EXPLIQUE SA FORME (meme jour). Le premier
battement a ete lu comme `(date - derniere_ecriture) / passes_absorbes` : une
MOYENNE. Or une moyenne ne decrit AUCUN intervalle reel des qu'une passe n'est
pas a l'heure (redemarrage, passe A LA DEMANDE). Mesure sur `vigie-profil`, dont
le journal PROUVE la cadence a 900 s et dont le compteur est juste (prouve :
3 -> 4 en une passe) : la MEME cadence a ete lue 450,5 s puis 600,3 s. Une
valeur fausse mais DANS la tolerance ne crie pas -- c'est le pire des temoins,
il rassure. Ce garde lit donc une SERIE d'horodatages et un ecart MEDIAN, jamais
une moyenne : un redemarrage deplace la mediane d'un cran, il ne divise plus le
resultat par deux.

CE QU'IL EXIGE, pour CHAQUE routine DECLAREE par le serveur `vie` -- la table se LIT
(`matrice/routines/vie/constants.py`), elle n'est plus recopiee ici (MO-479) :

  1. la cadence DECLAREE se lit a UN seul endroit : le fichier de constantes de la
     routine (le garde ne recopie aucune valeur, il dit OU lire --
     et il RESOUT les renvois, car `INTERVALLE_DECLARE_SECONDES = INTERVALLE_SECONDES`)
     ET la forme d APPEL posee par MO-429 (`INTERVALLE_DECLARE_SECONDES =
     cadence_planning('veille-flux')`), lue chez le moteur PARTAGE du planning
     (decision du createur D1 : le planning est la SOURCE des cadences), avec la
     CAUSE rendue quand la lecture echoue ;

  2. le BATTEMENT REEL se mesure dans une SERIE d'horodatages, selon le temoin que la
     routine DECLARE chez elle (`TEMOIN_CADENCE = (genre, fichier, clef)`) :
       - `journal` : la queue BORNEE de son journal, lue par le moteur PARTAGE
                     `rotation_journal` (jamais recopiee) ;
       - `anneau`  : l'ANNEAU DE PASSES garde dans un etat court
                     (`dernieres_passes`), ecrit par la routine avec le moteur
                     PARTAGE `data/commun/battement.py` ;
     et l'ecart est le MEDIAN de cette serie (moteur PARTAGE, jamais recopie).
     `TEMOIN_CADENCE` absent = KO (un OUBLI n'est pas un temoin) ; `= None` = la
     routine le DECLARE non mesurable, et le garde le DIT (jamais un faux vert) ;

  3. la comparaison TOLERE les ecarts normaux et ACCUSE les derives :
       - trop vite : battement < cadence / 2 (la rafale : 6 s contre 300 s) ;
       - trop lent : battement > cadence * 3 ;
       - arretee   : age de la derniere passe > cadence * 3 + marge, ET un PID
                     existe (sans PID, la routine est hors service par choix :
                     on le DIT au lieu d'accuser -- un non-controle assume) ;
       - un etat ECRIT SANS anneau de passes -> ACCUSE : le battement n'est plus
         mesurable, et un controle muet ne doit pas passer pour un controle vert ;
       - recul insuffisant -> `[--]` : la cadence DECLAREE fait foi et le garde
         DIT explicitement < ne pas attendre > (l'anneau de passes se remplit
         SEUL) -- jamais un faux vert, et jamais une invitation a patienter :
         une preuve se LIT, elle ne s'ATTEND pas (regle immuable
         `attente-ne-prouve-rien.md`, GO createur 2026-09-14).

  4. l'AUTOTEST rejoue l'incident REEL et la MESURE QUI MENSAIT (lecon L-032) :
     la rafale a 6,0 s contre 300 s doit etre ACCUSEE, l'override a 60 s aussi, un
     battement normal non ; et sur la SERIE REELLE du 14-09 (un ecrit a 06:55:28,
     des passes a 900 s, une passe A LA DEMANDE a 07:27:43) le MEDIAN doit rendre
     900 s -- l'intervalle reel -- la ou l'ancienne regle rendait 645 s, une
     valeur qui ne decrit AUCUN intervalle de la serie.

  5. la FABRIQUE est CABLEE : chaque routine a temoin `anneau` doit DECLARER
     `PASSES_GARDEES_ETAT` et `CLE_ANNEAU_PASSES` dans ses constantes et APPELER
     le moteur partage (`ajouter_passe(`) dans SA source (cherchee dans son
     domicile, jamais recopiee). Sans ce controle, on peut retirer l'anneau et
     laisser le garde afficher `[--]` pour toujours -- un controle qui ne dit
     plus rien.

CE QU'IL NE FAIT PAS : il ne touche RIEN, ne lance AUCUN processus de routine, et
ne lit que des fichiers d'etat et de journal -- en QUEUE BORNEE. Les fichiers de
service ne sont jamais modifies (un garde qui ecrit dans le service n'est plus un
garde, lecon L-040).

Usage: python verifier-cadence.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = racine introuvable.
"""

import argparse
import importlib.util
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# --- REFERENCES (aucune valeur en dur dans la logique) ----------------------
# Les DEUX moteurs PARTAGES : la queue bornee d'un journal, et le battement
# (anneau + ecart median). Charges par leur CHEMIN, jamais recopies (L-029).
MODULE_ROTATION = Path("matrice") / "data" / "commun" / "rotation_journal.py"
MODULE_BATTEMENT = Path("matrice") / "data" / "commun" / "battement.py"
# Le PLANNING est la SOURCE des cadences (decision du createur D1, MO-429) : les
# constantes d une routine ne portent plus la valeur, elles portent l APPEL
# `cadence_planning('nom')`. Le garde lit donc la cadence CHEZ LE MOTEUR PARTAGE
# quand la constante est un appel, et garde la lecture texte pour les renvois --
# meme parti que les deux autres moteurs (charge par leur CHEMIN, jamais recopie).
MODULE_PLANNING = Path("matrice") / "data" / "commun" / "planning_routines.py"
# Fenetre de lecture : PLUS DE NOMBRE ICI (MO-099). Elle vient du moteur PARTAGE,
# qui la deduit de la borne que le journal lu declare lui-meme
# (`SEUIL_OCTETS_JOURNAL` : 2 Mo veille, 8 Mo espion, 512 Ko vigies) : une queue
# plus petite que la borne declaree laisserait une rotation cacher des passes.

# Tolerances de la comparaison (nommees, jamais dispersees dans la logique).
FACTEUR_TROP_VITE = 0.5
FACTEUR_TROP_LENT = 3.0
FACTEUR_ARRET = 3.0
MARGE_ARRET_SECONDES = 60

FORMAT_HORODATAGE = "%Y-%m-%d %H:%M:%S"

# Doctrine (regle immuable `attente-ne-prouve-rien.md`, GO createur 2026-09-14) :
# un manque de recul ne se repare JAMAIS en attendant -- il se DIT. Le premier jet
# de ce garde laissait croire qu'il fallait trois passes (30 min) pour lire un
# battement : le repli est la cadence DECLAREE, et ce marqueur l'interdit.
MARQUEUR_NE_PAS_ATTENDRE = "NE PAS ATTENDRE"
# (le MOTIF d'assignation vit avec `valeurs_constantes`, plus bas : UN seul lecteur
#  de constantes -- deux motifs pour un meme fichier, c'est deux verites.)

# Fabrique de l'anneau : les DEUX noms que la source d'une routine a temoin
# `serie-etat` doit declarer et appeler. Ils sont NOMMES ici parce que le garde
# les cherche dans la source ; ils vivent, eux, dans les constantes de chaque
# routine (un seul nom par chose).
CONSTANTE_LONGUEUR_ANNEAU = "PASSES_GARDEES_ETAT"
CONSTANTE_CLEF_ANNEAU = "CLE_ANNEAU_PASSES"
APPEL_FABRIQUE_ANNEAU = "ajouter_passe("

# --- TABLE DES ROUTINES : ELLE SE LIT (MO-479) ------------------------------
# AUCUNE liste de routines ici. Le garde recopiait SIX lignes (nom, fichier de
# constantes, constante de cadence, fichier PID, temoin, source d ecriture) : la
# septieme (`verifier-liens-cartes`) n y etait pas et echappait au controle de
# cadence, une huitieme serait passee a cote, et le COMPTE etait meme fige
# (`len(ROUTINES) == 6`) -- un garde qui mesure un chiffre fige ne mesure rien.
# MO-479 : la table vient de `matrice/routines/vie/constants.py` (la meme que le
# serveur importe -- une seule verite, comme le maillon 7 du flux) et chaque champ
# se LIT chez la routine : NOM_PID, INTERVALLE_DECLARE_SECONDES, TEMOIN_CADENCE.
# Changer une routine change SON domicile ; ici, rien a changer.

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
    return bool(condition)


def charger_module(matrix, chemin_relatif, nom_module):
    """Un moteur PARTAGE, charge par son CHEMIN (jamais recopie)."""
    chemin = matrix / chemin_relatif
    if not chemin.is_file():
        return None
    specification = importlib.util.spec_from_file_location(nom_module, str(chemin))
    module = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(module)
    except Exception:  # noqa: BLE001 -- un moteur illisible est un ECHEC dit, pas un plantage
        return None
    return module


def horodate(texte):
    """datetime d'un horodatage du format unique, ou None (jamais d'exception)."""
    try:
        return datetime.strptime(str(texte), FORMAT_HORODATAGE)
    except (TypeError, ValueError):
        return None


def lire_texte(chemin):
    """Contenu d'un fichier, ou "" (un fichier illisible ne fait pas tomber un garde)."""
    try:
        return Path(chemin).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def lire_json(chemin):
    """JSON d'un fichier, ou {} (jamais d'exception dans un garde)."""
    try:
        return json.loads(Path(chemin).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


# La forme d APPEL posee par MO-429 : `INTERVALLE_DECLARE_SECONDES =
# cadence_planning('veille-flux')` (l'alias `cadence(` existe aussi -- un seul
# motif, deux noms pour la meme fonction partagee).
MOTIF_APPEL_PLANNING = re.compile(r"^(?:cadence_planning|cadence)\s*\(\s*['\"]([^'\"]+)['\"]\s*\)$")


def _cadence_du_planning(routine, moteur_planning, racine_planning):
    """(valeur, cause) : la cadence LUE dans le planning -- la source (D1).

    Un refus du planning (`PlanningIllisible`) est une CAUSE que le garde MONTRE :
    il ne dit jamais < illisible > sans raison, et il n'invente aucune valeur.
    """
    if moteur_planning is None:
        return None, "moteur du planning introuvable : " + str(MODULE_PLANNING)
    if racine_planning is None:
        return None, "racine du planning non fournie au garde"
    try:
        valeur = moteur_planning.cadence_planning(routine, racine=racine_planning)
    except Exception as erreur:  # noqa: BLE001 -- le refus du planning est une cause dite
        return None, "planning : " + str(erreur)
    if isinstance(valeur, int) and not isinstance(valeur, bool):
        return valeur, None
    return None, "planning : cadence non entiere pour " + str(routine)


def cadence_declaree(chemin, nom, moteur_planning=None, racine_planning=None):
    """(valeur, cause) : la cadence declaree dans SON fichier, deux formes resolues.

    Mesure MO-429 : DEUX formes cohabitent et les deux se lisent ici --
      `INTERVALLE_DECLARE_SECONDES = INTERVALLE_SECONDES`   (renvoi de constante) ;
      `INTERVALLE_DECLARE_SECONDES = cadence_planning('x')` (APPEL : la valeur vit
        desormais dans le PLANNING, decision D1 du createur, lue par le moteur
        partage `planning_routines`).
    Rien n'est importe du fichier lu : les modules `constants` des routines portent
    tous le meme nom (lecon L-029), un import les ferait se marcher dessus. Le
    second rendu est la CAUSE d'un echec (absente, renvoi non resolu, refus du
    planning) : un KO sans cause imposerait de relire le code (L-055).
    """
    valeurs = valeurs_constantes(chemin)
    courant = nom
    vus = set()
    while courant is not None and courant not in vus:
        vus.add(courant)
        valeur = valeurs.get(courant)
        if valeur is None:
            return None, "constante " + str(courant) + " absente de " + chemin.name
        if valeur.isdigit():
            return int(valeur), None
        appel = MOTIF_APPEL_PLANNING.match(valeur)
        if appel:
            return _cadence_du_planning(appel.group(1), moteur_planning, racine_planning)
        courant = valeur
    return None, "renvoi non resolu : " + nom


# --- SERIES D'HORODATAGES ---------------------------------------------------

def serie_journal(chemin, marqueur, moteur_rotation):
    """Horodatages d'un marqueur, depuis la QUEUE BORNEE d'un journal."""
    horodatages = []
    if not chemin.is_file() or moteur_rotation is None:
        return horodatages
    for ligne in moteur_rotation.lire_queue_journal(
        chemin, moteur_rotation.octets_queue_du_journal(chemin)
    ):
        if not ligne.strip():
            continue
        try:
            donnees = json.loads(ligne)
        except ValueError:
            continue
        if marqueur and str(donnees.get("type")) != marqueur:
            continue
        if donnees.get("date"):
            horodatages.append(str(donnees.get("date")))
    return horodatages


def serie_etat(chemin, clef):
    """(horodatages, clef_presente) : l'anneau de passes garde dans un etat court."""
    donnees = lire_json(chemin)
    return list(donnees.get(clef) or []), (clef in donnees)


# --- LA TABLE DECLAREE, CHAMP PAR CHAMP (MO-479) ----------------------------
TABLE_VIE = Path("matrice") / "routines" / "vie" / "constants.py"
# Le nom SHARED de la constante de cadence : un seul nom pour toutes les routines
# (la voix de la cadence est unique), jamais une valeur.
CONSTANTE_CADENCE = "INTERVALLE_DECLARE_SECONDES"
MOTIF_ASSIGNATION = re.compile(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*(.*)$")
MOTIF_ELEMENT_TEMOIN = re.compile(r'"([^"]*)"|([A-Za-z_][A-Za-z0-9_]*)')
GENRES_TEMOIN = ("journal", "anneau")


def sans_commentaire(valeur):
    """Le RHS d'une assignation, son commentaire hors chaine retire (ou tel quel)."""
    dans_chaine = None
    for caractere in valeur:
        if dans_chaine:
            if caractere == dans_chaine:
                dans_chaine = None
        elif caractere in ('"', "'"):
            dans_chaine = caractere
        elif caractere == "#":
            return valeur[:valeur.index(caractere)].rstrip()
    return valeur


def valeurs_constantes(chemin):
    """{nom: RHS brut} des assignations simples du fichier de constantes.

    TEXTe et jamais un import : les modules `constants` des routines portent tous le
    meme nom (L-029), un import les ferait se marcher dessus -- c'est le meme parti
    que `cadence_declaree`. Un fichier illisible rend {} (le garde le dit plus bas,
    il ne fabrique aucune valeur).
    """
    valeurs = {}
    for ligne in lire_texte(chemin).splitlines():
        resultat = MOTIF_ASSIGNATION.match(ligne)
        if resultat:
            valeurs[resultat.group(1)] = sans_commentaire(resultat.group(2).strip())
    return valeurs


def chaine_declaree(valeurs, nom, vus=None):
    """Chaine declaree, RENVOIS RESOLUS (`FOO = BAR`), ou None si absente/illisible."""
    vus = set() if vus is None else vus
    courant = nom
    while courant and courant not in vus:
        vus.add(courant)
        brut = valeurs.get(courant)
        if brut is None:
            return None
        if len(brut) >= 2 and brut[0] == brut[-1] and brut[0] in ('"', "'"):
            return brut[1:-1]
        courant = brut
    return None


def lire_temoin(valeurs):
    """(genre, fichier, clef) tels que la routine les DECLARE, ou None.

    `TEMOIN_CADENCE = ("journal", NOM_JOURNAL, "passe-debut")` : le genre est un
    LITTERAL ; le fichier et la clef sont soit un litteral, soit le NOM d'une autre
    constante du meme dossier (resolu ici -- jamais recopie). None dit une chose ou
    l'autre au garde : ABSENT ou ILLISIBLE, jamais un temoin invente.
    """
    brut = valeurs.get("TEMOIN_CADENCE")
    if not brut:
        return None
    morceaux = MOTIF_ELEMENT_TEMOIN.findall(brut)
    if len(morceaux) != 3:
        return None
    genre = morceaux[0][0] or morceaux[0][1]
    if genre not in GENRES_TEMOIN:
        return None
    pieces = []
    for litteral, nom in morceaux[1:]:
        valeur = litteral or chaine_declaree(valeurs, nom)
        if not valeur:
            return None
        pieces.append(valeur)
    return genre, pieces[0], pieces[1]


def charger_table_vie(matrix):
    """La table UNIQUE des routines, lue la ou elle vit. Rend (boucles, pid) ou None.

    `vie/constants.py` importe ses FRERES par leur nom (`constants_vigie_portes`, ...)
    : leur dossier doit etre joignable pendant le chargement, et seulement pendant lui.
    Rend None si la table est illisible -- le garde le DIT, il ne devine pas.
    """
    dossier = matrix / TABLE_VIE.parent
    commun = matrix / Path("matrice") / "data" / "commun"
    sys.path.insert(0, str(dossier))
    sys.path.insert(0, str(commun))
    try:
        module = charger_module(matrix, TABLE_VIE, "table_vie_cadence")
    finally:
        for chemine in (str(dossier), str(commun)):
            while chemine in sys.path:
                sys.path.remove(chemine)
    if module is None:
        return None
    try:
        boucles = [(str(nom), Path(chemin)) for nom, chemin in module.BOUCLES]
        pid_par_nom = dict(module.PID_PAR_NOM)
    except (AttributeError, TypeError):
        return None
    return boucles, pid_par_nom


def routines_declarees(matrix, moteur_planning=None):
    """[(nom, dossier, valeurs, nom_pid, temoin, declare)] -- la table, champ par champ.

    Rend (liste, erreur). `erreur` nomme un probleme de TABLE (illisible, vide) : le
    garde le DIT au lieu de tourner sur zero routine en croyant tout verifier. Un
    champ illisible dans UNE routine est rendu None POUR ELLE : jamais de defaut.
    La cadence se lit ensuite chez le moteur du PLANNING quand la constante est un
    appel (MO-429) -- la racine est LE dossier matrix lu, donc un cobaye fabrique
    SON planning a cote de sa table.
    """
    table = charger_table_vie(matrix)
    if table is None:
        return [], "table des routines illisible (" + str(TABLE_VIE) + ")"
    boucles, pid_par_nom = table
    if not boucles:
        return [], "table des routines VIDE : aucune boucle supervisee declaree"
    lignes = []
    for nom, dossier in boucles:
        valeurs = valeurs_constantes(dossier / "constants.py")
        cadence, cause_cadence = cadence_declaree(
            dossier / "constants.py", CONSTANTE_CADENCE, moteur_planning, matrix
        )
        lignes.append({
            "nom": nom,
            "dossier": dossier,
            "valeurs": valeurs,
            "nom_pid": chaine_declaree(valeurs, "NOM_PID") or pid_par_nom.get(nom)
                       or (nom + ".pid"),
            "temoin": lire_temoin(valeurs),
            "declare": "TEMOIN_CADENCE" in valeurs,
            "cadence": cadence,
            "cause_cadence": cause_cadence,
        })
    return lignes, None


def source_appelle_fabrique(dossier):
    """True si la source de la routine APPELE la fabrique partagee (hors commentaire).

    La source n'est recopiee nulle part : elle se cherche dans LE DOMICILE de la
    routine (`tour/`, `passe/`, ...), hors de son fichier de constantes qui DECLARE.
    """
    for chemin in sorted(Path(dossier).rglob("*.py")):
        if "__pycache__" in chemin.parts or ".bak." in chemin.name:
            continue
        for ligne in lire_texte(chemin).splitlines():
            if APPEL_FABRIQUE_ANNEAU in ligne and not ligne.lstrip().startswith("#"):
                return True
    return False


def classement(routines):
    """Les QUATRE familles de routines, selon ce que leur temoin DIT (MO-479).

    Meme regle, au meme endroit, pour le controle et pour son autotest : un garde
    dont la specification vit dans deux fichiers se contredit un jour.
      mesures         : temoin lisible -> le battement se mesure ;
      non_mesurables  : `TEMOIN_CADENCE = None` -> la routine le DECLARE ;
      absentes        : AUCUNE declaration -> un OUBLI (ecart) ;
      illisibles      : declaration presente mais illisible (ecart).
    """
    mesures, non_mesurables, absentes, illisibles = [], [], [], []
    for ligne in routines:
        brut = ligne["valeurs"].get("TEMOIN_CADENCE")
        if ligne["temoin"] is not None:
            mesures.append(ligne["nom"])
        elif brut is None:
            absentes.append(ligne["nom"])
        elif brut == "None":
            non_mesurables.append(ligne["nom"])
        else:
            illisibles.append(ligne["nom"])
    return {"mesures": mesures, "non_mesurables": non_mesurables,
            "absentes": absentes, "illisibles": illisibles}


def controler_table_evolute(matrix, moteur_planning=None):
    """La table du garde doit SUIVRE ce que la Matrice DECLARE (MO-479).

    Un cobaye fabrique une petite Matrice (deux routines) puis en AJOUTE une
    troisieme : `routines_declarees` doit la rendre SANS qu'on touche au garde --
    c'est la preuve qu'aucune liste n'est figee dedans. Puis on eprouve les REFUS :
    un temoin ILLISIBLE et une routine SANS temoin doivent etre DITS. Et MO-429 :
    la constante qui APPELLE le planning doit rendre la cadence du planning du
    cobaye (preuve que la lecture se fait chez le moteur partage), et une routine
    absente du planning doit rendre une CAUSE nommee (jamais un KO muet).
    """
    fabrique = charger_module(matrix, Path("matrice") / "data" / "commun"
                              / "cobayes_jetables.py", "cobayes_cadence")
    if fabrique is None:
        controler("table-evolutive", False, "fabrique de cobayes illisible (zone partagee)")
        return ["fabrique de cobayes illisible"]

    residus = []
    essais = []

    def ecrire_table(noms):
        vie = zone / "matrice" / "routines" / "vie"
        vie.mkdir(parents=True, exist_ok=True)
        lignes = [repr((nom, str(zone / "matrice" / "routines" / nom))) for nom in noms]
        (vie / "constants.py").write_text(
            "BOUCLES = (\n    " + ",\n    ".join(lignes) + ",\n)\nPID_PAR_NOM = {}\n",
            encoding="utf-8")

    def ecrire_routine(nom, temoin, cadence="300"):
        dossier = zone / "matrice" / "routines" / nom
        dossier.mkdir(parents=True, exist_ok=True)
        texte = ('NOM_PID = "' + nom + '.pid"\nINTERVALLE_DECLARE_SECONDES = ' + cadence + '\n'
                 'NOM_ETAT = "' + nom + '-etat.json"\nCLE_ANNEAU_PASSES = "dernieres_passes"\n')
        if temoin is not None:
            texte += "TEMOIN_CADENCE = " + temoin + "\n"
        (dossier / "constants.py").write_text(texte, encoding="utf-8")

    def ecrire_planning(paires):
        """Un planning COMPLETE, a cote de la table du cobaye (meme forme que le reel)."""
        entrees = [
            {"nom": nom, "cadence_secondes": cadence, "mode": "passe",
             "decalage_initial_secondes": 0, "priorite": 10,
             "tolerance_cadences": 3, "commande_passe": ["python3", "cobaye.py"]}
            for nom, cadence in paires
        ]
        vie = zone / "matrice" / "routines" / "vie"
        vie.mkdir(parents=True, exist_ok=True)
        (vie / "planning.json").write_text(
            json.dumps({"routines": entrees}, indent=2), encoding="utf-8")

    with fabrique.fixtures("cobaye-cadence-", residus) as zone:
        ecrire_routine("cobaye-a", '("anneau", NOM_ETAT, CLE_ANNEAU_PASSES)')
        ecrire_routine("cobaye-b", '("journal", "cobaye-b-log.jsonl", "passe")')
        ecrire_table(("cobaye-a", "cobaye-b"))
        lignes, erreur = routines_declarees(zone, moteur_planning)
        noms = sorted(l["nom"] for l in lignes)
        essais.append(("LIT sa table de cobaye (2 routines)",
                       ["cobaye-a", "cobaye-b"], noms,
                       erreur is None and noms == ["cobaye-a", "cobaye-b"]))

        # EVOLUTIVITE : la troisieme n'existe que dans la TABLE.
        ecrire_routine("cobaye-c", '("journal", "cobaye-c-log.jsonl", "passe")')
        ecrire_table(("cobaye-a", "cobaye-b", "cobaye-c"))
        lignes, erreur = routines_declarees(zone, moteur_planning)
        noms = sorted(l["nom"] for l in lignes)
        essais.append(("SUIT la table : la routine AJOUTEE est rendue sans toucher au garde",
                       ["cobaye-a", "cobaye-b", "cobaye-c"], noms,
                       erreur is None and noms == ["cobaye-a", "cobaye-b", "cobaye-c"]))

        # REFUS : un temoin illisible et un temoin absent doivent etre DITS.
        ecrire_routine("cobaye-d", '("musique", "pas-un-temoin")')
        ecrire_routine("cobaye-e", None)
        ecrire_table(("cobaye-a", "cobaye-b", "cobaye-c", "cobaye-d", "cobaye-e"))
        lignes, erreur = routines_declarees(zone, moteur_planning)
        mots = classement(lignes)
        essais.append(("DIT le temoin ILLISIBLE (genre inconnu) et le temoin ABSENT",
                       ["cobaye-d"], sorted(mots["illisibles"]),
                       mots["illisibles"] == ["cobaye-d"] and mots["absentes"] == ["cobaye-e"]))

        # LA CADENCE VIENT DU PLANNING (MO-429, decision D1 du createur) : la
        # constante n'est plus un nombre, c'est un APPEL -- le garde le resout
        # chez le moteur partage SANS qu'on ait touche a son code.
        ecrire_planning((("cobaye-a", 450), ("cobaye-b", 600)))
        ecrire_routine("cobaye-a", '("anneau", NOM_ETAT, CLE_ANNEAU_PASSES)',
                       "cadence_planning('cobaye-a')")
        ecrire_routine("cobaye-b", '("journal", "cobaye-b-log.jsonl", "passe")',
                       "cadence_planning('cobaye-b')")
        ecrire_table(("cobaye-a", "cobaye-b"))
        lignes, erreur = routines_declarees(zone, moteur_planning)
        par_nom = {ligne["nom"]: ligne["cadence"] for ligne in lignes}
        essais.append(("RESOUT l APPEL cadence_planning : la cadence se lit dans le PLANNING",
                       {"cobaye-a": 450, "cobaye-b": 600}, par_nom,
                       erreur is None and par_nom.get("cobaye-a") == 450
                       and par_nom.get("cobaye-b") == 600))

        # REFUS NOMME (L-055) : une routine absente du planning doit rendre sa
        # CAUSE -- un KO sans raison imposerait de relire le code.
        ecrire_routine("cobaye-f", '("journal", "cobaye-f-log.jsonl", "passe")',
                       "cadence_planning('cobaye-absente')")
        ecrire_table(("cobaye-f",))
        lignes, erreur = routines_declarees(zone, moteur_planning)
        cause = (lignes[0].get("cause_cadence") or "") if lignes else ""
        essais.append(("DIT la CAUSE d'une cadence prise dans un planning sans cette routine",
                       True, cause,
                       erreur is None and len(lignes) == 1
                       and lignes[0]["cadence"] is None and "absente" in cause))

    for libelle, attendu, obtenu, gagne in essais:
        print(("[OK] " if gagne else "[KO] ") + "table-evolutive : " + libelle
              + " -- attendu " + str(attendu) + ", obtenu " + str(obtenu))
    echecs = [l for l, _, _, g in essais if not g]
    if residus:
        echecs.append("residus de cobaye : " + ", ".join(residus))
        print("[KO] table-evolutive : RESIDUS de cobaye NON retires : " + ", ".join(residus))
    if not echecs and not residus:
        return []
    return ["table-evolutive : " + str(echecs)]


# --- DECISION (PURE) --------------------------------------------------------

def juger(cadence, battement, age, pid_vivant):
    """(etat, motif) : DECISION PURE -- aucune horloge, aucun disque, aucun import.

    `etat` vaut "OK", "KO" ou "--" (non-controle ASSUME, jamais un faux vert).
    """
    if cadence is None:
        return "--", "cadence declaree illisible"
    if age is not None and not pid_vivant:
        return "--", "sans PID : routine hors service (non controle)"
    if age is not None and age > cadence * FACTEUR_ARRET + MARGE_ARRET_SECONDES:
        return "KO", ("arretee : derniere passe il y a " + str(int(age)) + " s"
                      + " (cadence declaree " + str(cadence) + " s)")
    if battement is None:
        return "--", ("recul insuffisant pour mesurer un battement : la cadence"
                      " DECLAREE (" + str(cadence) + " s) fait foi -- "
                      + MARQUEUR_NE_PAS_ATTENDRE + ", cet anneau se remplit SEUL")
    if battement < cadence * FACTEUR_TROP_VITE:
        return "KO", ("trop vite : " + str(round(battement, 1)) + " s de battement"
                      + " pour " + str(cadence) + " s declarees")
    if battement > cadence * FACTEUR_TROP_LENT:
        return "KO", ("trop lent : " + str(round(battement, 1)) + " s de battement"
                      + " pour " + str(cadence) + " s declarees")
    return "OK", (str(round(battement, 1)) + " s de battement pour "
                  + str(cadence) + " s declarees")


def controler_decision_pure():
    """La decision est PURE : elle se rejoue sans disque ni horloge."""
    cas = (
        ("battement conforme", juger(300, 302.0, 1.0, True), "OK"),
        ("rafale a 6 s accusees", juger(300, 6.0, 1.0, True), "KO"),
        ("override a 60 s accuse", juger(300, 60.0, 1.0, True), "KO"),
        ("trop lent accuse", juger(300, 4000.0, 1.0, True), "KO"),
        ("routine arretee accuse", juger(300, None, 100000.0, True), "KO"),
        ("sans PID : non controle", juger(300, None, 100000.0, False), "--"),
        ("recul insuffisant : non controle", juger(300, None, 1.0, True), "--"),
    )
    echecs = [nom for nom, (etat, _), attendu in cas if etat != attendu]
    controler("decision-pure", not echecs,
              str(len(cas)) + " cas" + ("" if not echecs else " : ECHECS " + str(echecs)))
    return echecs


def controler_autotest():
    """L'incident REEL doit etre ACCUSE (lecon L-032) : la rafale de la friction 28."""
    rafale_veille_flux = 6.0        # ecart median mesure les 09-11 et 09-12
    override_vie = 60.0             # l'override du serveur, avant correction
    cadence_veille_flux = 300
    accusees = [valeur for valeur in (rafale_veille_flux, override_vie)
                if juger(cadence_veille_flux, valeur, 1.0, True)[0] == "KO"]
    conforme = juger(cadence_veille_flux, 301.0, 1.0, True)[0] == "OK"
    controler("autotest-rafale-reelle-accusee", len(accusees) == 2 and conforme,
              "la rafale (6,0 s) et l'override (60 s) contre 300 declarees : "
              + str(len(accusees)) + "/2 ACCUSE(s) ; un battement conforme reste OK")

    # Le manque de recul ne doit jamais se lire comme < attends trois passes >.
    etat_recul, motif_recul = juger(900, None, 1.0, True)
    recul_parle = etat_recul == "--" and MARQUEUR_NE_PAS_ATTENDRE in motif_recul
    controler("autotest-recul-ne-pas-attendre", recul_parle,
              "un recul insuffisant rend la cadence DECLAREE et DIT '"
              + MARQUEUR_NE_PAS_ATTENDRE + "' (regle immuable : une preuve se LIT)")

    echecs = [] if (len(accusees) == 2 and conforme) else ["l'autotest n'accuse pas l'incident reel"]
    if not recul_parle:
        echecs.append("un recul insuffisant n'interdit pas explicitement d'attendre")
    return echecs


def controler_battement(moteur_battement):
    """Le MEDIAN doit resister a ce qui a fait mentir la MOYENNE (L-032).

    On rejoue la SERIE REELLE du 2026-09-14 sur `vigie-profil` : un ecrit a
    06:55:28 (passe notable), des passes a 900 s (07:10:29, 07:25:29), puis une
    passe A LA DEMANDE a 07:27:43 -- l'intervalle irregulier qui a fait dire 450,5
    s puis 600,3 s a l'ancienne regle `(dernier - premier) / passes_absorbes`.
    """
    if moteur_battement is None:
        controler("autotest-mediane-robuste", False,
                  "moteur PARTAGE introuvable : " + str(MODULE_BATTEMENT))
        return ["moteur de battement introuvable"]
    serie = ("2026-09-14 06:55:28", "2026-09-14 07:10:29",
             "2026-09-14 07:25:29", "2026-09-14 07:27:43")
    median, _ = moteur_battement.battement_median(serie, FORMAT_HORODATAGE)
    debut = horodate(serie[0])
    fin = horodate(serie[-1])
    ancienne = (fin - debut).total_seconds() / (len(serie) - 1)
    controler("autotest-mediane-robuste",
              median == 900 and abs(ancienne - 645) < 1,
              "MEME serie : mediane " + str(median) + " s (un intervalle REEL de la serie)"
              " contre ancienne regle " + str(round(ancienne, 1)) + " s (qui ne decrit"
              " AUCUN intervalle de la serie)")

    suite = moteur_battement.ajouter_passe([], "2026-09-14 00:00:00", 3)
    for rang in range(1, 5):
        suite = moteur_battement.ajouter_passe(suite, "2026-09-14 00:0" + str(rang) + ":00", 3)
    borne = len(suite) == 3 and suite[-1] == "2026-09-14 00:04:00"
    controler("autotest-anneau-borne", borne,
              "5 ajouts avec une longueur de 3 : la suite en garde " + str(len(suite))
              + " (un etat ne grandit pas)")

    peu = moteur_battement.battement_median(("2026-09-14 00:00:00",), FORMAT_HORODATAGE)
    controler("autotest-recul-dit", peu[0] is None,
              "un seul horodatage : aucun ecart median rendu (le manque de recul se DIT)")

    if median == 900 and abs(ancienne - 645) < 1 and borne and peu[0] is None:
        return []
    return ["le battement en mediane ne se comporte pas comme exige"]


def controler_fabrique(routines):
    """Chaque routine a temoin `anneau` doit DECLARER et APPELER la fabrique.

    Sans ce controle, on peut retirer l'anneau de passes : le garde afficherait
    alors `[--]` pour toujours, et un controle qui ne dit plus rien passe pour un
    controle vert. La SOURCE qui ecrit l'anneau n'est recopiee NULLE PART : elle se
    cherche dans LE DOMICILE de la routine (MO-479), hors de son fichier de
    constantes qui DECLARE.
    """
    echecs = []
    for ligne in routines:
        if ligne["temoin"] is None or ligne["temoin"][0] != "anneau":
            continue
        nom, valeurs, dossier = ligne["nom"], ligne["valeurs"], ligne["dossier"]
        manquants = [constante for constante in (CONSTANTE_LONGUEUR_ANNEAU, CONSTANTE_CLEF_ANNEAU)
                     if constante not in valeurs]
        appel = source_appelle_fabrique(dossier)
        detail = (nom + " : declare " + CONSTANTE_LONGUEUR_ANNEAU + " + " + CONSTANTE_CLEF_ANNEAU
                  + " et appelle " + APPEL_FABRIQUE_ANNEAU.rstrip("(") + " dans sa source")
        if manquants or not appel:
            echecs.append(nom)
            detail = (nom + " : ECART -- manquant " + str(manquants)
                      + (" ; " + APPEL_FABRIQUE_ANNEAU + " ABSENT de sa source" if not appel else ""))
        controler("fabrique-cablee-" + nom, not manquants and appel, detail)
    return echecs


def controler_routine(matrix, ligne, moteur_rotation, moteur_battement, maintenant):
    """Controle UNE routine : cadence declaree vs battement reel, selon SON temoin.

    Tout ce qu'il lit vient de LA ROUTINE : sa cadence, son PID, son temoin. Rien
    n'est attendu d'ici (MO-479). Trois sorties honnetes sur le temoin :
      - ABSENT       -> KO : un OUBLI n'est pas un temoin (une routine ajoutee sans
                         declaration resterait invisible : le garde doit crier) ;
      - declare None -> `[--]` : la routine DIT n'avoir aucune mesure possible ;
      - ILLISIBLE    -> KO : la declaration existe mais ne dit rien de lisible.
    """
    nom, dossier, valeurs = ligne["nom"], ligne["dossier"], ligne["valeurs"]
    chemin_constantes = dossier / "constants.py"
    cadence = ligne["cadence"]
    if cadence is None:
        cause = ligne.get("cause_cadence") or "cause inconnue"
        controler(nom, False, "cadence declaree ILLISIBLE (" + str(chemin_constantes)
                  + ", constante " + CONSTANTE_CADENCE + ") -- " + cause)
        return nom + " : cadence declaree illisible (" + cause + ")"

    brut = valeurs.get("TEMOIN_CADENCE")
    if ligne["temoin"] is None:
        if brut is None:
            controler(nom, False, "[KO] TEMOIN_CADENCE ABSENT : cette routine n'a jamais"
                      " declare comment mesurer son battement (un oubli n'est pas un temoin)")
            return nom + " : TEMOIN_CADENCE non declare"
        if brut == "None":
            controler(nom, True, "[--] TEMOIN_CADENCE = None : routine DITE non mesurable"
                      " (dite, jamais un faux vert)")
            return None
        controler(nom, False, "[KO] TEMOIN_CADENCE ILLISIBLE (" + brut[:60]
                  + ") : attendu (genre, fichier, clef)")
        return nom + " : TEMOIN_CADENCE illisible"

    genre, fichier, cle = ligne["temoin"]
    chemin_temoin = dossier / fichier
    anneau_absent = False
    if genre == "journal":
        horodatages = serie_journal(chemin_temoin, cle, moteur_rotation)
        source = "journal " + fichier + " (" + cle + ")"
    else:
        horodatages, clef_presente = serie_etat(chemin_temoin, cle)
        source = "etat " + fichier + " (" + cle + ")"
        # Un etat ECRIT mais SANS anneau : la routine tourne et la mesure a
        # disparu. C'est un ECART, pas un manque de recul -- le dire, sinon le
        # garde afficherait `[--]` pour toujours.
        anneau_absent = bool(chemin_temoin.is_file()) and not clef_presente

    if anneau_absent:
        controler(nom, False, "[KO] etat ecrit SANS anneau de passes : le battement"
                  " n'est plus mesurable (la serie est le seul temoin)")
        return nom + " : anneau de passes absent de " + fichier

    battement, dernier = (moteur_battement.battement_median(horodatages, FORMAT_HORODATAGE)
                          if moteur_battement is not None else (None, None))
    pid_vivant = (dossier / ligne["nom_pid"]).is_file()
    age = (maintenant - dernier).total_seconds() if dernier is not None else None
    etat, motif = juger(cadence, battement, age, pid_vivant)

    controler(nom, etat != "KO",
              "[" + etat + "] " + motif + " [declaree " + str(cadence) + " s, lue dans "
              + chemin_constantes.name + " ; battement lu dans " + source + "]")
    return None if etat != "KO" else nom + " : " + motif


def controler_vivante_au_ring(routines):
    """LE CAS DE LA MISSION (MO-456) : une vigie VIVANTE au JOURNAL FIGE.

    Mesure du 2026-09-24 : la vigie-portes tournait (journal 19:11, 19:26, 19:41)
    mais son anneau s arretait a 18:56, et le garde accusait < arretee depuis 3299 s >.
    Deux choses ont change depuis, et le cobaye les MESURE (L-032) :
      - la routine declare SON temoin -- l ANNEAU des passes (un etat ecrit a
        CHAQUE passe), pas le journal, qui ne recoit que ce qui a CHANGE ;
      - une passe EN RETARD ecrit quand meme son anneau : la routine VIVANTE
        reste fraiche.
    Deux sens : un ANNEAU FRAIS epargne (le cas de la mission) ; un ANNEAU EN
    RETARD accuse encore -- sans ce contre-temoin, un garde qui ne crie jamais
    passerait pour un garde.
    """
    echecs = []
    cadence = 900
    # 1. ANNEAU FRAIS (derniere passe il y a 60 s) : la routine VIVANTE est
    #    EPARGNEE, meme si son journal est FIGE -- c est exactement le cas du
    #    2026-09-24, ou l accusation etait FAUSSE.
    etat_frais, _ = juger(cadence, 900.0, 60.0, True)
    controler("vivante-anneau-frais", etat_frais == "OK",
              "anneau frais (60 s) : etat " + etat_frais + " -- un journal FIGE"
              " n accuse plus (mesure MO-456)")
    if etat_frais != "OK":
        echecs.append("vivante-anneau-frais")
    # 2. CONTRE-TEMOIN : le MEME cas AVEC un anneau EN RETARD (3299 s, la mesure
    #    exacte de la mission) est ENCORE accuse -- le garde MORD toujours.
    etat_retard, motif_retard = juger(cadence, None, 3299.0, True)
    controler("contre-temoin-anneau-en-retard",
              etat_retard == "KO" and "arretee" in motif_retard,
              "anneau en retard (3299 s, la mesure MO-456) : etat " + etat_retard)
    if etat_retard != "KO":
        echecs.append("contre-temoin-anneau-en-retard")
    # 3. LA DECLARATION REELLE : la vigie-portes lit son ANNEAU (genre "anneau"),
    #    donc un journal fige n est PAS la reference de sa cadence (M-076 : le
    #    temoin est declare CHEZ la routine). Sans ce controle, la regle pourrait
    #    se perdre sans que rien ne le dise.
    ligne = next((l for l in routines if l["nom"] == "vigie-portes"), None)
    temoin = ligne["temoin"] if ligne else None
    controler("vigie-portes-lit-son-anneau", bool(temoin) and temoin[0] == "anneau",
              "TEMOIN_CADENCE de vigie-portes : " + repr(temoin)
              + " (genre attendu : anneau)")
    if not (temoin and temoin[0] == "anneau"):
        echecs.append("vigie-portes-lit-son-anneau")
    return echecs


def main():
    parser = argparse.ArgumentParser(description="Garde : une routine tient sa cadence declaree")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = parser.parse_args()

    matrix = trouver_matrix(Path(arguments.racine).resolve())
    if matrix is None:
        print("Dossier matrix/ introuvable sous " + str(arguments.racine))
        return 2

    ecarts = []
    print("VERIFIER CADENCE -- le battement REEL contre la cadence DECLAREE")
    print("-- la decision (pure) --")
    ecarts += controler_decision_pure()
    ecarts += controler_autotest()

    moteur_rotation = charger_module(matrix, MODULE_ROTATION, "moteur_lecture_cadence")
    controler("moteur-lecture-bornee", moteur_rotation is not None,
              "moteur partage charge par son chemin (lecture bornee de la queue)"
              if moteur_rotation is not None else "moteur PARTAGE introuvable : " + str(MODULE_ROTATION))
    if moteur_rotation is None:
        ecarts.append("moteur de lecture bornee introuvable")

    moteur_battement = charger_module(matrix, MODULE_BATTEMENT, "moteur_battement_cadence")
    controler("moteur-battement", moteur_battement is not None,
              "moteur partage charge par son chemin (anneau borne + ecart MEDIAN)"
              if moteur_battement is not None else "moteur PARTAGE introuvable : " + str(MODULE_BATTEMENT))
    if moteur_battement is None:
        ecarts.append("moteur de battement introuvable")

    # Le PLANNING est la source des cadences (D1, MO-429) : sans son moteur, la
    # forme d appel ne se resout plus -- le garde le DIT une fois, puis NOMME la
    # cause sur chaque routine concernee (jamais un KO muet).
    moteur_planning = charger_module(matrix, MODULE_PLANNING, "moteur_planning_cadence")
    controler("moteur-planning", moteur_planning is not None,
              "moteur partage charge par son chemin (la cadence se lit dans le PLANNING, D1)"
              if moteur_planning is not None else "moteur PARTAGE introuvable : " + str(MODULE_PLANNING))
    if moteur_planning is None:
        ecarts.append("moteur du planning introuvable")

    print("-- le battement (le median resiste a ce qui a fait mentir la moyenne) --")
    ecarts += controler_battement(moteur_battement)

    # La table se LIT : le compte ne vient plus d'un nombre fige (MO-479).
    print("-- la table DECLAREE (elle se lit, MO-479) --")
    routines, erreur_table = routines_declarees(matrix, moteur_planning)
    if erreur_table:
        controler("table-declaree", False, erreur_table)
        ecarts.append(erreur_table)
    else:
        mots = classement(routines)
        # Ce que la table ne couvre pas est DIT (jamais un vert silencieux), et un
        # OUBLI de declaration est un ECART : une routine ajoutee sans temoin ne
        # doit pas rester invisible. La meme regle sert son autotest (classement).
        controler("table-declaree", not mots["absentes"] and not mots["illisibles"],
                  str(len(routines)) + " routine(s) declaree(s) par le serveur vie -- "
                  + str(len(mots["mesures"])) + " mesuree(s)"
                  + (" ; TEMOIN ABSENT " + ",".join(mots["absentes"])
                     if mots["absentes"] else "")
                  + (" ; TEMOIN ILLISIBLE " + ",".join(mots["illisibles"])
                     if mots["illisibles"] else "")
                  + (" ; non mesurable (declaree None) " + ",".join(mots["non_mesurables"])
                     if mots["non_mesurables"] else ""))
        if mots["absentes"]:
            ecarts.append("TEMOIN_CADENCE absent de : " + ",".join(mots["absentes"]))
        if mots["illisibles"]:
            ecarts.append("TEMOIN_CADENCE illisible chez : " + ",".join(mots["illisibles"]))
        # L'AUTOTEST de la table se joue A CHAQUE execution : un garde que personne
        # ne joue n'en est pas un (MO-479).
        ecarts += controler_table_evolute(matrix, moteur_planning)
    # LE CAS DE LA MISSION (MO-456) : la routine VIVANTE au journal FIGE ne doit
    # pas etre accusee. Le cobaye se joue A CHAQUE execution, comme l autotest
    # de la table (un garde que personne ne joue n en est pas un).
    ecarts += controler_vivante_au_ring(routines)

    print("-- la fabrique de l'anneau est-elle cablee --")
    if routines:
        ecarts += controler_fabrique(routines)

    print("-- le battement des routines --")
    maintenant = datetime.now()
    for ligne in routines:
        ecart = controler_routine(matrix, ligne, moteur_rotation, moteur_battement, maintenant)
        if ecart:
            ecarts.append(ecart)

    if ecarts:
        print("\nVERDICT KO : une routine ne tient pas la cadence qu'elle declare"
              " (voir les ecarts nommes).")
        return 1
    print("\nVERDICT OK : chaque routine tient la cadence qu'elle declare"
          " (ou son manque de recul est DIT).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
