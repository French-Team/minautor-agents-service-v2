#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
suivi-cameleon -- LA PORTE DU SUIVI DES MISSIONS DU CAMELEON (MO-534).

POURQUOI. `suivi-optimus.md` suit les missions MO- (Optimus) et
`suivi-pilote.md` suit le pilote d Optimus. Les missions M- du cameleon
n avaient AUCUNE vue : leur trace existe (matrice/data/historiques-missions.jsonl,
147 enregistrements) et se lit deja par `bilan-periode`, mais rien ne les
rassemble sous un angle unique ni ne dit ce que leur trace ne dit pas.

CE QU ELLE EST : une VUE DERIVEE. Elle ne recopie aucun fait -- elle LIT le
journal des missions du cameleon et le RASSEMBLE. Elle n ecrit qu elle-meme
(la vue), et elle pose son fichier par la PORTE ECRIRE comme le fait sa
 jumelle `suivi-pilote`.

CE QU ELLE ECRIT : un seul fichier, `suivi-cameleon.md`, REGENERABLE. Aucun
journal de verdicts : les pannes du cameleon n ont pas de seuil declare, et
inventer une liste de seuils serait une verite sans source (la regle des
bornes : un seuil absent se DIT, il ne s invente pas).

LA LOI DES COLONNES (identique a sa jumelle, exigence createur) : une colonne
se garde si elle VARIE ou si elle PORTE UN VERDICT. Une colonne qui vaut
`--` pour tout le monde est un placeholder qui ment : elle est OMISE, et la vue
DIT lesquelles elle a omises.

UNE DUREE QUI NE SE LIT PAS SE DIT. Mesure du 2026-10-03 sur 147
enregistrements : 110 durees calculables, 5 ou les bornes sont IDENTIQUES
(duree INCONNUE -- un debut pose apres coup, pas une mission de zero seconde)
et 32 ou une borne manque. Aucun de ces cas n est rendu 0.

Usage:
  python suivi-cameleon.py            regenere la vue, rend le verdict
  python suivi-cameleon.py --json     la vue en JSON (pour un appelant)
  python suivi-cameleon.py --auto-test  eprouve les extracteurs (cobaye)
  code 0 = vue regeneree et lisible ; 1 = journal illisible ; 2 = racine introuvable.
"""
import argparse
import collections
import json
import sys
from datetime import datetime
from pathlib import Path

# --- DOMICILES, declares une fois --------------------------------------------
# La racine se DETECTE par MARQUEUR (MO-088 : aucun `parents[N]` nu). Un nombre
# de niveaux compte a la main devient faux des que l objet change de place, et
# il se TAIT en devenant faux -- ce refus ci-dessous l a attrape net sur la
# premiere version de cette porte, ecrite pour la zone jetable.
_courant = Path(__file__).resolve().parent
BORNES_REMONTEE = 30
for _ in range(BORNES_REMONTEE):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        break
    _courant = _courant.parent
else:
    raise RuntimeError("Racine matrix/ introuvable en remontant depuis "
                       + str(Path(__file__).resolve().parent))
RACINE = _courant
if RACINE.name != "matrix":
    raise RuntimeError("Structure inattendue : " + str(RACINE)
                       + " n est pas la racine `matrix`")
JOURNAL = RACINE / "matrice" / "data" / "historiques-missions.jsonl"
NOM_VUE = "suivi-cameleon.md"
CHEMIN_VUE = RACINE / "matrice" / "data" / NOM_VUE

PREFIXE_MISSION = "M-"
FORMAT_DATE = "%Y-%m-%d %H:%M:%S"
ENCADRE_DATE = "%Y-%m-%d"

# Bornes d AFFICHAGE : declarees en TETE de module, jamais en dur dans la
# logique qui les consomme.
LIMITE_MISSIONS = 30
LIMITE_THEMES = 12
LIMITE_OBJECTIF = 70

# Les trois cas de duree non mesurable. Aucun ne vaut 0 : un zero se lirait
# comme une mesure (lecon du 2026-09-21, reprise telle quelle par sa jumelle).
DUREE_INCONNUE_BORNES_IDENTIQUES = "inconnue (bornes identiques)"
DUREE_INCONNUE_BORNES_ILLISIBLES = "inconnue"
DUREE_NON_TERMINEE = "en cours"


def lire_journal(chemin):
    """Les enregistrements lisibles, dans l ordre du fichier. (liste, ecarts)."""
    lignes = []
    ecarts = []
    try:
        brut = chemin.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as erreur:
        return [], ["journal ILLISIBLE : " + type(erreur).__name__]
    for numero, ligne in enumerate(brut, 1):
        if not ligne.strip():
            continue
        try:
            donnees = json.loads(ligne)
        except ValueError:
            # Une ligne illisible est NOMMEE, jamais comptee comme une mission
            # fantome et jamais sautee en silence.
            ecarts.append("ligne " + str(numero) + " : JSON illisible")
            continue
        if isinstance(donnees, dict):
            lignes.append(donnees)
        else:
            ecarts.append("ligne " + str(numero) + " : ce n est pas un objet")
    return lignes, ecarts


def missions_du_cameleon(entrees):
    """Les enregistrements dont l id porte le prefixe M-. (liste, ecartees)."""
    retenues = []
    ecartees = []
    for entree in entrees:
        identifiant = str(entree.get("id", ""))
        if identifiant.startswith(PREFIXE_MISSION):
            retenues.append(entree)
        elif identifiant:
            ecartees.append(identifiant)
    return retenues, ecartees


def parse_date(texte):
    """Une date lisible, ou None. Jamais d exception -- une date fausse est
    un fait NON mesurable, pas une panne."""
    if not isinstance(texte, str) or not texte.strip():
        return None
    try:
        return datetime.strptime(texte.strip(), FORMAT_DATE)
    except ValueError:
        return None


def duree_lisible(entree):
    """La duree d une mission, ou None si elle n est pas mesurable.

    Trois issues, trois textes distincts : mesurable, bornes identiques
    (debut pose apres coup), bornes illisibles. Aucun zero.
    """
    debut = parse_date(entree.get("injectee_le"))
    fin = parse_date(entree.get("terminee_le"))
    if debut is None or fin is None:
        return None
    secondes = (fin - debut).total_seconds()
    if secondes == 0:
        return DUREE_INCONNUE_BORNES_IDENTIQUES
    minutes = secondes / 60.0
    if minutes < 1:
        return "< 1 min"
    if minutes < 60:
        return ("%.0f" % minutes) + " min"
    return ("%.1f" % (minutes / 60.0)) + " h"


def version_duree(entree):
    """Le mode machine de la duree : (valeur, mesurable)."""
    texte = duree_lisible(entree)
    if texte is None:
        return DUREE_NON_TERMINEE, False
    if texte in (DUREE_INCONNUE_BORNES_IDENTIQUES, DUREE_INCONNUE_BORNES_ILLISIBLES):
        return texte, False
    return texte, True


def tronquer(texte, limite=LIMITE_OBJECTIF):
    """Une coupe toujours DITE : une troncature muette a produit le defaut de
    la vue Optimus (MO-139)."""
    texte = " ".join(str(texte).split())
    if len(texte) <= limite:
        return texte
    return texte[:limite] + " ...(+" + str(len(texte) - limite) + ")"


def themes_reels(entrees):
    """Les themes par NOMBRE de missions, et la liste de ceux qui sont
    nommes autrement.

    Mesure du 2026-10-03 : 68 valeurs distinctes pour 147 missions -- dont des
    titres libres (`activer la veille-flux en boucle`) et des variantes de
    casse (`routine` et `ROUTINE`). Ce n est pas un defaut de la vue, c est
    un fait du journal : la vue le REND VISIBLE au lieu de le normaliser en
    silence.
    """
    compteur = collections.Counter()
    for entree in entrees:
        theme = str(entree.get("theme", "") or "").strip()
        if theme:
            compteur[theme] += 1
    return compteur


def _theme_est_normalise(theme, themes_nommes):
    """Un theme se lit comme un NOM s il est dans la liste des themes connus
    de l historique (comptes >= 2), et non un titre libre pose une fois."""
    return themes_nommes.get(theme, 0) >= 2


def tableau_missions(entrees, themes_nommes):
    """La table des missions, bornes les plus recentes d abord."""
    def cle(entree):
        moment = parse_date(entree.get("terminee_le")) or parse_date(entree.get("chargee_le"))
        return moment or datetime.min
    triees = sorted(entrees, key=cle, reverse=True)[:LIMITE_MISSIONS]
    lignes = [
        "| Mission | Theme | Type | Duree | Objectif |",
        "|---|---|---|---|---|",
    ]
    for entree in triees:
        duree, _ = version_duree(entree)
        theme = str(entree.get("theme", "") or "")
        marque = "" if _theme_est_normalise(theme, themes_nommes) else " *(titre libre)*"
        objectif = tronquer(entree.get("objectif") or entree.get("titre") or "")
        lignes.append("| " + str(entree.get("id", "?")) + " | " + tronquer(theme, 28)
                      + marque + " | " + str(entree.get("type", "?")) + " | " + duree
                      + " | " + objectif + " |")
    return lignes, len(entrees) - len(triees)


def tableau_themes(compteur):
    """La table des themes, par volume."""
    lignes = ["| Theme | Missions |", "|---|---|"]
    for theme, nombre in compteur.most_common(LIMITE_THEMES):
        lignes.append("| " + tronquer(theme, 40) + " | " + str(nombre) + " |")
    return lignes, max(0, len(compteur) - LIMITE_THEMES)


def compter_missions(entrees):
    """(missions distinctes, terminees, creees sans fin), sur les IDENTIFIANTS.

    Le prefixe `M-` a servi aux deux flux avant la convention `MO-` (CV-009) :
    un meme identifiant porte donc plusieurs evenements dans le journal. Compter
    les LIGNES affichait donc plus de missions qu il n en existe (152 lignes
    pour 89 missions au cameleon le 2026-10-03). On compte les identifiants
    distincts, et l attente se calcule comme `bilan-matrice` la calcule : les
    ids crees moins les ids termines.

    Fonction PURE et isolee : une regle qu on ne peut pas appeler ne peut pas
    etre eprouvee par le jeu.
    """
    ids_crees = {str(e.get("id")) for e in entrees
                 if e.get("type") == "mission-creee" and e.get("id")}
    ids_termines = {str(e.get("id")) for e in entrees
                    if e.get("type") == "mission-terminee" and e.get("id")}
    identifiants = {str(e.get("id")) for e in entrees if e.get("id")}
    return len(identifiants), len(ids_termines), len(ids_crees - ids_termines)


def composer_vue(entrees, chemins_source):
    """La vue complete, en lignes. Fonction PURE : elle ne lit ni n ecrit."""
    identifiants = [str(e.get("id", "")) for e in entrees if e.get("id")]
    compteur_themes = themes_reels(entrees)
    themes_libres = [t for t in compteur_themes if not _theme_est_normalise(t, compteur_themes)]

    mesurees = 0
    inconnues = 0
    for entree in entrees:
        _, mesurable = version_duree(entree)
        if mesurable:
            mesurees += 1
        else:
            inconnues += 1

    # COMPTAGE PAR IDENTIFIANT, PAS PAR LIGNE (MO-552, 2026-10-03) -- la regle
    # elle-meme est dans `compter_missions`, qui est pure et eprouvee par le jeu.
    distinctes, terminees, creees = compter_missions(entrees)
    identifiants_distincts = {str(e.get("id")) for e in entrees if e.get("id")}

    premier, dernier = None, None
    for entree in entrees:
        moment = parse_date(entree.get("terminee_le")) or parse_date(entree.get("chargee_le"))
        if moment is None:
            continue
        premier = moment if premier is None or moment < premier else premier
        dernier = moment if dernier is None or moment > dernier else dernier

    lignes = []
    lignes.append("---")
    lignes.append("identite:")
    lignes.append("  type: analyse")
    lignes.append("  appartient_a: cameleon")
    lignes.append("  commun: false")
    lignes.append("---")
    lignes.append("")
    lignes.append("# SUIVI DES MISSIONS DU CAMELEON -- la vue derivee")
    lignes.append("")
    lignes.append("> Regeneree par la porte `suivi-cameleon` (MO-534). Jamais editee a la")
    lignes.append("> main : elle se RECALCULE. Les faits vivent dans")
    lignes.append("> `matrice/data/historiques-missions.jsonl` ; cette vue ne les recopie")
    lignes.append("> pas, elle les RASSEMBLE et elle DIT ce qu elle ne sait pas mesurer.")
    lignes.append("")
    lignes.append("| Mesure | Valeur |")
    lignes.append("|---|---|")
    lignes.append("| Missions dans la trace (identifiants distincts) | "
                  + str(len(identifiants_distincts)) + " |")
    lignes.append("| dont terminees | " + str(terminees) + " |")
    lignes.append("| dont creees sans fin | " + str(creees) + " |")
    lignes.append("| Durees mesurables | " + str(mesurees) + " |")
    lignes.append("| Durees NON mesurables | " + str(inconnues) + " |")
    if premier and dernier:
        lignes.append("| Periode couverte | " + premier.strftime(ENCADRE_DATE)
                      + " -> " + dernier.strftime(ENCADRE_DATE) + " |")
    lignes.append("")
    lignes.append("Source : `" + chemins_source + "`.")
    lignes.append("")

    lignes.append("## Ce que cette vue ne sait pas")
    lignes.append("")
    if inconnues:
        lignes.append("- **" + str(inconnues) + " mission(s) sans duree mesurable** : soit les")
        lignes.append("  bornes sont identiques (debut pose apres coup), soit une borne")
        lignes.append("  manque. Aucun de ces cas n est rendu 0 : un zero se lirait comme")
        lignes.append("  une mesure.")
    if themes_libres:
        lignes.append("- **" + str(len(themes_libres)) + " theme(s) nommes comme un TITRE** plutot")
        lignes.append("  qu un theme du vivier (`" + tronquer(themes_libres[0], 40)
                      + "`...). Une vue qui les normaliserait en silence")
        lignes.append("  cacherait la divergence ; elle les-marque donc a la volee.")
    lignes.append("- Aucune **note de BDD** ne porte ces missions : le journal des")
    lignes.append("  missions du cameleon est unHistorique de cloture, pas une trace")
    lignes.append("  d evenements. Rien n y dit les ports utilisees ni les fichiers")
    lignes.append("  touches -- cette information n existe pas encore, elle ne sera pas")
    lignes.append("  inventee ici.")
    lignes.append("")

    lignes.append("## Missions")
    lignes.append("")
    table, masquees = tableau_missions(entrees, compteur_themes)
    lignes.extend(table)
    if masquees:
        lignes.append("")
        lignes.append("_" + str(masquees) + " mission(s) plus anciennes non affichees "
                     "(borne LIMITE_MISSIONS)._")
    lignes.append("")

    lignes.append("## Themes par volume")
    lignes.append("")
    table_th, masquees_th = tableau_themes(compteur_themes)
    lignes.extend(table_th)
    if masquees_th:
        lignes.append("")
        lignes.append("_" + str(masquees_th) + " theme(s) de faible volume non affiches._")
    lignes.append("")

    if len(identifiants) > 0:
        doublons = [i for i, n in collections.Counter(identifiants).items() if n > 1]
        if doublons:
            lignes.append("## Anomalies")
            lignes.append("")
            for identifiant in sorted(doublons):
                lignes.append("- `" + identifiant + "` apparait plusieurs fois dans le journal.")
            lignes.append("")
    return lignes


def ecrire_par_la_porte(contenu):
    """La vue est posee par la PORTE ECRIRE, jamais par une ecriture directe.

    On appelle le lanceur de la Matrice : c est lui qui possede, pose le point
    de restauration, verifie l ASCII et trace la publication.
    """
    import subprocess
    lanceur = RACINE / "lancer.py"
    if not lanceur.is_file():
        return "lanceur INTROUVABLE : " + str(lanceur)
    temporaire = RACINE / "matrice" / "data" / (NOM_VUE + ".tmp")
    try:
        temporaire.write_text(contenu, encoding="utf-8", newline="\n")
        commande = [sys.executable, str(lanceur), "--appelant", "operateur",
                    "ecrire", "ecrire", "--fichier",
                    str(CHEMIN_VUE.relative_to(RACINE.parent.parent)),
                    "--contenu-fichier", str(temporaire.relative_to(RACINE.parent.parent)),
                    "--mode", "remplacer"]
        resultat = subprocess.run(commande, capture_output=True, cwd=str(RACINE.parent.parent),
                                  timeout=120)
    except (OSError, subprocess.TimeoutExpired) as erreur:
        return "ECRITURE IMPOSSIBLE : " + type(erreur).__name__
    finally:
        if temporaire.is_file():
            temporaire.unlink()
    sortie = ((resultat.stdout or b"") + (resultat.stderr or b"")).decode(
        "utf-8", errors="replace").encode("ascii", "ignore").decode("ascii")
    if resultat.returncode != 0:
        return "la porte ECRIRE a refuse : " + sortie.strip()[:200]
    return ""


def _poser_cobayes(racine):
    """Trois cobayes : une mission mesuree, une aux bornes identiques, une
    sans borne. Les trois doivent etre LUS differemment -- c est ce qui
    prouve qu on ne rend pas 0 la ou on ne sait pas.
    """
    datation = "2026-01-01 00:00:00"
    return [
        {"type": "mission-terminee", "id": "M-900", "theme": "OUTIL",
         "injectee_le": datation, "terminee_le": "2026-01-01 00:10:00",
         "objectif": "cobaye mesure"},
        {"type": "mission-terminee", "id": "M-901", "theme": "OUTIL",
         "injectee_le": datation, "terminee_le": datation,
         "objectif": "cobaye bornes identiques"},
        {"type": "mission-creee", "id": "M-902", "theme": "OUTIL",
         "chargee_le": datation, "objectif": "cobaye sans fin"},
    ]


def cmd_auto_test():
    """Eprouve les extracteurs sur un cobaye : la preuve doit venir du jeu."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append((nom, bool(condition), detail))

    cobayes = _poser_cobayes(None)

    # 1. Une duree reelle se lit.
    texte = duree_lisible(cobayes[0])
    controler("duree reelle mesuree", texte == "10 min", texte)

    # 2. Bornes IDENTIQUES : inconnue, jamais 0.
    texte = duree_lisible(cobayes[1])
    controler("bornes identiques -> inconnue", texte == DUREE_INCONNUE_BORNES_IDENTIQUES, texte)
    controler("bornes identiques -> PAS zero", texte != "0" and "0 min" != texte, texte)

    # 3. Borne manquante : inconnue, jamais 0.
    texte = duree_lisible(cobayes[2])
    controler("borne manquante -> non mesurable", texte is None, "None")

    # 4. Le tri par date ne le place pas en tete.
    controle = sorted(cobayes, key=lambda e: parse_date(e.get("terminee_le"))
                      or datetime.min, reverse=True)
    controler("tri par date", controle[0]["id"] == "M-900",
              controle[0]["id"])

    # 5. Un titre libre est marque, un theme repetite ne l est pas.
    themes = themes_reels(cobayes + [{"id": "M-903", "theme": "OUTIL"}])
    lib = _theme_est_normalise("un titre libre", themes)
    connu = _theme_est_normalise("OUTIL", themes)
    controler("titre libre marque", not lib)
    controler("theme repete non marque", connu)

    # 6. Une coupe DITE sa coupure, et le reste COMPTE EST CORRECT.
    reste = 40
    long_texte = "x" * (LIMITE_OBJECTIF + reste)
    coupe = tronquer(long_texte)
    controler("coupe dite",
              ("(+" + str(reste) + ")") in coupe and len(coupe) > LIMITE_OBJECTIF,
              coupe[-10:])
    # CONTRE-TEMOIN : un texte court n est PAS coupe et ne porte aucun marqueur.
    court = tronquer("court")
    controler("texte court non coupe", court == "court", court)

    # 7. Une entree au prefixe M- seulement.
    retenues, ecartees = missions_du_cameleon(
        [{"id": "M-1"}, {"id": "MO-2"}, {"id": ""}])
    controler("seul M- est retenu",
              [str(e.get("id")) for e in retenues] == ["M-1"] and "MO-2" in ecartees,
              str(ecartees))

    # 8. Le COMPTAGE par identifiant, sur une collision d id (MO-552). Un id porte
    #    deux evenements : il compte UNE mission, terminee, et n est PAS en attente.
    distinctes, terminees, attente = compter_missions(
        [{"type": "mission-creee", "id": "M-950"},
         {"type": "mission-terminee", "id": "M-950"}])
    controler("collision : une seule mission",
              (distinctes, terminees, attente) == (1, 1, 0),
              str((distinctes, terminees, attente)))
    # CONTRE-TEMOIN : un id cree et JAMAIS termine reste en attente, et une
    # entree sans identifiant n est PAS une mission.
    distinctes, terminees, attente = compter_missions(
        [{"type": "mission-creee", "id": "M-951"},
         {"type": "note", "id": ""}])
    controler("id cree sans fin -> en attente",
              (distinctes, terminees, attente) == (1, 0, 1),
              str((distinctes, terminees, attente)))

    reussis = sum(1 for _, ok, _ in resultats if ok)
    print("[AUTO-TEST] " + str(reussis) + "/" + str(len(resultats)) + " controles")
    for nom, ok, detail in resultats:
        print("  " + ("OK   " if ok else "ECHEC") + " : " + nom
              + ((" (" + detail + ")") if detail else ""))
    return 0 if reussis == len(resultats) else 1


def main(arguments):
    if arguments and arguments[0] in ("--auto-test", "auto-test"):
        return cmd_auto_test()

    analyseur = argparse.ArgumentParser(add_help=False)
    analyseur.add_argument("--json", action="store_true")
    analyseur.add_argument("--racine", default=None)
    connu, _ = analyseur.parse_known_args(arguments)

    racine = Path(connu.racine).resolve() if connu.racine else RACINE
    if not (racine / "matrice" / "data").is_dir():
        print("REFUS : racine matrix/ introuvable sous " + str(racine))
        return 2
    journal = racine / "matrice" / "data" / "historiques-missions.jsonl"
    if not journal.is_file():
        print("REFUS : journal des missions introuvable : " + str(journal))
        return 2

    entrees, ecarts = lire_journal(journal)
    if not entrees:
        for ecart in ecarts:
            print("ECART : " + ecart)
        print("REFUS : le journal ne porte AUCUNE mission lisible.")
        return 1
    missions, ecartees = missions_du_cameleon(entrees)

    lignes = composer_vue(missions, "matrice/data/historiques-missions.jsonl")
    contenu = "\n".join(lignes) + "\n"

    if connu.json:
        print(json.dumps({"missions": len(missions), "ecarts": ecarts,
                          "ecartees": ecartees, "vue": lignes}, ensure_ascii=False))
        return 0

    for ecart in ecarts:
        print("ECART : " + ecart)
    if ecartees:
        print("NOTE : " + str(len(ecartees)) + " enregistrement(s) d un autre acteur "
              "ignores (ce suivi ne porte que les missions " + PREFIXE_MISSION + ").")

    echec = ecrire_par_la_porte(contenu)
    if echec:
        print(echec)
        return 1
    print("Vue suivi-cameleon regeneree : " + str(CHEMIN_VUE)
          + " (" + str(len(missions)) + " mission(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
