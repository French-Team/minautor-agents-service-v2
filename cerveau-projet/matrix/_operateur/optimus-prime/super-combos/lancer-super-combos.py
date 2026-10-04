#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lancer-super-combos.py -- Lanceur de super-combos par numero

Permet de lancer un super-combos par son numero numerote (sc-001, sc-002,
contrat de nommage CV-008 -- BDD conventions-matrice). Les anciennes formes
"#1" et "1" restent
acceptees et sont normalisees vers sc-001. La casse est libre (SC-001 ou
sc-001) : la forme canonique est en MINUSCULES (le `C-` majuscule est reserve
au champ `constat` fige, regle CV-009).

LE VERBE VIENT DU REGISTRE (correction MO-071, EO-114). Le lanceur n'ecrit plus
"executer" en dur : chaque entree de `registry.json` declare son CONTRAT DE
LANCEMENT, et c'est lui qui est lu.

    "verbe"  : le verbe par DEFAUT de l'objet (peut etre VIDE : un objet sans
               entree unique, comme un cycle a phases, n'en a pas)
    "verbes" : la liste des verbes ACCEPTES (la seule source de verite)

Un objet sans contrat, un contrat incoherent, ou un verbe demande hors contrat
est REFUSE NOMMEMENT (code 2) : jamais un verbe invente, jamais un echec muet.
C'est ce qui empeche un super-combo de naitre inlancable par construction (le
registre est verifie par `creer-combo.py verifier`, qui exige ce contrat).

Usage:
  python lancer-super-combos.py --numero <SC-NNN> [--verbe <verbe>] [--fichier <fichier>] [--mission <id>] [args du super-combo...]
  python lancer-super-combos.py --lister

Les arguments NON reconnus par le lanceur sont transmis TELS QUELS au
super-combo : c'est ainsi qu'on lui donne ses propres options (ex : les phases
de sc-002 exigent une phrase et --type/--gravite/--frequence).
"""

import sys
import json
import argparse
import subprocess
import time

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

# Le chemin du registre UNIQUE des usages se LIT a son domicile (M-076) : ce
# lanceur n a pas a savoir ou la maison range ses usages -- une valeur recopiee
# derive en silence, et c est elle qui porterait la PREUVE de passage.
from round_servi import CHEMIN_SAC_A_DOS  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())

from pathlib import Path


REGISTRY_PATH = Path(__file__).parent / "registry.json"

# Contrat de nommage CV-008 : les super-combos sont numerotes sc-001, sc-002...
# MINUSCULES (regle CV-009) : `C-` majuscule = champ constat fige, jamais un id.
PREFIXE_SUPER_COMBO = "sc-"
LARGEUR_NUMERO = 3

# Contrat de LANCEMENT (MO-071) : les deux champs lus dans le registre.
CLE_CONTRAT_VERBE = "verbe"
CLE_CONTRAT_VERBES = "verbes"

CODE_INCONNU = 1
CODE_REFUS = 2

# --- LA TRACE DE PASSAGE (MO-491, demande du createur 2026-09-26) ------------
# < Injecter des PROCESS qui LANCENT les super-combos quand on corrige, ameliore
# ou modifie des fichiers et les flux, AVEC LA PREUVE de leur passage. >
# Mesure du 2026-09-29 : la PREUVE N EXISTAIT PAS. Le registre unique des usages
# (matrice/data/usages-outils-combos.jsonl, 65686 lignes) ne portait qu UNE
# occurrence d un super-combo, et ce lanceur n ecrivait aucun journal : un passage
# ne laissait donc aucune trace. Un passage se NOTE desormais la ou les usages se
# notent DEJA -- par la PORTE `bdd-usages` -- jamais dans un second journal (un
# second registre serait un second domicile, M-076). Le chemin du registre se LIT
# chez son domicile (`round_servi.CHEMIN_SAC_A_DOS`) : il n est jamais recopie.
TAG_PASSAGE = "super-combo"
OUTIL_PORTE_USAGES = "bdd-usages"
APPELANT_ZONE = "operateur"
CLE_CONTRAT_COMBOS = "combos"


def charger_registry() -> dict:
    """Charger le registre des super-combos."""
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"super-combos": []}


def normaliser_numero(numero):
    """Normalise vers sc-<NNN> : accepte sc-001, SC-001, 1 et l'ancien #1."""
    brut = str(numero).strip().lstrip("#").lower()
    if brut.startswith(PREFIXE_SUPER_COMBO):
        return brut
    if brut.isdigit():
        return PREFIXE_SUPER_COMBO + brut.zfill(LARGEUR_NUMERO)
    return brut


def resoudre_lancement(combo, verbe_demande=""):
    """Retourne (code, verbe, message) : le verbe a lancer, ou un refus NOMME.

    Fonction PURE (aucun disque, aucun sous-processus) : elle se prouve sur des
    entrees piegees sans rien lancer. Trois refus, tous NOMMES :
      - l'entree ne declare aucun contrat (champs "verbe"/"verbes") ;
      - le "verbe" par defaut est absent de sa propre liste "verbes" ;
      - le verbe demande n'est pas dans la liste (ou il n'y a pas de defaut).
    """
    identifiant = combo.get("id", "?")
    verbes = [verbe for verbe in (combo.get(CLE_CONTRAT_VERBES) or []) if verbe]
    if not verbes:
        return (
            CODE_REFUS, "",
            "le super-combo " + identifiant + " ne declare AUCUN contrat de lancement "
            "dans registry.json (champs \"" + CLE_CONTRAT_VERBE + "\"/\"" + CLE_CONTRAT_VERBES
            + "\") : le poser par la porte (creer-combo.py verifier le refuse desormais)",
        )
    if verbe_demande:
        if verbe_demande not in verbes:
            return (
                CODE_REFUS, "",
                "verbe \"" + verbe_demande + "\" hors contrat de " + identifiant
                + " -- verbes acceptes : " + ", ".join(verbes),
            )
        return 0, verbe_demande, ""
    defaut = combo.get(CLE_CONTRAT_VERBE, "")
    if not defaut:
        return (
            CODE_REFUS, "",
            "le super-combo " + identifiant + " n'a pas d'entree unique : choisir un verbe "
            "avec --verbe <" + "|".join(verbes) + ">",
        )
    if defaut not in verbes:
        return (
            CODE_REFUS, "",
            "contrat incoherent pour " + identifiant + " : \"" + CLE_CONTRAT_VERBE + "\" = "
            + defaut + " est absent de \"" + CLE_CONTRAT_VERBES + "\" (" + ", ".join(verbes) + ")",
        )
    return 0, defaut, ""


def lister_super_combos():
    """Lister tous les super-combos disponibles (numerotes + contrat de lancement)."""
    registry = charger_registry()

    print("=" * 60)
    print("SUPER-COMBOS DISPONIBLES (numerotes, CV-008)")
    print("=" * 60)
    print()

    for combo in registry.get("super-combos", []):
        # Lecture defensive : un champ manquant est SIGNALE, il ne fait jamais
        # planter le lanceur (trou attrape le 2026-09-13 : sc-002 n'avait
        # jamais ete enregistre, seuls id/nom/fichier existaient).
        manquants = [c for c in ("description", "phases") if not combo.get(c)]
        if not combo.get(CLE_CONTRAT_VERBES):
            manquants.append(CLE_CONTRAT_VERBES)
        print("  " + str(combo.get("id", "?")).ljust(7) + " : " + str(combo.get("nom", "?")))
        print("          " + str(combo.get("description", "(description manquante)")))
        print("          Phases: " + (", ".join(combo.get("phases", [])) or "(non declarees)"))
        defaut = combo.get(CLE_CONTRAT_VERBE, "")
        verbes = combo.get(CLE_CONTRAT_VERBES) or []
        print("          Lancement: " + ("defaut " + defaut if defaut else "aucune entree unique")
              + (" -- verbes : " + ", ".join(verbes) if verbes else ""))
        if manquants:
            print("          ECART registre : champ(s) manquant(s) : " + ", ".join(manquants))
        print()

    print("Utilisation : python lancer-super-combos.py --numero <sc-NNN> [--verbe <verbe>]")
    print("Exemple : python lancer-super-combos.py --numero sc-001 --fichier mon_fichier.py")
    print("Exemple : python lancer-super-combos.py --numero sc-002 --verbe detecter \"Quand X, Y, car Z\" --type outil --gravite mineure --frequence ponctuelle")


def lancer_super_combos(numero, verbe_demande="", fichier=None, mission=None, extras=None):
    """Lancer un super-combos par son numero (sc-001, sc-002...)."""
    extras = list(extras or [])
    registry = charger_registry()
    numero = normaliser_numero(numero)

    combo = None
    for candidat in registry.get("super-combos", []):
        if candidat.get("id") == numero:
            combo = candidat
            break

    if not combo:
        print("ERREUR : Super-combos " + numero + " introuvable")
        return CODE_INCONNU

    print("Lancement du super-combos " + combo["id"] + " : " + str(combo.get("nom", "")))
    print()

    code, verbe, message = resoudre_lancement(combo, verbe_demande)
    if code != 0:
        print("REFUS : " + message)
        return code

    script_path = Path(__file__).parent / combo["fichier"]
    cmd = [sys.executable, str(script_path), verbe]

    if fichier:
        cmd.extend(["--fichier", fichier])

    if mission:
        cmd.extend(["--mission", mission])

    cmd.extend(extras)

    debut = time.monotonic()
    result = lancer_enfant(cmd, capture_output=True, text=True)
    duree_ms = int((time.monotonic() - debut) * 1000)

    if result.returncode == 0:
        print(result.stdout)
    else:
        # Un echec doit DIRE pourquoi. Le diagnostic d'un super-combo peut
        # partir sur STDOUT (sc-002 repond "Phase inconnue: executer" sur
        # stdout) : afficher stderr seul perdait le message et laissait un
        # "ERREUR :" vide devant l'agent (trou mesure le 2026-09-13, MO-067).
        print("ERREUR (code " + str(result.returncode) + ") :")
        for nom_flux, texte in (("stdout", result.stdout), ("stderr", result.stderr)):
            if texte and texte.strip():
                print("  [" + nom_flux + "] " + texte.strip())
        if not (result.stdout and result.stdout.strip()) and not (result.stderr and result.stderr.strip()):
            print("  (aucun message : le script n'a rien dit -- verifier " + str(script_path) + ")")

    # LA TRACE EST ECRITE QUEL QUE SOIT LE CODE : un passage qui a RATE laisse
    # aussi sa trace (elle porte son code). L echec de la notation n interrompt
    # jamais le lancement (doctrine : un outil ne bloque pas sur sa propre
    # comptabilite) -- mais il est DIT, jamais tu.
    noter_le_passage(combo, verbe, fichier, mission, result.returncode, duree_ms)
    return result.returncode


def chemin_registre_usages():
    """Le chemin du registre UNIQUE des usages, lu a son domicile (M-076)."""
    return Path(_RACINE_LANCEMENT).joinpath(*CHEMIN_SAC_A_DOS)


def noter_le_passage(combo, verbe, fichier, mission, code, duree_ms):
    """NOTE le passage d un super-combo par la PORTE des usages (MO-491).

    < La preuve de leur passage > : une ligne du registre qui NOMME le combo, le
    verbe, la cible et la MISSION (tag `mo-xxxx` ET detail -- sans elle, la preuve
    d un round ne se retrouve plus). Trois garanties : la PORTE `bdd-usages` est
    le SEUL ecrivain du registre (aucun second journal) ; la notation n echoue
    JAMAIS de facon bloquante, un passage qui a eu lieu ne se perd pas parce qu une
    notation a rate ; un echec de notation est DIT, jamais tu.
    """
    identifiant = str(combo.get("id", "?"))
    tags = [TAG_PASSAGE]
    detail = "cible : " + (str(fichier) if fichier else "(aucune)")
    mission_propre = str(mission or "").strip()
    if mission_propre:
        tags.append(mission_propre.lower())
        detail = "mission " + mission_propre + " ; " + detail
    contenu = [sys.executable, str(Path(_RACINE_LANCEMENT) / "lancer.py"),
               "--appelant", APPELANT_ZONE, OUTIL_PORTE_USAGES, "noter",
               "--outil", identifiant, "--commande", verbe,
               "--code", str(code), "--duree", str(duree_ms),
               "--tags", ",".join(tags), "--detail", detail]
    try:
        termine = lancer_enfant(contenu, capture_output=True, text=True,
                                encoding="utf-8", errors="replace")
    except OSError as erreur:
        print("passage NON NOTE (" + type(erreur).__name__ + ") : la trace manque pour "
              + identifiant)
        return False
    if termine.returncode != 0:
        print("passage NON NOTE (code " + str(termine.returncode) + ") : la trace manque"
              " pour " + identifiant)
        return False
    return True


def lire_registre_usages():
    """Les lignes du registre des usages, ou None si le registre est INTROUVABLE.

    Rend None -- jamais une liste vide -- pour que l appelant puisse DIRE < je n ai
    pas pu lire > au lieu de conclure < aucun passage > : un registre illisible et
    un registre sans passage ne disent pas la meme chose.
    """
    chemin = chemin_registre_usages()
    if not chemin.is_file():
        return None
    entrees = []
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        try:
            entrees.append(json.loads(ligne))
        except ValueError:
            continue
    return entrees


def _code_reussi(code):
    """Le code porte-t-il un PASSAGE REELLEMENT JOUE ? PURE.

    Mesure EO-484 (2026-09-29) : deux lancements de sc-004 ont rendu code 2
    (usage argparse : arguments non reconnus) et lejugement les lisait
    < passage PROUVE >, avec la cible et la date. Une preuve qui mesure une
    TENTATIVE n est pas une preuve.

    La regle est sobre : REUSSI = code 0. Une entree SANS code (un registre
    ecrit avant la trace, ou une ligne de main levee) n est PAS comptee comme
    reussie : on ne prouve pas un succes qu on n a pas mesure, et une entree
    sans code reste visible dans la sortie sous le mot ECHOUE plutot que
    d etre comptee. Le defaut est donc la PRUDENCE.
    """
    if code is None:
        return False
    if isinstance(code, bool):  # un booleen n est pas un code de sortie
        return False
    if isinstance(code, int):
        return code == 0
    texte = str(code).strip()
    if not texte:
        return False
    try:
        return int(texte) == 0
    except ValueError:
        # Un code non numerique n est pas un succes DEMONTRE : il est dit tel
        # quel par la sortie, jamais converti en preuve.
        return False


def juger_passages(entrees, combos_demandes, mission):
    """PURE : les PREUVES d une mission -- rend (code, passages, manquants).

    Elle prend des ENTREES (le registre deja lu) et une DEMANDE (les combos que le
    round declare pertinents), jamais un chemin : elle se prouve donc sur des
    entrees fabriquees. Un passage se prouve par une entree qui porte le TAG DE
    PASSAGE, le tag de la mission, ET un code 0. Elle rend (code, passages,
    manquants, echoues) : les ECHOUES sont rendues separement pour que
    l appelant les DITE -- un echec muet ne serait qu un demi-defaut.

    AUCUNE DEMANDE, AUCUNE ACCUSATION (code 0) : la fonction ne fabrique pas la
    demande a la place du round -- decider quels combos sont pertinents est un
    JUGEMENT de l agent, et un juge qui invente sa demande accuse au hasard.
    """
    tag_mission = str(mission or "").strip().lower()
    passages = []
    echoues = []
    for entree in entrees or []:
        tags = [str(tag).strip().lower() for tag in (entree.get("tags") or [])]
        if TAG_PASSAGE in tags and tag_mission in tags:
            # EO-484 : le CODE est le juge du passage. Une entree qui porte un
            # code NON nul dit qu on a TENTE le combo, pas qu il a PASSE --
            # sans cette lecture, une sortie de code 2 se lisait < passage PROUVE >
            # et la preuve mesurait une tentative.
            if _code_reussi(entree.get("code")):
                passages.append(entree)
            else:
                echoues.append(entree)
    faits = {str(entree.get("outil", "")) for entree in passages}
    manquants = [str(combo).strip() for combo in (combos_demandes or [])
                 if str(combo).strip() and str(combo).strip() not in faits]
    return (1 if manquants else 0), passages, manquants, echoues


def verifier_les_preuves(mission, combos_demandes):
    """Le VERBE des preuves : lit le registre, JUGE, DIT. Rend un code.

    Code 0 : chaque combo DEMANDE a son passage (ou rien n a ete demande). Code 1 :
    les combos demandes SANS aucun passage sont ACCUSES et NOMMES -- c est cette
    accusation qui fait du passage un PROCESS, au lieu d une consigne qu on peut
    oublier (L-165). Code 2 : le registre est INTROUVABLE (on ne conclut pas
    < aucun passage > sur un fichier qu on n a pas lu).

    EO-484 : un passage ECHOUE est DIT et NOMME, avec son code, et il compte
    comme un combo SANS passage (donc il reste dans l accusation). La preuve
    mesure un passage joue, pas une tentative.
    """
    entrees = lire_registre_usages()
    if entrees is None:
        print("REFUS : le registre des usages est INTROUVABLE -- " + str(chemin_registre_usages()))
        return CODE_REFUS
    code, passages, manquants, echoues = juger_passages(entrees, combos_demandes, mission)
    print("PREUVES DES SUPER-COMBOS -- mission " + str(mission))
    for entree in passages:
        print("  passage PROUVE : " + str(entree.get("outil", "?"))
              + " (" + str(entree.get("commande", "?")) + ") le " + str(entree.get("date", "?"))
              + " -- " + str(entree.get("detail", "")))
    for entree in echoues:
        nom = str(entree.get("outil", "?"))
        if nom in [str(c).strip() for c in (combos_demandes or [])]:
            print("  passage ECHOUE (code " + str(entree.get("code")) + ") : " + nom
                  + " (" + str(entree.get("commande", "?")) + ") le " + str(entree.get("date", "?"))
                  + " -- une tentative ne prouve pas un passage")
    for entree in echoues:
        nom = str(entree.get("outil", "?"))
        if nom not in [str(c).strip() for c in (combos_demandes or [])]:
            print("  passage ECHOUE (code " + str(entree.get("code")) + ") : " + nom
                  + " (" + str(entree.get("commande", "?")) + ") le " + str(entree.get("date", "?")))
    if not combos_demandes:
        print("  aucun combo DEMANDE : rien a prouver (la demande est un jugement du round)")
        return 0
    if manquants:
        print("  ECART : combo(s) demande(s) SANS aucun passage note : " + ", ".join(manquants))
        print("  Le passage se PROUVE : lance-les avec --mission " + str(mission) + ".")
        return code
    print("  preuve COMPLETE : " + str(len(combos_demandes)) + " combo(s) demande(s), tous passes")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Lanceur de super-combos")
    parser.add_argument("--numero", help="Numero du super-combos (sc-001, sc-002, etc.)")
    parser.add_argument("--verbe", default="", help="Verbe a lancer (defaut : celui du registre)")
    parser.add_argument("--fichier", help="Fichier a traiter")
    parser.add_argument("--mission", help="ID de la mission")
    parser.add_argument("--lister", action="store_true", help="Lister les super-combos disponibles")
    parser.add_argument("--preuves", help="Mission a juger : ses super-combos ont-ils un passage NOTE ?")
    parser.add_argument("--combos", help="Combos DEMANDES par --preuves (ex : sc-001,sc-002)")
    # Les arguments NON reconnus sont TRANSMIS au super-combo : c'est ainsi qu'on
    # lui donne ses propres options (les phases de sc-002 en exigent).
    args, extras = parser.parse_known_args()

    # LE VERBE DES PREUVES (MO-491) : il ne lance RIEN, il JUGE. Il est place AVANT
    # le lancement -- et avant le --lister -- parce qu un round vient chercher une
    # PREUVE, pas un catalogue.
    if args.preuves:
        demandes = [morceau for morceau in str(args.combos or "").split(",") if morceau.strip()]
        return verifier_les_preuves(args.preuves, demandes)

    if args.lister or not args.numero:
        lister_super_combos()
        return 0

    return lancer_super_combos(args.numero, args.verbe, args.fichier, args.mission, extras)


if __name__ == "__main__":
    sys.exit(main())
