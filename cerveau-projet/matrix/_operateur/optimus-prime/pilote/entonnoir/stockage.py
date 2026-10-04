"""Stockage de l'entonnoir : charger, enregistrer, horodater.

NOMMAGE : ce module s'appelle stockage.py (PAS commun.py) pour ne pas entrer
en collision avec les modules du pilote (le script importe depuis son dossier).
Chaque fonction fait UNE chose (convention-architecture-outils).
"""
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

REPERTOIRE_ENTONNOIR = Path(__file__).resolve().parent
REPERTOIRE_PILOTE = REPERTOIRE_ENTONNOIR.parent
if REPERTOIRE_PILOTE.name != "pilote":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_ENTONNOIR) + " n'est pas dans pilote/"
    )

try:
    from listes import (CHAMP_SOURCE_TRACE, NOM_ENTONNOIR, PREFIXE_ITEM, SOURCES)
except ImportError:  # importe comme paquet (depuis le pilote) : chemin complet
    from entonnoir.listes import (CHAMP_SOURCE_TRACE, NOM_ENTONNOIR, PREFIXE_ITEM,
                                  SOURCES)

CHEMIN_ENTONNOIR = REPERTOIRE_PILOTE / NOM_ENTONNOIR

ENCODAGE = "utf-8"
INDENTATION_JSON = 2


def verifier_famille(identifiant):
    """Refuse un id qui n'appartient PAS a la famille de CET entonnoir (CV-009).

    Pourquoi une garde ici : les deux entonnoirs (Optimus / cameleon) sont deux
    copies du meme outil, donc un id de l'autre flux ne se distingue de rien --
    il repondait simplement "Mission inconnue", ce qui ressemble a un oubli de
    saisie au lieu d'un id etranger. Un id hors famille est un ECART, pas une
    absence : on le dit (code 2, aucune ecriture).
    """
    if identifiant.startswith(PREFIXE_ITEM):
        return 0, ""
    return 2, (
        "Identifiant hors famille : " + repr(identifiant) + " (attendu "
        + PREFIXE_ITEM + "NNN pour cet entonnoir) -- un item de l'autre "
        "entonnoir ne se manipule pas ici."
    )


def separer_source(source):
    """Separe une source LEGACY (texte libre) en (provenance FERMEE, trace).

    Une provenance CONNUE suivie d un separateur (espace, tiret, parenthese,
    deux-points) ouvre la trace ; une source deja nue est rendue INCHANGEE avec
    une trace vide (idempotent) ; une source INCONNUE est rendue TELLE QUELLE
    avec une provenance vide -- jamais une conversion muette qui perdrait la
    trace. Une provenance vide DIT que le split n a pas eu lieu : c est
    l appelant qui decide quoi en faire, pas cette fonction.
    """
    texte = (source or "").strip()
    if not texte:
        return "", ""
    if texte in SOURCES:
        return texte, ""
    for provenance in SOURCES:
        if not texte.startswith(provenance):
            continue
        reste = texte[len(provenance):]
        if reste and reste[0] in " -(:":
            return provenance, reste.strip(" -:")
    return "", texte


def reparer_sources(etat):
    """Applique l auto-soin des sources LEGACY sur TOUT l etat de l entonnoir.

    Le BRIN porte des COPIES des missions des files (tresse.fonctions copie par
    `dict(m)`) : reparer les seules files laisserait le brin mentir -- or c est
    le BRIN que lit l enchainement. On reparcourt donc tout l etat.
    Idempotent : un item qui porte deja CHAMP_SOURCE_TRACE n est jamais retouche.
    Rend le nombre d items repares (0 quand l etat est deja sain).
    """
    repares = 0

    def parcourir(noeud):
        nonlocal repares
        if isinstance(noeud, dict):
            if "source" in noeud and CHAMP_SOURCE_TRACE not in noeud:
                provenance, trace = separer_source(noeud.get("source"))
                if provenance:
                    noeud["source"] = provenance
                    if trace:
                        noeud[CHAMP_SOURCE_TRACE] = trace
                    repares += 1
            for valeur in noeud.values():
                parcourir(valeur)
        elif isinstance(noeud, list):
            for valeur in noeud:
                parcourir(valeur)

    parcourir(etat)
    return repares


def normaliser_chargement(etat):
    """AUTO-SOIN a la lecture : l auto-validation est un INDEX d ids, pas une COPIE.

    Une mission presente dans deux listes = DEUX verites, et le brin se BLOQUE
    dessus (mesure MO-175 : tresser ne rend jamais la main quand un id vit dans
    deux files). Une file legacy est donc CONVERTIE en index et RETIREE des files :
    la mission ne vit plus qu a UN domicile.
    """
    try:
        from listes import (CHAMP_AUTO_VALIDATION, CLE_AUTO_VALIDEES,
                            CLE_LEGACY_AUTO_VALIDEE, VERDICT_AUTO)
    except ImportError:
        from entonnoir.listes import (CHAMP_AUTO_VALIDATION, CLE_AUTO_VALIDEES,
                                      CLE_LEGACY_AUTO_VALIDEE, VERDICT_AUTO)
    files = etat.get("files")
    index = list(etat.get(CLE_AUTO_VALIDEES) or [])
    if isinstance(files, dict):
        legacy = files.pop(CLE_LEGACY_AUTO_VALIDEE, None) or []
        for missions in list(files.values()) + [legacy]:
            for mission in missions or []:
                if not isinstance(mission, dict):
                    continue
                if mission.get(CHAMP_AUTO_VALIDATION) != VERDICT_AUTO:
                    continue
                if mission.get("id") and mission["id"] not in index:
                    index.append(mission["id"])
    etat.setdefault("files", {})
    if index:
        etat[CLE_AUTO_VALIDEES] = index
    # SOURCE (F1, 2026-09-19) : auto-soin des sources LEGACY -- la provenance
    # FERMEE dans `source`, la trace libre dans CHAMP_SOURCE_TRACE. Garde
    # d IDEMPOTENCE dans la fonction : un etat deja repare n est pas retouche.
    reparer_sources(etat)
    return etat


def charger_entonnoir():
    """Retourne l'etat de l'entonnoir, ou l'etat initial si le fichier n'existe pas.

    Echelon 0 : le vrac. Echelons 1-2 : une file PAR TYPE, rangee par categorie.
    """
    if not CHEMIN_ENTONNOIR.exists():
        return {"vrac": [], "files": {}, "compteur": 0}
    with open(CHEMIN_ENTONNOIR, "r", encoding=ENCODAGE) as flux:
        return normaliser_chargement(json.load(flux))


# Les deux champs que le TISSAGE pose sur chaque copie du brin. Ils ne font
# PAS partie de l identite d un item : un alignement doit pouvoir dire "rien n a
# bouge" sans se pieger lui-meme, donc ils sont exclus de toute comparaison.
CHAMPS_TISSAGE = ("position_brin", "tresse_le")


def signature_brin(brin):
    """L IDENTITE d un brin, hors horodatage de tissage.

    On compare la SEQUENCE DES SIGNAIRES, id par id, et le CONTENU utile de
    chaque item (theme, objectif, urgence, categorie, role, type...). Les deux
    champs de tissage sont exclus : les comparer ferait croire a un changement a
    chaque appel, puisque `marquer_brin` y met l heure du jour -- le brin serait
    alors retisse en boucle, sans fin.

    Pourquoi le contenu ET pas seulement les ids : le brin porte des COPIES
    (`tresser` fait `dict(m)`). Un item corrige sur place garde le meme id, donc
    une comparaison par ids seule laisserait le brin servir l ANCIEN texte -- la
    copie fantome que `corriger/entry.py` a lui-meme documentee.
    """
    signature = []
    for mission in brin or []:
        contenu = {cle: valeur for cle, valeur in mission.items()
                   if cle not in CHAMPS_TISSAGE}
        signature.append((mission.get("id"), tuple(sorted(
            (cle, repr(valeur)) for cle, valeur in contenu.items()))))
    return tuple(signature)


def aligner_brin(etat):
    """Re-derive le BRIN des files, et SEULEMENT quand il a bouge (C-001).

    LA CORVEE C-001 (2026-09-25, jamais executee) : le brin ne se retissait
    qu a la main, sur deux gestes seulement (`corriger`, `retirer`). Les huit
    autres verbes -- dont `classer`, qui fait passer un item du vrac a SA file --
    laissaient donc le brin perime, et le MAILLON 5 de la non-regression
    (brin-perime) le payait : 2 refus le 2026-09-25, et un item sur 25 ne le
    portait pas. Elle attendait "le depot tisse lui-meme le brin".

    ICI, au SEUL point d ecriture de l entonnoir. Pas dans chaque verbe : dix
    copies de la regle divergeraient (M-076), et il en resterait toujours une
    oubliee -- c est exactement ce qui est arrive.

    DEUX GARDES.
    L IDEMPOTENCE : si la signature du brin courant est celle qu on
    recomputerait, on ne touche a rien et on nerafraichit PAS `tresse_le`.
    Sans elle, chaque enregistrement retisserait le brin, donc le dirait
    vient d etre tresse alors que personne n a bouge -- et le maillon du
   _non-regression_ verrait un brin qui bouge tout seul.
    L INDEPENDANCE : l import de la tresse est DIFFERE (comme dans
    `retirer/fonctions.py`), sinon `tresse.fonctions` -- qui importe `horodater`
    d ici -- et ce module s importent mutuellement au chargement.

    Rend (aligne, nombre) : `aligne` dit si le brin a ete REFAIT, `nombre` la
    taille du brin aligne (0 quand rien n a bouge, pour ne pas faire croire a
    un changement).
    """
    from tresse.fonctions import marquer_brin, tresser

    brin = marquer_brin(tresser(etat.get("files", {})))
    if "brin" in etat and signature_brin(etat["brin"]) == signature_brin(brin):
        return False, len(etat["brin"])
    etat["brin"] = brin
    return True, len(brin)


def enregistrer_entonnoir(etat):
    """Ecrit l'etat de l'entonnoir de facon atomique (tmp + REMPLACEMENT, LF forces)."""
    aligner_brin(etat)
    chemin_tmp = CHEMIN_ENTONNOIR.with_name(NOM_ENTONNOIR + ".tmp")
    with open(chemin_tmp, "w", encoding=ENCODAGE, newline="\n") as flux:
        json.dump(etat, flux, indent=INDENTATION_JSON, ensure_ascii=True)
        flux.write("\n")
    os.replace(chemin_tmp, CHEMIN_ENTONNOIR)


def empreinte_texte(texte):
    """L empreinte SHA-256 d un TEXTE (la provenance du vote, EO-491).

    Meme choix que l empreinte d integrite (convention-integrite-sha256), mais
    sur une chaine et non sur un fichier : c est ce qu il faut pour dire SUR
    QUEL TEXTE un avis a ete rendu. Cette fonction est le SEUL domicile de ce
    calcul dans l entonnoir (M-076).
    """
    return hashlib.sha256((texte or "").encode("utf-8")).hexdigest()


def texte_juge(theme, objectif, type_propose=""):
    """Le TEXTE que l evaluateur lit : theme + objectif + type (UN SEUL domicile).

    L evaluateur assemble exactement ces trois champs
    (`" ".join([theme, objectif, type_propose])`,
    super-combos/combos/outils/evaluer-auto-validation.py, ligne 217). Une
    empreinte de provenance doit porter CE TEXTE et lui seul : une empreinte de
    l objectif seul ne voyait pas une correction du TITRE, alors que le titre
    est juge -- mesure du 2026-10-01 (EO-491 livre, verifie le jour meme sur un
    item reel : `correction --theme` laissait le vote fige malgre un texte
    soumis au juge different).
    """
    return " ".join([theme or "", objectif or "", type_propose or ""])


def horodater():
    """Retourne la date-heure locale au format des journaux."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def trouver_item(etat, identifiant):
    """Retourne (mission, type_file) pour un item, a TOUS les echelons.

    Le type_file (cle de la file, vide si l item est encore au vrac) est ce qui
    permet de valider les champs FERMES PAR TYPE -- la liste ou se ranger depend
    de la file ou l item vit.

    DOMICILE (EO-313) : ce chercheur etait defini dans `retiqueter/fonctions.py`,
    son premier consommateur. La porte `preparer` en a besoin AUSSI : une seule
    copie, ici, avec le reste du stockage -- deux copies divergeraient (M-076).
    """
    for mission in etat.get("vrac", []):
        if mission.get("id") == identifiant:
            return mission, ""
    for type_file, missions in (etat.get("files") or {}).items():
        for mission in missions:
            if mission.get("id") == identifiant:
                return mission, type_file
    return None, ""
