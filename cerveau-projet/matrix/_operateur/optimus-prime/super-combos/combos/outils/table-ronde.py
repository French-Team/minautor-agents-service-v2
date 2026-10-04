#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
table-ronde -- LE POST-TRAITEMENT : MESURER, SANS LIRE L AUTO-NOTE.

LE PROTOCOLE, ET CE QU IL TIENT.
L agent s auto-evalue LIBREMENT et depose sa note. Ensuite, et ensuite
seulement, on mesure. Le mesureur ne LIT PAS l auto-note : il ne la cherche
meme pas. Il rend un etat, pas un jugement -- et la comparaison des deux est
faite APRES, par un tiers qui voit les deux. Un mesureur qui lit la note
corrige sa note en meme temps qu il la verifie : il ne verifie plus rien.

ON BLAME, ON NE PENALISE PAS. Aucun des chiffres de ce rapport ne retire un
point, ne ferme une mission et ne banni un outil. Le blame sert a NOMMER ce qui
n a pas ete vu, pour que le meme chose ne se repete pas -- un rappel a l
ordre, pas une sanction. C est pourquoi la liste des blames est FERMEE et
DECLAREE : un rapport qui inventerait une categorie de reproche pourrait
reprocher n importe quoi.

LES SIX CHAMPS.
1. `missions_jouees` : les missions du round, et leur statut.
2. `portes_jouees` : les portes reellement appelees (la trace des usages).
3. `livrables_introuvables` : LE CHAMP AJOUTE PAR R1. Une mission close dont le
   bilan nomme des fichiers qui n existent plus sur le disque. C est le defaut
   de fond qu hier a produit : la trace dit `terminee`, le travail n existe
   plus, et la file ne voyait rien.
   `livrables_renommes` : ET LE TROISIEME MOT, QUE LA LECTURE SEULE NE VOIT
   PAS. Une mission ancienne nomme `combo-activites/main.py`, et le fichier
   s appelle desormais `c-006-activites/main.py` : le journal de MO-043 dit
   lui-meme que la migration a renomme sept combos. Un fichier renomme n est
   pas un fichier perdu, et un accuse qui ne sait pas faire la difference
   transforme une migrations posee en disparition. On ne devine pas le
   renommage -- on le cherche par NOM DE BASE, dans tout le parc, et ce
   n est trouve que si le nom est RARE dans le parc -- une seule occurrence.
   Retrouver un `main.py` ailleurs ne prouve pas que CE fichier-la a ete
   renomme, puisque le parc en compte 25 : au-dela d une occurrence, on ne
   sait pas, et le champ le dit au lieu de trancher par defaut.
   `livrables_indeterminables` : LA REGLE QUI EMPECHE CE CHAMP DE MENTIR. La
   trace des bilans nomme DEUX sortes de fichiers, melangees sans les
   distinguer : des livrables DURS, dont le chemin part de la racine, et des
   brouillons de zone jetable, cites par leur SEUL NOM parce qu ils ont ete
   ecrits dans le dossier de travail puis purges -- c etait CONVENU, pas un
   oubli. Resoudre un nom nu depuis la racine accuse donc 201 bilans
   parfaitement effaces. Ce que le champ ne sait pas resoudre, il ne
   l accuse pas : il le range en `indeterminable`, avec le motif, plutot que
   de le compter comme disparu. Un accuse a tort est pire qu un silence, car
   il entraine a reparer ce qui n est pas casse.
4. `nonsens_publies` : trois familles de defauts qu un lecteur ne voit pas --
   une condition qui passe toujours, une boucle vide, un format de date
   litteral. Ces trois-la sont mesurees sur l ARBRE SYNTAXTIQUE, jamais sur le
   texte : une expression qui se lit `f(x) == f(x)` n est PAS une tautologie
   alors qu elle a exactement la meme forme qu une qui l est. Un detecteur de
   forme accuse donc les sondes de determinisme, et le contre-temoin de
   l auto-test le prouve sur un cas reel.
5. `etat` : SAIN ou A_REPRENDRE.
6. `blames` : la liste fermee des trois familles, avec POURQUOI elle existe et
   ce qu elle a trouve. C est une liste nommee, pas un calcul, pas un score.

LA FILE ET SON ARCHIVE, ET LA LEON QUI VA AVEC.
Une premiere version lisait la seule file active et laissait la garde
`enchainement` la prendre en faute : elle lisait 51 missions quand
l archive en contient 487 de terminees. C est exact -- on ne mesure pas ce
qu on ne regarde pas. La file ET son archive sont donc lues, et le rapport
REND COMBIEN il a lu de chaque cote, pour qu on puisse verifier qu il a
regarde les deux.

CE QUE CE RAPPORT NE FAIT PAS.
- Il ne note pas l agent, et ne pretendra jamais le faire : il mesure des
  fichiers et des journaux.
- Il ne lit pas l auto-note, et ne connait pas son chemin (une porte qui
  receive le chemin de la note est une porte qui finira par la lire).
- Il ne corrige rien : un mesureur qui repare ne peut plus rien mesurer.
- Il ne recompte pas : quand il mesure 11 Mo de trace, il rend le nombre
  d evenements lus avec les noms d outil, pour qu un zero soit credible.
- Il n accuse pas un brouillon purge PAR CONVENTION : la zone jetable est
  videe a chaque fin de round, et un fichier qui y a vecu doit manquer.

Usage:
  python table-ronde.py                      (la mesure, sur le round courant)
  python table-ronde.py --mission MO-xxx     (une mission isolee)
  python table-ronde.py --sortie <fichier>   (pose la mesure dans un fichier)
  python table-ronde.py --auto-test          (les six champs sur faits fabriques)
  code 0 = SAIN ; 1 = A_REPRENDRE ; 2 = source de mesure introuvable.
"""
import argparse
import ast
import json
import sys
from datetime import datetime
from pathlib import Path

NL = chr(10)
# Les portes de NON-REGRESSION ne sont pas mesurees ici : ce sont des
# instruments, pas du travail. Mesurer l instrument avec l instrument serait
# circulaire.
DOMAINES_MESURES = ("matrice", "_operateur", "user-demandes")

RACINE = None
_courant = Path(__file__).resolve().parent
for _essai in range(30):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        RACINE = _courant
        break
    _courant = _courant.parent
RACINE_INTROUVABLE = ("Racine matrix/ introuvable en remontant depuis "
                      + str(Path(__file__).resolve().parent))

FILE_MISSIONS = "_operateur/optimus-prime/pilote/file-missions-optimus.json"
FILE_MISSIONS_ARCHIVE = ("_operateur/optimus-prime/pilote/"
                         "file-missions-optimus-archive.json")

# --- LES TROIS FAMILLES DE NONSENS, declarees, pas devinees ---------------------
# Une liste FINIE et nommee, chacune avec le POURQUOI de son existence. Elle
# n est ni un score, ni une note, ni un reproche invente au fil de la mesure.
FAMILLES_NONSENS = ("CONDITION TOUJOURS VRAIE", "BOUCLE VIDE",
                    "FORMAT DE DATE LITTERAL")

POURQUOI_NONSENS = {
    "CONDITION TOUJOURS VRAIE":
        "un `or True`, un `and False` ou une comparaison d un operande pur a "
        "lui-meme : la condition ne depend plus de ses entrees, donc le "
        "controle passe toujours et lit le fichier pour rien",
    "BOUCLE VIDE":
        "un corps de boucle qui ne contient que `pass` : la boucle existe "
        "pour une raison qu elle ne dit plus",
    "FORMAT DE DATE LITTERAL":
        "un `strftime` ou `strptime` dont le format ne contient aucun `%` "
        "(constante ou nom resolu) : il rend la chaine qu on lui a donnee, "
        "donc une vue publie une date fausse",
}

# Un operande PUR ne peut pas changer de valeur entre deux lectures : c'est ce
# qui distingue une tautologie d'une sonde de determinisme.
OPERANDES_PURS = (ast.Constant, ast.Name, ast.Attribute)
# On compare le DERNIER segment du nom appele : `d.strftime(...)` et
# `datetime.strftime(...)` sont le meme appel, et une liste de noms complets
# manquerait la forme la plus courante -- celle du test fabrique qui a deja
# attrape cette omission.
APPELS_DATE = ("strftime", "strptime")


def _constantes_du_module(arbre):
    """Les constantes de chaine nommees au niveau du module.

    Un format de date est presque toujours une constante nommee : sans ce
    premier passage, `strptime(TEXTE, FORMAT_DATE)` serait lu comme un format
    litteral sans `%` alors que `FORMAT_DATE` en contient. C'est ainsi qu'un
    detecteur accuse du code sain.
    """
    constantes = {}
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Assign):
            for cible in noeud.targets:
                if (isinstance(cible, ast.Name)
                        and isinstance(noeud.value, ast.Constant)
                        and isinstance(noeud.value.value, str)):
                    constantes[cible.id] = noeud.value.value
    return constantes


class _Detecteur(ast.NodeVisitor):
    """Les trois familles, sur l ARBRE, pas sur le texte."""

    def __init__(self, fichier, source, constantes):
        self.fichier = fichier
        self.lignes = source.split(NL)
        self.constantes = constantes
        self.trouves = []

    def _noter(self, famille, noeud, extrait):
        numero = getattr(noeud, "lineno", 0)
        self.trouves.append({"famille": famille, "fichier": self.fichier,
                             "ligne": numero,
                             "extrait": (self.lignes[numero - 1].strip()
                                         if 0 < numero <= len(self.lignes)
                                         else extrait)[:120]})

    def visit_BoolOp(self, noeud):
        for valeur in noeud.values:
            if isinstance(valeur, ast.Constant) and isinstance(valeur.value, bool):
                if (isinstance(noeud.op, ast.Or) and valeur.value) or \
                        (isinstance(noeud.op, ast.And) and not valeur.value):
                    self._noter("CONDITION TOUJOURS VRAIE", noeud,
                                ast.unparse(noeud))
        self.generic_visit(noeud)

    def visit_Compare(self, noeud):
        if len(noeud.ops) == 1 and isinstance(noeud.ops[0], (ast.Eq, ast.NotEq)):
            autre = noeud.comparators[0]
            if (ast.dump(noeud.left) == ast.dump(autre)
                    and isinstance(noeud.left, OPERANDES_PURS)
                    and isinstance(autre, OPERANDES_PURS)):
                self._noter("CONDITION TOUJOURS VRAIE", noeud,
                            ast.unparse(noeud))
        self.generic_visit(noeud)

    def visit_Call(self, noeud):
        nom = ast.unparse(noeud.func).split(".")[-1]
        if nom in APPELS_DATE and noeud.args:
            if nom == "strptime" and len(noeud.args) > 1:
                argument = noeud.args[1]
            else:
                argument = noeud.args[0]
            format_connu = None
            if isinstance(argument, ast.Constant) and \
                    isinstance(argument.value, str):
                format_connu = argument.value
            elif isinstance(argument, ast.Name):
                format_connu = self.constantes.get(argument.id)
            if format_connu is not None and "%" not in format_connu:
                self._noter("FORMAT DE DATE LITTERAL", noeud,
                            ast.unparse(noeud))
        self.generic_visit(noeud)


def _nonsens_dans_source(source, fichier="<fabrique>"):
    """Les nonsens d UN source, sous forme de liste (jamais un compte)."""
    try:
        arbre = ast.parse(source)
    except (SyntaxError, ValueError):
        return [], False
    detecteur = _Detecteur(fichier, source, _constantes_du_module(arbre))
    detecteur.visit(arbre)
    lignes = source.split(NL)
    for noeud in ast.walk(arbre):
        if isinstance(noeud, (ast.For, ast.While)) and noeud.body and \
                all(isinstance(corps, ast.Pass) for corps in noeud.body):
            numero = noeud.lineno
            extrait = (lignes[numero - 1].strip()
                       if 0 < numero <= len(lignes)
                       else ast.unparse(noeud))[:120]
            detecteur.trouves.append({"famille": "BOUCLE VIDE",
                                      "fichier": fichier, "ligne": numero,
                                      "extrait": extrait})
    return detecteur.trouves, True


def _faux_publies():
    """Les nonsens du parc, avec le nombre de fichiers LUS.

    Le compte de lecture est rendu : un controle qui n a rien lu ne peut pas
    rendre un zero credible, et un fichier que l AST refuse de lire doit etre
    COMPTE comme non mesure, jamais passe pour sain.
    """
    trouves = []
    lus = 0
    illisibles = []
    for domaine in DOMAINES_MESURES:
        base = RACINE / domaine
        if not base.is_dir():
            continue
        for chemin in sorted(base.rglob("*.py")):
            if "__pycache__" in chemin.parts or ".bak." in chemin.name:
                continue
            try:
                source = chemin.read_text(encoding="utf-8", errors="replace")
            except OSError as erreur:
                illisibles.append({"fichier": str(chemin),
                                   "cause": type(erreur).__name__})
                continue
            lus += 1
            trouvees, lisible = _nonsens_dans_source(source, str(chemin))
            if not lisible:
                illisibles.append({"fichier": str(chemin),
                                   "cause": "arbre illisible"})
                continue
            trouves.extend(trouvees)
    return {"fichiers_lus": lus, "illisibles": illisibles, "trouves": trouves}


def _lire_json(chemin, defaut):
    try:
        return json.loads(chemin.read_text(encoding="utf-8")), ""
    except (OSError, ValueError) as erreur:
        return defaut, (str(chemin) + " ILLISIBLE : " + type(erreur).__name__)


def _missions_de(conteneur, missions):
    """Les missions d un conteneur, sans les retraitrees, SANS les dedoublonner.

    On ne trie pas sur l identifiant seul : deux entrees peuvent porter le meme
    identifiant avec des statuts differents, et le tri ferait passer devant la
    plus ancienne. On trie sur l identifiant PUIS sur le statut, donc c'est la
    ligne la plus consistente qui ouvre la liste.
    """
    if not isinstance(conteneur, dict):
        return []
    liste = [m for m in conteneur.get("missions", [])
             if isinstance(m, dict) and str(m.get("statut", "")) != "retiree"]
    return sorted(liste, key=lambda m: (str(m.get("id", "")),
                                        str(m.get("statut", ""))))


def _toutes_les_missions():
    """La file active ET son archive, chacune comptee.

    La garde `enchainement` exige qu un temoin lise aussi l archive de son
    conteneur : la file seule laisse 487 missions terminees hors de la mesure,
    et une mesure qui ne compte que 51 d entre elles ne sait rien du reste.
    """
    missions, lus = [], {}
    for nom in (FILE_MISSIONS, FILE_MISSIONS_ARCHIVE):
        chemin = RACINE / nom
        donnees, echec = _lire_json(chemin, None)
        if echec:
            lus[nom] = 0
            continue
        trouvees = _missions_de(donnees, missions)
        lus[nom] = len(trouvees)
        missions.extend(trouvees)
    return missions, lus


def _existe(chemin_relatif):
    return (RACINE / chemin_relatif).exists()


def _ou_donne_est_ce_nom(nom):
    """Le MEME nom de fichier RARE ailleurs dans le parc, ou RIEN.

    Sert uniquement a separer un RENOMMAGE d une DISPARITION. On compare le
    nom de base seul : c est la seule chose qui reste quand un dossier change
    de nom. On ne pretendra pas savoir OU il est alle -- le parc entier est
    parcouru.

    MAIS UN NOM COURANT NE PROUVE RIEN. Le parc compte 25 `main.py` et 18
    `README.md` : les y retrouver ne dit pas que CE fichier-la a ete renomme,
    seulement qu il existe des `main.py`. Une premiere version de ce champ ne
    faisait pas la distinction et classait 45 disparus en renommes sur la seule
    foi de ces noms passe-partout. On ne conclut au renommage que si le nom
    est RARE : une seule occurrence dans tout le parc. Sinon on ne sait pas,
    et l ignorance se dit au lieu d etre tranchee par defaut.
    """
    base = nom.rsplit("/", 1)[-1]
    if not base:
        return []
    trouve = []
    for domaine in DOMAINES_MESURES:
        racine = RACINE / domaine
        if not racine.is_dir():
            continue
        for chemin in racine.rglob(base):
            if chemin.is_file():
                trouve.append(str(chemin.relative_to(RACINE)))
    if len(trouve) != 1:
        return []
    return sorted(trouve)


# Les bases entre lesquelles un chemin de livrable peut etre resolu. Elles
# sont DECLAREES ici, et cette declaration est rendue dans le rapport : un
# rapport qui chercherait ailleurs sans le dire ne pourrait pas etre relu.
BASES_RESOLUTION = ("", "matrice", "_operateur/optimus-prime",
                    "_operateur/optimus-prime/super-combos/combos/outils",
                    "_operateur/optimus-prime/super-combos/combos",
                    "_operateur/optimus-prime/super-combos")

PREFIXES_DURABLES = ("matrice/", "_operateur/", "user-demandes/")
# Les fichiers de zone jetable sont PURGES par convention en fin de round. Un
# livrable qui y est ne peut pas etre accuse de disparaitre : c est exactement
# ce qu on lui demande.
MOTIFS_JETABLES = ("tmp-optimus/", "/tmp-optimus/")


def _resoudre(nom):
    """Ou se trouve ce nom, ou pourquoi on ne peut pas le dire.

    Trois issues, jamais une seule -- et surtout jamais `absent` par defaut :
    un nom nu (`mo-571-bilan.md`) ou un chemin sans prefixe durable
    (`espions/espion-integrite-optimus.py`) se resout parfois sous une autre
    base. Une version de ce champ qui resolvait tout depuis la racine a accuse
    217 fichiers, dont 8 qui existaient bel et bien et 201 bilans de zone
    jetable effaces expres.
    """
    if nom.startswith(PREFIXES_DURABLES):
        # Un chemin ancre sur une base durable : son absence est un fait.
        if _existe(nom):
            return "present", RACINE / nom
        if any(motif in nom for motif in MOTIFS_JETABLES):
            return "purge_par_convention", None
        return "introuvable", None
    trouve = None
    for base in BASES_RESOLUTION:
        candidat = RACINE / base / nom if base else RACINE / nom
        if candidat.exists():
            trouve = (base + "/" + nom) if base else nom
            break
    if trouve:
        return "present", trouve
    if any(motif in nom for motif in MOTIFS_JETABLES):
        return "purge_par_convention", None
    return "indeterminable", None


def _evenements_du_journal():
    """Les evenements de `suivi-optimus.jsonl`, groupees par mission."""
    journal = RACINE / "matrice" / "data" / "suivi-optimus.jsonl"
    if not journal.is_file():
        return {}, "journal de suivi INTROUVABLE : " + str(journal)
    par_mission = {}
    for ligne in journal.read_text(encoding="utf-8").splitlines():
        try:
            evenement = json.loads(ligne)
        except ValueError:
            continue
        identifiant = str(evenement.get("mission") or "")
        if identifiant:
            par_mission.setdefault(identifiant, []).append(evenement)
    return par_mission, ""


def livrables_introuvables(missions, par_mission=None):
    """LE CHAMP DE R1 : un bilan qui nomme un fichier qui n existe plus.

    On ne lit que la liste `fichiers` portee par la trace du journal, quand elle
    existe : c est la liste ecrite par la porte, donc une declaration et non
    une interpretation du bilan. Une mission sans cette liste n est pas
    accusee -- une porte muette n invente pas de piece a charge.

    Le champ accuse CE QUE LA TRACE ANCRE SUR UNE BASE DURABLE et qui n est
    pas la. Le reste est rendu a part, avec son motif : voir `_resoudre`.
    """
    if par_mission is None:
        par_mission, echec = _evenements_du_journal()
        if echec:
            return [], [{"mission": "?", "fichier": "?", "motif": echec}], []
    introuvables = []
    indetermines = []
    renommes = []
    purges = 0
    clos = [m for m in missions if m.get("statut") == "terminee"]
    for mission in clos:
        identifiant = str(mission.get("id", "?"))
        nommes = set()
        for evenement in par_mission.get(identifiant, []):
            # L ACTION DIT LA NATURE DU NOM. Mesure sur le journal entier le
            # 2026-10-04 : sur 393 evenements `purge`, 369 ne citent QUE des
            # noms sans barre oblique, et les 24 restants citent `tmp-optimus/`
            # -- AUCUN ne cite un vrai livrable durable. Ce que la purge a
            # supprime n est donc jamais un livrable, et le lire comme tel
            # produisait 2206 accuses sur des fichiers effaces PAR
            # CONVENTION. La regle tient donc sur l ACTION, qui est deja
            # dans la trace, plutot que sur un nom de fichier devine a
            # l'ecriture : aucun champ nouveau, aucun lecteur a corriger, et
            # la correction vaut aussi pour l historique.
            if str(evenement.get("action")) == "purge":
                purges += 1
                continue
            nommes.update(evenement.get("fichiers") or [])
        for nom in sorted(nommes):
            etat, _resolu = _resoudre(nom)
            if etat == "introuvable":
                ailleurs = _ou_donne_est_ce_nom(nom)
                if ailleurs:
                    renommes.append({"mission": identifiant, "fichier": nom,
                                     "existe_aussi_sous": list(ailleurs),
                                     "motif": "renommage : le nom de base "
                                              "existe ailleurs dans le parc"})
                else:
                    introuvables.append({"mission": identifiant,
                                         "fichier": nom})
            elif etat == "indeterminable":
                indetermines.append({"mission": identifiant, "fichier": nom,
                                     "motif": "chemin sans base durable, "
                                              "non resolu ni accuse"})
    return introuvables, indetermines, renommes, purges


def _piles_de(nom):
    """La trace et TOUTES ses archives, sans nom d archive devine.

    Un nom de fichier date dans le code est un nom de fichier qui aura tort
    demain : le mesureur cherchait `-archive-20261004.jsonl`, un nom qu il
    avait invente le jour ou il a ete ecrit, et il lisait donc en silence une
    trace incomplete. On cherche ce qui existe.
    """
    base = RACINE / "matrice" / "data"
    piles = [base / (nom + ".jsonl")]
    piles.extend(sorted(base.glob(nom + "-archive-*.jsonl")))
    return piles


def portes_jouees():
    """Les portes reellement APPELES, lues dans la trace des usages."""
    vues = {}
    lus = 0
    for pile in _piles_de("usages-outils-combos"):
        if not pile.is_file():
            continue
        for ligne in pile.read_text(encoding="utf-8",
                                   errors="replace").splitlines():
            try:
                evenement = json.loads(ligne)
            except ValueError:
                continue
            lus += 1
            outil = evenement.get("outil")
            if outil:
                vues[str(outil)] = vues.get(str(outil), 0) + 1
    return sorted(vues), lus


def _blames(nonsens):
    """LA LISTE, et elle est la liste : chaque famille, son pourquoi, ses cas.

    Aucune famille n est inventee ici, et aucune ne peut l etre : la liste
    vient de `FAMILLES_NONSENS`, qui est fermee a la compilation du rapport.
    """
    par_famille = {}
    for cas in nonsens:
        par_famille.setdefault(cas["famille"], []).append(
            cas["fichier"] + ":" + str(cas["ligne"]))
    blames = []
    for famille in FAMILLES_NONSENS:
        cas = par_famille.get(famille, [])
        blames.append({"famille": famille,
                       "pourquoi": POURQUOI_NONSENS[famille],
                       "trouve": len(cas), "ou": cas,
                       "ce_que_ca_dit": ("rien a corriger pour cette famille"
                                         if not cas else
                                         "a nommer, pas a sanctionner")})
    return blames


def mesurer(missions=None):
    """LES SIX CHAMPS. Aucun ne lit l auto-note -- son chemin n existe pas ici."""
    lus = {}
    if missions is None:
        missions, lus = _toutes_les_missions()
    faux = _faux_publies()
    introuvables, indetermines, renommes, purges = \
        livrables_introuvables(missions)
    jouees = [{"id": str(m.get("id", "?")), "statut": str(m.get("statut", "?")),
               "theme": str(m.get("theme", "")),
               "bilan": bool(m.get("bilan"))}
              for m in missions if str(m.get("statut", "")) != "retiree"]
    noms_portes, lus_portes = portes_jouees()
    etat = "SAIN"
    if introuvables or faux["trouves"]:
        etat = "A_REPRENDRE"
    return {
        "mesure_le": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "round": "MO-567 a MO-572",
        "missions_jouees": jouees,
        "missions_lues_par_conteneur": lus,
        "portes_jouees": noms_portes,
        "portes_appels_lus": lus_portes,
        "livrables_introuvables": introuvables,
        "livrables_renommes": renommes,
        "livrables_indeterminables": indetermines,
        "bases_de_resolution": list(BASES_RESOLUTION),
        "nonsens_publies": faux["trouves"],
        "purges_ignorees": purges,
        "nonsens_fichiers_lus": faux["fichiers_lus"],
        "nonsens_fichiers_illisibles": faux["illisibles"],
        "etat": etat,
        "blames": _blames(faux["trouves"]),
    }, ""


def main(argv=None):
    analyseur = argparse.ArgumentParser(
        description="La mesure du round, sans lire l auto-note.")
    analyseur.add_argument("--mission", default="", help="une mission isolee")
    analyseur.add_argument("--sortie", default="", help="fichier ou poser la mesure")
    analyseur.add_argument("--auto-test", action="store_true",
                           help="les six champs sur faits fabriques")
    arguments = analyseur.parse_args(argv)
    if RACINE is None:
        print(RACINE_INTROUVABLE)
        return 2
    if arguments.auto_test:
        return auto_test()
    missions = None
    if arguments.mission:
        toutes, _lus = _toutes_les_missions()
        missions = [m for m in toutes if str(m.get("id")) == arguments.mission]
        if not missions:
            print("REFUS : mission INCONNUE : " + arguments.mission)
            return 2
    rapport, echec = mesurer(missions)
    if echec:
        print("REFUS : " + echec)
        return 2
    corps = json.dumps(rapport, ensure_ascii=True, indent=2,
                       sort_keys=True) + NL
    if arguments.sortie:
        chemin = RACINE / arguments.sortie
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(corps, encoding="utf-8", newline="")
        print("mesure posee : " + str(chemin))
    else:
        print(corps, end="")
    return 0 if rapport["etat"] == "SAIN" else 1


def auto_test():
    """Les six champs sur des faits FABRIQUES, dont des contre-temoins."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append((nom, bool(condition), detail))

    # 1. LA LISTE DES BLAMES EST FERMEE, ET ELLE DIT POURQUOI.
    controler("la liste des blames est FINIE et nommee",
              set(FAMILLES_NONSENS) == {"CONDITION TOUJOURS VRAIE",
                                        "BOUCLE VIDE",
                                        "FORMAT DE DATE LITTERAL"},
              FAMILLES_NONSENS)
    controler("chaque famille de nonsens dit POURQUOI elle existe",
              all(POURQUOI_NONSENS.get(f) for f in FAMILLES_NONSENS))
    controler("le rapport rend un champ blames, pas un score",
              isinstance(_blames([]), list) and len(_blames([])) == 3)

    # 2. LA DETECTION MARCHE SUR UN CAS FABRIQUE.
    trouvees, _ = _nonsens_dans_source("x = 1 if a or True else 2" + NL + "x")
    controler("une condition toujours vraie est trouvee",
              any(c["famille"] == "CONDITION TOUJOURS VRAIE"
                  for c in trouvees), trouvees)
    vide, _ = _nonsens_dans_source("for i in range(3):" + NL + "    pass")
    controler("une boucle vide est trouvee",
              any(c["famille"] == "BOUCLE VIDE" for c in vide), vide)
    date, _ = _nonsens_dans_source("d = d.strftime(\"2026-10-04\")")
    controler("un format de date litteral est trouve",
              any(c["famille"] == "FORMAT DE DATE LITTERAL" for c in date),
              date)

    # 3. LES CONTRE-TEMOINS : ce qui a la MEME FORME mais n est PAS un defaut.
    sonde, _ = _nonsens_dans_source("d = f(x) == f(x)")
    controler("une sonde de deterministe n est PAS accusee a tort",
              not any(c["famille"] == "CONDITION TOUJOURS VRAIE"
                      for c in sonde), sonde)
    nom, _ = _nonsens_dans_source(
        "FORMAT_DATE = \"%Y-%m-%d\"" + NL + "d = t.strptime(s, FORMAT_DATE)")
    controler("un format de date en constante nommee n est PAS accuse a tort",
              not nom, nom)
    sain = "x = 1" + NL + "for i in range(3):" + NL + "    print(i)"
    trouves_sain, _ = _nonsens_dans_source(sain)
    controler("du code sain ne declenche aucun nonsens", not trouves_sain,
              trouves_sain)

    # 4. LE LIVRABLE INTROUVABLE EST ACCUSE, LE PRESENT EST EPARNE -- sur une
    #    trace FABRIQUE, pas sur le journal du jour (qui, lui, ne contient
    #    aucune mission de ce nom et n accuserait donc personne).
    trace = {"MO-000": [{"fichiers": ["matrice/data/jamais/cree/jamais.md",
                                      "matrice/data/conservation.json",
                                      "mo-000-bilan.md",
                                      "_operateur/optimus-prime/tmp-optimus/x.py"]}],
             "MO-902": [{"fichiers": []}]}
    introuvables, indetermines, renommes, _p = livrables_introuvables(
        [{"id": "MO-000", "statut": "terminee"},
         {"id": "MO-901", "statut": "terminee"},
         {"id": "MO-902", "statut": "terminee"}], trace)
    accuses = {entree["fichier"] for entree in introuvables}
    controler("un livrable absent du disque est accuse",
              "matrice/data/jamais/cree/jamais.md" in accuses, introuvables)
    controler("un livrable present n est pas accuse",
              "matrice/data/conservation.json" not in accuses, accuses)
    controler("une mission close sans livrable nomme n est pas accusee",
              all(e["mission"] != "MO-902" for e in introuvables))
    noms_ind = {e["fichier"] for e in indetermines}
    controler("un nom SANS base durable n est pas accuse, il est INDETERMINE",
              "mo-000-bilan.md" in noms_ind
              and "mo-000-bilan.md" not in accuses, indetermines)
    jetable = "_operateur/optimus-prime/tmp-optimus/x.py"
    controler("un brouillon de zone jetable purge n est accuse par personne",
              jetable not in accuses and jetable not in noms_ind,
              (accuses, noms_ind))

    # 4 bis. LA REGLE DE L ACTION : un fichier purge est un SUPPRIME, pas un
    #       livrable. C est elle qui evite les 2206 accuses de la premiere
    #       version, et elle doit rester vraie pour les purges a venir.
    trace_purge = {"MO-904": [{"action": "purge",
                               "fichiers": ["mo-904-bilan.md",
                                            "mo-904-cobaye.py"]},
                              {"action": "fin",
                               "fichiers": ["matrice/data/jamais/la.md"]}]}
    introuvables_p, ind_p, _ren_p, purges_p = livrables_introuvables(
        [{"id": "MO-904", "statut": "terminee"}], trace_purge)
    controler("les fichiers d une action purge ne sont PAS des livrables",
              not any("mo-904" in e["fichier"] for e in introuvables_p)
              and not any("mo-904" in e["fichier"] for e in ind_p),
              (introuvables_p, ind_p))
    controler("le rapport DIT combien de purges il a ecartees",
              purges_p == 1, purges_p)
    controler("une action purge ne masque PAS le livrable du meme evenement",
              "matrice/data/jamais/la.md" in
              {e["fichier"] for e in introuvables_p}, introuvables_p)

    # 4 bis. LE RENOMMAGE N EST PAS UNE DISPARITION. Le nom cite existe sous
    #      un autre dossier : c est une migration, pas une perte.
    connu = "racine.py"          # un nom qui existe : matrice/data/commun/
    renomme = "matrice/ancien-dossier/jamais-la/" + connu
    trace_renommee = {"MO-903": [{"fichiers": [renomme]}]}
    introuvables_r, _ind_r, renommes_r, _p = livrables_introuvables(
        [{"id": "MO-903", "statut": "terminee"}], trace_renommee)
    controler("un fichier RENOMME n est pas accuse de disparaitre",
              not introuvables_r and len(renommes_r) == 1, renommes_r)
    controler("le renommage DIT ou le nom existe desormais",
              bool(renommes_r) and "existe_aussi_sous" in renommes_r[0],
              renommes_r)

    # 5. LA FILE ET SON ARCHIVE SONT LUES, ET LE RAPPORT LE DIT.
    missions, lus = _toutes_les_missions()
    controler("la mesure lit la file ET son archive",
              sorted(lus) == sorted([FILE_MISSIONS, FILE_MISSIONS_ARCHIVE]),
              lus)
    controler("le rapport DIT combien il a lu dans chaque conteneur",
              all(v > 0 for v in lus.values()) and len(missions) > 0, lus)
    controler("les missions RETIREES ne sont pas mesurees",
              all(str(m.get("statut")) != "retiree" for m in missions))

    # 6. LES COMPTES DE LECTURE SONT RENDUS : un controle qui n a rien lu ne
    #    rend pas un zero credible.
    rapport, _echec = mesurer([])
    controler("le rapport DIT combien de fichiers il a lus",
              rapport["nonsens_fichiers_lus"] > 0,
              rapport["nonsens_fichiers_lus"])
    controler("le rapport DIT combien d appels de portes il a lus",
              rapport["portes_appels_lus"] > 0, rapport["portes_appels_lus"])

    # 7. LE RAPPORT NE CONTIENT AUCUN CHEMIN VERS L AUTO-NOTE.
    corps = json.dumps(rapport, ensure_ascii=True).lower()
    controler("le rapport ne nomme aucune auto-note",
              "auto-note" not in corps and "autonote" not in corps)

    # 8. L ETAT EST DIT, ET IL EST TIRE DES FAITS, PAS D UN SCORE.
    controler("l etat est un mot, pas un nombre",
              rapport["etat"] in ("SAIN", "A_REPRENDRE"), rapport["etat"])

    reussis = sum(1 for _n, ok, _d in resultats if ok)
    for nom, ok, detail in resultats:
        print(("  [OK] " if ok else "  [KO] ") + nom
              + ("" if ok else " : " + str(detail)[:160]))
    print("AUTO-TEST : " + str(reussis) + "/" + str(len(resultats)) + ".")
    return 0 if reussis == len(resultats) else 1


if __name__ == "__main__":
    sys.exit(main())
