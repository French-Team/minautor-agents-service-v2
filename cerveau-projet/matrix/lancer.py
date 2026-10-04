#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lancer.py -- lanceur UNIQUE des outils de la Matrice.

Le NOM suffit : le lanceur resout l outil vers son main.py, pose l INTERPRETEUR
(sys.executable) et le CHEMIN ABSOLU -- la commande n est plus jamais ecrite a la
main (question du createur : moins d erreurs de syntaxe).

Usage :
  python3 cerveau-projet/matrix/lancer.py <outil> [arguments...]
  python3 cerveau-projet/matrix/lancer.py --appelant <identite> <outil> [arguments...]
  python3 cerveau-projet/matrix/lancer.py --lister
  python3 cerveau-projet/matrix/lancer.py --aide
  python3 cerveau-projet/matrix/lancer.py --auto-test

Un flag du LANCEUR (--lister, --aide, --auto-test, --appelant) va AVANT le nom
de la brique ; ce qui vient APRES appartient a l outil.

Resolution (source UNIQUE, EO-287 : matrice/data/commun/resolution_outils.py) :
  1. un outil de la Matrice : matrix/matrice/data/outils/<nom>/main.py
  2. une routine            : matrix/matrice/routines/<nom>/main.py
  3. un chemin explicite    : un fichier .py EXISTANT (chemin ancre)

Refus NOMMES (code 2) : nom inconnu (avec les noms proches), aucun main.py,
identite hors vocabulaire ferme, porte privee ouverte au MAUVAIS flux.
Le lanceur ne devine JAMAIS : il DIT quoi faire.

PORTE COMMUNE / PORTE PRIVEE (MO-434) -- la cle `commun` de la carte a enfin un
CONSOMMATEUR (mesure 2026-09-23 : le garde en verifiait la PRESENCE, le moteur
pouvait la FILTRER, personne ne l APPLIQUAIT) :
  - `commun: true`  -> porte COMMUNE : ouverte a tous les appelants, en silence ;
  - `commun: false` -> porte PRIVEE : l appelant SE DECLARE (--appelant <identite>
    ou variable d environnement MATRICE_APPELANT ; vocabulaire FERME : cameleon
    -> flux 1, operateur -> flux 2) et son flux est CROISE avec la cle `flux` de
    la carte QUAND ELLE PORTE : un flux etranger est REFUSE (code 2).
    L ANONYMAT n est PAS refuse -- 18 commandes documentees y passent, dont 9
    dans le protocole gele proto-12 que cette mission n a pas le droit de
    toucher -- mais il est NOMME a chaque passage, jamais un silence ;
  - carte absente : rien a juger, et le lanceur le DIT ([SANS CARTE]).
Une identite se DECLARE, elle ne se PROUVE pas (meme utilisateur OS, meme
shell) : ce controle est un GARDE (refus nomme + signalement), pas un verrou
OS. Il refuse le flux ETRANGER DECLARE ; il ne pretend pas prouver qui est
derriere le clavier -- ceci est DIT, pas sous-entendu.

Cette facade ne recopie AUCUNE regle de resolution : elle lit le module partage,
comme les appelants internes (un seul domicile, M-076). La regle `commun` non
plus : la grammaire de la carte vient de data/commun/carte_identite.py.
"""


import os
import subprocess
import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-416, lot -- fin du residu) -----------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu) : on remonte
# jusqu au dossier `matrix`, et on REFUSE plutot que de deviner (garde-foi L-006).
# Bloc AUTOSUFFISANT : il ne depend ni de l ordre des imports du fichier, ni de la
# presence d un `import subprocess` de module (mesure du 2026-09-25 : deux fichiers
# casses par ces deux pieges, invisibles au py_compile).
_RACINE_LANCEMENT = Path(__file__).resolve().parent
while _RACINE_LANCEMENT.name != "matrix":
    if _RACINE_LANCEMENT.parent == _RACINE_LANCEMENT:
        raise RuntimeError("racine `matrix` introuvable en remontant depuis " + __file__)
    _RACINE_LANCEMENT = _RACINE_LANCEMENT.parent
_REPERTOIRE_COMMUN_LANCEMENT = _RACINE_LANCEMENT / "matrice" / "data" / "commun"
if not (_REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(_REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(_REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(_REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())


def popen_enfant(*arguments, **options):
    """Le lancement DETACHE de cet outil : jamais de fenetre."""
    return subprocess.Popen(*arguments, **options, **drapeaux_popen())


import subprocess
import sys
from pathlib import Path

from resolution_outils import entrer_outils, resoudre  # noqa: E402
from carte_identite import COMMUN_NON, COMMUN_OUI, lire_carte  # noqa: E402

# --- PORTE COMMUNE / PORTE PRIVEE (MO-434) ----------------------------------
# LA GORGE : toute brique NOMMEE passe ici, la regle `commun` est donc appliquee
# UNE fois, jamais recopiee dans les 168 portes (M-076 -- recopier, c est
# fabriquer 168 verites qui divergent au premier changement).
NOM_OPTION_APPELANT = "--appelant"
# La variable d environnement : elle EST HERITEE par les enfants, ce que l option
# ne fait pas -- un pilote qui declare une fois couvre toute sa descendance.
VAR_APPELANT = "MATRICE_APPELANT"
# Vocabulaire FERME identite -> flux. Une valeur acceptee implicitement serait
# une valeur devinable (convention FLAG) : hors liste = refus nomme.
APPELANTS_FLUX = {"cameleon": "1", "operateur": "2"}
# La carte git A COTE de la brique (meme dossier que main.py).
CARTE_BRIQUE = "DESCRIPTION.md"


# LES FLAGS QUE LE LANCEUR POSSEDE SEUL (EO-488). Ils ne sont lus qu AVANT le
# nom de la brique : place APRES, ils sont transmis a l outil, qui les ignore ou
# les refuse -- et le lanceur ne dit RIEN. `--aide`, `-h` et `--help` en sont
# EXCLUS sur dessein : apres une brique, ils veulent dire l aide de CET outil,
# c est legitime et les signaler serait un faux positif. Mesure : aucun outil du
# depot ne consomme `--appelant` (les deux usages trouves -- passerelle-demandes
# et rendre-graphe -- le placent avant la brique, comme il se doit).
FLAGS_LANCEUR_SEULS = (NOM_OPTION_APPELANT, "--lister", "--auto-test")


def flags_tardifs(suite, nom):
    """(positions, message) : les flags du lanceur places APRES la brique.

    PURE : ni disque, ni environnement -- c est elle que l auto-test rejoue.
    Le flag tardif n est PAS deplace (il appartient desormais a la commande de
    l outil, et le deplacer changerait cette commande) : il est SIGNALE par son
    nom et sa position. Un silence se lit comme une identite declaree, alors
    que la porte va juger l appel comme ANONYME : c est le piege mesure.
    """
    trouves = [(index + 1, valeur) for index, valeur in enumerate(suite)
               if valeur in FLAGS_LANCEUR_SEULS]
    if not trouves:
        return trouves, ""
    details = ", ".join(valeur + " " + valeur_suivante(suite, position)
                        + " (position " + str(position) + " apres " + nom + ")"
                        for position, valeur in trouves)
    return trouves, ("flag(s) du lanceur place(s) APRES la brique " + nom + " : "
                     + details + " -- le lanceur ne lit ses flags qu AVANT le nom"
                     " de la brique : l option a ete transmise A L OUTIL, et la"
                     " porte va juger l appel comme ANONYME. Reecrivez : le flag"
                     " passe EN TETE, devant le nom de la brique.")


def valeur_suivante(suite, position):
    """Le jeton qui suit le flag (1-indexe sur `suite`), ou rien s il n y en a pas."""
    return suite[position] if position < len(suite) else "(valeur absente)"


def valider_appelant(valeur):
    """(identite, refus) : l identite declaree, ou un refus NOMME (jamais muet).

    Une identite vide rend ("", None) : l anonymat n est pas une faute en soi, il
    sera signale plus bas. Une identite HORS vocabulaire est refusee -- laisser
    un typo devenir de l anonymat silencieux serait accepter une valeur par defaut.
    """
    propre = str(valeur or "").strip().lower()
    if not propre:
        return "", None
    if propre not in APPELANTS_FLUX:
        return "", ("appelant inconnu <" + propre + "> -- vocabulaire ferme : "
                    + ", ".join(sorted(APPELANTS_FLUX)))
    return propre, None


def carte_de_brique(cible):
    """(carte, motif) : la carte qui git a cote de la brique, ou (None, motif).

    Le motif est TOUJOURS non vide quand la carte manque : un controle qui ne
    peut pas juger le DIT, il ne se tait pas (L-100 -- un silence passerait pour
    un feu vert).
    """
    chemin = Path(cible).parent / CARTE_BRIQUE
    if not chemin.is_file():
        return None, "carte absente : " + CARTE_BRIQUE + " cote de " + Path(cible).name
    try:
        texte = chemin.read_text(encoding="utf-8", errors="replace")
    except OSError as erreur:
        return None, "carte illisible : " + type(erreur).__name__
    carte = lire_carte(texte)
    if not carte:
        return None, ("carte illisible : front-matter `identite:` absent dans "
                      + CARTE_BRIQUE)
    return carte, ""


def juger_carte(carte, appelant):
    """(refus, signalement) de la regle `commun` sur une carte DEJA lue.

    PURE : ni disque, ni environnement -- c est elle que l auto-test cobaye
    rejoue. Refus non None = la porte est FERMEE a cet appelant (code 2) ;
    signalement non None = le passage est autorise mais NOMME (aucun laisse-
    passer muet sur une porte privee).
    """
    commun = str(carte.get("commun", "")).strip()
    if commun != COMMUN_NON:
        if commun and commun != COMMUN_OUI:
            return None, ("carte a reparer : commun doit dire " + COMMUN_OUI + " ou "
                          + COMMUN_NON + " : <" + commun + ">")
        return None, None                      # porte COMMUNE : ouverture, silence
    attente = (" -- declarez : " + NOM_OPTION_APPELANT + " <identite> (ou "
               + VAR_APPELANT + "=<identite>) ; vocabulaire "
               + ", ".join(sorted(APPELANTS_FLUX)))
    flux_carte = str(carte.get("flux", "")).strip()
    if not appelant:
        if flux_carte:
            # OPTION A du createur (MO-540, arbitrage MO-529 publie dans
            # preparation/arbitrage-lancer-anonymat.md) : le croisement refuse
            # l ANONYMAT comme il refuse deja l identite declaree du mauvais
            # flux. Avant, ce passage etait signale et joue -- donc le lanceur
            # punissait l honnetete et recompensait l anonymat. La porte et le
            # vocabulaire sont NOMMES, comme le refus d identite hors
            # vocabulaire : un refus muet serait un feu vert (L-100).
            return ("porte privee du flux " + flux_carte
                    + " appelee SANS identite declaree : cette porte n est pas "
                    "jouable par anonymat, elle appartient au flux " + flux_carte
                    + " -- declarez : " + NOM_OPTION_APPELANT + " <identite> (ou "
                    + VAR_APPELANT + "=<identite>) ; vocabulaire "
                    + ", ".join(sorted(APPELANTS_FLUX))), None
        return None, "porte privee appelee SANS identite declaree" + attente
    flux_appelant = APPELANTS_FLUX[appelant]   # vocabulaire verifie avant
    if flux_carte and flux_appelant != flux_carte:
        return ("porte privee du flux " + flux_carte + " appelee par le flux "
                + flux_appelant + " (appelant declare : " + appelant
                + "; la carte porte flux: " + flux_carte
                + ") -- cette porte n est pas la votre : elle appartient a "
                "l autre flux", None)
    if not flux_carte:
        return None, ("porte privee ouverte a l appelant <" + appelant
                      + "> : la carte ne porte PAS la cle `flux` -- le croisement "
                      "des flux n est donc PAS juge ici (carte sans flux, pas un "
                      "refus : la regle de cette porte est dit ailleurs)")
    return None, None


def controle(cible, appelant):
    """(refus, signalement) : la regle `commun` appliquee a UNE brique resolue."""
    carte, motif = carte_de_brique(cible)
    if carte is None:
        return None, "[SANS CARTE] " + Path(cible).parent.name + " : " + motif
    refus, signal = juger_carte(carte, appelant)
    if refus is not None:
        return refus, None
    if signal:
        return None, "[PORTE] " + Path(cible).parent.name + " : " + signal
    return None, None


def auto_test():
    """Le controle se PIEGE lui-meme (L-032) : cobayes REFUSES, contre-temoins PASSES.

    Un detecteur qui n a jamais vu de refus ne prouve rien : chaque epreuve dit
    ce qu elle attend, et le verdict compte celles qui ont rate.
    """
    epreuves = [
        ("porte COMMUNE ouverte sans identite (contre-temoin)",
         {"commun": COMMUN_OUI}, "", False),
        ("privee du flux 1 appelee par le flux 2 (COBAYE)",
         {"commun": COMMUN_NON, "flux": "1"}, "operateur", True),
        ("privee du flux 1 appelee par le flux 1 (contre-temoin)",
         {"commun": COMMUN_NON, "flux": "1"}, "cameleon", False),
        ("privee du flux 2 appelee par le flux 1 (COBAYE)",
         {"commun": COMMUN_NON, "flux": "2"}, "cameleon", True),
        ("anonymat sur une porte privee du flux : REFUSE (COBAYE, option A)",
         {"commun": COMMUN_NON, "flux": "1"}, "", True),
        ("anonymat sur une porte privee SANS cle flux : signale (contre-temoin)",
         {"commun": COMMUN_NON}, "", False),
        ("privee SANS cle flux : impossible a juger, donc pas refusee",
         {"commun": COMMUN_NON}, "cameleon", False),
        ("carte qui ment (commun hors vocabulaire) : signalee",
         {"commun": "peut-etre"}, "", False),
        ("identite hors vocabulaire : refusee en nommant le vocabulaire",
         {"commun": COMMUN_OUI}, "intrus", True),
    ]
    reussies = []
    ratees = []
    for texte, carte, appelant, attendu in epreuves:
        if appelant == "intrus":
            _, refus = valider_appelant("intrus")
        else:
            _, refus = valider_appelant(appelant)
            if refus is None:
                refus, _ = juger_carte(carte, appelant)
        obtenu = refus is not None
        (reussies if obtenu == attendu else ratees).append(texte)
        print(("  [OK] " if obtenu == attendu else "  [KO] ") + texte)
    # LE FLAG TARDIF (EO-488) : un detecteur qui n a jamais vu de signalement ne
    # prouve rien. Un COBAYE qui doit MORDRE, deux CONTRE-TEMOINS qui doivent
    # EPARGNER (la position correcte reste MUETTE, l aide de l outil aussi).
    epreuves_tardifs = [
        ("flag du lanceur place TARD : signale (COBAYE)",
         ["--appelant", "operateur"], "vigie-portes", True),
        ("flag du lanceur en tete : muet (contre-temoin)",
         [], "vigie-portes", False),
        ("aide de l outil placee apres la brique : muette (contre-temoin)",
         ["--aide", "-h"], "vigie-portes", False),
    ]
    for texte_t, suite_t, nom_t, attendu_t in epreuves_tardifs:
        _, message_t = flags_tardifs(suite_t, nom_t)
        obtenu_t = bool(message_t)
        if obtenu_t == attendu_t:
            reussies.append(texte_t)
        else:
            ratees.append(texte_t)
        print(("  [OK] " if obtenu_t == attendu_t else "  [KO] ") + texte_t)

    # Le cas SANS CARTE : rien a juger, mais le lanceur ne se tait pas (L-100).
    texte_sans = "carte absente : signalee ([SANS CARTE]), jamais refusee"
    refus_sans, signal_sans = controle(Path("brique-qui-n-existe-pas") / "main.py", "")
    if refus_sans is None and signal_sans and signal_sans.startswith("[SANS CARTE]"):
        reussies.append(texte_sans)
        print("  [OK] " + texte_sans)
    else:
        ratees.append(texte_sans)
        print("  [KO] " + texte_sans)

    print("")
    print("  epreuves : " + str(len(reussies)) + "/" + str(len(reussies) + len(ratees))
          + " (cobayes refuses : " + str(sum(1 for e in epreuves if e[3]))
          + ")")
    if ratees:
        print("VERDICT KO : " + ", ".join(ratees))
        return 1
    print("VERDICT OK : le controle refuse le flux etranger et nomme l anonymat.")
    return 0


def lister():
    for famille, nom, _ in entrer_outils():
        print(famille + "  " + nom)
    return 0


def main():
    arguments = sys.argv[1:]
    if not arguments:
        print(__doc__)
        return 2
    if arguments[0] in ("--aide", "-h", "--help"):
        print(__doc__)
        return 0
    if arguments[0] == "--lister":
        return lister()
    if arguments[0] == "--auto-test":
        return auto_test()
    appelant = ""
    if arguments[0] == NOM_OPTION_APPELANT:
        if len(arguments) < 2:
            print("REFUS : " + NOM_OPTION_APPELANT + " attend une identite parmi : "
                  + ", ".join(sorted(APPELANTS_FLUX)))
            return 2
        appelant, refus = valider_appelant(arguments[1])
        if refus is not None:
            print("REFUS : " + refus)
            return 2
        arguments = arguments[2:]
    else:
        appelant, refus = valider_appelant(os.environ.get(VAR_APPELANT, ""))
        if refus is not None:
            print("REFUS : " + VAR_APPELANT + " : " + refus)
            return 2
    if not arguments:
        print(__doc__)
        return 2
    nom, suite = arguments[0], arguments[1:]
    # UN FLAG DU LANCEUR PLACE TARD EST SIGNALE (EO-488) : il n est pas deplace
    # (il appartient a la commande de l outil), mais il est dit -- comme les
    # autres signalements, sur la SORTIE D ERREUR, pour que le stdout reste
    # CELUI DE L OUTIL.
    _tardifs, message_tardif = flags_tardifs(suite, nom)
    if message_tardif:
        print("[PORTE] " + nom + " : " + message_tardif, file=sys.stderr)
    cible, refus = resoudre(nom)
    if refus is not None:
        print("REFUS : " + refus)
        return 2
    refus_porte, signal = controle(cible, appelant)
    if signal:
        # Les signalements vont sur la SORTIE D ERREUR : le stdout reste CELUI DE
        # L OUTIL (un appelant qui lit la sortie d un verbe n y voit pas le garde).
        print(signal, file=sys.stderr)
    if refus_porte is not None:
        print("REFUS : " + refus_porte)
        return 2
    interieur = lancer_enfant([sys.executable, str(cible), *suite])
    return interieur.returncode


if __name__ == "__main__":
    sys.exit(main())
