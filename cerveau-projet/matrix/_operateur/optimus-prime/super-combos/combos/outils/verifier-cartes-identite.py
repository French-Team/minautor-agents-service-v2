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
  4. `type` vient d'un VOCABULAIRE FERME -- un type neuf doit etre DECLARE dans
     le DOMICILE de la grammaire (matrice/data/commun/carte_identite.py), jamais
     invente au fil de l'eau (c'est ainsi que `preparation-readme` et
     `outil-pilote-optimus` sont nes) ;
  5. `gravite` (5 valeurs) et `niveau` (1-10), QUAND ils sont declares, viennent de
     leurs listes fermees : ce sont les deux cles d IMPORTANCE (EO-457), elles
     servent a ORDONNER le travail -- une valeur inventee est un ecart.

DEPUIS LE 2026-09-21, CE GARDE NE RECOPIE PLUS LA GRAMMAIRE : ce fichier en
etait la SEULE copie, et le moteur de recherche -- qui doit savoir chercher par
COMBINAISON de champs de carte -- aurait du la dupliquer. La grammaire vit dans
son domicile (M-076), les deux consommateurs la partagent.

L'AUTOTEST le PIEGE (lecon L-032) : un cobaye complet est ACCEPTE, une carte
absente est ACCUSEE, un `appartient_a` en chemin est ACCUSE, un type inconnu est
ACCUSE. Un detecteur jamais vu crier ne prouve rien.

CE QU'IL NE FAIT PAS : lecture seule -- il lit des en-tetes de fichiers.

DEPUIS LE 2026-09-23, LE GARDE COUVRE LES DEUX ARBRES (decision createur) : la
zone de l operateur ET l arbre `matrice/`. Mesure du jour, AVANT reparation :
l arbre `matrice/` portait SIX cartes sans la cle obligatoire `commun`, SIX `type`
hors vocabulaire et QUARANTE-QUATRE documents sans aucune carte -- quand la zone de
l operateur, elle, etait propre (92/92). Un garde qui ne regarde qu un arbre sur
deux laissait passer exactement les ecarts pour lesquels il existe. Les deux zones
sont desormais jugees, et la sortie DIT laquelle parle.

Le NOUVEAU vocabulaire (decision du meme jour) : `routine` y entre -- quatre
documents de routines le disaient deja sans y avoir droit, et l arbre `matrice/`
en compte quatre de plus.

Usage: python verifier-cartes-identite.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = racine introuvable.
"""

import argparse
import shutil
import subprocess

import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-414, vague 4 du lot) -----------------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu) : on remonte
# jusqu au dossier `matrix`, et on REFUSE plutot que de deviner (garde-foi L-006).
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

import sys
import tempfile
from pathlib import Path

# Le moteur de recherche et son lanceur : la carte n'est pas decorative -- ce que
# le document DIT, on doit pouvoir le CHERCHER (mesure 2026-09-21).
DOSSIER_MOTEUR = Path("matrice") / "data" / "outils" / "rechercher"
NOM_LANCEUR = "lancer.py"
# Le domicile de la grammaire : ce garde le CONSOMME (M-076) et verifie que le
# moteur le consomme AUSSI, au lieu d'en tenir une seconde copie.
NOM_DOMICILE = "carte_identite"
# Ce qu'une reponse en mode carte doit DIRE, et ce qu'un refus doit NOMMER.
MARQUEUR_MODE_CARTE = "(carte)"
MARQUEUR_REFUS = "illisible"
# Un cobaye fonctionnel qui ne revient pas est un cobaye qui pend : borne DITE.
DELAI_MOTEUR_SECONDES = 180

# --- REFERENCES (aucune valeur en dur dans la logique) -----------------------
ZONE = Path("_operateur") / "optimus-prime"
# L ARBRE DE LA MATRICE (2026-09-23) : le second arbre, juge par le MEME garde et
# la MEME grammaire. Mesure d origine : six cartes y avaient perdu une cle
# obligatoire, six `type` y etaient inconnus, quarante-quatre documents n avaient
# aucune carte.
ZONE_MATRICE = Path("matrice")
# Les zones Jugees, avec l ETIQUETTE qui dit laquelle parle dans la sortie (deux
# lignes nommees pareil ne se distinguent plus).
ZONES_GARDEES = ((ZONE, "operateur"), (ZONE_MATRICE, "matrice"))
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
# La GRAMMAIRE de la carte vit dans SON domicile (matrice/data/commun/
# carte_identite.py, M-076) : ce garde la CONSOMME, il ne la recopie plus. Le
# chemin est DETECTE puis VERIFIE, jamais suppose (L-013) : sans le domicile, on
# s ARRETE au lieu de juger avec une grammaire imaginaire.
def _charger_grammaire():
    depart = Path(__file__).resolve()
    for parent in [depart] + list(depart.parents):
        candidat = parent / "matrice" / "data" / "commun" / "carte_identite.py"
        if candidat.is_file():
            if str(candidat.parent) not in sys.path:
                sys.path.insert(0, str(candidat.parent))
            from carte_identite import lire_carte
            from carte_identite import EXTENSION, CLE_IDENTITE, CLES_OBLIGATOIRES
            from carte_identite import CLE_LIENS, MARQUEUR_FRONT, SEPARATEURS_INTERDITS, TYPES_RECONNUS
            from carte_identite import liens_de_carte, valider_importance
            from carte_identite import juger_titre, titre_d_une_carte
            # La FORME d'un chemin de la Matrice a le MEME domicile que les cles de
            # la BDD des modifications (cible.forme_canonique, EO-363/EO-347) : ce
            # garde la CONSOMME pour juger les LIENS, il ne la recopie pas (L-029).
            from cible import forme_canonique
            return (MARQUEUR_FRONT, CLE_IDENTITE, CLES_OBLIGATOIRES, TYPES_RECONNUS,
                    SEPARATEURS_INTERDITS, EXTENSION, lire_carte, CLE_LIENS,
                    liens_de_carte, forme_canonique, valider_importance,
                    juger_titre, titre_d_une_carte)
    raise RuntimeError("domicile de la carte introuvable depuis " + str(depart))


(MARQUEUR_FRONT, CLE_IDENTITE, CLES_OBLIGATOIRES, TYPES_RECONNUS,
 SEPARATEURS_INTERDITS, EXTENSION, LIRE_CARTE, CLE_LIENS,
 LIENS_DE_CARTE, FORME_CANONIQUE, VALIDER_IMPORTANCE,
 JUGER_TITRE, TITRE_D_UNE_CARTE) = _charger_grammaire()

# Bornes de la remontee vers la Matrice (jamais un parents[N] nu : convention 1.3).
BORNES_REMONTEE = 12


def racine_matrice_de(zone):
    """Le dossier de la Matrice, deduit de la ZONE par remontee GARDEE, ou None.

    Un lien de carte se RESOUT contre la racine de la Matrice : sans elle, on ne
    juge pas < le fichier existe >, on le suppose -- et un lien mort passerait vert.
    """
    courant = zone
    for _ in range(BORNES_REMONTEE):
        if (courant / "matrice" / "data").is_dir():
            return courant
        courant = courant.parent
    return None

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

    DELEGUE au domicile de la grammaire (M-076) : le lecteur est le MEME que
    celui du moteur de recherche, donc un document ne peut pas etre "une carte"
    pour l'un et "pas une carte" pour l'autre (mesure 2026-09-21 : c'etait le
    risque exact de deux copies de la meme regle).
    """
    return LIRE_CARTE(texte)


def controler_zone(zone, collecteur=None, silencieux=False, etiquette=""):
    """Chaque .md porte une carte complete, un nom d'appartenance et un type reconnu.

    `etiquette` NOMME la zone jugee dans la sortie : depuis le 2026-09-23 le garde
    couvre DEUX arbres, et deux controles qui portent le meme nom ne se
    distinguent plus.
    """
    # `dire` relaie le collecteur et le silence : l autotest ne parle plus au nom
    # du corpus reel (MO-218/EO-212).
    prefixe = etiquette + "/" if etiquette else ""

    def dire(nom, condition, detail=""):
        return controler(prefixe + nom, condition, detail, collecteur, silencieux)

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
    titres_muets = []
    importance_invalide = []
    liens_fautifs, liens_morts, liens_egocentriques = [], [], []
    LIENS_DECLARES = 0
    racine = racine_matrice_de(zone)
    for chemin in fichiers:
        # La forme NOMMEE est CANONIQUE (posix) : un ecart nomme avec les
        # antislashs de la machine ne se compare pas a la carte qui le declare.
        relatif = chemin.relative_to(zone).as_posix()
        texte = lire_texte(chemin)
        carte = carte_de(texte)
        if carte is None:
            sans_carte.append(relatif)
            continue
        # LE TITRE INFORME (demande createur 2026-09-30). Un titre qui ne fait
        # que repeter le nom du dossier laisse le chemin muet : c etait la
        # mesure sur 45 outils (26 titres muets, 7 cartes sans titre). Le
        # jugement est celui du DOMICILE, consume ici, jamais recopie.
        for ecart_titre in JUGER_TITRE(carte, TITRE_D_UNE_CARTE(texte), chemin):
            titres_muets.append(relatif + " -> " + ecart_titre)
        manquantes = [cle for cle in CLES_OBLIGATOIRES if cle not in carte]
        if manquantes:
            cle_manquante.append(relatif + " (" + ",".join(manquantes) + ")")
        appartenance = carte.get("appartient_a", "")
        if any(sep in appartenance for sep in SEPARATEURS_INTERDITS):
            app_fautif.append(relatif + " -> " + appartenance)
        type_doc = carte.get("type", "")
        if type_doc and type_doc not in TYPES_RECONNUS:
            type_inconnu.append(relatif + " -> " + type_doc)
        # L IMPORTANCE (EO-457) : les cles gravite/niveau, QUAND elles sont la, sont
        # jugees par le DOMICILE (valider_importance) -- le garde ne recopie pas la
        # regle (M-076).
        for ecart_importance in VALIDER_IMPORTANCE(carte):
            importance_invalide.append(relatif + " -> " + ecart_importance)
        # LES LIENS (EO-347) : la carte peut nommer les fichiers qui lui sont
        # connectes. Un lien n'est juge que s'il est DECLARE -- une carte sans
        # `liens` est NORMALE (tout document n'a pas de voisin).
        # Le CHEMIN CANONIQUE du document (relatif a la racine de la Matrice) : sous
        # la zone `matrice/`, c est LUI que la carte emploie. Comparer seulement au
        # chemin relatif a la zone laissait passer une auto-reference ecrite dans la
        # forme que le garde EXIGE par ailleurs.
        canonique = relatif
        if racine is not None:
            try:
                canonique = chemin.relative_to(racine).as_posix()
            except ValueError:
                canonique = relatif
        for lien in LIENS_DE_CARTE(carte):
            LIENS_DECLARES += 1
            if FORME_CANONIQUE(lien, chemin) != lien:
                liens_fautifs.append(relatif + " -> " + lien)
            elif lien in (relatif, canonique):
                liens_egocentriques.append(relatif)
            elif racine is not None and not (racine / lien).is_file():
                liens_morts.append(relatif + " -> " + lien)

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

    dire("importance-valide", not importance_invalide,
              "gravite et niveau, quand ils sont declares, sont dans leurs listes fermees"
              if not importance_invalide else "IMPORTANCE INVALIDE : "
              + ", ".join(importance_invalide[:8]))
    if importance_invalide:
        ecarts.append("importance invalide : " + ", ".join(importance_invalide))

    # LES TROIS CONTROLES DU LIEN (EO-347). La QUESTION est celle d'EO-363 : le
    # lien est-il a SA forme canonique, et pointe-t-il un fichier VIVANT ?
    if not liens_fautifs:
        detail_liens = ("aucun lien declare" if not LIENS_DECLARES
                        else "chaque lien est relatif a la racine de la Matrice ("
                             + str(LIENS_DECLARES) + " lien(s) declare(s))")
    else:
        detail_liens = "LIENS NON CANONIQUES : " + ", ".join(liens_fautifs[:8])
    dire("liens-a-la-bonne-forme", not liens_fautifs, detail_liens)
    if liens_fautifs:
        ecarts.append("liens non canoniques : " + ", ".join(liens_fautifs))

    dire("liens-vivants", not liens_morts,
              "aucun lien mort" if not liens_morts else "LIENS MORTS : " + ", ".join(liens_morts[:8]))
    if liens_morts:
        ecarts.append("liens morts : " + ", ".join(liens_morts))

    # LE TITRE DIT CE QUE LE NOM NE DIT PAS (demande createur 2026-09-30). Un
    # titre muet ne casse rien : il rend le chemin incapable de distinguer deux
    # voisins. C est un ecart de LISSIBILITE, pas de conformite de carte.
    detail_titres = ("chaque carte d outil dit ce que l outil fait"
                     if not titres_muets
                     else "TITRES MUETS : " + ", ".join(titres_muets[:8]))
    dire("titres-informent", not titres_muets, detail_titres)
    if titres_muets:
        ecarts.append("titres muets : " + ", ".join(titres_muets))

    dire("liens-sans-auto-reference", not liens_egocentriques,
              "aucun document ne se cite lui-meme" if not liens_egocentriques
              else "AUTO-REFERENCE : " + ", ".join(liens_egocentriques[:8]))
    if liens_egocentriques:
        ecarts.append("liens auto-references : " + ", ".join(liens_egocentriques))

    return ("cartes-presentes", not ecarts,
            str(len(fichiers)) + " document(s) verifie(s)"), ecarts


def controler_moteur(matrix):
    """La carte n'est pas decorative : ce que le document DIT, on peut le CHERCHER.

    Mesure du 2026-09-21 (demande createur) : chercher "convention" rendait 106
    hits de TEXTE -- des lignes qui PARLENT de conventions -- et le moteur ne
    savait pas rendre les DOCUMENTS qui SONT la chose. Le moteur sait desormais
    chercher par COMBINAISON des champs de la carte.

    Trois controles, dont DEUX FONCTIONNELS : un moteur jamais vu ni repondre ni
    refuser ne prouve rien (L-032). Le premier tient le DOMICILE unique : la
    grammaire de la carte n'est pas recopiee dans le moteur (L-029).
    """
    ecarts = []
    dossier = matrix / DOSSIER_MOTEUR
    lanceur = matrix / NOM_LANCEUR

    # 1. UN SEUL DOMICILE : le moteur CONSOMME la grammaire, il ne la recopie pas.
    sources = sorted(dossier.rglob("*.py")) if dossier.is_dir() else []
    texte_moteur = "\n".join(lire_texte(chemin) for chemin in sources)
    consomme = ("from " + NOM_DOMICILE + " import") in texte_moteur
    recopie = "TYPES_RECONNUS" in texte_moteur
    controler(
        "moteur-consomme-le-domicile", consomme and not recopie,
        (str(len(sources)) + " source(s) du moteur : consomme " + NOM_DOMICILE
         + ", ne recopie pas le vocabulaire")
        if consomme and not recopie else
        ("le moteur ne consomme pas " + NOM_DOMICILE if not consomme
         else "le moteur a RECOPIE le vocabulaire ferme (TYPES_RECONNUS)"))
    if not consomme:
        ecarts.append("le moteur ne consomme pas le domicile " + NOM_DOMICILE)
    if recopie:
        ecarts.append("le moteur recopie le vocabulaire ferme (TYPES_RECONNUS)")

    # 2 et 3. FONCTIONNELS : une combinaison repond, une demande illisible est
    # refusee. Le moteur est lance comme le fait un agent (par le lanceur), sur le
    # corpus REEL : un cobaye en dossier jetable ne prouverait rien du perimetre.
    def lancer(arguments):
        try:
            termine = lancer_enfant(
                [sys.executable, str(lanceur)] + arguments,
                capture_output=True, text=True, cwd=str(matrix),
                timeout=DELAI_MOTEUR_SECONDES)
            return termine, ""
        except (OSError, subprocess.SubprocessError) as erreur:
            return None, repr(erreur)

    if not lanceur.is_file():
        ecarts.append("lanceur introuvable : " + str(lanceur))
        controler("moteur-repond-par-carte", False, "lanceur introuvable : " + str(lanceur))
        controler("demande-illisible-refusee", False, "lanceur introuvable")
        return ("moteur-cherche-par-carte", False, "lanceur introuvable"), ecarts

    resultat, erreur = lancer(["rechercher", "--champ", "type=convention", "--prive",
                               "--limite", "1"])
    if resultat is None:
        repond, detail_repond = False, "moteur non lance : " + erreur
    else:
        repond = resultat.returncode == 0 and MARQUEUR_MODE_CARTE in resultat.stdout
        detail_repond = ("code " + str(resultat.returncode) + ", marqueur "
                         + MARQUEUR_MODE_CARTE + " "
                         + ("present" if MARQUEUR_MODE_CARTE in resultat.stdout
                            else "ABSENT"))
    controler("moteur-repond-par-carte", repond,
              "une combinaison de champs rend des DOCUMENTS (" + detail_repond + ")"
              if repond else "LA COMBINAISON NE REPOND PAS : " + detail_repond)
    if not repond:
        ecarts.append("le moteur ne repond pas par carte : " + detail_repond)

    resultat, erreur = lancer(["rechercher", "--champ", "type", "--prive"])
    if resultat is None:
        refuse, detail_refus = False, "moteur non lance : " + erreur
    else:
        refuse = resultat.returncode == 2 and MARQUEUR_REFUS in resultat.stdout
        detail_refus = ("code " + str(resultat.returncode) + ", marqueur "
                        + MARQUEUR_REFUS + " "
                        + ("present" if MARQUEUR_REFUS in resultat.stdout
                           else "ABSENT"))
    controler("demande-illisible-refusee", refuse,
              "une demande sans valeur est REFUSEE en la nommant (" + detail_refus + ")"
              if refuse else "LA DEMANDE ILLISIBLE N'EST PAS REFUSEE : " + detail_refus)
    if not refuse:
        ecarts.append("demande illisible non refusee : " + detail_refus)

    return ("moteur-cherche-par-carte", not ecarts,
            "3 controles (domicile, reponse, refus)"), ecarts


def controler_autotest():
    """Le garde se PIEGE (lecon L-032) : des cobayes qui MORDENT, et les
    contre-temoins qui doivent passer (neuf epreuves, deux zones)."""
    racine = Path(tempfile.mkdtemp(prefix="verifier-cartes-autotest-"))
    zone = racine / ZONE
    zone.mkdir(parents=True, exist_ok=True)

    def poser(nom, contenu):
        (zone / nom).write_text(contenu, encoding="utf-8")

    def carte(type_doc, appartenance, commun="false", liens=None):
        bloc = ("---\nidentite:\n  type: " + type_doc + "\n  appartient_a: "
                + appartenance + "\n  commun: " + commun + "\n")
        if liens:
            bloc += "  liens: " + liens + "\n"
        return bloc + "---\n\n# Doc\n"

    # Le faux corpus porte une Matrice MINIMALE : sans elle, la racine est
    # introuvable et le controle < le lien pointe un fichier VIVANT > ne peut pas
    # juger -- un cobaye muet ne prouve rien (L-032).
    (racine / "matrice" / "data").mkdir(parents=True, exist_ok=True)
    (racine / "matrice" / "data" / "cible-vivante.md").write_text("# Cible\n", encoding="utf-8")
    VIVANTE = "matrice/data/cible-vivante.md"

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

        # L IMPORTANCE (EO-457) : le cobaye qui MORD porte une gravite HORS liste
        # ET un niveau HORS bornes ; le contre-temoin est le `doc-sain.md` plus haut
        # (une carte SANS importance declaree reste CONFORME -- une absence n est
        # jamais un ecart).
        shutil.rmtree(zone)
        zone.mkdir(parents=True, exist_ok=True)
        poser("importance-fausse.md",
              "---\nidentite:\n  type: convention\n  appartient_a: optimus-prime\n"
              "  commun: false\n  gravite: tresurgent\n  niveau: 0\n---\n\n# Doc\n")
        _, ecarts = controler_zone(zone, collecteur=[], silencieux=True)
        epreuves.append(("IMPORTANCE INVALIDE ACCUSEE",
                         any("importance invalide" in e for e in ecarts)))

        # LES LIENS (EO-347) -- le cas NOUVEAU : le cobaye qui MORD doit etre un
        # lien FAUX, et le contre-temoin un lien CANONIQUE ET VIVANT.
        shutil.rmtree(zone)
        zone.mkdir(parents=True, exist_ok=True)
        poser("lien-sain.md", carte("convention", "optimus-prime", liens=VIVANTE))
        _, ecarts = controler_zone(zone, collecteur=[], silencieux=True)
        epreuves.append(("lien CANONIQUE ET VIVANT ACCEPTE", not ecarts))

        shutil.rmtree(zone)
        zone.mkdir(parents=True, exist_ok=True)
        poser("lien-prefixe.md", carte("convention", "optimus-prime",
                                       liens="cerveau-projet/matrix/" + VIVANTE))
        _, ecarts = controler_zone(zone, collecteur=[], silencieux=True)
        epreuves.append(("lien PREFIXE ACCUSE",
                         any("non canoniques" in e for e in ecarts)))

        shutil.rmtree(zone)
        zone.mkdir(parents=True, exist_ok=True)
        poser("lien-mort.md", carte("convention", "optimus-prime",
                                    liens="matrice/data/nexiste-pas.md"))
        _, ecarts = controler_zone(zone, collecteur=[], silencieux=True)
        epreuves.append(("lien MORT ACCUSE", any("morts" in e for e in ecarts)))

        shutil.rmtree(zone)
        zone.mkdir(parents=True, exist_ok=True)
        # L'auto-reference se juge sur le chemin RELATIF A LA ZONE (c'est la forme
        # que `controler_zone` compare) -- mon premier cobaye ecrivait le chemin
        # COMPLET et ne pouvait donc pas mordre : un cobaye faux ne prouve rien.
        poser("lien-auto.md", carte("convention", "optimus-prime", liens="lien-auto.md"))
        _, ecarts = controler_zone(zone, collecteur=[], silencieux=True)
        epreuves.append(("AUTO-REFERENCE ACCUSEE", any("auto-references" in e for e in ecarts)))

        # LE CAS NOUVEAU (extension a l arbre matrice, 2026-09-23) : sous la zone
        # `matrice/`, un document qui se cite par son CHEMIN CANONIQUE doit etre
        # accuse -- c est la forme que la carte y emploie REELLEMENT.
        (racine / "matrice" / "data" / "auto-canonique.md").write_text(
            carte("readme", "matrice", liens="matrice/data/auto-canonique.md"), encoding="utf-8")
        _, ecarts = controler_zone(racine / "matrice", collecteur=[], silencieux=True)
        epreuves.append(("AUTO-REFERENCE CANONIQUE ACCUSEE (zone matrice)",
                         any("auto-references" in e for e in ecarts)))
    finally:
        shutil.rmtree(racine, ignore_errors=True)

    for nom, ok in epreuves:
        print("[--] cobaye " + ("ACCEPTE" if ok else "NON REPERE") + " : " + nom)
    reussies = sum(1 for ok in [ok for _, ok in epreuves] if ok)
    detail = ("piege (" + str(reussies) + "/" + str(len(epreuves)) + ")"
              if reussies == len(epreuves)
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

    # LES DEUX ARBRES (2026-09-23) : la zone de l operateur ET l arbre `matrice/`.
    for zone, etiquette in ZONES_GARDEES:
        resultat, ecarts = controler_zone(matrix / zone, etiquette=etiquette)
        resultats.append(resultat)
        ecarts_nommes.extend(ecarts)
    resultat, ecarts = controler_moteur(matrix)
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
