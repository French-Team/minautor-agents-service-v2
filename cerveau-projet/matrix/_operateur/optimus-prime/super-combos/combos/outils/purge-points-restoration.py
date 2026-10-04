#!/usr/bin/env python3
"""PURGE DES POINTS DE RESTAURATION (.bak) -- la regle de MO-544, outillee.

LE FAIT MESURE (2026-10-02, disque ET index). 1298 fichiers `.bak` sont SUIVIS
par git, soit 26 % des 5008 fichiers du depot ; 363 d entre eux sont ABSENTS du
disque (ils ne peuvent plus rien proteger : ils ne sont que de la graisse dans
l index) ; les 935 presents occupent 13,05 Mo, age median 8,1 jours, aucun
jamais purge. Aucune regle `.gitignore` ne les ecarte : chaque point de
restauration produit par une porte entre dans le commit SUIVANT. Un point de
restauration qui ne s efface jamais cesse d etre une securite -- il devient un
bruit que personne ne lit.

LA REGLE (createur, 2026-10-02) : garder les N derniers points de restauration
D UN FICHIER DONNE, purger les plus anciens, et ne plus committer les `.bak`.
N est une CONSTANTE NOMMEE (`CONSERVEES_PAR_FICHIER`) : la regle se change en un
endroit, jamais dans le code qui l applique.

L OUTIL NE DEVINE PAS. Un nom qui se termine par `.bak` sans marque horodatee
n est pas un point de restauration : un fichier peut s appeler legitimement
`donnees.bak`, et le detruire serait une faute. La suppression n est jamais faite
par defaut : sans `--oui`, l outil INVENTORIE et sort 0 -- un outil qui detruit
par defaut est un outil qu on evite d installer.

La DECISION est pure et separee du parcours du disque (`points_en_trop`) :
c est elle que l auto-test eprouve, sur une serie fabriquee en memoire, sans
qu aucun fichier ne soit lu ni touche.

Usage :
    purge-points-restoration.py inventaire [--racine <matrice>] [--conservees N]
    purge-points-restoration.py purger    [--racine <matrice>] [--conservees N] --oui
    purge-points-restoration.py --auto-test
"""
import argparse
import os
import re
import sys
import time
from pathlib import Path

# --- LA REGLE, en un seul endroit -------------------------------------------
# Points de restauration CONSERVES par fichier d origine. Le createur a laisse
# le choix ouvert (3 ou 5) : 5 est retenu, un seul nombre a changer.
CONSERVEES_PAR_FICHIER = 5

# Un point de restauration se reconnait a son NOM : le fichier, puis `.bak`,
# puis une marque horodatee. Sans marque, ou avec une marque qui n est pas une
# date, ce n est PAS un point de restauration : le motif est CALIBRE (MO-549) et
# ANCRE sur le nom entier, sinon `a.bak.txt` passerait pour un point de
# restauration de `a`.
MOTIF_BAK = re.compile(r"^(?P<origine>.+)\.bak(?:\.(?P<marque>.*))?$")
MARQUE_HORODATEE = re.compile(r"^\d{8}(_\d{6}(-\d+)?)?$")

# Zones ou un point de restauration ne dit pas la meme chose, donc ou l outil
# ne purge pas : le cache Python (regenere), le depot git, et la zone jetable
# (`tmp-*`, purgee a chaque cloture -- y purger serait un double geste).
MOTIFS_IGNORES = ("__pycache__", ".git")
PREFIXE_ZONE_JETABLE = "tmp-"

# Le siege du depot n'est PAS suppose : il est DEMANDE a git (rev-parse). Ce nom
# ne sert qu au message, pour que l refus dise ce qu il n a pas trouve.
NOM_IHM = "depot git"

# LA RACINE SE DETECTE PAR MARQUEUR, JAMAIS PAR UN COMPTE DE NIVEAUX (MO-088 :
# aucun `parents[N]` nu). Un index demande ici vaut trois niveaux au-dessus
# AUJOURD'HUI, et trois-plus-tard demain, quand l outil aura change de place : un
# decompte n est pas un ancrage, c est une peine a purger. Le marqueur est un
# NOM de dossier (`matrix`) -- le meme que consomme creer-combo.py.
NOM_RACINE = "matrix"
BORNES_REMONTEE = 30


def racine_matrice(depart=None):
    """La racine de la Matrice, trouvee en remontant jusqu au dossier `matrix`."""
    courant = Path(depart if depart is not None else __file__).resolve()
    for _ in range(BORNES_REMONTEE):
        if courant.name == NOM_RACINE:
            return courant
        if courant.parent == courant:
            break
        courant = courant.parent
    raise RuntimeError("racine " + NOM_RACINE + " introuvable en remontant depuis "
                       + str(depart))


# --- LA DECISION, pure ------------------------------------------------------
def classer(nom):
    """(origine, marque) si le nom est un point de restauration, sinon None."""
    trouve = MOTIF_BAK.match(nom)
    if trouve is None:
        return None
    origine = trouve.group("origine")
    marque = trouve.group("marque")
    if not origine or not marque:
        return None
    if not MARQUE_HORODATEE.match(marque):
        return None
    return origine, marque


def points_en_trop(points, conservees):
    """Les points a purger : ceux qui debordent la retenue.

    `points` est la liste des points de restauration D UN SEUL fichier, chacun
    (marque, chemin). L ordre se fait sur la MARQUE -- l horodatage pose par la
    porte -- et non sur la date du systeme : deux points ecrits dans la meme
    seconde restent compares, et un point restaure depuis une copie de travail
    n est pas classe au hasard. La retenue porte sur les DERNIERS points : une
    retenue qui garderait les plus anciens laisserait le point le plus proche
    du travail actuel etre purge, ce qui n est pas une retention mais un oubli.
    """
    tries = sorted(points, key=lambda paire: paire[0])
    return [chemin for _, chemin in tries[:max(0, len(tries) - conservees)]]


# --- LA MESURE, sur le disque ------------------------------------------------
def ignores(relatif):
    parts = Path(relatif).parts
    if any(part in MOTIFS_IGNORES for part in parts):
        return True
    return any(part.startswith(PREFIXE_ZONE_JETABLE) for part in parts)


def inventorier(racine, conservees=CONSERVEES_PAR_FICHIER):
    """(a_purger, total, fichiers) : la regle appliquee a tout l arbre."""
    groupes = {}
    for chemin in racine.rglob("*"):
        if not chemin.is_file() or ignores(chemin.relative_to(racine).as_posix()):
            continue
        trouve = classer(chemin.name)
        if trouve is not None:
            origine, marque = trouve
            cle = (chemin.parent.relative_to(racine).as_posix(), origine)
            groupes.setdefault(cle, []).append((marque, chemin))
    a_purger = []
    for points in groupes.values():
        a_purger.extend(points_en_trop(points, conservees))
    return sorted(a_purger, key=lambda c: c.as_posix()), sum(
        len(p) for p in groupes.values()), len(groupes)


def age_jours(chemin, maintenant=None):
    moment = maintenant if maintenant is not None else time.time()
    return (moment - chemin.stat().st_mtime) / 86400.0


def decrire(chemin):
    """Un rapport qui ne peut pas PLANTER sur la faute qu il denonce (MO-540)."""
    return ascii(str(chemin))


def reparable(relatifs, suivis):
    """(purgables, irrecuperables) sur des chemins RELATIFS en posix.

    Fonction PURE : elle ne lit rien, c est elle que l auto-test eprouve. Un
    point de restoration que git ne suit pas ne rendrait RIEN apres
    suppression : le retirer de la purge n est pas une precaution de style, c
    est la difference entre un point de restauration et une perte. Si git ne
    repond pas (`suivis is None`), rien n est purge : une porte ne suppose pas
    ce qu elle ne peut pas mesurer.
    """
    if suivis is None:
        return [], list(relatifs)
    return ([r for r in relatifs if r in suivis],
            [r for r in relatifs if r not in suivis])


def suivis_par_git(racine):
    """L ensemble des chemins que git sait restituer, ou None si git ne repond pas.

    UNE PORTE QUI DETRUIT DOIT DIRE CE QU'ELLE DETRUIT IRREVERSIBLEMENT. Un point
    de restoration N'EST PAS dans l historique git des lors qu'il n'est pas
    suivi : le supprimer alors ne rendrait rien, et l'affirmation inverse
    ("chaque point reste dans l historique") serait un fait invente -- la
    connaissance qui rassure alors qu'elle ne protege pas (L-055). Le siege est
    declare par `NOM_IHM` et rien n'est devine : sans depot, on rend None et la
    purge refuse.
    """
    import subprocess

    drapeaux = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0

    def interroger(commande):
        try:
            return subprocess.run(commande, capture_output=True, text=True,
                                  timeout=120, creationflags=drapeaux)
        except (OSError, subprocess.SubprocessError):
            return None

    # LE SIEGE SE DEMANDE, IL NE SE DEVINE PAS. Mesure du 2026-10-02 : le depot
    # est a la RACINE DU WORKSPACE, deux niveaux au-dessus de la matrice -- un
    # `.git` cherche sous la matrice rendait git MUET alors qu il repondait, et
    # la purge refusait de purger des points parfaitement restitubles (un refus
    #.muet sur une mesure fausse est un garde turned against its own cause).
    # `rev-parse --show-toplevel` est la seule reponse qui ne depende pas d un
    #siege suppose.
    sonde = interroger(["git", "-C", str(racine), "rev-parse", "--show-toplevel"])
    if sonde is None or sonde.returncode != 0:
        return None
    liste = interroger(["git", "-C", str(racine), "ls-files", "-z"])
    if liste is None or liste.returncode != 0:
        return None
    return set(ligne for ligne in (liste.stdout or "").split("\0") if ligne)


# --- L AUTO-TEST : la decision pure, sur une serie fabriquee en memoire ------
def verifier_auto_test():
    """Trois temoins : le cobaye, son CONTRE-TEMOIN, et l epargne calibree.

    Une preuve positive qui ne peut pas dire NON ne prouve rien (lecon L-132) :
    chaque cas < on purge > est donc accompagne du meme cas < on ne purge pas >.
    """
    def serie(nombre, debut=1):
        """(marque, chemin) de points de restauration d UN fichier."""
        return [("202601%02d_0000%02d" % (pas, pas),
                 "CHEMEIN/bilan.md.bak.202601%02d_0000%02d" % (pas, pas))
                for pas in range(debut, debut + nombre)]

    # LE COBAYE : sept points pour UN fichier, cinq conserves -> les DEUX plus
    # anciens sont a purger, et ce sont eux (pas deux au hasard).
    purges = points_en_trop(serie(7), CONSERVEES_PAR_FICHIER)
    attendus = ["CHEMEIN/bilan.md.bak.20260101_000001",
                "CHEMEIN/bilan.md.bak.20260102_000002"]
    if purges != attendus:
        print("[KO] sept points, cinq conserves : rendu " + str(purges))
        return 1
    print("[OK] sept points, cinq conserves : " + str(len(purges)) + " purge(s), les plus anciens")

    # LE CONTRE-TEMOIN : exactement N points -> RIEN n est purge. Une regle qui
    # purge toujours detruit des points encore utiles.
    if points_en_trop(serie(5), CONSERVEES_PAR_FICHIER) != []:
        print("[KO] cinq points pour cinq conserves : quelque chose est purge")
        return 1
    print("[OK] cinq points pour cinq conserves : rien a purger")

    # LE CONTRE-TEMOIN DU DESORDRE : la retenue ne depend pas de l ordre d
    # arrivee sur le disque. Sans ce temoin, un point purge selon son ordre de
    # lecture ferait du hasard une regle.
    melange = serie(7)
    melange = [melange[i] for i in (3, 0, 6, 2, 5, 1, 4)]
    if sorted(points_en_trop(melange, CONSERVEES_PAR_FICHIER)) != sorted(purges):
        print("[KO] l ordre de lecture change le verdict : la retenue n est pas une regle")
        return 1
    print("[OK] l ordre de lecture ne change pas le verdict")

    # L EPARGNE CALIBREE : quatre noms qui portent `.bak` sans etre des points
    # de restauration. Un detecteur non calibre detruit des fichiers ordinaires.
    for faux, pourquoi in (("donnees.bak", "marque absente"),
                           ("notes.bak.txt", "marque non horodatee"),
                           ("x.bak.hier", "marque non horodatee"),
                           ("modele.py", "pas .bak")):
        if classer(faux) is not None:
            print("[KO] epargne a tort : " + faux + " (" + pourquoi + ")")
            return 1
    print("[OK] epargne a tort : quatre noms qui ne sont pas des points de restauration")

    # LE TEMOIN DE L ANCRAGE : un nom a plusieurs points reste reconnu, et
    # l origine rendue est le fichier ENTIER (jamais une coupe au premier point).
    ancre = classer("rapport.2026.bak.20260101_000001")
    if ancre != ("rapport.2026", "20260101_000001"):
        print("[KO] l ancrage du nom : rendu " + str(ancre))
        return 1
    print("[OK] l ancrage du nom : origine = " + str(ancre[0]))

    # LE CONTRE-TEMOIN DE L IRREVERSIBILITE : un point de restauration que git
    # ne suit PAS ne rendrait rien apres suppression. Sans ce temoin, la purge
    # detruirait des points perdus, et l outil affirmerait l inverse.
    candidats = ["a/bilan.md.bak.1", "b/notes.md.bak.2", "c/vieux.md.bak.3"]
    suivis = {"a/bilan.md.bak.1", "b/notes.md.bak.2"}
    purgables, irrecuperables = reparable(candidats, suivis)
    if purgables != ["a/bilan.md.bak.1", "b/notes.md.bak.2"] \
            or irrecuperables != ["c/vieux.md.bak.3"]:
        print("[KO] le refus de purger ce que git ne suit pas : " + str(purgables)
              + " / " + str(irrecuperables))
        return 1
    print("[OK] le refus de purger ce que git ne suit pas : 1 epargne sur 3")

    # LE CONTRE-TEMOIN DU SILENCE : git ne repond pas -> RIEN n est purge. Une
    # porte qui suppose l historique purge ce qu elle ne peut pas restituer.
    if reparable(candidats, None) != ([], candidats):
        print("[KO] git muet : la purge a choisi quelque chose")
        return 1
    print("[OK] git muet : rien n est purge plutot que tout")
    return 0


def main(argv):
    analyseur = argparse.ArgumentParser(
        description="Inventorier, puis purger, les points de restauration en trop.")
    analyseur.add_argument("verbe", nargs="?", default="inventaire",
                           choices=("inventaire", "purger"))
    analyseur.add_argument("--racine", default=None)
    analyseur.add_argument("--conservees", type=int, default=CONSERVEES_PAR_FICHIER)
    analyseur.add_argument("--oui", action="store_true",
                           help="exige pour purger : sans lui, rien n est detruit")
    analyseur.add_argument("--auto-test", action="store_true")
    args = analyseur.parse_args(argv[1:])

    if args.auto_test:
        return verifier_auto_test()
    if args.conservees < 0:
        print("REFUS : --conservees ne peut pas etre negatif")
        return 2

    # LA RACINE EST LA MATRICE ENTIERE, jamais son seul dossier `matrice/` : la
    # zone des operateurs (`_operateur/`) porte a elle seule 287 des 613 points
    # de restauration du perimetre. Un inventaire qui s arretait a `matrice/`
    # rendait 326 au lieu de 613 -- un ZERO FAUX, indiscernable d une regle qui
    # n aurait rien a dire (mesure du 2026-10-02, MO-544).
    try:
        base = Path(args.racine) if args.racine else racine_matrice()
    except RuntimeError as erreur:
        print("REFUS : " + ascii(str(erreur)))
        return 2
    if not base.is_dir():
        print("REFUS : la racine " + NOM_RACINE + " est introuvable : " + decrire(base))
        return 2
    if (base / "matrice").is_dir() and (base / "_operateur").is_dir():
        racine = base
    elif (base / "matrice").is_dir():
        racine = base / "matrice"
    elif (base / "_operateur").is_dir():
        racine = base
    else:
        print("REFUS : racine INTROUVABLE : " + decrire(base))
        return 2

    a_purger, total, fichiers = inventorier(racine, args.conservees)
    relatifs = [chemin.relative_to(racine).as_posix() for chemin in a_purger]
    suivis = suivis_par_git(racine)
    purges, irrecuperables = reparable(relatifs, suivis)
    if suivis is None:
        print("git : SANS REPONSE (" + NOM_IHM + " injoignable sous " + decrire(racine)
              + ") -- aucun point n est purge : rien ne rendrait ce qu on detruit")
    print("racine : " + decrire(racine))
    print("fichiers d origine : " + str(fichiers)
          + " | points de restauration : " + str(total)
          + " | conserves par fichier : " + str(args.conservees))
    liberes = sum(chemin.stat().st_size for chemin in a_purger)
    print("a purger : " + str(len(a_purger))
          + " | volume : " + str(round(liberes / 1048576.0, 2)) + " Mo")
    for chemin in a_purger:
        marque = "  - " if decrire(chemin.relative_to(racine)) in purges else "  [GARDE] "
        print(marque + decrire(chemin) + "  (" + str(round(age_jours(chemin), 1)) + " j)")
    if irrecuperables:
        print("NON SUIVIS par git, donc NON purges (" + str(len(irrecuperables))
              + ") : les supprimer serait une perte, pas une retention")

    if args.verbe == "inventaire":
        print("INVENTAIRE SEUL : rien n a ete detruit (--oui purge)")
        return 0
    if not args.oui:
        print("REFUS : purger exige --oui -- un outil qui detruit par defaut est un outil qu on evite")
        return 2
    if suivis is None:
        print("REFUS : git ne repond pas -- une porte ne suppose pas l historique")
        return 2
    a_purger = [chemin for chemin in a_purger
                if chemin.relative_to(racine).as_posix() in purges]
    echecs = []
    for chemin in a_purger:
        try:
            os.remove(str(chemin))
        except OSError as erreur:
            echecs.append(decrire(chemin) + " : " + ascii(str(erreur)))
    for echec in echecs:
        print("  [KO] purge impossible : " + echec)
    print("PURGE : " + str(len(a_purger) - len(echecs)) + " supprime(s), "
          + str(len(echecs)) + " echec(s), " + str(len(irrecuperables))
          + " epargne(s) car non suivis par git. Chaque point supprime reste"
          " dans l historique git.")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
