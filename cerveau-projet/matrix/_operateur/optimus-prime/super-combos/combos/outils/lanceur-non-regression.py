#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lanceur-non-regression.py -- Non-regression zone Optimus en une commande (M-104)

ORDRE IMPOSE (correction 2026-09-14, friction 29) : on MODIFIE le code, on MET A
JOUR ce que la suite lit, on LANCE. Le PRE-VOL (etape 0) verifie ce troisieme
point AVANT toute action couteuse -- frictions qualifiees, fichiers TRACES,
remorque attellee -- et s'ARRETE en nommant QUOI mettre a jour et PAR QUELLE
PORTE. Sans lui, on parcourait tout avant d'apprendre qu'une friction n'etait pas
qualifiee, puis on corrigeait, puis on relancait : la correction etait payee DEUX
fois (constate deux fois le 2026-09-14).

Rejoue : PRE-VOL (integrite + activite/frictions + remorque)
+ py_compile (outils .py) + tester-theme (3 themes) + cartographe
+ garde-ascii (zone) + compilation des scripts de zone + PREFIXES (CV-009/CV-011)
+ FLUX (imperatif 62, E-095) + VERIFIER SANS ATTENDRE (MO-062)
+ TRACE suivi-optimus (un debut + une fin par mission, empreinte)
+ CROISEMENT file du pilote <-> journal (une mission menee SANS entrer dans le
 marbre crie -- `verifier` seul ne le voit pas, MO-096)
+ ANTI-SPAM MISSIONS (le depot d'une vigie est borne par mission, MO-070/MO-073)
+ CHAPITRES ESPION (l'annonce d'une passe est celle qu'elle produit, MO-072)
+ EXEMPTIONS VISIBLES (une exemption muette est un angle mort, MO-075)
+ ROTATION JOURNAL (borner un journal ne perd rien, l'archive est dans le connu, MO-077)
+ HISTORIQUE / OBSERVATIONS / PASSES NON REDONDANTS (un etat n'est pas un fait,
 MO-080, MO-081, MO-082) + SUPER-COMBO sc-001 (un controle qui peut echouer, MO-083)
+ CADENCE (le battement REEL contre la cadence DECLAREE, friction 28, MO-084)
+ PARCOURS (tout theme `pret` est ROUTE, et toute route mene quelque part, MO-087)
+ CHEMINS (aucun `parents[N]` nu, la racine se DETECTE par marqueur, MO-088)
+ CARTES D'IDENTITE (tout document dit QUOI il est, MO-089)
+ SUIVI DU PILOTE (la VUE du pilote est recalculee et la Table 0 doit etre vide --
 le silence, l'age, la forme du lot et une trace absente sont surveilles, EO-273)
+ ROLES (chaque type a une POSTURE reelle du vivier, et le pilote l'INJECTE,
 MAILLON 2/5 de la revision)
+ RECHERCHE (le pilote INJECTE la question au moteur, une seule derivation
 partagee, deux chemins par flux, le Flux 1 jamais ouvert, EO-131)
+ FICHE (courte sous un PLAFOND declare, roles et parcours NOMMES, et AUCUNE
 regle immuable perdue dans l'allegement, EO-124)
+ RATTRAPAGE (le pilote COMBLE a chaque cloture les fichiers notes au DOMICILE et
 muets au journal, AVANT la vue qui ne lit que le journal, EO-133).
+ JUMEAUX (deux domiciles declarent le meme nom : une divergence compile
 et change le SENS, MO-175)
+ MIROIRS (les DEUX flancs declarent la MEME chose : chaque litteral lu dans
 les 28 fichiers miroirs des deux pilotes dit la MEME valeur, SAUF si son nom
 est declare LIBRE avec sa raison ; une absence de vocabulaire partage ou une
 divergence non declaree est un ECART, MO-230/EO-224, rendu RECURRENT par EO-225)
+ CROCHETS (la liste fermee et sa convention disent la MEME chose, dans les
 deux sens, et le type transmis appartient a la liste fermee, R5)
+ APPELS NON LIES (un appel orphelin est un NameError en puissance, R5)
+ REFUS NOMME DES OPTIONS INCONNUES (la sonde sc-004 : tout outil qui avale ou
 refuse muettement une option fautive est ACCUSE, et la suite PROUVE qu'elle sait
 rougir sur un cobaye muet en zone jetable, T4 de PB-002, MO-215)
+ TITRE DES ITEMS (le titre d'un item n'est pas une ETIQUETTE : les DEUX entonnoirs
 sont juges par le GARDE DE CHAQUE ARBRE, les deux portes refusent un theme du
 vivier sans laisser naitre d'item, et les cobayes sont rejoues, 2026-09-23)
Verdict OK/KO. code 0 = OK, code 1 = KO.

Bloquants : le controle des PREFIXES du contrat fondamental (CV-009/CV-011) et,
parce qu'ils attrapent chacun une panne invisible, le flux, l'attente, la trace,
le croisement file <-> journal et le TITRE DES ITEMS (une etiquette du vivier
affichee a la place d'une phrase se lit comme un titre : rien ne la montre).
Usage: python lanceur-non-regression.py [--racine <path>]
"""

import sys
import argparse
import py_compile
import subprocess
import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430, premier lot du residu) -------------------
# Mesure du 2026-09-25 (audit-lancements-a-nu) : cet outil portait 51 appels de
# processus A NU -- 45 % du residu d'_operateur a lui seul. Recopier les drapeaux
# 51 fois aurait fait 51 occasions de deriver : le motif est donc LU au domicile
# de la Matrice (`lancement.drapeaux_popen`), et les 51 sites passent par le verbe
# unique ci-dessous. Un seul point porte la regle.
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu) : remontee par
# `.parent` et CONTROLE DU MARQUEUR -- si le dossier ne s appelle pas `matrix`, on
# REFUSE au lieu de deviner (garde-foi L-006, meme forme que verifier-selecteur).
if Path(__file__).resolve().parent.name != "outils":
    raise RuntimeError("Structure inattendue : " + str(Path(__file__).resolve())
                       + " -- l outil n est pas dans son dossier `outils`")
RACINE_MATRICE = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
if RACINE_MATRICE.name != "matrix":
    raise RuntimeError("Structure inattendue : " + str(RACINE_MATRICE)
                       + " n est pas la racine `matrix` de la Matrice (garde-foi L-006)")
DOSSIER_COMMUN = RACINE_MATRICE / "matrice" / "data" / "commun"
if not (DOSSIER_COMMUN / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(DOSSIER_COMMUN)
                       + " ne porte pas le domicile du lancement")
if str(DOSSIER_COMMUN) not in sys.path:
    sys.path.insert(0, str(DOSSIER_COMMUN))
from lancement import drapeaux_popen  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())
import tempfile
from pathlib import Path


def _eprouver_saut_lot(racine):
    """MAILLON 46 (MO-470 / EO-445) : eprouve EN MEMOIRE la porte de saut du lot.

    Charge le DOMICILE du pilote (commun.py) par son CHEMIN (aucun sys.path
    laisse), remplace l ecriture de la file par une fonction vide, et rejoue les
    epreuves qui MORDENT : l ordre SERVI suit le lot (jamais la file, L-151), le
    saut place la visee en tete sans perdre personne, et hors lot / mission morte /
    sans lot sont REFUSES en le nommant. Rend la liste des ecarts (vide = OK).
    """
    import importlib.util
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    # La racine recue peut etre DEJA matrix/ (le maillon lui passe zone.parent.parent,
    # comme le maillon 45) : les TROIS formes sont essayees, jamais une supposee.
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    pilote = matrice / "_operateur" / "optimus-prime" / "pilote"
    chemin = pilote / "commun.py"
    if not chemin.is_file():
        return ["commun.py du pilote INTROUVABLE : " + str(chemin)]
    sys.path.insert(0, str(pilote))
    try:
        specification = importlib.util.spec_from_file_location("commun_saut_lot", chemin)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except Exception as erreur:  # noqa: BLE001
        return ["commun.py ILLISIBLE (" + type(erreur).__name__ + " : "
                + str(erreur)[:60] + ")"]
    finally:
        sys.path.remove(str(pilote))
    module.enregistrer_file = lambda fm: None
    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    def fichier(ordre_file, ids_lot, statuts):
        missions = [{"id": i, "statut": statuts.get(i, module.STATUT_EN_ATTENTE)}
                    for i in ordre_file]
        return {"missions": missions, "lot": {"ids": list(ids_lot)}}

    fm = fichier(["MO-202", "MO-201", "MO-203"], ["MO-201", "MO-202", "MO-203"], {})
    servi = module.prochaine_du_lot(fm)
    ep("ordre-servi-par-le-LOT", servi is not None and servi["id"] == "MO-201",
       "servi " + (servi["id"] if servi else "None") + " (le lot commande, pas la file)")

    code, message = module.avancer_du_lot(fm, "MO-203")
    ep("saut-place-la-visee-en-tete", code == 0 and module.ids_en_lot(fm)[0] == "MO-203",
       "code=" + str(code) + " ids=" + ",".join(module.ids_en_lot(fm)))
    ep("saut-ne-perd-aucune-mission",
       sorted(module.ids_en_lot(fm)) == ["MO-201", "MO-202", "MO-203"],
       "ids=" + ",".join(module.ids_en_lot(fm)))
    servi2 = module.prochaine_du_lot(fm)
    ep("apres-saut-visee-servie", servi2 is not None and servi2["id"] == "MO-203",
       "servi " + (servi2["id"] if servi2 else "None"))

    fm2 = fichier(["MO-201", "MO-202"], ["MO-201", "MO-202"], {})
    code3, message3 = module.avancer_du_lot(fm2, "MO-999")
    ep("hors-lot-REFUSE", code3 == 2 and "HORS du lot" in message3, message3[:70])

    fm3 = fichier(["MO-201", "MO-202"], ["MO-201", "MO-202"],
                  {"MO-202": module.STATUT_TERMINEE})
    code4, message4 = module.avancer_du_lot(fm3, "MO-202")
    ep("mission-morte-REFUSEE", code4 == 2 and "TERMINEE" in message4, message4[:70])

    code5, message5 = module.avancer_du_lot({"missions": [], "lot": None}, "MO-201")
    ep("sans-lot-REFUSE", code5 == 2 and "aucun lot" in message5, message5[:70])
    return ecarts


def _eprouver_fiche(racine):
    """MAILLON 47 (MO-471) : eprouve la FICHE TECHNIQUE DE TRAVAIL EN MEMOIRE.

    Charge injection/fonctions.py (le domicile de la fiche) et verifie, sans rien
    ecrire : la fiche est plus LEGERE que l injection, elle NE PERD RIEN de ce qui
    decide (aucun KO sur une injection coherente), elle MORD sur un champ du NOYAU
    absent, et elle DIT le plafond. Rend la liste des ecarts (vide = OK).
    """
    import importlib.util
    import json as _json
    from pathlib import Path as _Chemin
    NL = chr(10)
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    pilote = matrice / "_operateur" / "optimus-prime" / "pilote"
    chemin = pilote / "injection" / "fonctions.py"
    if not chemin.is_file():
        return ["injection/fonctions.py INTROUVABLE : " + str(chemin)]
    sys.path.insert(0, str(pilote))
    try:
        specification = importlib.util.spec_from_file_location("injection_fonctions_fiche", chemin)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except Exception as erreur:  # noqa: BLE001
        return ["injection/fonctions.py ILLISIBLE (" + type(erreur).__name__ + " : "
                + str(erreur)[:60] + ")"]
    finally:
        sys.path.remove(str(pilote))
    ecarts = []
    plein = {"mission": "MO-900", "theme": "PILOTE", "objectif": "faire X",
             "checklist": ["a"], "role": {"posture": "PILOTE"}, "rappel": "conduis",
             "auto_validation": "auto", "recherche": {"question": "q"},
             "lecons_utiles": [{"lecon": "long " * 200}],
             "themes_utiles": [{"nom": "T"}] * 50, "modes_emploi": [{"nom": "O"}] * 30,
             "profil": {"Pseudo": "p"}, "si_j_etais_user": {"applique": False},
             # MO-539 : le personnage de l agent est un champ du NOYAU comme un
             # autre. La fixture le porte DES SON debut -- sans lui, la fiche
             # accuse une injection qui est en realite coherente, et le maillon
             # devient un rouge permanent (il l a fait au premier passage).
             "role_agent": {"applique": True, "motif": "",
                            "personnage": "# ROLE", "domicile": "role-optimus-prime.md"},
             "poids_tokens": 500}
    texte = NL.join(module.fiche_technique(plein))
    if not texte.strip():
        ecarts.append("fiche-vide")
    if len(texte) >= len(_json.dumps(plein, ensure_ascii=True)):
        ecarts.append("fiche-PAS-plus-legere")
    if "KO :" in texte:
        ecarts.append("fiche-accuse-une-injection-coherente")
    # EO-492 : le CONTRE-TEMOIN qui manquait. Le maillon jouait la fiche avec un
    # rappel PLEIN, donc il ne pouvait pas mordre sur le cas REEL -- le rappel
    # VIDE, qui est le cas COMMUN (143 missions dev sur 152). Un rappel vide
    # doit passer, et en disant pourquoi il est vide.
    vide = dict(plein)
    vide["rappel"] = ""
    texte_vide = NL.join(module.fiche_technique(vide))
    if "KO :" in texte_vide:
        ecarts.append("fiche-accuse-un-rappel-VIDE (silence par design, EO-492)")
    if "vide par design" not in texte_vide:
        ecarts.append("fiche-ne-DIT-pas-que-le-rappel-est-vide-par-design")
    # MO-539 : le CONTRE-TEMOIN du PERSONNAGE ABSENT. Un agent sans role est un
    # agent qui agit sans son role : la fiche doit le CRIER, nommer le champ.
    # C est le pendant du rappel vide de EO-492, et c est ce qui rend le champ
    # obligatoire plutot que decoratif.
    sans_role = dict(plein)
    sans_role["role_agent"] = {}
    texte_sans_role = NL.join(module.fiche_technique(sans_role))
    if "KO :" not in texte_sans_role:
        ecarts.append("fiche-accept-un-sac-a-dos-SANS-personnage")
    elif "role_agent" not in texte_sans_role:
        ecarts.append("fiche-accuse-un-sac-a-dos-sans-personnage-SANS-LE-NOMMER")

    raison = getattr(module, "CHAMPS_PEUVENT_SE_TAIRE", None)
    if not isinstance(raison, dict) or not raison:
        ecarts.append("aucun champ du noyau ne declare son silence")
    else:
        for champ_silencieux in raison:
            if champ_silencieux not in module.NOYAU_FICHE:
                ecarts.append("un silence declare porte sur un champ HORS noyau : "
                              + str(champ_silencieux))
            elif not raison[champ_silencieux].strip():
                ecarts.append("un silence declare sans RAISON : " + str(champ_silencieux))
    casse = dict(plein)
    casse["role"] = None
    texte_casse = NL.join(module.fiche_technique(casse))
    if not ("KO :" in texte_casse and "role" in texte_casse):
        ecarts.append("fiche-ne-mord-pas-sur-noyau-absent")
    plafond = getattr(module, "PLAFOND_INJECTION_TOKENS", 0)
    if not isinstance(plafond, int) or plafond <= 0:
        ecarts.append("plafond-global-non-declare")
    # MO-473 : la remise a son PROPRE plafond (la fiche est ce que l agent LIT a chaque
    # round) ; il se DECLARE et se MESURE par le verbe --peser.
    plafond_remise = getattr(module, "PLAFOND_REMISE_TOKENS", 0)
    if not isinstance(plafond_remise, int) or plafond_remise <= 0:
        ecarts.append("plafond-de-remise-non-declare")
    elif not callable(getattr(module, "poids_fiche", None)):
        ecarts.append("poids-fiche-absent")
    # MO-471 (CABLAGE) : la fiche doit etre LUE sans commande -- la remise de round
    # (fin/fonctions.py) et le demarrage (injection/cycle.py) la servent. Un controle
    # qui ne verifie que la fiche, jamais son BRANCHEMENT, laisserait le cablage
    # disparaitre en silence (MO-246). Verifie sur le TEXTE de la source.
    fin_fonctions = pilote / "fin" / "fonctions.py"
    if not fin_fonctions.is_file():
        ecarts.append("fin/fonctions.py INTROUVABLE")
    elif "fiche_technique(" not in fin_fonctions.read_text(encoding="utf-8"):
        ecarts.append("remise-de-round-sans-fiche")
    cycle = pilote / "injection" / "cycle.py"
    if not cycle.is_file():
        ecarts.append("injection/cycle.py INTROUVABLE")
    elif 'self.fiche("demarrage")' not in cycle.read_text(encoding="utf-8"):
        ecarts.append("demarrage-sans-fiche")
    return ecarts


def _eprouver_fiche_moule(racine):
    """MAILLON 48 (MO-471, decisions D1/D5) : eprouve les MOULES DE FICHE EN MEMOIRE.

    Charge injection/injecter.py (le moteur des moules) et verifie, sans rien
    ecrire : le rendu REMPLACE les jetons connus ; un jeton INCONNU est NOMME et
    RENDU TEL QUEL (jamais remplace en silence) ; et LES QUATRE MOULES DU DOMICILE
    ne portent AUCUN jeton hors du moteur -- un moule a trou serait servi comme une
    fiche complete (L-055). Rend la liste des ecarts (vide = OK).
    """
    import importlib.util
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    injection = matrice / "_operateur" / "optimus-prime" / "pilote" / "injection"
    chemin = injection / "injecter.py"
    if not chemin.is_file():
        return ["injection/injecter.py INTROUVABLE : " + str(chemin)]
    specification = importlib.util.spec_from_file_location("injecter_moule", chemin)
    module = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(module)
    except Exception as erreur:  # noqa: BLE001
        return ["injecter.py ILLISIBLE (" + type(erreur).__name__ + " : "
                + str(erreur)[:60] + ")"]
    ecarts = []
    rendu, inconnus = module.rendre_moule("a __CATEGORIE__ b", {"CATEGORIE": "X"})
    if rendu != "a X b" or inconnus:
        ecarts.append("rendu-jeton-connu -> " + rendu + " inconnus=" + ",".join(inconnus))
    rendu2, inconnus2 = module.rendre_moule("__ZZZ__", {})
    if inconnus2 != ["ZZZ"]:
        ecarts.append("jeton-inconnu-PAS-nomme -> inconnus=" + ",".join(inconnus2))
    if "__ZZZ__" not in rendu2:
        ecarts.append("jeton-inconnu-REMPLACE-en-silence")
    connus = set(getattr(module, "JETONS_FICHE", ()))
    if len(connus) != 4:
        ecarts.append("JETONS_FICHE attendu a 4 jetons, trouve " + str(len(connus)))
    trouves = 0
    for categorie in ("demarrage", "avant-mission", "pendant-mission", "apres-mission"):
        moule = injection / "templates" / categorie / "fiche.moule"
        if not moule.is_file():
            ecarts.append("moule ABSENT : " + categorie)
            continue
        trouves += 1
        texte = moule.read_text(encoding="utf-8")
        rendu_moule, restants = module.rendre_moule(texte, {j: "x" for j in connus})
        if restants:
            ecarts.append("moule " + categorie + " : jeton(s) hors moteur : "
                          + ",".join(sorted(set(restants))))
        if "__" in rendu_moule:
            ecarts.append("moule " + categorie + " : jeton NON rendu par le moteur")
    if trouves != 4:
        ecarts.append("moules trouves : " + str(trouves) + " / 4")
    return ecarts


def _verifier_remise_cockpit(texte):
    """Ecarts de l ENCART /remise pour un TEXTE de cockpit donne (pure, testable).

    Un cockpit qui aurait perdu son branchement (route absente, ROUTERS ou ROUTES
    sans `remise`, plafond RECOPIE au lieu d etre CONSOMME chez son domicile) doit
    etre REFUSE. La fonction est PURE : elle prend le texte, rend les ecarts -- c est
    ce qui permet a la contre-epreuve de mordre sur un cockpit fabrique (L-032).
    """
    ecarts = []
    if "def route_remise(" not in texte:
        ecarts.append("route_remise ABSENTE")
    if "def _charger_fonctions_injection(" not in texte:
        ecarts.append("chargement du domicile de la fiche ABSENT")
    if '"remise": route_remise' not in texte:
        ecarts.append("route /remise NON branchee dans ROUTERS")
    if '"remise"' not in texte:
        ecarts.append("remise ABSENTE du vocabulaire des routes (ROUTES)")
    if "PLAFOND_REMISE_TOKENS" not in texte:
        ecarts.append("le PLAFOND DE REMISE n est PAS consomme chez son domicile")
    if "poids_fiche(" not in texte or "poids_injection(" not in texte:
        ecarts.append("les PESEURS de la remise ne sont PAS consommes")
    if "CHEMIN_OUTBOX_FLUX" not in texte or "LIGNES_REMISE_SERIE" not in texte:
        ecarts.append("la SOURCE de la serie (outbox + taille) n est PAS declaree")
    # MO-476 : le poids d INJECTION TOTAL (l injection entiere) et son EVOLUTION dans
    # le temps doivent etre VISIBLES -- le plafond GLOBAL se consomme chez son
    # domicile, et la tendance se lit sur la SERIE (etincelle + direction).
    if "PLAFOND_INJECTION_TOKENS" not in texte:
        ecarts.append("le PLAFOND GLOBAL d injection n est PAS consomme chez son domicile")
    if "TENDANCE" not in texte or "_direction_tendance(" not in texte:
        ecarts.append("la TENDANCE (evolution dans le temps) est ABSENTE")
    if "_etincelle(" not in texte:
        ecarts.append("l etincelle de tendance est ABSENTE")
    # MO-477 : une HAUSSE PROLONGEE du poids d injection doit etre SIGNALEE : le
    # seuil de derive se consomme chez son domicile et le detecteur doit etre present.
    if "SEUIL_DERIVE_POURCENT" not in texte or "_deriver_tendance(" not in texte:
        ecarts.append("le SEUIL DE DERIVE (hausse prolongee) est ABSENT")
    return ecarts


def _eprouver_remise_cockpit(racine):
    """MAILLON 49 (MO-474) : eprouve l ENCART /remise du cockpit EN MEMOIRE.

    Demande createur (2026-09-26) : le POIDS DE REMISE PAR ROUND doit etre visible
    dans le cockpit pour surveiller, dans le TEMPS, le PLAFOND DE REMISE (MO-473).
    Ce maillon MORD sur une route NON branchee (fonction absente, ROUTERS ou ROUTES
    sans `remise`) et sur un cockpit qui RECOPIERAIT le plafond au lieu de le
    CONSOMMER chez son domicile (injection/fonctions.py, M-076) ; il EPARGNE le
    fichier reel. Eprouve sur le TEXTE (aucune ecriture, aucun processus lance).
    """
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    cockpit = matrice / "_operateur" / "optimus-prime" / "cockpit" / "cockpit-matrice.py"
    if not cockpit.is_file():
        return ["cockpit/cockpit-matrice.py INTROUVABLE : " + str(cockpit)]
    ecarts = _verifier_remise_cockpit(cockpit.read_text(encoding="utf-8"))
    # CONTRE-EPREUVE : le meme controle doit MORDRE sur un cockpit non branche --
    # un controle qu on ne peut pas pieger ne prouve rien (L-032).
    if not _verifier_remise_cockpit("def route_remise(racine):" + chr(10) + "    pass" + chr(10)):
        ecarts.append("contre-epreuve : un cockpit NON branche n est PAS refuse")
    return ecarts


def _verifier_boite_trace(texte_constantes, texte_injection):
    """Ecarts de la DECLARATION "la boite du cameleon est une TRACE" (MO-441).

    PURE : elle prend les DEUX textes (le domicile et la porte qui depose) et rend
    les ecarts -- c est ce qui permet a la contre-epreuve de mordre sur un cobaye
    fabrique (L-032). Un depot MUET sur la nature de la boite, une declaration
    RECOPIEE au lieu d etre CONSOMMEE chez son domicile, ou une checklist qui
    n est plus remise par le statut doivent etre REFUSES.
    """
    ecarts = []
    if chr(34) + "trace" + chr(34) not in texte_constantes or "NATURE_BOITE_PILOTE_OUT" not in texte_constantes:
        ecarts.append("la NATURE de la boite (trace) n est PAS declaree au domicile")
    if "DECLARATION_BOITE_PILOTE_OUT" not in texte_constantes:
        ecarts.append("la DECLARATION de la boite n est PAS declaree au domicile")
    if "DECLARATION_BOITE_PILOTE_OUT" not in texte_injection:
        ecarts.append("le DEPOSANT ne CONSOMME pas la declaration (M-076)")
    if texte_injection.count("annoncer_depot_boite(") < 3:
        ecarts.append("les DEUX chemins de depot (simple + lot) ne passent pas par annoncer_depot_boite")
    if "annoncer_checklist(" not in texte_injection:
        ecarts.append("le STATUT ne remet pas la checklist (le canal des ordres)")
    muets = texte_injection.count("print(" + chr(34) + "Injection deposee pour " + chr(34))
    if muets != 1:
        ecarts.append("le depot MUET n est pas centralise dans annoncer_depot_boite (attendu :"
                      " 1 occurrence -- les DEUX chemins portaient avant un message muet"
                      " chacun ; mesure : " + str(muets) + ")")
    return ecarts


def _eprouver_boite_trace(racine):
    """MAILLON 50 (MO-441) : eprouve la NATURE de la boite du cameleon EN MEMOIRE.

    L ecart EC4 (audit MO-365) a mesure que le pilote du Flux 1 depose son
    injection et que PERSONNE n en reprend le contenu (les seuls lecteurs sont la
    TAILLE, cockpit, et la LISIBILITE, maillon 6). Decision MO-441 : la boite est
    une TRACE, jamais un canal -- et la declaration doit rester VRAIE : elle se
    CONSOMME chez son domicile, le depot la PORTE (les deux chemins), et le statut
    remet la checklist lue dans la file. Ce maillon MORD sur un depot muet, sur une
    declaration recopiee et sur la checklist absente ; il EPARGNE les fichiers
    reels et se CONTRE-EPROUVE en memoire (L-032).
    """
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    constantes = matrice / "matrice" / "pilote" / "constants.py"
    injection = matrice / "matrice" / "pilote" / "injection" / "fonctions.py"
    for chemin in (constantes, injection):
        if not chemin.is_file():
            return ["fichier INTROUVABLE : " + str(chemin)]
    ecarts = _verifier_boite_trace(constantes.read_text(encoding="utf-8"),
                                   injection.read_text(encoding="utf-8"))
    if not _verifier_boite_trace("", ""):
        ecarts.append("contre-epreuve : un depot MUET n est PAS refuse")
    if not _verifier_boite_trace("NATURE_BOITE_PILOTE_OUT = " + chr(34) + "trace" + chr(34),
                                 "DECLARATION_BOITE_PILOTE_OUT"):
        ecarts.append("contre-epreuve : une declaration RECOPIEE n est PAS refusee")
    return ecarts


def _verifier_bilan_etranger(texte_domicile, texte_cloture):
    """Ecarts de la regle "le TITRE du bilan declare la mission close" (MO-480).

    PURE : elle prend les DEUX textes (le domicile du jugement et la cloture qui le
    consomme) et rend les ecarts -- c est ce qui permet a la contre-epreuve de mordre
    sur un cobaye fabrique (L-032).
    """
    ecarts = []
    if "MOTIF_TITRE_BILAN" not in texte_domicile or "def bilan_etranger(" not in texte_domicile:
        ecarts.append("le DOMICILE ne porte pas le jugement du titre (bilan_etranger)")
    if "def bilan_etranger(" in texte_domicile and "def normaliser_id(" not in texte_domicile:
        ecarts.append("la comparaison des identifiants n est PAS normalisee (M-076)")
    if "refus_bilan_etranger(" not in texte_cloture:
        ecarts.append("le refus n est PAS branche a la cloture (fin/fonctions.py)")
    return ecarts


def _eprouver_bilan_etranger(racine):
    """MAILLON 51 (MO-480 / EO-455) : eprouve le REFUS DU BILAN ETRANGER EN MEMOIRE.

    La panne payee en MO-440 : la mission SERVIE close avec le bilan d une AUTRE, sans
    qu aucun garde ne morde -- journal, file et controle de coherence disaient tous
    D ACCORD. Ce maillon rejoue le jugement du DOMICILE sur le CORPUS REEL des bilans :
      - il MORD sur les DEUX clotures fausses REELLES (MO-407 declare MO-412 ; MO-440
        declare MO-463) et il exige qu il y en ait EXACTEMENT DEUX : une troisieme
        accusation serait soit une faute neuve, soit une regle qui se met a crier --
        les deux doivent se voir ;
      - il EPARGNE les autres bilans du corpus (aucun faux positif) ;
      - il CONTRE-EPREUVE les titres sans identifiant, la famille M- contre MO-, et le
        CORPS d un recit qui cite legitimement une autre mission (L-032).
    Aucune ecriture, aucun processus lance.
    """
    import importlib.util
    import json
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    domicile = matrice / "matrice" / "data" / "commun" / "cloture_fausse.py"
    cloture = matrice / "_operateur" / "optimus-prime" / "pilote" / "fin" / "fonctions.py"
    historique = matrice / "matrice" / "data" / "historiques-missions-optimus.jsonl"
    for chemin in (domicile, cloture, historique):
        if not chemin.is_file():
            return ["fichier INTROUVABLE : " + str(chemin)]
    ecarts = _verifier_bilan_etranger(domicile.read_text(encoding="utf-8"),
                                      cloture.read_text(encoding="utf-8"))
    spec = importlib.util.spec_from_file_location("domicile_cloture_fausse", str(domicile))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fausses = []
    lues = 0
    for ligne in historique.read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        try:
            entree = json.loads(ligne)
        except ValueError:
            continue
        lues += 1
        couple = module.bilan_etranger(entree.get("id"), entree.get("bilan"))
        if couple:
            fausses.append(couple)
    attendues = [("MO-407", "MO-412"), ("MO-440", "MO-463")]
    if fausses != attendues:
        ecarts.append("le jugement sur le CORPUS REEL rend " + str(fausses) + " au lieu de "
                      + str(attendues) + " (" + str(lues) + " entree(s) lue(s))")
    if module.bilan_etranger("MO-480", "BILAN MO-480 -- le titre de sa propre mission") is not None:
        ecarts.append("contre-epreuve : le titre de SA PROPRE mission est accuse")
    if module.bilan_etranger("MO-480", "MO-480 faite (serie 1/2)") is not None:
        ecarts.append("contre-epreuve : un titre SANS identifiant est accuse")
    if module.bilan_etranger("MO-480", "BILAN MO-480 -- suite de MO-463") is not None:
        ecarts.append("contre-epreuve : un CORPS qui cite une autre mission est accuse")
    if module.bilan_etranger("MO-480", "BILAN M-480 -- la famille du cameleon") is None:
        ecarts.append("contre-epreuve : M-480 (cameleon) n est PAS distingue de MO-480")
    if module.bilan_etranger("MO-480", "BILAN MO-463 -- le titre etranger") is None:
        ecarts.append("contre-epreuve : un bilan ETRANGER n est PAS accuse")
    return ecarts


def _verifier_promotion(texte_domicile, texte_pilote, texte_cloture):
    """Ecarts du CABLAGE de la promotion automatique (MO-481 / EO-457).

    PURE : elle prend les TROIS textes (le DOMICILE de la regle et les DEUX
    consommateurs) et rend les ecarts -- la contre-epreuve peut donc mordre sur un
    cobaye fabrique (L-032).
    """
    ecarts = []
    for defaut in ("def promotion_requise(", "def reclasser_par_importance(",
                   "def reclasser_apres("):
        if defaut not in texte_domicile:
            ecarts.append("le DOMICILE ne porte pas " + defaut)
    if "import promotion" not in texte_pilote:
        ecarts.append("le pilote n importe PAS le domicile de la promotion (M-076)")
    if "promouvoir_les_suivants(file_missions, reference)" not in texte_pilote:
        ecarts.append("la promotion n est PAS definie sur la reference (pilote/commun.py)")
    if "promouvoir_les_suivants(file_missions, mission)" not in texte_cloture:
        ecarts.append("le reclassement n est PAS branche a la cloture (fin/fonctions.py)")
    return ecarts


def _eprouver_promotion(racine):
    """MAILLON 52 (MO-481 / EO-457) : eprouve la PROMOTION AUTOMATIQUE EN MEMOIRE.

    La regle du createur : < un item plus important que la mission en cours se
    reclasse seul >, et < jamais la mission en cours > (serie stricte). Ce maillon
    execute le DOMICILE reel (data/commun/promotion.py) :
      - il MORD : un item STRICTEMENT plus important est promu (gravite superieure,
        ou niveau superieur DANS la meme bande) ;
      - il EPARGNE : une importance EGALE ne reclasse RIEN (contre-temoin), une
        importance moindre non plus, et deux items SANS importance non plus ;
      - il PROUVE l ORDRE : `reclasser_apres` laisse le PREFIXE intact (la mission en
        cours est menee a son terme) et reordonne la SUITE ; a importance egale,
        l ordre d arrivee est CONSERVE (tri stable).
    Eprouve EN MEMOIRE (aucune ecriture, aucun processus lance).
    """
    import importlib
    import sys
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    commun = matrice / "matrice" / "data" / "commun"
    domicile = commun / "promotion.py"
    pilote = matrice / "_operateur" / "optimus-prime" / "pilote" / "commun.py"
    cloture = matrice / "_operateur" / "optimus-prime" / "pilote" / "fin" / "fonctions.py"
    for chemin in (domicile, pilote, cloture):
        if not chemin.is_file():
            return ["fichier INTROUVABLE : " + str(chemin)]
    ecarts = _verifier_promotion(domicile.read_text(encoding="utf-8"),
                                 pilote.read_text(encoding="utf-8"),
                                 cloture.read_text(encoding="utf-8"))
    chemin_commun = str(commun)
    ajoute = chemin_commun not in sys.path
    if ajoute:
        sys.path.insert(0, chemin_commun)
    try:
        carte = importlib.import_module("carte_identite")
        promotion = importlib.import_module("promotion")
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["import IMPOSSIBLE du domicile : " + str(erreur)]
    finally:
        if ajoute and chemin_commun in sys.path:
            sys.path.remove(chemin_commun)
    reference = {"gravite": "important", "niveau": 10}
    if not promotion.promotion_requise({"gravite": "tres-urgent", "niveau": 1},
                                       reference):
        ecarts.append("le MORDANT ne mord PAS : gravite superieure non promue")
    if not promotion.promotion_requise({"gravite": "important", "niveau": 10},
                                       {"gravite": "important", "niveau": 3}):
        ecarts.append("le MORDANT ne mord PAS : niveau superieur non promu")
    if promotion.promotion_requise({"gravite": "important", "niveau": 10}, reference):
        ecarts.append("contre-epreuve : une importance EGALE est promue")
    if promotion.promotion_requise({"gravite": "optionnel", "niveau": 1}, reference):
        ecarts.append("contre-epreuve : une importance MOINDRE est promue")
    if promotion.promotion_requise({}, {}):
        ecarts.append("contre-epreuve : deux defauts se promeuvent entre eux")
    bas = {"id": "bas", "gravite": "optionnel", "niveau": 1}
    haut = {"id": "haut", "gravite": "tres-urgent", "niveau": 10}
    milieu = {"id": "milieu", "gravite": "normal", "niveau": 5}
    ordre = [e["id"] for e in promotion.reclasser_apres([bas, milieu, haut], 1)]
    if ordre != ["bas", "haut", "milieu"]:
        ecarts.append("l ORDRE n est pas tenu : " + str(ordre)
                      + " au lieu de ['bas', 'haut', 'milieu']")
    egaux = [{"id": "a", "gravite": "normal", "niveau": 5},
             {"id": "b", "gravite": "normal", "niveau": 5},
             {"id": "c", "gravite": "normal", "niveau": 5}]
    if [e["id"] for e in promotion.reclasser_par_importance(egaux)] != ["a", "b", "c"]:
        ecarts.append("la STABILITE est perdue : a importance egale, l ordre bouge")
    if not carte.valider_importance({"gravite": "urgentissime"}):
        ecarts.append("contre-epreuve : une gravite HORS liste n est PAS accuse")
    if carte.valider_importance({"type": "readme"}):
        ecarts.append("contre-epreuve : une carte SANS importance est accusee")
    return ecarts


def _verifier_source_privee(texte_constantes, texte_commun, texte_entry):
    """Ecarts du CABLAGE de la SOURCE BDD PRIVEE (MO-482 / EO-458). PURE."""
    ecarts = []
    if "BDD_SOURCES_PRIVEES" not in texte_constantes:
        ecarts.append("le moteur ne DECLARE pas BDD_SOURCES_PRIVEES")
    if '"segments"' not in texte_constantes:
        ecarts.append("la source privee `segments` n est PAS declaree")
    if "chemin_prive = BDD_SOURCES_PRIVEES.get(src)" not in texte_commun:
        ecarts.append("scanner_bdd ne lit PAS la source privee declaree")
    if "privee = True" not in texte_commun:
        ecarts.append("la source privee n est PAS marquee privee (L-016)")
    if "sources_bdd_privees()" not in texte_entry:
        ecarts.append("le refus sans --prive n est PAS branche (entry.py)")
    return ecarts


def _eprouver_source_privee(racine):
    """MAILLON 53 (MO-482 / EO-458) : eprouve la SOURCE BDD PRIVEE EN MEMOIRE.

    La decision du createur : une BDD de raisonnement pour Optimus, DANS LA ZONE
    INVISIBLE, declaree au moteur comme source PRIVEE (servie seulement sous
    --prive, L-016). Ce maillon MORD sur l absence de declaration, de lecture
    privee ou de refus sans --prive ; il EPARGNE un cablage coherent. Il verifie
    AUSSI que le generateur (dupliquer-template) cible la ZONE INVISIBLE (jamais
    sous `matrice/`). Eprouve EN MEMOIRE (aucune ecriture, aucun processus lance).
    """
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    rechercheur = matrice / "matrice" / "data" / "outils" / "rechercher"
    constants = rechercheur / "constants.py"
    commun = rechercheur / "commun.py"
    entry = rechercheur / "rechercher" / "entry.py"
    bdd = matrice / "_operateur" / "optimus-prime" / "raisonnement" / "segments.json"
    outil = (matrice / "_operateur" / "optimus-prime" / "raisonnement"
             / "bdd-raisonnement" / "main.py")
    surcharge = matrice / "matrice" / "templates" / "outil-bdd-prive" / "constants.py.moule"
    for chemin in (constants, commun, entry, bdd, outil, surcharge):
        if not chemin.is_file():
            return ["fichier INTROUVABLE : " + str(chemin)]
    texte_constantes = constants.read_text(encoding="utf-8")
    ecarts = _verifier_source_privee(texte_constantes,
                                     commun.read_text(encoding="utf-8"),
                                     entry.read_text(encoding="utf-8"))
    if '"_operateur/optimus-prime/raisonnement/segments.json"' not in texte_constantes:
        ecarts.append("la source privee ne pointe PAS la zone invisible (L-016)")
    generateur = matrice / "matrice" / "data" / "outils" / "dupliquer-template" / "constants.py"
    if not generateur.is_file():
        ecarts.append("dupliquer-template/constants.py INTROUVABLE")
    else:
        texte_gen = generateur.read_text(encoding="utf-8")
        if "ZONE_PRIVEE" not in texte_gen:
            ecarts.append("le generateur ne connait PAS ZONE_PRIVEE")
        if 'REPERTOIRE_MATRICE.parent / "_operateur"' not in texte_gen:
            ecarts.append("le generateur cible `matrice/`, PAS la zone invisible")
    return ecarts


def _eprouver_source_partagee(racine):
    """MAILLON 54 (MO-483 / EO-459) : eprouve la SOURCE BDD PARTAGEE (cameleon).

    La decision du createur : la BDD de raisonnement du CAMELEON vit dans SON
    domicile (`agents/cameleon/raisonnement/`), VISIBLE et PARTAGEE -- le moteur
    la sert SANS `--prive`. Ce maillon MORD sur l absence de declaration, de
    branche de lecture partagee, de zone du generateur ou de surcharge. Eprouve
    EN MEMOIRE (aucune ecriture, aucun processus lance).
    """
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "matrice").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    rechercheur = matrice / "matrice" / "data" / "outils" / "rechercher"
    constants = rechercheur / "constants.py"
    commun = rechercheur / "commun.py"
    bdd = matrice / "agents" / "cameleon" / "raisonnement" / "segments-cameleon.json"
    outil = (matrice / "agents" / "cameleon" / "raisonnement"
             / "bdd-raisonnement-cameleon" / "main.py")
    surcharge = (matrice / "matrice" / "templates" / "outil-bdd-cameleon"
                 / "constants.py.moule")
    generateur = (matrice / "matrice" / "data" / "outils" / "dupliquer-template"
                  / "constants.py")
    for chemin in (constants, commun, bdd, outil, surcharge, generateur):
        if not chemin.is_file():
            return ["fichier INTROUVABLE : " + str(chemin)]
    ecarts = []
    texte_constantes = constants.read_text(encoding="utf-8")
    if "BDD_SOURCES_PARTAGEES" not in texte_constantes:
        ecarts.append("le moteur ne DECLARE pas BDD_SOURCES_PARTAGEES")
    if '"segments-cameleon"' not in texte_constantes:
        ecarts.append("la source partagee `segments-cameleon` n est PAS declaree")
    texte_commun = commun.read_text(encoding="utf-8")
    if "chemin_partage = BDD_SOURCES_PARTAGEES.get(src)" not in texte_commun:
        ecarts.append("scanner_bdd ne lit PAS la source partagee declaree")
    if "chemin = REPERTOIRE_MATRIX / chemin_partage" not in texte_commun:
        ecarts.append("la source partagee n est PAS servie SANS --prive")
    if "list(BDD_SOURCES_PARTAGEES)" not in texte_commun:
        ecarts.append("sources_bdd n expose PAS la source partagee")
    texte_gen = generateur.read_text(encoding="utf-8")
    if "ZONE_CAMELEON" not in texte_gen:
        ecarts.append("le generateur ne connait PAS ZONE_CAMELEON")
    if 'REPERTOIRE_MATRICE.parent / "agents"' not in texte_gen:
        ecarts.append("le generateur ne cible PAS le domicile du cameleon")
    return ecarts


def _verifier_champ_multiple(texte_carte, texte_entry):
    """Ecarts du CABLAGE du 0 MUET sur un champ a VALEURS MULTIPLES (MO-450). PURE."""
    ecarts = []
    if "def valeur_dans_champ_multiple(" not in texte_carte:
        ecarts.append("le domicile ne DECLARE pas valeur_dans_champ_multiple")
    if "CLE_LIENS = " not in texte_carte or "SEPARATEUR_LIENS = " not in texte_carte:
        ecarts.append("le domicile ne DECLARE pas la cle et le separateur des liens")
    if "valeur_dans_champ_multiple" not in texte_entry:
        ecarts.append("la porte rechercher ne CONSOMME pas le predicat (0 muet)")
    if "NOM_OPTION_LIEN" not in texte_entry:
        ecarts.append("la porte ne NOMME pas le mode dedie dans le 0 muet")
    return ecarts


def _eprouver_champ_multiple(racine):
    """MAILLON 55 (MO-450) : eprouve le 0 MUET d un --champ sur une cle a VALEURS
    MULTIPLES EN MEMOIRE.

    Mesure MO-402/MO-405 : `--champ liens=<un lien>` rendait 0 alors que la valeur
    figure -- un champ a valeurs multiples se compare EN ENTIER, jamais element par
    element. Ce maillon execute le DOMICILE reel (data/commun/carte_identite.py) :
      - il MORD : un element d une LISTE (separee par la virgule) est VU ;
      - il EPARGNE : un champ a valeur UNIQUE, une valeur ABSENTE de la liste et
        une liste d UN SEUL element ne declenchent RIEN (contre-temoins) ;
      - il verifie le CABLAGE : la porte consomme le predicat et NOMME le mode
        dedie (--lien).
    Eprouve EN MEMOIRE (aucune ecriture, aucun processus lance).
    """
    import importlib
    import sys
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    commun = matrice / "matrice" / "data" / "commun"
    domicile = commun / "carte_identite.py"
    entry = (matrice / "matrice" / "data" / "outils" / "rechercher"
             / "rechercher" / "entry.py")
    for chemin in (domicile, entry):
        if not chemin.is_file():
            return ["fichier INTROUVABLE : " + str(chemin)]
    ecarts = _verifier_champ_multiple(domicile.read_text(encoding="utf-8"),
                                      entry.read_text(encoding="utf-8"))
    chemin_commun = str(commun)
    ajoute = chemin_commun not in sys.path
    if ajoute:
        sys.path.insert(0, chemin_commun)
    try:
        carte = importlib.import_module("carte_identite")
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["import IMPOSSIBLE du domicile : " + str(erreur)]
    finally:
        if ajoute and chemin_commun in sys.path:
            sys.path.remove(chemin_commun)
    multiple = [{"liens": "matrice/a.md, matrice/b.md"}]
    if not carte.valeur_dans_champ_multiple(multiple, "liens", "matrice/b.md"):
        ecarts.append("le MORDANT ne mord PAS : un element d une LISTE n est PAS vu")
    if carte.valeur_dans_champ_multiple([{"type": "outil"}], "type", "outil"):
        ecarts.append("contre-epreuve : un champ a valeur UNIQUE est pris pour une liste")
    if carte.valeur_dans_champ_multiple(multiple, "liens", "matrice/zzz.md"):
        ecarts.append("contre-epreuve : une valeur ABSENTE de la liste est vue presente")
    if carte.valeur_dans_champ_multiple([{"liens": "matrice/seul.md"}],
                                        "liens", "matrice/seul.md"):
        ecarts.append("contre-epreuve : une liste d UN element est prise pour multiple")
    return ecarts


def _verifier_round_servi(texte_domicile, texte_commun, texte_fin, texte_constantes,
                          texte_injection, texte_suivi):
    """Ecarts du CABLAGE du ROUND SERVI (MO-451). PURE."""
    ecarts = []
    if "def servi_non_conduit(" not in texte_domicile:
        ecarts.append("le domicile ne DECLARE pas servi_non_conduit")
    if "def message_rappel(" not in texte_domicile:
        ecarts.append("le domicile ne DECLARE pas le message de rappel")
    if "def lire_acte_agent(" not in texte_domicile:
        ecarts.append("le domicile ne DECLARE pas la lecture de l acte agent")
    if "import round_servi" not in texte_commun or "rappel_round_servi_non_conduit" not in texte_commun:
        ecarts.append("le pilote ne CONSOMME pas le domicile (commun.py)")
    if "rappel_round_servi_non_conduit(charger_file)" not in texte_fin:
        ecarts.append("la remise des ordres ne DIT pas le rappel (fin/fonctions.py)")
    if "RAPPEL_ROUND_SERVI" not in texte_constantes:
        ecarts.append("le texte du rappel de chaine n est PAS declare (constants.py)")
    if "RAPPEL_ROUND_SERVI" not in texte_injection:
        ecarts.append("l injection ne porte pas le rappel de chaine (injection/fonctions.py)")
    if "round_servi.servi_non_conduit(" not in texte_suivi:
        ecarts.append("le suivi ne CONSOMME pas le domicile (suivi-pilote.py)")
    return ecarts


def _eprouver_round_servi(racine):
    """MAILLON 56 (MO-451) : eprouve le ROUND SERVI ET JAMAIS CONDUIT EN MEMOIRE.

    Retour createur : < quand un round est servi -> tu dois le faire et ne pas stopper
    pour faire ton bilan >. Le FAIT vit au domicile partage (data/commun/round_servi.py).
    Ce maillon :
      - MORD : une PRISE restee le DERNIER acte (aucun acte agent depuis) est VUE ;
        un acte agent EGAL a la prise ne blanchit PAS (meme frontiere que le suivi) ;
      - EPARGNE : un acte agent POSTERIEUR (round CONDUIT), un dernier acte qui n est
        PAS une prise, et une mesure IMPOSSIBLE (acte agent absent = None) : le
        contre-temoin d une chaine FERMEE (aucun candidat) ne declenche RIEN ;
      - verifie le CABLAGE : le pilote et le suivi CONSOMMENT le domicile, la remise
        DIT le rappel, l injection de chaine le porte.
    Eprouve EN MEMOIRE (aucune ecriture, aucun processus lance).
    """
    import importlib
    import sys
    from datetime import datetime, timedelta
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    commun = matrice / "matrice" / "data" / "commun"
    domicile = commun / "round_servi.py"
    pilote = matrice / "_operateur" / "optimus-prime" / "pilote"
    fichiers = {
        "commun": pilote / "commun.py",
        "fin": pilote / "fin" / "fonctions.py",
        "constantes": pilote / "constants.py",
        "injection": pilote / "injection" / "fonctions.py",
        "suivi": (matrice / "_operateur" / "optimus-prime" / "super-combos" / "combos"
                  / "outils" / "suivi-pilote.py"),
    }
    for chemin in [domicile] + list(fichiers.values()):
        if not chemin.is_file():
            return ["fichier INTROUVABLE : " + str(chemin)]
    ecarts = _verifier_round_servi(
        domicile.read_text(encoding="utf-8"),
        fichiers["commun"].read_text(encoding="utf-8"),
        fichiers["fin"].read_text(encoding="utf-8"),
        fichiers["constantes"].read_text(encoding="utf-8"),
        fichiers["injection"].read_text(encoding="utf-8"),
        fichiers["suivi"].read_text(encoding="utf-8"))
    chemin_commun = str(commun)
    ajoute = chemin_commun not in sys.path
    if ajoute:
        sys.path.insert(0, chemin_commun)
    try:
        round_servi = importlib.import_module("round_servi")
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["import IMPOSSIBLE du domicile : " + str(erreur)]
    finally:
        if ajoute and chemin_commun in sys.path:
            sys.path.remove(chemin_commun)
    prise = datetime(2026, 9, 27, 15, 16, 17)
    if round_servi.servi_non_conduit("prise", prise, prise - timedelta(minutes=5)) is not True:
        ecarts.append("le MORDANT ne mord PAS : une prise restee seule n est PAS vue")
    if round_servi.servi_non_conduit("prise", prise, prise) is not True:
        ecarts.append("la frontiere a l EGAL a change : un acte egal blanchit la prise")
    if round_servi.servi_non_conduit("prise", prise, prise + timedelta(minutes=1)) is not False:
        ecarts.append("contre-epreuve : un round CONDUIT est encore accuse")
    if round_servi.servi_non_conduit("fin", prise, prise - timedelta(minutes=5)) is not False:
        ecarts.append("contre-epreuve : un dernier acte NON-prise est accuse")
    if round_servi.servi_non_conduit("prise", prise, None) is not None:
        ecarts.append("contre-epreuve : une mesure IMPOSSIBLE est conclue")
    if not round_servi.message_rappel("MO-451", "2026-09-27 15:16:17").strip():
        ecarts.append("le rappel est MUET : il ne porte aucun texte")
    return ecarts


def _eprouver_regularisation(racine):
    """MAILLON 57 (MO-461 / EO-433) : eprouve la PORTE DE REGULARISATION du pilote.

    La panne payee : une FIN declaree au JOURNAL pour une mission que la FILE dit
    encore < en-attente > ne pouvait etre fermee par AUCUNE porte -- `enregistrer`
    refuse un id deja present, `fin` ne close que la mission EN COURS. Le controle
    de coherence rendait donc des ecarts que RIEN ne pouvait faire tomber (mesure :
    MO-412, close au journal le 25/09 a 08:53:31, restee en-attente dans la file).

    Ce maillon joue la porte sur une RACINE JETABLE (tempfile : aucune trace du
    depot n est touchee) et fait trancher le CONTROLE REEL par sa porte
    (suivi-optimus coherence --racine <cobaye>) :
      - il MORD : les 3 ecarts du cobaye existent AVANT, et les 2 ecarts de la
        mission regularisee TOMBENT par la porte (il n en reste plus qu un) ;
      - il EPARGNE (contre-temoin) : une mission < terminee > dans la file SANS fin
        au journal est REFUSEE par la porte, la file n est PAS touchee, et le
        controle l ACCUSE TOUJOURS -- c est ce qui interdit a la porte d etouffer
        un vrai ecart en inventant une borne ;
      - il NOMME les refus : motif manquant, id inconnu, mission en cours, sans fin ;
      - il verifie le CABLAGE : le verbe est route par main.py, l action
        `regularisation` est au vocabulaire ferme de suivi-optimus, la borne de fin
        est declaree IDEMPOTENTE (donc jamais doublee) et l ACTE a une action a LUI.
    """
    import importlib.util
    import json
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    pilote = matrice / "_operateur" / "optimus-prime" / "pilote"
    domicile = pilote / "regulariser" / "fonctions.py"
    entree = pilote / "regulariser" / "entry.py"
    router = pilote / "main.py"
    suivi = matrice / "matrice" / "data" / "outils" / "suivi-optimus"
    porte_suivi = suivi / "main.py"
    constants_suivi = suivi / "constants.py"
    for chemin in (domicile, entree, router, porte_suivi, constants_suivi):
        if not chemin.is_file():
            return ["fichier INTROUVABLE : " + str(chemin)]

    # CABLAGE : trois fils, et chacun est un fil qu on peut oublier en silence.
    texte_router = router.read_text(encoding="utf-8")
    ecarts = []
    if "from regulariser.entry import executer as regulariser_executer" not in texte_router:
        ecarts.append("le routeur n importe pas la categorie regulariser")
    if '"regulariser": regulariser_executer' not in texte_router:
        ecarts.append("le verbe regulariser n est PAS route par main.py")
    if "regularisation" not in constants_suivi.read_text(encoding="utf-8"):
        ecarts.append("l action `regularisation` n est pas au vocabulaire de suivi-optimus")
    if "regulariser --id MO-XXX --motif" not in texte_router:
        ecarts.append("l usage de regulariser n est pas documente dans la facade")

    sys.path.insert(0, str(pilote))
    try:
        specification = importlib.util.spec_from_file_location(
            "regulariser_fonctions", domicile)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["regulariser/fonctions.py ILLISIBLE ("
                         + type(erreur).__name__ + " : " + str(erreur)[:60] + ")"]
    finally:
        sys.path.remove(str(pilote))

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    # LES DECISIONS : pures, donc eprouvables sans aucune trace.
    en_attente = {"id": "MO-901", "statut": "en-attente", "theme": "PILOTE"}
    terminee = {"id": "MO-902", "statut": "terminee", "theme": "PILOTE"}
    ep("mord-decision", module.diagnostiquer("m", en_attente, True) == (0, "regularisation"),
       "une fin au journal et une file en-attente ne sont plus regularisables : "
       + repr(module.diagnostiquer("m", en_attente, True)))
    ep("epargne-deja-terminee", module.diagnostiquer("m", terminee, True) == (1, "deja-terminee"),
       repr(module.diagnostiquer("m", terminee, True)))
    ep("contre-temoin-sans-fin",
       module.diagnostiquer("m", en_attente, False) == (1, "sans-fin-au-journal"),
       "une fin INVENTEE serait acceptee : " + repr(module.diagnostiquer("m", en_attente, False)))
    ep("refus-en-cours",
       module.diagnostiquer("m", {"id": "MO-903", "statut": "en-cours"}, True) == (1, "en-cours"),
       repr(module.diagnostiquer("m", {"id": "MO-903", "statut": "en-cours"}, True)))
    ep("refus-inconnue", module.diagnostiquer("m", None, True) == (1, "inconnue"),
       repr(module.diagnostiquer("m", None, True)))
    ep("refus-motif-manquant", module.diagnostiquer("   ", en_attente, True)
       == (2, "motif-manquant"), repr(module.diagnostiquer("   ", en_attente, True)))

    # L ACTE : les cotes qui ecrivent sont remplaces (aucune trace du depot touchee).
    traces_marbre = []
    module.horodater = lambda: "2026-09-28 08:00:00"
    module.declarer_borne_marbre = (
        lambda mission, action, detail, fichiers=None, portes=None, si_absent=True:
        traces_marbre.append((action, si_absent)) or 0)
    module.journaliser_mission = lambda entree: None

    def coherence(cible):
        """Le controle REEL, joue par SA porte sur la racine <cible>. (code, ecarts)."""
        resultat = lancer_enfant([sys.executable, str(porte_suivi), "coherence",
                                  "--racine", str(cible)],
                                  capture_output=True, text=True)
        sortie = resultat.stdout or ""
        accuses = [l for l in sortie.splitlines() if l.startswith("ECART :")]
        return resultat.returncode, accuses, sortie

    with tempfile.TemporaryDirectory(prefix="cobaye-regularisation-") as jetable:
        cobaye = _Chemin(jetable)
        dossier_pilote = cobaye / "_operateur" / "optimus-prime" / "pilote"
        (cobaye / "matrice" / "data").mkdir(parents=True)
        dossier_pilote.mkdir(parents=True)
        chemin_file = dossier_pilote / "file-missions-optimus.json"
        chemin_archive = dossier_pilote / "file-missions-optimus-archive.json"
        chemin_journal = cobaye / "matrice" / "data" / "suivi-optimus.jsonl"
        # MO-901 : la file la dit en-attente, le journal porte DEJA sa fin (le cas
        # paye). MO-902 : la file la dit terminee, le journal N A PAS sa fin (le
        # contre-temoin : cet ecart doit SURVIVRE a la porte).
        evenements = [
            {"mission": "MO-901", "action": "charge"},
            {"mission": "MO-901", "action": "debut"},
            {"mission": "MO-901", "action": "prise"},
            {"mission": "MO-901", "action": "fin"},
            {"mission": "MO-902", "action": "charge"},
            {"mission": "MO-902", "action": "debut"},
        ]
        chemin_journal.write_text("".join(json.dumps(e) + "\n" for e in evenements),
                                  encoding="utf-8", newline="\n")
        chemin_archive.write_text(json.dumps({"missions": []}), encoding="utf-8",
                                  newline="\n")
        chemin_file.write_text(
            json.dumps({"missions": [{"id": "MO-901", "statut": "en-attente",
                                      "theme": "PILOTE"},
                                     {"id": "MO-902", "statut": "terminee",
                                      "theme": "PILOTE"}],
                        "compteur": 9999, "lot": None}),
            encoding="utf-8", newline="\n")
        module.lire_evenements_marbre = lambda: evenements
        module.enregistrer_file = lambda fm: chemin_file.write_text(
            json.dumps(fm), encoding="utf-8", newline="\n")
        charger = lambda: json.loads(chemin_file.read_text(encoding="utf-8"))

        code_avant, accuses_avant, sortie_avant = coherence(cobaye)
        ep("cobaye-rouge-avant", code_avant == 1 and len(accuses_avant) == 3,
           "code=" + str(code_avant) + " ecarts=" + str(len(accuses_avant))
           + " : " + sortie_avant.strip()[-160:])
        ep("cobaye-accuse-les-DEUX", sum(1 for a in accuses_avant if "MO-901" in a) == 2,
           "les 2 ecarts de MO-901 ne sont pas accuses : " + str(accuses_avant))

        code_porte = module.regulariser_mission(charger, "MO-901", "m")
        ep("porte-accepte", code_porte == 0, "la porte refuse MO-901 (code "
           + str(code_porte) + ")")
        apres = charger()
        m901 = next(m for m in apres["missions"] if m["id"] == "MO-901")
        ep("file-dit-terminee", m901.get("statut") == module.STATUT_TERMINEE,
           "statut=" + str(m901.get("statut")))
        ep("motif-et-date-traces",
           m901.get("motif_regularisation") == "m" and m901.get("regularisee_le") == "2026-09-28 08:00:00",
           "motif=" + str(m901.get("motif_regularisation")))
        ep("borne-declaree-IDEMPOTENTE", ("fin", True) in traces_marbre,
           "la fin n est pas declaree idempotente : " + str(traces_marbre))
        ep("acte-a-son-propre-verbe", ("regularisation", True) in traces_marbre,
           "l ACTE n a pas d action a lui : " + str(traces_marbre))
        ep("fin-jamais-deux-fois",
           len([a for a, _ in traces_marbre if a == "fin"]) == 1,
           "la borne de fin est declaree DEUX fois : " + str(traces_marbre))

        code_apres, accuses_apres, sortie_apres = coherence(cobaye)
        ep("les-2-ecarts-TOMBENT-par-la-porte",
           not any("MO-901" in a for a in accuses_apres),
           "MO-901 est encore accuse : " + str(accuses_apres))
        ep("il-en-reste-EXACTEMENT-un", code_apres == 1 and len(accuses_apres) == 1,
           "code=" + str(code_apres) + " ecarts=" + str(len(accuses_apres))
           + " : " + sortie_apres.strip()[-160:])

        code_refus = module.regulariser_mission(charger, "MO-902", "m")
        ep("contre-temoin-REFUSE", code_refus == 1,
           "la porte a accepte une mission SANS fin au journal (code "
           + str(code_refus) + ")")
        apres2 = charger()
        m902 = next(m for m in apres2["missions"] if m["id"] == "MO-902")
        ep("contre-temoin-file-INTACTE",
           m902.get("statut") == module.STATUT_TERMINEE
           and not m902.get("regularisee_le")
           and not m902.get("motif_regularisation"),
           "la file de MO-902 a ete touchee : " + json.dumps(m902))
        code_final, accuses_final, sortie_final = coherence(cobaye)
        ep("contre-temoin-accuse-TOUJOURS",
           code_final == 1 and len(accuses_final) == 1 and "MO-902" in accuses_final[0],
           "code=" + str(code_final) + " : " + sortie_final.strip()[-160:])
    return ecarts


def _eprouver_rouvrir(racine):
    """MAILLON 80 (MO-548 / EO-553) : eprouve la PORTE DE REOUVERTURE du pilote.

    LE MANQUE MESURE : `fin` clos la mission EN COURS, le bilan est ecrit, et plus
    AUCUNE porte ne rend la main. Mesure du 2026-10-02 : la porte `fin` a clos
    MO-534 avec le bilan de MO-547, et le controle de coherence -- qui lit la
    file ET le journal -- ne pouvait pas voir la difference : une mission du
    createur passait pour faite.

    Ce maillon joue la porte sur une RACINE JETABLE (tempfile : aucune trace du
    depot n est touchee) et fait trancher le CONTROLE REEL par sa porte
    (suivi-optimus coherence --racine <cobaye>) :
      - la DECISION est PURE : huit cas sans toucher une trace, dont le
        CONTRE-TEMOIN de la regle du motif (une branche de refus que rien ne peut
        atteindre ne garde rien -- lecon L-032) ;
      - elle MORD : le bilan faux est RETIRE et CONSERVE, la mission redevient A
        FAIRE avec sa date et son compteur, l ACTE a son action a lui, et le
        COHERENTIEL file <-> journal n accuse plus la mission -- la borne
        `rouverture` neutralise son debut et annule sa fin anterieure, comme
        `report` le fait depuis EO-190 ;
      - elle EPARGNE (contre-temoin sur le MEME etat) : on retire la borne
        `rouverture` du journal du cobaye -- c est exactement ce que faisait la
        premiere version de la porte -- et le meme controle accuse la mission
        DEUX fois. Une mission en-attente dont le journal porte une fin sans
        rouverture (MO-904) reste accusee elle aussi ;
      - elle NOMME ses refus : motif manquant, motif qui ne nomme rien, id
        inconnu, ce qui est deja a faire, ce qui est deja ouvert, en cours, bilan
        deja retire ;
      - elle verifie le CABLAGE : le verbe est route par main.py, son usage est
        documente, l action `rouverture` est au vocabulaire de suivi-optimus et
        n est PAS SINGULIERE (une mission peut etre rouverte plusieurs fois).
    """
    import importlib.util
    import json
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    pilote = matrice / "_operateur" / "optimus-prime" / "pilote"
    domicile = pilote / "rouvrir" / "fonctions.py"
    router = pilote / "main.py"
    suivi = matrice / "matrice" / "data" / "outils" / "suivi-optimus"
    porte_suivi = suivi / "main.py"
    constantes_suivi = suivi / "constants.py"
    for chemin in (domicile, router, porte_suivi, constantes_suivi):
        if not chemin.is_file():
            return ["fichier INTROUVABLE : " + str(chemin)]

    # CABLAGE : trois fils, et chacun est un fil qu on peut oublier en silence.
    texte_router = router.read_text(encoding="utf-8")
    texte_constantes = constantes_suivi.read_text(encoding="utf-8")
    ecarts = []
    if "from rouvrir.entry import executer as rouvrir_executer" not in texte_router:
        ecarts.append("le routeur n importe pas la categorie rouvrir")
    if '"rouvrir": rouvrir_executer' not in texte_router:
        ecarts.append("le verbe rouvrir n est PAS route par main.py")
    if "rouvrir --id MO-XXX --motif" not in texte_router:
        ecarts.append("l usage de rouvrir n est pas documente dans la facade")
    if '"rouverture"' not in texte_constantes:
        ecarts.append("l action `rouverture` n est pas au vocabulaire de suivi-optimus")
    debut_singulieres = texte_constantes.find("ACTIONS_SINGULIERES = (")
    if debut_singulieres != -1:
        fin_singulieres = texte_constantes.find(")", debut_singulieres)
        if "rouverture" in texte_constantes[debut_singulieres:fin_singulieres]:
            ecarts.append("`rouverture` est dans ACTIONS_SINGULIERES : une mission "
                          "rouverte deux fois passerait pour un doublon a archiver")

    sys.path.insert(0, str(pilote))
    try:
        specification = importlib.util.spec_from_file_location(
            "rouvrir_fonctions", domicile)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["rouvrir/fonctions.py ILLISIBLE ("
                         + type(erreur).__name__ + " : " + str(erreur)[:60] + ")"]
    finally:
        sys.path.remove(str(pilote))

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    # LA DECISION, PURE : huit cas, aucun disque. Une mission close dont le bilan
    # annonce une AUTRE mission -- c est le fait que la porte vient (MO-534,
    # MO-527), donc le cas est reproduit tel quel.
    close = {"id": "MO-901", "statut": "terminee", "theme": "PILOTE",
             "bilan": "MO-902 (CONSTRUCTEUR, item EO-900) -- le travail de MO-902\n"}
    ep("motif-manquant", module.diagnostiquer("   ", close)
       == (2, "motif-manquant"), repr(module.diagnostiquer("   ", close)))
    ep("inconnue", module.diagnostiquer("MO-901", None)
       == (1, "inconnue"), repr(module.diagnostiquer("MO-901", None)))
    ep("deja-en-attente",
       module.diagnostiquer("MO-901", {"id": "MO-901", "statut": "en-attente"})
       == (1, "deja-en-attente"),
       repr(module.diagnostiquer("MO-901", {"id": "MO-901", "statut": "en-attente"})))
    ep("en-cours",
       module.diagnostiquer("MO-901", {"id": "MO-901", "statut": "en-cours"})
       == (1, "en-cours"),
       repr(module.diagnostiquer("MO-901", {"id": "MO-901", "statut": "en-cours"})))
    # LE CAS REEL, PAS LE CAS LISIBLE : une mission rouverte porte a la fois
    # `bilan_retire` ET `statut = en-attente`. C est cette combinaison-la qui
    # rendait la branche `bilan-deja-retire` INATTEIGNABLE (MO-548) -- un second
    # essai ne recevait que < deja en-attente >, sans jamais nommer le retrait
    # precedent ni son motif. Aucune donnee n est une chaine multi-lignes ici :
    # `diagnostiquer` ne lit que le statut et `bilan_retire`, donc un texte d une
    # seule ligne suffit (et evite d ecrire un retour a la ligne dans un litteral).
    rouverte = {"id": "MO-901", "statut": "en-attente", "theme": "PILOTE",
                "bilan": "BILAN MO-901 -- RETIRE LE 2026-10-02 22:00:00",
                "bilan_retire": {"date": "2026-10-02 22:00:00", "motif": "m",
                                 "texte": "bilan d autrui"}}
    ep("bilan-deja-retire-ATTEIGNABLE-sur-le-cas-reel",
       module.diagnostiquer("MO-901", rouverte) == (1, "bilan-deja-retire"),
       repr(module.diagnostiquer("MO-901", rouverte)))
    ep("bilan-deja-retire-sur-le-cas-lisible",
       module.diagnostiquer("MO-901", dict(close, bilan_retire={"date": "2026-10-02"}))
       == (1, "bilan-deja-retire"),
       repr(module.diagnostiquer("MO-901",
                                 dict(close, bilan_retire={"date": "2026-10-02"}))))
    # LE CONTRE-TEMOIN DU MOTIF : la regle exige que le motif NOMME ce qu il
    # retire. Premier jet : les ids du bilan comptaient comme nommes, donc la
    # branche de refus etait INATTEIGNABLE par aucun motif -- un garde qui ne
    # peut pas dire NON ne garde rien (lecon L-032).
    ep("motif-qui-ne-nomme-rien-est-refuse",
       module.diagnostiquer("je reprends le travail forget", close)
       == (2, "travail-non-nomme"),
       repr(module.diagnostiquer("je reprends le travail forget", close)))
    ep("ouverture-par-son-id",
       module.diagnostiquer("MO-901 : le bilan est repris", close)
       == (0, "ouverture"),
       repr(module.diagnostiquer("MO-901 : le bilan est repris", close)))
    ep("ouverture-par-l-id-annonce",
       module.diagnostiquer("le bilan de MO-902 ne vaut pas pour MO-901", close)
       == (0, "ouverture"),
       repr(module.diagnostiquer("le bilan de MO-902 ne vaut pas pour MO-901", close)))

    def coherence(cible):
        """Le controle REEL, joue par SA porte sur la racine <cible>."""
        resultat = lancer_enfant([sys.executable, str(porte_suivi), "coherence",
                                  "--racine", str(cible)],
                                 capture_output=True, text=True)
        sortie = resultat.stdout or ""
        return (resultat.returncode,
                [l for l in sortie.splitlines() if l.startswith("ECART :")],
                [l for l in sortie.splitlines() if l.startswith("DETTE :")],
                sortie)

    with tempfile.TemporaryDirectory(prefix="cobaye-rouvrir-") as jetable:
        cobaye = _Chemin(jetable)
        dossier_pilote = cobaye / "_operateur" / "optimus-prime" / "pilote"
        (cobaye / "matrice" / "data").mkdir(parents=True)
        dossier_pilote.mkdir(parents=True)
        chemin_file = dossier_pilote / "file-missions-optimus.json"
        chemin_archive = dossier_pilote / "file-missions-optimus-archive.json"
        chemin_journal = cobaye / "matrice" / "data" / "suivi-optimus.jsonl"
        evenements = [
            {"mission": "MO-901", "action": "debut"},
            {"mission": "MO-901", "action": "fin"},
            {"mission": "MO-902", "action": "debut"},
            {"mission": "MO-902", "action": "fin"},
            {"mission": "MO-903", "action": "debut"},
            {"mission": "MO-904", "action": "debut"},
            {"mission": "MO-904", "action": "fin"},
        ]
        chemin_journal.write_text("".join(json.dumps(e) + "\n" for e in evenements),
                                  encoding="utf-8", newline="\n")
        chemin_archive.write_text(json.dumps({"missions": []}), encoding="utf-8",
                                  newline="\n")
        # MO-901 : terminee, fin au journal -- SAIN, c est la porte qui va le
        # rendre A FAIRE. MO-903 : en-attente, un debut SANS bornage (1 ecart).
        # MO-904 : en-attente, une fin SANS rouverture (2 ecarts) -- c est l etat
        # que produisait la premiere version de la porte, et son contre-temoin.
        chemin_file.write_text(
            json.dumps({"missions": [
                {"id": "MO-901", "statut": "terminee", "theme": "PILOTE",
                 "bilan": "MO-902 (CONSTRUCTEUR, item EO-900) -- le travail de MO-902\n"},
                {"id": "MO-902", "statut": "terminee", "theme": "PILOTE",
                 "bilan": "BILAN MO-902 -- fait\n"},
                {"id": "MO-903", "statut": "en-attente", "theme": "PILOTE"},
                {"id": "MO-904", "statut": "en-attente", "theme": "PILOTE"},
            ], "compteur": 9999, "lot": None}),
            encoding="utf-8", newline="\n")

        # Les trois ecrivains du depot sont DETOURNES vers le cobaye : une porte
        # qui ecrit dans la vraie file pendant qu on la met a l epreuve ruinerait
        # la trace qu elle est censee proteger.
        traces_marbre, journalisees = [], []
        module.horodater = lambda: "2026-10-02 22:00:00"
        module.enregistrer_file = lambda fm: chemin_file.write_text(
            json.dumps(fm), encoding="utf-8", newline="\n")

        def borne_jetable(mission, action, detail, fichiers=None, portes=None):
            """La borne du marbre, ecrite dans le JOURNAL DU COBAYE (et nowhere
            d ailleurs) : le controle de coherence doit la lire pour de vrai."""
            evenement = {"mission": mission.get("id"),
                         "theme": mission.get("theme", ""), "action": action,
                         "detail": detail, "fichiers": list(fichiers or []),
                         "portes": list(portes or []), "date": "2026-10-02 22:00:00",
                         "duree_s": ""}
            with open(chemin_journal, "a", encoding="utf-8", newline="\n") as flux:
                flux.write(json.dumps(evenement, ensure_ascii=True) + "\n")
            traces_marbre.append((action, list(portes or [])))
            return 0

        module.declarer_borne_marbre = borne_jetable
        module.journaliser_mission = lambda entree: journalisees.append(entree)
        charger = lambda: json.loads(chemin_file.read_text(encoding="utf-8"))
        avant_refus = chemin_file.read_text(encoding="utf-8")
        avant_journal = chemin_journal.read_text(encoding="utf-8")

        # LES REFUS, AVANT toute ecriture : une porte qui refuse en ecrivant ne
        # refuse pas (elle pollue).
        ep("porte-refuse-sans-motif",
           module.rouvrir_mission(charger, "MO-901", "   ") == 2,
           "un motif vide serait accepte")
        ep("porte-refuse-un-motif-qui-ne-nomme-rien",
           module.rouvrir_mission(charger, "MO-901", "je reprends le travail") == 2,
           "un motif qui ne nomme rien serait accepte")
        ep("porte-refuse-un-id-inconnu",
           module.rouvrir_mission(charger, "MO-777", "MO-777") == 1,
           "un id inconnu serait accepte")
        ep("porte-refuse-ce-qui-est-deja-a-faire",
           module.rouvrir_mission(charger, "MO-903", "MO-903") == 1,
           "une mission en-attente serait rouverte")
        ep("les-refus-n-ont-rien-ecrit",
           chemin_file.read_text(encoding="utf-8") == avant_refus
           and chemin_journal.read_text(encoding="utf-8") == avant_journal
           and not traces_marbre and not journalisees,
           "la file, le journal ou la trace ont bouge a un refus : "
           + str(traces_marbre) + " / " + str(journalisees))

        # L OUVERTURE, REELLEMENT jouee sur le cobaye.
        code_porte = module.rouvrir_mission(
            charger, "MO-901", "le bilan de MO-902 ne vaut pas pour MO-901")
        ep("porte-accepte", code_porte == 0, "code=" + str(code_porte))
        apres = charger()
        m901 = next(m for m in apres["missions"] if m["id"] == "MO-901")
        ep("file-dit-A-FAIRE", m901.get("statut") == "en-attente",
           "statut=" + str(m901.get("statut")))
        ep("motif-date-et-compteur-traces",
           (m901.get("motif_rouverture") or "").startswith("le bilan de MO-902")
           and m901.get("rouverte_le") == "2026-10-02 22:00:00"
           and m901.get("compteur_rouvertures") == 1,
           "motif=" + str(m901.get("motif_rouverture")) + " date="
           + str(m901.get("rouverte_le")) + " compteur="
           + str(m901.get("compteur_rouvertures")))
        # LE FILTRE EST ECRIT AVEC `in`, JAMAIS `splitlines()[i].startswith(...)` :
        # cette seconde forme est celle d une EXTRACTION de sortie (le filtre d un
        # garde sur les lignes de sa sortie), et le garde des filtres
        # (verifier-extraction-ecarts) l accuse a tort quand le filtre ne
        # correspond a aucun producteur imprime -- meme famille de faux positif que
        # `garde-segment` et les acces d attribut (item EO-561).
        lignes = (m901.get("bilan") or "").splitlines()
        tete = lignes[0] if lignes else "(vide)"
        ep("le-bilan-fautif-est-RETIRE-pas-efface",
           "BILAN MO-901 -- RETIRE" in tete and "MO-902" not in tete,
           "1re ligne du bilan=" + tete[:90])
        texte_retire = (m901.get("bilan_retire") or {}).get("texte", "")
        ep("le-texte-fautif-est-CONSERVE", "MO-902" in texte_retire[:80],
           "bilan_retire=" + json.dumps(m901.get("bilan_retire"),
                                        ensure_ascii=True)[:140])
        ep("l-acte-a-son-propre-action",
           traces_marbre == [("rouverture", ["pilote:rouvrir"])],
           "traces=" + str(traces_marbre))
        ep("la-fin-n-est-pas-redeposee",
           not [a for a, _ in traces_marbre if a == "fin"],
           "la borne de fin a ete rejouee : " + str(traces_marbre))
        ep("porte-refuse-ce-qui-est-deja-ouvert",
           module.rouvrir_mission(
               charger, "MO-901", "le bilan de MO-902 ne vaut pas pour MO-901") == 1,
           "une mission deja rouverte serait rouverte deux fois")

        # LE COHERENTIEL, juge par le CONTROLE REEL sur la racine du cobaye.
        code_avec, accuses_avec, dettes_avec, sortie_avec = coherence(cobaye)
        ep("la-mission-rouverte-n-est-plus-accusee",
           not any("MO-901" in a for a in accuses_avec),
           "MO-901 est encore accuse : " + str(accuses_avec))
        ep("et-elle-est-DITE-comme-dette",
           any("MO-901" in d and "ROUVRTE" in d for d in dettes_avec),
           "dettes=" + str(dettes_avec))
        ep("les-autres-ecarts-SURVIVENT",
           any("MO-903" in a for a in accuses_avec)
           and any("MO-904" in a for a in accuses_avec),
           "les contre-temoins ont disparu : " + str(accuses_avec))
        # LE CONTRE-TEMOIN, SUR LE MEME ETAT : on retire la borne `rouverture`
        # du journal -- c est EXACTEMENT ce que faisait la premiere version de la
        # porte -- et le meme controle doit accuser la mission DEUX fois.
        avec_borne = chemin_journal.read_text(encoding="utf-8")
        chemin_journal.write_text(
            "".join(ligne + "\n" for ligne in avec_borne.splitlines()
                    if '"rouverture"' not in ligne),
            encoding="utf-8", newline="\n")
        code_sans, accuses_sans, dettes_sans, sortie_sans = coherence(cobaye)
        chemin_journal.write_text(avec_borne, encoding="utf-8", newline="\n")
        ep("contre-temoin-SANS-la-borne-l-ecart-revient",
           code_sans == 1
           and sum(1 for a in accuses_sans if "MO-901" in a) == 2,
           "code=" + str(code_sans) + " : " + sortie_sans.strip()[-200:])
        ep("et-il-ne-revient-QU-A-CA", len(dettes_sans) == 0,
           "dettes sans la borne=" + str(dettes_sans))
    return ecarts


def _eprouver_interruption(racine):
    """MAILLON 58 (MO-464 / EO-436) : l INTERRUPTION PARQUE, elle ne CHARGE pas.

    La panne payee : quand un round est INTERROMPU, le pilote PARQUE sa courante
    (`report`) et FORGE la suivante (`charge`) dans la MEME seconde -- mesure du
    2026-09-25 : report MO-409 a 09:54:00, charge MO-416 a 09:54:01 ; MEME mesure le
    2026-09-28 : report MO-461 a 06:51:48, charge MO-486 a 06:51:48. Le round courant
    n est pas ferme : DEUX missions sont OUVERTES dans la file (la parquee, qui
    reprendra son round, et la forgee, que personne ne sert), la file ne dit plus
    QUELLE mission le round reprend, et le suivi du pilote a accuse une CLOTURE
    FAUSSE qui n avait PAS eu lieu.

    Ce maillon eprouve, sur une FILE COBAYE EN MEMOIRE (aucune trace du depot n est
    touchee : les cotes qui ecrivent sont remplaces) :
      - le JUGEMENT (pur, importe de son domicile data/commun/interruption.py) : il
        MORD sur une mission PARQUEE (en-attente + reporte_le) et EPARGNE la file
        ordinaire (en-attente sans report : elle ATTEND son tour) et un round EN COURS ;
      - le GESTE MESURE : `charger` REFUSE de forger pendant qu un round parque attend
        sa reprise -- le bug est mort, l ancien geste n a plus de chemin -- et la file
        n est PAS touchee ;
      - le REMEDE : `charger --conduire` FORGE ET SERT dans le MEME geste (le service
        est appele, la PRISE est notee), donc aucune mission forgee ne reste sans
        round ;
      - le CONTRE-TEMOIN : une file SANS round parque charge normalement ;
      - le CABLAGE : les DEUX chargements (mission simple et LOT) consomment le MEME
        refus, l usage de `--conduire` est documente, et l exception OUVERTE de
        `cloture-fausse` a ete LEVEE (la classe est reparee, pas blanchie).
    LIMITE DITE : le SERVICE lui-meme (`preparer_injection`) est REMPLACE par un faux
    fidele au contrat -- l appeler pour de vrai ecrirait dans l ARBRE REEL (c est
    exactement la faute payee en eprouvant ce round). Le maillon prouve donc le
    CABLAGE (un seul geste, prise notee) et le JUGEMENT, pas l injection.
    """
    import importlib.util
    import json
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    pilote = matrice / "_operateur" / "optimus-prime" / "pilote"
    domicile = matrice / "matrice" / "data" / "commun" / "interruption.py"
    fonctions = pilote / "file" / "fonctions.py"
    router = pilote / "main.py"
    declaration = matrice / "_operateur" / "optimus-prime" / "suivi-pilote" / "pannes-declarees.json"
    for chemin in (domicile, fonctions, router, declaration):
        if not chemin.is_file():
            return ["fichier INTROUVABLE : " + str(chemin)]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    # CABLAGE : les DEUX chargements consomment le MEME refus, l usage est documente,
    # et l exception ouverte de cloture-fausse a ete LEVEE (sinon la classe reparee
    # resterait couverte par une excuse).
    texte_fonctions = fonctions.read_text(encoding="utf-8")
    if texte_fonctions.count("refus_parquage_en_attente(") < 2:
        ecarts.append("le refus d interruption n est pas consomme par les DEUX"
                      " chargements (mission simple ET lot)")
    if "--conduire" not in router.read_text(encoding="utf-8"):
        ecarts.append("l usage de `charger --conduire` n est pas documente dans la facade")
    try:
        pannes = json.loads(declaration.read_text(encoding="utf-8")).get("pannes") or []
    except ValueError:
        pannes = []
        ecarts.append("pannes-declarees.json ILLISIBLE (JSON invalide)")
    cloture = next((p for p in pannes if p.get("id") == "cloture-fausse"), None)
    if cloture is None:
        ecarts.append("la panne cloture-fausse a disparu de la declaration")
    elif cloture.get("ouverte"):
        ecarts.append("l exception OUVERTE de cloture-fausse n a pas ete levee : la"
                      " classe est reparee, elle ne doit plus etre couverte")

    # LE JUGEMENT : pur, importe de son domicile, eprouve sans aucune trace.
    specification = importlib.util.spec_from_file_location("interruption_jugement", domicile)
    jugement = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(jugement)
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["interruption.py ILLISIBLE (" + type(erreur).__name__
                         + " : " + str(erreur)[:60] + ")"]
    parquee = {"id": "MO-890", "statut": "en-attente", "theme": "PILOTE",
               "reporte_le": "2026-09-25 09:54:00", "raison_report": "Round interrompu"}
    attente = {"id": "MO-891", "statut": "en-attente", "theme": "PILOTE"}
    en_cours = {"id": "MO-892", "statut": "en-cours", "theme": "PILOTE"}

    def fichier(liste):
        return {"missions": [dict(m) for m in liste], "compteur": 899, "lot": None}

    ep("mord-round-parque",
       jugement.round_parque_en_attente(fichier([parquee])) is not None,
       "une mission parquee qui attend sa reprise n est pas vue")
    ep("epargne-attente-ordinaire",
       jugement.round_parque_en_attente(fichier([attente])) is None,
       "une mission en-attente SANS report est prise pour une interruption")
    ep("epargne-round-en-cours",
       jugement.round_parque_en_attente(fichier([parquee, en_cours])) is None,
       "un round EN COURS tient le creneau : il n y a plus rien a reprendre")

    # LE GESTE REEL : `charger` sur une file cobaye en memoire.
    sys.path.insert(0, str(pilote))
    try:
        specification = importlib.util.spec_from_file_location("file_fonctions_cobaye", fonctions)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        import injection.fonctions as injection_fonctions
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["file/fonctions.py ILLISIBLE (" + type(erreur).__name__
                         + " : " + str(erreur)[:60] + ")"]
    finally:
        sys.path.remove(str(pilote))

    etat = {}

    def charger():
        return json.loads(json.dumps(etat["file"]))

    def enregistrer(file_missions):
        etat["file"] = json.loads(json.dumps(file_missions))

    module.enregistrer_file = enregistrer
    module.noter_journal = lambda *a, **k: (0, "trace")
    module.declarer_borne_marbre = lambda *a, **k: 0
    module.horodater = lambda: "2026-09-28 09:00:00"
    module.prochain_id = lambda file_missions: "MO-900"
    module.defcon_bloque_theme = lambda theme: (0, "")
    prises = []
    module.noter_prise_round = lambda file_missions=None: prises.append(1) or 0
    servis = []

    def faux_preparer(charger_file, enchainer=False, mission_forcee=None):
        """Le CONTRAT du service, sans son ecriture (elle toucherait l arbre REEL)."""
        fichier_courant = charger_file()
        for mission in fichier_courant.get("missions", []):
            if mission.get("id") == mission_forcee:
                mission["statut"] = "en-cours"
                mission["injectee_le"] = "2026-09-28 09:00:00"
        enregistrer(fichier_courant)
        servis.append(mission_forcee)
        return 0

    injection_fonctions.preparer_injection = faux_preparer
    afficher = lambda file_missions: 0
    base = {"missions": [dict(parquee)], "compteur": 899, "lot": None}

    # (1) LE GESTE MESURE EST REFUSE, et la file n est pas touchee.
    etat["file"] = json.loads(json.dumps(base))
    code = module.charger_mission(["--theme", "PILOTE", "--type", "reparation",
                                   "--objectif", "demande urgente"], charger, afficher)
    ep("le-geste-mesure-est-REFUSE", code == 1,
       "charger a forge pendant qu un round parque attendait sa reprise (code "
       + str(code) + ")")
    ep("le-refus-ne-touche-PAS-la-file",
       [m.get("id") for m in etat["file"]["missions"]] == ["MO-890"],
       "la file a change : " + json.dumps(etat["file"]))

    # (2) LE REMEDE : forger ET servir dans le MEME geste.
    etat["file"] = json.loads(json.dumps(base))
    servis[:] = []
    prises[:] = []
    code = module.charger_mission(["--theme", "PILOTE", "--type", "reparation",
                                   "--objectif", "demande urgente", "--conduire"],
                                  charger, afficher)
    ep("le-remede-sert-dans-le-meme-geste",
       code == 0 and servis == ["MO-900"] and len(prises) == 1,
       "code=" + str(code) + " servis=" + str(servis) + " prises=" + str(len(prises)))
    ep("aucune-mission-forgee-sans-round",
       [m.get("statut") for m in etat["file"]["missions"] if m.get("id") == "MO-900"]
       == ["en-cours"],
       "la mission forgee n est pas servie : "
       + json.dumps(etat["file"]["missions"], ensure_ascii=False)[:200])

    # (3) CONTRE-TEMOIN : une file SANS round parque charge normalement.
    etat["file"] = {"missions": [dict(attente)], "compteur": 899, "lot": None}
    code = module.charger_mission(["--theme", "PILOTE", "--type", "reparation",
                                   "--objectif", "mission ordinaire"], charger, afficher)
    ep("contre-temoin-file-ordinaire",
       code == 0 and [m.get("statut") for m in etat["file"]["missions"]] == ["en-attente",
                                                                             "en-attente"],
       "code=" + str(code) + " file=" + json.dumps(etat["file"]["missions"])[:160])

    # (4) LE LOT : un lot ne SERT rien dans le geste, il tombe sous le MEME refus.
    etat["file"] = json.loads(json.dumps(base))
    code = module.charger_lot(["--lot", "COBAYE", "--theme", "PILOTE", "--type",
                               "reparation", "--objectif", "un"], charger)
    ep("le-LOT-tombe-sous-le-meme-refus", code == 1,
       "charger_lot a forge pendant un parquage (code " + str(code) + ")")
    ep("le-refus-du-LOT-ne-touche-PAS-la-file",
       [m.get("id") for m in etat["file"]["missions"]] == ["MO-890"],
       "la file a change : " + json.dumps(etat["file"])[:160])
    return ecarts


def _eprouver_controles_inverses(racine):
    """MAILLON 59 (MO-487 / EO-462) : un controle dont l etat NORMAL est ROUGE est INVERSE.

    La plainte du createur (2026-09-28) : nos controles affichaient ROUGE alors que
    leur etat normal est VERT, ce qui obligeait a se souvenir en permanence que le
    rouge etait normal. DEUX cas mesures :
      (1) l epreuve `invisibilite` du benchmark rendait ROUGE < FUITE L-016 > tout
          fichier de NOTRE zone invisible -- le cas NORMAL de nos fichiers -- et le
          protocole devait rappeler < 1 ROUGE attendu > a chaque round (heritage
          MO-216). Elle CONSTATE desormais la zone : VERT dans les DEUX cas normaux.
      (2) le declencheur `perimetre-write` de la defcon s allumait (niveau 5) sur
          `.kilo/.gitignore`, un fichier de l OUTIL EXTERIEUR declare : un artefact
          declare a moitie laisse un rouge qu on doit se rappeler normal (EO-408).

    Ce maillon JOUE les deux cas normaux ET leurs CONTRE-TEMOINS :
      - epreuve : la sortie REELLE du benchmark (sous-processus) dit VERT sur un
        fichier de notre zone invisible ; le CONTRE-TEMOIN rejoue l ANCIENNE regle
        (`ok = not est_zone_invisible`) sur ce meme fichier : elle MORD encore -- le
        defaut etait reel, pas suppose ;
      - declencheur : le DOMICILE partage met de cote le fichier de l outil exterieur
        (`.kilo/.gitignore`), et le CONTRE-TEMOIN (un fichier lambda hors de `.kilo`)
        reste une violation a part entiere -- une exemption large rendrait le garde
        aveugle a ce qu il doit garder.
    """
    import importlib.util
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    commun = matrice / "matrice" / "data" / "commun"
    invisibilite = commun / "invisibilite.py"
    artefacts = commun / "artefacts_externes.py"
    benchmark = matrice / "matrice" / "data" / "outils" / "benchmark" / "main.py"
    garde = (matrice / "_operateur" / "optimus-prime" / "super-combos" / "combos"
             / "outils" / "garde-perimetre-write.py")
    invisible = matrice / "_operateur" / "optimus-prime" / "pilote" / "main.py"
    for chemin in (invisibilite, artefacts, benchmark, garde, invisible):
        if not chemin.is_file():
            return ["fichier INTROUVABLE : " + str(chemin)]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    def charger_module(alias, chemin):
        specification = importlib.util.spec_from_file_location(alias, chemin)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        return module

    # --- (1) L EPREUVE `invisibilite` : le cas NORMAL est VERT.
    try:
        jugement = charger_module("invisibilite_domicile", invisibilite)
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["invisibilite.py ILLISIBLE (" + type(erreur).__name__
                         + " : " + str(erreur)[:60] + ")"]
    dans_notre_zone = jugement.est_invisible(invisible)
    ep("le-fichier-de-notre-zone-est-BIEN-invisible", dans_notre_zone is True,
       "un fichier de notre zone n est pas vu comme invisible")
    # CONTRE-TEMOIN : l ANCIENNE regle rendait ROUGE sur ce MEME fichier.
    ep("contre-temoin-l-ancienne-regle-rendait-ROUGE",
       (not dans_notre_zone) is False,
       "l ancienne regle ne mordait pas : le defaut n est pas reproduit, la preuve"
       " ne vaut rien")

    complet = lancer_enfant([sys.executable, str(benchmark), "benchmark",
                             "--fichier", str(invisible)],
                            capture_output=True, text=True, cwd=str(matrice))
    sortie = (complet.stdout or "") + (complet.stderr or "")
    lignes = [ligne.strip() for ligne in sortie.splitlines() if "invisibilite" in ligne]
    ep("l-epreuve-REELLE-dit-VERT", "VERT invisibilite" in sortie,
       "la sortie du benchmark ne porte pas [VERT invisibilite] : " + " | ".join(lignes)[:160])
    ep("la-sortie-NE-porte-PLUS-de-fuite", "FUITE L-016" not in sortie,
       "la sortie porte encore [FUITE L-016] (le rouge du cas normal)")

    # --- (2) LE DECLENCHEUR `perimetre-write` : l artefact exterieur est mis de cote.
    try:
        declaration = charger_module("artefacts_domicile", artefacts)
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["artefacts_externes.py ILLISIBLE (" + type(erreur).__name__
                         + " : " + str(erreur)[:60] + ")"]
    gitignore = racine / ".kilo" / ".gitignore"
    ep("l-artefact-exterieur-est-mis-de-cote",
       declaration.artefact_de(gitignore, racine) is not None,
       ".kilo/.gitignore n est PAS reconnu comme artefact : le declencheur"
       " perimetre-write s allumerait sur le cas NORMAL")
    # CONTRE-TEMOIN : une ecriture REELLE hors de `.kilo` reste une violation.
    ep("contre-temoin-une-ecriture-reelle-reste-accusee",
       declaration.artefact_de(racine / "hors-perimetre.txt", racine) is None,
       "un fichier lambda hors de .kilo est mis de cote : l exemption est trop large")

    complet = lancer_enfant([sys.executable, str(garde), "--racine", str(racine),
                             "--jours", "7"], capture_output=True, text=True,
                            cwd=str(racine))
    sortie = (complet.stdout or "") + (complet.stderr or "")
    ep("le-garde-REPOND",
       ("Perimetre sain" in sortie) or ("PERIMETRE VIOLE" in sortie),
       "le garde n a pas rendu de verdict : " + sortie.strip()[:160])
    suite_verdict = (sortie.split("PERIMETRE VIOLE", 1)[1]
                     if "PERIMETRE VIOLE" in sortie else "")
    ep("le-garde-n-accuse-PAS-l-artefact-exterieur", ".kilo" not in suite_verdict,
       "le garde accuse encore .kilo dans son verdict : " + suite_verdict[:160])

    return ecarts


def _detecter_copies_ascii(donnees):
    """Ou VIT la regle ASCII dans <donnees> (matrice/data) ? Rend la liste des ecarts.

    Le DETECTEUR est isole de la suite pour pouvoir etre JOUE sur des arbres
    FABRIQUES (le cobaye ne peut pas salir l arbre reel). Une regle vit a UN
    domicile (M-076), et `unicodedata.normalize` est la MARQUE de la conversion
    ASCII (NFKD) : elle ne doit donc apparaitre QUE dans
    data/commun/texte_ascii.py. Toute autre occurrence est une COPIE qui divergera
    en silence (L-029 ; EO-365 / MO-466) : chercher `NFKD` tout court accuserait
    les COMMENTAIRES qui racontent l histoire du domicile, d ou la marque de CODE.
    """
    donnees = Path(donnees)
    domicile = donnees / "commun" / "texte_ascii.py"
    if not domicile.is_file():
        return ["le DOMICILE manque : " + str(domicile)]
    try:
        texte_domicile = domicile.read_text(encoding="utf-8")
    except OSError as erreur:
        return ["domicile ILLISIBLE : " + type(erreur).__name__ + " : " + str(erreur)[:60]]
    ecarts = []
    if "unicodedata.normalize" not in texte_domicile:
        ecarts.append("le domicile ne porte PLUS la regle (unicodedata.normalize absent)")
    if "def vers_ascii" not in texte_domicile:
        ecarts.append("le domicile n expose plus vers_ascii")
    for chemin in sorted(donnees.rglob("*.py")):
        if chemin == domicile:
            continue
        try:
            contenu = chemin.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "unicodedata.normalize" in contenu:
            ecarts.append("COPIE de la regle ASCII hors de son domicile : "
                          + str(chemin.relative_to(donnees)).replace("\\", "/"))
    return ecarts


def _une_lettre_oubliee_est_proposee(module, parc):
    """Le cobaye COMMUN aux deux consommateurs (MO-468) : une lettre oubliee au MILIEU
    d un nom REEL doit etre PROPOSEE par le refus du module. Le resultat n est alors
    plus une SOUS-CHAINE du nom : seule la PROXIMITE du domicile peut le retrouver.
    Rend True des qu UN cas le prouve (un parc ou AUCUN nom n est assez long ne prouve
    rien -- c est dit par False, jamais lu comme un succes).
    """
    for candidat in parc:
        if len(candidat) < 12:
            continue
        milieu = len(candidat) // 2
        essai = candidat[:milieu] + candidat[milieu + 1:]
        if not essai or essai in parc:
            continue
        return candidat in module.refus_nom(essai)
    return False


def _detecter_copies_noms_proches(matrice):
    """Ou VIT la regle des NOMS PROCHES (inclusion + proximite) ? Rend les ecarts.

    Le DETECTEUR est isole de la suite pour pouvoir etre JOUE sur des arbres FABRIQUES
    (le cobaye ne peut pas salir l arbre reel). La regle a UN domicile (M-076) :
    matrice/data/commun/noms_proches.py. Sa MARQUE est un appel de CODE a difflib --
    chercher le nom de la bibliotheque tout court accuserait les COMMENTAIRES qui
    racontent l histoire du domicile (lecon L-029 ; EO-384 / MO-468).

    LE DETECTEUR JUGE LES DEUX ARBRES : la regle est consommee par la MATRICE
    (resolution_outils : les briques nommables) ET par le PILOTE (modes_emploi : les
    briques servables). Une copie peut donc repousser des DEUX cotes -- c est la mesure
    meme de ce round : deux comportements sous un seul nom de regle.
    """
    matrice = Path(matrice).resolve()
    domicile = matrice / "matrice" / "data" / "commun" / "noms_proches.py"
    if not domicile.is_file():
        return ["le DOMICILE manque : " + str(domicile)]
    try:
        texte_domicile = domicile.read_text(encoding="utf-8")
    except OSError as erreur:
        return ["domicile ILLISIBLE : " + type(erreur).__name__ + " : " + str(erreur)[:60]]
    ecarts = []
    if "get_close_matches" not in texte_domicile:
        ecarts.append("le domicile ne porte PLUS la regle (appel difflib absent)")
    if "def proches(" not in texte_domicile:
        ecarts.append("le domicile n expose plus proches")
    # CE FICHIER EST HORS DU SCAN : il CITE la marque (et la fabrique pour ses cobayes),
    # il ne la RECOPIE pas. Accuser une citation serait un FAUX POSITIF, et un garde qui
    # crie a tort n est jamais branche (lecon deja payee) : une copie REELLE vit dans un
    # AUTRE fichier.
    soi = Path(__file__).resolve()
    # UNE REGLE PARTAGEE QUE PLUS PERSONNE N APPELLE EST UNE REGLE MORTE : le jour ou
    # un consommateur cesse de la consommer, sa copie revient. Les deux sont NOMMES.
    consommateurs = (
        (matrice / "matrice" / "data" / "commun" / "resolution_outils.py", "la Matrice"),
        (matrice / "_operateur" / "optimus-prime" / "pilote" / "injection" / "modes_emploi.py",
         "le pilote"),
    )
    for chemin, qui in consommateurs:
        if not chemin.is_file():
            ecarts.append("le consommateur " + qui + " MANQUE : " + str(chemin))
            continue
        try:
            contenu = chemin.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "from noms_proches import" not in contenu or "proches(" not in contenu:
            ecarts.append(qui + " ne CONSOMME plus le domicile (noms_proches) : "
                          + chemin.relative_to(matrice).as_posix())
    exclus = ("__pycache__", "tmp-optimus")
    for racine in (matrice / "matrice" / "data", matrice / "_operateur" / "optimus-prime"):
        if not racine.is_dir():
            continue
        for chemin in sorted(racine.rglob("*.py")):
            if chemin == domicile or chemin == soi:
                continue
            if any(partie in exclus for partie in chemin.parts):
                continue
            try:
                contenu = chemin.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if "get_close_matches" in contenu:
                ecarts.append("COPIE de la regle des noms proches hors de son domicile : "
                              + chemin.relative_to(matrice).as_posix())
    return ecarts


def _eprouver_domicile_noms_proches(racine):
    """MAILLON 62 (MO-468 / EO-384) : la regle des noms proches vit a UN SEUL domicile.

    Mesure qui fonde ce maillon : la MEME regle < les noms PROCHES d un nom fautif >
    vivait en DEUX copies qui ne se comportaient PAS pareil -- resolution_outils.py
    (INCLUSION + PROXIMITE, reparee sous MO-367) et pilote/injection/modes_emploi.py
    (la SOUS-CHAINE seule, donc un nom fautif d UNE LETTRE ne proposait RIEN). Deux
    comportements sous un MEME nom de regle (L-029) : le refus du pilote se taisait
    exactement quand l agent en avait besoin. Le round les a reunies dans
    matrice/data/commun/noms_proches.py (M-076).

    Le DETECTEUR est JOUE sur des arbres FABRIQUES avant l arbre REEL : un detecteur
    qu on ne fait pas MORDRE ne prouve rien (regle 4.4).
      - CONTRE-TEMOIN (epargne) : la regle vit SEULE au domicile, les DEUX
        consommateurs la consomment -> AUCUN ecart ;
      - COBAYE (mord) : une copie repousse dans l arbre de la MATRICE, puis dans celui
        du PILOTE -> accusee, et le fichier fautif est NOMME ;
      - COBAYE DU BRANCHEMENT (mord) : un consommateur cesse de consommer -> accuse ;
      - LA REGLE EN EXECUTION (listes fabriquees, aucun parc touche) : une lettre
        oubliee est PROPOSEE ; un nom VIDE et un nom ETRANGER ne font naitre AUCUNE
        proposition (un refus qui inventerait un proche serait pire qu un refus muet) ;
      - LES DEUX CONSOMMATEURS, CHARGES ET COMPARES au domicile : l objet de regle qu
        ils emploient doit etre CELUI du domicile, et chacun doit PROPOSER sur une
        lettre oubliee de SON parc ;
      - l ARBRE REEL doit etre sain.
    """
    import importlib.util

    racine = Path(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    matrice = matrice.resolve()
    donnees = matrice / "matrice" / "data"
    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    regle = ("import difflib" + chr(10) + chr(10) + chr(10)
             + "def proches(nom, noms):" + chr(10)
             + "    return difflib.get_close_matches(nom, noms)" + chr(10))
    consommateur = ("from noms_proches import proches" + chr(10) + chr(10) + chr(10)
                    + "def refus(nom):" + chr(10)
                    + "    return proches(nom, [])" + chr(10))
    domicile_relatif = Path("matrice") / "data" / "commun" / "noms_proches.py"
    consommateurs_relatifs = (
        Path("matrice") / "data" / "commun" / "resolution_outils.py",
        Path("_operateur") / "optimus-prime" / "pilote" / "injection" / "modes_emploi.py",
    )

    with tempfile.TemporaryDirectory(prefix="cobaye-noms-proches-") as temporaire:
        faux = Path(temporaire).resolve()
        (faux / domicile_relatif).parent.mkdir(parents=True)
        (faux / domicile_relatif).write_text(regle, encoding="utf-8")
        for relatif in consommateurs_relatifs:
            (faux / relatif).parent.mkdir(parents=True, exist_ok=True)
            (faux / relatif).write_text(consommateur, encoding="utf-8")

        # CONTRE-TEMOIN : la regle vit SEULE au domicile -> RIEN a accuser.
        propres = _detecter_copies_noms_proches(faux)
        ep("contre-temoin-l-arbre-propre-n-est-PAS-accuse", propres == [],
           "la regle au seul domicile a ete accusee : " + str(propres)[:160])

        # COBAYE 1 : une SECONDE copie repousse dans l arbre de la MATRICE -> elle MORD.
        copie = faux / "matrice" / "data" / "outils" / "un" / "fonctions.py"
        copie.parent.mkdir(parents=True)
        copie.write_text(regle, encoding="utf-8")
        morsure = _detecter_copies_noms_proches(faux)
        ep("le-cobaye-une-copie-DECLENCHE-l-accusation", len(morsure) == 1,
           "une copie de la regle n a pas ete accusee : " + str(morsure)[:160])
        ep("l-accusation-NOMME-le-fichier-fautif",
           bool(morsure) and all("fonctions.py" in ecart for ecart in morsure),
           "l ecart n a pas nomme le fichier fautif : " + str(morsure)[:160])
        copie.unlink()

        # COBAYE 2 (le cote du PILOTE, celui qui DIVERGEAIT) : la meme copie repousse
        # sous l arbre de l operateur -> meme accusation.
        copie_pilote = (faux / "_operateur" / "optimus-prime" / "pilote" / "injection"
                        / "copie-de-la-regle.py")
        copie_pilote.write_text(regle, encoding="utf-8")
        morsure_pilote = _detecter_copies_noms_proches(faux)
        ep("le-cobaye-du-cote-PILOTE-est-accuse-lui-aussi",
           len(morsure_pilote) == 1 and "copie-de-la-regle.py" in morsure_pilote[0],
           "la copie cote pilote n a pas ete accusee : " + str(morsure_pilote)[:160])
        copie_pilote.unlink()

        # COBAYE 3 : un consommateur CESSE de consommer -> la regle partagee
        # redeviendrait une regle morte, et la copie reviendrait.
        consommateur_pilote = faux / consommateurs_relatifs[1]
        consommateur_pilote.write_text("def refus(nom):" + chr(10) + "    return []" + chr(10),
                                       encoding="utf-8")
        morsure_branchement = _detecter_copies_noms_proches(faux)
        ep("le-cobaye-un-consommateur-qui-ne-consomme-plus-est-ACCUSE",
           any("ne CONSOMME plus" in ecart for ecart in morsure_branchement),
           "un consommateur muet n a pas ete accuse : " + str(morsure_branchement)[:160])

    # L ARBRE REEL : la regle vit a UN SEUL domicile, consommee par les DEUX.
    reels = _detecter_copies_noms_proches(matrice)
    ep("l-arbre-reel-n-a-AUCUNE-copie", reels == [], "; ".join(reels[:6]))

    # LA REGLE ELLE-MEME, EN EXECUTION : elle est chargee par SON chemin (la meme
    # source que les deux consommateurs), puis jouee sur des listes FABRIQUEES.
    domicile = donnees / "commun" / "noms_proches.py"
    if str(donnees / "commun") not in sys.path:
        sys.path.insert(0, str(donnees / "commun"))
    try:
        specification = importlib.util.spec_from_file_location("noms_proches", str(domicile))
        maison = importlib.util.module_from_spec(specification)
        sys.modules["noms_proches"] = maison
        specification.loader.exec_module(maison)
    except (ImportError, OSError, SyntaxError) as erreur:
        ep("le-DOMICILE-est-chargeable", False,
           type(erreur).__name__ + " : " + str(erreur)[:120])
        return ecarts
    parc = ["suivi-optimus", "garde-flux2", "bdd-lecons", "ecrire"]
    propose = maison.proches("suivi-optimu", parc)
    ep("la-regle-PROPOSE-sur-une-lettre-oubliee", propose == ["suivi-optimus"],
       "une lettre oubliee n a pas ete proposee : " + str(propose))
    ep("CONTRE-TEMOIN-un-nom-VIDE-ne-propose-RIEN", maison.proches("", parc) == [],
       "un nom vide a propose quelque chose : " + str(maison.proches("", parc)))
    vide = maison.proches("zzz-rien-a-voir", parc)
    ep("CONTRE-TEMOIN-un-nom-ETRANGER-ne-fait-naissance-a-AUCUN-proche", vide == [],
       "le refus a DEVINE un proche : " + str(vide))

    # LES DEUX CONSOMMATEURS, EXECUTES ET COMPARES AU DOMICILE : un consommateur qui
    # garderait sa PROPRE copie rendrait un AUTRE objet -- deux comportements sous un
    # meme nom de regle, exactement ce que ce maillon refuse.
    consommateurs = (
        (Path("matrice") / "data" / "commun" / "resolution_outils.py", "la Matrice",
         "noms_connus"),
        (Path("_operateur") / "optimus-prime" / "pilote" / "injection" / "modes_emploi.py",
         "le pilote", "noms_servables"),
    )
    for relatif, qui, nom_du_parc in consommateurs:
        chemin = matrice / relatif
        try:
            specification = importlib.util.spec_from_file_location(
                "consommateur_" + relatif.stem.replace("-", "_"), str(chemin))
            module = importlib.util.module_from_spec(specification)
            specification.loader.exec_module(module)
        except (ImportError, OSError, SyntaxError, AttributeError, NameError) as erreur:
            ep("le-consommateur-" + qui + "-est-EXECUTABLE", False,
               type(erreur).__name__ + " : " + str(erreur)[:120])
            continue
        ep(qui + " : la regle consommee EST celle du domicile",
           getattr(module, "proches", None) is maison.proches,
           qui + " n emploie pas l OBJET du domicile (copie, ou nom absent)")
        parc_reel = list(getattr(module, nom_du_parc)())
        ep(qui + " : un nom fautif d UNE LETTRE est PROPOSE",
           _une_lettre_oubliee_est_proposee(module, parc_reel),
           qui + " ne propose RIEN sur une lettre oubliee (le defaut de MO-468 est revenu)")

    return ecarts


def _eprouver_domicile_ascii(racine):

    """MAILLON 60 (MO-466 / EO-365) : la regle ASCII vit a UN SEUL domicile.

    Mesure qui fonde ce maillon : la MEME regle (NFKD, puis encodage ASCII avec
    `errors=ignore`) vivait en DEUX copies recopiees -- assainir_ascii
    (bdd-sessions/ajouter) et vers_ascii (suivi-optimus/vue) -- PLUS une 3e non
    declaree (chaine-pense-bete, titre_vers_slug). Deux copies d une meme regle
    divergent en silence : le jour ou l une apprend un cas, l autre l ignore
    (L-029). Le round les a reunies dans data/commun/texte_ascii.py (M-076).

    Le DETECTEUR est JOUE sur des arbres FABRIQUES avant l arbre reel : un
    detecteur qu on ne fait pas MORDRE ne prouve rien (4.4).
      - CONTRE-TEMOIN (epargne) : la regle vit SEULE au domicile -> 0 ecart ;
      - COBAYE (mord) : le MEME arbre + une copie -> accuse, et il NOMME le
        fichier fautif ;
      - l ARBRE REEL doit etre sain : aucune copie hors du domicile.
    """
    racine = Path(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    donnees = matrice / "matrice" / "data"
    if not donnees.is_dir():
        return ["data/ INTROUVABLE : " + str(donnees)]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    regle = ("import unicodedata\n\n\ndef vers_ascii(texte):\n"
             "    return unicodedata.normalize(\"NFKD\", str(texte))\n")

    with tempfile.TemporaryDirectory(prefix="cobaye-ascii-") as temporaire:
        faux = Path(temporaire)
        (faux / "commun").mkdir(parents=True)
        (faux / "outils" / "un").mkdir(parents=True)
        (faux / "commun" / "texte_ascii.py").write_text(regle, encoding="utf-8")
        voisin = faux / "outils" / "un" / "fonctions.py"
        voisin.write_text("def rien(texte):\n    return texte\n", encoding="utf-8")

        # CONTRE-TEMOIN : la regle vit SEULE au domicile -> RIEN a accuser.
        propres = _detecter_copies_ascii(faux)
        ep("contre-temoin-l-arbre-propre-n-est-PAS-accuse", propres == [],
           "la regle au seul domicile a ete accusee : " + str(propres)[:160])

        # COBAYE : une SECONDE copie de la regle apparait -> le detecteur MORD.
        voisin.write_text(regle, encoding="utf-8")
        morsure = _detecter_copies_ascii(faux)
        ep("le-cobaye-une-copie-DECLENCHE-l-accusation", len(morsure) == 1,
           "une copie de la regle n a pas ete accusee : " + str(morsure)[:160])
        ep("l-accusation-NOMME-le-fichier-fautif",
           any("fonctions.py" in ecart for ecart in morsure),
           "l ecart n a pas nomme le fichier fautif : " + str(morsure)[:160])

    # L ARBRE REEL : la regle doit vivre a UN SEUL domicile.
    reels = _detecter_copies_ascii(donnees)
    ep("l-arbre-reel-n-a-AUCUNE-copie", reels == [], "; ".join(reels[:6]))

    return ecarts


def _verifier_demande_segment(texte_constantes, texte_commun, texte_fin, texte_entry,
                              texte_enregistrer, texte_loi):
    """Ecarts du CABLAGE de la DEMANDE DE SEGMENT (MO-500 / EO-478). PURE.

    POURQUOI CE MAILLON MESURE LE BRANCHEMENT, ET PAS SEULEMENT L OUTIL : le sujet
    entier de l audit MO-499 etait un BRANCHEMENT MANQUANT. L outil, la BDD et la
    source declaree au moteur existaient, les maillons 53 et 54 les verifiaient, et
    AUCUN chemin de round ne les appelait : les deux BDD restaient au segment
    FONDATEUR. Un maillon qui se contenterait de constater que l outil est la
    repeterait exactement l angle mort qu il est ecrit pour fermer (L-060 : un
    livrable que son seul temoin appelle est un livrable non prouve).
    """
    ecarts = []
    for nom in ("CHEMIN_OUTIL_RAISONNEMENT", "CHEMIN_BDD_RAISONNEMENT", "OPTION_SEGMENT",
                "CHAMPS_SEGMENT", "CHAMPS_SEGMENT_REQUIS", "VERBE_SEGMENT"):
        if nom not in texte_constantes:
            ecarts.append("la constante " + nom + " n est PAS declaree au pilote")
    for nom in ("def lire_segments(", "def lire_bdd_raisonnement(",
                "def juger_raisonnement(", "def deposer_segments_raisonnement(",
                "def controler_raisonnement_mission("):
        if nom not in texte_commun:
            ecarts.append("le pilote ne declare pas " + nom)
    if "deposer_segments_raisonnement(mission, segments)" not in texte_fin:
        ecarts.append("la cloture ne DEPOSE pas le segment (le branchement manquant de"
                      " MO-499 est revenu)")
    if "controler_raisonnement_mission(mission)" not in texte_fin:
        ecarts.append("la cloture ne MESURE pas le depot (le silence redevient possible)")
    if "lire_segments(" not in texte_entry or "OPTION_SEGMENT" not in texte_entry:
        ecarts.append("la porte `fin` n ouvre pas l option du segment")
    if "deposer_segments_raisonnement(" not in texte_enregistrer:
        ecarts.append("la DEUXIEME cloture (`enregistrer`) ne repond pas du meme geste")
    if "SEGMENT DE RAISONNEMENT EST DEMANDE A LA CLOTURE" not in texte_loi:
        ecarts.append("la LOI DU ROUND ne porte pas la demande (proto-12, geste 4.7)")
    # LA FORME DES CHAMPS EST UN CONTRAT, PAS UNE COERCITION (MO-502) : la loi dit les
    # champs FERMES mais PAS leur FORME, et la cloture transporte le segment en LIGNE
    # DE COMMANDE (--tags "a,b"). Mesure : RS-004 (source MO-468) a recu une LISTE
    # JSON, transportee telle quelle, decoupee sur ses virgules et ABIMEE en silence
    # dans la BDD. Une loi qui ne dit pas la forme laisse l agent la deviner.
    if "jamais une liste JSON" not in texte_loi:
        ecarts.append("la LOI DU ROUND ne DIT pas la FORME du champ `tags` (une CHAINE"
                      " separee par des virgules, jamais une liste JSON) -- un tags en"
                      " liste arrivait decoupee et ABIME en silence (mesure : RS-004)")

    # Le NOM du bilan suit le CANON de la zone jetable (reprise MO-500) : la loi
    # proposait un nom LIBRE (bilan-moXXX.txt), que le garde de zone accuse RESIDU --
    # une commande copiee de la loi fabriquait donc un ecart, et la zone doit etre vide
    # a la cloture. Le canon se DEMANDE a sa porte (fichiers-travail nommer).
    if "tmp-optimus/mo-XXX-bilan.txt" not in texte_loi:
        ecarts.append("la LOI DU ROUND ne nomme pas le bilan par le CANON de la zone"
                      " jetable (fichiers-travail nommer : mo-XXX-bilan.txt) -- un nom"
                      " libre y est accuse RESIDU par le garde de zone")
    return ecarts


def _lire_si_present(chemin):
    """Le TEXTE du fichier, ou une chaine vide s il est absent (jamais d exception)."""
    return chemin.read_text(encoding="utf-8") if chemin.is_file() else ""


def _lire_fichiers_moule(moule):
    """Les fichiers du moule qui portent les verbes, par chemin RELATIF (texte ou None).

    Les DEUX categories sont lues, pas seulement `corriger` : un controle
    qui n a pas lu un fichier ne peut pas dire qu il lui manque -- il
    crierait a tort sur une categorie qu il n a jamais regardee (EO-537).
    """
    fichiers = {}
    for relatif in ("main.py.moule", "corriger/entry.py.moule",
                    "corriger/fonctions.py.moule",
                    "retirer/entry.py.moule",
                    "retirer/fonctions.py.moule"):
        chemin = moule / relatif
        fichiers[relatif] = chemin.read_text(encoding="utf-8") if chemin.is_file() else None
    return fichiers


def _verifier_verbe_correction(routeur, facade, fiche, fichiers_moule):
    """Le verbe `corriger` est-il DECLARE partout ou il doit l etre (MO-503) ?

    PURE : elle prend des TEXTES, jamais un chemin -- donc elle s eprouve sur des
    textes FABRIQUES (cobayes) comme sur les textes reels. Quatre faits : l outil le
    DECLARE (son routeur), sa FACADE le dit, la fiche du MANUEL le dit, et le MOULE --
    domicile de tout outil BDD -- le PORTE EN JETONS (une valeur du clone recopiee
    dans le moule est une divergence qui attend ; M-076 : un moteur se partage, il ne
    se recopie pas).
    """
    ecarts = []
    if '"corriger"' not in routeur:
        ecarts.append("le VERBE `corriger` n est plus DECLARE par le routeur de l outil"
                      " de raisonnement -- un tag abime n aurait plus de porte pour"
                      " etre remis d aplomb (mesure : RS-004 / MO-502)")
    if "corriger --id" not in facade:
        ecarts.append("le verbe `corriger` n est plus DECRIT par la facade de l outil"
                      " (DESCRIPTION.md) : un verbe que sa facade tait est un verbe que"
                      " personne ne trouvera")
    if "corriger --id RS-" not in fiche:
        ecarts.append("le verbe `corriger` n est plus DECRIT par la fiche du manuel"
                      " (bdd-raisonnement) : la facade de l outil n est pas la seule a"
                      " devoir le dire")
    if '"corriger"' not in (fichiers_moule.get("main.py.moule") or ""):
        ecarts.append("le routeur du MOULE ne DECLARE pas `corriger` : un clone regenere"
                      " serait livre SANS la porte de correction (M-076 : le clone de"
                      " demain nait du moule, pas du clone d aujourd hui)")
    for relatif in ("corriger/entry.py.moule", "corriger/fonctions.py.moule"):
        texte_moule = fichiers_moule.get(relatif)
        if texte_moule is None:
            ecarts.append("le MOULE ne porte PAS " + relatif + " : le verbe ne vit que"
                          " dans le CLONE -- l outil regenere demain naitrait sans la"
                          " porte de correction")
            continue
        if "__CLE_LISTE__" not in texte_moule:
            ecarts.append("le moule " + relatif + " ne parle PAS en JETONS"
                          " (__CLE_LISTE__ absent) : la valeur du clone a ete RECOPIEE"
                          " dans le moule (M-076)")
        if '"segments"' in texte_moule:
            ecarts.append("le moule " + relatif + " porte le vocabulaire du CLONE"
                          " (segments en dur) : une divergence qui attend")
    return ecarts


def _eprouver_verbe_correction():
    """COBAYES et CONTRE-TEMOIN du controle ci-dessus, sur des textes FABRIQUES.

    Un controle qu on n a jamais vu MORDRE ne garde rien : chaque fait prive de sa
    marque a tour de role doit etre ACCUSE, et un jeu COMPLET doit rester MUET.
    """
    routeur_juste = '"ajouter": a, "corriger": c, "lire": l, "verifier": v'
    facade_juste = 'lancer.py bdd-raisonnement corriger --id RS-XXX --tags "a,b"'
    fiche_juste = '| `corriger` | `<outil>/main.py corriger --id RS-XXX` |'
    fichiers_justes = {"main.py.moule": '"corriger": c',
                       "corriger/entry.py.moule": 'donnees.get("__CLE_LISTE__", [])',
                       "corriger/fonctions.py.moule": 'donnees.get("__CLE_LISTE__", [])'}
    jeux = (
        ("le routeur de l outil ne DECLARE plus le verbe",
         ('"ajouter": a, "lire": l, "verifier": v', facade_juste, fiche_juste, fichiers_justes), True),
        ("la facade de l outil ne DIT plus le verbe",
         (routeur_juste, "lancer.py bdd-raisonnement lire [--tag X]", fiche_juste,
          fichiers_justes), True),
        ("la fiche du manuel ne DIT plus le verbe",
         (routeur_juste, facade_juste, "| `lire` | `<outil>/main.py lire` |",
          fichiers_justes), True),
        ("le MOULE ne DECLARE plus le verbe",
         (routeur_juste, facade_juste, fiche_juste,
          {"main.py.moule": '"ajouter": a, "lire": l, "verifier": v'}), True),
        ("le MOULE n a plus la categorie corriger",
         (routeur_juste, facade_juste, fiche_juste,
          {"main.py.moule": routeur_juste,
           "corriger/entry.py.moule": 'donnees.get("__CLE_LISTE__", [])'}), True),
        ("le MOULE parle le vocabulaire du CLONE",
         (routeur_juste, facade_juste, fiche_juste,
          dict(fichiers_justes,
               **{"corriger/fonctions.py.moule": 'donnees.get("segments", [])'})), True),
        ("CONTRE-TEMOIN -- les trois textes et le moule en jetons",
         (routeur_juste, facade_juste, fiche_juste, fichiers_justes), False),
    )
    ecarts = []
    for nom, arguments, doit_mordre in jeux:
        ecarts_jeu = _verifier_verbe_correction(*arguments)
        if doit_mordre and not ecarts_jeu:
            ecarts.append("cobaye NON MORDANT (" + nom + ") : le controle n a rien"
                          " accuse alors que le fait manquait")
        if not doit_mordre and ecarts_jeu:
            ecarts.append("contre-temoin ACCUSE A TORT (" + nom + ") : "
                          + str(ecarts_jeu)[:160])
    return ecarts


def _charger_module(chemin, nom):
    specification = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def _trouver_entree(entrees, identifiant):
    """L entree qui porte CET identifiant (comparaison EXACTE, jamais un proche)."""
    for entree in entrees:
        if entree.get("id") == identifiant:
            return entree
    return None


def _doublons_actifs(entrees, champ="segment"):
    """Les couples (segment, source) portes par PLUSIEURS entrees actives.

    PURE : elle prend la LISTE des entrees, jamais un chemin -- donc le cobaye
    peut la priver de chaque fait a tour de role, et le contre-temoin doit rester
    muet. Un controle qu on n a jamais vu mordre ne garde rien (lecon L-029).
    """
    ecarts = []
    vues = {}
    for entree in entrees:
        cle = (str(entree.get(champ, "")), str(entree.get("source", "")))
        vues.setdefault(cle, []).append(str(entree.get("id", "?")))
    for (texte, source), ids in sorted(vues.items()):
        if len(ids) > 1:
            ecarts.append("DOUBLON actif : " + ", ".join(sorted(ids))
                          + " portent le meme contenu pour la source "
                          + repr(source) + " -- un raisonnement lu deux fois comme"
                            " s il en etait deux, et le compteur gonfle d autant")
    return ecarts


def _juger_retraits(donnees):
    """Les retraits sont-ils TRACANTS ? Un retrait sans temoin est un effacement.

    PURE : elle prend le DICTIONNAIRE de la BDD, jamais un chemin.
    """
    ecarts = []
    retraits = donnees.get("retraits") or []
    if not isinstance(retraits, list):
        return ["le champ `retraits` n est pas une liste : " + type(retraits).__name__]
    for numero, temoin in enumerate(retraits, start=1):
        if not isinstance(temoin, dict):
            ecarts.append("retrait " + str(numero) + " n est pas un objet : "
                          + type(temoin).__name__)
            continue
        if not temoin.get("date"):
            ecarts.append("retrait " + str(numero) + " ("
                          + str(temoin.get("entree", {}).get("id", "?"))
                          + ") ne porte pas sa date : on ne sa pas quand il a eu lieu")
        entree = temoin.get("entree")
        if not isinstance(entree, dict) or not entree.get("id"):
            ecarts.append("retrait " + str(numero)
                          + " ne porte pas l entree ENTIERE : un retrait dont le"
                            " temoin est ampute n est pas reversible")
            continue
        for champ in ("segment", "tags", "source"):
            if champ not in entree:
                ecarts.append("le temoin du retrait de " + str(entree.get("id"))
                              + " ne porte pas le champ " + champ
                              + " : le retrait n est reversible qu en apparence")
    return ecarts


def _eprouver_jugement_doublon():
    """COBAYES et CONTRE-TEMOIN de `_doublons_actifs` et `_juger_retraits`."""
    ecarts = []

    def controler(nom, condition, detail="", fait=""):
        # On n accumule QUE les anomalies : un verdict vrai ne se range pas
        # dans une liste d ecarts (sinon le rendu `"[KO] " + ecart` plante).
        print("  [" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
        if fait and not condition:
            ecarts.append("jugement du doublon -- " + nom + " : " + fait)

    doublons = [
        ("le doublon actif est ACCUSE (le cas mesure du round)",
         [{"id": "RS-033", "segment": "X", "source": "MO-508"},
          {"id": "RS-038", "segment": "X", "source": "MO-508"}], True),
        ("CONTRE-TEMOIN : deux segments de MEME TEXTE, sources DIFFERENTES -> rien",
         [{"id": "RS-033", "segment": "X", "source": "MO-508"},
          {"id": "RS-034", "segment": "X", "source": "MO-509"}], False),
        ("CONTRE-TEMOIN : des textes differents, meme source -> rien",
         [{"id": "RS-033", "segment": "X", "source": "MO-508"},
          {"id": "RS-034", "segment": "Y", "source": "MO-508"}], False),
        ("CONTRE-TEMOIN : une liste vide -> rien", [], False),
    ]
    for nom, entrees, doit_mordre in doublons:
        ecarts_jeu = _doublons_actifs(entrees)
        controler(nom, (bool(ecarts_jeu) == doit_mordre)
                  and (not doit_mordre or "RS-033" in " ".join(ecarts_jeu)),
                  str(len(ecarts_jeu)) + " ecart(s)",
                  "le doublon attendu n a pas ete accuse, ou accuse a tort")

    retraits = [
        ("un retrait SANS date est ACCUSE",
         {"retraits": [{"motif": "x", "entree": {"id": "RS-1", "segment": "s",
                                                 "tags": [], "source": "m"}}]}, True),
        ("un temoin AMPUTE (pas d entree entiere) est ACCUSE",
         {"retraits": [{"date": "2026-09-30 10:00:00", "entree": {"id": "RS-1"}}]}, True),
        ("CONTRE-TEMOIN : un temoin COMPLET ne dit rien",
         {"retraits": [{"date": "2026-09-30 10:00:00", "motif": "m",
                        "entree": {"id": "RS-1", "segment": "s", "tags": ["a"],
                                   "source": "MO-508", "date": "2026-09-30 09:00:00"}}]},
         False),
        ("CONTRE-TEMOIN : le champ ABSENT ne dit rien", {}, False),
    ]
    for nom, donnees, doit_mordre in retraits:
        ecarts_jeu = _juger_retraits(donnees)
        controler(nom, bool(ecarts_jeu) == doit_mordre,
                  str(len(ecarts_jeu)) + " ecart(s)",
                  "le retrait attendu n a pas ete juge, ou juge a tort")
    return ecarts


def _verifier_verbe_retirer(routeur, facade, manuel, fichiers_moule):
    """Le verbe `retirer` est-il DECLARE partout, et parle-t-on en jetons ?

    Meme discipline que le controle de `corriger` : quatre faits, et le MOULE
    parle en JETONS (`__CLE_LISTE__`) -- une valeur du clone recopiee dans le
    moule est une divergence qui attend.
    """
    ecarts = []
    if '"retirer"' not in routeur:
        ecarts.append("le VERBE `retirer` n est plus DECLARE par le routeur de l"
                      " outil de raisonnement : une entree fautive n aurait plus de"
                      " porte pour disparaitre")
    if "retirer --id" not in facade:
        ecarts.append("le verbe `retirer` n est plus DECRIT par la facade de l outil")
    if "retirer --id RS-" not in manuel:
        ecarts.append("le verbe `retirer` n est plus DECRIT par la fiche du manuel")
    if '"retirer"' not in (fichiers_moule.get("main.py.moule") or ""):
        ecarts.append("le routeur du MOULE ne DECLARE pas `retirer` : un clone"
                      " regenere serait livre sans la porte de retrait")
    for relatif in ("retirer/entry.py.moule", "retirer/fonctions.py.moule"):
        texte = fichiers_moule.get(relatif)
        if texte is None:
            ecarts.append("le MOULE ne porte PAS " + relatif + " : le verbe ne vit"
                          " que dans le CLONE -- l outil regenere naitrait sans lui")
            continue
        if "__CLE_LISTE__" not in texte:
            ecarts.append("le moule " + relatif + " ne parle PAS en JETONS"
                          " (__CLE_LISTE__ absent)")
        if '"segments"' in texte:
            ecarts.append("le moule " + relatif + " porte le vocabulaire du CLONE")
    return ecarts


def _eprouver_verbe_retirer():
    """Les sept jeux de la declaration, sur des textes FABRIQUES."""
    routeur = '"ajouter": a, "corriger": c, "lire": l, "retirer": r, "verifier": v'
    facade = 'lancer.py bdd-raisonnement retirer --id RS-XXX [--index N]'
    manuel = '| `retirer` | `<outil>/main.py retirer --id RS-XXX` |'
    joues = {"main.py.moule": '"corriger": c, "retirer": r',
             "retirer/entry.py.moule": 'donnees.get("__CLE_LISTE__", [])',
             "retirer/fonctions.py.moule": 'donnees.get("__CLE_LISTE__", [])'}
    jeux = (
        ("le routeur ne declare plus le verbe",
         ('"ajouter": a, "corriger": c, "lire": l, "verifier": v', facade, manuel,
          joues), True),
        ("la facade ne dit plus le verbe",
         (routeur, "lancer.py bdd-raisonnement lire", manuel, joues), True),
        ("le manuel ne dit plus le verbe",
         (routeur, facade, "| `lire` | x |", joues), True),
        ("le MOULE ne declare plus le verbe",
         (routeur, facade, manuel, {"main.py.moule": '"corriger": c'}), True),
        ("le MOULE n a plus la categorie retirer",
         (routeur, facade, manuel, dict(joues, **{"retirer/entry.py.moule": None})),
         True),
        ("le MOULE parle le vocabulaire du CLONE",
         (routeur, facade, manuel,
          dict(joues, **{"retirer/fonctions.py.moule": 'donnees.get("segments", [])'})),
         True),
        ("CONTRE-TEMOIN -- tout est declare, en jetons",
         (routeur, facade, manuel, joues), False),
    )
    ecarts = []
    for nom, arguments, doit_mordre in jeux:
        ecarts_jeu = _verifier_verbe_retirer(*arguments)
        if doit_mordre and not ecarts_jeu:
            ecarts.append("cobaye NON MORDANT (" + nom + ") : le controle n a rien"
                          " accuse alors que le fait manquait")
        if not doit_mordre and ecarts_jeu:
            ecarts.append("contre-temoin ACCUSE A TORT (" + nom + ") : "
                          + str(ecarts_jeu)[:160])
    return ecarts


def _rendre_erreur(sortie, limite=2000):
    """Le POURQUOI entier d un echec de clone, jamais un coupe-goutte.

    Un traceback porte sa CAUSE sur sa DERNIERE ligne : tronquer par la TETE
    (`sortie[:120]`) conserve le fichier et le numero de ligne -- l utile a
    rien -- et coupe le message AU MILIEU d un chemin. Mesure EO-537 : le
    lanceur affichait `...raisonnemen; les-DEUX-verbes-JOUES...`, et la cause
    reelle (`racine `matrix` introuvable en remontant`) n est apparue qu en
    rejouant le meme montage HORS du lanceur. Quatre corrections ont suivi,
    dont trois cherchaient un defaut qui n etait pas la.

    On rend donc les lignes ENTIERES depuis la fin, et on DIT quand on coupe.
    PURE : elle prend un texte, jamais un chemin -- donc elle se joue sur des
    chaines fabriquees.
    """
    lignes = sortie.splitlines()
    utiles = [ligne for ligne in lignes if ligne.strip()]
    if not utiles:
        return "(sortie vide)"
    rendues = []
    total = 0
    for ligne in reversed(utiles):
        if rendues and total + len(ligne) > limite:
            break
        rendues.append(ligne)
        total += len(ligne) + 1
    rendues.reverse()
    if len(rendues) < len(utiles):
        rendues.insert(0, "(... " + str(len(utiles) - len(rendues))
                       + " ligne(s) de tete non rendues)")
    return " | ".join(rendues)


def _eprouver_rendu_erreur():
    """COBAYES et CONTRE-TEMOIN de `_rendre_erreur`, sur des textes FABRIQUES.

    Le fait a prouver : une cause au-dela du seuil de l ancien coupe-goutte
    reste VISIBLE, parce que la queue se rend et la tete se dit coupee.
    """
    ecarts = []

    def controler(nom, condition, detail=""):
        print("  [" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
        if not condition:
            ecarts.append("rendu de l erreur -- " + nom + " : " + detail)

    # Les chemins du cobaye sont CONSTRUITS, jamais ecrits en dur : une valeur
    # figee dans un fichier de production est une divergence qui attend
    # (M-076). La longueur, elle, vient du prefixe du dossier temporaire.
    import tempfile
    from pathlib import Path
    racine_cobaye = Path(tempfile.gettempdir()) / ("tmp-" + "0" * 12) / "arbre"
    cause = ("RuntimeError: racine `matrix` introuvable en remontant depuis "
             + str(racine_cobaye / "matrice" / "data" / "commun" / "sac_a_dos.py"))
    traceback_long = "\n".join([
        "Traceback (most recent call last):",
        '  File "' + str(racine_cobaye.parent / "clone-outil" / "main.py")
        + '", line 38, in <module>',
        "    from sac_a_dos import envelopper",
        cause,
    ])
    # COBAYE : la cause est AU-DELA des 140 caracteres du coupe-goutte d hier.
    rendu = _rendre_erreur(traceback_long)
    controler("cobaye -- la cause, au-dela du seuil, reste VISIBLE",
              cause in rendu, "cause absente du rendu")
    # Pour que la coupe ait LIEU, la sortie doit reellement deborder la limite :
    # le traceback court ci-dessus ne demande rien, et un cobaye qui accuse la
    # quand il n a rien a mesurer ne prouve rien (lecon L-029).
    traceback_enorme = "\n".join(
        ["ligne " + str(numero) for numero in range(400)] + [cause])
    rendu_enorme = _rendre_erreur(traceback_enorme)
    controler("cobaye -- sortie debordante : la coupe de tete est DIITE",
              "ligne(s) de tete non rendues" in rendu_enorme,
              "la coupe n est pas annoncee alors que la sortie deborde")
    controler("cobaye -- meme en debordant, la CAUSE de fin survit",
              cause in rendu_enorme, "la cause a ete coupee avec la tete")
    controler("contre-temoin -- le traceback COURT, lui, ne crie pas de coupe",
              "ligne(s) de tete non rendues" not in rendu,
              "coupe annoncee alors que rien n a ete coupe")
    controler("contre-temoin -- un rendu COURT ne crie pas une coupe",
              "non rendues" not in _rendre_erreur("ValueError: rien"),
              "coupe annoncee sur un texte court")
    vide = _rendre_erreur("")
    controler("contre-temoin -- une sortie vide rend une phrase, jamais rien",
              vide == "(sortie vide)", str(vide))
    controler("contre-temoin -- une sortie FAITE de lignes VIDES se dit aussi",
              _rendre_erreur("\n \n") == "(sortie vide)",
              str(_rendre_erreur("\n \n")))
    # CONTRE-TEMOIN -- l'ancien coupe-goutte ECHOUERAIT sur ce cobaye : la preuve
    # que le nouveau rendu fait mieux, sinon le test ne prouverait rien.
    controler("contre-temoin -- l ancien coupe-goutte aurait ECHOUE la",
              cause not in traceback_long[:140],
              "la cause tient dans 140 caracteres : le cobaye ne mordrait pas")
    return ecarts


def _jouer_sur_un_clone(outil, zone_temporaire):
    """Le VERBE joue EN ENFANT sur un clone complet de l outil.

    LE CLONE EST COMPLET, PAS SEULEMENT LE JSON : l outil localise sa BDD par
    `__file__` (constants.py : REPERTOIRE_OUTIL.parent), donc une copie de donnee
    posee a cote ne serait JAMAIS lue et les ecritures partiraient dans le
    service. C est un defaut que mes premieres preuves ont commis.

    Rend (ecarts, faits) : les ecarts nommes, et les faits pour le compte-rendu.
    """
    import json
    import shutil
    import subprocess
    import sys
    from pathlib import Path

    ecarts = []
    faits = []
    # L ARBORESCENCE FICTIVE (motif eprouve par le maillon de la garde) : l outil
    # REFUSE de se charger hors d une racine portant `matrice/data/commun/options.py`
    # ET un `AGENTS.md`. Un clone pose dans un dossier nu meurt sur son propre
    # chargement et ne prouve rien.
    # La RACINE PORTE LE NOM `matrix` : deux gardes du service montent par nom
    # (`sac_a_dos`) ou cherchent `matrice/data/commun` au-dessus d elles
    # (`constants.py`). Une racine nommee autrement refuse de charger l outil.
    arbre = Path(zone_temporaire) / "matrix"
    marqueur = arbre / "AGENTS.md"
    marqueur.parent.mkdir(parents=True, exist_ok=True)
    marqueur.write_text("racine factice du maillon 80\n", encoding="utf-8", newline="\n")
    commun_source = RACINE_MATRICE / "matrice" / "data" / "commun"
    commun_cible = arbre / "matrice" / "data" / "commun"
    commun_cible.parent.mkdir(parents=True, exist_ok=True)
    if not (commun_source / "options.py").is_file():
        return ["le dossier PARTAGE `matrice/data/commun` est introuvable : le clone"
                " ne pourrait pas se charger"], faits
    shutil.copytree(str(commun_source), str(commun_cible))
    dossier = arbre / "_operateur" / "optimus-prime" / "raisonnement" \
        / "bdd-raisonnement"
    if dossier.exists():
        shutil.rmtree(str(dossier))
    dossier.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(str(Path(outil).parent), str(dossier),
                    ignore=shutil.ignore_patterns("__pycache__", "*.bak.*"))
    entree = dossier / "main.py"
    if not entree.is_file():
        return ["le clone n a pas de main.py"], faits
    texte = "COBAYE-MAILLON80 -- un contenu de preuve, depose une seule fois."
    source = "maillon-80"
    autre = "maillon-80-bis"

    def jouer(*arguments):
        resultat = subprocess.run([sys.executable, str(entree)] + [str(a) for a in arguments],
                                 capture_output=True, text=True, cwd=str(dossier),
                                 timeout=120)
        return (resultat.returncode,
                ((resultat.stdout or "") + (resultat.stderr or "")).strip())

    code, sortie = jouer("ajouter", "--segment", texte, "--tags", "cobaye",
                         "--source", source)
    if code != 0:
        return ["le premier depot est REFUSE sur le clone : "
                + _rendre_erreur(sortie)], faits
    faits.append("premier depot accepte")

    code, sortie = jouer("ajouter", "--segment", texte, "--tags", "cobaye",
                         "--source", source)
    if code != 2 or "DOUBLON" not in sortie:
        ecarts.append("le doublon n est pas REFUSE en ENFANT sur le clone (code "
                      + str(code) + ") : " + _rendre_erreur(sortie))
    else:
        faits.append("doublon refuse en nommant l id")

    code, sortie = jouer("ajouter", "--segment", texte, "--tags", "cobaye",
                         "--source", autre)
    if code != 0:
        ecarts.append("le MEME TEXTE sous une AUTRE source est refuse (code "
                      + str(code) + ") : la regle du doublon est trop large -- deux"
                      " missions peuvent produire le meme raisonnement : "
                      + _rendre_erreur(sortie))
    else:
        faits.append("meme texte, autre source : accepte")

    # Le second depot a produit une entrete : on la retire par son id, mesure sur
    # le JSON DU CLONE (jamais celui du service).
    # L outil ecrit SA BDD un niveau au-dessus de lui (REPERTOIRE_OUTIL.parent) :
    # la lire a cote du clone est donc la seule lecture qui voie ses ecritures.
    bdd = dossier.parent / "segments.json"
    if not bdd.is_file():
        return ecarts + ["la BDD du clone est introuvable : le retrait n est pas"
                         " epreuve"], faits
    donnees = json.loads(bdd.read_text(encoding="utf-8"))
    visee = [str(e.get("id")) for e in donnees.get("segments", [])
             if e.get("segment") == texte and str(e.get("source")) == autre]
    if not visee:
        return ecarts + ["l entree du contre-temoin est introuvable dans la BDD"
                         " du clone"], faits
    code, sortie = jouer("retirer", "--id", visee[0], "--motif", "maillon 80")
    if code != 0:
        ecarts.append("le retrait REFUSE sur le clone (code " + str(code) + ") : "
                      + _rendre_erreur(sortie))
        return ecarts, faits
    faits.append("retrait accepte")

    donnees = json.loads(bdd.read_text(encoding="utf-8"))
    temoins = donnees.get("retraits") or []
    if not temoins:
        ecarts.append("le retrait n a laisse AUCUN temoin : c est un effacement"
                      " (lecon L-055)")
    else:
        entree_retiree = temoins[-1].get("entree") or {}
        for champ in ("id", "segment", "tags", "source"):
            if champ not in entree_retiree:
                ecarts.append("le temoin du retrait ne porte pas " + champ
                              + " : le retrait n est pas reversible")
        if str(entree_retiree.get("id")) == visee[0]:
            faits.append("temoin du retrait porte l entree ENTIERE")
        else:
            ecarts.append("le temoin porte " + str(entree_retiree.get("id"))
                          + " au lieu de " + visee[0])
    code, sortie = jouer("verifier")
    if code != 0:
        ecarts.append("verifier n est pas VERT apres les retraits : une ecriture a"
                      " casse l empreinte sans la reposer : "
                      + _rendre_erreur(sortie))
    else:
        faits.append("empreinte reposee a chaque ecriture")
    return ecarts, faits




def _juger_tags_bdd(entrees):
    """La BDD de raisonnement est-elle SAINE et TRACANTE (MO-503) ?

    PURE : elle prend la liste des entrees, jamais un chemin. Deux faits : un tag
    ABIME (le crochet y est la signature d une liste transportee par la cloture,
    mesure du 2026-09-28) et une correction SANS trace des anciens tags (une
    correction qui efface sa trace se lit comme une entree nee juste).
    """
    ecarts = []
    for entree in entrees:
        abimes = [tag for tag in entree.get("tags", [])
                  if "[" in str(tag) or "]" in str(tag)]
        if abimes:
            ecarts.append("tag ABIME (signature d une liste transportee par la cloture)"
                          " dans " + str(entree.get("id")) + " : " + str(abimes)[:120])
        corrections = entree.get("corrections") or []
        if corrections and not all(isinstance(correction, dict)
                                   and "anciens_tags" in correction
                                   for correction in corrections):
            ecarts.append("correction SANS trace des anciens tags dans "
                          + str(entree.get("id")) + " : une correction doit dire ce"
                          " qu elle a remplace")
    return ecarts


def _eprouver_demande_segment(racine):

    """MAILLON 61 (MO-500 / EO-478) : la cloture DEMANDE le segment de raisonnement.

    TROIS epreuves, dans cet ordre :
      1. le CABLAGE est lu dans la SOURCE (`_verifier_demande_segment`) : les DEUX
         clotures demandent, et la loi du round le dit ;
      2. la REGLE est EPROUVEE EN EXECUTION : le pilote est charge PAR SON CHEMIN
         (motif du maillon 46 -- le chemin est retire apres coup, aucun sys.path
         laisse), puis `lire_segments` et `juger_raisonnement` sont joues sur des
         fixtures JETABLES ; le cobaye MORD (la source declaree par l agent est
         REFUSEE, un AUTRE round est ACCUSE, une BDD illisible se DIT) et le
         CONTRE-TEMOIN EPARGNE (le segment de CE round est TROUVE et NOMME) ;
      3. la DONNEE REELLE est mesuree : les constantes POINTENT les vrais fichiers
         (l outil, la BDD), la BDD se lit, et le jugement rend OUI pour la mission
         qui l a deposee, NON pour une mission sans segment -- la mesure porte donc
         sur des faits, pas seulement sur des fixtures.
    """
    import ast
    import importlib.util
    import json
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    operateur = matrice / "_operateur" / "optimus-prime"
    pilote = operateur / "pilote"
    chemins = {
        "constantes": pilote / "constants.py",
        "commun": pilote / "commun.py",
        "fin": pilote / "fin" / "fonctions.py",
        "entry": pilote / "fin" / "entry.py",
        "enregistrer": pilote / "file" / "fonctions.py",
        "loi": operateur / "protocoles" / "proto-12-loi-du-round.md",
        "bdd": operateur / "raisonnement" / "segments.json",
    }
    for etiquette in sorted(chemins):
        if not chemins[etiquette].is_file():
            return ["fichier INTROUVABLE (" + etiquette + ") : " + str(chemins[etiquette])]

    ecarts = _verifier_demande_segment(
        chemins["constantes"].read_text(encoding="utf-8"),
        chemins["commun"].read_text(encoding="utf-8"),
        chemins["fin"].read_text(encoding="utf-8"),
        chemins["entry"].read_text(encoding="utf-8"),
        chemins["enregistrer"].read_text(encoding="utf-8"),
        chemins["loi"].read_text(encoding="utf-8"))

    sys.path.insert(0, str(pilote))
    try:
        specification = importlib.util.spec_from_file_location("commun_segment",
                                                               chemins["commun"])
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["commun.py du pilote ILLISIBLE (" + type(erreur).__name__
                         + " : " + str(erreur)[:60] + ")"]
    finally:
        sys.path.remove(str(pilote))

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    # --- LES CONSTANTES POINTENT LES VRAIS FICHIERS (le cablage, en fait).
    ep("l-outil-declare-EXISTE", _Chemin(str(module.CHEMIN_OUTIL_RAISONNEMENT)).is_file(),
       "CHEMIN_OUTIL_RAISONNEMENT ne pointe aucun main.py : "
       + str(module.CHEMIN_OUTIL_RAISONNEMENT))
    ep("la-BDD-declaree-est-celle-du-depot",
       _Chemin(str(module.CHEMIN_BDD_RAISONNEMENT)).resolve()
       == chemins["bdd"].resolve(),
       "CHEMIN_BDD_RAISONNEMENT ne pointe pas la BDD du depot : "
       + str(module.CHEMIN_BDD_RAISONNEMENT))

    with tempfile.TemporaryDirectory(prefix="cobaye-segment-") as temporaire:
        faux = _Chemin(temporaire)
        # --- lire_segments : le fichier declare, champs FERMES, source INTERDITE.
        code, segments, message = module.lire_segments("")
        ep("un-round-SANS-fichier-ne-declare-AUCUN-segment", code == 0 and segments == [],
           "sans chemin : " + str((code, segments)))
        valide = faux / "valide.jsonl"
        valide.write_text(json.dumps({"segment": "un raisonnement", "tags": "a,b"})
                          + chr(10), encoding="utf-8")
        code, segments, message = module.lire_segments(str(valide))
        ep("un-segment-VALIDE-est-lu", code == 0 and len(segments) == 1
           and segments[0]["tags"] == "a,b",
           "lecture : " + str((code, segments, message))[:160])
        # LA FORME DES CHAMPS EST UN CONTRAT (MO-502) : le cobaye MORD sur la LISTE de
        # tags qui a reellement abime RS-004 (source MO-468) -- la cloture transporte
        # le segment en LIGNE DE COMMANDE, donc une liste y arrive decoupee sur ses
        # virgules. Le CONTRE-TEMOIN EPARGNE juste au-dessus : la chaine a virgules
        # (--tags "a,b") est LUE, et c est la forme que la loi dit desormais.
        liste = faux / "liste.jsonl"
        liste.write_text(json.dumps({"segment": "x", "tags": ["a", "b"]}) + chr(10),
                         encoding="utf-8")
        code, segments, message = module.lire_segments(str(liste))
        ep("un-champ-de-type-INVALIDE-est-REFUSE-et-NOMME",
           code == 2 and "tags" in message and "INVALIDE" in message
           and "virgules" in message,
           "une LISTE de tags est passee : " + str((code, segments, message))[:160])
        avec_source = faux / "source.jsonl"

        avec_source.write_text(json.dumps({"segment": "x", "tags": "a",
                                           "source": "MO-901"}) + chr(10),
                               encoding="utf-8")
        code, segments, message = module.lire_segments(str(avec_source))
        ep("la-SOURCE-declaree-par-l-agent-est-REFUSEE", code == 2 and "source" in message,
           "la source de l agent est passee : " + str((code, message))[:160])
        vide = faux / "vide.jsonl"
        vide.write_text(json.dumps({"segment": "x", "tags": ""}) + chr(10),
                        encoding="utf-8")
        code, segments, message = module.lire_segments(str(vide))
        ep("un-champ-REQUIS-vide-est-REFUSE", code == 2 and "tags" in message,
           "un champ requis vide est passe : " + str((code, message))[:160])
        faux_json = faux / "faux.jsonl"
        faux_json.write_text("pas du json" + chr(10), encoding="utf-8")
        code, segments, message = module.lire_segments(str(faux_json))
        ep("une-ligne-non-JSON-est-REFUSEE", code == 2,
           "ligne invalide acceptee : " + str(code))

        # --- le CHEMIN est RESOLU comme celui du bilan (MO-364 ; reprise MO-500) : le
        # raccourci que la LOI DU ROUND ecrit en 4.7 (tmp-optimus/...) doit marcher
        # TEL QUEL, et un chemin introuvable NOMME les trois candidats au lieu de
        # rendre un OSError brut -- la commande copiee de la loi ne doit pas echouer.
        candidats = module.resoudre_chemin_bilan("tmp-optimus/x.jsonl")
        ep("le-raccourci-de-la-ZONE-JETABLE-est-RESOLU",
           len(candidats) == 3
           and _Chemin(str(candidats[2])).parent == _Chemin(str(module.REPERTOIRE_ZONE_TMP)),
           "le raccourci ne tombe pas dans la zone jetable : "
           + str([str(candidat) for candidat in candidats]))
        code, segments, message = module.lire_segments("tmp-optimus/inexistant-xyz.jsonl")
        ep("un-chemin-INTROUVABLE-nomme-les-TROIS-candidats",
           code == 2 and "INTROUVABLE" in message and "inexistant-xyz" in message,
           "le refus ne nomme pas le chemin : " + str((code, message))[:160])

        # --- la MESURE : le contre-temoin EPARGNE, le cobaye MORD.
        fabriquee = {"segments": [{"id": "RS-901", "source": "MO-901",
                                   "segment": "s", "tags": ["a"]}]}
        code, message = module.juger_raisonnement(fabriquee, "MO-901")
        ep("contre-temoin-le-segment-de-CE-round-est-TROUVE-et-NOMME",
           code == 0 and "RS-901" in message, "jugement : " + str((code, message))[:160])
        code, message = module.juger_raisonnement(fabriquee, "MO-902")
        ep("cobaye-un-round-SANS-segment-est-ACCUSE", code == 1 and "NON" in message,
           "un round sans segment n a pas ete accuse : " + str((code, message))[:160])
        code, message = module.juger_raisonnement(fabriquee, "M-901")
        ep("la-famille-M-ne-vaut-PAS-pour-MO", code == 1,
           "la famille M- a ete confondue avec MO- : " + str(code))
        code, message = module.juger_raisonnement(None, "MO-901")
        ep("une-BDD-ILLISIBLE-se-DIT-au-lieu-de-se-TAIRE",
           code == 1 and "ILLISIBLE" in message,
           "l aveuglement n a pas ete dit : " + str((code, message))[:160])
        code, message = module.juger_raisonnement({"segments": []}, "MO-901")
        ep("une-BDD-vide-DIT-son-compte", code == 1 and "0 segment" in message,
           "le compte ne se lit pas : " + str((code, message))[:160])

    # --- LA CORRECTION DES TAGS (MO-503) : le manque mesure par MO-502 etait un VERBE
    # ABSENT -- sans lui, les tags abimes de RS-004 ne pouvaient pas etre remis d aplomb
    # autrement que par une ecriture DIRECTE, interdite dans cette BDD (elle a son
    # empreinte et ses refus, L-016). Quatre mesures, du plus faible au plus fort :
    #   1. STATIQUE : le verbe est DECLARE par l outil (routeur ET facade) et DECRIT par
    #      la fiche 41 du manuel -- un verbe que sa facade ne dit pas est un verbe que
    #      personne ne trouvera ;
    #   2. MOULE : l outil est GENERE depuis `templates/outil-bdd` -- le verbe doit vivre
    #      dans le MOULE aussi, sinon le clone de demain nait SANS la porte (M-076 : un
    #      moteur se partage, il ne se recopie pas), et ses fichiers de categorie parlent
    #      en JETONS (jamais le vocabulaire du clone, qui trahirait une recopie) ;
    #   3. DONNEE : la BDD REELLE ne porte AUCUN tag abime (un crochet dans un tag est la
    #      signature d une liste qui a traverse la cloture, mesure du 2026-09-28), et
    #      toute entree CORRIGEE TRACE ses anciens tags -- une correction qui efface sa
    #      trace se lirait comme une entree nee juste ;
    #   4. EXECUTION : le verbe est BRANCHE -- joue en SUBPROCESS sur son chemin, il
    #      REFUSE un id inconnu (code 2) SANS RIEN ECRIRE : un refus est donc jouable sur
    #      la BDD reelle (un garde n ecrit jamais dans le service, L-053).
    # --- LA CORRECTION DES TAGS (MO-503) : le manque mesure par MO-502 etait un VERBE
    # ABSENT -- sans lui, les tags abimes de RS-004 ne pouvaient pas etre remis d aplomb
    # autrement que par une ecriture DIRECTE, interdite dans cette BDD (elle a son
    # empreinte et ses refus, L-016). Quatre mesures, du plus faible au plus fort :
    #   1. STATIQUE : le verbe est DECLARE par l outil (routeur ET facade) et DECRIT par
    #      la fiche du manuel -- un verbe que sa facade tait est un verbe que personne
    #      ne trouvera ;
    #   2. MOULE : l outil est GENERE depuis `matrice/templates/outil-bdd` -- le verbe
    #      doit vivre dans le MOULE aussi, sinon le clone de demain nait SANS la porte
    #      (M-076 : un moteur se partage, il ne se recopie pas), et ses fichiers de
    #      categorie parlent en JETONS (jamais le vocabulaire du clone, qui trahirait
    #      une recopie) ;
    #   3. DONNEE : la BDD REELLE ne porte AUCUN tag abime (un crochet dans un tag est la
    #      signature d une liste qui a traverse la cloture, mesure du 2026-09-28), et
    #      toute entree CORRIGEE TRACE ses anciens tags -- une correction qui efface sa
    #      trace se lirait comme une entree nee juste ;
    #   4. EXECUTION : le verbe est BRANCHE -- joue en SUBPROCESS sur son chemin, il
    #      REFUSE un id inconnu (code 2) SANS RIEN ECRIRE : un refus est donc jouable sur
    #      la BDD reelle (un garde n ecrit jamais dans le service, L-053).
    # Les deux controles STATIQUE et DONNEE sont des FONCTIONS PURES (elles prennent des
    # textes et des entrees, jamais un chemin) : les cobayes les privent de chaque fait
    # a tour de role et le contre-temoin doit rester MUET -- un controle qu on n a jamais
    # vu mordre ne garde rien (lecon L-029).
    outil_raisonnement = operateur / "raisonnement" / "bdd-raisonnement" / "main.py"
    facade_outil = outil_raisonnement.parent / "DESCRIPTION.md"
    fiche_manuel = matrice / "matrice" / "data" / "manuel-outils.md"
    moule_raisonnement = matrice / "matrice" / "templates" / "outil-bdd"
    for chemin_attendu in (outil_raisonnement, facade_outil, fiche_manuel):
        if not chemin_attendu.is_file():
            ecarts.append("fichier INTROUVABLE (le verbe `corriger` n y est donc PAS"
                          " juge) : " + str(chemin_attendu))
    if not moule_raisonnement.is_dir():
        ecarts.append("le MOULE de l outil INTROUVABLE (le clone de demain n a plus de"
                      " domicile) : " + str(moule_raisonnement))
    ecarts += _eprouver_verbe_correction()
    ecarts += _verifier_verbe_correction(_lire_si_present(outil_raisonnement),
                                         _lire_si_present(facade_outil),
                                         _lire_si_present(fiche_manuel),
                                         _lire_fichiers_moule(moule_raisonnement))

    # --- MAILLON 80 (EO-537) : le DOUBLON est refuse, le RETRAIT est trace.
    # Les deux verbes doivent etre DECLARES (routeur, facade, manuel, moule en
    # jetons) ET JOUES : une declaration sans jeu est une porte que personne
    # n utilise, et le jeu se fait sur un clone COMPLET de l outil pose en zone
    # jetable, jamais sur le service.
    import json  # local comme tous les imports de ce lanceur
    ecarts += _eprouver_verbe_retirer()
    ecarts += _eprouver_rendu_erreur()
    ecarts += _verifier_verbe_retirer(_lire_si_present(outil_raisonnement),
                                      _lire_si_present(facade_outil),
                                      _lire_si_present(fiche_manuel),
                                      _lire_fichiers_moule(moule_raisonnement))
    ecarts += _eprouver_jugement_doublon()
    with tempfile.TemporaryDirectory() as zone_jetable:
        ecarts_clone, faits_clone = _jouer_sur_un_clone(outil_raisonnement, zone_jetable)
        ecarts += ecarts_clone
        ep("les-DEUX-verbes-JOUES-sur-un-clone",
           not ecarts_clone,
           (" ; ".join(faits_clone) if faits_clone else "aucun fait joue")
           + (" | ecart(s) : " + " ; ".join(ecarts_clone[:3]) if ecarts_clone else ""))
        # La DONNEE REELLE : pas de doublon actif, et des retraits TRACANTS.
        # La BDD est lue ICI, a sa source : plus loin le maillon 61 la relit pour
        # la coherence du round, donc emprunter sa variable DONNERAIT deux usages
        # a un meme objet (M-076).
        donnees_reelles_du_round = json.loads(
            chemins["bdd"].read_text(encoding="utf-8"))
        segments_du_round = donnees_reelles_du_round.get("segments", [])
        ecarts_donnee = (_doublons_actifs(segments_du_round)
                         + _juger_retraits(donnees_reelles_du_round))
        ep("la-DONNEE-REELLE-est-saine", not ecarts_donnee,
           str(len(segments_du_round)) + " segment(s) actif(s)"
           + (" | ecart(s) : " + " ; ".join(ecarts_donnee[:3]) if ecarts_donnee else ""))
        ecarts += ecarts_donnee

    # --- LA DONNEE REELLE : la BDD du depot, jugee par une fonction PURE.
    donnees_reelles = None
    try:
        donnees_reelles = json.loads(chemins["bdd"].read_text(encoding="utf-8"))
    except (OSError, ValueError) as erreur:
        ecarts.append("la BDD de raisonnement est ILLISIBLE (" + type(erreur).__name__
                      + ") : aucune entree ne peut etre jugee")
    if isinstance(donnees_reelles, dict):
        ecarts += _juger_tags_bdd(donnees_reelles.get("segments", []))
    ep("cobaye-un-tag-ABIME-est-ACCUSE",
       bool(_juger_tags_bdd([{"id": "RS-901", "tags": ["['a'", "'b']"]}])),
       "un tag abime (signature d une liste transportee) n est pas accuse")
    ep("cobaye-une-correction-SANS-trace-est-ACCUSEE",
       bool(_juger_tags_bdd([{"id": "RS-902", "tags": ["a"],
                              "corrections": [{"date": "2026-09-28 21:00:00"}]}])),
       "une correction sans anciens_tags n est pas accusee")
    ep("contre-temoin-une-BDD-SAINE-ne-dit-RIEN",
       _juger_tags_bdd([{"id": "RS-903", "tags": ["a", "b"]},
                        {"id": "RS-904", "tags": ["a"],
                         "corrections": [{"anciens_tags": ["x"]}]}]) == [],
       "une BDD saine a ete accusee")

    # --- L EXECUTION : le refus est JOUE sur la BDD reelle -- il n ecrit rien, donc le
    # garde n ecrit jamais dans le service (L-053).
    resultat_refus = None
    try:
        resultat_refus = lancer_enfant([sys.executable, str(outil_raisonnement),
                                        "corriger", "--id", "RS-999999",
                                        "--tags", "a",
                                        "--motif", "garde de non-regression"],
                                       capture_output=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as erreur:
        ecarts.append("le verbe `corriger` n a pas pu etre JOUE (" + type(erreur).__name__
                      + ") : le refus n est pas eprouve")
    if resultat_refus is not None:
        sortie_refus = ((resultat_refus.stdout or b"") + (resultat_refus.stderr or b"")
                        ).decode("utf-8", errors="replace")
        if resultat_refus.returncode != 2 or "REFUS" not in sortie_refus:
            ecarts.append("le verbe `corriger` ne REFUSE pas un id inconnu (code "
                          + str(resultat_refus.returncode) + ") : "
                          + sortie_refus.strip()[:120])

    # --- LA DONNEE REELLE : la BDD du depot, lue PAR LE LECTEUR DU PILOTE.

    reelle = module.lire_bdd_raisonnement()
    segments_reels = reelle.get("segments") if isinstance(reelle, dict) else None
    if not isinstance(segments_reels, list) or not segments_reels:
        return ecarts + ["la BDD de raisonnement ne porte AUCUN segment lisible : "
                         + str(type(segments_reels).__name__)]
    source_reelle = str(segments_reels[-1].get("source") or "")
    code, message = module.juger_raisonnement(reelle, source_reelle)
    ep("la-DONNEE-REELLE-porte-son-segment", code == 0,
       "le dernier segment (" + source_reelle + ") n a pas ete reconnu : "
       + str((code, message))[:160])
    code, message = module.juger_raisonnement(reelle, "MO-999999")
    ep("la-DONNEE-REELLE-accuse-un-round-qui-n-a-rien-depose", code == 1,
       "un round absent de la BDD n a pas ete accuse : " + str((code, message))[:160])

    # --- LE CHEMIN DE CLOTURE EST LIE (reprise MO-500) : la PRESENCE des fonctions
    # ne suffit PAS. Mesure du 2026-09-28 : `VERBE_SEGMENT` manquait a l import de
    # commun.py -- py_compile passe (il ne resout pas les noms), la porte ECRIRE
    # passe (elle verifie les imports ECRITS, jamais un nom UTILISE), et les trois
    # preuves du round passaient : aucune n EXECUTAIT le DEPOT. La CLOTURE REELLE a
    # rendu un NameError. Ce mordant le voit SANS executer, borne aux fonctions du
    # chemin de cloture. Le classeur de noms est CONSOMME a son domicile
    # (verifier-contrat-fondamental : noms_lies + LIES_DE_BASE, M-076).
    chemin_classeur = (operateur / "super-combos" / "combos" / "outils"
                       / "verifier-contrat-fondamental.py")
    if not chemin_classeur.is_file():
        ecarts.append("le classeur de noms INTROUVABLE : " + str(chemin_classeur))
    else:
        specification = importlib.util.spec_from_file_location("classeur_noms",
                                                               chemin_classeur)
        classeur = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(classeur)
        arbre_commun = ast.parse(chemins["commun"].read_text(encoding="utf-8"))
        connus = classeur.noms_lies(arbre_commun) | classeur.LIES_DE_BASE
        surveillees = ("lire_segments", "lire_bdd_raisonnement", "juger_raisonnement",
                       "deposer_segments_raisonnement", "controler_raisonnement_mission")
        for fonction in ast.walk(arbre_commun):
            if not isinstance(fonction, ast.FunctionDef) or fonction.name not in surveillees:
                continue
            chargees = {noeud.id for noeud in ast.walk(fonction)
                        if isinstance(noeud, ast.Name)
                        and isinstance(noeud.ctx, ast.Load)}
            for nom in sorted(chargees - connus):
                ecarts.append("`" + nom + "` est UTILISE par " + fonction.name
                              + " mais rien ne le lie (import manquant ?) -- le"
                              " NameError n apparait qu a la CLOTURE reelle")
        orphelin = ast.parse("def cobaye():" + chr(10) + "    return NOM_JAMAIS_LIE_XYZ"
                             + chr(10))
        chargees_orphelin = {noeud.id for noeud in ast.walk(orphelin)
                             if isinstance(noeud, ast.Name)
                             and isinstance(noeud.ctx, ast.Load)}
        ep("cobaye-un-nom-ORPHELIN-est-ACCUSE",
           "NOM_JAMAIS_LIE_XYZ" in chargees_orphelin - connus,
           "le mordant ne voit PAS un nom orphelin (il ne mord pas)")
    return ecarts


# --- MO-488 (EO-446) : LE PATTERN DE MAINTENANCE -----------------------------
# Les faits que le pattern doit DIRE a chaque session. Le createur les a nommes :
# en maintenance, on est en EVOLUTION PERMANENTE, donc ce qui est ancien ou pas
# encore conforme est un ETAT DE TRANSITION -- ni une panne, ni a masquer, ni a
# casser. Ces signatures sont des CHAINES LUES dans le texte servi ; elles sont
# declarees UNE fois ici, jamais ecrites dans la logique du controle.
SIGNATURE_PATTERN_MAINTENANCE = (
    "PATTERN DE MAINTENANCE -- LA MAINTENANCE EST UNE EVOLUTION PERMANENTE")
SIGNATURES_PATTERN_EXIGEES = (
    "EVOLUTION PERMANENTE",
    "ECART DE DATE",
    "JE NE LE MASQUE PAS",
    "JE NE LE CASSE PAS",
)
NOM_FICHIER_PATTERN = "pattern-maintenance.md"
CATEGORIE_PATTERN = "demarrage"
CHEMIN_CARTE_IDENTITE = ("matrice", "data", "commun", "carte_identite.py")


def _declarations_pattern(catalogue):
    """Les entrees, TOUTES categories, qui DECLARENT le pattern (texte pur).

    Rend des couples (categorie, entree). Un pattern declare AILLEURS que dans le
    DEMARRAGE du flux maintenance n est pas un branchement : c est une fuite.
    """
    trouvees = []
    injections = (catalogue or {}).get("injections") or {}
    for categorie in sorted(injections):
        for entree in injections[categorie] or []:
            identifiant = str(entree.get("id", ""))
            source = str(entree.get("source", ""))
            if "pattern" in identifiant or "pattern" in source:
                trouvees.append((categorie, entree))
    return trouvees


def _juger_branchement_pattern(catalogue_maintenance, catalogue_autre, texte_pattern,
                               types_reconnus):
    """PURE : le pattern est-il BRANCHE au demarrage, et la SEULEMENT (MO-488) ?

    Prend des CATALOGUES et des TEXTES -- donc s eprouve sur des jeux FABRIQUES
    (cobayes) comme sur les jeux reels. Cinq faits :
      1. le pattern est DECLARE au catalogue de DEMARRAGE de la maintenance ;
      2. son entree est OBLIGATOIRE et sa source NOMME le fichier attendu -- une
         source optionnelle absente n est qu une ALERTE : le pattern disparaitrait
         en silence (L-055) ;
      3. son texte DIT les quatre faits exiges ET il est ASCII strict ;
      4. le type `pattern` est RECONNU par le vocabulaire ferme des cartes (sinon
         le garde des cartes refuserait le document : un document sans type reconnu
         n a plus d identite) ;
      5. l AUTRE flux ne le declare NI ne le lit -- coherence d invisibilite (L-016).
    """
    ecarts = []
    declarations = _declarations_pattern(catalogue_maintenance)
    if not declarations:
        ecarts.append("le PATTERN DE MAINTENANCE n est plus DECLARE par le catalogue de"
                      " la maintenance : l agent ne lirait plus, a chaque session, que le"
                      " monde est en EVOLUTION PERMANENTE -- des missions anciennes et des"
                      " fichiers pas encore conformes sont un etat de transition, pas une"
                      " panne (le defaut exact que EO-446 repare)")
    hors_demarrage = sorted({categorie for categorie, _e in declarations
                             if categorie != CATEGORIE_PATTERN})
    if hors_demarrage:
        ecarts.append("le pattern est DECLARE hors du demarrage ("
                      + ", ".join(hors_demarrage) + ") : sa place est le demarrage, une"
                      " fois par session (decision D5 du cadrage, EO-446)")
    for _categorie, entree in declarations:
        if not entree.get("obligatoire", False):
            ecarts.append("l entree `" + str(entree.get("id")) + "` du pattern n est pas"
                          " OBLIGATOIRE : une source optionnelle absente n est qu une"
                          " ALERTE -- le pattern s effacerait en silence (L-055)")
        if str(entree.get("source", "")).split("/")[-1] != NOM_FICHIER_PATTERN:
            ecarts.append("l entree `" + str(entree.get("id")) + "` ne pointe pas "
                          + NOM_FICHIER_PATTERN + " : " + str(entree.get("source")))
    if "pattern" not in types_reconnus:
        ecarts.append("le type `pattern` a disparu du VOCABULAIRE FERME des cartes d"
                      " identite : le garde des cartes REFUSERAIT le document du pattern")
    for signature in SIGNATURES_PATTERN_EXIGEES:
        if signature not in texte_pattern:
            ecarts.append("le pattern ne DIT plus `" + signature + "` : le message du"
                          " createur doit tenir en entier -- ce qui est ancien n est pas"
                          " une panne, et il ne faut ni le masquer ni le casser")
    try:
        texte_pattern.encode("ascii")
    except UnicodeEncodeError as erreur:
        ecarts.append("le pattern n est pas ASCII strict (" + str(erreur)[:80] + ")")
    for categorie, entree in _declarations_pattern(catalogue_autre):
        ecarts.append("le pattern FUITE dans l AUTRE flux (categorie `" + categorie
                      + "`, entree `" + str(entree.get("id")) + "`) : la coherence d"
                      " invisibilite (L-016) interdit que ce qu il lit porte ce texte")
    return ecarts


def _eprouver_pattern_maintenance(racine):
    """MAILLON 63 (MO-488 / EO-446) : le PATTERN DE MAINTENANCE est BRANCHE au
    demarrage de la maintenance, et INVISIBLE dans l autre flux.

    Le jugement est PUR (`_juger_branchement_pattern`) : il est donc JOUE sur des
    jeux FABRIQUES avant la donnee REELLE -- un controle qu on n a jamais vu
    MORDRE ne garde rien (L-032).
      - CONTRE-TEMOIN : le jeu conforme reste MUET ;
      - COBAYES (un fait retire a la fois) : source retiree du demarrage, entree
        declaree dans l AUTRE flux, entree rendue OPTIONNELLE, entree declaree hors
        du demarrage, type `pattern` efface du vocabulaire, une signature retiree
        du texte -- chacun doit ACCUSER ;
      - LA MESURE REELLE : les DEUX injecteurs sont EXECUTES (le catalogue reel, par
        sa porte), et l on exige le pattern PRESENT d un cote et ABSENT de l autre ;
        le catalogue reel est en plus juge par le jugement pur.
    """
    import ast
    import json
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    injection_maintenance = (matrice / "_operateur" / "optimus-prime" / "pilote"
                             / "injection")
    injection_autre = matrice / "matrice" / "pilote" / "injection"
    catalogue_maintenance = injection_maintenance / "config.json"
    catalogue_autre = injection_autre / "config.json"
    injecter_maintenance = injection_maintenance / "injecter.py"
    injecter_autre = injection_autre / "injecter.py"
    carte_identite = matrice / _Chemin(*CHEMIN_CARTE_IDENTITE)
    for etiquette, chemin in (("catalogue-maintenance", catalogue_maintenance),
                              ("catalogue-autre", catalogue_autre),
                              ("injecter-maintenance", injecter_maintenance),
                              ("injecter-autre", injecter_autre),
                              ("carte-identite", carte_identite)):
        if not chemin.is_file():
            return ["fichier INTROUVABLE (" + etiquette + ") : " + str(chemin)]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    # LE JUGEMENT PUR, EPROUVE SUR DES JEUX FABRIQUES (aucun FICHIER touche).
    texte_juste = (SIGNATURE_PATTERN_MAINTENANCE + chr(10)
                   + chr(10).join(SIGNATURES_PATTERN_EXIGEES) + chr(10))
    entree_juste = {"id": "pattern-maintenance",
                    "source": "injection/" + NOM_FICHIER_PATTERN,
                    "type": "fichier",
                    "obligatoire": True}
    types_justes = ("analyse", "pattern", "readme")
    aucun = {"injections": {}}

    def catalogue(entrees, categorie=CATEGORIE_PATTERN):
        return {"injections": {categorie: list(entrees)}}

    jeux = (
        ("CONTRE-TEMOIN -- le jeu conforme reste MUET",
         (catalogue([entree_juste]), aucun, texte_juste, types_justes), False),
        ("le pattern n est plus DECLARE au demarrage",
         (catalogue([]), aucun, texte_juste, types_justes), True),
        ("le pattern est declare dans l AUTRE flux",
         (catalogue([entree_juste]), catalogue([dict(entree_juste)]), texte_juste,
          types_justes), True),
        ("l entree du pattern n est plus OBLIGATOIRE",
         (catalogue([dict(entree_juste, obligatoire=False)]), aucun, texte_juste,
          types_justes), True),
        ("le type `pattern` a disparu du vocabulaire ferme",
         (catalogue([entree_juste]), aucun, texte_juste, ("analyse", "readme")), True),
        ("une signature du message a ete retiree",
         (catalogue([entree_juste]), aucun,
          texte_juste.replace(SIGNATURES_PATTERN_EXIGEES[2], ""), types_justes), True),
        ("le pattern est declare HORS du demarrage",
         (catalogue([entree_juste], "avant-mission"), aucun, texte_juste,
          types_justes), True),
    )
    for nom, arguments, doit_mordre in jeux:
        ecarts_jeu = _juger_branchement_pattern(*arguments)
        if doit_mordre and not ecarts_jeu:
            ecarts.append("cobaye NON MORDANT (" + nom + ") : le controle n a rien"
                          " accuse alors que le fait manquait")
        if not doit_mordre and ecarts_jeu:
            ecarts.append("contre-temoin ACCUSE A TORT (" + nom + ") : "
                          + str(ecarts_jeu)[:160])

    # LA DONNEE REELLE : le catalogue de la maintenance et son fichier de pattern.
    donnees_maintenance = json.loads(catalogue_maintenance.read_text(encoding="utf-8"))
    donnees_autre = json.loads(catalogue_autre.read_text(encoding="utf-8"))
    # Le vocabulaire FERME des types est LU EN LITTERAL chez son domicile (M-076) :
    # le controle ne le recopie pas et n execute pas la grammaire pour le lire.
    types_reconnus = ()
    for noeud in ast.parse(carte_identite.read_text(encoding="utf-8")).body:
        if not isinstance(noeud, ast.Assign):
            continue
        noms = [cible.id for cible in noeud.targets if isinstance(cible, ast.Name)]
        if "TYPES_RECONNUS" in noms and isinstance(noeud.value, ast.Tuple):
            types_reconnus = tuple(element.value for element in noeud.value.elts
                                   if isinstance(element, ast.Constant))
    if not types_reconnus:
        return ecarts + ["TYPES_RECONNUS est INTROUVABLE ou vide dans "
                         + str(carte_identite) + " : la grammaire des cartes n a plus de"
                         " vocabulaire a opposer"]
    source_pattern = None
    for _categorie, entree in _declarations_pattern(donnees_maintenance):
        candidat = (injection_maintenance.parent / str(entree.get("source", ""))).resolve()
        if candidat.is_file():
            source_pattern = candidat
    texte_reel = source_pattern.read_text(encoding="utf-8") if source_pattern else ""
    if not texte_reel:
        ecarts.append("le FICHIER du pattern est INTROUVABLE depuis le catalogue de la"
                      " maintenance : le branchement pointe un texte qui n existe pas")
    ecarts += _juger_branchement_pattern(donnees_maintenance, donnees_autre, texte_reel,
                                         types_reconnus)

    # LA MESURE EN EXECUTION : les DEUX injecteurs servis par LEUR porte, sans
    # interpreteur recopie -- le pattern doit etre PRESENT d un cote, ABSENT de
    # l autre. C est la seule mesure qui parle du FLUX, pas du catalogue.
    for etiquette, script, present_attendu in (
            ("injecter-maintenance", injecter_maintenance, True),
            ("injecter-autre", injecter_autre, False)):
        resultat = lancer_enfant([sys.executable, str(script), CATEGORIE_PATTERN],
                                 capture_output=True, text=True)
        sortie = (resultat.stdout or "") + (resultat.stderr or "")
        if resultat.returncode != 0:
            lignes = [ligne for ligne in sortie.splitlines() if ligne.strip()]
            ecarts.append(etiquette + " n a pas pu servir `" + CATEGORIE_PATTERN
                          + "` (code " + str(resultat.returncode) + ") : "
                          + (lignes[-1][:160] if lignes else "aucune sortie"))
            continue
        vu = SIGNATURE_PATTERN_MAINTENANCE in sortie
        if present_attendu:
            ep("le pattern est PRESENT dans l injection de demarrage de la maintenance",
               vu, "la signature du pattern est ABSENTE de l injection de demarrage :"
                   " le branchement ne sert rien")
        else:
            ep("le pattern est ABSENT de l injection de l AUTRE flux", not vu,
               "la signature du pattern APPARAIT dans l injection de l autre flux : la"
               " coherence d invisibilite (L-016) est rompue")
    return ecarts


def _verifier_citation_sources(texte_constantes, texte_commun, texte_fonctions,
                              texte_facade, texte_manuel, texte_jugement):
    """Ecarts du CABLAGE du jugement des citations (MO-489). PURE.

    Le fait mesure n est pas < le garde est vert > -- un vert peut venir d un garde
    devenu AVEUGLE -- mais < le garde CONSOMME le domicile de la zone des sources >.
    La decision vit dans data/commun/zone_sources.py (MO-377, la meme que la porte
    ECRIRE et le garde ASCII) : elle se LIT, elle ne se recopie jamais (M-076). Un nom
    de zone ecrit EN DUR dans le jugement serait la divergence qui attend, et une
    exemption MUETTE serait un angle mort qu aucune suite ne voit (MO-075).
    """
    ecarts = []
    if "zone_sources import" not in texte_constantes:
        ecarts.append("les CONSTANTES du garde n importent plus le domicile de la zone"
                      " des sources (data/commun/zone_sources.py) : la decision serait"
                      " recopiee, ou perdue (M-076)")
    if "est_zone_sources" not in texte_constantes:
        ecarts.append("les CONSTANTES du garde n exposent plus `est_zone_sources` : le"
                      " jugement n aurait plus rien a consommer")
    # OU EST LE JUGEMENT, ET NON SEULEMENT COMMENT IL S APPELLE (EO-479). La regle
    # a change de DOMICILE : elle vit dans data/commun/jugement_citations.py, que
    # les trois verificateurs consomment (M-076). Exiger l appel dans commun.py
    # revenait a EXIGER que la regle soit recopiee -- c est a dire, a interdire la
    # reparation. Ce maillon suit donc le jugement la ou il est, et exige en plus
    # que le consommateur le consomme : les deux moities de la regle, pas une.
    if "est_zone_sources(" not in texte_jugement:
        ecarts.append("le JUGEMENT (data/commun/jugement_citations.py) n appelle plus"
                      " `est_zone_sources` : une citation de la zone des sources serait"
                      " de nouveau ACCUSEE sans qu aucun remede soit possible (le"
                      " defaut de MO-489 est revenu)")
    if "jugement_citations" not in texte_commun:
        ecarts.append("le CONSOMMATEUR (commun.py) ne consomme plus jugement_citations :"
                      " il porterait sa propre copie du jugement, donc deux verites (M-076)")
    if '"docs"' in texte_commun or "'docs'" in texte_commun:
        ecarts.append("le JUGEMENT porte le nom de la zone EN DUR (docs) : la valeur se"
                      " lit au domicile, elle ne s ecrit pas chez le consommateur"
                      " (M-076)")
    if "afficher_dit(" not in texte_fonctions:
        ecarts.append("la SORTIE du garde n affiche plus le groupe DIT : l exemption"
                      " deviendrait MUETTE, donc un angle mort (MO-075)")
    if "HORS CHAMP" not in texte_facade:
        ecarts.append("la FACADE du garde (DESCRIPTION.md) ne DIT plus ce qu il mesure"
                      " sans le juger : un garde dont la facade tait son exemption laisse"
                      " croire qu il juge tout")
    if "HORS CHAMP" not in texte_manuel:
        ecarts.append("la fiche du MANUEL ne DIT plus le groupe hors champ : la facade"
                      " de l outil n est pas la seule a devoir le dire")
    return ecarts


def _eprouver_citation_sources(racine):
    """MAILLON 64 (MO-489 / EO-451) : une citation de la ZONE DES SOURCES du createur
    est MESUREE et DITE, jamais accusee -- parce que la porte ECRIRE la REFUSE.

    LA MESURE QUI FONDE CE MAILLON (2026-09-29). Le garde du marbre accusait une ligne
    morte de l index des protocoles (../../../docs/conversation-unslot-gemma-4.md,
    cite pour dire d ou viennent les protocoles 3-4). La cible a ete SUPPRIMEE par le
    commit du createur (8ff87a76, 2026-09-27). La Matrice l avait deja recouvree une
    fois par git (MO-320), et le commit suivant l a retiree : le recouvrement etait en
    PURE PERTE. Or la porte ECRIRE -- SEUL passage d ecriture -- REFUSE toute ecriture
    dans docs/ en la nommant (zone_sources.py, MO-377). Le garde exigeait donc une
    ecriture que la porte du MEME domaine interdit : un rouge permanent, present sur
    /sante depuis le 2026-09-26, que personne ne pouvait reparer. C est le defaut
    qu a deja repare MO-377 dans le garde ASCII -- deux instruments de la meme maison
    qui disent deux choses differentes sur la meme zone.

    L ORDRE, comme partout : le CABLAGE (le garde CONSOMME le domicile), puis les
    JEUX (un contre-temoin qui EPARGNE, des cobayes qui MORDENT et qui DISENT), puis
    la MESURE REELLE (le garde EXECUTE sur l index du depot : code 0, aucun ECART, et
    l exemption DITE).
    """
    import importlib.util
    from pathlib import Path as _Chemin
    # RESOLUE : le chemin d un script se resout contre le cwd de l ENFANT, donc un
    # chemin relatif lance depuis un autre dossier ne trouve plus rien (le sous-processus
    # rendait code 2, sortie vide -- mesure de ce round ; la suite ne le voit que si elle
    # JOUE la mesure, ce qu elle fait).
    racine = _Chemin(racine).resolve()
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    outil = matrice / "matrice" / "data" / "outils" / "verifier-protocoles"
    chemins = {
        "constantes": outil / "constants.py",
        "commun": outil / "commun.py",
        "fonctions": outil / "verifier" / "fonctions.py",
        "facade": outil / "DESCRIPTION.md",
        "manuel": matrice / "matrice" / "data" / "manuel-outils.md",
        # LE DOMICILE DU JUGEMENT (EO-479) : c'est ici que la regle vit, et c'est
        # ici -- et plus dans commun.py -- que l on verifie qu elle consomme la
        # zone des sources.
        "jugement": matrice / "matrice" / "data" / "commun" / "jugement_citations.py",
    }
    for etiquette in sorted(chemins):
        if not chemins[etiquette].is_file():
            return ["fichier INTROUVABLE (" + etiquette + ") : " + str(chemins[etiquette])]

    ecarts = _verifier_citation_sources(
        _lire_si_present(chemins["constantes"]),
        _lire_si_present(chemins["commun"]),
        _lire_si_present(chemins["fonctions"]),
        _lire_si_present(chemins["facade"]),
        _lire_si_present(chemins["manuel"]),
        _lire_si_present(chemins["jugement"]))

    # LA REGLE EST JOUEE, pas seulement lue : le jugement de l outil est charge par son
    # CHEMIN (motif des maillons 46 et 61 -- le dossier du garde et data/commun entrent
    # dans sys.path, puis en SORTENT : aucun sys.path laisse).
    dossier_commun = matrice / "matrice" / "data" / "commun"
    # PIEGE MESURE CE ROUND (le maillon a d abord rendu KO avec un ImportError) : un
    # module charge PAR SON CHEMIN qui importe un nom NU (`from constants import ...`)
    # prend celui qui est DEJA EN CACHE -- ici les `constants.py` d un AUTRE outil,
    # importes par un maillon precedent. Un nom nu est un nom GLOBAL : le sys.path de
    # l appelant ne suffit pas a designer SES voisins. On ecarte donc les noms
    # glissants le temps du chargement, et on les REMET ensuite (rien n est laisse
    # derriere : ni chemin, ni module en cache).
    glissants = ("constants", "commun", "zone_sources", "cible", "racine")
    sauve = {}
    for nom in glissants:
        if nom in sys.modules:
            sauve[nom] = sys.modules.pop(nom)
    ajoutes = [str(outil), str(dossier_commun)]
    for chemin in ajoutes:
        sys.path.insert(0, chemin)
    try:
        specification = importlib.util.spec_from_file_location("commun_citations", chemins["commun"])
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["commun.py du garde ILLISIBLE (" + type(erreur).__name__
                         + " : " + str(erreur)[:60] + ")"]
    finally:
        for chemin in ajoutes:
            sys.path.remove(chemin)
        for nom in glissants:
            sys.modules.pop(nom, None)
        sys.modules.update(sauve)

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    reels = [_Chemin("proto-1-reprise-mission.md")]
    verdict = module.verifier_index(["| 1. Reprise | proto-1-reprise-mission.md |"], reels)
    if not isinstance(verdict, tuple) or len(verdict) != 3:
        return ecarts + ["le jugement ne rend PAS trois verdicts (manquants, morts,"
                         " hors_champ) : un garde sans troisieme verdict accuse ce"
                         " qu il ne peut pas reparer (MO-489)"]

    citation_source = "../../../docs/conversation-unslot-gemma-4.md"
    jeux = (
        # CONTRE-TEMOIN : la citation des sources est EPARGNEE et DITE.
        ("la-citation-des-SOURCES-n-est-PAS-accusee",
         ["| Discussion d origine | " + citation_source + " |",
          "| 1. Reprise | proto-1-reprise-mission.md |"], False, True),
        # COBAYES : hors de la zone des sources, le garde MORD encore.
        ("une-ligne-morte-de-la-MATRICE-est-ACCUSEE",
         ["| Ressource | ../../../matrice/docs/absent-cobaye-mo489.md |"], True, False),
        ("un-nom-nu-ABSENT-est-ACCUSE",
         ["| Protocole | absent-cobaye-mo489.md |"], True, False),
        # COBAYE : cible ABSENTE dans la zone -- le garde ne l accuse pas, il la DIT.
        ("la-cible-ABSENTE-des-SOURCES-est-DITE",
         ["| Source | ../../../docs/absent-cobaye-mo489.md |"], False, True),
        # COBAYE : cible PRESENTE dans la zone -- mesuree, dite, jamais jugee non plus.
        ("la-cible-PRESENTE-des-SOURCES-est-DITE-aussi",
         ["| Source | ../../../docs/IMPERATIF.md |"], False, True),
    )
    for nom, lignes, doit_mordre, doit_dire in jeux:
        _, morts, hors_champ = module.verifier_index(lignes, reels)
        if doit_mordre and not morts:
            ecarts.append("cobaye NON MORDANT (" + nom + ") : le jugement n a RIEN"
                          " accuse alors qu une cible manquait hors de la zone")
        if not doit_mordre and morts:
            ecarts.append("contre-temoin ACCUSE A TORT (" + nom + ") : " + str(morts)[:160])
        if doit_dire and not hors_champ:
            ecarts.append("l exemption est MUETTE (" + nom + ") : la citation est passee"
                          " sans etre DITE -- une exemption muette est un angle mort")
        if not doit_dire and hors_champ:
            ecarts.append("HORS CHAMP a tort (" + nom + ") : " + str(hors_champ)[:160])

    # LA MESURE REELLE : le garde du depot, EXECUTE (aucune ecriture).
    lanceur = matrice / "lancer.py"
    if not lanceur.is_file():
        return ecarts + ["lancer.py INTROUVABLE : " + str(lanceur)]
    # La base de lancement se DETECTE par marqueur (AGENTS.md), jamais par un nombre de
    # parents suppose : la Matrice vit sous cerveau-projet/matrix dans le depot, et
    # directement sous la racine dans une installation deploiee.
    espace = matrice
    while espace.parent != espace and not (espace / "AGENTS.md").is_file():
        espace = espace.parent
    resultat = lancer_enfant([sys.executable, str(lanceur), "verifier-protocoles", "verifier"],
                             capture_output=True, text=True, cwd=str(espace))
    sortie = resultat.stdout or ""
    ep("le-garde-du-DEPOT-rend-0", resultat.returncode == 0,
       "code " + str(resultat.returncode) + " : "
       + (sortie.strip().splitlines()[-1][:160] if sortie.strip() else "(sortie vide)"))
    ep("l-index-du-DEPOT-n-a-PLUS-de-ligne-morte", "ECART" not in sortie,
       "le garde accuse encore : "
       + "; ".join(ligne.strip() for ligne in sortie.splitlines() if "ECART" in ligne)[:200])
    ep("l-exemption-du-DEPOT-est-DITE",
       "HORS CHAMP" in sortie and "conversation-unslot-gemma-4.md" in sortie,
       "l exemption n est pas DITE par le garde du depot : une exemption muette est un"
       " angle mort")
    return ecarts


# La MISSION TEMOIN des cobayes du maillon 65 : un identifiant QU UNE VRAIE MISSION
# ne peut pas porter (la file numerote MO-XXX a trois chiffres). Il n aura donc
# JAMAIS de passage note : c est ce qui rend la mesure REELLE stable -- elle ne
# depend pas du contenu (rotatif) du registre des usages.
MISSION_SANS_PASSAGE = "MO-999999"
TAG_PASSAGE_LANCEUR = '"super-combo"'
NOM_PORTE_USAGES = "bdd-usages"
VERBE_PREUVES = "--preuves"
NOM_JUGEMENT = "def juger_passages"


def _citations_combos(texte):
    """Les ids `sc-NNN` cites par un texte, tries et uniques (aucune dependance a `re`)."""
    trouves = set()
    for position in range(len(texte) - 5):
        morceau = texte[position:position + 6]
        if morceau.startswith("sc-") and morceau[3:].isdigit():
            trouves.add(morceau)
    return sorted(trouves)


def _verifier_processus_super_combos(texte_processus, texte_lanceur, combos_attendus,
                                     catalogue_demarrage, catalogue_autre):
    """Ecarts du CABLAGE du processus des super-combos (MO-491 / EO-447). PURE.

    Quatre faits, et chacun est un maillon de la chaine :
      (1) le processus NOMME tous les combos que le REGISTRE declare -- l autorite
          est le registre, le texte ne fait que le nommer : un combo ajoute au
          registre sans etre nomme n aurait AUCUN demandeur ;
      (2) il n en nomme AUCUN qui n y est plus : un fantome envoie l agent lancer
          ce qui n existe pas ;
      (3) il DIT la PREUVE (le registre des usages et le verbe `--preuves`) : un
          passage exige sans preuve verifiable reste une consigne qu on oublie ;
      (4) le LANCEUR porte la TRACE et le JUGE : sinon la preuve n a pas de
          producteur (personne ne note), ou pas de lecture (on ne juge rien).
    """
    ecarts = []
    for combo in combos_attendus:
        if combo not in texte_processus:
            ecarts.append("le PROCESSUS ne NOMME pas " + combo + " : le registre le"
                          " declare, aucun texte ne le demande -- un combo sans"
                          " demandeur ne se passe jamais")
    for combo in _citations_combos(texte_processus):
        if combo not in combos_attendus:
            ecarts.append("le PROCESSUS nomme " + combo + " qui n est PAS au registre :"
                          " un combo fantome envoie l agent lancer ce qui n existe pas")
    for marque in (VERBE_PREUVES, "usages-outils-combos"):
        if marque not in texte_processus:
            ecarts.append("le PROCESSUS ne DIT pas la PREUVE (" + marque + " absent) : un"
                          " passage exige sans preuve verifiable est une consigne, pas un"
                          " processus (L-165)")
    for marque, quoi in ((TAG_PASSAGE_LANCEUR, "le TAG de passage"),
                         (NOM_PORTE_USAGES, "la PORTE des usages"),
                         (VERBE_PREUVES, "le VERBE des preuves"),
                         (NOM_JUGEMENT, "le jugement (`juger_passages`)")):
        if marque not in texte_lanceur:
            ecarts.append("le LANCEUR ne porte plus " + quoi + " : la preuve n a plus de"
                          " producteur -- ou plus de lecture")
    if "processus-super-combos" not in catalogue_demarrage:
        ecarts.append("le catalogue de DEMARRAGE ne declare plus le processus : aucune"
                      " session ne le recevrait")
    if "processus-super-combos" in catalogue_autre:
        ecarts.append("le processus est declare dans l AUTRE flux : il doit rester"
                      " INVISIBLE (L-016)")
    return ecarts


def _eprouver_processus_super_combos(racine):
    """MAILLON 65 (MO-491 / EO-447) : le PROCESSUS des super-combos est BRANCHE, il
    NOMME ce que le REGISTRE declare, et la PREUVE de passage EXISTE.

    LA MESURE QUI FONDE CE MAILLON (2026-09-29). Demande du createur : < un PROCESS
    INJECTE qui NOMME et LANCE les super-combos pertinents, quand on corrige,
    ameliore ou modifie des fichiers et les flux -- avec la PREUVE de leur
    passage. > Constat mesure : la Matrice POSSEDAIT les super-combos, et l agent
    SAVAIT quand les employer (leurs modes d emploi voyagent avec la mission), mais
    rien ne FORCAIT leur passage, et la PREUVE n existait PAS : le registre unique
    des usages ne portait qu UNE occurrence d un super-combo sur 65686 lignes, et
    le lanceur n ecrivait aucune trace. Une consigne qu on peut oublier est une
    discipline, pas un processus (L-165).

    L ORDRE, comme partout : le CABLAGE (lu dans les textes, juge par une fonction
    PURE), puis les JEUX du jugement (un contre-temoin qui EPARGNE, quatre cobayes
    qui MORDENT), puis la MESURE REELLE -- le lanceur est EXECUTE sur une mission
    qui ne peut pas avoir de passage (il ACCUSE et NOMME) et sans demande (il
    n accuse rien). Le jugement est JOUE sur des entrees FABRIQUEES pour le cas
    < passage present > : le registre reel est un journal ROTATIF, donc une
    assertion sur son contenu d aujourd hui deviendrait fausse sans qu aucun
    defaut soit ne (une mesure qui vieillit accuse a tort).
    """
    import importlib.util
    import json
    from pathlib import Path as _Chemin
    racine = _Chemin(racine).resolve()
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    operateur = matrice / "_operateur" / "optimus-prime"
    combos = operateur / "super-combos"
    chemins = {
        "lanceur": combos / "lancer-super-combos.py",
        "registre": combos / "registry.json",
        "processus": operateur / "pilote" / "injection" / "processus-super-combos.md",
        "catalogue": operateur / "pilote" / "injection" / "config.json",
        "catalogue-autre": matrice / "matrice" / "pilote" / "injection" / "config.json",
    }
    for etiquette in sorted(chemins):
        if not chemins[etiquette].is_file():
            return ["fichier INTROUVABLE (" + etiquette + ") : " + str(chemins[etiquette])]

    try:
        donnees = json.loads(chemins["registre"].read_text(encoding="utf-8"))
    except ValueError as erreur:
        return ["le REGISTRE des super-combos est ILLISIBLE (" + str(erreur)[:60] + ")"]
    combos_attendus = [str(combo.get("id", "")) for combo in donnees.get("super-combos", [])]
    if not combos_attendus:
        return ["le REGISTRE est VIDE : il n y a rien a demander, donc rien a prouver"]

    ecarts = _verifier_processus_super_combos(
        _lire_si_present(chemins["processus"]),
        _lire_si_present(chemins["lanceur"]),
        combos_attendus,
        _lire_si_present(chemins["catalogue"]),
        _lire_si_present(chemins["catalogue-autre"]))

    # LES JEUX DU CABLAGE : le MEME jugement est JOUE sur des textes FABRIQUES, avant
    # la donnee reelle -- un controle qu on n a jamais vu MORDRE ne garde rien (L-032).
    texte_juste = (" ".join(combos_attendus) + " " + VERBE_PREUVES
                   + " usages-outils-combos.jsonl")
    lanceur_juste = (TAG_PASSAGE_LANCEUR + " " + NOM_PORTE_USAGES + " "
                     + VERBE_PREUVES + " " + NOM_JUGEMENT)
    catalogue_juste = '{"id": "processus-super-combos"}'
    jeux_cablage = (
        ("CONTRE-TEMOIN -- les textes justes restent MUETS",
         (texte_juste, lanceur_juste, combos_attendus, catalogue_juste, "autre"), False),
        ("COBAYE -- un combo du registre n est plus NOMME",
         (texte_juste.replace(combos_attendus[-1], ""), lanceur_juste, combos_attendus,
          catalogue_juste, "autre"), True),
        ("COBAYE -- le processus nomme un combo FANTOME",
         (texte_juste + " sc-999", lanceur_juste, combos_attendus, catalogue_juste,
          "autre"), True),
        ("COBAYE -- la PREUVE n est plus DITE",
         (" ".join(combos_attendus) + " " + VERBE_PREUVES, lanceur_juste, combos_attendus,
          catalogue_juste, "autre"), True),
        ("COBAYE -- le LANCEUR ne note plus le passage",
         (texte_juste, lanceur_juste.replace(TAG_PASSAGE_LANCEUR, ""), combos_attendus,
          catalogue_juste, "autre"), True),
        ("COBAYE -- le LANCEUR ne JUGE plus",
         (texte_juste, lanceur_juste.replace(NOM_JUGEMENT, ""), combos_attendus,
          catalogue_juste, "autre"), True),
        ("COBAYE -- le catalogue de DEMARRAGE ne le declare plus",
         (texte_juste, lanceur_juste, combos_attendus, "rien", "autre"), True),
        ("COBAYE -- il est declare dans l AUTRE flux",
         (texte_juste, lanceur_juste, combos_attendus, catalogue_juste,
          "processus-super-combos"), True),
    )
    for nom, arguments, doit_mordre in jeux_cablage:
        ecarts_jeu = _verifier_processus_super_combos(*arguments)
        if doit_mordre and not ecarts_jeu:
            ecarts.append("cobaye NON MORDANT (" + nom + ") : le controle n a RIEN"
                          " accuse alors que le fait manquait")
        if not doit_mordre and ecarts_jeu:
            ecarts.append("contre-temoin ACCUSE A TORT (" + nom + ") : "
                          + str(ecarts_jeu)[:160])

    # LE JUGEMENT EST JOUE, pas seulement lu : le lanceur est charge PAR SON CHEMIN
    # (motif des maillons 61 et 64), et les noms NU en CACHE sont ecartes le temps du
    # chargement -- un module qui importe `lancement` ou `round_servi` prendrait
    # celui d un AUTRE appelant (un nom nu est un nom GLOBAL).
    glissants = ("lancement", "round_servi", "constants", "commun")
    sauve = {}
    for nom in glissants:
        if nom in sys.modules:
            sauve[nom] = sys.modules.pop(nom)
    try:
        specification = importlib.util.spec_from_file_location("lanceur_super_combos",
                                                               chemins["lanceur"])
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["le LANCEUR est ILLISIBLE (" + type(erreur).__name__ + " : "
                         + str(erreur)[:80] + ")"]
    finally:
        for nom in glissants:
            sys.modules.pop(nom, None)
        sys.modules.update(sauve)

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    def usage(combo, mission, tags=None, code=0):
        return {"date": "2026-09-29 00:00:00", "outil": combo, "commande": "status",
                "code": code, "tags": tags or ["super-combo", mission.lower()],
                "detail": "mission " + mission + " ; cible : X"}

    jeux = (
        ("contre-temoin-un-passage-PROUVE-epargne",
         [usage("sc-005", "MO-901")], ["sc-005"], "MO-901", 0),
        ("cobaye-un-combo-DEMANDE-sans-passage-est-ACCUSE",
         [usage("sc-005", "MO-901")], ["sc-005", "sc-001"], "MO-901", 1),
        ("cobaye-le-passage-d-une-AUTRE-mission-ne-compte-PAS",
         [usage("sc-005", "MO-900")], ["sc-005"], "MO-901", 1),
        ("cobaye-une-entree-SANS-le-tag-de-passage-ne-compte-PAS",
         [usage("sc-005", "MO-901", tags=["sac-a-dos", "mo-901"])], ["sc-005"], "MO-901", 1),
        ("contre-temoin-AUCUNE-demande-n-accuse-RIEN",
         [], [], "MO-901", 0),
        # EO-484 (MO-512) : LE CODE EST LE JUGE DU PASSAGE. Un combo lance qui
        # rend code 2 a bien ete TENTE, mais il n a pas PASSE : le compter comme
        # preuve mesurait une tentative, et lisait le verdict < preuve COMPLETE >
        # sur un combo casse.
        ("cobaye-un-passage-ECHOUE-n-est-PAS-un-passage-PROUVE",
         [usage("sc-005", "MO-901", code=2)], ["sc-005"], "MO-901", 1),
        ("contre-temoin-un-passage-REUSSI-code-0-est-un-passage-PROUVE",
         [usage("sc-005", "MO-901", code=0)], ["sc-005"], "MO-901", 0),
        ("cobaye-un-code-EN-CHAINE-0-compte-comme-REUSSI",
         [usage("sc-005", "MO-901", code="0")], ["sc-005"], "MO-901", 0),
        ("cobaye-un-code-EN-CHAINE-2-ne-compte-PAS",
         [usage("sc-005", "MO-901", code="2")], ["sc-005"], "MO-901", 1),
        ("cobaye-une-entree-SANS-code-n-est-PAS-un-succes-DEMONTRE",
         [{"date": "2026-09-29 00:00:00", "outil": "sc-005", "commande": "status",
           "tags": ["super-combo", "mo-901"], "detail": "sans code"}],
         ["sc-005"], "MO-901", 1),
        ("contre-temoin-un-code-NON-numerique-n-est-pas-un-succes-invente",
         [usage("sc-005", "MO-901", code="inconnu")], ["sc-005"], "MO-901", 1),
    )
    for nom, entrees, demandes, mission, code_attendu in jeux:
        code, passages, manquants, echoues = module.juger_passages(entrees, demandes, mission)
        ep(nom, code == code_attendu,
           "code " + str(code) + " au lieu de " + str(code_attendu) + " -- passages : "
           + str(len(passages)) + ", manquants : " + str(manquants)[:120])
        if nom.startswith(("cobaye-un-passage-ECHOUE", "cobaye-un-code-EN-CHAINE-2",
                           "cobaye-une-entree-SANS-code",
                           "contre-temoin-un-code-NON")):
            ep(nom + " : l ECHEC est RENDU, jamais muet", len(echoues) >= 1,
               "aucune entree Echouee rendue : un echec muet ne dit pas ce qui a rate")
            ep(nom + " : l ECHEC n est PAS compte comme passage", len(passages) == 0,
               "un passage echoue est compte comme prouve : la mesure ment")
        if code_attendu == 1:
            ep(nom + " : l accusation NOMME le combo manquant", bool(manquants),
               "l accusation ne nomme aucun combo : elle ne dit pas QUOI passer")

    # LA MESURE REELLE : le lanceur est EXECUTE -- `--preuves` ne lance AUCUN combo et
    # n ecrit RIEN (lecture du registre + jugement). Un garde n ecrit jamais dans le
    # service (L-053).
    resultat = lancer_enfant([sys.executable, str(chemins["lanceur"]), VERBE_PREUVES,
                              MISSION_SANS_PASSAGE, "--combos", ",".join(combos_attendus)],
                             capture_output=True, text=True)
    sortie = resultat.stdout or ""
    ep("une-mission-SANS-passage-est-ACCUSEE", resultat.returncode == 1,
       "code " + str(resultat.returncode) + " : " + sortie.strip()[:160])
    ep("l-accusation-NOMME-TOUS-les-combos-demandes",
       all(combo in sortie for combo in combos_attendus),
       "l accusation ne nomme pas tous les combos demandes : " + sortie.strip()[:160])
    resultat = lancer_enfant([sys.executable, str(chemins["lanceur"]), VERBE_PREUVES,
                              MISSION_SANS_PASSAGE],
                             capture_output=True, text=True)
    ep("sans-demande-le-lanceur-n-accuse-RIEN", resultat.returncode == 0,
       "code " + str(resultat.returncode) + " : " + (resultat.stdout or "").strip()[:160])
    return ecarts


def _eprouver_extraction_passerelle(racine):
    """MAILLON 68 (MO-505 / EO-481) : la CHAINE D EXTRACTION de la passerelle.

    Demande du createur : LIRE la passerelle du user, en faire des ITEMS, et
    RETIRER du canal ce qui a ete servi -- sans jamais perdre les MOTS EXACTS.

    LA MESURE QUI FONDE CE MAILLON (2026-09-29, premiere extraction reelle). La
    porte lisait l identifiant attribue par un `search` du motif large sur TOUTE la
    sortie de l entonnoir -- or cette sortie NOMME AUSSI les items PROCHES (le
    verdict de DOUBLON POSSIBLE). Mesure : la demande du user a ete archivee sous
    EO-476, l item d un AUTRE, alors que l entonnoir venait d attribuer EO-482 ; et
    le verdict de doublon etait AVALE. Un identifiant faux n est pas un detail : le
    journal du canal est la MEMOIRE des mots du user, et elle pointait ailleurs.

    Ce maillon JOUE : le jugement de l identifiant sur la SORTIE REELLE qui a
    trompe la porte (et ses contre-temoins : sans ligne d item, aucun id invente),
    la CHAINE ENTIERE dans un bac a sable jetable (canal cobaye + porte d entonnoir
    cobaye : item journalise sous l id de la PORTE, mots du user conserves, demande
    servie retiree, voisine INTACTE, doute DIT), le REFUS de retirer une demande
    sans item, le suivi des etats, le DRY qui n ecrit rien -- puis la MESURE REELLE
    sur le canal vivant du user : il est LU, et rien n est ecrit.
    """
    import contextlib
    import hashlib
    import importlib
    import io
    import shutil
    import tempfile
    from pathlib import Path as _Chemin

    racine = _Chemin(racine).resolve()
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    porte = matrice / "_operateur" / "optimus-prime" / "pilote" / "passerelle"
    pilote = porte.parent
    chemins = {
        "fonctions": porte / "fonctions.py",
        "readme": porte / "README.md",
        "pilote": pilote / "main.py",
        "canal": matrice / "user-demandes" / "user-demandes.md",
    }
    manquants = [cle for cle in sorted(chemins) if not chemins[cle].is_file()]
    if manquants:
        return ["fichier INTROUVABLE : " + ", ".join(manquants)]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    def empreinte(chemin):
        """L empreinte du canal : une LECTURE ne doit pas la changer."""
        return hashlib.sha256(_Chemin(chemin).read_bytes()).hexdigest()

    # 1. LE CABLAGE : le pilote route la porte ; la porte DIT ses verbes et son DRY.
    ep("le pilote ROUTE la passerelle",
       '"passerelle": passerelle_executer' in _lire_si_present(chemins["pilote"]),
       "le pilote ne route pas la passerelle")
    texte_readme = _lire_si_present(chemins["readme"])
    ep("la porte DIT ses deux verbes",
       "passerelle lire" in texte_readme and "extraire" in texte_readme,
       "le readme de la porte ne dit pas ses verbes")
    ep("la porte DIT son DRY par defaut", "DRY" in texte_readme,
       "le readme ne dit pas que extraire est DRY par defaut")

    # 2. LE MODULE DE LA PORTE, charge a SON chemin, ses voisins ecartes (motif 61/64).
    glissants = ("passerelle", "passerelle.constants", "passerelle.fonctions",
                 "passerelle_user")
    sauve = {}
    for glissant in glissants:
        if glissant in sys.modules:
            sauve[glissant] = sys.modules.pop(glissant)
    sys.path.insert(0, str(pilote))
    try:
        module = importlib.import_module("passerelle.fonctions")
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["passerelle/fonctions.py ILLISIBLE (" + type(erreur).__name__
                         + " : " + str(erreur)[:80] + ")"]
    finally:
        sys.path.remove(str(pilote))

    # 3. LE JUGEMENT DE L IDENTIFIANT, joue sur la SORTIE REELLE qui a trompe la
    #    porte : le verdict de doublon nomme EO-476, la ligne d item porte EO-482.
    sortie_reelle = (
        "ATTENTION DOUBLON POSSIBLE (1 item(s) proche(s), 1 mot(s) commun(s) ou plus) :\n"
        "  - EO-476 : LE MODE SIMULE DE LA ROUTE [parcours] ECRIT QUAND MEME LE FICHIER"
        " [communs : fichiers]\n"
        "  (rien n est bloque : si c est le meme travail, REUNIR les items ; sinon"
        " continuer.)\n"
        "Mission EO-482 deposee au vrac (urgence normale, source operateur)"
        " -- type propose : dev\n")
    ep("l identifiant se lit sur la LIGNE D ITEM",
       module.item_de_sortie(sortie_reelle) == "EO-482",
       "rendu " + repr(module.item_de_sortie(sortie_reelle)) + " (attendu EO-482 ;"
       " l item d un AUTRE est nomme plus haut)")
    ep("sans ligne d item, aucun identifiant n est INVENTE",
       module.item_de_sortie("  - EO-476 : un proche\nun resume\n") == "",
       "un identifiant est invente hors de la ligne d item")
    ep("sortie vide, aucun identifiant", module.item_de_sortie("") == "",
       "un identifiant est invente sur une sortie vide")

    # 4. LA CHAINE ENTIERE, dans un BAC A SABLE jetable (aucune trace dans la Matrice).
    bac = _Chemin(tempfile.mkdtemp(prefix="maillon68-"))
    sauve_chemins = (module.CHEMIN_CANAL, module.CHEMIN_JOURNAL,
                     module.CHEMIN_ENTONNOIR_MAIN)
    try:
        canal_cobaye = bac / "canal.md"
        canal_cobaye.write_text(
            "---\nidentite:\n  type: passerelle\n---\n\n# head cobaye\n\n"
            "##A-FAIRE################################\n##FAIT###################################\n"
            "##A-CONTROLER############################\n"
            "[question] une demande cobaye a extraire\npourquoi : prouver la chaine.\n\n"
            "##FAIT###################################\n##A-CONTROLER############################\n"
            "##CERTIFIER##############################\n"
            "[audit] une demande cobaye deja servie -- elle ne doit PAS bouger\n"
            "doit rester.\n", encoding="utf-8", newline="\n")
        faux = bac / "faux-entonnoir.py"
        faux.write_text(
            "print('ATTENTION DOUBLON POSSIBLE (1 item(s) proche(s)) :')\n"
            "print('  - EO-476 : un item PROCHExx [communs : fichiers]')\n"
            "print('Mission EO-999 deposee au vrac (urgence normale, source operateur)')\n",
            encoding="utf-8", newline="\n")
        muet = bac / "faux-entonnoir-muet.py"
        muet.write_text("print('aucune ligne d item ici')\n", encoding="utf-8", newline="\n")
        journal = bac / "archives" / "journal.md"

        module.CHEMIN_CANAL = canal_cobaye
        module.CHEMIN_JOURNAL = journal
        module.CHEMIN_ENTONNOIR_MAIN = faux
        depart = canal_cobaye.read_text(encoding="utf-8")

        # 4a. DRY : RIEN n est ecrit, et la porte le DIT.
        tampon = io.StringIO()
        with contextlib.redirect_stdout(tampon):
            code_dry = module.extraire(["--rang", "1"])
        ep("extraire SANS --appliquer n ecrit RIEN",
           code_dry == 0 and canal_cobaye.read_text(encoding="utf-8") == depart
           and not journal.exists(),
           "le DRY a ecrit quelque chose (code " + str(code_dry) + ")")
        ep("le DRY se DIT", "DRY" in tampon.getvalue(), "le DRY ne le dit pas")

        # 4b. APPLIQUER : item journalise sous l id de la PORTE, mots du user
        #     conserves, demande servie retiree, voisine INTACTE, doute DIT.
        tampon = io.StringIO()
        with contextlib.redirect_stdout(tampon):
            code_applique = module.extraire(["--rang", "1", "--appliquer"])
        dit = tampon.getvalue()
        texte_journal = journal.read_text(encoding="utf-8") if journal.is_file() else ""
        apres = canal_cobaye.read_text(encoding="utf-8")
        ep("l extraction aboutit", code_applique == 0, "code " + str(code_applique))
        ep("le journal NOMME l item de la PORTE", "EO-999" in texte_journal,
           "le journal ne porte pas EO-999")
        ep("le journal NE POINTE PAS l item d un AUTRE", "EO-476" not in texte_journal,
           "le journal pointe EO-476 : l id a ete pris au verdict de doublon")
        ep("les MOTS du user sont au journal",
           "une demande cobaye a extraire" in texte_journal,
           "les mots du user ne sont pas au journal")
        ep("la demande servie QUITTE le canal",
           "demande cobaye a extraire" not in apres, "la demande servie est restee")
        ep("la demande NON servie est INTACTE", "doit rester" in apres,
           "le retrait a emporte un voisin")
        ep("le retrait est DIT", "item EO-999 depose" in dit,
           "la porte ne dit pas l item retenu")
        ep("le DOUTE de l entonnoir est DIT", "DOUBLON POSSIBLE" in dit,
           "la porte avale le verdict de doublon")

        # 4c. SANS ITEM : la demande NE QUITTE PAS le canal, et l absence se DIT.
        canal_cobaye.write_text(depart, encoding="utf-8", newline="\n")
        journal_avant = journal.read_text(encoding="utf-8")
        module.CHEMIN_ENTONNOIR_MAIN = muet
        tampon = io.StringIO()
        with contextlib.redirect_stdout(tampon):
            module.extraire(["--rang", "1", "--appliquer"])
        ep("sans ligne d item, RIEN ne quitte le canal",
           canal_cobaye.read_text(encoding="utf-8") == depart
           and journal.read_text(encoding="utf-8") == journal_avant,
           "le canal ou le journal a bouge sans item depose")
        ep("l absence d item se DIT", "AUCUNE ligne d item" in tampon.getvalue(),
           "la porte ne dit pas que sa sortie ne portait aucun item")

        # 4d. LES ETATS SE SUIVENT : une demande deja servie ne s extrait pas.
        tampon = io.StringIO()
        with contextlib.redirect_stdout(tampon):
            code_fait = module.extraire(["--rang", "2"])
        ep("une demande deja servie ne s extrait pas", code_fait == 2,
           "code " + str(code_fait) + " sur une demande qui n est pas a extraire")
        ep("le refus d etat se DIT", "ne se saute pas" in tampon.getvalue(),
           "le refus ne dit pas pourquoi")
        ep("le refus d etat se DIT", "ne se saute pas" in tampon.getvalue(),
           "le refus ne dit pas pourquoi")

        # 4e. LES FINS DE LIGNE DU USER (exigence 4) : elles ne se TRADUISENT pas.
        #     Mesure qui fonde ce controle : un canal cobaye en CRLF (18 fins)
        #     ressortait en LF (0 fin CRLF) -- le fichier ENTIER reecrit pour UNE
        #     demande retiree, donc une diff de tout le fichier chez le user.
        for etiquette, fin in (("LF", "\n"), ("CRLF", "\r\n")):
            canal_cobaye.write_bytes(depart.replace("\n", fin).encode("utf-8"))
            module.CHEMIN_ENTONNOIR_MAIN = faux
            depart_octets = canal_cobaye.read_bytes()
            tampon = io.StringIO()
            with contextlib.redirect_stdout(tampon):
                module.extraire(["--rang", "1", "--appliquer"])
            restes = canal_cobaye.read_bytes()
            texte_restant = restes.decode("utf-8")
            if fin == "\r\n":
                ep("un canal CRLF reste ENTIEREMENT en CRLF",
                   restes.count(b"\r\n") == restes.count(b"\n")
                   and restes.count(b"\r\n") < depart_octets.count(b"\r\n"),
                   "le canal a ete TRADUIT : " + str(restes.count(b"\n")
                   - restes.count(b"\r\n")) + " fin(s) LF seule(s)")
            else:
                ep("un canal LF reste ENTIEREMENT en LF", restes.count(b"\r") == 0,
                   "le canal LF a recu " + str(restes.count(b"\r")) + " CR")
            ep("le retrait tient dans un canal " + etiquette,
               "demande cobaye a extraire" not in texte_restant
               and "doit rester" in texte_restant,
               "le retrait a mal vise dans un canal " + etiquette)

        # 4f. CE QU ELLE NE SAIT PAS, ELLE LE DIT (exigence 3) : un mot d etat
        #     inconnu et un bloc de patternes SANS demande sont SIGNALES, jamais
        #     avales en silence.
        canal_cobaye.write_text(
            "---\nidentite:\n  type: passerelle\n---\n\n# head cobaye\n\n"
            "##A-FAIRE################################\n##FAIT###################################\n"
            "##A-CONTROLER############################\n"
            "[question] une demande bien formee\n\n"
            "##INCONNU################################\n"
            "[audit] une demande au mot d etat INCONNU\n\n"
            "##FAIT###################################\n##A-CONTROLER############################\n"
            "##CERTIFIER##############################\n\n"
            "##A-FAIRE################################\n##FAIT###################################\n"
            "##A-CONTROLER############################\n"
            "[mission] la derniere demande\n",
            encoding="utf-8", newline="\n")
        tampon = io.StringIO()
        with contextlib.redirect_stdout(tampon):
            module.extraire(["--rang", "1"])
        vu = tampon.getvalue()
        ep("un mot d etat INCONNU est DIT", "INCONNU" in vu,
           "la porte avale un mot d etat inconnu")
        ep("un bloc SANS demande est DIT", "SANS demande" in vu,
           "la porte avale un bloc de patternes vide")
    finally:
        (module.CHEMIN_CANAL, module.CHEMIN_JOURNAL,
         module.CHEMIN_ENTONNOIR_MAIN) = sauve_chemins
        shutil.rmtree(bac, ignore_errors=True)

    # 5. LA MESURE REELLE : le canal du user est LU, et RIEN n est ecrit.
    avant = empreinte(chemins["canal"])
    lecture = lancer_enfant([sys.executable, str(chemins["pilote"]), "passerelle", "lire"],
                            capture_output=True, text=True)
    ep("le canal du user est LU", lecture.returncode == 0,
       "code " + str(lecture.returncode) + " : " + (lecture.stdout or "")[:120])
    ep("la lecture DIT le canal et ses demandes",
       "CANAL :" in lecture.stdout and "demandes :" in lecture.stdout,
       "la lecture ne dit pas le canal : " + (lecture.stdout or "").strip()[:120])
    ep("une LECTURE n ecrit RIEN", empreinte(chemins["canal"]) == avant,
       "le canal a bouge pendant une LECTURE")
    refus = lancer_enfant([sys.executable, str(chemins["pilote"]), "passerelle", "extraire",
                           "--rang", "99", "--appliquer"],
                          capture_output=True, text=True)
    ep("un rang hors bornes est REFUSE", refus.returncode == 2,
       "code " + str(refus.returncode))
    ep("un refus n ecrit RIEN", empreinte(chemins["canal"]) == avant,
       "le canal a bouge sur un refus")

    return ecarts


def _eprouver_passerelle_user(racine):
    """MAILLON 66 (MO-492 / EO-452) : la PASSERELLE USER est HORS JUGEMENT, et les
    instruments la lisent au MEME domicile.

    LA MESURE QUI FONDE CE MAILLON (2026-09-29). `garde-ascii` rendait code 1 sur
    `user-demandes/user-demandes.md` et sur `user-demandes/le-vivier/le-vivier.md`
    alors que le createur avait DECLARE ce canal hors jugement (MO-475) : la decision
    etait ecrite DANS UN SEUL instrument (`controle-attribution.py`, constante
    `DOSSIER_DEMANDES_OPERATEUR`), donc les autres ne la voyaient pas -- et ce canal
    est la PASSERELLE ou le user ecrit ses demandes EN CLAIR, que la Matrice suit et
    EXTRAIT. C est la famille exacte que MO-377 avait fermee pour `docs/` : deux
    instruments, une seule decision, deux verdicts.

    L ORDRE, comme partout : le DOMICILE (une declaration, des consommateurs), le
    JUGEMENT joue sur des cas fabriques, le CABLAGE (les deux instruments
    CONSOMMENT, aucun ne recopie), la REGLE (l exception est ECRITE la ou elle fait
    foi), puis la MESURE REELLE (le garde EXECUTE : code 0 et exemption DITE sur la
    passerelle, ACCUSATION sur un vrai non-ASCII hors zone).
    """
    import importlib.util
    from pathlib import Path as _Chemin

    # Le chemin d un script se resout contre le cwd de l ENFANT : on RESOUT (mesure du
    # maillon 64 -- un chemin relatif lance d ailleurs ne trouve plus rien).
    racine = _Chemin(racine).resolve()
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    commun = matrice / "matrice" / "data" / "commun"
    outils = matrice / "_operateur" / "optimus-prime" / "super-combos" / "combos" / "outils"
    chemins = {
        "domicile": commun / "passerelle_user.py",
        "garde": outils / "garde-ascii.py",
        "attribution": outils / "controle-attribution.py",
        "cobayes": commun / "cobayes_jetables.py",
        "regle": matrice / "_operateur" / "optimus-prime" / "regles-immuables" / "ascii-strict.md",
    }
    manquants = [cle for cle in sorted(chemins) if not chemins[cle].is_file()]
    if manquants:
        return ["fichier INTROUVABLE : " + ", ".join(manquants)]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    def charger(nom, chemin):
        """Le module charge PAR SON CHEMIN, ses voisins ecartes (motif des maillons 61/64).

        Un nom NU (`cible`, `racine`) prendrait celui d un AUTRE outil deja en cache :
        on les ecarte le temps du chargement, et on les REMET ensuite -- ni chemin
        laisse, ni module en cache.
        """
        glissants = ("cible", "racine", "passerelle_user", "zone_sources", "cobayes_jetables")
        sauve = {}
        for glissant in glissants:
            if glissant in sys.modules:
                sauve[glissant] = sys.modules.pop(glissant)
        sys.path.insert(0, str(commun))
        try:
            specification = importlib.util.spec_from_file_location(nom, str(chemin))
            module = importlib.util.module_from_spec(specification)
            specification.loader.exec_module(module)
            return module, None
        except Exception as erreur:  # noqa: BLE001
            return None, (nom + " ILLISIBLE (" + type(erreur).__name__
                          + " : " + str(erreur)[:60] + ")")
        finally:
            sys.path.remove(str(commun))
            for glissant in glissants:
                sys.modules.pop(glissant, None)
            sys.modules.update(sauve)

    # 1. LE DOMICILE : une declaration, et elle DIT son role et sa raison.
    module, erreur = charger("passerelle_epreuve", chemins["domicile"])
    if erreur:
        return [erreur]
    ep("le domicile DECLARE le nom de la passerelle",
       getattr(module, "NOM_PASSERELLE_USER", "") == "user-demandes",
       "NOM_PASSERELLE_USER = " + repr(getattr(module, "NOM_PASSERELLE_USER", None)))
    motif = getattr(module, "MOTIF_PASSERELLE_USER", "")
    ep("le domicile porte un MOTIF", bool(motif), "MOTIF_PASSERELLE_USER vide")
    ep("le motif NOMME la decision du createur", "MO-475" in motif,
       "le motif ne cite pas MO-475 : " + motif[:80])
    ep("le motif DIT ce que la zone EST", "passerelle" in motif.lower(), motif[:80])

    # 2. LE JUGEMENT, joue sur des cas FABRIQUES : il mord, et il epargne.
    jugements = (
        ("user-demandes/user-demandes.md", True),
        ("user-demandes/le-vivier/le-vivier.md", True),
        ("matrice/data/user-demandes/homonyme.md", False),
        ("matrice/user-demandes/homonyme.md", False),
        ("matrice/data/commun/cible.py", False),
    )
    for chemin, attendu in jugements:
        verdict = module.est_passerelle_user(chemin)
        ep("jugement " + chemin, verdict is attendu,
           "rendu " + str(verdict) + " pour un attendu " + str(attendu))

    # 3. LE CABLAGE : les DEUX instruments consomment le domicile, aucun ne le recopie.
    texte_garde = _lire_si_present(chemins["garde"])
    texte_attribution = _lire_si_present(chemins["attribution"])
    ep("garde-ascii CONSOMME le domicile", "from passerelle_user import" in texte_garde,
       "garde-ascii n importe pas passerelle_user")
    ep("garde-ascii ne RECOPIE pas le nom", '"user-demandes"' not in texte_garde,
       "garde-ascii redit le nom en dur : deux declarations divergeraient (M-076)")
    ep("garde-ascii DIT ce qu il met de cote",
       "HORS CHAMP" in texte_garde and "mis de cote" in texte_garde,
       "garde-ascii ne DIT plus son exemption : un angle mort muet (L-104)")
    ep("l attribution CONSOMME le predicat", "est_passerelle_user(" in texte_attribution,
       "controle-attribution ne consomme pas le predicat du domicile")
    ep("l attribution ne DECLARE plus la constante",
       "DOSSIER_DEMANDES_OPERATEUR = " not in texte_attribution,
       "la declaration survit dans le garde : deux domiciles pour une decision")

    # 4. LA REGLE : l exception est ECRITE la ou elle fait foi (c est elle qui fait foi).
    texte_regle = _lire_si_present(chemins["regle"])
    ep("la regle ECRIT l exception", "user-demandes/" in texte_regle,
       "la regle ASCII ne nomme pas la passerelle")
    ep("la regle NOMME le domicile", "passerelle_user.py" in texte_regle,
       "la regle ne dit pas ou vit la declaration")

    # 5. LA MESURE REELLE : le garde EXECUTE, sur la passerelle ET sur la Matrice.
    def jouer(cible):
        return lancer_enfant([sys.executable, str(chemins["garde"]), str(cible)],
                             capture_output=True, text=True)

    passe = jouer(matrice / "user-demandes")
    ep("la passerelle est HORS CHAMP (code 0)", passe.returncode == 0,
       "code " + str(passe.returncode) + " : " + passe.stdout.strip()[:160])
    ep("l exemption est DITE", "HORS CHAMP" in passe.stdout, passe.stdout.strip()[:160])

    entier = jouer(matrice)
    ep("le compte des zones est DIT", "fichier(s) mis de cote" in entier.stdout,
       "le verdict ne DIT pas ce qu il met de cote")
    # SUR LA MATRICE ENTIERE le verdict n est PAS exige vert : le cobaye non-ASCII d un
    # round vit dans la zone jetable -- c est une VRAIE violation (le garde a raison de
    # la nommer), et l exiger verte ferait un controle dont l etat normal est ROUGE
    # (R-008 / MO-487 : un controle rouge par construction apprend a l ignorer). Le
    # critere juste est CIBLE : la passerelle n apparait JAMAIS parmi les ACCUSES.
    accuses = entier.stdout.split("HORS CHAMP")[0]
    ep("aucun fichier de la passerelle n est accuse", "user-demandes" not in accuses,
       "la passerelle est accusee : " + accuses.strip()[-200:])

    # CONTRE-TEMOIN : un VRAI non-ASCII HORS zone declaree reste ACCUSE -- sans lui, ce
    # maillon prouverait seulement qu un garde peut se taire.
    cobayes, erreur = charger("cobayes_epreuve", chemins["cobayes"])
    if erreur:
        return ecarts + [erreur]
    with cobayes.fixtures("cobaye-mo492-") as dossier:
        faux = dossier / "vraie-violation.md"
        faux.write_bytes("accent volontaire: \u00e9\n".encode("utf-8"))
        accuse = jouer(faux)
        ep("un VRAI non-ASCII hors zone est ACCUSE (code 1)", accuse.returncode == 1,
           "code " + str(accuse.returncode) + " : " + accuse.stdout.strip()[:160])
        ep("la violation est NOMMEE", "vraie-violation.md" in accuse.stdout,
           accuse.stdout.strip()[:160])

    return ecarts


# Les faits attendus du SOCLE de la passerelle (maillon 67) : ce que le HEAD porte,
# la ligne du user qui prouve qu il n a pas ete REMPLACE, et les pieces du dossier.
TYPE_PASSERELLE = "passerelle"
TITRE_HEAD_PASSERELLE = "# PASSERELLE USER"
MARQUE_SPEC_USER = "# Ce document doit servir de passerelle"
PIECES_SOCLE_PASSERELLE = ("README.md", "template-demande.md")
MARQUE_DEMANDE = "##A-FAIRE#"


def _a_le_head(texte):
    """True si <texte> ouvre sur le HEAD : carte d identite + mode d emploi.

    PURE (aucun fichier) : c est ce qui rend le jugement JOUABLE sur des textes
    fabriques -- un cobaye qui ne peut pas dire non ne prouve rien.
    """
    debut = texte.lstrip()
    return (debut.startswith("---") and ("type: " + TYPE_PASSERELLE) in texte
            and TITRE_HEAD_PASSERELLE in texte)


def _garde_la_spec_du_user(texte):
    """True si la SPEC du user est toujours la : le HEAD s AJOUTE, il ne remplace rien."""
    return MARQUE_SPEC_USER in texte


def _eprouver_socle_passerelle(racine):
    """MAILLON 67 (MO-504 / EO-481) : la PASSERELLE USER a son SOCLE -- un HEAD qui
    la declare, un README de dossier, un TEMPLATE de delimiteurs -- et les MOTS DU
    USER sont INTACTS.

    LA DEMANDE (createur, 2026-09-29) : < donner a la passerelle son readme, son head
    et son template de delimiteurs >. Le socle est ecrit par la Matrice, en ASCII ;
    le canal (`user-demandes.md`) porte les mots du user, qui ne sont JAMAIS
    reecrits : le HEAD s AJOUTE en tete, la spec d origine reste dessous.

    LES JUGEMENTS (purs, jouables sur des textes fabriques) : un texte qui PORTE le
    head est reconnu ; un texte qui ne le porte pas est ACCUSE et la raison est
    NOMMEE ; un canal qui aurait perdu la spec du user est ACCUSE (le head n a pas
    le droit de remplacer ses mots). Puis la MESURE REELLE : le type `passerelle`
    est DECLARE au vocabulaire ferme (lu par AST chez son domicile), les trois
    pieces existent et sont ASCII, et le canal porte toujours la premiere ligne du
    user ET au moins une demande delimitee.
    """
    import importlib.util
    from pathlib import Path as _Chemin

    racine = _Chemin(racine).resolve()
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    commun = matrice / "matrice" / "data" / "commun"
    passerelle = matrice / "user-demandes"
    chemins = {
        "canal": passerelle / "user-demandes.md",
        "domicile-types": commun / "carte_identite.py",
        "cobayes": commun / "cobayes_jetables.py",
    }
    for piece in PIECES_SOCLE_PASSERELLE:
        chemins[piece] = passerelle / piece
    manquants = [cle for cle in sorted(chemins) if not chemins[cle].is_file()]
    if manquants:
        return ["fichier INTROUVABLE : " + ", ".join(manquants)]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    def charger(nom, chemin):
        glissants = ("cible", "racine", "cobayes_jetables")
        sauve = {}
        for glissant in glissants:
            if glissant in sys.modules:
                sauve[glissant] = sys.modules.pop(glissant)
        sys.path.insert(0, str(commun))
        try:
            specification = importlib.util.spec_from_file_location(nom, str(chemin))
            module = importlib.util.module_from_spec(specification)
            specification.loader.exec_module(module)
            return module, None
        except Exception as erreur:  # noqa: BLE001
            return None, (nom + " ILLISIBLE (" + type(erreur).__name__
                          + " : " + str(erreur)[:60] + ")")
        finally:
            sys.path.remove(str(commun))
            for glissant in glissants:
                sys.modules.pop(glissant, None)
            sys.modules.update(sauve)

    # 1. LES JUGEMENTS, sur des textes FABRIQUES : ils mordent, et ils epargnent.
    head_complet = ("---\nidentite:\n  type: " + TYPE_PASSERELLE
                    + "\n  appartient_a: x\n  commun: false\n---\n\n"
                    + TITRE_HEAD_PASSERELLE + " -- x\n\n" + MARQUE_SPEC_USER + "\n")
    ep("un canal QUI PORTE le head est reconnu", _a_le_head(head_complet) is True,
       "le jugement refuse un head complet")
    ep("un canal SANS head est ACCUSE",
       _a_le_head(MARQUE_DEMANDE + "\n[mission] faire ceci\n") is False,
       "le jugement accepte un canal sans head")
    ep("un head d un AUTRE type est ACCUSE",
       _a_le_head(head_complet.replace("type: " + TYPE_PASSERELLE, "type: readme")) is False,
       "le jugement accepte une carte d un autre type")
    ep("un canal qui A PERDU la spec du user est ACCUSE",
       _garde_la_spec_du_user(head_complet.replace(MARQUE_SPEC_USER, "x")) is False,
       "le head a remplace les mots du user sans que rien ne morde")
    ep("le canal reel GARDE la spec du user",
       _garde_la_spec_du_user(_lire_si_present(chemins["canal"])) is True,
       "la spec du user a disparu du canal")

    # 2. LA MESURE REELLE : le head est en TETE, et les trois pieces sont la.
    texte = _lire_si_present(chemins["canal"])
    ep("le canal OUVRE sur son head", _a_le_head(texte) is True,
       "le head n est pas en tete du canal : " + texte.strip()[:80])
    ep("le canal PORTE une demande delimitee", MARQUE_DEMANDE in texte,
       "aucune demande delimitee dans le canal")
    for piece in PIECES_SOCLE_PASSERELLE:
        brut = chemins[piece].read_bytes()
        ep("le socle est ASCII (" + piece + ")",
           all(octet < 128 for octet in brut),
           piece + " porte du non-ASCII : la Matrice ecrit en ASCII")

    # 3. LE TYPE, DECLARE au vocabulaire ferme (lu par AST chez son domicile : aucun
    #    import du domicile, la SOURCE fait foi).
    cobayes, erreur = charger("cobayes_socle", chemins["cobayes"])
    if erreur:
        return ecarts + [erreur]
    table = cobayes.litteraux(chemins["domicile-types"])
    types = table.get("TYPES_RECONNUS", (None,))[0]
    ep("le type `" + TYPE_PASSERELLE + "` est DECLARE au vocabulaire",
       isinstance(types, tuple) and TYPE_PASSERELLE in types,
       "types lus : " + str(types)[:120])

    return ecarts


def _eprouver_rendre_graphe(racine):
    """MAILLON 69 (MO-493 / EO-449) : COMPOSER EN MERMAID, CONVERTIR EN SVG.

    Demande du createur : transformer N IMPORTE QUOI en MERMAID puis en SVG, pour
    que l agent lise le MERMAID et que le createur lise le SVG -- et que les
    incoherences cachees dans les parcours et le vivier deviennent VISIBLES.

    CE QU IL EPROUVE, et pourquoi chacun :
      - LA CHAINE ENTIERE sur la donnee REELLE (source -> mermaid -> svg) : le
        texte porte `flowchart TD`, l image s OUVRE (ElementTree) -- une image
        qu aucun lecteur XML ne peut ouvrir n est pas une image ;
      - LE DRAPEAU DECLARE DEUX FOIS : c est le piege TOMBE ce round -- un drapeau
        qui n est QUE dans la liste des drapeaux n est jamais RECONNU, et
        `--appliquer` etait alors REFUSE comme une option inconnue (le depot de la
        vue ne pouvait pas aboutir). Le controle lit les DEUX listes ;
      - LE MORDANT, sur des donnees FABRIQUEES (index a fichier absent et a nom
        double, vivier a id et categorie hors liste) : un juge qui n accuse pas
        n est pas un juge. AUCUN compte de la donnee VIVANTE n est fige ici :
        exiger "le parcours reel a N incoherences" rendrait rouge le jour ou le
        createur les repare (famille R-008, defaut deja paye au maillon 66) ;
      - LE RENDU DETERMINISTE et le CYCLE : meme texte -> memes octets, et un
        cycle ne boucle pas ;
      - LES VUES LIVREES : ASCII, et les `.svg` s ouvrent.
    """
    import importlib
    import re
    import sys as _sys
    from pathlib import Path as _Chemin
    from xml.etree import ElementTree as _XML

    racine = _Chemin(racine).resolve()
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    outil = matrice / "matrice" / "data" / "outils" / "rendre-graphe"
    chemins = {
        "main": outil / "main.py",
        "description": outil / "DESCRIPTION.md",
        "entry-mermaid": outil / "mermaid" / "entry.py",
        "entry-svg": outil / "svg" / "entry.py",
        "fonctions-svg": outil / "svg" / "fonctions.py",
        "fonctions-verifier": outil / "verifier" / "fonctions.py",
        "vues-mermaid": matrice / "_operateur" / "optimus-prime" / "vues" / "mermaid",
        "vues-svg": matrice / "_operateur" / "optimus-prime" / "vues" / "svg",
    }
    manquants = [cle for cle in sorted(chemins) if not chemins[cle].exists()]
    if manquants:
        return ["INTROUVABLE : " + ", ".join(manquants)]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    # 1. LE ROUTAGE et la FACADE : trois verbes, et le DRY est DIT.
    texte_main = chemins["main"].read_text(encoding="utf-8", errors="replace")
    for verbe in ("mermaid", "svg", "verifier"):
        ep("le point d entree ROUTE " + verbe, '"' + verbe + '":' in texte_main,
           "main.py ne route pas " + verbe)
    texte_description = chemins["description"].read_text(encoding="utf-8", errors="replace")
    ep("la facade DECLARE ses trois verbes",
       all(verbe in texte_description for verbe in ("mermaid", "svg", "verifier")),
       "DESCRIPTION.md ne declare pas ses verbes")
    ep("la facade DIT le DRY par defaut", "DRY PAR DEFAUT" in texte_description,
       "DESCRIPTION.md ne dit pas que rien ne s ecrit sans --appliquer")

    # 2. LE DRAPEAU, dans les DEUX listes (piege mesure ce round : un drapeau qui
    #    n est que dans les drapeaux est REFUSE comme une option inconnue).
    for nom_entree in ("entry-mermaid", "entry-svg"):
        texte_entree = chemins[nom_entree].read_text(encoding="utf-8", errors="replace")
        # LA DECLARATION se lit par un MOTIF (jamais par un filtre de lignes : un
        # filtre sur la sortie d un garde doit correspondre a un PRODUCTEUR
        # imprime -- `verifier-extraction-ecarts.py` a raison de l exiger, et une
        # lecture de SOURCE n est pas une lecture de sortie).
        declaration = re.search(r"^NOMS_OPTIONS = \(([^)]*)\)", texte_entree, re.M)
        ep("le drapeau appliquer est un NOM CONNU (" + nom_entree + ")",
           declaration is not None and "appliquer" in declaration.group(1),
           "NOMS_OPTIONS ne porte pas appliquer : --appliquer serait REFUSE")
        ep("le drapeau appliquer est DECLARE (" + nom_entree + ")",
           'DRAPEAUX = ("appliquer",)' in texte_entree,
           "DRAPEAUX ne declare pas appliquer")

    # 3. LES FONCTIONS, chargees a LEUR chemin (motif 61/64/68 : les noms glissants
    #    `constants`, `commun`, `cible`, `svg` sont ecartes avant, jamais laisses
    #    en memoire -- deux outils du meme nom se voleraient leur module).
    glissants = ("constants", "commun", "cible", "carte_ascii", "options",
                 "lancement", "racine", "svg", "svg.fonctions", "mermaid",
                 "mermaid.fonctions", "mermaid.entry", "verifier",
                 "verifier.fonctions")
    sauve = {}
    for glissant in glissants:
        if glissant in _sys.modules:
            sauve[glissant] = _sys.modules.pop(glissant)
    _sys.path.insert(0, str(matrice / "matrice" / "data" / "commun"))
    _sys.path.insert(0, str(outil))
    try:
        fonctions_svg = importlib.import_module("svg.fonctions")
        fonctions_verifier = importlib.import_module("verifier.fonctions")
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["l outil est ILLISIBLE (" + type(erreur).__name__ + " : "
                         + str(erreur)[:100] + ")"]
    finally:
        _sys.path.remove(str(outil))
        _sys.path.remove(str(matrice / "matrice" / "data" / "commun"))
        for glissant, module in sauve.items():
            _sys.modules[glissant] = module

    # 4. LE MORDANT : le juge ACCUSE ce qui est casse (donnees fabriquees).
    codes_index = [i["code"] for i in
                   fonctions_verifier.juger_index({"parcours": [
                       {"theme": "AAA", "ordre": 1,
                        "fichier": "themes/theme-absent-du-disque.json"},
                       {"theme": "AAA", "ordre": 2,
                        "fichier": "themes/theme-absent-du-disque.json"},
                   ]})[0]]
    ep("l index COBAYE est accuse (fichier absent + nom double)",
       "fichier-absent" in codes_index and "nom-double" in codes_index,
       "codes rendus : " + str(sorted(set(codes_index))[:6]))
    ep("un index qui liste TOUS les themes du disque n est PAS accuse d orphelin",
       all(code != "theme-orphelin" for code in fonctions_verifier.juger_index(
           {"parcours": [
               {"theme": c.stem.replace("theme-", "").upper(), "ordre": r,
                "fichier": "themes/" + c.name}
               for r, c in enumerate(sorted(
                   (matrice / "_operateur" / "optimus-prime" / "parcours" / "themes")
                   .glob("theme-*.json")), 1)]})[0]),
       "un theme pourtant liste est accuse d orphelin")
    codes_vivier = [i["code"] for i in fonctions_verifier.incoherences_vivier(
        {"themes": [
            {"id": "XX-1", "nom": "DOUBLE", "categorie": "SYSTEME", "but": "un but"},
            {"id": "TH-002", "nom": "DOUBLE", "categorie": "HORS-LISTE", "but": "un but"},
            {"id": "TH-003", "nom": "SANS-BUT", "categorie": "SYSTEME", "but": "  "},
        ]}, ("SYSTEME", "PERSONNALITE", "QUESTION", "GOUVERNANCE"))[0]]
    ep("le vivier COBAYE est accuse (id, categorie, nom double, but vide)",
       set(codes_vivier) >= {"id-invalide", "categorie-inconnue", "nom-double", "but-vide"},
       "codes rendus : " + str(sorted(set(codes_vivier))[:6]))
    renvoi_casse = fonctions_verifier.resoudre_renvoi(
        {"type": "theme", "fichier": "theme-reprise-mission.json",
         "case": "case-qui-nexiste-pas"})
    ep("un renvoi vers une CASE introuvable est ACCUSE",
       renvoi_casse.get("resolu") is False, "le renvoi a ete declare resolvable")
    ep("le renvoi vers un fichier ABSENT nomme le fichier",
       "n existe pas" in fonctions_verifier.resoudre_renvoi(
           {"type": "protocole", "fichier": "protocoles/nexiste-pas.md"})["motif"],
       "le motif ne nomme pas le fichier cite")

    # 5. LE RENDU : deterministe, un cycle ne boucle pas, les formes se LISENT.
    brut = ('flowchart TD\n    A["Source"] --> B{"Choix"}\n'
            '    B -- "oui" --> C([Vue])\n    B -- "non" --> D[[INCOHERENCE]]\n')
    premier = fonctions_svg.rendre_svg(brut, "t", "s")
    ep("meme texte -> memes octets", premier == fonctions_svg.rendre_svg(brut, "t", "s"),
       "deux rendus du meme texte ont donne des octets DIFFERENTS")
    try:
        _XML.fromstring(fonctions_svg.rendre_svg(
            'flowchart TD\n    A["A"] --> B["B"]\n    B --> A\n', "cycle", ""))
        valide = True
    except _XML.ParseError:
        valide = False
    ep("un CYCLE est rendu et l image s OUVRE", valide, "le SVG du cycle n est pas valide")
    noeuds, _index, _aretes = fonctions_svg.analyser_mmd(brut)
    formes = dict((element["label"], element["forme"]) for element in noeuds)
    ep("les quatre FORMES se lisent dans le texte",
       formes.get("Source") == "rect" and formes.get("Choix") == "diamond"
       and formes.get("Vue") == "stadium" and formes.get("INCOHERENCE") == "erreur",
       "formes lues : " + str(sorted(formes.items()))[:120])

    # 6. LA CHAINE REELLE, par la ligne de commande (lanceur officiel).
    lanceur = matrice / "lancer.py"
    etapes = (("mermaid", ["--source", "vivier"]), ("svg", ["--source", "vivier"]),
              ("mermaid", ["--source", "parcours"]), ("svg", ["--source", "parcours"]),
              ("verifier", ["--source", "vivier"]))
    for verbe, options in etapes:
        resultat = lancer_enfant([sys.executable, str(lanceur), "--appelant", "operateur",
                                  "rendre-graphe", verbe] + options,
                                 capture_output=True, text=True)
        sortie = resultat.stdout or ""
        if verbe == "verifier":
            # UN VERDICT, jamais un refus : 0 ou 1. Le code 2 serait un REFUS.
            ep("verifier " + options[1] + " rend un VERDICT (0 ou 1)",
               resultat.returncode in (0, 1),
               "code " + str(resultat.returncode) + " : " + sortie.strip()[:120])
            ep("le verdict de verifier NOMME sa source", "VERDICT :" in sortie,
               "la sortie ne porte pas de verdict")
            continue
        ep(verbe + " " + options[1] + " rend son texte (code 0)", resultat.returncode == 0,
           "code " + str(resultat.returncode) + " : " + sortie.strip()[:120])
        if verbe == "mermaid":
            ep("le MERMAID porte son en-tete de flux", "flowchart TD" in sortie,
               "le texte rendu n est pas un flowchart")
        else:
            debut = sortie.find("<?xml")
            fin = sortie.find("</svg>")
            ep("le SVG est PRESENT dans la sortie", debut >= 0 and fin > debut,
               "aucun document SVG rendu")
            if debut >= 0 and fin > debut:
                try:
                    _XML.fromstring(sortie[debut:fin + 6])
                    ouvrable = True
                except _XML.ParseError as erreur:
                    ouvrable = False
                    ecarts.append("le SVG rendu ne s OUVRE PAS -> " + str(erreur)[:100])
                ep("le SVG rendu s OUVRE (XML)", ouvrable, "document invalide")

    # 7. LES VUES LIVREES : ASCII, et les `.svg` s ouvrent.
    for dossier, suffixe in ((chemins["vues-mermaid"], ".mmd"), (chemins["vues-svg"], ".svg")):
        fichiers = sorted(c for c in dossier.glob("*" + suffixe) if c.is_file())
        ep("des vues " + suffixe + " sont LIVREES", bool(fichiers),
           "aucune vue " + suffixe + " dans " + str(dossier))
        for chemin in fichiers:
            octets = chemin.read_bytes()
            ep("la vue est ASCII : " + chemin.name,
               all(octet <= 127 for octet in octets),
               str(sum(1 for o in octets if o > 127)) + " octet(s) non-ASCII")
            if suffixe == ".svg":
                try:
                    _XML.fromstring(octets.decode("ascii"))
                    ok_xml = True
                except (_XML.ParseError, UnicodeDecodeError):
                    ok_xml = False
                ep("la vue s OUVRE : " + chemin.name, ok_xml, "document invalide")

    return ecarts


def _eprouver_recul_absorbee(racine):
    """MAILLON 70 (MO-494) : la FENETRE D ABSORPTION, mesuree AVANT d accuser.

    Le defaut mesure le 2026-09-27 : le lanceur a rendu KO sur
    `passe-absorbee-sur-le-service : 0 passe(s) sans fait absorbee(s)` alors que le
    service etait SAINT -- replay direct deux minutes plus tard : VERDICT OK, l etat
    ayant ete ECRIT a 07:52:22 pour une cadence declaree d environ 60 s. La suite
    jugeait un ETAT AU MOMENT DU BALAYAGE : entre la ligne servie et la passe
    suivante, `0` est NORMAL.

    LA CAUSE, et c est elle que ce maillon surveille : la decision existait deja,
    ecrite dans UN SEUL des deux gardes de la maison (`verifier-observations-non-
    redondantes.py`, MO-097) ; son voisin `verifier-historique-non-redondant.py`,
    qui juge la MEME propriete sur la MEME routine, l IGNORAIT -- et accusait a
    tort. Une decision ecrite dans l instrument qui la consomme n existe pas pour
    les autres (lecon L-211, meme famille que MO-492).

    CE QU IL EPROUVE :
      - UN SEUL DOMICILE : `recul_insuffisant` et `age_secondes` sont definis UNE
        fois, et les DEUX gardes les CONSOMMENT (aucune copie du critere) -- le
        balayage IGNORE la zone jetable, dont le nom est DECLARE par zone_tmp ;
      - LE COBAYE : (0 absorbe, etat FRAIS) -> EPARGNE ;
      - LE CONTRE-TEMOIN : (0 absorbe, etat ANCIEN) -> ACCUSE -- sans lui, le
        maillon serait vert par construction (lecon L-032) ;
      - LE FAIL-CLOSED : un age ou une cadence ILLISIBLE n accorde AUCUNE fenetre
        (un controle qui ne peut pas prouver se tait sur l epargne, jamais sur
        l ecart) ;
      - LES DEUX GARDES passent sur le service REEL (sous-processus, code 0).
    """
    import importlib
    import sys as _sys
    from pathlib import Path as _Chemin

    racine = _Chemin(racine).resolve()
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    outils = matrice / "_operateur" / "optimus-prime" / "super-combos" / "combos" / "outils"
    garde_historique = outils / "verifier-historique-non-redondant.py"
    garde_observations = outils / "verifier-observations-non-redondantes.py"
    domicile = matrice / "matrice" / "data" / "commun" / "etat_histoire.py"
    regle_zone = matrice / "matrice" / "data" / "commun" / "zone_tmp.py"

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    manquants = [chemin.name for chemin in (garde_historique, garde_observations, domicile,
                                            regle_zone) if not chemin.is_file()]
    if manquants:
        return ["INTROUVABLE : " + ", ".join(manquants)]

    # 1. LES DEUX DOMICILES, charges a LEUR chemin, leurs voisins ecartes (motif
    #    61/64/68/69). La DECISION (etat_histoire : la fenetre) et la REGLE DE NOM
    #    de la zone jetable (zone_tmp : `tmp-*`) sont CONSOMMEES, jamais recopiees.
    glissants = ("etat_histoire", "zone_tmp")
    sauve = {}
    for glissant in glissants:
        if glissant in _sys.modules:
            sauve[glissant] = _sys.modules.pop(glissant)
    _sys.path.insert(0, str(matrice / "matrice" / "data" / "commun"))
    try:
        etat_histoire = importlib.import_module("etat_histoire")
        zone_tmp = importlib.import_module("zone_tmp")
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["le domicile est ILLISIBLE (" + type(erreur).__name__ + " : "
                         + str(erreur)[:100] + ")"]
    finally:
        _sys.path.remove(str(matrice / "matrice" / "data" / "commun"))
        for glissant, module in sauve.items():
            _sys.modules[glissant] = module

    # 2. UN SEUL DOMICILE : la definition, et les deux CONSOMMATEURS.
    # LES AIGUILLES SE CONSTRUISENT (elles ne s ecrivent jamais en clair ici) : un
    # maillon qui porterait le texte `def <nom>(` se compterait LUI-MEME comme un
    # site de definition -- defaut deja paye au maillon 66, ou mon propre cobaye
    # faisait rougir mon propre controle.
    # LA ZONE JETABLE EST HORS JUGEMENT (prefixe DECLARE par zone_tmp) : mes propres
    # copies de travail y dorment pendant la mission ; les compter ferait accuser un
    # faux domicile (mesure du 2026-09-29 : `mo-494-lanceur-old.py` a fait rougir ce
    # maillon sur un fichier que la cloture supprime).
    fonctions = ("recul_insuffisant", "age_secondes", "battement_de_passes")
    textes = {}
    for chemin in sorted(matrice.rglob("*.py")):
        if "__pycache__" in chemin.parts or ".bak." in chemin.name \
                or any(part.startswith(zone_tmp.PREFIXE_ZONE) for part in chemin.parts):
            continue
        textes[chemin.name] = chemin.read_text(encoding="utf-8", errors="replace")
    for nom_fonction in fonctions:
        marque = "def " + nom_fonction + "("
        site = sorted(chemin for chemin, texte in textes.items() if marque in texte)
        ep("le domicile de " + nom_fonction + " est UNIQUE",
           site == ["etat_histoire.py"], "site(s) : " + str(site))
    for chemin in (garde_historique, garde_observations):
        texte = textes.get(chemin.name, "")
        for nom_fonction in fonctions:
            ep("le garde CONSOMME le domicile : " + nom_fonction + " dans " + chemin.name,
               nom_fonction + "(" in texte,
               "le garde n appelle pas " + nom_fonction)
            ep("le garde n a AUCUNE copie du critere : " + nom_fonction + " dans " + chemin.name,
               "def " + nom_fonction not in texte,
               "le critere est redefini dans le garde : la divergence reviendra")

    # 3. LE COBAYE ET LE CONTRE-TEMOIN, joues sur la DECISION PURE.
    cadence = 60
    epargne, motif_epargne = etat_histoire.recul_insuffisant(0, 5, cadence)
    ep("COBAYE -- 0 absorbe, etat FRAIS : EPARGNE",
       epargne is True and "recul-insuffisant" in motif_epargne,
       "rendu " + repr(epargne) + " / " + repr(motif_epargne[:80]))
    accuse, _ = etat_histoire.recul_insuffisant(0, 300, cadence)
    ep("CONTRE-TEMOIN -- 0 absorbe, etat ANCIEN : ACCUSE", accuse is False,
       "rendu " + repr(accuse) + " : un temoin fige serait epargne a tort")
    servi, _ = etat_histoire.recul_insuffisant(3, 5, cadence)
    ep("un temoin qui A absorbe n est jamais un ecart", servi is False,
       "rendu " + repr(servi))
    for age, nom_age in ((None, "age ILLISIBLE"), (5, "cadence ILLISIBLE")):
        cadence_essaie = cadence if age is None else None
        fenetre, motif = etat_histoire.recul_insuffisant(0, age, cadence_essaie)
        ep("FAIL-CLOSED -- " + nom_age + " : aucune fenetre accordee",
           fenetre is False and bool(motif),
           "rendu " + repr(fenetre) + " -- une epargne muette serait un faux vert")
    ep("l age d un horodatage ILLISIBLE rend None (jamais 0)",
       etat_histoire.age_secondes("pas une date") is None,
       "rendu " + repr(etat_histoire.age_secondes("pas une date")))

    # --- LA FENETRE SUR LE BATTEMENT MESURE (EO-559) --------------------------
    # LE DEFAUT MESURE : la cadence DECLAREE est une cadence de SOMMEIL. Sur
    # routeur-maintenance, 30 s declarees pour un battement median de 61 s : le
    # garde accusait une routine SAINE pendant environ 31 s sur 61. La serie
    # ci-dessous est FABRIQUEE (61 s de battement regulier) ; le service reel est
    # joue plus bas, par les deux gardes en sous-processus.
    serie_61 = ("2026-10-02 20:00:00", "2026-10-02 20:01:01", "2026-10-02 20:02:02",
                "2026-10-02 20:03:03", "2026-10-02 20:04:04")
    battement, motif_battement = etat_histoire.battement_de_passes(serie_61)
    ep("le battement median se LIT sur la serie publiee",
       battement == 61.0,
       "rendu " + repr(battement) + " -- la mesure ne se deduit pas de la cadence")
    # LE COBAYE : 45 s d age, cadence 30 s, battement 61 s -> le temoin doit etre
    # EPARNE. Avant la reparation, 45 >= 30 rendait une ACCUSATION sur un service
    # sain : c est le faux positif observe en direct.
    ouvert, motif_ouvert = etat_histoire.recul_insuffisant(0, 45, 30, battement)
    ep("COBAYE -- le battement MESURE ouvre la fenetre que la cadence fermait",
       ouvert is True and "MESURE" in motif_ouvert,
       "rendu " + repr(ouvert) + " / " + repr(motif_ouvert[:90]))
    # LE CONTRE-TEMOIN : au-dela du battement, la fenetre se REFERME. Sans lui,
    # une fenetre elargie sans borne epargnerait un service reellement arrete.
    referme, _ = etat_histoire.recul_insuffisant(0, 70, 30, battement)
    ep("CONTRE-TEMOIN -- au-dela du battement mesure, la fenetre se referme",
       referme is False,
       "rendu " + repr(referme) + " : un service arrete serait epargne a tort")
    # LE CONTRE-TEMOIN DU REPLI : un battement NON mesurable rend la main a la
    # cadence declaree. On ne COMPTE PAS les passes pour les attendre (doctrine
    # attente-ne-prouve-rien) : c est le repli, pas une attente.
    # L AGE EST CELUI DU COBAYE (45 s) : seule la MESURE change, donc l epreuve
    # DISCRIMINE -- avec un battement lisible elle epargne, sans elle elle accuse.
    # Le motif n est PAS exige ici, et c est voulu : sur une ACCUSATION la decision
    # rend un motif vide (rien a epargner n a besoin d etre explique). Le premier
    # jet exigeait "cadence declaree" dans ce motif et fut rouge pour cette raison
    # -- une preuve qui exige un texte sur un refus exige une chose qui n existe pas.
    sans_recul, motif_sans_recul = etat_histoire.battement_de_passes(serie_61[:1])
    repli, _motif_repli = etat_histoire.recul_insuffisant(0, 45, 30, sans_recul)
    ep("CONTRE-TEMOIN -- battement non mesure : la cadence declaree fait foi",
       sans_recul is None and repli is False,
       "battement " + repr(sans_recul) + " -> fenetre " + repr(repli)
       + " ; " + motif_sans_recul[:60])
    ep("CONTRE-TEMOIN -- et le meme age AVEC battement reste epargne",
       etat_histoire.recul_insuffisant(0, 45, 30, battement)[0] is True,
       "45 s : seule la mesure decide, l epreuve mord donc dans les deux sens")
    # LE CONTRE-TEMOIN DE L ELARGISSEMENT : un battement aberrant, plus PETIT que
    # la cadence declaree, ne doit pas RETRECIR la fenetre -- la cadence reste un
    # plancher. L AGE EST CHOISI ENTRE LES DEUX (10 s : plus grand que le
    # battement aberrant 5 s, plus petit que la cadence 30 s) : c est la seule
    # bande qui DISCRIMINE. Mesure du premier jet : l epreuve jouait a 45 s, ou la
    # fenetre correcte (30 s) et la fenetre fautive (5 s) rendent toutes deux
    # False -- elle etait VERTE DANS LES DEUX CAS, donc elle ne prouvait rien
    # (lecon L-132 : une preuve qui ne peut pas dire NON ne prouve rien).
    aberrant, motif_aberrant = etat_histoire.recul_insuffisant(0, 10, 30, 5)
    ep("CONTRE-TEMOIN -- un battement aberrant ne RETRECIT pas la fenetre",
       aberrant is True and "cadence declaree" in motif_aberrant,
       "rendu " + repr(aberrant) + " / " + repr(motif_aberrant[:70]))
    ep("CONTRE-TEMOIN -- et il ne la RETRECIT pas non plus (age sous les deux)",
       etat_histoire.recul_insuffisant(0, 3, 30, 5)[0] is True,
       "3 s : la fenetre reste ouverte, un battement aberrant ne la referme pas")
    ep("CONTRE-TEMOIN -- au-dela du plancher, la fenetre se referme quand meme",
       etat_histoire.recul_insuffisant(0, 31, 30, 5)[0] is False,
       "31 s : la cadence declaree reste le plancher, meme battement aberrant")

    # 4. LES DEUX GARDES, sur le SERVICE REEL (le meme critere, deux consommateurs).
    for chemin in (garde_historique, garde_observations):
        resultat = lancer_enfant([sys.executable, str(chemin), "--racine", str(racine)],
                                 capture_output=True, text=True)
        sortie = (resultat.stdout or "") + (resultat.stderr or "")
        ep("le garde passe sur le service reel : " + chemin.name,
           resultat.returncode == 0,
           "code " + str(resultat.returncode) + " : "
           + "; ".join(ligne.strip() for ligne in sortie.splitlines()
                        if ligne.strip().startswith("[KO"))[:160])
        # L EPARGNE SE DIT : un garde qui voit 0 absorbe SANS nommer la fenetre
        # serait un garde muet sur sa propre decision (L-055 : un epargne muet se
        # lit comme un vert de complaisance). Le controle ne peut donc PAS etre une
        # tautologie : il ne s applique QUE quand le garde voit 0 absorbe.
        ligne_fenetre = next((ligne for ligne in sortie.splitlines()
                              if "passe-absorbee-sur-le-service" in ligne), "")
        # LE COMPTE EST LU, JAMAIS CHERCHE COMME UNE SOUS-CHAINE : la ligne du garde
        # dit `860 passe(s) sans changement...`, qui CONTIENT `0 passe(s) sans` -- un
        # service ayant absorbes se lisait donc comme un 0, et le maillon accusait un
        # garde qui, lui, epargnait a juste titre (mesure du 2026-09-29 : 860 absorbes).
        detail = ligne_fenetre.strip()
        if detail.startswith("[OK]"):
            detail = detail[4:].strip()
        compte = detail.split("passe(s)")[0].strip() if "passe(s)" in detail else ""
        if compte == "0":
            ep("le garde DIT la fenetre quand il epargne : " + chemin.name,
               "recul-insuffisant" in ligne_fenetre,
               "0 absorbe mais AUCUN motif de fenetre : " + ligne_fenetre.strip()[:140])
    return ecarts


def _eprouver_perimetre_racine(racine):
    """MAILLON 71 (MO-495) : LE GARDE DU PERIMETRE VOIT LA RACINE.

    LE DEFAUT, MESURE (2026-09-27/29). Le walk du garde elaguait la branche qui mene
    au perimetre, PUIS faisait `continue` -- et ce `continue` sautait la boucle des
    FICHIERS du dossier courant. Or ce dossier, quand il est un ancetre du perimetre,
    c est la RACINE du workspace : ses fichiers n etaient donc JAMAIS juges, et
    l ALLOWLIST racine etait du CODE MORT (jamais atteinte). Mesure d avant
    reparation : un fichier cobaye pose a la RACINE rendait exit 0 (invisible), le
    MEME fichier dans `outils-llm/` etait accuse. Deuxieme defaut du meme elagage :
    le premier morceau du chemin vers le perimetre (`cerveau-projet`) etait retire de
    la descente, donc TOUT le cerveau v1/v2 -- ou la regle interdit d ecrire -- etait
    hors de vue.

    CE QU IL EPROUVE :
      - LE MORDANT, sur une RACINE FICTIVE (fixture jetable) : un fichier pose a la
        RACINE est ACCUSE et NOMME, et un fichier de la branche v1/v2
        (`cerveau-projet/agents/`) l est aussi -- c est exactement ce que les deux
        defauts cachaient ;
      - LES CONTRE-TEMOINS : le demarrage autorise par la PORTE n est jamais accuse ;
        le PERIMETRE (matrix/) ne l est jamais ; et un cobaye HORS FENETRE non plus
        (le garde juge des ECRITURES, pas un heritage) ;
      - LE FILET DE LA PORTE : sa sauvegarde `X.bak.<horodatage>` est EPARGNEE et
        NOMMEE (exemption visible), tandis qu une sauvegarde d un nom que la porte
        n autorise pas est ACCUSEE -- sans ce contre-temoin, l exemption serait un
        angle mort ;
      - LE FAIL-CLOSED, eprouve sur la DECISION PURE : sans motif lu, aucun filet
        n est reconnu, et sans declaration RIEN n est autorise a la racine ;
      - AUCUNE RECOPIE (M-076) : le garde CONSOMME la declaration de la porte ECRIRE
        (liste + motif du point de restauration) ; un garde qui les reecrirait en dur
        est ACCUSE ici, sinon la divergence reviendrait en silence (L-207/L-211).
    """
    import importlib.util
    import os
    import re as _re
    import shutil as _shutil
    import sys as _sys
    import tempfile
    from pathlib import Path as _Chemin

    racine = _Chemin(racine).resolve()
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    garde = (matrice / "_operateur" / "optimus-prime" / "super-combos" / "combos"
             / "outils" / "garde-perimetre-write.py")
    if not garde.is_file():
        return ["INTROUVABLE : " + garde.name]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    def charger_module(alias, chemin):
        specification = importlib.util.spec_from_file_location(alias, str(chemin))
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        return module

    # 1. LE GARDE SE CHARGE, et sa declaration VIENT DE LA PORTE (M-076).
    try:
        juge = charger_module("garde_perimetre_cobaye", garde)
    except Exception as erreur:  # noqa: BLE001
        return ecarts + ["le garde est ILLISIBLE (" + type(erreur).__name__ + " : "
                         + str(erreur)[:80] + ")"]
    allowlist, prefixes, motif = juge.charger_declaration_porte()
    ep("la declaration de la porte ECRIRE est LUE par le garde",
       bool(allowlist) and bool(prefixes) and motif is not None,
       "rendu " + repr((allowlist, prefixes)) + " / motif " + repr(motif is not None))
    texte = garde.read_text(encoding="utf-8", errors="replace")
    ep("le garde ne RECOPIE pas la liste de la porte",
       "ALLOWLIST = {" not in texte,
       "la liste des demarrages est recopiee en dur : deux instruments divergeront")
    ep("le garde ne RECOPIE pas le motif du point de restauration",
       _re.search(r"bak\.\d{8}", texte) is None,
       "le motif du filet est recopie en dur au lieu d etre lu a son domicile")

    # 2. LES DECISIONS PURES, dont le FAIL-CLOSED (aucune exemption muette).
    filet = "demarrer-optimus-prime.md.bak.20260927_091045"
    ep("sans motif lu, AUCUN filet n est reconnu",
       juge.est_filet_de_la_porte(filet, allowlist, prefixes, None) is False,
       "un filet est reconnu sans le motif de la porte : exemption muette")
    ep("le filet d un nom AUTORISE est reconnu",
       juge.est_filet_de_la_porte(filet, allowlist, prefixes, motif) is True,
       "le filet de la porte n est pas reconnu")
    ep("le filet d un nom INTERDIT n est PAS reconnu",
       juge.est_filet_de_la_porte("README.md.bak.20260927_091045",
                                  allowlist, prefixes, motif) is False,
       "une sauvegarde d un nom interdit est epargnee : l exemption est trop large")
    ep("sans declaration, RIEN n est autorise a la racine",
       juge.autorise_par_la_porte("AGENTS.md", (), ()) is False,
       "une exemption survit a l absence de declaration")

    # 3. LE MORDANT ET LES CONTRE-TEMOINS, sur une RACINE FICTIVE (jetable).
    temp_root = tempfile.mkdtemp(prefix="cobaye-mo495-")
    try:
        fictive = _Chemin(temp_root)
        (fictive / "cerveau-projet" / "matrix" / "matrice" / "data").mkdir(parents=True)
        poses = (
            ("cerveau-projet/matrix/matrice/data/dedans.py", 0.0),
            ("cerveau-projet/matrix/matrice/data/dedans-frais.py", 0.0),
            ("cobaye-racine.md", 0.0),
            ("demarrer-optimus-prime.md", 0.0),
            ("demarrer-cameleon.md", 0.0),
            ("AGENTS.md", 0.0),
            ("demarrer-optimus-prime.md.bak.20260927_091045", 0.0),
            ("README.md.bak.20260927_091045", 0.0),
            ("vieux-cobaye.md", 30.0),
            ("cerveau-projet/agents/plume.md", 0.0),
            ("cerveau-projet/README-v2.md", 0.0),
            ("outils-llm/un-outil.py", 0.0),
        )
        for relatif, age_jours in poses:
            chemin = fictive / relatif
            chemin.parent.mkdir(parents=True, exist_ok=True)
            chemin.write_text("cobaye\n", encoding="utf-8", newline="\n")
            if age_jours:
                vieux = 1700000000 - age_jours * 86400
                os.utime(str(chemin), (vieux, vieux))

        resultat = lancer_enfant([sys.executable, str(garde), "--racine", str(fictive),
                                 "--jours", "7"], capture_output=True, text=True)
        sortie = (resultat.stdout or "") + (resultat.stderr or "")
        verdict = (sortie.split("PERIMETRE VIOLE", 1)[1]
                   if "PERIMETRE VIOLE" in sortie else "")
        # Les details ne sont plus coupe-gouttes : `_rendre_erreur` rend la queue
        # ENTIERE et DIT la coupe. Un verdict tronque au milieu d un chemin ne
        # nommait pas la regle qui l avait produit (mesure EO-537 : la cause
        # d un echec de clone est sur sa DERNIERE ligne, pas sous le seuil).
        ep("le garde rend un VERDICT, pas une trace", "Traceback" not in sortie,
           _rendre_erreur(sortie))
        ep("un fichier pose a la RACINE est ACCUSE et NOMME",
           "cobaye-racine.md" in verdict,
           "la RACINE est restee MUETTE : " + _rendre_erreur(sortie))
        ep("un fichier de la branche v1/v2 est ACCUSE",
           "cerveau-projet" in verdict and "plume.md" in verdict,
           "le cerveau v1/v2 hors matrix n est pas juge : " + _rendre_erreur(verdict))
        ep("CONTRE-TEMOIN -- le demarrage autorise par la porte est EPARGNE",
           "demarrer-optimus-prime.md (" not in verdict, _rendre_erreur(verdict))
        ep("CONTRE-TEMOIN -- AGENTS.md, ecrit par sa porte, est EPARGNE",
           "AGENTS.md (" not in verdict, _rendre_erreur(verdict))
        ep("le FILET de la porte est EPARGNE et NOMME",
           "FILET(S) DE LA PORTE" in sortie
           and "demarrer-optimus-prime.md.bak.20260927_091045" in sortie,
           _rendre_erreur(sortie))
        ep("CONTRE-TEMOIN -- la sauvegarde d un nom INTERDIT est ACCUSEE",
           "README.md.bak.20260927_091045" in verdict, _rendre_erreur(verdict))
        ep("un cobaye HORS FENETRE n est pas accuse", "vieux-cobaye.md" not in sortie,
           _rendre_erreur(sortie))
        ep("le PERIMETRE (matrix/) n est jamais accuse", "dedans.py" not in sortie,
           _rendre_erreur(sortie))
        ep("un sous-dossier hors perimetre est accuse (outils-llm)",
           "un-outil.py" in verdict, _rendre_erreur(verdict))
    finally:
        _shutil.rmtree(temp_root, ignore_errors=True)
    return ecarts


def _eprouver_portes_de_la_loi(racine):
    """MAILLON 72 (MO-496) : LA LOI PRESCRIT DES PORTES JOUABLES PAR CELUI QUI LES JOUE.

    LE DEFAUT, MESURE (2026-09-27, reproduit le 2026-09-29). ORDRE 4.6 de la loi du
    round prescrivait `lancer.py vigie-portes tour --si-due`. La carte de la vigie
    porte `flux: 1` : appelee par le flux 2 (identite declaree `operateur`), elle rend
    < porte privee du flux 1 appelee par le flux 2 > (code 2). UNE ETAPE PRESCRITE
    PAR LE TEXTE ESTait INEXECUTABLE, et l agent qui suit la loi etait refuse a chaque
    round -- sans qu'aucune suite ne le voie. Mesure sur les 11 portes citees par le
    protocole : vigie-portes etait la SEULE refusee au flux 2 (les 10 autres passent,
    dont 5 sans carte -- ce que le lanceur signale deja).

    LE PIEGE, et c est lui qui fait la CAUSE : l appel paraissait reussir. Un appel
    SANS identite declaree n est que NOMME, jamais refuse (choix mesure et documente
    dans lancer.py, pour ne pas casser 18 commandes documentees). La porte de l autre
    flux s executait donc... en cacheant son auteur. Un texte qui n aboutit qu en
    cachant qui l appelle enseigne a l agent de se taire : c est ce que ce maillon
    ferme, en tolerant aucune porte prescrite qui ne soit JOUABLE par le flux 2.

    CE QU IL EPROUVE :
      - LE COBAYE : chaque porte prescite par la loi est RESOLUE et lue par le juge
        REEL du lanceur (`controle`, appele a son chemin -- aucune regle recopiee,
        M-076) avec l identite du flux 2 : AUCUNE ne doit rendre de refus ;
      - LE CONTRE-TEMOIN DE DISCRIMINATION : une porte privee du flux 1 reste REFUSEE
        au flux 2. Sans lui, le controle serait une tautologie -- il passerait aussi
        bien si le croisement avait disparu (lecon L-132) ;
      - LE CONTRE-TEMOIN DE NON-VACUITE : le protocole doit encore prescrire des
        portes (un protocole vide ne prouverait rien) et chaque nom doit se resoudre ;
      - LA COHERENCE DU TEXTE : ORDRE 4.6 ne prescrit plus d ACTE sur une porte de
        l autre flux -- il se lit, il ne se joue pas.
    """
    import importlib.util
    import re as _re
    from pathlib import Path as _Chemin

    racine = _Chemin(racine).resolve()
    matrice = next((c for c in (racine, racine / "cerveau-projet" / "matrix", racine / "matrix")
                    if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    lanceur = matrice / "lancer.py"
    protocole = (matrice / "_operateur" / "optimus-prime" / "protocoles"
                 / "proto-12-loi-du-round.md")
    for absent in (lanceur, protocole):
        if not absent.is_file():
            return ["INTROUVABLE : " + absent.name]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    # LE JUGE EST CELUI DU LANCEUR, charge a SON CHEMIN : la regle du croisement a un
    # seul domicile, et un maillon qui la reecrirait validerait sa propre version.
    specification = importlib.util.spec_from_file_location("lanceur_loi_mo496", str(lanceur))
    juge = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(juge)
    except Exception as erreur:  # noqa: BLE001
        return ["le lanceur est ILLISIBLE (" + type(erreur).__name__ + " : "
                + str(erreur)[:80] + ")"]

    texte = protocole.read_text(encoding="utf-8", errors="replace")
    # UNE PORTE EST PRESCRITE PAR UNE COMMANDE, JAMAIS PAR UNE PHRASE : les lignes de
    # commentaire sont ecartees AVANT la lecture. Sans cela, l explication qui dit
    # pourquoi un acte a ete retire nommerait une porte qui redeviendrait prescrite
    # (lecon L-170 : le cobaye ne doit pas mordre sur le remede).
    prescrites = "\n".join(l for l in texte.splitlines()
                           if not l.strip().startswith("#"))
    cites = []
    for nom in _re.findall(r"lancer\.py ([a-z0-9\-]+)", prescrites):
        if nom.startswith("--") or nom in cites:   # une option n est pas une porte
            continue
        cites.append(nom)
    ep("la loi prescite encore des portes", len(cites) >= 5,
       str(len(cites)) + " porte(s) trouvee(s) -- un protocole vide ne prouverait rien")

    jouables = 0
    for nom in cites:
        cible, refus = juge.resoudre(nom)
        if refus is not None:
            ecarts.append("porte prescrite INTROUVABLE : " + nom + " -> " + str(refus)[:90])
            continue
        refus_porte, _signal = juge.controle(cible, "operateur")
        if refus_porte is not None:
            ecarts.append("porte prescrite REFUSEE au flux 2 : " + nom + " -> "
                          + str(refus_porte)[:110])
        else:
            jouables += 1
    ep("aucune porte prescrite n est close au flux qui la joue", jouables == len(cites),
       str(jouables) + " jouable(s) sur " + str(len(cites)))

    # LE CONTRE-TEMOIN : le croisement, lui, doit TOUJOURS mordre. Une porte privee
    # du flux 1 (la vigie-portes, carte `flux: 1`) reste inaccessible au flux 2 --
    # sinon ce maillon validerait un lanceur qui aurait ouvert toutes les portes.
    cible_vigie, refus_vigie = juge.resoudre("vigie-portes")
    if refus_vigie is not None:
        ecarts.append("CONTRE-TEMOIN impossible : vigie-portes introuvable -> "
                      + str(refus_vigie)[:90])
    else:
        refus_croisement, _ = juge.controle(cible_vigie, "operateur")
        ep("CONTRE-TEMOIN -- l ACTE de la porte de l autre flux reste REFUSE",
           refus_croisement is not None,
           "le croisement des flux ne mord plus : la regle a disparu")
        refus_meme, _ = juge.controle(cible_vigie, "cameleon")
        ep("CONTRE-TEMOIN -- son PROPRE flux reste servi",
           refus_meme is None,
           "la porte du flux 1 se refuse a elle-meme : " + str(refus_meme)[:90])

    # LE TEXTE : ORDRE 4.6 se LIT, il ne se JOUE pas.
    # CE QUI EST JUGE ICI, ET CE QUI NE L EST PAS. Une commande se reconnait a son
    # DEBUT (elle commence par python3) et une ligne de commande peut ANNOTER son
    # invocation -- nommer la vigie dans un renvoi n est pas l appeler. Greper le
    # texte entier confondait les deux (mesure du jour : l accusation est tombee sur
    # la LIGNE DE LECTURE, dont l annotation cite la cadence de la vigie).
    # L ACTE INTERDIT N EST DONC PAS GARE ICI : il l est par la LISTE DES PORTES
    # ci-dessus, qui exige que chaque porte PRESCRITE soit jouable au flux 2 -- si
    # quelqu un reintroduit `lancer.py vigie-portes tour`, cette porte-la reaparait
    # dans la liste, se fait REFUSER, et le maillon mord. Un controle faible qui
    # mord sur sa propre reparation vaut moins qu un controle fort (lecon L-132).
    ordre_46 = texte.split("### 4.6", 1)[-1].split("### 4.7", 1)[0] if "### 4.6" in texte else ""
    commandes_46 = [l.strip() for l in ordre_46.splitlines() if l.strip().startswith("python3")]
    ep("ORDRE 4.6 PRESCRIT une lecture reelle",
       any("cockpit-matrice --route etat" in c for c in commandes_46),
       "aucune commande de lecture dans ORDRE 4.6 : " + str(len(commandes_46)) + " commande(s)")
    ep("ORDRE 4.6 PRESCRIT des commandes",
       len(commandes_46) >= 4,
       str(len(commandes_46)) + " commande(s) : une section vide ne prouverait rien")

    # LE MAILLON PORTE SON PROPRE COBAYE (L-032 : un detecteur qui n a jamais vu de
    # refus ne prouve rien). L ACTE INTERDIT est re-insere dans une COPIE EN MEMOIRE
    # du protocole -- le fichier de service n est JAMAIS touche -- et l on exige les
    # DEUX maillons de la preuve : (1) la logique de citation le PRESCRIT alors
    # (sinon le maillon resterait muet sur une regression) ; (2) le juge REEL le
    # REFUSE au flux 2 (sinon il n y aurait rien a prescrire). Mesure du jour : sans
    # ce bloc, un cobaye construit sur une racine jetable mordait pour la MAUVAISE
    # raison -- le lanceur refuse de se charger hors de sa vraie structure -- et le
    # contre-temoin echouait avec lui : la preuve ne distinguait rien.
    lignes = texte.splitlines()
    porte_interdite = "vigie-portes"
    cible_refusee, refus_resolution = juge.resoudre(porte_interdite)
    if refus_resolution is not None:
        ecarts.append("COBAYE impossible : " + porte_interdite + " introuvable -> "
                      + str(refus_resolution)[:90])
    else:
        refus_attendu, _ = juge.controle(cible_refusee, "operateur")
        ligne_interdite = ("    python3 cerveau-projet/matrix/lancer.py "
                           + porte_interdite + " tour")
        if not commandes_46:
            ecarts.append("COBAYE impossible : ORDRE 4.6 ne porte aucune commande")
        else:
            # On reinjecte juste avant la PREMIERE commande de la section : la copie
            # ne depend d AUCUN mot du texte (le protocole peut etre reecrit).
            avant = next((k for k, ligne in enumerate(lignes)
                          if ligne.strip().startswith("python3")), None)
            copie = list(lignes)
            copie.insert(avant, ligne_interdite)
            cites_cobaye = [n for n in _re.findall(r"lancer\.py ([a-z0-9\-]+)",
                                                     "\n".join(copie))
                            if not n.startswith("--")]
            ep("COBAYE -- l acte interdit re-prescrit serait CITE",
               porte_interdite in cites_cobaye,
               "la citation ne le voit pas : ce maillon ne morderait pas sur la "
               "regression qu il est cense garder")
            ep("COBAYE -- et le juge REEL le REFUSERait au flux 2",
               refus_attendu is not None,
               "la porte de l autre flux est ouverte : plus rien ne mordrait")
    return ecarts


def _eprouver_banque_hors_jugement(racine):
    """MAILLON 73 (MO-497) : LA BANQUE v1/v2 EST HORS JUGEMENT, ET ELLE SE DIT.

    LE DEFAUT, MESURE (le 2026-09-27, reproduit et enlarge le 2026-09-29). Rendu sur
    la RACINE du workspace, le garde ASCII accusait 72 fichiers non-ASCII : 70 dans
    `cerveau-projet/` (agents, freelance, exemples), 1 dans `outils-llm/`, 1 a la
    racine. AUCUN n est de la v3, et AUCUN n est corrigeable : les corriger serait
    MUTER le cerveau v1/v2, ce qu ORDRE 3.4 interdit. Un garde qui accuse 72 fois un
    etat LEGAL est un garde qu on apprend a ignorer (R-008, MO-487). L item visait
    au debut le worktree `.kilo` ; cet artefact-la a DISPARU entre-temps (mesure du
    2026-09-29 : plus aucun fichier `.kilo` sur le disque) et le second rouge
    (`.kilo/.gitignore`) etait deja VERT depuis MO-487. La vraie cause, elle, etait
    plus large que l item : le garde n avait pas de DOMICILE pour la banque.

    LA REPARATION, et ce qu elle a dungue. `data/commun/zone_banque.py` declare la
    banque par son PREDICAT -- HORS perimetre d ecriture, et ni artefact externe ni
    zone jetable -- et le garde la consomme comme les trois zones deja declarees
    (M-076). PREMIER ESSAI, PREMIER KO : le predicat designe des FICHIERS, mais la
    cible du garde est un DOSSIER ; la racine du workspace fut alors declaree hors
    champ et le garde rendit 0 SANS controler le moindre fichier. Un vert obtenu par
    ABSENCE de controle est le pire des verdicts (L-132) : d ou `contient_le_perimetre`,
    qui dit qu une ZONE NE CONTIENT PAS SON CONTENANT.

    CE QU IL EPROUVE (sur une ARBORESCENCE FICTIVE, jamais sur le service) :
      - LE MORDANT : un fichier non-ASCII DANS le perimetre est ACCUSE et NOMME ;
      - LE CONTRE-TEMOIN 1 : le MEME contenu non-ASCII hors perimetre n est pas
        accuse -- et il est COMPTE et NOMME (une exemption muette serait un angle
        mort, L-104) ;
      - LE CONTRE-TEMOIN 2 : le perimetre lui-meme ne peut pas etre declare hors
        champ (sinon le garde ne controle plus rien : le piege mesure ci-dessus) ;
      - LA DECLARATION EST PARTAGEE : les quatre zones viennent de LEURS domiciles,
        les zones precises avant la zone large, et le garde n en recopie aucune.
    """
    import shutil
    import subprocess
    import sys as _sys
    import tempfile
    from pathlib import Path as _Chemin

    racine = _Chemin(racine).resolve()
    matrice = next((c for c in (racine, racine / "cerveau-projet" / "matrix", racine / "matrix")
                    if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    garde = (matrice / "_operateur" / "optimus-prime" / "super-combos" / "combos"
             / "outils" / "garde-ascii.py")
    if not garde.is_file():
        return ["INTROUVABLE : " + garde.name]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    specification = importlib.util.spec_from_file_location("garde_ascii_mo497", str(garde))
    juge = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(juge)
    except Exception as erreur:  # noqa: BLE001
        return ["le garde est ILLISIBLE (" + type(erreur).__name__ + " : "
                + str(erreur)[:80] + ")"]

    # LA DECLARATION EST PARTAGEE ET ORDONNEE. La banque vient EN DERNIER : une zone
    # large lue avant une zone precise absorberait celle-ci et son motif disparaitrait
    # du rapport -- un ordre de table qui decide d un motif est une regle, pas du gout.
    noms = [entree[0] for entree in juge.ZONES_HORS_CHAMP]
    ep("les zones declarees sont au nombre de quatre", len(noms) == 4,
       str(len(noms)) + " zone(s) : " + ", ".join(noms))
    ep("la BANQUE est declaree EN DERNIER", bool(noms) and noms[-1] == juge.NOM_ZONE_BANQUE,
       "ordre lu : " + ", ".join(noms))
    ep("chaque zone a un MOTIF non vide",
       all(entree[1] for entree in juge.ZONES_HORS_CHAMP),
       "une zone sans motif est une zone muette")

    # L ARBORESCENCE FICTIVE : une copie de la garde ET de ses domiciles, pour que le
    # perimetre de la v3 soit le faux `matrix/` et que rien du service ne soit lu.
    temp_root = tempfile.mkdtemp(prefix="cobaye-mo497-")
    try:
        fictif = _Chemin(temp_root) / "matrix"
        outils = fictif / "_operateur" / "optimus-prime" / "super-combos" / "combos" / "outils"
        outils.mkdir(parents=True)
        shutil.copy2(str(garde), str(outils / garde.name))
        commun_source = matrice / "matrice" / "data" / "commun"
        commun_cible = fictif / "matrice" / "data" / "commun"
        commun_cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(str(commun_source), str(commun_cible))
        # DEUX fichiers au MEME contenu non-ASCII : l'un DANS le perimetre, l'autre
        # hors perimetre. La seule difference est leur POSITION : c'est elle qui doit
        # decider du verdict, jamais leur contenu.
        accent = "accent non ascii : e" + chr(0xE0) + "\n"
        dedans = fictif / "matrice" / "donnees" / "lecon-non-ascii.md"
        dedans.parent.mkdir(parents=True, exist_ok=True)
        dedans.write_text(accent, encoding="utf-8", newline="\n")
        dehors = _Chemin(temp_root) / "cerveau-projet" / "agents" / "heritage-non-ascii.md"
        dehors.parent.mkdir(parents=True, exist_ok=True)
        dehors.write_text(accent, encoding="utf-8", newline="\n")
    except Exception as erreur:  # noqa: BLE001
        shutil.rmtree(temp_root, ignore_errors=True)
        return ["la COBAYE n a pas pu etre construite (" + type(erreur).__name__ + " : "
                + str(erreur)[:90] + ")"]

    # La construction est faite : on joue la garde REELLE du depot sur l arbre
    # fictif -- c est elle qu on eprouve, pas une reecriture de ses regles.
    for cible, attendu_code, est_accuse in (
            (fictif, 1, True),               # LE MORDANT
            (_Chemin(temp_root), 0, False)): # LE CONTRE-TEMOIN 1
        resultat = subprocess.run([_sys.executable, str(garde), str(cible)],
                                 capture_output=True, text=True)
        sortie = (resultat.stdout or "") + (resultat.stderr or "")
        etiquette = "MORDANT" if est_accuse else "CONTRE-TEMOIN"
        ep(etiquette + " -- la garde rend un VERDICT sur " + cible.name,
           "Traceback" not in sortie, (sortie.strip().splitlines() or ["vide"])[-1][:110])
        ep(etiquette + " -- code " + str(attendu_code) + " sur " + cible.name,
           resultat.returncode == attendu_code,
           "code " + str(resultat.returncode) + " : " + sortie.strip()[:140])
        if est_accuse:
            ep("MORDANT -- le fichier non-ASCII du PERIMETRE est ACCUSE et NOMME",
               "lecon-non-ascii.md" in sortie, sortie.strip()[:140])
        else:
            ep("CONTRE-TEMOIN -- le meme contenu HORS perimetre n est pas accuse",
               "heritage-non-ascii.md" not in sortie, sortie.strip()[:140])
            ep("CONTRE-TEMOIN 1 -- l exclusion est COMPTE et NOMMEE (jamais muette)",
               "HORS CHAMP" in sortie and juge.NOM_ZONE_BANQUE in sortie,
               sortie.strip()[:140])
            ep("CONTRE-TEMOIN 2 -- le perimetre reste CONTROLE (pas de vert par absence)",
               "ASCII sain" in sortie, sortie.strip()[:140])
    shutil.rmtree(temp_root, ignore_errors=True)
    return ecarts


def _eprouver_banque_hors_jugement(racine):
    """MAILLON 73 (MO-497) : LA BANQUE v1/v2 EST HORS JUGEMENT, ET ELLE SE DIT.

    LE DEFAUT, MESURE (le 2026-09-27, reproduit et enlarge le 2026-09-29). Rendu sur
    la RACINE du workspace, le garde ASCII accusait 72 fichiers non-ASCII : 70 dans
    `cerveau-projet/` (agents, freelance, exemples), 1 dans `outils-llm/`, 1 a la
    racine. AUCUN n est de la v3, et AUCUN n est corrigeable : les corriger serait
    MUTER le cerveau v1/v2, ce qu ORDRE 3.4 interdit. Un garde qui accuse 72 fois un
    etat LEGAL est un garde qu on apprend a ignorer (R-008, MO-487). L item visait
    au debut le worktree `.kilo` ; cet artefact-la a DISPARU entre-temps (mesure du
    2026-09-29 : plus aucun fichier `.kilo` sur le disque) et le second rouge
    (`.kilo/.gitignore`) etait deja VERT depuis MO-487. La vraie cause, elle, etait
    plus large que l item : le garde n avait pas de DOMICILE pour la banque.

    LA REPARATION, et ce qu elle a dungue. `data/commun/zone_banque.py` declare la
    banque par son PREDICAT -- HORS perimetre d ecriture, et ni artefact externe ni
    zone jetable -- et le garde la consomme comme les trois zones deja declarees
    (M-076). PREMIER ESSAI, PREMIER KO : le predicat designe des FICHIERS, mais la
    cible du garde est un DOSSIER ; la racine du workspace fut alors declaree hors
    champ et le garde rendit 0 SANS controler le moindre fichier. Un vert obtenu par
    ABSENCE de controle est le pire des verdicts (L-132) : d ou `contient_le_perimetre`,
    qui dit qu une ZONE NE CONTIENT PAS SON CONTENANT.

    CE QU IL EPROUVE (sur une ARBORESCENCE FICTIVE, jamais sur le service) :
      - LE MORDANT : un fichier non-ASCII DANS le perimetre est ACCUSE et NOMME ;
      - LE CONTRE-TEMOIN 1 : le MEME contenu non-ASCII hors perimetre n est pas
        accuse -- et il est COMPTE et NOMME (une exemption muette serait un angle
        mort, L-104) ;
      - LE CONTRE-TEMOIN 2 : le perimetre lui-meme ne peut pas etre declare hors
        champ (sinon le garde ne controle plus rien : le piege mesure ci-dessus) ;
      - LA DECLARATION EST PARTAGEE : les quatre zones viennent de LEURS domiciles,
        les zones precises avant la zone large, et le garde n en recopie aucune.
    """
    import importlib.util
    import shutil
    import subprocess
    import sys as _sys
    import tempfile
    from pathlib import Path as _Chemin

    racine = _Chemin(racine).resolve()
    matrice = next((c for c in (racine, racine / "cerveau-projet" / "matrix", racine / "matrix")
                    if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    garde = (matrice / "_operateur" / "optimus-prime" / "super-combos" / "combos"
             / "outils" / "garde-ascii.py")
    if not garde.is_file():
        return ["INTROUVABLE : " + garde.name]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    specification = importlib.util.spec_from_file_location("garde_ascii_mo497", str(garde))
    juge = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(juge)
    except Exception as erreur:  # noqa: BLE001
        return ["le garde est ILLISIBLE (" + type(erreur).__name__ + " : "
                + str(erreur)[:80] + ")"]

    # LA DECLARATION EST PARTAGEE ET ORDONNEE. La banque vient EN DERNIER : une zone
    # large lue avant une zone precise absorberait celle-ci et son motif disparaitrait
    # du rapport -- un ordre de table qui decide d un motif est une regle, pas du gout.
    noms = [entree[0] for entree in juge.ZONES_HORS_CHAMP]
    ep("les zones declarees sont au nombre de quatre", len(noms) == 4,
       str(len(noms)) + " zone(s) : " + ", ".join(noms))
    ep("la BANQUE est declaree EN DERNIER", bool(noms) and noms[-1] == juge.NOM_ZONE_BANQUE,
       "ordre lu : " + ", ".join(noms))
    ep("chaque zone a un MOTIF non vide",
       all(entree[1] for entree in juge.ZONES_HORS_CHAMP),
       "une zone sans motif est une zone muette")

    # L ARBORESCENCE FICTIVE : une copie de la garde ET de ses domiciles, pour que le
    # perimetre de la v3 soit le faux `matrix/` et que rien du service ne soit lu.
    temp_root = tempfile.mkdtemp(prefix="cobaye-mo497-")
    try:
        fictif = _Chemin(temp_root) / "matrix"
        outils = fictif / "_operateur" / "optimus-prime" / "super-combos" / "combos" / "outils"
        outils.mkdir(parents=True)
        shutil.copy2(str(garde), str(outils / garde.name))
        commun_source = matrice / "matrice" / "data" / "commun"
        commun_cible = fictif / "matrice" / "data" / "commun"
        commun_cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(str(commun_source), str(commun_cible))
        # DEUX fichiers au MEME contenu non-ASCII : l'un DANS le perimetre, l'autre
        # hors perimetre. La seule difference est leur POSITION : c'est elle qui doit
        # decider du verdict, jamais leur contenu.
        accent = "accent non ascii : e" + chr(0xE0) + "\n"
        dedans = fictif / "matrice" / "donnees" / "lecon-non-ascii.md"
        dedans.parent.mkdir(parents=True, exist_ok=True)
        dedans.write_text(accent, encoding="utf-8", newline="\n")
        dehors = _Chemin(temp_root) / "cerveau-projet" / "agents" / "heritage-non-ascii.md"
        dehors.parent.mkdir(parents=True, exist_ok=True)
        dehors.write_text(accent, encoding="utf-8", newline="\n")
    except Exception as erreur:  # noqa: BLE001
        shutil.rmtree(temp_root, ignore_errors=True)
        return ["la COBAYE n a pas pu etre construite (" + type(erreur).__name__ + " : "
                + str(erreur)[:90] + ")"]

    # La construction est faite : on joue la garde REELLE du depot sur l arbre
    # fictif -- c est elle qu on eprouve, pas une reecriture de ses regles.
    for cible, attendu_code, est_accuse in (
            (fictif, 1, True),               # LE MORDANT
            (_Chemin(temp_root), 0, False)): # LE CONTRE-TEMOIN 1
        resultat = subprocess.run([_sys.executable, str(garde), str(cible)],
                                 capture_output=True, text=True)
        sortie = (resultat.stdout or "") + (resultat.stderr or "")
        etiquette = "MORDANT" if est_accuse else "CONTRE-TEMOIN"
        ep(etiquette + " -- la garde rend un VERDICT sur " + cible.name,
           "Traceback" not in sortie, (sortie.strip().splitlines() or ["vide"])[-1][:110])
        ep(etiquette + " -- code " + str(attendu_code) + " sur " + cible.name,
           resultat.returncode == attendu_code,
           "code " + str(resultat.returncode) + " : " + sortie.strip()[:140])
        if est_accuse:
            ep("MORDANT -- le fichier non-ASCII du PERIMETRE est ACCUSE et NOMME",
               "lecon-non-ascii.md" in sortie, sortie.strip()[:140])
        else:
            ep("CONTRE-TEMOIN -- le meme contenu HORS perimetre n est pas accuse",
               "heritage-non-ascii.md" not in sortie, sortie.strip()[:140])
            ep("CONTRE-TEMOIN 1 -- l exclusion est COMPTE et NOMMEE (jamais muette)",
               "HORS CHAMP" in sortie and juge.NOM_ZONE_BANQUE in sortie,
               sortie.strip()[:140])
            ep("CONTRE-TEMOIN 2 -- le perimetre reste CONTROLE (pas de vert par absence)",
               "ASCII sain" in sortie, sortie.strip()[:140])
    shutil.rmtree(temp_root, ignore_errors=True)
    return ecarts


def _eprouver_banque_hors_jugement(racine):
    """MAILLON 73 (MO-497) : LA BANQUE v1/v2 EST HORS JUGEMENT, ET ELLE SE DIT.

    LE DEFAUT, MESURE (le 2026-09-27, reproduit et enlarge le 2026-09-29). Rendu sur
    la RACINE du workspace, le garde ASCII accusait 72 fichiers non-ASCII : 70 dans
    `cerveau-projet/` (agents, freelance, exemples), 1 dans `outils-llm/`, 1 a la
    racine. AUCUN n est de la v3, et AUCUN n est corrigeable : les corriger serait
    MUTER le cerveau v1/v2, ce qu ORDRE 3.4 interdit. Un garde qui accuse 72 fois un
    etat LEGAL est un garde qu on apprend a ignorer (R-008, MO-487). L item visait
    au debut le worktree `.kilo` ; cet artefact-la a DISPARU entre-temps (mesure du
    2026-09-29 : plus aucun fichier `.kilo` sur le disque) et le second rouge
    (`.kilo/.gitignore`) etait deja VERT depuis MO-487. La vraie cause, elle, etait
    plus large que l item : le garde n avait pas de DOMICILE pour la banque.

    LA REPARATION, et ce qu elle a dungue. `data/commun/zone_banque.py` declare la
    banque par son PREDICAT -- HORS perimetre d ecriture, et ni artefact externe ni
    zone jetable -- et le garde la consomme comme les trois zones deja declarees
    (M-076). PREMIER ESSAI, PREMIER KO : le predicat designe des FICHIERS, mais la
    cible du garde est un DOSSIER ; la racine du workspace fut alors declaree hors
    champ et le garde rendit 0 SANS controler le moindre fichier. Un vert obtenu par
    ABSENCE de controle est le pire des verdicts (L-132) : d ou `contient_le_perimetre`,
    qui dit qu une ZONE NE CONTIENT PAS SON CONTENANT.

    CE QU IL EPROUVE (sur une ARBORESCENCE FICTIVE, jamais sur le service) :
      - LE MORDANT : un fichier non-ASCII DANS le perimetre est ACCUSE et NOMME ;
      - LE CONTRE-TEMOIN 1 : le MEME contenu non-ASCII hors perimetre n est pas
        accuse -- et il est COMPTE et NOMME (une exemption muette serait un angle
        mort, L-104) ;
      - LE CONTRE-TEMOIN 2 : le perimetre lui-meme ne peut pas etre declare hors
        champ (sinon le garde ne controle plus rien : le piege mesure ci-dessus) ;
      - LA DECLARATION EST PARTAGEE : les quatre zones viennent de LEURS domiciles,
        les zones precises avant la zone large, et le garde n en recopie aucune.
    """
    import importlib.util
    import shutil
    import subprocess
    import sys as _sys
    import tempfile
    from pathlib import Path as _Chemin

    racine = _Chemin(racine).resolve()
    matrice = next((c for c in (racine, racine / "cerveau-projet" / "matrix", racine / "matrix")
                    if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    garde = (matrice / "_operateur" / "optimus-prime" / "super-combos" / "combos"
             / "outils" / "garde-ascii.py")
    if not garde.is_file():
        return ["INTROUVABLE : " + garde.name]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    specification = importlib.util.spec_from_file_location("garde_ascii_mo497", str(garde))
    juge = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(juge)
    except Exception as erreur:  # noqa: BLE001
        return ["le garde est ILLISIBLE (" + type(erreur).__name__ + " : "
                + str(erreur)[:80] + ")"]

    # LA DECLARATION EST PARTAGEE ET ORDONNEE. La banque vient EN DERNIER : une zone
    # large lue avant une zone precise absorberait celle-ci et son motif disparaitrait
    # du rapport -- un ordre de table qui decide d un motif est une regle, pas du gout.
    noms = [entree[0] for entree in juge.ZONES_HORS_CHAMP]
    ep("les zones declarees sont au nombre de quatre", len(noms) == 4,
       str(len(noms)) + " zone(s) : " + ", ".join(noms))
    ep("la BANQUE est declaree EN DERNIER", bool(noms) and noms[-1] == juge.NOM_ZONE_BANQUE,
       "ordre lu : " + ", ".join(noms))
    ep("chaque zone a un MOTIF non vide",
       all(entree[1] for entree in juge.ZONES_HORS_CHAMP),
       "une zone sans motif est une zone muette")

    # L ARBORESCENCE FICTIVE : une copie de la garde ET de ses domiciles, pour que le
    # perimetre de la v3 soit le faux `matrix/` et que rien du service ne soit lu.
    temp_root = tempfile.mkdtemp(prefix="cobaye-mo497-")
    try:
        # LE MARQUEUR DE RACINE. `racine.detecter_racine` cherche AGENTS.md en
        # remontant : sans lui, les domiciles REFUSENT de se charger et la cobaye
        # echouerait sur sa propre fixture -- un cobaye qui tombe pour une raison
        # etrangere a ce qu il doit prouver ne prouve rien (mesure du jour, meme
        # famille que le cobaye du maillon 70 monte sur une racine artificeille).
        (_Chemin(temp_root) / "AGENTS.md").write_text("racine factice\n",
                                                      encoding="utf-8", newline="\n")
        fictif = _Chemin(temp_root) / "matrix"
        outils = fictif / "_operateur" / "optimus-prime" / "super-combos" / "combos" / "outils"
        outils.mkdir(parents=True)
        shutil.copy2(str(garde), str(outils / garde.name))
        commun_source = matrice / "matrice" / "data" / "commun"
        commun_cible = fictif / "matrice" / "data" / "commun"
        commun_cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(str(commun_source), str(commun_cible))
        # DEUX fichiers au MEME contenu non-ASCII : l'un DANS le perimetre, l'autre
        # hors perimetre. La seule difference est leur POSITION : c'est elle qui doit
        # decider du verdict, jamais leur contenu.
        accent = "accent non ascii : e" + chr(0xE0) + "\n"
        dedans = fictif / "matrice" / "donnees" / "lecon-non-ascii.md"
        dedans.parent.mkdir(parents=True, exist_ok=True)
        dedans.write_text(accent, encoding="utf-8", newline="\n")
        dehors = _Chemin(temp_root) / "cerveau-projet" / "agents" / "heritage-non-ascii.md"
        dehors.parent.mkdir(parents=True, exist_ok=True)
        dehors.write_text(accent, encoding="utf-8", newline="\n")
    except Exception as erreur:  # noqa: BLE001
        shutil.rmtree(temp_root, ignore_errors=True)
        return ["la COBAYE n a pas pu etre construite (" + type(erreur).__name__ + " : "
                + str(erreur)[:90] + ")"]

    # La construction est faite : on joue la garde REELLE du depot sur l arbre
    # fictif -- c est elle qu on eprouve, pas une reecriture de ses regles.
    for cible, attendu_code, est_accuse in (
            (fictif, 1, True),               # LE MORDANT
            (_Chemin(temp_root), 0, False)): # LE CONTRE-TEMOIN 1
        resultat = subprocess.run([_sys.executable, str(garde), str(cible)],
                                 capture_output=True, text=True)
        sortie = (resultat.stdout or "") + (resultat.stderr or "")
        etiquette = "MORDANT" if est_accuse else "CONTRE-TEMOIN"
        ep(etiquette + " -- la garde rend un VERDICT sur " + cible.name,
           "Traceback" not in sortie, (sortie.strip().splitlines() or ["vide"])[-1][:110])
        ep(etiquette + " -- code " + str(attendu_code) + " sur " + cible.name,
           resultat.returncode == attendu_code,
           "code " + str(resultat.returncode) + " : " + sortie.strip()[:140])
        if est_accuse:
            ep("MORDANT -- le fichier non-ASCII du PERIMETRE est ACCUSE et NOMME",
               "lecon-non-ascii.md" in sortie, sortie.strip()[:140])
        else:
            ep("CONTRE-TEMOIN -- le meme contenu HORS perimetre n est pas accuse",
               "heritage-non-ascii.md" not in sortie, sortie.strip()[:140])
            ep("CONTRE-TEMOIN 1 -- l exclusion est COMPTE et NOMMEE (jamais muette)",
               "HORS CHAMP" in sortie and juge.NOM_ZONE_BANQUE in sortie,
               sortie.strip()[:140])
            ep("CONTRE-TEMOIN 2 -- le perimetre reste CONTROLE (pas de vert par absence)",
               "ASCII sain" in sortie, sortie.strip()[:140])
    shutil.rmtree(temp_root, ignore_errors=True)
    return ecarts


def _eprouver_banque_hors_jugement(racine):
    """MAILLON 73 (MO-497) : LA BANQUE v1/v2 EST HORS JUGEMENT, ET ELLE SE DIT.

    LE DEFAUT, MESURE (le 2026-09-27, reproduit et enlarge le 2026-09-29). Rendu sur
    la RACINE du workspace, le garde ASCII accusait 72 fichiers non-ASCII : 70 dans
    `cerveau-projet/` (agents, freelance, exemples), 1 dans `outils-llm/`, 1 a la
    racine. AUCUN n est de la v3, et AUCUN n est corrigeable : les corriger serait
    MUTER le cerveau v1/v2, ce qu ORDRE 3.4 interdit. Un garde qui accuse 72 fois un
    etat LEGAL est un garde qu on apprend a ignorer (R-008, MO-487). L item visait
    au debut le worktree `.kilo` ; cet artefact-la a DISPARU entre-temps (mesure du
    2026-09-29 : plus aucun fichier `.kilo` sur le disque) et le second rouge
    (`.kilo/.gitignore`) etait deja VERT depuis MO-487. La vraie cause, elle, etait
    plus large que l item : le garde n avait pas de DOMICILE pour la banque.

    LA REPARATION, et ce qu elle a dungue. `data/commun/zone_banque.py` declare la
    banque par son PREDICAT -- HORS perimetre d ecriture, et ni artefact externe ni
    zone jetable -- et le garde la consomme comme les trois zones deja declarees
    (M-076). PREMIER ESSAI, PREMIER KO : le predicat designe des FICHIERS, mais la
    cible du garde est un DOSSIER ; la racine du workspace fut alors declaree hors
    champ et le garde rendit 0 SANS controler le moindre fichier. Un vert obtenu par
    ABSENCE de controle est le pire des verdicts (L-132) : d ou `contient_le_perimetre`,
    qui dit qu une ZONE NE CONTIENT PAS SON CONTENANT.

    CE QU IL EPROUVE (sur une ARBORESCENCE FICTIVE, jamais sur le service) :
      - LE MORDANT : un fichier non-ASCII DANS le perimetre est ACCUSE et NOMME ;
      - LE CONTRE-TEMOIN 1 : le MEME contenu non-ASCII hors perimetre n est pas
        accuse -- et il est COMPTE et NOMME (une exemption muette serait un angle
        mort, L-104) ;
      - LE CONTRE-TEMOIN 2 : le perimetre lui-meme ne peut pas etre declare hors
        champ (sinon le garde ne controle plus rien : le piege mesure ci-dessus) ;
      - LA DECLARATION EST PARTAGEE : les quatre zones viennent de LEURS domiciles,
        les zones precises avant la zone large, et le garde n en recopie aucune.
    """
    import importlib.util
    import shutil
    import subprocess
    import sys as _sys
    import tempfile
    from pathlib import Path as _Chemin

    racine = _Chemin(racine).resolve()
    matrice = next((c for c in (racine, racine / "cerveau-projet" / "matrix", racine / "matrix")
                    if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    garde = (matrice / "_operateur" / "optimus-prime" / "super-combos" / "combos"
             / "outils" / "garde-ascii.py")
    if not garde.is_file():
        return ["INTROUVABLE : " + garde.name]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    specification = importlib.util.spec_from_file_location("garde_ascii_mo497", str(garde))
    juge = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(juge)
    except Exception as erreur:  # noqa: BLE001
        return ["le garde est ILLISIBLE (" + type(erreur).__name__ + " : "
                + str(erreur)[:80] + ")"]

    # LA DECLARATION EST PARTAGEE ET ORDONNEE. La banque vient EN DERNIER : une zone
    # large lue avant une zone precise absorberait celle-ci et son motif disparaitrait
    # du rapport -- un ordre de table qui decide d un motif est une regle, pas du gout.
    noms = [entree[0] for entree in juge.ZONES_HORS_CHAMP]
    ep("les zones declarees sont au nombre de quatre", len(noms) == 4,
       str(len(noms)) + " zone(s) : " + ", ".join(noms))
    ep("la BANQUE est declaree EN DERNIER", bool(noms) and noms[-1] == juge.NOM_ZONE_BANQUE,
       "ordre lu : " + ", ".join(noms))
    ep("chaque zone a un MOTIF non vide",
       all(entree[1] for entree in juge.ZONES_HORS_CHAMP),
       "une zone sans motif est une zone muette")

    # L ARBORESCENCE FICTIVE : une copie de la garde ET de ses domiciles, pour que le
    # perimetre de la v3 soit le faux `matrix/` et que rien du service ne soit lu.
    temp_root = tempfile.mkdtemp(prefix="cobaye-mo497-")
    try:
        # LE MARQUEUR DE RACINE. `racine.detecter_racine` cherche AGENTS.md en
        # remontant : sans lui, les domiciles REFUSENT de se charger et la cobaye
        # echouerait sur sa propre fixture -- un cobaye qui tombe pour une raison
        # etrangere a ce qu il doit prouver ne prouve rien (mesure du jour, meme
        # famille que le cobaye du maillon 70 monte sur une racine artificeille).
        (_Chemin(temp_root) / "AGENTS.md").write_text("racine factice\n",
                                                      encoding="utf-8", newline="\n")
        fictif = _Chemin(temp_root) / "matrix"
        outils = fictif / "_operateur" / "optimus-prime" / "super-combos" / "combos" / "outils"
        outils.mkdir(parents=True)
        shutil.copy2(str(garde), str(outils / garde.name))
        commun_source = matrice / "matrice" / "data" / "commun"
        commun_cible = fictif / "matrice" / "data" / "commun"
        commun_cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(str(commun_source), str(commun_cible))
        # DEUX fichiers au MEME contenu non-ASCII : l'un DANS le perimetre, l'autre
        # hors perimetre. La seule difference est leur POSITION : c'est elle qui doit
        # decider du verdict, jamais leur contenu.
        accent = "accent non ascii : e" + chr(0xE0) + "\n"
        dedans = fictif / "matrice" / "donnees" / "lecon-non-ascii.md"
        dedans.parent.mkdir(parents=True, exist_ok=True)
        dedans.write_text(accent, encoding="utf-8", newline="\n")
        dehors = _Chemin(temp_root) / "cerveau-projet" / "agents" / "heritage-non-ascii.md"
        dehors.parent.mkdir(parents=True, exist_ok=True)
        dehors.write_text(accent, encoding="utf-8", newline="\n")
    except Exception as erreur:  # noqa: BLE001
        shutil.rmtree(temp_root, ignore_errors=True)
        return ["la COBAYE n a pas pu etre construite (" + type(erreur).__name__ + " : "
                + str(erreur)[:90] + ")"]

    # La construction est faite : on joue la COPIE de la garde, celle de l arbre
    # fictif -- sa racine de Matrice EST le faux `matrix/`. Jouer la garde du depot
    # depuis l exterieur n auraiT aucun sens : elle jugerait le faux arbre avec le
    # perimetre du service, donc tout y serait hors perimetre (mesure du jour).
    garde_fictive = outils / garde.name
    for cible, attendu_code, est_accuse in (
            (fictif, 1, True),               # LE MORDANT
            (_Chemin(temp_root), 0, False)): # LE CONTRE-TEMOIN 1
        resultat = subprocess.run([_sys.executable, str(garde_fictive), str(cible)],
                                 capture_output=True, text=True)
        sortie = (resultat.stdout or "") + (resultat.stderr or "")
        etiquette = "MORDANT" if est_accuse else "CONTRE-TEMOIN"
        ep(etiquette + " -- la garde rend un VERDICT sur " + cible.name,
           "Traceback" not in sortie, (sortie.strip().splitlines() or ["vide"])[-1][:110])
        ep(etiquette + " -- code " + str(attendu_code) + " sur " + cible.name,
           resultat.returncode == attendu_code,
           "code " + str(resultat.returncode) + " : " + sortie.strip()[:140])
        if est_accuse:
            ep("MORDANT -- le fichier non-ASCII du PERIMETRE est ACCUSE et NOMME",
               "lecon-non-ascii.md" in sortie, sortie.strip()[:140])
        else:
            ep("CONTRE-TEMOIN -- le meme contenu HORS perimetre n est pas accuse",
               "heritage-non-ascii.md" not in sortie, sortie.strip()[:140])
            ep("CONTRE-TEMOIN 1 -- l exclusion est COMPTE et NOMMEE (jamais muette)",
               "HORS CHAMP" in sortie and juge.NOM_ZONE_BANQUE in sortie,
               sortie.strip()[:140])
            ep("CONTRE-TEMOIN 2 -- le perimetre reste CONTROLE (pas de vert par absence)",
               "ASCII sain" in sortie, sortie.strip()[:140])
    shutil.rmtree(temp_root, ignore_errors=True)
    return ecarts


def _eprouver_banque_hors_jugement(racine):
    """MAILLON 73 (MO-497) : LA BANQUE v1/v2 EST HORS JUGEMENT, ET ELLE SE DIT.

    LE DEFAUT, MESURE (le 2026-09-27, reproduit et enlarge le 2026-09-29). Rendu sur
    la RACINE du workspace, le garde ASCII accusait 72 fichiers non-ASCII : 70 dans
    `cerveau-projet/` (agents, freelance, exemples), 1 dans `outils-llm/`, 1 a la
    racine. AUCUN n est de la v3, et AUCUN n est corrigeable : les corriger serait
    MUTER le cerveau v1/v2, ce qu ORDRE 3.4 interdit. Un garde qui accuse 72 fois un
    etat LEGAL est un garde qu on apprend a ignorer (R-008, MO-487). L item visait
    au debut le worktree `.kilo` ; cet artefact-la a DISPARU entre-temps (mesure du
    2026-09-29 : plus aucun fichier `.kilo` sur le disque) et le second rouge
    (`.kilo/.gitignore`) etait deja VERT depuis MO-487. La vraie cause, elle, etait
    plus large que l item : le garde n avait pas de DOMICILE pour la banque.

    LA REPARATION, et ce qu elle a dungue. `data/commun/zone_banque.py` declare la
    banque par son PREDICAT -- HORS perimetre d ecriture, et ni artefact externe ni
    zone jetable -- et le garde la consomme comme les trois zones deja declarees
    (M-076). PREMIER ESSAI, PREMIER KO : le predicat designe des FICHIERS, mais la
    cible du garde est un DOSSIER ; la racine du workspace fut alors declaree hors
    champ et le garde rendit 0 SANS controler le moindre fichier. Un vert obtenu par
    ABSENCE de controle est le pire des verdicts (L-132) : d ou `contient_le_perimetre`,
    qui dit qu une ZONE NE CONTIENT PAS SON CONTENANT.

    CE QU IL EPROUVE (sur une ARBORESCENCE FICTIVE, jamais sur le service) :
      - LE MORDANT : un fichier non-ASCII DANS le perimetre est ACCUSE et NOMME ;
      - LE CONTRE-TEMOIN 1 : le MEME contenu non-ASCII hors perimetre n est pas
        accuse -- et il est COMPTE et NOMME (une exemption muette serait un angle
        mort, L-104) ;
      - LE CONTRE-TEMOIN 2 : le perimetre lui-meme ne peut pas etre declare hors
        champ (sinon le garde ne controle plus rien : le piege mesure ci-dessus) ;
      - LA DECLARATION EST PARTAGEE : les quatre zones viennent de LEURS domiciles,
        les zones precises avant la zone large, et le garde n en recopie aucune.
    """
    import importlib.util
    import shutil
    import subprocess
    import sys as _sys
    import tempfile
    from pathlib import Path as _Chemin

    racine = _Chemin(racine).resolve()
    matrice = next((c for c in (racine, racine / "cerveau-projet" / "matrix", racine / "matrix")
                    if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    garde = (matrice / "_operateur" / "optimus-prime" / "super-combos" / "combos"
             / "outils" / "garde-ascii.py")
    if not garde.is_file():
        return ["INTROUVABLE : " + garde.name]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    specification = importlib.util.spec_from_file_location("garde_ascii_mo497", str(garde))
    juge = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(juge)
    except Exception as erreur:  # noqa: BLE001
        return ["le garde est ILLISIBLE (" + type(erreur).__name__ + " : "
                + str(erreur)[:80] + ")"]

    # LA DECLARATION EST PARTAGEE ET ORDONNEE. La banque vient EN DERNIER : une zone
    # large lue avant une zone precise absorberait celle-ci et son motif disparaitrait
    # du rapport -- un ordre de table qui decide d un motif est une regle, pas du gout.
    noms = [entree[0] for entree in juge.ZONES_HORS_CHAMP]
    ep("les zones declarees sont au nombre de quatre", len(noms) == 4,
       str(len(noms)) + " zone(s) : " + ", ".join(noms))
    ep("la BANQUE est declaree EN DERNIER", bool(noms) and noms[-1] == juge.NOM_ZONE_BANQUE,
       "ordre lu : " + ", ".join(noms))
    ep("chaque zone a un MOTIF non vide",
       all(entree[1] for entree in juge.ZONES_HORS_CHAMP),
       "une zone sans motif est une zone muette")

    # L ARBORESCENCE FICTIVE : une copie de la garde ET de ses domiciles, pour que le
    # perimetre de la v3 soit le faux `matrix/` et que rien du service ne soit lu.
    temp_root = tempfile.mkdtemp(prefix="cobaye-mo497-")
    try:
        # LE MARQUEUR DE RACINE. `racine.detecter_racine` cherche AGENTS.md en
        # remontant : sans lui, les domiciles REFUSENT de se charger et la cobaye
        # echouerait sur sa propre fixture -- un cobaye qui tombe pour une raison
        # etrangere a ce qu il doit prouver ne prouve rien (mesure du jour, meme
        # famille que le cobaye du maillon 70 monte sur une racine artificeille).
        (_Chemin(temp_root) / "AGENTS.md").write_text("racine factice\n",
                                                      encoding="utf-8", newline="\n")
        fictif = _Chemin(temp_root) / "matrix"
        outils = fictif / "_operateur" / "optimus-prime" / "super-combos" / "combos" / "outils"
        outils.mkdir(parents=True)
        shutil.copy2(str(garde), str(outils / garde.name))
        commun_source = matrice / "matrice" / "data" / "commun"
        commun_cible = fictif / "matrice" / "data" / "commun"
        commun_cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(str(commun_source), str(commun_cible))
        # DEUX fichiers au MEME contenu non-ASCII : l'un DANS le perimetre, l'autre
        # hors perimetre. La seule difference est leur POSITION : c'est elle qui doit
        # decider du verdict, jamais leur contenu.
        accent = "accent non ascii : e" + chr(0xE0) + "\n"
        dedans = fictif / "matrice" / "donnees" / "lecon-non-ascii.md"
        dedans.parent.mkdir(parents=True, exist_ok=True)
        dedans.write_text(accent, encoding="utf-8", newline="\n")
        dehors = _Chemin(temp_root) / "cerveau-projet" / "agents" / "heritage-non-ascii.md"
        dehors.parent.mkdir(parents=True, exist_ok=True)
        dehors.write_text(accent, encoding="utf-8", newline="\n")
    except Exception as erreur:  # noqa: BLE001
        shutil.rmtree(temp_root, ignore_errors=True)
        return ["la COBAYE n a pas pu etre construite (" + type(erreur).__name__ + " : "
                + str(erreur)[:90] + ")"]

    # La construction est faite : on joue la COPIE de la garde, celle de l arbre
    # fictif -- sa racine de Matrice EST le faux `matrix/`. Jouer la garde du depot
    # depuis l exterieur n auraiT aucun sens : elle jugerait le faux arbre avec le
    # perimetre du service, donc tout y serait hors perimetre (mesure du jour).
    garde_fictive = outils / garde.name
    for cible, etiquette in ((fictif, "MORDANT"), (_Chemin(temp_root), "CONTRE-TEMOIN")):
        resultat = subprocess.run([_sys.executable, str(garde_fictive), str(cible)],
                                 capture_output=True, text=True)
        sortie = (resultat.stdout or "") + (resultat.stderr or "")
        ep(etiquette + " -- la garde rend un VERDICT sur " + cible.name,
           "Traceback" not in sortie, (sortie.strip().splitlines() or ["vide"])[-1][:110])
        # DANS LES DEUX CAS le code est 1 : le fichier non-ASCII du PERIMETRE est
        # accuse. La difference entre les deux passages n est pas le code, c est
        # QUE le scan large AJOUTE le heritage au COMPTE des epargnes sans jamais
        # l inscrire parmi les violations.
        ep(etiquette + " -- le non-ASCII du PERIMETRE est ACCUSE (code 1)",
           resultat.returncode == 1 and "lecon-non-ascii.md" in sortie,
           "code " + str(resultat.returncode) + " : " + sortie.strip()[:140])
        ep(etiquette + " -- le heritage HORS perimetre n est PAS une violation",
           "heritage-non-ascii.md" not in sortie, sortie.strip()[:140])
        if etiquette == "CONTRE-TEMOIN":
            ep("CONTRE-TEMOIN 1 -- l exclusion est COMPTE et NOMMEE (jamais muette)",
               "HORS CHAMP" in sortie and juge.NOM_ZONE_BANQUE in sortie,
               sortie.strip()[:140])
            ep("CONTRE-TEMOIN 2 -- le perimetre reste CONTROLE (pas de vert par absence)",
               "ASCII VIOLE" in sortie and "HORS CHAMP" in sortie,
               sortie.strip()[:140])
    shutil.rmtree(temp_root, ignore_errors=True)
    return ecarts


def _eprouver_age_sur_trace_de_service(racine):
    """MAILLON 74 (MO-501) : L AGE D UNE MISSION SE MESURE SUR SA TRACE DE SERVICE.

    LE DEFAUT, MESURE (le 2026-09-28 par le projet lui-meme, reproduit en boucle).
    `detecter_age_mission` calculait l age d une mission EN COURS sur son champ
    `chargee_le`. Or un LOT entier partage le meme `chargee_le` (fait ecrit dans le
    code de ce meme fichier) : une mission servie depuis DEUX MINUTES se lisait
    < en cours depuis 2.4 j >. Consequence : le rouge est NORMAL pendant toute la
    conduite d un lot arme, la suite est rouge du premier au dernier round, et
    chacun apprend a l ignorer -- exactement le motif que le createur a fait inverser
    en MO-487 (R-008 : un controle dont l etat normal est rouge s inverse).

    LE REMEDE EXISTAIT DEJA ET NE CONSUMAIT PERSONNE. `charges_tracees` (ecrit par la
    porte depuis le 2026-09-22) sait lire les actes `charge` -- le VRAI moment du
    service -- mais aucun appelant ne le consommait. Un remede ecrit et non consomme
    est une decision qui dort (regle immuable `evolution-decidee`) : c est la panne
    de ce depot, et elle se reproduit ici.

    CE QU IL EPROUVE, sur une VUE FABRIQUE (en memoire, aucun fichier de service) :
      - LE COBAYE : une mission servie il y a 2 min, dont `chargee_le` dit 3 jours,
        n est PAS accusee -- l age vient de la trace ;
      - LE CONTRE-TEMOIN : la MEME mission SANS trace de service (champ seul) EST
        accusee -- sans lui, le maillon passerait aussi bien avec un detecteur muet ;
      - LE REPLI : la source de l age est NOMMEE dans le fait accuse, donc un age
        sans horloge ne peut pas etre discute ;
      - LA LECTURE EST UNIQUE : l age passe par `dernieres_charges`, qui consomme
        `charges_tracees` -- une deuxieme lecture du journal divergerait (M-076).
    """
    import importlib.util
    import json
    from datetime import datetime, timedelta
    from pathlib import Path as _Chemin

    racine = _Chemin(racine).resolve()
    matrice = next((c for c in (racine, racine / "cerveau-projet" / "matrix", racine / "matrix")
                    if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    outil = (matrice / "_operateur" / "optimus-prime" / "super-combos" / "combos"
             / "outils" / "suivi-pilote.py")
    declaration = (matrice / "_operateur" / "optimus-prime" / "suivi-pilote"
                   / "pannes-declarees.json")
    for absent in (outil, declaration):
        if not absent.is_file():
            return ["INTROUVABLE : " + absent.name]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    specification = importlib.util.spec_from_file_location("suivi_pilote_mo501", str(outil))
    juge = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(juge)
    except Exception as erreur:  # noqa: BLE001
        return ["le suivi du pilote est ILLISIBLE (" + type(erreur).__name__ + " : "
                + str(erreur)[:80] + ")"]
    try:
        reglages = json.loads(declaration.read_text(encoding="utf-8"))
    except ValueError:
        return ["pannes-declarees.json ILLISIBLE (JSON invalide)"]

    maintenant = datetime.now()
    veille = (maintenant - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
    frais = (maintenant - timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S")

    class VueFabrique:
        """UNE vue de service, en MEMOIRE : c est elle qu on eprouve, jamais le disque."""

        def __init__(self, evenements):
            self.evenements = evenements
            self.maintenant = maintenant
            self.dernier_fait = {}

        def en_cours(self):
            return [{"id": "MO-990", "chargee_le": veille}]

    mission_lot = {"action": "charge", "mission": "MO-990", "date": frais}

    # LE COBAYE : la trace dit 2 min, le champ dit 3 jours. C'est le LOT.
    accusee_avec_trace = juge.detecter_age_mission(VueFabrique([mission_lot]), reglages, "")
    ep("COBAYE -- une mission servie depuis 2 min n est PAS accusee",
       accusee_avec_trace is None,
       "accusee alors que sa trace de service date de 2 min : " + str(accusee_avec_trace)[:130])
    # LE CONTRE-TEMOIN : pas de trace, le champ seul. Elle DOIT etre accusee.
    verdict = juge.detecter_age_mission(VueFabrique([]), reglages, "")
    ep("CONTRE-TEMOIN -- sans trace de service, la MEME mission EST accusee",
       verdict is not None,
       "muette : le detecteur ne mordrait sur rien (L-132)")
    if verdict is not None:
        ep("CONTRE-TEMOIN -- le fait nomme l horloge mesuree",
           "chargee_le" in str(verdict[2]),
           "l age est accuse sans dire d ou il sort : " + str(verdict[2])[:120])
    # LA LECTURE EST UNIQUE ET CONSOMMEE.
    ep("la table des charges est consommee depuis la trace unique",
       "charges_tracees(vue)" in outil.read_text(encoding="utf-8"),
       "les charges sont relues autrement qu au domicile (M-076)")
    ep("une trace plus recente l emporte sur une plus ancienne",
       juge.dernieres_charges(VueFabrique([
           {"action": "charge", "mission": "MO-990", "date": veille},
           mission_lot])).get("MO-990", (None, None))[1] == frais,
       "la DERNIERE trace n est pas retenue")
    return ecarts


def _eprouver_age_sur_trace_de_service(racine):
    """MAILLON 74 (MO-501) : L AGE D UNE MISSION SE MESURE SUR SA TRACE DE SERVICE.

    LE DEFAUT, MESURE (le 2026-09-28 par le projet lui-meme, reproduit en boucle).
    `detecter_age_mission` calculait l age d une mission EN COURS sur son champ
    `chargee_le`. Or un LOT entier partage le meme `chargee_le` (fait ecrit dans le
    code de ce meme fichier) : une mission servie depuis DEUX MINUTES se lisait
    < en cours depuis 2.4 j >. Consequence : le rouge est NORMAL pendant toute la
    conduite d un lot arme, la suite est rouge du premier au dernier round, et
    chacun apprend a l ignorer -- exactement le motif que le createur a fait inverser
    en MO-487 (R-008 : un controle dont l etat normal est rouge s inverse).

    LE REMEDE EXISTAIT DEJA ET NE CONSUMAIT PERSONNE. `charges_tracees` (ecrit par la
    porte depuis le 2026-09-22) sait lire les actes `charge` -- le VRAI moment du
    service -- mais aucun appelant ne le consommait. Un remede ecrit et non consomme
    est une decision qui dort (regle immuable `evolution-decidee`) : c est la panne
    de ce depot, et elle se reproduit ici.

    CE QU IL EPROUVE, sur une VUE FABRIQUE (en memoire, aucun fichier de service) :
      - LE COBAYE : une mission servie il y a 2 min, dont `chargee_le` dit 3 jours,
        n est PAS accusee -- l age vient de la trace ;
      - LE CONTRE-TEMOIN : la MEME mission SANS trace de service (champ seul) EST
        accusee -- sans lui, le maillon passerait aussi bien avec un detecteur muet ;
      - LE REPLI : la source de l age est NOMMEE dans le fait accuse, donc un age
        sans horloge ne peut pas etre discute ;
      - LA LECTURE EST UNIQUE : l age passe par `dernieres_charges`, qui consomme
        `charges_tracees` -- une deuxieme lecture du journal divergerait (M-076).
    """
    import importlib.util
    import json
    from datetime import datetime, timedelta
    from pathlib import Path as _Chemin

    racine = _Chemin(racine).resolve()
    matrice = next((c for c in (racine, racine / "cerveau-projet" / "matrix", racine / "matrix")
                    if (c / "_operateur").is_dir()), None)
    if matrice is None:
        return ["matrix/ INTROUVABLE sous " + str(racine)]
    outil = (matrice / "_operateur" / "optimus-prime" / "super-combos" / "combos"
             / "outils" / "suivi-pilote.py")
    declaration = (matrice / "_operateur" / "optimus-prime" / "suivi-pilote"
                   / "pannes-declarees.json")
    for absent in (outil, declaration):
        if not absent.is_file():
            return ["INTROUVABLE : " + absent.name]

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    specification = importlib.util.spec_from_file_location("suivi_pilote_mo501", str(outil))
    juge = importlib.util.module_from_spec(specification)
    try:
        specification.loader.exec_module(juge)
    except Exception as erreur:  # noqa: BLE001
        return ["le suivi du pilote est ILLISIBLE (" + type(erreur).__name__ + " : "
                + str(erreur)[:80] + ")"]
    try:
        reglages = json.loads(declaration.read_text(encoding="utf-8"))
    except ValueError:
        return ["pannes-declarees.json ILLISIBLE (JSON invalide)"]

    maintenant = datetime.now()
    veille = (maintenant - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
    frais = (maintenant - timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S")

    class VueFabrique:
        """UNE vue de service, en MEMOIRE : c est elle qu on eprouve, jamais le disque."""

        def __init__(self, evenements):
            self.evenements = evenements
            self.maintenant = maintenant
            self.dernier_fait = {}

        def en_cours(self):
            return [{"id": "MO-990", "chargee_le": veille}]

    mission_lot = {"action": "charge", "mission": "MO-990", "date": frais}

    # LE COBAYE : la trace dit 2 min, le champ dit 3 jours. C'est le LOT.
    accusee_avec_trace = juge.detecter_age_mission(VueFabrique([mission_lot]), reglages, "")
    ep("COBAYE -- une mission servie depuis 2 min n est PAS accusee",
       accusee_avec_trace is None,
       "accusee alors que sa trace de service date de 2 min : " + str(accusee_avec_trace)[:130])
    # LE CONTRE-TEMOIN : pas de trace, le champ seul. Elle DOIT etre accusee.
    verdict = juge.detecter_age_mission(VueFabrique([]), reglages, "")
    ep("CONTRE-TEMOIN -- sans trace de service, la MEME mission EST accusee",
       verdict is not None,
       "muette : le detecteur ne mordrait sur rien (L-132)")
    if verdict is not None:
        ep("CONTRE-TEMOIN -- le fait nomme l horloge mesuree",
           "chargee_le" in str(verdict[2]),
           "l age est accuse sans dire d ou il sort : " + str(verdict[2])[:120])
    # LA LECTURE EST UNIQUE ET CONSOMMEE.
    ep("la table des charges est consommee depuis la trace unique",
       "charges_tracees(vue)" in outil.read_text(encoding="utf-8"),
       "les charges sont relues autrement qu au domicile (M-076)")
    ep("une trace plus recente l emporte sur une plus ancienne",
       juge.dernieres_chargees(VueFabrique([
           {"action": "charge", "mission": "MO-990", "date": veille},
           mission_lot])).get("MO-990", (None, None))[1] == frais,
       "la DERNIERE trace n est pas retenue")
    return ecarts


def _eprouver_les_trois_cases_exigees(pilote):
    """MAILLON 75 (EO-475 / MO-506) : LES TROIS CASES EXIGEES SONT PRESENTES ET ORDONEES.

    LE TROU, MESURE AVANT LA REPARATION. Le garde du MIROIR (theme <-> table) verifie
    l ACCORD, pas l EXISTENCE : retiree des DEUX cotes, la case [expertise] rendait un
    miroir VERT, une chaine de 9 maillons au lieu de 10, et la demande du createur
    disparaissait sans un mot. Le miroir est de plus UNIDIRECTIONNEL -- il parcourt les
    cases du THEME, donc une case que le theme perd et que la table garde passe aussi.
    Les deux cas sont DAUX : c est ce maillon qui les garde.

    Ce maillon joue le CONTROLE REEL, sur des copies EN MEMOIRE du parcours du
    createur : il n ecrit JAMAIS dans le theme. Une autorisation d ecrire n oblige pas a
    prendre le risque quand la meme fonction se prouve sans lui -- et la preuve est la
    meme, parce que c est le CONTROLE qui est joue, pas le fichier.

    Cobaye : une case exigee absente des DEUX cotes est ACCUSEE, et l accusation la
    NOMME. Contre-temoins : le parcours REEL est epargne ; les trois lais mais DANS LE
    desordre sont accuses ; un parcours vide accuse les TROIS (jamais une formule).
    Et la mission reste la DERNIERE ligne dans les quatre cas -- une accusee ajoutee ne
    doit jamais pousser la mission hors de la chaine.
    """
    # `importlib` n est PAS un module de niveau de ce fichier : chaque maillon qui
    # charge un domicile l importe ICI, dans son propre corps. Le mien l oubliait, et le
    # maillon REPORTAIT le defaut au lieu de faire tomber la suite -- mais un garde qui
    # ne joue pas ne prouve rien, meme en disant qu il ne joue pas.
    import importlib.util

    ecarts = []
    chemin = pilote / "filtrer" / "cadrage.py"
    if not chemin.is_file():
        return ["filtrer/cadrage.py INTROUVABLE : " + str(chemin)]
    sys.path.insert(0, str(pilote))
    try:
        specification = importlib.util.spec_from_file_location("cadrage_m75", chemin)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except Exception as erreur:  # noqa: BLE001
        return ["filtrer/cadrage.py ILLISIBLE (" + type(erreur).__name__ + " : "
                + str(erreur)[:60] + ")"]
    finally:
        sys.path.remove(str(pilote))

    controler = getattr(module, "controler_cases_exigees", None)
    if not callable(controler):
        return ["le controle controler_cases_exigees N EXISTE PAS : les trois cases "
                "exigees ne sont ni verifiees ni accusees"]
    exigees = tuple(getattr(module, "CASES_EXIGEES", ()))
    if exigees != ("expertise", "oui, mais...", "si j'etais user"):
        ecarts.append("la liste des cases exigees n est pas celle du createur : "
                      + str(exigees))

    def nom_de(cas):
        """Le NOM d une case est ce qui vit ENTRE les crochets de son besoin."""
        besoin = str(cas.get("besoin", ""))
        debut = besoin.find("[")
        fin = besoin.find("]", debut + 1) if debut >= 0 else -1
        return besoin[debut + 1:fin].strip() if (debut >= 0 and fin > debut) else ""

    def accuses(noms):
        rendus = controler(noms)
        if isinstance(rendus, list):
            return rendus
        return ["le controle ne rend pas une liste d ecarts : " + str(type(rendus))]

    # Le parcours REEL, lu par le DOMICILE (jamais recopie ici).
    reel = module.charger_cases()
    if reel is None:
        return ecarts + ["le parcours reel n est pas lisible : les contre-temoins ne "
                         "peuvent pas etre joues"]
    reel = [dict(cas) for cas in reel]

    # CONTRE-TEMOIN -- le parcours REEL, intact : il ne doit etre accuse de RIEN.
    trouves = accuses([nom_de(cas) for cas in reel])
    if trouves:
        ecarts.append("le parcours REEL est accuse alors qu il est intact : "
                      + " ; ".join(trouves[:3]))

    # COBAYE -- [expertise] retiree des DEUX cotes (le theme ET la table) : c est le
    # cas que le miroir seul ne voit pas. La table est restauree aussitot.
    table = getattr(module, "MAILLONS_DECLARES", ())
    sans_expertise = [cas for cas in reel if nom_de(cas) != "expertise"]
    trouves = accuses([nom_de(cas) for cas in sans_expertise])
    if not trouves:
        ecarts.append("COBAYE muet : une case exigee ABSENTE n est pas accusee -- le "
                      "trou d avant la reparation est revenu")
    elif not any("expertise" in t for t in trouves):
        ecarts.append("COBAYE partial : la case absente n est pas NOMMEE par "
                      "l accusation : " + " ; ".join(trouves[:3]))
    try:
        module.MAILLONS_DECLARES = tuple(t for t in table if t[0] != "expertise")
        maillons = module.constituer_la_chaine("T", "", sans_expertise)
        accusations_du_miroir = [m["case"] for m in maillons
                                if "NON DECLAREE" in str(m.get("objectif", ""))]
        accusations_du_controle = [m for m in maillons
                                   if m.get("case") == "cases-exigees"]
        # Le miroir DOIT rester MUET : c est ce silence qui prouve que le trou
        # existait. S il accuse, c est que le trou ne se reproduit plus et que ce
        # contre-temoin ne prouve plus rien -- il faut alors le dire, pas le passer.
        if accusations_du_miroir:
            ecarts.append("le miroir n est plus muet sur ce cas (il accuse "
                          + ", ".join(accusations_du_miroir[:3]) + ") : le "
                          "contre-temoin du maillon ne prouve plus le trou qu il doit "
                          "prouver")
        if not accusations_du_controle:
            ecarts.append("COBAYE muet sur la CHAINE : la case exigee absente des deux "
                          "cotes ne produit aucun maillon d accuse")
    finally:
        module.MAILLONS_DECLARES = table

    # CONTRE-TEMOIN -- les trois lais, mais DANS LE DESORDRE.
    trouves = accuses([nom_de(cas) for cas in reversed(reel)])
    if not trouves:
        ecarts.append("CONTRE-TEMOIN muet : les trois cases lais mais DESORDEES ne "
                      "sont pas accusees")
    elif not any("DESORDRE" in t for t in trouves):
        ecarts.append("le desordre n est pas accuse comme un desordre : "
                      + " ; ".join(trouves[:3]))

    # CONTRE-TEMOIN -- un parcours VIDE accuse les TROIS, nominativement.
    trouves = accuses([])
    if len(trouves) != 3:
        ecarts.append("un parcours vide doit accuses les TROIS cases : "
                      + str(len(trouves)) + " accusee(s) -- " + " ; ".join(trouves[:3]))

    # LA MISSION RESTE LA DERNIERE LIGNE, meme accusee : le controle AJOUTE une ligne
    # de reproche, il ne repousse pas la fin de la chaine.
    for nom, cases in (("temps-ordinal", reel), ("cobaye", sans_expertise),
                       ("desordre", list(reversed(reel))), ("vide", [])):
        try:
            maillons = module.constituer_la_chaine("T", "", [dict(c) for c in cases])
        except Exception as erreur:  # noqa: BLE001
            ecarts.append("la chaine ne se constitue plus sur le cas " + nom + " ("
                          + type(erreur).__name__ + " : " + str(erreur)[:60] + ")")
            continue
        if not maillons:
            ecarts.append("la chaine est VIDE sur le cas " + nom)
            continue
        if maillons[-1].get("case") != "mission":
            ecarts.append("la MISSION n est plus la derniere ligne sur le cas " + nom
                          + " (derniere : " + str(maillons[-1].get("case")) + ") -- le "
                          "controle a pousse la fin de la chaine hors de la chaine")
    return ecarts

def _eprouver_profil_en_fin_de_compte_rendu(zone):
    """MAILLON 76 (EO-480 / MO-507) : LE PROFIL SE SERT EN DERNIER, AU COMPTE-RENDU.

    LE FAUT, MESURE AVANT. La fiche `matrix/USER-PROFIL.md` etait remplie (Pseudo, Style
    de conversation) et son bloc voyageait avec la mission -- mais comme AJUSTABLE : la
    fiche technique rendait `profil : present (506 o)` et s arretait la. Un agent qui ne
    demandait pas `--complet` n avait donc JAMAIS le pseudo sous les yeux. La donnee
    arrivait et rien ne disait ce qu on en faisait : meme classe que la mesure du
    2026-09-21 (une fiche remplie que personne ne lisait), un cran plus loin.

    LA REPARATION. Un type de source `profil`, rendu par SON motif partage
    (matrice/data/commun/fiche_profil.py) -- jamais la fiche relue a cote, sinon deux
    verites. L entree est placee EN DERNIER de `apres-mission` : c est la decision
    createur, parce que le profil n a de sens qu au moment ou l agent s adresse a
    l utilisateur, et ce moment est le compte-rendu de fin.

    CE QUE CE MAILLON GARDE, ET CE QU IL NE GARDE PAS.
    - Il GARDE l ordre : le profil est le DERNIER de la phase, pas au milieu.
    - Il GARDE que la lecture vient du MOTIF : la source reelle est nommee dans le
      rendu, donc une fiche relue a cote se verrait.
    - Il GARDE qu il ne s est pas INVITE ailleurs : les trois autres phases du
      catalogue sont comptees, et toute occurrence du profil dans une phase anterieure
      ou parallele est une faute -- le createur a dit < on ajustera l injection par la
      suite >, donc ce maillon ne la fait pas a sa place, il la SIGNALE.
    - Il NE GARDE PAS le contenu du pseudo : une fiche vide est un etat de la fiche,
      pas un defaut de l injection.
    """
    import json
    import importlib.util
    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    catalogue = zone / "pilote" / "injection" / "config.json"
    if not catalogue.is_file():
        return ["injection/config.json INTROUVABLE : " + str(catalogue)]
    try:
        donnees = json.loads(catalogue.read_text(encoding="utf-8"))
    except (OSError, ValueError) as erreur:
        return ["injection/config.json ILLISIBLE (" + type(erreur).__name__ + " : "
                + str(erreur)[:60] + ")"]
    injections = donnees.get("injections") or {}
    entrees = injections.get("apres-mission") or []
    if not entrees:
        return ["la phase apres-mission est VIDE : le compte-rendu n a plus de rituel"]

    # LA PRESENCE, et la DERNIERE PLACE.
    ids = [str(e.get("id", "")) for e in entrees]
    ep("le profil est servi dans apres-mission",
       "profil-utilisateur" in ids,
       "le profil n est plus servi au compte-rendu : ids servis = " + ", ".join(ids))
    ep("le profil est servi EN DERNIER (decision createur)",
       bool(ids) and ids[-1] == "profil-utilisateur",
       "il est servi en position " + str(ids.index("profil-utilisateur") + 1)
       + " sur " + str(len(ids)) + " -- il doit etre le dernier, juste avant la remise")
    entree = entrees[ids.index("profil-utilisateur")] if "profil-utilisateur" in ids else {}
    ep("l entree porte le type `profil`, pas un chemin de fichier",
       entree.get("type") == "profil",
       "type = " + str(entree.get("type")) + " -- un chemin de fichier serait un second "
       "acces a la fiche, donc deux verites (M-076)")
    ep("l entree ne DECLARE PAS de source",
       not entree.get("source"),
       "elle declare source = " + str(entree.get("source")) + " : son domicile est le "
       "motif partage, pas un chemin du catalogue")

    # IL NE S EST PAS INVITE AILLEURS.
    for phase in ("demarrage", "avant-mission", "pendant-mission"):
        autres = [str(e.get("id", "")) for e in (injections.get(phase) or [])]
        ep("le profil n est pas servi dans " + phase,
           "profil-utilisateur" not in autres,
           "il y est servi : le createur a dit < on ajustera l injection par la suite >, "
           "donc la suite n a pas ete prise ici -- a trancher, pas a inventer")

    # LE RENDU, joue par le MOTEUR (jamais une reecriture de la regle).
    moteur = zone / "pilote" / "injection" / "injecter.py"
    if not moteur.is_file():
        return ecarts + ["injection/injecter.py INTROUVABLE : " + str(moteur)]
    sys.path.insert(0, str(moteur.parent))
    sys.path.insert(0, str(zone / "pilote"))
    try:
        specification = importlib.util.spec_from_file_location("injecter_m76", str(moteur))
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except Exception as erreur:  # noqa: BLE001
        sys.path.remove(str(zone / "pilote"))
        sys.path.remove(str(moteur.parent))
        return ecarts + ["injection/injecter.py ILLISIBLE (" + type(erreur).__name__
                         + " : " + str(erreur)[:60] + ")"]
    sys.path.remove(str(zone / "pilote"))
    sys.path.remove(str(moteur.parent))

    if not callable(getattr(module, "servir_profil", None)):
        return ecarts + ["le moteur ne rend pas le profil (servir_profil absent) : le "
                         "type est declare mais rien ne le joue"]
    texte, alertes, refus = module.servir(dict(entree), "texte")
    ep("le profil se rend sans REFUS ni ALERTE",
       not refus and not alertes,
       "refus = " + "; ".join(refus[:2]) + " | alertes = " + "; ".join(alertes[:2]))
    ep("le rendu DIT d ou viennent les donnees (le motif, pas une copie)",
       "USER-PROFIL.md" in texte or "PROFIL NON SERVI" in texte,
       "le rendu ne nomme aucune source : on ne sait pas d ou il vient")
    ep("le rendu PORTE la consigne d emploi (le bloc seul ne demandait rien)",
       "EMPLOI" in texte and "compte" in texte.lower(),
       "le bloc est servi muet : la donnee arrive et rien ne dit ce qu on en fait -- "
       "c est exactement le trou que EO-480 accuse")

    # CONTRE-TEMOIN : une fiche VIDE ne casse rien et ne se lit pas comme un profil
    # complet. On le prouve sur un chemin ABSENT, sans toucher la vraie fiche.
    try:
        from constantes import PLAFOND_PROFIL_TOKENS  # noqa: F401
    except Exception:  # noqa: BLE001
        pass
    ep("le moteur se tait JAMAIS sur une fiche absente",
       "PROFIL NON SERVI" in texte or "champs" in texte or "AVERTISSEMENT" in texte
       or "remplis" in texte,
       "le rendu ne dit rien de l etat de la fiche : un bloc muet se lirait comme un "
       "profil complet")
def _eprouver_les_quatre_portes_anti_heredoc(zone):
    """MAILLON 77 (demande createur 2026-09-30) : LES QUATRE PORTES ANTI-HEREDOC TIENNENT.

    LE FAUT, MESURE AVANT. Quatre dispositifs existent deja contre le heredoc :
      1. la porte EXECUTER refuse `<<` et nomme le recours (`--contenu-chemin @file`) ;
      2. le garde des COMMANDES DOCUMENTEES accuse `<<` ET `python -c` dans les blocs ;
      3. la porte ECRIRE/EDITER transporte le texte par `@fichier` ou en base64 (MO-376) ;
      4. la loi du round interdit d ecrire un fichier soi-meme, shell ou heredoc compris.
    Aucun maillon ne les JOUGAIT. Une porte qu on ne joue pas est une porte qu on ne sait
    pas fermer : elle peut etre relachee un soir de fatigue sans qu un seul signal parle.

    MESURES QUI FONDENT CE MAILLON (zone jetable, 2026-09-30, mesuree puis purgee) :
      - un heredoc contenant des triples quotes : code 1, stdout vide, stderr
        `<< ?tait inattendu` ; le MEME code ecrit dans un fichier puis joue : code 0.
        Le heredoc ne transporte donc pas le code, il le casse -- c est ce qui a fait
        echouer trois greffes de la session ;
      - le transport par quote tient a 8 000 caracteres et casse a 16 000 : le seuil
        est mesure, pas suppose (le `;` et l accent grave, eux, passent) ;
      - sur cette machine, le Python natif ne resout pas le chemin `/z/...` d un
        disque monte par une lettre (isfile = False) alors que la forme avec la
        LETTRE existe : les deux ne designent PAS le meme fichier. Tout script qui
        invoque le chemin `/z/` echoue en silence, sans message -- le chemin se
        deduit donc du REPERTOIRE, il ne s ecrit jamais en dur.

    CE QUE CE MAILLON GARDE. Il JOUE chaque porte (il ne la lit pas) : un refus
    exprimes pour un heredoc, un heresiasme constate sur un document construit pour
    l occasion, les deux transports de la porte d ecriture nommes, et la loi citee. Une
    porte qui cesse de refuser est un KO, pas un detail.

    CE QU IL NE GARDE PAS. Il ne juge pas les commandes que l agent tape : elles ne
    passent par aucune de ces quatre portes, et c est un fait, pas une defaillance
    d outil. Il ne dit pas non plus QUOI faire a la place -- le choix du transport
    appartient a celui qui ecrit.
    """
    import json
    import importlib.util
    import tempfile
    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    # -- PORTE 1 : EXECUTER refuse le heredoc ET nomme le recours ---------------
    executer = zone.parent.parent / "matrice" / "data" / "outils" / "executer"
    commun = executer / "commun.py"
    if not commun.is_file():
        return ["executer/commun.py INTROUVABLE : " + str(commun)]
    # `commun.py` fait `from constants import ...` : le module `constants` est deja
    # dans sys.modules (un autre outil l a charge), et Python lui donne CEUX-LA.
    # D ou l ImportError du premier essai. On retire les GLISSANTS le temps du
    # chargement et on les REMET ensuite : meme motif que les maillons voisins,
    # rien n est laisse derriere (ni chemin, ni module en cache).
    glissants = ("constants", "commun")
    sauve = {}
    for nom in glissants:
        if nom in sys.modules:
            sauve[nom] = sys.modules.pop(nom)
    if str(executer) not in sys.path:
        sys.path.insert(0, str(executer))
    module_commun = None
    try:
        specification = importlib.util.spec_from_file_location("commun_m77", str(commun))
        module_commun = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module_commun)
    except Exception as erreur:  # noqa: BLE001
        for nom in glissants:
            sys.modules.pop(nom, None)
        sys.modules.update(sauve)
        if str(executer) in sys.path:
            sys.path.remove(str(executer))
        return ["executer/commun.py ILLISIBLE (" + type(erreur).__name__ + " : "
                + str(erreur)[:60] + ")"]

    valide, message = module_commun.valider_commande("python3 -c print(1) <<EOF")
    ep("la porte EXECUTER refuse un heredoc",
       not valide, "elle ACCEPTE un heredoc : le code part en argument et le shell le mange")
    ep("le refus NOMME le recours (pas un 'non' nu)",
       "--contenu-chemin" in message,
       "le refus dit seulement " + repr(message) + " -- l agent est bloque sans porte de sortie")
    for interdit, pourquoi in (("|", "pipe"), (">", "redirection")):
        if interdit == "|":
            ok, quoi = module_commun.valider_commande("python3 script.py | tee a.txt")
        else:
            ok, quoi = module_commun.valider_commande("python3 script.py > a.txt")
        ep("la porte EXECUTER refuse la " + pourquoi, not ok,
           "elle accepte : le shell reprend la main et la sortie n est plus lisible")
    for nom in glissants:
        sys.modules.pop(nom, None)
    sys.modules.update(sauve)
    if str(executer) in sys.path:
        sys.path.remove(str(executer))

    # -- PORTE 2 : le garde des commandes accuse, sur un document CIBLE -------
    garde = zone / "super-combos" / "combos" / "outils" / "verifier-commandes.py"
    if not garde.is_file():
        return ecarts + ["verifier-commandes.py INTROUVABLE : " + str(garde)]
    try:
        specification = importlib.util.spec_from_file_location("garde_cmd_m77", str(garde))
        module_garde = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module_garde)
        function_examiner = getattr(module_garde, "examiner", None)
        ep("le garde des commandes peut etre JOUE (examiner est appelable)",
           callable(function_examiner),
           "examiner est absent : la porte n est plus jouable, seulement lisible")
        if callable(function_examiner):
            with tempfile.TemporaryDirectory() as trou:
                document = Path(trou) / "cobaye.md"
                document.write_text(
                    "```\npython3 - <<PYEOF\nprint(1)\nPYEOF\n```\n"
                    "```\npython3 -c \"print(1)\"\n```\n"
                    "```\npython3 cerveau-projet/matrix/lancer.py --lister\n```\n",
                    encoding="utf-8")
                verdicts = function_examiner(document)
                accuses = [v[2] for v in verdicts]
                ep("le garde ACCUSE le heredoc d un document",
                   any("heredoc" in a for a in accuses),
                   "sur un document construit pour lui, il n accuse rien : "
                   + str(accuses)[:80])
                ep("le garde ACCUSE le code en ARGUMENT (python -c)",
                   any("-c" in a for a in accuses),
                   "sur un document construit pour lui, il n accuse rien : "
                   + str(accuses)[:80])
                ep("le garde LAISSE PASSER la commande correcte (il ne condamne pas tout)",
                   not any("heredoc" in accuse or "-c" in accuse
                           for numero, cmd, accuse in verdicts
                           if cmd.endswith("--lister")),
                   "il accuse une commande correcte : un garde trop large est un garde ignore")
    except Exception as erreur:  # noqa: BLE001
        ecarts.append("le garde des commandes est ILLISIBLE au maillon ("
                      + type(erreur).__name__ + " : " + str(erreur)[:60] + ")")

    # -- PORTE 3 : les DEUX transports de la porte d ecriture sont la ---------
    racine_matrice = zone.parent.parent / "matrice" / "data" / "outils" / "ecrire"
    texte_outils = ""
    for candidat in sorted(racine_matrice.rglob("*.py")):
        if ".bak" in candidat.name:
            continue
        try:
            texte_outils += candidat.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
    ep("la porte d ecriture transporte par FICHIER (@fichier)",
       "@fichier" in texte_outils or "@fichier" in texte_outils.replace("@file", "@fichier"),
       "aucun transport par fichier : le texte long n aurait pas de porte")
    ep("la porte d ecriture transporte en BASE64 (chaine hostile)",
       "base64" in texte_outils,
       "aucun transport base64 : un guillemet imbrique n aurait pas de porte")

def _eprouver_le_jugement_des_citations(zone):
    """MAILLON 78 (EO-479 / MO-508) : LE JUGEMENT DES CITATIONS A UN SEUL DOMICILE.

    LE FAUT, MESURE AVANT. Trois instruments de la meme maison jugeaient les
    citations d index, TROIS fois. `verifier-protocoles` portait la regle
    correcte (chemins relatifs reconnus jusqu au bout, zone des sources
    exemptee ET dite, MO-489) ; ses deux jumeaux portaient un motif qui ne
    captait que le NOM de fichier. Mesure du 2026-09-30, sur une ligne de table
    fantome de la zone des sources :
      - protocoles  : hors_champ = ['<docs/...>.md : cible ABSENTE'], morts = []
      - conventions : morts = ['<docs/...>.md']     <-- le ROUGE sans remede
      - regles      : idem
    Le rouge sans remede est le pire des deux : la porte ECRIRE -- seul passage
    d ecriture -- REFUSE la zone des sources en la nommant (zone_sources.py,
    MO-377). Un garde qui exige une ecriture que la porte du meme domaine
    interdit ne garde rien : il fabrique un rouge permanent.

    LA REPARATION EST UN DEPLACEMENT, PAS UN AJOUT. Ajouter l exemption aux
    deux jumeaux aurait porte la regle a QUATRE endroits, et la prochaine
    divergence aurait ete inevitable. Elle vit maintenant au DOMICILE UNIQUE
    `data/commun/jugement_citations.py` (M-076), que les trois consomment --
    y compris la FORMULATION de ce qui est dit, et l affichage DIT lui-meme,
    qui n existait que chez protocoles.

    CE QUE CE MAILLON GARDE, ET CE QU IL NE GARDE PAS.
    - Il GARDE l unicite : un des trois qui porte encore son propre motif de
      citation, ou une copie du jugement, est un KO -- une regle a quatre
      domiciles redeviendrait divergente.
    - Il GARDE que le jugement MORD : une vraie citation morte reste ACCUSEE
      par les trois. Une reparation qui eclaircit trop rend muet.
    - Il GARDE que le contre-temoin est EPARNE : une citation de la zone des
      sources n entre JAMAIS dans les morts, et sort DITE, mesuree.
    - Il GARDE que les trois PRONONCENT LA MEME CHOSE sur la meme ligne.
    - Il NE GARDE PAS le contenu des index reels : le garde tourne sur des
      lignes de table construites pour l occasion, jamais sur l arbre vivant.
    """
    import importlib.util
    import tempfile
    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    racine_outils = zone.parent.parent / "matrice" / "data" / "outils"
    racine_commun = zone.parent.parent / "matrice" / "data" / "commun"
    if not racine_outils.is_dir():
        return ["matrice/data/outils INTROUVABLE : " + str(racine_outils)]
    outils = ("verifier-conventions", "verifier-protocoles", "verifier-regles")

    # -- L UNICITE, lue sur le disque (avant de jouer quoi que ce soit) ------
    for outil in outils:
        chemin = racine_outils / outil / "commun.py"
        if not chemin.is_file():
            ecarts.append(outil + "/commun.py INTROUVABLE : " + str(chemin))
            continue
        texte = chemin.read_text(encoding="utf-8")
        tete = texte.split("def verifier_index")[0]
        ep(outil + " ne porte plus son PROPRE motif de citation",
           "MOTIF" not in tete,
           "il redemarre encore par un motif local : la regle a deux domiciles")
        ep(outil + " consomme le domicile partage",
           "jugement_citations" in texte,
           "rien ne consomme jugement_citations.py : son verifier_index reste sa copie")
    for outil in outils:
        chemin = racine_outils / outil / "verifier" / "fonctions.py"
        if not chemin.is_file():
            ecarts.append(outil + "/verifier/fonctions.py INTROUVABLE : " + str(chemin))
            continue
        texte = chemin.read_text(encoding="utf-8")
        ep(outil + " ne porte plus sa PROPRE formulation du DIT",
           "MESUREE, jamais accusee" not in texte,
           "il formule encore l exemption lui-meme : deux formulations, donc deux verites")

    # -- LE JUGEMENT JOUE, sur des lignes de table construites pour l occasion
    outillage = [str(racine_outils), str(racine_commun)]
    glissants = ("constants", "commun", "jugement_citations", "cible", "zone_sources")
    sauve = {}
    for nom in glissants:
        if nom in sys.modules:
            sauve[nom] = sys.modules.pop(nom)
    for chemin in outillage:
        if chemin not in sys.path:
            sys.path.insert(0, chemin)
    with tempfile.TemporaryDirectory() as trou:
        document = Path(trou) / "index-cobaye.md"
        document.write_text(
            "| mort | ../../../matrice/data/fichier-qui-nexiste-pas.md | x |\n"
            "| source | ../../../docs/une-source-du-createur.md | x |\n"
            "| presente | ../../../docs/IMPERATIF.md | x |\n",
            encoding="utf-8")
        lignes = document.read_text(encoding="utf-8").splitlines()
        mort = [l for l in lignes if "fichier-qui-nexiste-pas" in l]
        source = [l for l in lignes if "une-source-du-createur" in l]
        presente = [l for l in lignes if "IMPERATIF" in l]
        for outil in outils:
            dossier = racine_outils / outil
            for nom in ("constants", "commun"):
                sys.modules.pop(nom, None)
            sys.path.insert(0, str(dossier))
            try:
                specification = importlib.util.spec_from_file_location(
                    "commun_m78", str(dossier / "commun.py"))
                module = importlib.util.module_from_spec(specification)
                specification.loader.exec_module(module)
            except Exception as erreur:  # noqa: BLE001
                ecarts.append(outil + " n a pas pu charger commun.py ("
                              + type(erreur).__name__ + " : " + str(erreur)[:60] + ")")
                continue
            finally:
                if str(dossier) in sys.path:
                    sys.path.remove(str(dossier))
            lister = None
            for candidat in sorted(dir(module)):
                if candidat.startswith("lister_fichiers"):
                    lister = getattr(module, candidat)
                    break
            if not callable(lister) or not callable(getattr(module, "verifier_index", None)):
                ecarts.append(outil + " n expose ni sa liste de fichiers ni verifier_index")
                continue
            reels = lister()
            # (1) LA VRAIE MORTE EST ACCUSEE -- le cobaye mord
            morts = module.verifier_index(mort, reels)[1]
            ep(outil + " accuse la vraie citation morte",
               any("fichier-qui-nexiste-pas.md" in m for m in morts),
               "morts = " + str(morts) + " : la reparation a eclairci le jugement "
               "au point de le rendre muet")
            # (2) LA SOURCE EST EPARGNE ET DITE -- le contre-temoin
            absents, hors = module.verifier_index(source, reels)[1:]
            ep(outil + " n accuse JAMAIS la source ABSENTE du createur",
               absents == [],
               "morts = " + str(absents) + " : la porte ECRIRE refuse cette zone, "
               "le rouge serait sans remede")
            ep(outil + " DIT la source absente (elle ne se tait pas)",
               len(hors) == 1 and "cible ABSENTE" in hors[0],
               "hors_champ = " + str(hors) + " : une exemption muette est un angle mort (MO-075)")
            # (3) LA SOURCE PRESENTE EST EPARGNEE ET DITE COMME PRESENTE
            absents2, hors2 = module.verifier_index(presente, reels)[1:]
            ep(outil + " n accuse JAMAIS la source PRESENTE",
               absents2 == [],
               "morts = " + str(absents2) + " : une source qui existe est citee legitimement")
            ep(outil + " DIT la source PRESENTE comme presente",
               len(hors2) == 1 and "cible PRESENTE" in hors2[0],
               "hors_champ = " + str(hors2) + " : la mesure doit distinguer presente de absente")
    for nom in glissants:
        sys.modules.pop(nom, None)
    sys.modules.update(sauve)
def _decider_doc_par_domicile(briques, textes, groupes):
    """DECISION PURE : quelles briques ne sont documentees par AUCUNE des listes.

    Trois listes decrivent le parc outils et aucune ne se comparait. Ce controle
    ne prend que des NOMS et des TEXTES, jamais un chemin.

    Les groupes sont la partie qui compte. Une brique peut n etre nommee par sa
    seule presence, alors que son DOMICILE porte une fiche de GROUPE qui la
    couvre -- c est le cas de la couche native `data/commun` : la fiche 22 du
    manuel les decrit par role, jamais par nom. Sans la declaration des groupes,
    ce controle accuserait 20 modules tres bien documentes, et un controle qui
    accuse faux est un controle que l on finit par ignorer.

    Retourne (accuses, groupes_couverts).
    """
    accuses = []
    groupes_couverts = []
    for brique in briques:
        nom = brique.get("nom", "")
        domicile = brique.get("domicile", "")
        if not nom:
            continue
        if any(texte is not None and nom in texte for texte in textes):
            continue
        couvert = False
        for nom_groupe, domiciles in groupes.items():
            if domicile in domiciles:
                couvert = True
                if nom_groupe not in groupes_couverts:
                    groupes_couverts.append(nom_groupe)
                break
        if not couvert:
            accuses.append(nom)
    return accuses, groupes_couverts


def _constats_doc_par_domicile(briques, textes):
    """Les memes faits, par DOMICILE : la couverture se LIT avant d etre jugee.

    Un total global ne dit rien de DECI : il peut masquer un domicile sans
    couverture derriere un autre a couverture parfaite. Le detail par domicile
    est ce qui rend la divergence lisible -- une comparaison des listes n a de
    sens que si l on sait OU elle bite.
    """
    par_domaine = {}
    for brique in briques:
        domicile = brique.get("domicile", "?")
        nom = brique.get("nom", "")
        compte = par_domaine.setdefault(domicile, [0, 0])
        compte[0] += 1
        if any(texte is not None and nom and nom in texte for texte in textes):
            compte[1] += 1
    return par_domaine


def _eprouver_la_fraicheur_des_vues(zone):
    """MAILLON 82 (MO-568) : UNE VUE DE SUIVI PERIMEE EST ACCUSEE, AVEC SA PORTE.

    LE FAUT, MESURE AVANT. Les vues de suivi sont REGENERABLES : elles se
    regenerent par une porte, donc A LA DEMANDE -- et une porte qu on ne joue
    pas ne se signale pas. Une vue perimee garde sa date, ses chiffres et sa
    mise en page : rien ne distinguait "mesure a 04:10" de "mesure a hier". Le
    lecteur qui la consultait recevait des FAITS MORTS, bien mis en page -- le
    pire etat pour un instrument, celui qui a l air de repondre.

    LA REPARATION. La porte `fraicheur-vues.py` lit une DECLARATION
    (`suivi-parties/frais-declarees.json`) qui nomme, par vue : la porte qui la
    regenere, ses SOURCES, le DELAI au-dela duquel elle est perimee, et le COUT
    de la rafraichir. Elle mesure le RETARD entre le sceau de la vue et la
    source la plus recente, et ACCUSE en nommant la porte a jouer.
    Trois refus, et ils sont choisis :
    - elle ne REGENERE rien -- rafraichir une vue est une decision, et le faire
      en douce effacerait la preuve qu elle etait perimee ;
    - elle ne DEVINE ni porte, ni source, ni seuil : les trois sont declares ;
    - elle ne juge pas l URGENCE : elle donne le fait et le prix, la decision
      de relire ou de regenerer reste au lecteur.

    LE NOM `retard_secondes`, ET PAS `age_secondes`. Une collision de homonyme
    avec un autre `age_secondes` du parc faisait tressaillir la mesure du
    2026-10-03 : le nombre affiche etait celui d une AUTRE vue, sans qu on le
    voie. Ici le nom dit ce qu il mesure -- l ECART entre la source et la vue.

    CE QUE CE MAILLON GARDE, ET CE QU IL NE GARDE PAS.
    - Il GARDE que la porte ACCUSE : sur un fait FABRIQUE (vue dont le sceau
      est anterieur a sa source) le maillon appelle la fonction de la porte
      lui-meme et exige le verdict `perime` ET une accusation qui NOMME la
      porte a jouer. Le contre-temoin exige le meme appel sur une vue a jour et
      exige qu elle passe.
    - Il GARDE qu elle EPARGNE ce qui n est pas une faute : un sceau en avance
      (retard negatif) n est pas une peremption.
    - Il GARDE que le SILENCE est impossible : une vue sans sceau, une vue
      declaree absente, une source declaree introuvable sont accusees et
      NOMMEES, jamais ignorees.
    - Il GARDE que la declaration se LIT et que les vues REELLEMENT declarees
      sont mesurees -- une declaration introuvable, malformee, ou vide de vues
      est un echec du maillon, pas un "zero vue".
    - Il GARDE L ANGLE MORT (MO-571) : la porte DECOUVRE les vues par un
      PERIMETRE declare (racines + motif + exclusions motives), et accuse
      toute vue du perimetre que la declaration ne nomme pas. Sans ce point, une
      vue neuve etait invisible PAR CONSTRUCTION : personne ne l accuse, donc
      personne ne la declare, donc elle le reste. Le maillon exige donc qu une
      vue presente et non declaree soit ACCUSEE et nommee, qu une exclusion ne
      soit pas accusee a tort, et que les exclusions soient DITES meme quand
      leur fichier a disparu (une exclusion muette se ferme au premier
      renommage).
    - Il NE GARDE PAS le CONTENU des vues : une vue peut dire des choses fausses
      tant qu elle porte un sceau. Sa justesse est celle de la porte qui la
      regenere, pas de ce maillon.
    """
    import importlib.util
    import json
    import os
    import shutil
    import tempfile
    from datetime import datetime, timedelta

    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    outil = zone / "super-combos" / "combos" / "outils" / "fraicheur-vues.py"
    if not outil.is_file():
        return ["fraicheur-vues.py INTROUVABLE : " + str(outil)]

    # (1) L AUTO-TEST DE LA PORTE, joue dans son PROPRE sous-processus.
    auto = subprocess.run([sys.executable, str(outil), "--auto-test"],
                         capture_output=True, text=True)
    sortie = (auto.stdout or "").strip().splitlines()
    ep("auto-test de la porte", "AUTO-TEST : 12/12." in (auto.stdout or ""),
       "la porte ne dit pas 12/12 (code " + str(auto.returncode) + ") : "
       + (sortie[-1] if sortie else "(aucune sortie)"))

    # (2) LA MESURE REELLE, en JSON : c est ce que le maillon consomme.
    reel = subprocess.run([sys.executable, str(outil), "--json"],
                          capture_output=True, text=True)
    donnees = None
    try:
        donnees = json.loads(reel.stdout or "")
    except ValueError as erreur:
        ecarts.append("la porte ne rend pas de JSON -> " + str(erreur)[:80])
    if donnees is not None:
        ep("declaration lue", donnees.get("nb_vues", 0) > 0,
           "la declaration ne declare AUCUNE vue : rien ne sera jamais accuse")
        # Une vue reellement PERIMEE est un echec du maillon : c est
        # exactement ce que la porte existe pour dire.
        for entree in donnees.get("a_jouer") or []:
            ecarts.append("vue a rafraichir -> " + str(entree.get("id")) + " : "
                          + str(entree.get("porte")) + " (retard "
                          + str(entree.get("retard_secondes")) + " s)")
        ep("aucune vue non declaree", not donnees.get("non_declarees"),
           "vues presentes dans le perimetre et jamais declarees : "
           + ", ".join(donnees.get("non_declarees") or []))

    # (3) LE CONTRE-TEMOIN, joue par le MAILLON sur des faits FABRIQUES : il
    # appelle la FONCTION de la porte, pas son rapport, donc il ne se fie ni a
    # son auto-test ni a son code de sortie.
    spec = importlib.util.spec_from_file_location("fraicheur_vues_mesure", outil)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    base = Path(tempfile.mkdtemp(prefix="maillon82-"))
    try:
        moment = datetime(2026, 10, 4, 4, 10, 0)
        (base / "vue.md").write_text("Mesure du 2026-10-04 04:10:00 | fines : 3\n",
                                     encoding="utf-8", newline="\n")
        source = base / "source.txt"
        source.write_text("x", encoding="utf-8")
        # La source a bouge 3600 s APRES le sceau : la vue est perimee.
        stamp = (moment + timedelta(seconds=3600)).timestamp()
        os.utime(source, (stamp, stamp))

        def vue(sources, tolerance=300):
            return {"id": "fabrique", "fichier": "vue.md", "porte": "porte-a-jouer",
                    "tolerance_secondes": tolerance, "frais": {"valeur": 1.0},
                    "sources": sources}

        mesure = module.mesurer_vue(vue(["source.txt"]), base)
        ep("la porte accuse une vue perimee", mesure.get("verdict") == "perime",
           "verdict " + repr(mesure.get("verdict")) + " au lieu de perime")
        ep("l accusation NOMME la porte a jouer",
           "porte-a-jouer" in str(mesure.get("accusation")),
           "l accusation ne nomme pas la porte : " + repr(mesure.get("accusation")))
        ep("le retard est mesure, pas devine",
           isinstance(mesure.get("retard_secondes"), int)
           and mesure["retard_secondes"] >= 3599,
           "retard " + repr(mesure.get("retard_secondes")))

        # LE CONTRE-TEMOIN : la source a bouge de 5 s APRES le sceau, donc la
        # vue a 5 s de retard -- sous sa tolerance de 300 s, elle passe.
        # (5 s AVANT le sceau donnerait un retard NEGATIF, donc `en_avance` :
        # ce serait eprouver autre chose que ce qu on croit eprouver. C est
        # precisement ce que le premier jet faisait -- et le maillon l a vu.)
        stamp = (moment + timedelta(seconds=5)).timestamp()
        os.utime(source, (stamp, stamp))
        mesure = module.mesurer_vue(vue(["source.txt"]), base)
        ep("contre-temoin : une vue a jour passe", mesure.get("verdict") == "a_jour",
           "verdict " + repr(mesure.get("verdict")) + " au lieu de a_jour")

        # ET LE SCEAU EN AVANCE, qui n est pas une faute : source anterieure
        # au sceau, donc retard negatif.
        stamp = (moment - timedelta(seconds=5)).timestamp()
        os.utime(source, (stamp, stamp))
        mesure = module.mesurer_vue(vue(["source.txt"]), base)
        ep("un sceau en avance n est pas une peremption",
           mesure.get("verdict") == "en_avance",
           "verdict " + repr(mesure.get("verdict")) + " au lieu de en_avance")

        # Le SILENCE : une vue sans sceau, une source introuvable, une vue
        # declaree absente -- tous trois doivent etre ACCUSES et NOMMES.
        (base / "muette.md").write_text("Aucune date ici.\n", encoding="utf-8",
                                        newline="\n")
        sans_sceau = dict(vue(["source.txt"]), fichier="muette.md")
        mesure = module.mesurer_vue(sans_sceau, base)
        ep("une vue sans sceau est accusee", mesure.get("verdict") == "illisible",
           "verdict " + repr(mesure.get("verdict")))

        mesure = module.mesurer_vue(vue(["source-absente.txt"]), base)
        ep("une source declaree introuvable est NOMMEE",
           mesure.get("verdict") == "illisible"
           and "source-absente.txt" in str(mesure.get("accusation")),
           "verdict " + repr(mesure.get("verdict")) + " / "
           + repr(mesure.get("accusation")))

        mesure = module.mesurer_vue(dict(vue(["source.txt"]), fichier="absente.md"), base)
        ep("une vue declaree absente est nommee", mesure.get("verdict") == "absente",
           "verdict " + repr(mesure.get("verdict")))

        # --- L ANGLE MORT : une vue PRESENTE et non declaree doit etre
        # ACCUSEE. Sans ce contre-temoin, le perimetre pourrait disparaitre et
        # le maillon resterait vert : on ne verrait plus que les vues
        # declarees, c est a dire celles qu on a deja vues.
        (base / "vues" / "regles").mkdir(parents=True)
        (base / "vues" / "suivi-neuve.md").write_text(
            "Mesure du 2026-10-04 04:10:00 | fines : 0\n",
            encoding="utf-8", newline="\n")
        (base / "vues" / "regles" / "suivi-marbre.md").write_text(
            "suivi- mais pas un visuel\n",
            encoding="utf-8", newline="\n")
        perimetre = {"racines": ["vues"],
                     "motif": "^suivi-[a-z0-9-]*\\.md$",
                     "exclus": [{"fichier": "vues/regles/suivi-marbre.md",
                                 "motif": "MARBRE"}]}
        non_declarees, exclus = module.accuser_non_declarees(
            {"vues": [], "perimetre": perimetre}, base, "declaration.json")
        ep("une vue PRESENTE et non declaree est accusee et nommee",
           [l["fichier"] for l in non_declarees] == ["vues/suivi-neuve.md"]
           and non_declarees[0]["verdict"] == "non_declaree",
           non_declarees)
        ep("une exclusion n est pas accusee a tort, et son motif est DIT",
           not any("marbre" in l["fichier"] for l in non_declarees)
           and exclus and exclus[0]["motif"] == "MARBRE",
           (non_declarees, exclus))
        perimetre["exclus"].append({"fichier": "vues/gone.md", "motif": "deja absent"})
        _l, exclus = module.accuser_non_declarees(
            {"vues": [], "perimetre": perimetre}, base, "declaration.json")
        ep("une exclusion dont le fichier est ABSENT reste dite",
           any("gone.md" in e["fichier"] for e in exclus), exclus)
    finally:
        shutil.rmtree(base, ignore_errors=True)

    return ecarts


def _parc_resolvable(matrice):
    """Les noms que le LANCEUR sait joindre -- sa source de verite, importee.

    On importe le module lui-meme plutot que de recopier son parcours : une copie
    diverge en silence, et c'est precisement ce que ce maillon doit attraper. Le
    bytecode n'est pas ecrit (`dont_write_bytecode`) :.control-attribution refuse
    les `__pycache__` du parc, un maillon ne doit pas en creer un.
    """
    import importlib
    commun = matrice / "matrice" / "data" / "commun"
    if not commun.is_dir():
        return None
    ajoute = str(commun) not in sys.path
    if ajoute:
        sys.path.insert(0, str(commun))
    avant = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        import resolution_outils
        importlib.reload(resolution_outils)
        return set(resolution_outils.noms_connus())
    except Exception:
        return None
    finally:
        sys.dont_write_bytecode = avant
        if ajoute:
            try:
                sys.path.remove(str(commun))
            except ValueError:
                pass


def _forme_nom(nom):
    """Le nom COMPARABLE : deux formes, un seul nom.

    Le REGISTRE nomme une brique-scripts par son nom de FICHIER (`x.py`) ; le
    LANCEUR rend le nom de la brique (`x`). Comparer les formes brutes accusait
    80 briques sur 135 -- un maillon qui accuse trop est un maillon qu on coupe,
    exactement comme un garde qui mord deux fois a tort sans jamais mordre.
    """
    texte = str(nom or "")
    return texte[:-3] if texte.endswith(".py") else texte


def _servies_introuvables(briques, resolubles):
    """Les briques DECLAREES servies a l'injection que le lanceur ne joint pas.

    LA CLASSE NUEVE (MO-575). Le parc se decrit deux fois -- au registre des outils
    (`servi_a_l_injection`) et dans le parcours du lanceur -- et rien ne comparait
    les DEUX. L'angle mort du sens " declarees et introuvables " laisse le
    controle existant (briques du parc absentes du registre) passer : il ne voit
    que l'autre sens. Consequence mesuree : trois BDD servies a l'injection que le
    lanceur REFUSAIT sous le nom qu'elles portent -- une porte qui parle sans agir.

    Un brique declaree NON servie et introuvable n'est PAS accusee ici : ce cas
    appartient au controle du sens oppose, et le confondre ferait compter deux fois
    le meme ecart.
    """
    return sorted(str(brique.get("nom") or "") for brique in briques
                  if brique.get("servi_a_l_injection")
                  and _forme_nom(brique.get("nom")) not in resolubles)


import sys
sys.dont_write_bytecode = True


def _depot_git_contamine(racine, decision=None):
    """Le depot git abide-t-il de SA convention ? Rend (ecarts, faits).

    EO-529. La convention dit ce qui contamine un depot : les points de
    restauration `.bak.*`, les jetables, les `__pycache__`. Elle nomme ces
    familles par NOM -- donc le controle les LIT la, il ne les redecrit pas.

    CE QUE CE MAILLON FAIT, ET POURQUOI IL EXISTE : la doctrine du depot
    n est un texte que si quelque chose la fait appliquer. C est le meme
    schema que le vice `or True` corrige le 2026-10-03 et que
    `nonsens_publies` : un instrument juste et non lu reste un tiers du
    travail. Ici l instrument MANQUE, donc la convention etait muette.

    MESURE, PAS INTUITION (2026-10-04) : 1083 points de restauration
    `.bak.*` sont SUIVIS par git. Ils ne sont pas la faute de la
    convention -- ils la PRECEDENT. Ce maillon les nomme donc comme un
    ETAT A RAMENER, pas comme une faute de la doctrine.

    LA LECTURE EST DERIVEE ET REPLAYABLE : le maillon se joue sur une
    racine qu on lui donne. Sur le depot reel il accuse ce qui existe ;
    sur une racine cobaye il accuse ce qu on y a mis. C est ce qui
    permet de prouver qu il MORD sans fabriquer un faux etat dans le
    depot du createur.
    """
    import subprocess as _sp

    racines = [racine]
    # CONTRE-TEMOIN D ABORD : un depot VIDE doit ressortir muet, sinon le
    # maillon accuse l absence de commits comme une contamination.
    codes = [_sp.run(["git", "-C", str(r), "ls-files"], capture_output=True)
             for r in racines]
    if not codes or codes[0].returncode != 0:
        return [], []

    # Les familles sont declarees ICI, lisiblement, et la convention les
    # nomme aussi : une famille ajoutee a la convention doit l etre ici.
    familles = (
        ("point de restauration", ".bak."),
        ("jetable", "tmp-optimus/"),
    )
    ecarts = []
    faits = []
    for famille, marqueur in familles:
        nombre = 0
        exemples = []
        for code in codes:
            for chemin in code.stdout.decode("utf-8", "replace").splitlines():
                if marqueur in chemin:
                    nombre += 1
                    if len(exemples) < 3:
                        exemples.append(chemin)
        if nombre:
            ecarts.append(
                famille + " : " + str(nombre) + " fichier(s) suivi(s) par git -- "
                "la convention `convention-depot-git.md` (EO-529) les ecarte")
            for chemin in exemples:
                faits.append("    " + famille + " : " + chemin)
    return ecarts, faits


def _file_de_missions_sans_trou(zone, decision=None):
    """La file de missions se suit-elle, et son COMPTEUR dit-il la verite ?

    MESURE (2026-10-04, MO-579). Un `git checkout --` de l agent a ramene une
    version anterieure de `file-missions-optimus.json` : cinq fiches ont disparu
    (MO-575 a MO-579) et le compteur est revenu de 579 a 574. La non-regression
    est restee VERTE pendant toute la perte, parce qu'AUCUN maillon ne lisait ce
    fichier. Un fichier que rien ne lit peut perdre ce qu'il contient sans que
    personne ne le sache -- c'est le motif ecrit-mais-non-lu, TROISIEME fois dans
    ce round (apres `or True` et `nonsens_publies`).

    CE QUE CE MAILLON MESURE, deux faits qui ne se remplacent pas :
      (a) LA CONTINUITE -- un identifiant MO-xxx absent entre deux presents est
          un TROU. La file est une suite ordonnee : un trou ne se comble pas tout
          seul, il se rebouche par une reconstitution qui doit etre dite.
      (b) LE COMPTEUR -- il doit valoir le PLUS GRAND identifiant present. Un
          compteur en deca, c'est un identifiant deja attribuable : la prochaine
          mission chargee reprendrait un numero deja pris, c'est-a-dire un id
          REUTILISE (le cas que `enregistrer` documente pour MO-045 a MO-048).

    LA LECTURE EST DERIVEE ET REPLAYABLE : le maillon se joue sur une racine qu on
    lui donne, il n'a aucun litteral de chemin. Sur un depot reel il mesure ; sur
    une racine cobaye il accuse ce qu on y a mis -- c'est ce qui prouve qu il
    MORD sans fabriquer un faux etat chez le createur.

    LE CONTRE-TEMOIN EST DANS LE JEU : un fichier qui declare lui-meme des trous
    (cobaye) sort muet si on le croit, et le maillon sort KO quand on le croit
    VRAI. Un controle qui ne peut pas etre trompe par ce qu'il annonce ne prouve
    rien.
    """
    import json as _json

    fichier = zone / "_operateur" / "optimus-prime" / "pilote" / "file-missions-optimus.json"
    if not fichier.is_file():
        return [], []
    try:
        donnees = _json.loads(fichier.read_text(encoding="utf-8"))
    except (OSError, ValueError) as erreur:
        return ["fichier ILLISIBLE : " + type(erreur).__name__
                + " -- une file qu on ne lit pas est une file qu on ne surveille pas"], []
    missions = donnees.get("missions") or []
    ecarts, faits = [], []
    nombres = []
    for mission in missions:
        identifiant = str(mission.get("id") or "")
        numero = None
        if identifiant.startswith("MO-"):
            chiffres = identifiant[3:]
            if chiffres.isdigit():
                numero = int(chiffres)
        if numero is not None:
            nombres.append(numero)
    nombres_tries = sorted(set(nombres))
    # (a) LA CONTINUITE : les trous entre le plus petit et le plus grand.
    trous = []
    if nombres_tries:
        for attendu in range(nombres_tries[0], nombres_tries[-1] + 1):
            if attendu not in nombres_tries:
                trous.append(attendu)
    if trous:
        nommage = ", ".join("MO-" + str(n) for n in trous[:8])
        ecarts.append("continuite : " + str(len(trous)) + " identifiant(s) ABSENT(S) de la file ("
                      + nommage + (" ..." if len(trous) > 8 else "")
                      + ") -- une fiche perdue ne se rebouche pas seule")
        faits.append("    trou : de MO-" + str(min(trous)) + " a MO-" + str(max(trous))
                     + " (" + str(len(trous)) + " identifiant(s))")
    # (b) LE COMPTEUR : il vaut le plus grand identifiant present.
    compteur = donnees.get("compteur")
    if isinstance(compteur, int) and nombres_tries and compteur < max(nombres_tries):
        ecarts.append("compteur : " + str(compteur) + " alors que MO-"
                      + str(max(nombres_tries)) + " existe -- la prochaine mission "
                      "chargee reprendrait un identifiant DEJA ATTRIBUE")
        faits.append("    compteur en deca : " + str(compteur) + " < MO-"
                     + str(max(nombres_tries)))
    return ecarts, faits


def _eprouver_les_nonsens_bloquants(racine):
    """MAILLON 84 (MO-577) : une CONDITION TOUJOURS VRAIE dans le parc est ACCUSEE.

    LE MANQUE MESURE. `table-ronde.py` (MO-573) sait deja mesurer trois familles
    de defauts que le lecteur ne voit pas, et la premiere est la nete :
    `CONDITION TOUJOURS VRAIE` -- un `or True`, un `and False` ou une comparaison
    d un operande pur a lui-meme. Il les PUBLIE dans `nonsens_publies`.

    MAIS PERSONNE NE LES LISAIT. Mesure du 2026-10-04 : ce maillon n existait
    pas, et `sc-006-lacunes/main.py` portait depuis son commit un `or True` dans
    un auto-test -- sa branche ne pouvait pas echouer, donc l auto-test passait sur
    une sortie FAUSSE et le lisait pour rien. L instrument etait correct et sa
    mesure juste : le vice a survecu parce que le resultat n etait relie a AUCUN
    maillon bloquant. C est le schema de MO-528 (un instrument livre sans
    appelant) ; ici l appelant existe mais n exigeait rien.

    LA REPARTITION DU POUVOIR EST RESPECTEE. La regle de detection N EST PAS
    recopiee ici : ce maillon IMPORTE et CONSOMME le domicile (M-076, L-029).
    Une deuxieme implementation deriverait en silence de la premiere -- et le
    desaccord serait muet, ce qui est exactement le vice qu on combat.

    LE PERIMETRE EST DIT, jamais suppose : la mesure porte sur les trois
    domaines que `table-ronde.py` declare lui-meme, et le maillon REND ce compte.
    Un controle qui ne dit pas ce qu il a lu ne peut pas rendre un zero credible.
    """
    import importlib.util
    sys.dont_write_bytecode = True
    # LE DOMICILE EST JOINT PAR SON MARQUEUR, jamais par un indice de parent :
    # la zone de l operateur est la seule qui porte `parcours/themes`, et c est
    # exactement le repere que le lanceur a deja resolu (L-013).
    chemin_domicile = None
    base = Path(racine)
    for zone in (base / "cerveau-projet" / "matrix" / "_operateur"
                 / "optimus-prime",
                 base / "_operateur" / "optimus-prime",
                 base):
        if not (zone / "parcours" / "themes").is_dir():
            continue
        candidat = zone / "super-combos" / "combos" / "outils" / "table-ronde.py"
        if candidat.is_file():
            chemin_domicile = candidat
            break
    if chemin_domicile is None:
        return ["table-ronde.py INTROUVABLE : le domicile de la mesure est absent"], []
    spec = importlib.util.spec_from_file_location("table_ronde_nonsens",
                                                   chemin_domicile)
    if spec is None or spec.loader is None:
        return ["table-ronde.py ILLISIBLE : " + str(chemin_domicile)], []
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as erreur:      # un domicile casse doit etre DIT, pas masquer
        return ["table-ronde.py ne s importe pas : "
                + type(erreur).__name__ + " -- " + str(erreur)[:120]], []
    mesurer_nonsens = getattr(module, "_faux_publies", None)
    if mesurer_nonsens is None:
        return ["table-ronde.py n expose pas _faux_publies : "
                "le maillon ne peut plus consommer la regle"], []

    # --- LA DECISION EST PURE : le domicile repond sur des faits FABRIQUES ----
    #    Un seul cas suffit, et c est celui qui a survecu : la tautologie dans
    #    une condition. Le CONTRE-TEMOIN compte autant que le cobaye -- sans lui,
    #    un detecteur qui accuse tout serait accepte aussi facilement.
    cobaye = "x = 1 if a or True else 2" + chr(10) + "x"
    trouvees, lisible = module._nonsens_dans_source(cobaye, "<cobaye-maillon-84>")
    if not lisible:
        return ["le domicile ne lit pas le cobaye : la regle n est pas eprouvee"], []
    if not any(c.get("famille") == "CONDITION TOUJOURS VRAIE" for c in trouvees):
        return ["la decision ne mord pas : le cobaye "
                + repr(cobaye.splitlines()[0]) + " n est pas accuse"], []
    temoin = "x = 1 if a else 2" + chr(10) + "x"
    temoins, _ = module._nonsens_dans_source(temoin, "<contre-temoin-maillon-84>")
    if any(c.get("famille") == "CONDITION TOUJOURS VRAIE" for c in temoins):
        return ["la decision accuse a tort : une condition qui depend de ses "
                "entrees est designee toujours vraie"], []

    # --- LA DONNEE REELLE : le parc, mesure par le domicile -----------------
    resultat = mesurer_nonsens()
    ecarts = []
    faits = [str(resultat.get("fichiers_lus", 0)) + " fichier(s) lu(s) par le "
             "domicile, sur les domaines qu il declare"]
    illisibles = resultat.get("illisibles") or []
    trouves = resultat.get("trouves") or []
    if illisibles:
        ecarts.append(str(len(illisibles)) + " fichier(s) ILLISIBLES : l AST les a "
                      "refuses -- un fichier non mesure ne passe pas pour sain")
    for trouve in trouves:
        ecarts.append(str(trouve.get("famille", "?")) + " : "
                      + str(trouve.get("fichier", "?")) + " ligne "
                      + str(trouve.get("ligne", "?")) + " -- "
                      + str(trouve.get("extrait", ""))[:80])
    if not trouves and not illisibles:
        faits.append("aucun nonsens dans le parc : les conditions testent "
                     "quelque chose")
    return ecarts, faits


def _eprouver_les_briques_servies_introuvables(racine):
    """MAILLON 83 (MO-575) : DECLARE SERVIE A L INJECTION ET introuvable, c'est ACCUSE."""
    import json
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "matrice" / "data").is_dir()), None)
    if matrice is None:
        return ["matrice/data/ INTROUVABLE sous " + str(racine)], []
    registre = matrice / "matrice" / "data" / "registre-outils.json"
    if not registre.is_file():
        return ["registre-outils.json INTROUVABLE : " + str(registre)], []
    try:
        briques = json.loads(registre.read_text(encoding="utf-8")).get("outils", [])
    except ValueError as erreur:
        return ["registre-outils.json ILLISIBLE : " + str(erreur)], []
    if not isinstance(briques, list) or not briques:
        return ["registre-outils.json ne porte AUCUNE brique : rien a comparer"], []
    resolubles = _parc_resolvable(matrice)
    if resolubles is None:
        return ["resolution_outils INTROUVABLE ou illisible sous " + str(matrice)], []

    # --- LA DECISION EST PURE : trois cas, dont deux contre-temoins ----------
    cobayes = [{"nom": "outil-servi-resolu", "servi_a_l_injection": True},
               {"nom": "outil-servi-absent", "servi_a_l_injection": True},
               {"nom": "outil-servi-absent.py", "servi_a_l_injection": True},
               {"nom": "outil-servi-resolu.py", "servi_a_l_injection": True},
               {"nom": "outil-muet-absent", "servi_a_l_injection": False}]
    charges = _servies_introuvables(cobayes, {"outil-servi-resolu"})
    if charges != ["outil-servi-absent", "outil-servi-absent.py"]:
        return ["la decision ne mord pas : accuses = " + str(charges)], []

    ecarts = []
    faits = []
    reelles = _servies_introuvables(briques, resolubles)
    servis = sum(1 for b in briques if b.get("servi_a_l_injection"))
    faits.append(str(len(resolubles)) + " nom(s) joignable(s) par le lanceur, "
                + str(servis) + " brique(s) declaree(s) servie(s) a l injection")
    for nom in reelles:
        ecarts.append("brique DECLAREE servie a l injection et introuvable au lanceur : "
                      + nom)
    if not reelles:
        faits.append("aucune brique servie n est introuvable")
    return ecarts, faits


def _eprouver_doc_des_outils(racine):
    """MAILLON 81 (MO-534) : LES TROIS LISTES DU PARC OUTILS SE COMPARENT.

    LE MANQUE MESURE. Le parc outils est decrit TROIS fois, jamais compare :
      - `matrice/data/registre-outils.json` -- les briques, GENEREES par la
        porte `registre-outils` (la seule des trois veridiques par
        construction) ;
      - `matrice/data/manuel-outils.md` -- des FICHES, dont plusieurs sont des
        fiches de GROUPE (une fiche pour un domicile entier) ;
      - `.../combos/outils/outils-readme.md` -- le readme de la zone des outils
        transverses.
    Mesure du 2026-10-03 : une large part des briques sont nommees dans l une
    des deux markdown, et le reste PARAIT des oublies -- dont 20 modules de la
    couche native et 20 outils transverses, tous couverts par une fiche de
    groupe. Un controle naif les accuserait tous : 58 trous inexistants. Les
    4 VRAIS sans doc (`benchmark`, `chaine-pense-bete`, `maintenir`,
    `passerelle-demandes`) sont, eux, invisibles : rien ne les comparait.

    Ce maillon joue la DECISION pure (quatre cas, deux contre-temoins) puis la
    DONNEE REELLE, et il en LAISSE les faits visibles au lieu de se borner a un
    code : la divergence est un COMPTE, pas une faute.
    """
    import json
    from pathlib import Path as _Chemin
    racine = _Chemin(racine)
    candidats = [racine, racine / "cerveau-projet" / "matrix", racine / "matrix"]
    matrice = next((c for c in candidats if (c / "matrice" / "data").is_dir()), None)
    if matrice is None:
        return ["matrice/data/ INTROUVABLE sous " + str(racine)], []
    registre = matrice / "matrice" / "data" / "registre-outils.json"
    manuel = matrice / "matrice" / "data" / "manuel-outils.md"
    readme = (matrice / "_operateur" / "optimus-prime" / "super-combos" / "combos"
              / "outils" / "outils-readme.md")
    for chemin in (registre, manuel, readme):
        if not chemin.is_file():
            return ["fichier INTROUVABLE : " + str(chemin)], []
    try:
        donnees = json.loads(registre.read_text(encoding="utf-8"))
    except ValueError as erreur:
        return ["registre-outils.json ILLISIBLE : " + str(erreur)], []
    briques = donnees.get("outils", [])
    if not isinstance(briques, list) or not briques:
        return ["registre-outils.json ne porte AUCUNE brique : rien a comparer"], []
    textes = [manuel.read_text(encoding="utf-8"), readme.read_text(encoding="utf-8")]

    # Les groupes sont DECLARES ici, dans le controle, et non deduits : un groupe
    # deduit du texte serait une invention du controle (une liste de mots qui
    # ressemble a un nom d outil). La liste dit precisement ce qu elle couvre.
    groupes = {"Modules partages": ("matrice/data/commun",)}

    faits = []
    ecarts = []

    # --- LA DECISION EST PURE : quatre cas, dont deux CONTRE-TEMOINS ---------
    cobayes = [{"nom": "outil-documente", "domicile": "matrice/data/outils"},
               {"nom": "outil-oublie", "domicile": "matrice/data/outils"},
               {"nom": "module-natif", "domicile": "matrice/data/commun"}]

    # 1. TEMOIN NEGATIF : l'outil sans mention est ACCUSE, l'ecrit est laisse.
    charges, _ = _decider_doc_par_domicile(cobayes, ["outil-documente"], groupes)
    if charges != ["outil-oublie"]:
        return ["la decision ne mord pas : accuses = " + str(charges)], []

    # 2. TEMOIN POSITIF : le groupe COUVRE le module, le controle se TAIT, et
    #    il DIT quel groupe il a couvert (un silence serait muet).
    charges, groupes_tous = _decider_doc_par_domicile(cobayes, ["outil-documente"], groupes)
    if "module-natif" in charges or "Modules partages" not in groupes_tous:
        return ["la decision de groupe ne tient pas (charges " + str(charges)
                + ", groupes " + str(groupes_tous) + ")"], []

    # 3. CONTRE-TEMOIN : SANS groupe, le module natif EST accuse. C est ce qui
    #    prouve que le groupe fait le travail et non une coincidence.
    charges_sans_groupe, _ = _decider_doc_par_domicile(cobayes, ["outil-documente"], {})
    if "module-natif" not in charges_sans_groupe:
        return ["le groupe ne change rien : le contre-temoin ne prouve pas le groupe"], []

    # 4. CONTRE-TEMOIN : un texte ABSENT (None, fichier manquant) ne doit pas
    #    accuser une brique qui est ecrite dans l AUTRE liste.
    charges_texte_manquant, _ = _decider_doc_par_domicile(
        [{"nom": "outil-documente", "domicile": "matrice/data/outils"}],
        [None, "outil-documente"], {})
    if charges_texte_manquant:
        return ["un texte absent accuse a tort une brique documentee ailleurs"], []

    # --- LA DONNEE REELLE : la divergence se LIT, elle ne se cache pas -------
    charges_reels, _ = _decider_doc_par_domicile(briques, textes, groupes)
    par_domaine = _constats_doc_par_domicile(briques, textes)
    dans_les_deux = 0
    for brique in briques:
        nom = brique.get("nom", "")
        if not nom:
            continue
        if sum(1 for texte in textes if texte and nom in texte) > 1:
            dans_les_deux += 1
    faits.append(str(len(briques)) + " briques au registre")
    faits.append(str(len(charges_reels)) + " sans aucune mention (groupes inclus)")
    faits.append(str(dans_les_deux) + " nommees dans les DEUX listes")
    for domicile in sorted(par_domaine):
        compte, couvertes = par_domaine[domicile]
        faits.append("%-46s %4d briques, %4d nommees" % (domicile, compte, couvertes))
    return ecarts, faits


def _eprouver_la_ligne_du_head(zone):
    """MAILLON 79 (audit createur 2026-09-30) : LA LIGNE DU HEAD DIT CE QU ELLE COMPTE.

    LE FAUT, MESURE AVANT. La ligne d entete de `suivi-optimus.md` alignait trois
    chiffres sur UNE seule ligne, et ils ne parlaient pas du meme livre :
      - `tracees` et `finies` comptaient le JOURNAL DE SUIVI (data/suivi-optimus.jsonl) ;
      - `en attente` comptait la FILE du pilote, puis un AUTRE journal
        (historiques-missions-optimus.jsonl).
    Aucun chiffre n etait faux pris isolement -- c est ce qui rendait le defaut
    invisible. Le createur lisait `455 finies` et `0 en attente`, les deux
    vraisembles, et n avait aucun moyen de savoir qu ils ne parlaient pas du meme
    livre. Mesure : 34 missions de la file (MO-252...MO-283) ne figuraient dans
    AUCUNE des trois colonnes -- ni tracees, ni finies, ni en attente.

    ET LE TROU VRAI, DANS LE MEME CHANTIER. `ACTION_REPORT` (EO-190) neutralise un
    `debut` SANS produire de `fin` : une mission reportee n est ni terminee ni a
    faire. Entre `finies` et `en attente` elle n avait AUCUNE colonne : elle
    disparaissait de la ligne. Le `0 en attente` restait exact, et la mission
    restait invisible.

    LA REPARATION. Chaque chiffre porte desormais le nom de sa source, la ligne
    DIT laquelle parle, et `ouvertes` se calcule PAR SOUSTRACTION
    (tracees - finies) : une mission reportee ne peut plus disparaitre, elle
    passe dans `ouvertes`, ce qui est vrai. Les deux populations -- le travail
    fait et le travail a faire -- restent deux colonnes : elles sont LEGITIMEMENT
    differentes, et les fusionner aurait menti autrement.

    CE QUE CE MAILLON GARDE.
    - Il GARDE que la ligne NOMME ses sources : une colonne sans source dans la
      legende est une colonne dont on ne peut pas verifier le sens.
    - Il GARDE l INVARIANT `tracees = finies + ouvertes` sur l arbre REEL, en
      relisant le fichier publie et en le comparant a sa source. C est la seule
      preuve qu un visuel genere reste fidele.
    - Il GARDE que le `debut` et le `fin` du dernier evenement sont comptes :
      une vue qui affiche 2144 sur une source de 2145 est un visuel FAUX, meme
      si tout le reste est juste. Mesure du defaut : exactement ce decalage.
    - Il NE GARDE PAS le contenu du travail : la vue le montre, il ne le juge pas.
    """
    import json
    ecarts = []

    def ep(nom, condition, detail):
        if not condition:
            ecarts.append(nom + " -> " + detail)

    racine = zone.parent.parent
    vue = zone / "suivi-optimus.md"
    source = racine / "matrice" / "data" / "suivi-optimus.jsonl"
    if not vue.is_file():
        return ["suivi-optimus.md INTROUVABLE : " + str(vue)]
    if not source.is_file():
        return ecarts + ["suivi-optimus.jsonl INTROUVABLE : " + str(source)]

    texte = vue.read_text(encoding="utf-8")
    lignes = texte.splitlines()
    # ON NE FILTRE PAS SUR UN PREFIXE DE LIGNE ICI. Le garde des extractions
    # (`verifier-extraction-ecarts`) mesure tout filtre de prefixe applique a une
    # sortie decoupee en lignes, et exige qu un producteur imprime ce prefixe. Il
    # a raison de le voir : un filtre doit dire d ou vient sa ligne. On localise
    # donc la LIGNE PAR SON CONTENU, sans passer par un filtre de prefixe.
    entete = ""
    donnees = ""
    for ligne in lignes:
        if ligne[:1] == "|" and "Derniere mise a jour" in ligne and not entete:
            entete = ligne
        elif (entete and not donnees and ligne[:1] == "|"
              and ligne.strip("| -") != ""):
            donnees = ligne
    # La PREMIERE cellule est un horodatage, pas un nombre : on le garde pour la
    # comparaison, mais il ne doit pas passer dans la boucle des entiers (un
    # controle qui convertit une date en nombre echoue sur une vue correcte --
    # c'est un garde qui fabrique du rouge, pas un garde qui garde).
    if not entete or not donnees:
        return ecarts + ["la ligne du head est INTROUVABLE (en-tete ou donnees manquantes)"]

    # -- LA LIGNE NOMME SES SOURCES -----------------------------------------
    # On verifie que la legende NOMME les deux populations, en cherchant les noms
    # EXACTS des colonnes du head (casse comprise) plutot qu une formulation
    # libre : un test qui depend d une casse posee par l auteur du test est un
    # test qui casse sur une reecriture legitime de la legende.
    ep("la ligne du head DIT ce que chaque colonne compte",
       "NE PARLENT PAS DU MEME LIVRE" in texte
       and "JOURNAL DE SUIVI" in texte
       and "file du pilote" in texte.lower(),
       "la legende ne nomme plus les sources : une colonne sans source ne se "
       "verifie pas (attendu : 'journal de suivi' et 'file du pilote')")

    colonnes = [c.strip() for c in donnees.strip().strip("|").split("|")]
    en_tetes = [c.strip() for c in entete.strip().strip("|").split("|")]
    if len(colonnes) != len(en_tetes):
        return ecarts + ["la ligne et son en-tete n ont pas le meme nombre de colonnes ("
                         + str(len(en_tetes)) + " / " + str(len(colonnes)) + ")"]
    horodatage = colonnes[0] if colonnes else ""
    nombres = [None]
    for valeur in colonnes[1:]:
        try:
            nombres.append(int(valeur))
        except ValueError:
            nombres.append(None)
    par_nom = dict(zip(en_tetes, nombres))

    # -- L INVARIANT, sur l ARBRE REEL ---------------------------------------
    for nom_attendu in ("Evenements", "Missions tracees", "Missions finies",
                        "Missions ouvertes", "File du pilote"):
        ep("la colonne " + nom_attendu + " existe",
           nom_attendu in par_nom,
           "colonnes trouvees : " + ", ".join(en_tetes))
    # La DATE est un horodatage assume (sa place est None) : le test ne porte que
    # sur les cellules CHIFFREES. Un controle qui accuse la date de ne pas etre un
    # nombre accuse une vue correcte.
    if any(v is None for v in nombres[1:]):
        return ecarts + ["une cellule chiffree du head n est pas un nombre : " + donnees]
    evenements_reels = sum(1 for l in source.read_text(encoding="utf-8").splitlines()
                           if l.strip())
    ep("le head compte autant d evenements que la source en porte",
       par_nom.get("Evenements") == evenements_reels,
       "head = " + str(par_nom.get("Evenements")) + " | source = " + str(evenements_reels)
       + " : un visuel genere en retard est un visuel FAUX, meme si le reste est juste")
    tracees = par_nom.get("Missions tracees")
    finies = par_nom.get("Missions finies")
    ouvertes = par_nom.get("Missions ouvertes")
    ep("l invariant tracees = finies + ouvertes tient",
       tracees is not None and finies is not None and ouvertes is not None
       and tracees == finies + ouvertes,
       "l invariant ne se calcule pas : tracees = " + repr(tracees)
       + " | finies = " + repr(finies) + " | ouvertes = " + repr(ouvertes)
       + " -- une mission disparait entre les colonnes (le cas est le `report`, EO-190)")

    # -- LE CONTRE-TEMOIN : une mission REPORTEE reste visible ---------------
    evenements = [json.loads(l) for l in source.read_text(encoding="utf-8").splitlines()
                  if l.strip()]
    with_report = {e.get("mission") for e in evenements
                   if e.get("mission") and e.get("action") == "report"}
    if with_report:
        non_finies = {e.get("mission") for e in evenements
                      if e.get("mission") and e.get("action") != "fin"}
        ep("une mission REPORTEE est comptee comme ouverte, jamais comme terminee",
           with_report <= non_finies,
           "des missions reportees (" + str(len(with_report)) + ") ne sont ni finies ni "
           "ouvertes : elles ont disparu de la ligne")
    return ecarts


    for chemin in outillage:
        if chemin in sys.path:
            sys.path.remove(chemin)
    return ecarts


    # -- PORTE 4 : la loi du round l INTERDIT, et elle est la ------------------
    loi = zone / "protocoles" / "proto-12-loi-du-round.md"
    if loi.is_file():
        texte_loi = loi.read_text(encoding="utf-8")
        ep("la loi interdit d ecrire un fichier soi-meme (shell OU heredoc)",
           "heredoc" in texte_loi and "porte ECRIRE" in texte_loi,
           "la loi ne cite plus le heredoc : l interdiction a ete elargie sans le dire")
    else:
        ecarts.append("proto-12-loi-du-round.md INTROUVABLE : " + str(loi))
    return ecarts


    return ecarts


def main():


    parser = argparse.ArgumentParser(description="Non-regression zone Optimus")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    args = parser.parse_args()

    racine = Path(args.racine).resolve()
    zone = None
    for cand in (racine, racine / "cerveau-projet" / "matrix" / "_operateur" / "optimus-prime"):
        if (cand / "parcours" / "themes").is_dir():
            zone = cand if cand.name == "optimus-prime" else cand / "cerveau-projet" / "matrix" / "_operateur" / "optimus-prime"
            break
    if zone is None or not zone.is_dir():
        # racine est peut-etre deja la zone ou son parent direct
        cand = racine / "_operateur" / "optimus-prime"
        if (cand / "parcours" / "themes").is_dir():
            zone = cand
    if zone is None or not (zone / "parcours" / "themes").is_dir():
        print(f"Zone Optimus introuvable depuis {args.racine}")
        return 2

    outils = zone / "super-combos" / "combos" / "outils"
    themes = sorted((zone / "parcours" / "themes").glob("theme-*.json"))
    ko = []

    # 0. PRE-VOL -- A JOUR AVANT DE LANCER (correction 2026-09-14).
    #    Ces trois controles repondent a UNE question : "ai-je mis a jour ce que la
    #    suite va lire ?" -- frictions qualifiees, fichiers TRACES, remorque
    #    attellee. Ils vivaient au MILIEU de la suite (etape 5) : on parcourait
    #    donc TOUT (py_compile, themes, cartographe, garde-ascii, flux, attente,
    #    trace, anti-spam, chapitres, exemptions, rotation, historique,
    #    observations, passes, sc-001) avant d'apprendre qu'une friction n'etait
    #    pas qualifiee -- puis on corrigeait, puis on RELANCAIT. Des actions
    #    inutiles, payees DEUX fois (constate deux fois le 2026-09-14 : un faux
    #    vert de sc-001 et le garde de cadence).
    #    L'ORDRE impose est : on MODIFIE le code, on MET A JOUR les frictions, on
    #    LANCE, et si ca passe on continue. Le pre-vol fait respecter cet ordre :
    #    il s'arrete ICI, avant toute action couteuse, en nommant QUOI mettre a
    #    jour et PAR QUELLE PORTE.
    print("== 0. PRE-VOL (a jour avant de lancer) ==")
    pre_vol = [
        ([zone / "espions" / "espion-integrite-optimus.py", "verifier"], "integrite",
         "tracer les fichiers modifies (bdd-modifications noter) PUIS reposer la"
         " reference (espion-integrite-optimus enregistrer)"),
        ([zone / "espions" / "espion-activite-optimus.py"], "activite",
         "QUALIFIER les frictions AVANT de lancer : bdd-frictions archiver --id <id>"
         " --statut valide|annule --raison \"...\""),
        ([zone / "remorque" / "remorque-optimus.py", "etat"], "remorque",
         "declarer l'equipement (outils-readme + remorque-optimus inventorier)"),
    ]
    def ligne_accusation(sortie):
        """Premiere ligne ACCUSATRICE de la sortie d un controle (EO-226).

        Prendre la DERNIERE ligne etait un indice qui MENTAIT : la remorque
        accuse un equipement (UNE ligne) puis DIT ses points de restauration
        (59 lignes le 2026-09-19) -- le pre-vol nommait donc un .bak EXEMPTE au
        lieu du vrai coupable, et envoyait reparer un fichier innocent. Une
        accusation qui designe le mauvais fichier coute plus cher qu aucune
        accusation (friction 77, L-055).
        """
        lignes = [l.strip() for l in sortie.splitlines() if l.strip()]
        for ligne in lignes:
            if ligne[0] in "-+":
                return ligne
        return lignes[-1] if lignes else "?"

    pre_vol_ko = []
    for commande, nom, remede in pre_vol:
        if not Path(commande[0]).is_file():
            print(f"  {nom}: ABSENT ({Path(commande[0]).name})")
            pre_vol_ko.append(f"{nom}: binaire absent ({Path(commande[0]).name})")
            continue
        resultat = lancer_enfant([sys.executable, str(commande[0]), *commande[1:]],
                                  capture_output=True, text=True)
        etat = "OK" if resultat.returncode == 0 else "KO"
        print(f"  {nom}: {etat}")
        if resultat.returncode != 0:
            detail = ligne_accusation(resultat.stdout)
            pre_vol_ko.append(f"{nom}: {detail}")
            print(f"        -> A FAIRE AVANT DE LANCER : {remede}")
    if pre_vol_ko:
        print("")
        print("VERDICT KO (PRE-VOL) : la suite n'a PAS ete lancee -- mets a jour ce qu'elle")
        print("lit, PUIS relance. Lancer d'abord oblige a corriger ensuite et a relancer :")
        print("on paie deux fois (friction 29, 2026-09-14).")
        for ecart in pre_vol_ko:
            print(f"  - {ecart}")
        return 1

    # 1. py_compile sur tous les .py d outils (hors dossiers-outils et pycache)
    print("== 1. py_compile ==")
    py_files = [p for p in outils.rglob("*.py") if "__pycache__" not in p.parts]
    ko_py = []
    for p in py_files:
        try:
            py_compile.compile(str(p), doraise=True)
        except py_compile.PyCompileError as e:
            ko_py.append(f"{p.name}: {e}")
    print(f"  {len(py_files) - len(ko_py)}/{len(py_files)} OK")
    ko += [f"py_compile: {x}" for x in ko_py]

    # 2. tester-theme sur chaque theme
    print("== 2. tester-theme ==")
    for t in themes:
        r = lancer_enfant([sys.executable, str(outils / "tester-theme.py"), str(t)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  {t.name}: {etat}")
        if r.returncode != 0:
            ko.append(f"tester-theme {t.name}: {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else '?'}")

    # 3. cartographe
    print("== 3. cartographe ==")
    r = lancer_enfant([sys.executable, str(outils / "cartographe-matrice.py"), "--racine", str(zone)],
                       capture_output=True, text=True)
    etat = "OK" if r.returncode == 0 else "KO"
    print(f"  carte: {etat}")
    if r.returncode != 0:
        ko.append("cartographe: cibles manquantes")

    # 4. garde-ascii sur la zone
    print("== 4. garde-ascii ==")
    r = lancer_enfant([sys.executable, str(outils / "garde-ascii.py"), str(zone)],
                       capture_output=True, text=True)
    etat = "OK" if r.returncode == 0 else "KO"
    print(f"  ascii: {etat}")
    if r.returncode != 0:
        ko.append("garde-ascii: violations")

    # 5. espions + remorque (zone, invisible cameleon : outil en zone,
    #    execute par Optimus seul, resultats en BDD/suivi de zone)
    print("== 5. espions + remorque ==")
    zone_scripts = [
        zone / "espions" / "espion-integrite-optimus.py",
        zone / "espions" / "espion-activite-optimus.py",
        zone / "remorque" / "remorque-optimus.py",
    ]
    for script in zone_scripts:
        if not script.is_file():
            print(f"  {script.name}: ABSENT")
            ko.append(f"manquant: {script.name}")
            continue
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as e:
            print(f"  {script.name}: COMPILE KO")
            ko.append(f"py_compile: {script.name}")
            continue
        print(f"  {script.name}: compile OK")
    # Les trois CONTROLES des espions et de la remorque ne sont plus ici : ils sont
    # devenus le PRE-VOL (etape 0), parce qu'ils repondent a "ai-je mis a jour ce
    # que la suite va lire ?" et qu'une suite qui parcourt tout avant de le dire
    # fait payer deux fois la meme correction (friction 29, 2026-09-14). Il ne
    # reste ici que leur COMPILATION, qui est le controle de la zone.

    # 6. PREFIXES (contrat fondamental CV-009 / CV-011) : une famille d ids =
    #    UN prefixe, aucun prefixe partage entre deux familles, aucun prefixe
    #    declare MORT re-emis. BLOQUANT : le doublon C- a survecu des mois sans
    #    qu'aucune suite ne se plaigne -- celle-ci ne le laissera plus passer.
    print("== 6. prefixes ==")
    verificateur = outils / "verifier-contrat-fondamental.py"
    if not verificateur.is_file():
        print("  prefixes: ABSENT")
        ko.append("manquant: verifier-contrat-fondamental.py")
    else:
        r = lancer_enfant([sys.executable, str(verificateur), "prefixes"],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  prefixes: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("ECART")]
            ko.append("prefixes: " + ("; ".join(ecarts) if ecarts else "voir verifier-contrat-fondamental.py"))

    # 7. FLUX (imperatif 62 / E-095) : la chaine peut-elle porter une mission ?
    #    Une suite qui ne surveille que les fichiers ne voit pas une chaine
    #    rompue (pilote muet, boucle qui ne finit plus, brin perime).
    print("== 7. flux ==")
    lanceur_flux = outils / "lanceur-non-regression-flux.py"
    if not lanceur_flux.is_file():
        print("  flux: ABSENT")
        ko.append("manquant: lanceur-non-regression-flux.py")
    else:
        # La racine du FLUX est matrix/, jamais le dossier courant : le flux
        # traverse la Matrice entiere. Passer `racine` (le cwd) faisait echouer ce
        # maillon pour une raison de DOSSIER COURANT -- "Dossier matrix/
        # introuvable sous ...\optimus-prime" -- donc a CHAQUE execution, toujours
        # pour la meme fausse raison : un controle qu'on apprend a ignorer ne
        # garde plus rien (2026-09-13).
        racine_flux = zone.parent.parent
        r = lancer_enfant([sys.executable, str(lanceur_flux), "--racine", str(racine_flux)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  flux: {etat}")
        if r.returncode != 0:
            lignes = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("- MAILLON")]
            ko.append("flux rompu: " + ("; ".join(lignes) if lignes else "voir lanceur-non-regression-flux.py"))

        # EO-404 / MO-478 : le maillon 3 du flux doit LIRE sa table, jamais la
        # recopier -- c'est ce qui a laisse quatre routines hors surveillance
        # pendant une journee. Sa suite porte donc deux autotests, et ils sont
        # REJOUES ici : un garde que personne ne joue n'en est pas un.
        for drapeau, libelle in (("--autotest", "autotest maillon 7 (fantomes)"),
                                 ("--autotest-maillon3", "autotest maillon 3 (table entretenue)"),
                                 ("--autotest-pid-serveur", "autotest PID serveur (reparation, MO-458)")):
            auto = lancer_enfant(
                [sys.executable, str(lanceur_flux), "--racine", str(racine_flux), drapeau],
                capture_output=True, text=True,
            )
            print(f"  {libelle}: " + ("OK" if auto.returncode == 0 else "KO"))
            if auto.returncode != 0:
                dernier = (auto.stdout or "").strip().splitlines()
                ko.append(libelle + " ROMPU : " + (dernier[-1][:120] if dernier else "aucune sortie"))

    # 8. VERIFIER SANS ATTENDRE (MO-062) : la cadence se LIT, elle ne s'attend
    #    pas. Sans ce maillon, on peut remettre un `time.sleep(intervalle)` en un
    #    bloc dans une boucle et ne le decouvrir qu'en patientant 15 minutes --
    #    c'est-a-dire jamais.
    print("== 8. attente (verifier sans attendre) ==")
    garde_attente = outils / "verifier-sans-attendre.py"
    if not garde_attente.is_file():
        print("  attente: ABSENT")
        ko.append("manquant: verifier-sans-attendre.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_attente), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  attente: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "->"))]
            ko.append("attente: " + ("; ".join(ecarts) if ecarts else "voir verifier-sans-attendre.py"))

    # 9. TRACE suivi-optimus : un debut + une fin PAR MISSION, et l'empreinte du
    #    journal. Le doublon MO-061 (2 debuts, 2 fins) a vecu des heures SANS
    #    qu'aucune suite se plaigne : le controle `verifier` le criait depuis sa
    #    porte, mais rien ne l'appelait. Un controle que personne ne lance ne
    #    protege rien -- celui-ci est desormais BLOQUANT.
    print("== 9. trace (suivi-optimus) ==")
    suivi_optimus = zone.parent.parent / "matrice" / "data" / "outils" / "suivi-optimus" / "main.py"
    if not suivi_optimus.is_file():
        print("  trace: ABSENT")
        ko.append("manquant: suivi-optimus/main.py")
    else:
        r = lancer_enfant([sys.executable, str(suivi_optimus), "verifier"],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  trace: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("ECART")]
            ko.append("trace: " + ("; ".join(ecarts) if ecarts else "voir suivi-optimus verifier"))
        # 9 bis. CROISEMENT FILE DU PILOTE <-> JOURNAL (MO-096) : `verifier` ne juge
        # que la coherence INTERNE du journal -- une mission menee sans jamais y
        # entrer est invisible pour lui (MO-095, 2026-09-15 : mission entiere hors
        # marbre sous un verifier vert). La meme lecon que ci-dessus, apprise une
        # deuxieme fois : un controle que personne ne lance ne protege rien. Le
        # croisement (categorie `coherence`, MO-048) est donc appele ICI aussi.
        if suivi_optimus.is_file():
            croisement = lancer_enfant(
                [sys.executable, str(suivi_optimus), "coherence",
                 "--racine", str(zone.parent.parent)],
                capture_output=True, text=True)
            etat_croisement = "OK" if croisement.returncode == 0 else "KO"
            print(f"  croisement file<->journal: {etat_croisement}")
            if croisement.returncode != 0:
                ecarts_c = [l.strip() for l in croisement.stdout.splitlines()
                            if l.strip().startswith("ECART")]
                ko.append("croisement: " + ("; ".join(ecarts_c) if ecarts_c
                                           else "voir suivi-optimus coherence"))

        # 9 ter. LA BORNE DU MARBRE REJOUEE SUR UN JOURNAL JETABLE (MO-250) : la
        #       borne `debut` avait DEUX ecrivains -- le pilote a l injection et
        #       l agent sur l ORDRE 4.5 -- donc un agent obeissant fabriquait le
        #       doublon que `verifier` accusait (MO-202, MO-240). Le 9 ci-dessus
        #       juge le VRAI journal (propre aujourd'hui) ; il ne dit donc RIEN du
        #       chemin qui l a produit. Ce maillon REJOUE le chemin complet dans un
        #       workspace JETABLE : le doublon est fabrique, ACCUSE, puis REPARE par
        #       la porte nommee (`archiver --doublons`), et `verifier` doit rendre
        #       VERT avec 1 debut / 1 fin. Un controle que rien ne rejoue ne
        #       protege rien -- la lecon du 9, apprise une troisieme fois.
        garde_marbre = outils / "verifier-marbre.py"
        if not garde_marbre.is_file():
            print("  marbre: ABSENT")
            ko.append("manquant: verifier-marbre.py")
        else:
            r = lancer_enfant([sys.executable, str(garde_marbre),
                                "--racine", str(zone.parent.parent)],
                               capture_output=True, text=True)
            etat = "OK" if r.returncode == 0 else "KO"
            cobaye_marbre = [l.strip() for l in r.stdout.splitlines()
                             if l.strip().startswith("cobaye ")]
            print(f"  marbre: {etat}"
                  + (f" (cobaye : {len(cobaye_marbre)} epreuve(s) rejouee(s))"
                     if cobaye_marbre else ""))
            if r.returncode != 0:
                ecarts = [l.strip() for l in r.stdout.splitlines()
                          if l.strip().startswith(("[KO", "ECART", "DETTE"))]
                ko.append("marbre: " + ("; ".join(ecarts) if ecarts
                                        else "voir verifier-marbre.py"))

    # 10. ANTI-SPAM MISSIONS (MO-070 / MO-073) : le depot d'une vigie est borne
    #     par MISSION, pas par etat changeant. Les DEUX vigies ont eu le MEME
    #     defaut, decouvert deux fois (fiche remplie champ par champ -> 4 depots en
    #     3 min ; observations basses signees -> vigie muette). Sans ce maillon,
    #     une refonte de l'anti-spam peut ramener la panne en silence : c'est
    #     exactement ce qui s'est passe ENTRE les deux vigies.
    print("== 10. anti-spam missions (borne par mission) ==")
    garde_anti_spam = outils / "verifier-anti-spam-missions.py"
    if not garde_anti_spam.is_file():
        print("  anti-spam: ABSENT")
        ko.append("manquant: verifier-anti-spam-missions.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_anti_spam), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  anti-spam: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "->"))]
            ko.append("anti-spam: " + ("; ".join(ecarts) if ecarts else "voir verifier-anti-spam-missions.py"))

    # 11. CHAPITRES ESPION (MO-072 / EO-102) : une passe de `espion-integrite`
    #     annoncait `"chapitres": [1, 2]` ECRIT EN DUR alors que le chapitre 2 ne
    #     peut produire une ligne que pour une BDD a-construire -- le registre
    #     n'en avait plus depuis le 2026-09-06 (canal declare mais vide). Sans ce
    #     maillon, on peut remettre une annonce statique et ne le decouvrir qu'en
    #     relisant le journal a la main, c'est-a-dire jamais.
    print("== 11. chapitres espion (annonce == production) ==")
    garde_chapitres = outils / "verifier-chapitres-espion.py"
    if not garde_chapitres.is_file():
        print("  chapitres: ABSENT")
        ko.append("manquant: verifier-chapitres-espion.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_chapitres), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  chapitres: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("ECART")]
            ko.append("chapitres: " + ("; ".join(ecarts) if ecarts else "voir verifier-chapitres-espion.py"))

    # 12. EXEMPTIONS VISIBLES (MO-075 / EO-103) : `corriger-ascii` ecartait EN
    #     SILENCE les BDD sous etalon et tous les journaux `.jsonl` (angle mort
    #     mesure : 545 fichiers reecrivables contre 577 vus). Sans ce maillon, une
    #     refonte peut remettre l'exclusion muette sans qu'aucune suite se plaigne.
    print("== 12. exemptions visibles (corriger-ascii) ==")
    garde_exemptions = outils / "verifier-exemptions-visibles.py"
    if not garde_exemptions.is_file():
        print("  exemptions: ABSENT")
        ko.append("manquant: verifier-exemptions-visibles.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_exemptions), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  exemptions: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("ECART")]
            ko.append("exemptions: " + ("; ".join(ecarts) if ecarts else "voir verifier-exemptions-visibles.py"))

    # 13. ROTATION JOURNAL (MO-077 / EO-115) : une rotation reeeCRIT un journal en
    #     ajout seul -- l'operation la plus dangereuse du projet. Elle doit
    #     deplacer sans perdre ni dupliquer, inclure l'ARCHIVE dans son "deja
    #     connu" (lecon L-040 : sinon elle se reecrit des jumeaux au passage
    #     suivant) et REFUSER d'ecraser un journal qui bouge sous ses pieds. Sans
    #     ce maillon, une refonte du bornage peut perdre des dizaines de milliers
    #     de lignes en silence, ou doubler l'archive apres verification.
    print("== 13. rotation journal (borner ne perd rien) ==")
    garde_rotation = outils / "verifier-rotation-journal.py"
    if not garde_rotation.is_file():
        print("  rotation: ABSENT")
        ko.append("manquant: verifier-rotation-journal.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_rotation), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  rotation: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "ECART"))]
            ko.append("rotation: " + ("; ".join(ecarts) if ecarts else "voir verifier-rotation-journal.py"))

    # 14. HISTORIQUE NON REDONDANT (MO-080) : le journal du routeur de maintenance
    #     ecrivait une ligne a CHAQUE passe -- mesure : 510 lignes identiques a la
    #     date pres sur 512 (99,4 %), ~150 Ko par jour pour rien. La reparation
    #     separe l'ETAT (ecrit chaque passe, ecrase, et qui TRACE les passes
    #     absorbees) de l'HISTOIRE (append sur FAIT : courrier route, anomalie qui
    #     change). Sans ce maillon, la passe peut se remettre a recopier un etat
    #     dans un journal en ajout seul, et noyer les faits sans que rien ne crie.
    print("== 14. historique non redondant (faits, pas un etat) ==")
    garde_historique = outils / "verifier-historique-non-redondant.py"
    if not garde_historique.is_file():
        print("  historique: ABSENT")
        ko.append("manquant: verifier-historique-non-redondant.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_historique), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  historique: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "ECART"))]
            ko.append("historique: " + ("; ".join(ecarts) if ecarts
                      else "voir verifier-historique-non-redondant.py"))

    # 15. OBSERVATIONS NON REDONDANTES (MO-081) : la passe de l'espion journalisait
    #     14 observations (une par BDD) a CHAQUE tour -- mesure : 504 134
    #     observations pour 36 000 passes, 93 % du journal. Or l'integrite d'une
    #     BDD est un ETAT. Le tableau part dans l'etat court
    #     (`espion-etat-bdds.json`, ecrit chaque passe et ECRASE, avec le compte des
    #     passes absorbees) ; les observations ne repartent au journal que si le
    #     tableau CHANGE, et la ligne `passe` reste ecrite a chaque tour (c'est le
    #     TEMOIN DE VIE du maillon 3 : il n'a pas le droit de devenir aveugle). Sans
    #     ce maillon, la passe peut se remettre a recopier le tableau et noyer les
    #     faits sans que rien ne crie.
    print("== 15. observations non redondantes (un etat, pas un fait) ==")
    garde_observations = outils / "verifier-observations-non-redondantes.py"
    if not garde_observations.is_file():
        print("  observations: ABSENT")
        ko.append("manquant: verifier-observations-non-redondantes.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_observations), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  observations: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "ECART"))]
            ko.append("observations: " + ("; ".join(ecarts) if ecarts
                      else "voir verifier-observations-non-redondantes.py"))

    # 16. PASSES NON REDONDANTES (MO-082) : les DEUX vigies ecrivaient la meme
    #     ligne `passe` a CHAQUE tour -- mesure : vigie-profil 194 fois la meme
    #     ligne sur 330 (58,8 %), vigie-portes 105 sur 204 (51,5 %). Or une passe
    #     est un ETAT. La photo part dans l'etat court (`*-etat-passes.json`, ecrit
    #     chaque passe et ECRASE, avec le compte des passes absorbees et le motif de
    #     la decision) ; le journal ne recoit la passe que si ce qu'elle a VU a
    #     change. La regression qui se cache derriere : le motif de la decision
    #     anti-spam disparaitrait AVEC les lignes supprimees -- c'est pourquoi il
    #     est trace dans l'etat. Sans ce maillon, une refonte peut remettre une
    #     ligne par passe (le defaut a ete trouve quatre fois : routeur MO-080,
    #     espion MO-081, deux vigies MO-082).
    print("== 16. passes non redondantes (un etat, pas un fait) ==")
    garde_passes = outils / "verifier-passes-non-redondantes.py"
    if not garde_passes.is_file():
        print("  passes: ABSENT")
        ko.append("manquant: verifier-passes-non-redondantes.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_passes), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  passes: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "ECART"))]
            ko.append("passes: " + ("; ".join(ecarts) if ecarts
                      else "voir verifier-passes-non-redondantes.py"))

    # 17. SUPER-COMBO sc-001 (MO-083) : sc-001 lancait chaque theme par
    #     `python theme-X.json`. Or un theme est l'ARBRE DE DECISION (JSON) que lit
    #     l'agent : en Python c'est un LITTERAL DE DICTIONNAIRE -- une expression
    #     valide, SANS EFFET, qui sort en code 0. La chaine rendait donc "6/6
    #     succes, TOUS LES THEMES ONT REUSSI" sur un fichier INEXISTANT : le vert
    #     ne dependait ni de la cible, ni de la mission, ni de l'etat des themes.
    #     Un faux vert est invisible PAR NATURE (il ne se plaint jamais) : sans ce
    #     maillon, une refonte peut rendre le controle incapable d'echouer et
    #     personne ne le saura. Le maillon lance l'AUTO-TEST du super-combo, qui
    #     rejoue l'ANCIEN mecanisme (code 0 muet, qui doit etre ACCUSE) et un
    #     cobaye en dossier jetable ou un theme corrompu puis un theme ABSENT
    #     doivent etre ACCUSES ET NOMMES.
    print("== 17. super-combo sc-001 (un controle qui peut echouer) ==")
    sc001 = zone / "super-combos" / "sc-001-auto-xxx" / "main.py"
    if not sc001.is_file():
        print("  sc-001: ABSENT")
        ko.append("manquant: sc-001-auto-xxx/main.py")
    else:
        r = lancer_enfant([sys.executable, str(sc001), "auto-test"],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  sc-001: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("[KO]")]
            ko.append("sc-001: " + ("; ".join(ecarts) if ecarts else "voir sc-001 main.py auto-test"))

    # 18. CADENCE (friction 28, MO-084) : une routine DECLARE sa cadence et la
    #     PUBLIE -- mais personne ne MESURAIT son battement. `veille-flux` a
    #     tourne a 6,0 s contre 300 s declarees pendant DEUX JOURS (20 219 passes
    #     en trop, ~5,6 h de CPU, ~39 000 lignes de journal, 19 500 appels a
    #     `corriger-ascii`) et le seul temoin fut la TAILLE du journal, constatee
    #     trois jours plus tard. Le garde lit une SERIE d'horodatages et un ecart
    #     MEDIAN -- jamais une moyenne : le premier temoin de cadence, une moyenne
    #     (`(date - derniere_ecriture) / passes_absorbes`), a lu 450,5 s puis
    #     600,3 s pour une cadence de 900 s PROUVEE par le journal, et une valeur
    #     fausse mais DANS la tolerance ne crie pas. Sans ce maillon, la troisieme
    #     jambe (declarer / publier / MESURER) peut etre retiree et une rafale
    #     revivre sans que rien ne s'en apercoive.
    print("== 18. cadence (le battement REEL vs la cadence DECLAREE) ==")
    garde_cadence = outils / "verifier-cadence.py"
    if not garde_cadence.is_file():
        print("  cadence: ABSENT")
        ko.append("manquant: verifier-cadence.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_cadence), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  cadence: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "ECART"))]
            ko.append("cadence: " + ("; ".join(ecarts) if ecarts else "voir verifier-cadence.py"))

    # 19. PARCOURS (MO-087) : le catalogue d'Optimus declarait DOUZE themes
    #     `statut: pret` (index-themes.json) alors que son PARCOURS
    #     (index-parcours.json) n'en routait que CINQ -- sept themes etaient
    #     ECRITS, testes et JAMAIS ROUTES (FICHIER, AUTO-CORRECTION, AUTO-TESTING,
    #     AUTO-OPTIMISATION, AUTO-PERFORMANCE, AUTO-AUDIT-NEMESIS, AUTO-XXX).
    #     Personne ne s'en plaignait : aucun controle ne croisait les deux index
    #     (une chose ecrite n'est pas une chose LUE). Sans ce maillon, la
    #     divergence peut revenir et un theme -- ou la case [decision] de la
    #     chaine [purification] -- peut redevenir inatteignable en silence.
    print("== 19. parcours (tout theme pret est ROUTE) ==")
    garde_parcours = outils / "verifier-parcours.py"
    if not garde_parcours.is_file():
        print("  parcours: ABSENT")
        ko.append("manquant: verifier-parcours.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_parcours), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  parcours: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "ECART"))]
            ko.append("parcours: " + ("; ".join(ecarts) if ecarts else "voir verifier-parcours.py"))

    # 20. CHEMINS (contrat fondamental, L-006 / L-013) : AUCUN chemin ne se
    #     COMPTE a la main (`parents[N]`) et aucun ne part du cwd -- la racine se
    #     DETECTE par un marqueur partage (`matrice/data/commun/racine.py`) et son
    #     echec doit se DIRE. NEUF dettes de ce type ont vecu sans bruit (MO-087)
    #     parce que cette suite ne lancait que le controle des PREFIXES : une
    #     dette que personne ne regarde devient un chemin FAUX et SILENCIEUX le
    #     jour ou la profondeur change. Les 9 sites sont ancres ; ce maillon, en
    #     mode --strict, rend la dette BLOQUANTE pour qu'elle ne revienne pas.
    print("== 20. chemins (aucun parents[N] nu) ==")
    garde_chemins = outils / "verifier-contrat-fondamental.py"
    if not garde_chemins.is_file():
        print("  chemins: ABSENT")
        ko.append("manquant: verifier-contrat-fondamental.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_chemins), "chemins", "--strict"],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  chemins: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("ECART", "DETTE"))]
            ko.append("chemins: " + ("; ".join(ecarts) if ecarts else "voir verifier-contrat-fondamental.py"))

    # 21. CARTES D'IDENTITE (MO-089) : sur 65 documents de la zone, VINGT-SIX
    #     n'avaient AUCUNE carte et rien ne s'en plaignait -- les trois
    #     verificateurs du marbre (regles, protocoles, conventions) ne regardent
    #     que `matrice/data/`. Un document sans carte est un document SANS TYPE :
    #     le pilote ne peut pas savoir QUOI il injecte, et une doctrine qu'on veut
    #     injecter au bon moment ne peut pas etre choisie si elle ne dit pas ce
    #     qu'elle est. Le garde exige la carte (type + appartient_a + commun), un
    #     `appartient_a` en NOM (jamais un chemin) et un `type` du VOCABULAIRE
    #     FERME. Sans ce maillon, les cartes peuvent disparaitre en silence.
    print("== 21. cartes d'identite (tout document dit QUOI il est) ==")
    garde_cartes = outils / "verifier-cartes-identite.py"
    if not garde_cartes.is_file():
        print("  cartes: ABSENT")
        ko.append("manquant: verifier-cartes-identite.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_cartes), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  cartes: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "ECART"))]
            ko.append("cartes: " + ("; ".join(ecarts) if ecarts else "voir verifier-cartes-identite.py"))

    # 21 BIS. PLACEHOLDERS (EO-268, 2026-09-19) : un champ DECLARE ne doit pas
    #     CONTREDIRE une mesure calculable depuis le MEME document. Le pilote
    #     declarait duree_s = 0 a chaque cloture et la vue affichait zero alors que
    #     les bornes du meme journal donnaient 149 s (L-055) : personne ne s en
    #     plaignait. Le garde rejoue la regle du DOMICILE (la vue du suivi), il ne
    #     la recopie pas, et il porte son autotest : contradiction ACCUSEE, silence
    #     NON accuse, zero legitime NON accuse.
    print("== 21 bis. placeholders (un declare ne contredit pas la mesure) ==")
    garde_placeholders = outils / "verifier-placeholders.py"
    if not garde_placeholders.is_file():
        print("  placeholders: ABSENT")
        ko.append("manquant: verifier-placeholders.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_placeholders), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  placeholders: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("[KO")]
            ko.append("placeholders: " + ("; ".join(ecarts) if ecarts else "voir verifier-placeholders.py"))

    # 21 TER. CHAINES (MO-246, 2026-09-19) : le STATUT porte dans la carte d identite
    #     d une chaine n etait verifie par AUCUN controle -- une colonne vide se lit
    #     comme un fait (constat N6 de l audit MO-220). Le garde LIT les etapes au
    #     domicile (chaine-pense-bete/constants.py, M-076), il ne les recopie pas, et
    #     il porte son AUTOTEST : le controle est PERMANENT, jamais un cobaye jetable
    #     qui meurt avec tmp-optimus.
    print("== 21 ter. chaines (le statut declare est coherent) ==")
    garde_chaines = outils / "verifier-chaines.py"
    if not garde_chaines.is_file():
        print("  chaines: ABSENT")
        ko.append("manquant: verifier-chaines.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_chaines), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  chaines: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("[KO")]
            ko.append("chaines: " + ("; ".join(ecarts) if ecarts else "voir verifier-chaines.py"))

    # 21 QUATER. VALEURS EN DUR (M-102 : dette de precision FERMEE le 2026-09-19) : le
    #     scan existait depuis MO-093 mais n etait JAMAIS branche -- il exigeait une
    #     cible (donc aucun controle permanent) et il accusait 167 lignes dont 164
    #     legitimes (les journaux et les archives de missions portent de VRAIS chemins).
    #     Deux corrections mesurees : le motif `chemin-win` est ANCRE (il attrapait le
    #     `s:` d une adresse web et le `e:` d une sequence d echappement -- un scan qui
    #     crie a tort n est jamais branche), et un motif `perimetre-en-dur` est AJOUTE
    #     (une liste de dossiers REELS recopiee dans un corps de fonction : c est AINSI
    #     que la racine de la Matrice etait sortie du balayage des points de
    #     restauration, EO-277). Le controle tourne sur les ZONES DE CODE, ou le scan
    #     est propre (mesure : 373 fichiers, 0 valeur) ; les journaux, qui portent des
    #     chemins par nature, ne sont pas le juge -- et ce fait est DIT.
    print("== 21 quater. valeurs en dur (tout le .py de la Matrice) ==")
    scan_valeurs = outils / "scan-valeurs-en-dur.py"
    if not scan_valeurs.is_file():
        print("  valeurs-en-dur: ABSENT")
        ko.append("manquant: scan-valeurs-en-dur.py")
    else:
        # AUCUNE LISTE ICI : la cible est la Matrice ENTIERE en .py. Ecrire une paire
        # de dossiers aurait ete la MEME faute que celle qu on vient de fermer (le
        # scan l accuse d ailleurs) -- une valeur de perimetre s ecrit UNE fois, chez
        # elle (M-076). La racine vient de l ancrage deja connu du lanceur.
        racine_mat = zone.parent.parent
        r = lancer_enfant(
            [sys.executable, str(scan_valeurs), str(racine_mat),
             "--ext", ".py", "--racine", str(racine_mat)],
            capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print("  valeurs-en-dur (.py de la Matrice): " + etat)
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith("- ")]
            ko.append("valeurs-en-dur: "
                      + ("; ".join(ecarts) if ecarts else "voir scan-valeurs-en-dur.py"))

    # 21 quinquies. COMMANDES (MO-249 / P3) : les autres gardes surveillent les
    #     FICHIERS ; celui-ci surveille les COMMANDES que les agents COPIENT --
    #     les lignes de commande des blocs de code des documents. Un appel sans
    #     interpreteur, un chemin d argument non ancre, un heredoc ou un python -c
    #     se paient en erreurs de syntaxe (question du createur). Le lanceur unique
    #     (matrix/lancer.py) est la reponse ; ce garde empeche le retour des
    #     mauvaises habitudes.
    print("== 21 quinquies. commandes (garde des commandes documentees) ==")
    garde_commandes = outils / "verifier-commandes.py"
    if not garde_commandes.is_file():
        print("  commandes: ABSENT")
        ko.append("manquant: verifier-commandes.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_commandes), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print("  commandes: " + etat)
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("[KO]")]
            ko.append("commandes: " + ("; ".join(ecarts) if ecarts else "voir verifier-commandes.py"))

    # 21 SEXIES. BRIQUES (EO-287 / MO-293) : le lanceur ET les appelants internes
    #     resolvent une brique par son NOM. Ce contrat n etait prouve que par un
    #     cobaye JETABLE, purge avec la zone -- rien ne le rejouait. Il l est
    #     maintenant a chaque suite : CONTRE-TEMOIN (chaque nom RENDU rend un main.py
    #     qui existe, et les noms des appelants -- DECOUVERTS par leur import du
    #     domicile, donc AUCUNE table a tenir -- resolvent bien leur cible) et COBAYE
    #     (un nom INCONNU rend un
    #     REFUS NOMME : nom fautif, proches, remede -- jamais un refus silencieux),
    #     plus la FACADE (--lister == domicile, nom inconnu = code 2). Le garde porte
    #     son AUTOTEST (SIX epreuves) : deux resolutions truquees doivent crier, un FAUX
    #     appelant doit rester INVISIBLE et un appelant SAIN non accuse -- un garde qu on
    #     ne peut pas faire rougir ne prouve rien, un garde qui accuse tout non plus.
    print("== 21 sexies. briques (le nom rend la brique, ou refuse en la nommant) ==")
    garde_briques = outils / "verifier-resolution.py"
    if not garde_briques.is_file():
        print("  briques: ABSENT")
        ko.append("manquant: verifier-resolution.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_briques), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print("  briques: " + etat)
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("[KO]")]
            ko.append("briques: " + ("; ".join(ecarts) if ecarts else "voir verifier-resolution.py"))

    # 22. ROLES (MAILLON 2/5 de la revision, 2026-09-14) : le cameleon recoit UNE
    #     personnalite par mission ; Optimus n'en recevait AUCUNE -- ses missions
    #     ne portaient qu'un theme de CHANTIER (le QUOI toucher) et le catalogue
    #     DERVERSAIT la fiche ENTIERE au demarrage. Le garde exige que chaque TYPE
    #     de l'entonnoir ait une POSTURE reelle du vivier (categorie PERSONNALITE),
    #     que le catalogue la DECLARE et que le MOTEUR la SERVE, et que les DEUX
    #     chemins d'injection (simple et lot) la portent. Sans ce maillon, une
    #     mission peut repartir sans conduite -- et une posture inventee peut se
    #     faire passer pour un theme (c'est arrive pour les roles d'entonnoir).
    print("== 22. roles (chaque type a une posture, injectee) ==")
    garde_roles = outils / "verifier-roles.py"
    if not garde_roles.is_file():
        print("  roles: ABSENT")
        ko.append("manquant: verifier-roles.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_roles), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  roles: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "ECART"))]
            ko.append("roles: " + ("; ".join(ecarts) if ecarts else "voir verifier-roles.py"))

    # 23. RESOLUTION (PAS 1 DU CHANTIER NATIF, fiche I-00, controle B) : le nom
    #     ne decide plus seul -- un import par NOM NU ne vise jamais l'interieur,
    #     et la fabrique d'insertions de chemin est surveillee. Le blocage porte
    #     sur le PERIMETRE MIGRE (declare DANS l'outil, vide tant que la
    #     migration n'a pas commence) ; ailleurs la dette est CHIFFREE et ne doit
    #     JAMAIS remonter. Sans ce maillon, la classe de panne entiere (deux
    #     homonymes qui se masquent en silence) peut revenir sans que rien ne crie.
    print("== 23. resolution (garde du pas 1 : nom nu + insertions) ==")
    garde_resolution = outils / "verifier-contrat-fondamental.py"
    if not garde_resolution.is_file():
        print("  resolution: ABSENT")
        ko.append("manquant: verifier-contrat-fondamental.py")
    else:
        for verbe in ("resolution", "insertions"):
            r = lancer_enfant([sys.executable, str(garde_resolution), verbe,
                                "--racine", str(zone.parent.parent)],
                               capture_output=True, text=True)
            etat = "OK" if r.returncode == 0 else "KO"
            print(f"  {verbe}: {etat}")
            if r.returncode != 0:
                ecarts = [l.strip() for l in r.stdout.splitlines()
                          if l.strip().startswith("ECART")]
                ko.append(verbe + ": " + ("; ".join(ecarts) if ecarts
                                          else "voir verifier-contrat-fondamental.py"))

    # 24. RECHERCHE (EO-131) : le pilote INJECTE la question a poser au moteur,
    #     au moment ou elle sert -- le sujet de la mission. Sans ce maillon, le
    #     moteur redevient ce qu'il etait avant MO-138 : une CAPACITE que personne
    #     n'utilise, donc une fonctionnalite morte (un moteur qu'il faut penser a
    #     lancer est un moteur eteint). Le garde exige UNE derivation partagee
    #     (deux copies divergeraient, L-029), les DEUX chemins d'injection par flux
    #     (simple ET lot), et que le Flux 1 ne recoive JAMAIS l'option qui ouvre
    #     une zone interne (L-016).
    print("== 24. recherche (le pilote injecte la question) ==")
    garde_recherche = outils / "verifier-recherche.py"
    if not garde_recherche.is_file():
        print("  recherche: ABSENT")
        ko.append("manquant: verifier-recherche.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_recherche), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  recherche: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "ECART"))]
            ko.append("recherche: " + ("; ".join(ecarts) if ecarts else "voir verifier-recherche.py"))

    # 25. FICHE (EO-124) : ma fiche doit rester COURTE -- c'est le createur qui l'a
    #     demande, et la raison est de fond : une fiche qui verse tout au demarrage
    #     rend l'agent instable et lui fait perdre, a la fin, ce qu'il devait faire.
    #     Mais une fiche qu'on allege sans garde perd des regles en silence : ce
    #     maillon tient les DEUX bouts -- un PLAFOND declare, et la COUVERTURE de
    #     toutes les regles immuables (aucune perdue). Sans lui, la fiche regrossit
    #     ligne par ligne, ou maigrit en oubliant une regle : personne ne le voit.
    print("== 25. fiche (courte, et aucune regle perdue) ==")
    garde_fiche = outils / "verifier-fiche.py"
    if not garde_fiche.is_file():
        print("  fiche: ABSENT")
        ko.append("manquant: verifier-fiche.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_fiche), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  fiche: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "ECART"))]
            ko.append("fiche: " + ("; ".join(ecarts) if ecarts else "voir verifier-fiche.py"))

    # 26. RATTRAPAGE (EO-133) : la vue ne lit QUE le journal -- une modification
    #     notee au DOMICILE apres la cloture d'une mission n'y apparait donc JAMAIS
    #     (mesure : 576 fichiers sur 80 missions invisibles, il a fallu les recrire
    #     a la main). Le createur a tranche : c'est le PILOTE qui comble le trou a
    #     chaque cloture, la vue restant un rendereur. Ce maillon exige que le
    #     rattrapage DETECTE les trous, ne DOUBLE jamais, se TAISE proprement quand
    #     il ne peut pas lire, et tourne AVANT l'entretien de la vue -- un
    #     rattrapage place apres elle ne serait visible qu'au tour suivant.
    print("== 26. rattrapage (le pilote comble les fichiers non traces) ==")
    garde_rattrapage = outils / "verifier-rattrapage.py"
    if not garde_rattrapage.is_file():
        print("  rattrapage: ABSENT")
        ko.append("manquant: verifier-rattrapage.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_rattrapage),
                            "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  rattrapage: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "ECART"))]
            ko.append("rattrapage: " + ("; ".join(ecarts) if ecarts else "voir verifier-rattrapage.py"))

    # 27. JUMEAUX DE LITTERAUX (MO-175) : deux domiciles declarent le MEME nom
    #     (pilote/constants.py et pilote/entonnoir/listes.py). Une divergence
    #     compile, passe py_compile et change le SENS : elle ne se voit qu a
    #     l usage -- c est exactement ce qui a fait tomber l avis d auto-
    #     validation a NON (chemin double). Ce maillon la rend BLOQUANTE.
    print("== 27. jumeaux (deux domiciles, un seul sens) ==")
    garde_jumeaux = outils / "verifier-contrat-fondamental.py"
    if not garde_jumeaux.is_file():
        print("  jumeaux: ABSENT")
        ko.append("manquant: verifier-contrat-fondamental.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_jumeaux), "jumeaux"],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        # Le cobaye a fixtures jetables REJOUE le piege a chaque execution : on le
        # DIT (sinon le lecteur ne sait pas que la detection a ete eprouvee, la et
        # pas seulement une fois dans un compte-rendu).
        cobaye = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("cobaye ")]
        print(f"  jumeaux: {etat}"
              + (f" (cobaye : {len(cobaye)} epreuve(s) rejouee(s))" if cobaye else ""))
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("ECART", "DETTE"))]
            ko.append("jumeaux: " + ("; ".join(ecarts) if ecarts
                                     else "voir verifier-contrat-fondamental.py"))

    # 28. MIROIR DES CROCHETS (R5, audit MO-174) : la liste FERMEE des crochets vit
    #     dans le code (pilote/filtrer/entry.py) ET dans sa convention. Le
    #     2026-09-18 les deux avaient diverge en SILENCE : `[purification]` etait
    #     declare par la convention et INCONNU du pilote, et aucun instrument ne
    #     voyait l ecart. Ce maillon rend la divergence BLOQUANTE dans les deux
    #     sens, et exige qu un crochet qui part a l entonnoir declare un type de
    #     la liste fermee TYPES -- depuis R5 le type est TRANSMIS, un type hors
    #     liste ferait REFUSER le depot.
    print("== 28. crochets (le code et sa convention disent la MEME chose) ==")
    garde_crochets = outils / "verifier-contrat-fondamental.py"
    if not garde_crochets.is_file():
        print("  crochets: ABSENT")
        ko.append("manquant: verifier-contrat-fondamental.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_crochets), "crochets"],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        # Le cobaye rejoue le miroir dans les DEUX sens a chaque execution : on le
        # DIT, sinon la lecture croirait que seul le cas nominal a ete mesure.
        cobaye = [l.strip() for l in r.stdout.splitlines() if "cas rejoues" in l]
        print(f"  crochets: {etat}"
              + (" (cobaye : les deux sens accuses)" if cobaye and r.returncode == 0 else ""))
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("ECART", "DETTE"))]
            ko.append("crochets: " + ("; ".join(ecarts) if ecarts
                                      else "voir verifier-contrat-fondamental.py"))


    # 29. APPELS NON LIES (R5, audit MO-174) : un nom APPELE que rien ne lie est
    #     un NameError en puissance -- au coeur de la chaine de cloture le
    #     2026-09-18 (`fin/entry.py` appelait `lire_defauts` sans l'importer).
    #     py_compile etait VERT (le compilateur ne resout pas les noms), la porte
    #     `editer` aussi (elle verifie que les imports ECRITS existent, jamais
    #     qu'un nom UTILISE est importe). Ce maillon le voit SANS executer.
    print("== 29. appels non lies (un appel que rien ne lie) ==")
    garde_appels = outils / "verifier-contrat-fondamental.py"
    if not garde_appels.is_file():
        print("  appels-non-lies: ABSENT")
        ko.append("manquant: verifier-contrat-fondamental.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_appels), "appels-non-lies"],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        # Le cobaye tient les DEUX bords (4 liaisons tues, 1 orphelin accuse) : on
        # le DIT, sinon la lecture croirait qu'un seul cote a ete mesure.
        cobaye = [l.strip() for l in r.stdout.splitlines() if "cas (4 liaisons" in l]
        print(f"  appels-non-lies: {etat}"
              + (" (cobaye : 4 liaisons tues, 1 orphelin accuse)" if cobaye else ""))
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("ECART", "DETTE"))]
            ko.append("appels-non-lies: " + ("; ".join(ecarts[:6]) if ecarts
                                             else "voir verifier-contrat-fondamental.py"))


    # 30. CONTRATS DES OUTILS (MO-214 / EO-204) : les controles qui vivaient dans les
    #     cobayes d'une mission MOURAIENT avec elle -- `tmp-optimus` est purge a chaque
    #     cloture, donc une preuve d'aujourd'hui ne surveille rien demain. Trois contrats
    #     gagnes le 2026-09-19 sont desormais GARDES : l'aide de la porte dit son contrat
    #     (MO-212), la carte ASCII a un seul domicile et la porte corrige les fautes
    #     futiles / refuse le reste (MO-210), l'entonnoir repare la categorie comme le
    #     role (MO-213). Le garde porte son AUTOTEST du piege (L-032) et travaille en
    #     SOUS-PROCESSUS ISOLES (deux outils ont chacun un module `constants`).
    print("== 30. contrats des outils (aide <-> contrat, carte ascii, categorie) ==")
    garde_contrats = outils / "verifier-contrats-outils.py"
    if not garde_contrats.is_file():
        print("  contrats: ABSENT")
        ko.append("manquant: verifier-contrats-outils.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_contrats), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  contrats: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "ECART"))]
            ko.append("contrats: " + ("; ".join(ecarts) if ecarts
                      else "voir verifier-contrats-outils.py"))

    # 31. MIROIRS INTER-FLUX (MO-230 / EO-224, rendu RECURRENT par EO-225) : le
    #     flanc cameleon avait ses DECLARATIONS PROPRES couvertes par AUCUN
    #     controle de son cote -- le seul lecteur etait ce verbe, et il ne tournait
    #     que si quelqu'un le tapait a la main. Un controle qui ne tourne JAMAIS
    #     est un constat de round, pas une surveillance (meme piege que MO-214 :
    #     un controle qui vit dans un cobaye meurt avec lui). Il devient donc le
    #     maillon 31. Les DEUX pilotes sont deux flux ISOLES par decision, on ne
    #     peut pas leur donner un domicile unique -- mais leur accord devient une
    #     RELATION CONTROLEE : chaque litteral lu dans les 28 fichiers miroirs dit
    #     la MEME valeur, SAUF si son nom est declare LIBRE avec sa raison. Une
    #     absence de vocabulaire partage, une divergence non declaree ou une zone
    #     absente est un ECART. Les 5 epreuves du cobaye (couple tel quel, mutation
    #     a gauche, a droite, retrait, liberte mutee) sont rejouees a CHAQUE
    #     execution : on le DIT, sinon la lecture croirait que seul le cas nominal
    #     a ete mesure.
    print("== 31. miroirs (deux flancs, un seul contrat) ==")
    garde_miroirs = outils / "verifier-contrat-fondamental.py"
    if not garde_miroirs.is_file():
        print("  miroirs: ABSENT")
        ko.append("manquant: verifier-contrat-fondamental.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_miroirs), "miroirs"],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        cobaye = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("cobaye ")]
        print(f"  miroirs: {etat}"
              + (f" (cobaye : {len(cobaye)} epreuve(s) rejouee(s))" if cobaye else ""))
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("ECART", "DETTE"))]
            ko.append("miroirs: " + ("; ".join(ecarts[:6]) if ecarts
                                     else "voir verifier-contrat-fondamental.py"))

    # 32. REFUS NOMME DES OPTIONS INCONNUES (T4 de PB-002, MO-215). Mesure
    #     d'origine (MO-195) : une option inconnue rendait le resultat du DEFAUT,
    #     indiscernable d'un appel correct (L-055). La chaine PB-002 a repare le
    #     DOMICILE (T1), les outils hors domicile (T2) et le CRITERE de la sonde
    #     (T3). Le CONTROLE PERMANENT manquait : la sonde sc-004 existait mais ne
    #     tournait que si quelqu'un la tapait a la main -- un controle qui ne
    #     tourne JAMAIS est un constat de round, pas une surveillance (meme piege
    #     que MO-214). Ce maillon l'entre dans la suite ET prouve qu'elle sait
    #     rougir : un cobaye MUET, ecrit dans une zone JETABLE SYSTEME (jamais un
    #     outil reel abime), doit etre ACCUSE et NOMME. Sans lui, un refus muet
    #     peut revenir sans que rien ne rougisse.
    print("== 32. refus nomme des options inconnues (une option fautive se DIT) ==")
    sonde_options = zone / "super-combos" / "sc-004-auto-diagnostic" / "main.py"
    if not sonde_options.is_file():
        print("  sonde options: ABSENT")
        ko.append("manquant: sc-004-auto-diagnostic/main.py")
    else:
        r = lancer_enfant([sys.executable, str(sonde_options), "inspection"],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  sonde options: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("[")]
            ko.append("options: " + ("; ".join(ecarts) if ecarts else "voir sc-004 inspection"))
        # L'AUTO-TEST : la sonde SAIT ACCUSER (3 cobayes en zone jetable) -- un
        # controle qui ne peut pas echouer ne prouve rien.
        r = lancer_enfant([sys.executable, str(sonde_options), "auto-test"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("- ")]
            ko.append("sonde auto-test: " + ("; ".join(ecarts) if ecarts
                      else "voir sc-004 auto-test"))
        # LA PREUVE DE ROUGE : un cobaye MUET, en zone jetable, doit faire ROUGIR
        # l'inspection -- la suite ne peut donc pas etre verte par construction.
        with tempfile.TemporaryDirectory(prefix="cobaye-refus-muet-") as jetable:
            dossier_cobaye = Path(jetable) / "cobaye-muet"
            dossier_cobaye.mkdir()
            (dossier_cobaye / "main.py").write_text(
                "import sys\n"
                "def main():\n"
                "    print(\"usage : cobaye-muet\")\n"
                "    return 2\n"
                "if __name__ == \"__main__\":\n"
                "    sys.exit(main())\n",
                encoding="utf-8", newline="\n")
            r = lancer_enfant([sys.executable, str(sonde_options), "inspection",
                                "--outils", jetable], capture_output=True, text=True)
            if r.returncode != 0 and "cobaye-muet" in r.stdout and "refus-muet" in r.stdout:
                print("  sonde options: cobaye muet ACCUSE (la suite sait rougir)")
            else:
                ko.append("options: un cobaye MUET n a PAS ete accuse -- la suite"
                          " serait verte par construction")

    # 33. PROFIL DE L'UTILISATEUR (demande createur, 2026-09-21) : la fiche
    #     USER-PROFIL.md etait remplie avec le createur mais AUCUN agent ne la
    #     lisait. Mesure du jour : le pilote ne l'ouvrait qu'au DEMARRAGE, pour
    #     tester un champ, puis jetait le contenu -- les 8 champs n'atteignaient
    #     aucune mission. Le profil voyage desormais AVEC la mission (comme la
    #     posture et la question de recherche), BORNE par un plafond declare, et
    #     les champs ecartes sont DITS. Le garde tient les quatre bouts : un seul
    #     domicile (le motif partage), le champ PESE (sinon la mesure se tairait
    #     sur ce qu'elle livre -- defaut exact de MO-314), les DEUX chemins
    #     d'injection, et un cobaye OBESE qui doit mordre puis DISPARAITRE (la
    #     zone jetable reste vide : la suite ne laisse rien derriere elle).
    print("== 33. profil utilisateur (injecte, borne) ==")
    garde_profil = outils / "verifier-profil-injection.py"
    if not garde_profil.is_file():
        print("  profil: ABSENT")
        ko.append("manquant: verifier-profil-injection.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_profil), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        cobaye = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("cobaye ")]
        print(f"  profil: {etat}" + (f" ({cobaye[0]})" if cobaye else ""))
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "ECART"))]
            ko.append("profil: " + ("; ".join(ecarts) if ecarts
                                    else "voir verifier-profil-injection.py"))

    # 34. SOURCE D'UN ITEM (demande createur, 2026-09-21) : < reparer le champ source
    #     des missions recentes : il a perdu le type, la cible et l urgence que
    #     portaient les anciennes >. Mesure : la fabrique AUTOMATIQUE composait la
    #     forme LONGUE (96 missions) quand les DEUX chemins MANUELS ecrivaient
    #     `entonnoir:<id>` : 46 missions ont perdu a la naissance le type, la
    #     categorie et l urgence de leur item -- trois domiciles pour une idee, deux
    #     en desaccord. La composition vit desormais dans UN SEUL domicile, les deux
    #     chemins manuels l appellent, et un item INTROUVABLE est DIT au lieu de se
    #     taire. Le garde tient les trois champs (listes FERMEES : type, categorie de
    #     SON type, urgence), la borne REELLE du correctif (les 46 anciennes ne sont
    #     pas accusees : on ne reecrit pas l histoire avec des valeurs inventees),
    #     les DEUX LECTEURS, et un cobaye qui doit MORDRE puis DISPARAITRE.
    print("== 34. source d'un item (trois champs, un seul domicile) ==")
    garde_source = outils / "verifier-source-item.py"
    if not garde_source.is_file():
        print("  source: ABSENT")
        ko.append("manquant: verifier-source-item.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_source), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        cobaye = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("cobaye ")]
        print(f"  source: {etat}" + (f" ({cobaye[0]})" if cobaye else ""))
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith(("[KO", "ECART"))]
            ko.append("source: " + ("; ".join(ecarts) if ecarts
                                    else "voir verifier-source-item.py"))

    # 35. ENCHAINEMENT (une mission CHARGEe garde son verdict d auto-validation) :
    #     mesure du 2026-09-21, `est_auto_validee` comparait l id de la MISSION
    #     (MO-N) a un index qui ne porte que des ids d ITEM (EO-N) -- le verdict se
    #     perdait au pont, 45 missions sur 83 n en portaient aucune trace, et la
    #     chaine s arretait APRES CHAQUE mission (EO-264). Ce maillon exige le
    #     domicile UNIQUE du format de provenance, les consommateurs qui le lisent,
    #     le cobaye qui MORD (index vide, item non auto), et la mesure REELLE que
    #     l item exige : la tete du brin, son verdict, l etat du lot.
    print("== 35. enchainement (le verdict d'une mission chargee se resout) ==")
    garde_enchainement = outils / "verifier-enchainement.py"
    if not garde_enchainement.is_file():
        print("  enchainement: ABSENT")
        ko.append("manquant: verifier-enchainement.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_enchainement), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        mesure = [l.strip() for l in r.stdout.splitlines() if "MESURE REELLE" in l]
        print(f"  enchainement: {etat}" + (f" ({mesure[0][:110]})" if mesure else ""))
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith("[KO")]
            ko.append("enchainement: " + ("; ".join(ecarts) if ecarts
                                          else "voir verifier-enchainement.py"))

    # 36. EXTRACTION DES ECARTS (lecon L-163, MO-382/383/384) : les maillons 34 et
    #     35 filtraient la sortie de leur garde par un prefixe que ce garde n imprime
    #     JAMAIS (`KO]` quand `controler()` imprime `[KO`) : un ecart non extrait est
    #     un ROUGE MUET -- le verdict sait QU une chose a echoue et jamais LAQUELLE,
    #     alors que la cause ETAIT ecrite par le garde et perdue au dernier metre de
    #     la lecture. Ce maillon mesure sur TOUTE la Matrice les sites d extraction et
    #     exige que chaque filtre soit le DEBUT d une ligne qu un fichier IMPRIME, ou
    #     une exemption NOMMEE (document, aide, indentation). Il DIT aussi sa
    #     COUVERTURE : un controle qui ne lit rien passerait pour vert. Sa mesure est
    #     lue par un CONTENU et non par un prefixe -- un filtre neuf ecrit ici serait
    #     precisement le defaut que ce maillon surveille.
    print("== 36. extraction des ecarts (tout filtre a un producteur) ==")
    garde_extraction = outils / "verifier-extraction-ecarts.py"
    if not garde_extraction.is_file():
        print("  extraction: ABSENT")
        ko.append("manquant: verifier-extraction-ecarts.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_extraction), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        produit = [l.strip() for l in r.stdout.splitlines()
                   if "filtre(s) sans producteur" in l]
        print(f"  extraction: {etat}" + (f" ({produit[0][:110]})" if produit else ""))
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith("[KO")]
            ko.append("extraction: " + ("; ".join(ecarts) if ecarts
                                        else "voir verifier-extraction-ecarts.py"))

    # 37. SUIVI DU PILOTE (T4 de PB-003/SP-003/TD-003, EO-273) : la VUE du pilote
    #     (suivi-pilote, T2) est recalculee et le maillon tombe si la Table 0 n est
    #     PAS vide. C est le CONTROLE PERMANENT : les gardes de la zone surveillent
    #     ce qui est ECRIT et ce qui REPOND ; cette vue surveille le SILENCE, l AGE,
    #     la FORME DU LOT et une CONTRADICTION dont l une des traces est absente.
    #     Mesure du 2026-09-22 (pose du maillon) : la vue a ACCUSE une panne
    #     VIVANTE le jour meme (journal en pause sans reprise du 2026-09-12, etat
    #     absent -- dix jours sans que personne ne le voie). Une panne CONSTATEE et
    #     DEPOSEE (exception OUVERTE, nommee et motivee dans la declaration) ne
    #     gele pas la suite : elle reste VISIBLE dans la vue et dans la sortie.
    print("== 37. suivi du pilote (la Table 0 doit etre vide) ==")
    porte_suivi = outils / "suivi-pilote.py"
    if not porte_suivi.is_file():
        print("  suivi-pilote: ABSENT")
        ko.append("manquant: suivi-pilote.py")
    else:
        r = lancer_enfant([sys.executable, str(porte_suivi), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        vert = r.returncode == 0
        print("  suivi-pilote: " + ("OK" if vert else "KO"))
        for ligne in r.stdout.splitlines():
            if ligne.startswith("[KO]"):
                print("    " + ligne.strip()[:150])
            if ligne.startswith("[--]") and "OUVERTE" in ligne:
                print("    " + ligne.strip()[:150])
            if ligne.startswith("VERDICT"):
                print("    " + ligne.strip()[:150])
        if not vert:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("[KO]")]
            ko.append("suivi-pilote: " + ("; ".join(ecarts) if ecarts
                                          else "voir suivi-pilote.py -- la Table 0 n est pas vide"))

    # 38. CONTROLE D'ATTRIBUTION (ORDRE 3.2, M-153, MO-357) : une source a
    #     CHANGE -- par quelle PORTE ? Aucun controle ne repondait : l'empreinte
    #     d'integrite dit QU'il y a eu ecriture, jamais QUI l'a faite, et un outil
    #     natif ou une commande du shell laissent la MEME trace qu'une porte. Ce
    #     maillon exige que chaque changement posterieur a la pose porte une NOTE
    #     TRACEE posterieure, au domicile des modifications : sans note, ECRITURE
    #     HORS DE SA PORTE, accusee nommement. Les exclusions (formes d'etat,
    #     etats de routines, points de restauration, zones jetables, archives) sont
    #     DECLAREES ET COMPTEES -- une exclusion muette serait un angle mort
    #     (L-104). La portee est MESUREE a la pose (L-286) : le controle ne doit
    #     pas accuser une ecriture legitime.
    print("== 38. attribution (toute ecriture passe par sa porte) ==")
    garde_attribution = outils / "controle-attribution.py"
    if not garde_attribution.is_file():
        print("  attribution: ABSENT")
        ko.append("manquant: controle-attribution.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_attribution), "verifier"],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print("  attribution: " + etat)
        for ligne in r.stdout.splitlines():
            depouille = ligne.strip()
            if (depouille.startswith("- ") or depouille.startswith("changees depuis")
                    or depouille.startswith("sources NEUVES")):
                print("    " + depouille[:150])
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("- ")]
            ko.append("attribution: " + ("; ".join(ecarts[:6]) if ecarts
                      else "voir controle-attribution.py"))
    # 39. GARDE DES VERSIONS (R-003 / R-004 / ORDRE 3.4, M-154, MO-358) : les
    #     fichiers v1/v2 ne sont JAMAIS touches par la v3 et la v3 ne les
    #     ADRESSE pas. Deux populations : les sources GELEES dont l'empreinte a
    #     change (ou apparu, ou disparu) depuis la pose, et les litteraux du CODE
    #     de la v3 qui ATTEIGNENT une zone gelee. Une MENTION (commentaire,
    #     message, liste d'interdiction) n'est pas une adresse : la difference est
    #     mesuree, sinon le garde accuserait des fichiers sains des la pose.
    print("== 39. versions (v1/v2 gelees, aucune adresse de la v3) ==")
    garde_versions = outils / "garde-versions.py"
    if not garde_versions.is_file():
        print("  versions: ABSENT")
        ko.append("manquant: garde-versions.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_versions), "verifier"],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print("  versions: " + etat)
        for ligne in r.stdout.splitlines():
            depouille = ligne.strip()
            if depouille.startswith("- ") or depouille.startswith("code de la v3"):
                print("    " + depouille[:150])
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("- ")]
            ko.append("versions: " + ("; ".join(ecarts[:6]) if ecarts
                      else "voir garde-versions.py"))
    # 40. PLAFOND DES ACTES EN ATTENTE (P4 du createur, 2026-09-20 ; M-155,
    #     MO-361) : < UN GARDE ACCUSE quand le nombre d ACTES EN ATTENTE depasse
    #     un PLAFOND DECLARE -- une masse qui grandit en silence n est pas une
    #     politique >. La PORTE existe deja (bdd-conservation controler-plafond)
    #     et la cloture du pilote l appelle -- mais AUCUN controle PERMANENT ne la
    #     lisait : mesure du 2026-09-22, les 15 pannes declarees du suivi du pilote
    #     n en portaient aucune. Un stock qui grossit ne se voit donc qu a la
    #     cloture, et jamais dans la suite : c est exactement le piege MO-246 (un
    #     controle qui vit dans un cobaye meurt avec lui). Ce maillon la lit.
    print("== 40. plafond des actes en attente (P4) ==")
    porte_plafond = ["bdd-conservation", "controler-plafond"]
    lanceur = zone.parent.parent / "lancer.py"
    r = lancer_enfant([sys.executable, str(lanceur)] + porte_plafond,
                       capture_output=True, text=True, cwd=str(lanceur.parent))
    etat = "OK" if r.returncode == 0 else "KO"
    print("  plafond: " + etat)
    for ligne in r.stdout.splitlines():
        depouille = ligne.strip()
        if (depouille.startswith("VERDICT") or depouille.startswith("plafond declare")
                or depouille.startswith("actes en attente") or depouille.startswith("ECART")):
            print("    " + depouille[:150])
    if r.returncode != 0:
        ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("ECART")]
        ko.append("plafond: " + ("; ".join(ecarts[:4]) if ecarts
                  else "voir bdd-conservation controler-plafond"))
    # 41. TITRE DES ITEMS (mesure 2026-09-23) : DEUX items sur 29 portaient un NOM
    #     DU VIVIER dans `theme` -- le TITRE de la demande -- et la file affichait
    #     `OUTIL` la ou on attend une phrase. Les deux items ont ete RE-TITRES par le
    #     verbe `corriger` (id conserve) et les DEUX portes de depot refusent ce theme
    #     AVANT toute ecriture. Ce maillon juge LES DEUX ARBRES (la Matrice et
    #     l'operateur) par le GARDE DE CHAQUE ARBRE (sa porte, M-042 -- aucune liste
    #     recopiee ici), PROUVE que les deux portes refusent sans laisser naitre
    #     d'item, et REJOUE ses cobayes : le detecteur est vu mordre et passer.
    #     Sans ce maillon le garde vivrait dans un cobaye, et MO-246 est formel : un
    #     controle qui vit dans un cobaye meurt avec lui.
    print("== 41. titre des items (un titre n'est pas une etiquette du vivier) ==")
    garde_titre = outils / "verifier-titre-item.py"
    if not garde_titre.is_file():
        print("  titre: ABSENT")
        ko.append("manquant: verifier-titre-item.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_titre), "--racine", str(zone.parent.parent),
                            "--auto-test"],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print("  titre: " + etat)
        for ligne in r.stdout.splitlines():
            depouille = ligne.strip()
            if (depouille.startswith("[KO") or depouille.startswith("cobaye NON REPERE")
                    or depouille.startswith("VERDICT")):
                print("    " + depouille[:150])
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith("[KO")]
            ko.append("titre: " + ("; ".join(ecarts[:6]) if ecarts
                      else "voir verifier-titre-item.py"))

    # 42. RESIDUS DES ZONES JETABLES (MO-378) : garde-tmp juge le DOMICILE des
    #     zones et leur README, jamais leur CONTENU -- un residu RESTE dans une
    #     zone apres une cloture n etait donc accuse par PERSONNE. Ce maillon
    #     lance le garde garde-residus-zone.py : son --auto-test prouve qu il CRIE
    #     sur un cobaye (residu non canonique, purge mentie) et se TAIT sur une
    #     zone propre, puis il lit les zones REELLES. La zone du cameleon est citee
    #     HORS Matrice : le garde la resout par son domicile declare (zone_tmp).
    #     Sans ce maillon le garde vivrait dans un cobaye, et MO-246 est formel :
    #     un controle qui vit dans un cobaye meurt avec lui.
    print("== 42. residus des zones jetables ==")
    garde_residus = outils / "garde-residus-zone.py"
    if not garde_residus.is_file():
        print("  residus: ABSENT")
        ko.append("manquant: garde-residus-zone.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_residus), "--auto-test"],
                           capture_output=True, text=True)
        print("  cobaye: " + ("OK" if r.returncode == 0 else "KO"))
        for ligne in r.stdout.splitlines():
            depouille = ligne.strip()
            if depouille.startswith("[KO") or depouille.startswith("AUTO-TEST"):
                print("    " + depouille[:150])
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("[KO")]
            ko.append("residus (cobaye): " + ("; ".join(ecarts[:6]) if ecarts
                      else "voir garde-residus-zone.py --auto-test"))
        else:
            r2 = lancer_enfant([sys.executable, str(garde_residus),
                                 "--racine", str(zone.parent.parent)],
                                capture_output=True, text=True)
            print("  zones reelles: " + ("OK" if r2.returncode == 0 else "KO"))
            for ligne in r2.stdout.splitlines():
                depouille = ligne.strip()
                if depouille.startswith("ECARTS") or depouille.startswith("- "):
                    print("    " + depouille[:150])
            if r2.returncode != 0:
                ecarts = [l.strip() for l in r2.stdout.splitlines() if l.strip().startswith("- ")]
                ko.append("residus (zones reelles): " + ("; ".join(ecarts[:6]) if ecarts
                          else "voir garde-residus-zone.py"))

    # 43. CREDIBILITE DES MISSIONS ANCIENNES (MO-409) : le process
    #     verifier-credibilite-missions.py n etait joue QUE par le DEMARRAGE
    #     du pilote, et ses COBAYES par personne : le mordant ajoute par MO-409
    #     (le DOUBLON DE FAIT, lu dans les TAGS de
    #     matrice/data/modifications-par-fichier.json) n aurait donc vecu que
    #     dans un cobaye -- et MO-246 est formel : un controle qui vit dans un
    #     cobaye meurt avec lui. Ce maillon REJOUE ses cobayes : le mordant est
    #     vu MORDRE (un fichier deja livre par une mission TERMINEE anterieure
    #     -> deja-faite) et vu EPARGNER (meme nom sans livraison, JUMEAU d un
    #     autre dossier, texte AVANT/APRES, source non relisible), et il exige
    #     que l ANGLE MORT du doublon soit DIT dans le motif (L-163 : un vert
    #     muet ne dit pas ce qu il ne mesure pas).
    print("== 43. credibilite des missions anciennes ==")
    processus_credibilite = outils / "verifier-credibilite-missions.py"
    if not processus_credibilite.is_file():
        print("  credibilite: ABSENT")
        ko.append("manquant: verifier-credibilite-missions.py")
    else:
        r = lancer_enfant([sys.executable, str(processus_credibilite), "--auto-test"],
                          capture_output=True, text=True)
        print("  cobaye: " + ("OK" if r.returncode == 0 else "KO"))
        for ligne in r.stdout.splitlines():
            depouille = ligne.strip()
            if (depouille.startswith("VERDICT") or depouille.startswith("[KO")
                    or "DOUBLON DE FAIT" in depouille or "angle mort" in depouille
                    or "RESTAUREE hier" in depouille):
                print("    " + depouille[:150])
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith("[KO")]
            ko.append("credibilite (cobaye): " + ("; ".join(ecarts[:6]) if ecarts
                      else "voir verifier-credibilite-missions.py --auto-test"))

    # 44. LES EPREUVES DU SUIVI DU PILOTE (MO-416) : le maillon 37 RECALCULE la
    #     vue -- il joue donc bien les detecteurs -- mais il ne rejouait AUCUNE de
    #     leurs EPREUVES : le mordant ajoute par MO-416 (la SOURCE NON INJECTEE,
    #     lue dans la TRACE DECLAREE) et la REPARATION de l epreuve de pause n
    #     auraient donc vecu que dans un auto-test que PERSONNE ne lancait -- et
    #     MO-246 est formel : un controle qui vit dans un cobaye meurt avec lui.
    #     Ce maillon REJOUE l auto-test de la porte, qui MORD (absence de trace
    #     d injection ; pause CONTRADICTOIRE) et EPARGNE (la trace declaree, la
    #     mission qui ne redemande rien, la mission servie AVANT la pose, la paire
    #     de pause coherente). Meme racine que le maillon 37.
    print("== 44. epreuves du suivi du pilote ==")
    if not porte_suivi.is_file():
        print("  suivi-pilote: ABSENT")
        ko.append("manquant: suivi-pilote.py")
    else:
        r = lancer_enfant([sys.executable, str(porte_suivi),
                           "--racine", str(zone.parent.parent), "--auto-test"],
                          capture_output=True, text=True)
        print("  epreuves: " + ("OK" if r.returncode == 0 else "KO"))
        for ligne in r.stdout.splitlines():
            depouille = ligne.strip()
            if depouille.startswith("[KO") or "NON INJECTEE" in depouille:
                print("    " + depouille[:150])
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines()
                      if l.strip().startswith("[KO")]
            ko.append("suivi-pilote (epreuves): " + ("; ".join(ecarts[:6]) if ecarts
                      else "voir suivi-pilote.py --auto-test"))

    # 45. LA LISTE DES MAILLONS (MO-427) : le maillon [chaine] du theme CADRAGE exige
    #     que la chaine devienne un FICHIER DE PILOTAGE ecrit par un OUTIL. Mesure du
    #     2026-09-26 : la chaine n existait QUE comme texte imprime (sept maillons
    #     types et prouvables affiches, aucun fichier) -- et RIEN ne le voyait : un
    #     texte imprime se lit comme une chaine complete. Le garde LIT le vocabulaire
    #     des types a son domicile (entonnoir/listes.py) et rejoue son autotest : le
    #     controle est PERMANENT, jamais un cobaye qui meurt avec tmp-optimus.
    print("== 45. la liste des maillons (ecrite, ordonnee, typee, prouvable) ==")
    garde_maillons = outils / "verifier-maillons.py"
    if not garde_maillons.is_file():
        print("  maillons: ABSENT")
        ko.append("manquant: verifier-maillons.py")
    else:
        r = lancer_enfant([sys.executable, str(garde_maillons), "--racine", str(zone.parent.parent)],
                           capture_output=True, text=True)
        etat = "OK" if r.returncode == 0 else "KO"
        print(f"  maillons: {etat}")
        if r.returncode != 0:
            ecarts = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("[KO")]
            ko.append("maillons: " + ("; ".join(ecarts) if ecarts else "voir verifier-maillons.py"))

    # 46. PORTE DE SAUT DU LOT (MO-470 / EO-445) : une chaine dont les maillons sont
    #     ENTRELACES avec des missions etrangeres dans un lot arme n avait AUCUN
    #     chemin (conduire refuse une mission du lot, reporter ne charge pas la
    #     suivante, aucun verbe ne reordonne). Ce maillon MORD sur l ORDRE SERVI (le
    #     lot porte sa suite, L-151) et sur `avancer_du_lot` : la visee passe en tete
    #     sans perdre personne ; hors lot, mission morte et absence de lot sont
    #     REFUSES en le nommant. Eprouve EN MEMOIRE (aucune file touchee).
    print("== 46. porte de saut du lot (avancer_du_lot) ==")
    ecarts_saut = _eprouver_saut_lot(zone.parent.parent)
    print("  saut-lot: " + ("OK" if not ecarts_saut else "KO"))
    if ecarts_saut:
        for ecart in ecarts_saut:
            print("    [KO] " + ecart)
        ko.append("saut-lot: " + "; ".join(ecarts_saut[:6]))

    # 47. LA FICHE TECHNIQUE DE TRAVAIL (MO-471, decisions D2/D3/D4) : le cadrage
    #     < templates d injection > a exige une fiche PLUS LEGERE, SANS PERDRE ce qui
    #     decide, et un PLAFOND GLOBAL declare. Ce maillon MORD sur une fiche qui ne
    #     bornerait rien (pas plus legere), qui ACCUSERAIT une injection coherente, ou
    #     qui ne crierait PAS sur un champ du NOYAU absent ; il EPARGNE une injection
    #     complete. Eprouve EN MEMOIRE (aucune ecriture).
    print("== 47. la fiche technique de travail (bornee, sans perte) ==")
    ecarts_fiche = _eprouver_fiche(zone.parent.parent)
    print("  fiche: " + ("OK" if not ecarts_fiche else "KO"))
    if ecarts_fiche:
        for ecart in ecarts_fiche:
            print("    [KO] " + ecart)
        ko.append("fiche: " + "; ".join(ecarts_fiche[:6]))

    # 48. LES MOULES DE LA FICHE D INJECTION (MO-471, decisions D1/D5) : un moule a
    #     jetons par CATEGORIE vit a son domicile (injection/templates/) et le
    #     moteur le REND. Ce maillon MORD sur un jeton inconnu (il doit etre NOMME,
    #     jamais remplace en silence) et sur un moule du domicile qui porterait un
    #     jeton hors du moteur ou un trou non rendu ; il EPARGNE un rendu coherent.
    #     Eprouve EN MEMOIRE (aucune ecriture).
    print("== 48. les moules de la fiche d injection (rendu, sans trou muet) ==")
    ecarts_moule = _eprouver_fiche_moule(zone.parent.parent)
    print("  moules-fiche: " + ("OK" if not ecarts_moule else "KO"))
    if ecarts_moule:
        for ecart in ecarts_moule:
            print("    [KO] " + ecart)
        ko.append("moules-fiche: " + "; ".join(ecarts_moule[:6]))

    # 49. L ENCART /remise DU COCKPIT (MO-474) : le POIDS DE REMISE PAR ROUND doit
    #     etre VISIBLE pour surveiller, dans le TEMPS, le PLAFOND DE REMISE (MO-473).
    #     Ce maillon MORD sur une route NON branchee (fonction absente, ROUTERS ou
    #     ROUTES sans `remise`) et sur un cockpit qui RECOPIERAIT le plafond au lieu
    #     de le CONSOMMER chez son domicile ; il EPARGNE le fichier reel et se
    #     CONTRE-EPROUVE sur un cockpit fabrique (L-032). Eprouve sur le TEXTE
    #     (aucune ecriture, aucun processus lance).
    print("== 49. l encart /remise du cockpit (branche, consomme son domicile) ==")
    ecarts_remise = _eprouver_remise_cockpit(zone.parent.parent)
    print("  remise-cockpit: " + ("OK" if not ecarts_remise else "KO"))
    if ecarts_remise:
        for ecart in ecarts_remise:
            print("    [KO] " + ecart)
        ko.append("remise-cockpit: " + "; ".join(ecarts_remise[:6]))

    # 50. LA BOITE DU CAMELEON EST UNE TRACE, PAS UN CANAL (MO-441, ecart EC4 de
    #     l audit MO-365) : le pilote du Flux 1 depose son injection et AUCUN
    #     lecteur de contenu ne la reprend (les seuls lecteurs sont la TAILLE,
    #     cockpit, et la LISIBILITE, maillon 6). La decision -- TRACE, le canal est
    #     la FILE -- doit rester VRAIE : la declaration se CONSOMME chez son
    #     domicile, le depot la PORTE (les deux chemins), et le statut remet la
    #     checklist lue dans la file. Ce maillon MORD sur un depot muet, sur une
    #     declaration recopiee et sur la checklist absente ; il EPARGNE les
    #     fichiers reels et se CONTRE-EPROUVE en memoire (L-032).
    print("== 50. la boite du cameleon est une TRACE (declaree, portee, protegee) ==")
    ecarts_boite = _eprouver_boite_trace(zone.parent.parent)
    print("  boite-trace: " + ("OK" if not ecarts_boite else "KO"))
    if ecarts_boite:
        for ecart in ecarts_boite:
            print("    [KO] " + ecart)
        ko.append("boite-trace: " + "; ".join(ecarts_boite[:6]))

    # 51. LE REFUS DU BILAN ETRANGER (MO-480 / EO-455) : la panne payee en MO-440 --
    #     la mission SERVIE close avec le bilan d une AUTRE. Le JOURNAL ne peut pas la
    #     voir (la fin nomme bien la mission close) : journal, file et controle de
    #     coherence disaient tous D ACCORD. Ce maillon rejoue le jugement du DOMICILE
    #     (data/commun/cloture_fausse.py) sur le CORPUS REEL : il MORD sur les DEUX
    #     clotures fausses reelles (MO-407 et MO-440) et exige EXACTEMENT ces deux-la
    #     (une troisieme accusation serait une faute neuve ou une regle qui se met a
    #     crier) ; il EPARGNE les autres bilans et se CONTRE-EPROUVE sur les titres
    #     sans identifiant, la famille M- contre MO-, et un recit qui cite une autre
    #     mission. Eprouve EN MEMOIRE (aucune ecriture, aucun processus lance).
    print("== 51. le refus du bilan etranger (le titre declare la mission close) ==")
    ecarts_bilan = _eprouver_bilan_etranger(zone.parent.parent)
    print("  bilan-etranger: " + ("OK" if not ecarts_bilan else "KO"))
    if ecarts_bilan:
        for ecart in ecarts_bilan:
            print("    [KO] " + ecart)
        ko.append("bilan-etranger: " + "; ".join(ecarts_bilan[:6]))

    # 52. LA PROMOTION AUTOMATIQUE (MO-481 / EO-457) : la regle du createur -- < un
    #     item plus important que la mission en cours se reclasse seul >, sans JAMAIS
    #     interrompre le round qui tourne (serie stricte). Ce maillon execute le
    #     DOMICILE reel (data/commun/promotion.py) et MORD sur les cas reels : il
    #     promeut un item STRICTEMENT plus important (gravite, puis niveau DANS la
    #     bande), EPARGNE une importance egale ou moindre, et prouve l ORDRE (prefixe
    #     intact, suite reclassee, tri STABLE). Il verifie AUSSI le cablage (le pilote
    #     importe le domicile, la cloture l appelle). Eprouve EN MEMOIRE (aucune
    #     ecriture, aucun processus lance).
    print("== 52. la promotion automatique (un item plus important se reclasse) ==")
    ecarts_promotion = _eprouver_promotion(zone.parent.parent)
    print("  promotion: " + ("OK" if not ecarts_promotion else "KO"))
    if ecarts_promotion:
        for ecart in ecarts_promotion:
            print("    [KO] " + ecart)
        ko.append("promotion: " + "; ".join(ecarts_promotion[:6]))

    # 53. LA SOURCE BDD PRIVEE (MO-482 / EO-458) : la decision du createur -- une
    #     BDD de raisonnement pour OPTIMUS, DANS LA ZONE INVISIBLE, declaree au
    #     moteur comme source PRIVEE (servie seulement sous --prive, L-016). Ce
    #     maillon MORD sur l absence de declaration, de lecture privee ou de refus
    #     sans --prive, et verifie que le generateur cible bien la zone invisible
    #     (jamais sous matrice/). Eprouve EN MEMOIRE (aucune ecriture, aucun
    #     processus lance).
    print("== 53. la source BDD privee (BDD de raisonnement d Optimus) ==")
    ecarts_privee = _eprouver_source_privee(zone.parent.parent)
    print("  source-privee: " + ("OK" if not ecarts_privee else "KO"))
    if ecarts_privee:
        for ecart in ecarts_privee:
            print("    [KO] " + ecart)
        ko.append("source-privee: " + "; ".join(ecarts_privee[:6]))

    # 54. LA SOURCE BDD PARTAGEE (MO-483 / EO-459) : la decision du createur --
    #     la BDD de raisonnement du CAMELEON vit dans SON domicile
    #     (agents/cameleon/raisonnement/), VISIBLE et PARTAGEE : le moteur la sert
    #     SANS --prive. Ce maillon MORD sur l absence de declaration, de lecture
    #     partagee, de zone du generateur ou de surcharge. Eprouve EN MEMOIRE.
    print("== 54. la source BDD partagee (BDD de raisonnement du cameleon) ==")
    ecarts_partagee = _eprouver_source_partagee(zone.parent.parent)
    print("  source-partagee: " + ("OK" if not ecarts_partagee else "KO"))
    if ecarts_partagee:
        for ecart in ecarts_partagee:
            print("    [KO] " + ecart)
        ko.append("source-partagee: " + "; ".join(ecarts_partagee[:6]))
    # 55. LE 0 MUET SUR UN CHAMP A VALEURS MULTIPLES (MO-450) : quand --champ
    #     interroge une cle qui porte une LISTE (les valeurs separent par la
    #     virgule -- convention des liens), viser UN element rendait un 0 nu,
    #     indiscernable d une absence alors que la valeur EXISTE. Le gap DIT
    #     desormais que la valeur figure et NOMME le mode dedie (--lien). Ce maillon
    #     execute le DOMICILE reel (carte_identite.valeur_dans_champ_multiple),
    #     MORD sur un element de liste, EPARGNE un champ unique et une valeur
    #     absente, et verifie le cablage de la porte. Eprouve EN MEMOIRE.
    print("== 55. le 0 muet sur un champ a valeurs multiples (nomme --lien) ==")
    ecarts_champ_multiple = _eprouver_champ_multiple(zone.parent.parent)
    print("  champ-multiple: " + ("OK" if not ecarts_champ_multiple else "KO"))
    if ecarts_champ_multiple:
        for ecart in ecarts_champ_multiple:
            print("    [KO] " + ecart)
        ko.append("champ-multiple: " + "; ".join(ecarts_champ_multiple[:6]))

    # 56. LE ROUND SERVI ET JAMAIS CONDUIT (MO-451) : la machine a SERVI et PRIS le
    #     round suivant, et l agent a rendu la main sur un bilan-rapport. Le FAIT
    #     vit au DOMICILE PARTAGE (data/commun/round_servi.py) et se dit SANS seuil
    #     (rappel a la remise des ordres) ; le suivi le crie, lui, apres SON seuil.
    #     Ce maillon MORD sur une prise restee seule, EPARGNE un round conduit (et
    #     le contre-temoin d une chaine fermee : aucun candidat), et verifie que le
    #     pilote et le suivi CONSOMMENT la MEME regle. Eprouve EN MEMOIRE.
    print("== 56. le round servi et jamais conduit (rappele sans seuil) ==")
    ecarts_round_servi = _eprouver_round_servi(zone.parent.parent)
    print("  round-servi: " + ("OK" if not ecarts_round_servi else "KO"))
    if ecarts_round_servi:
        for ecart in ecarts_round_servi:
            print("    [KO] " + ecart)
        ko.append("round-servi: " + "; ".join(ecarts_round_servi[:6]))

    # 57. LA PORTE DE REGULARISATION (MO-461 / EO-433) : une FIN au JOURNAL pour une
    #     mission que la FILE disait encore < en-attente > ne pouvait etre fermee par
    #     AUCUNE porte (`enregistrer` refuse un id deja present, `fin` ne close que la
    #     mission EN COURS) : le controle de coherence rendait des ecarts que rien ne
    #     pouvait faire tomber. Ce maillon joue la porte sur une racine JETABLE et
    #     fait trancher le CONTROLE REEL : il MORD (avant = 3 ecarts, apres la porte
    #     il n en reste qu UN -- les 2 de la mission regularisee TOMBENT), il EPARGNE
    #     le contre-temoin (une mission terminee dans la file SANS fin au journal est
    #     REFUSEE, sa file est INTACTE et le controle l ACCUSE TOUJOURS), il NOMME les
    #     refus et verifie le CABLAGE (routeur, vocabulaire d action, borne declaree
    #     IDEMPOTENTE, acte a son propre verbe). Eprouve EN MEMOIRE + racine jetable.
    print("== 57. la porte de regularisation (les ecarts tombent par la porte) ==")
    ecarts_regularisation = _eprouver_regularisation(zone.parent.parent)
    print("  regularisation: " + ("OK" if not ecarts_regularisation else "KO"))
    if ecarts_regularisation:
        for ecart in ecarts_regularisation:
            print("    [KO] " + ecart)
        ko.append("regularisation: " + "; ".join(ecarts_regularisation[:6]))

    # 58. L INTERRUPTION (MO-464 / EO-436) : quand un round est INTERROMPU, le pilote
    #     PARQUAIT sa courante et FORGEAIT la suivante dans la MEME seconde (mesure du
    #     2026-09-25, et de nouveau le 2026-09-28 a 06:51:48) : DEUX missions restaient
    #     OUVERTES, la file ne disait plus laquelle le round reprend, et le suivi a
    #     accuse une CLOTURE FAUSSE qui n avait pas eu lieu. Ce maillon JOUE le refus
    #     (le geste mesure est mort), le REMEDE (`charger --conduire` forge ET sert dans
    #     le meme geste), le CONTRE-TEMOIN (file ordinaire), le LOT (meme refus) et le
    #     CABLAGE (les deux chargements, l usage documente, l exception LEVEE).
    #     Eprouve EN MEMOIRE : aucune trace du depot n est touchee.
    print("== 58. l interruption parque : elle ne charge pas (charger --conduire) ==")
    ecarts_interruption = _eprouver_interruption(zone.parent.parent)
    print("  interruption: " + ("OK" if not ecarts_interruption else "KO"))
    if ecarts_interruption:
        for ecart in ecarts_interruption:
            print("    [KO] " + ecart)
        ko.append("interruption: " + "; ".join(ecarts_interruption[:6]))

    # 59. L INVERSION DES CONTROLES (MO-487 / EO-462) : un controle dont l etat NORMAL
    #     est ROUGE est INVERSE. Deux cas mesures : (1) l epreuve `invisibilite` du
    #     benchmark rendait ROUGE < FUITE L-016 > tout fichier de NOTRE zone invisible
    #     (le cas normal) -- elle CONSTATE desormais la zone ; (2) le declencheur
    #     `perimetre-write` de la defcon s allumait sur `.kilo/.gitignore`, un fichier
    #     de l OUTIL EXTERIEUR declare -- le domicile met desormais de cote `.kilo`
    #     entier. Le maillon JOUE les deux cas normaux ET leurs CONTRE-TEMOINS.
    print("== 59. un controle dont l etat NORMAL est ROUGE est INVERSE ==")
    ecarts_inverses = _eprouver_controles_inverses(zone.parent.parent)
    print("  controles-inverses: " + ("OK" if not ecarts_inverses else "KO"))
    if ecarts_inverses:
        for ecart in ecarts_inverses:
            print("    [KO] " + ecart)
        ko.append("controles-inverses: " + "; ".join(ecarts_inverses[:6]))

    # 60. LE DOMICILE UNIQUE DE LA REGLE ASCII (MO-466 / EO-365) : la MEME regle
    #     (NFKD + encodage ASCII `ignore`) vivait recopiee en trois exemplaires --
    #     assainir_ascii (bdd-sessions/ajouter), vers_ascii (suivi-optimus/vue) et
    #     titre_vers_slug (chaine-pense-bete, celle-la non declaree). Le round les a
    #     reunies dans data/commun/texte_ascii.py. Ce maillon MORD si une copie
    #     repousse : il JOUE son detecteur sur des arbres FABRIQUES (contre-temoin
    #     epargne, cobaye accusateur) avant de le jouer sur l arbre REEL.
    print("== 60. la regle ASCII vit a UN SEUL domicile (aucune copie) ==")
    ecarts_domicile_ascii = _eprouver_domicile_ascii(zone.parent.parent)
    print("  domicile-ascii: " + ("OK" if not ecarts_domicile_ascii else "KO"))
    if ecarts_domicile_ascii:
        for ecart in ecarts_domicile_ascii:
            print("    [KO] " + ecart)
        ko.append("domicile-ascii: " + "; ".join(ecarts_domicile_ascii[:6]))

    # 61. LA DEMANDE DE SEGMENT DE RAISONNEMENT A LA CLOTURE (MO-500 / EO-478) :
    #     l audit MO-499 a mesure que le mecanisme du raisonnement segmente existait
    #     ENTIER -- outil, BDD, source declaree au moteur, maillons 53 et 54 -- et
    #     qu AUCUN chemin de round ne l appelait : les deux BDD restaient au segment
    #     FONDATEUR, celui de la mission qui a construit le mecanisme. Ce maillon
    #     mesure donc le BRANCHEMENT (les DEUX clotures demandent, la loi du round le
    #     dit), EPROUVE la regle en EXECUTION sur des fixtures jetables (un cobaye
    #     qui MORD, un contre-temoin qui EPARGNE) et la mesure ensuite sur la DONNEE
    #     REELLE du depot.
    print("== 61. la cloture DEMANDE le segment de raisonnement (deposer, ou le DIRE) ==")
    ecarts_segment = _eprouver_demande_segment(zone.parent.parent)
    print("  demande-segment: " + ("OK" if not ecarts_segment else "KO"))
    if ecarts_segment:
        for ecart in ecarts_segment:
            print("    [KO] " + ecart)
        ko.append("demande-segment: " + "; ".join(ecarts_segment[:6]))

    # 62. LE DOMICILE UNIQUE DE LA REGLE DES NOMS PROCHES (MO-468 / EO-384) : la MEME
    #     regle < les noms PROCHES d un nom fautif > vivait en DEUX copies qui ne se
    #     comportaient PAS pareil -- INCLUSION + PROXIMITE dans resolution_outils.py,
    #     SOUS-CHAINE seule dans pilote/injection/modes_emploi.py : le refus du pilote
    #     se taisait sur une lettre oubliee, la ou la facade proposait deja (L-029).
    #     Ce maillon MORD sur une copie qui repousse des DEUX cotes (Matrice ET
    #     operateur) et sur un consommateur qui cesse de consommer ; il EPROUVE la
    #     regle en EXECUTION (cobaye : une lettre oubliee est proposee ; contre-temoins :
    #     un nom vide et un nom etranger ne proposent RIEN) et il CHARGE les DEUX
    #     consommateurs pour exiger que l objet de regle qu ils emploient soit CELUI du
    #     domicile.
    print("== 62. la regle des noms proches vit a UN SEUL domicile (aucune copie) ==")
    ecarts_noms_proches = _eprouver_domicile_noms_proches(zone.parent.parent)
    print("  domicile-noms-proches: " + ("OK" if not ecarts_noms_proches else "KO"))
    if ecarts_noms_proches:
        for ecart in ecarts_noms_proches:
            print("    [KO] " + ecart)
        ko.append("domicile-noms-proches: " + "; ".join(ecarts_noms_proches[:6]))

    # 63. LE PATTERN DE MAINTENANCE (MO-488 / EO-446) : le createur a demande un
    #     PATTERN de MAINTENANCE injecte EN DEBUT DE SESSION, qui dit a l agent de
    #     la maintenance que la v3 evolue en PERMANENCE -- donc que des missions
    #     anciennes, des fichiers pas encore conformes et des artefacts de
    #     transition sont un ETAT DE TRANSITION : ni une panne, ni une raison de
    #     masquer ou de casser. Ce maillon EXECUTE les DEUX injecteurs de demarrage
    #     (le pattern PRESENT dans la maintenance, ABSENT de l autre flux, L-016),
    #     juge le catalogue REEL par le jugement pur, et JOUE ce jugement sur un
    #     contre-temoin et six cobayes. Eprouve EN MEMOIRE + deux processus de
    #     lecture (aucune ecriture).
    print("== 63. le pattern de maintenance (branche au demarrage, invisible ailleurs) ==")
    ecarts_pattern = _eprouver_pattern_maintenance(zone.parent.parent)
    print("  pattern-maintenance: " + ("OK" if not ecarts_pattern else "KO"))
    if ecarts_pattern:
        for ecart in ecarts_pattern:
            print("    [KO] " + ecart)
        ko.append("pattern-maintenance: " + "; ".join(ecarts_pattern[:6]))

    # 64. LA CITATION DE LA ZONE DES SOURCES (MO-489 / EO-451) : le garde du marbre
    #     accusait une ligne morte de l index des protocoles -- une citation de
    #     `docs/conversation-unslot-gemma-4.md`, dont le document a ete SUPPRIME par le
    #     commit du createur (8ff87a76, 2026-09-27). Or la porte ECRIRE REFUSE toute
    #     ecriture dans docs/ en la nommant (zone_sources.py, MO-377) : le garde
    #     exigeait donc une ecriture que la porte du MEME domaine interdit. La Matrice
    #     l avait deja recouvree par git (MO-320) et le commit suivant l a retiree --
    #     recouvrement en PURE PERTE, et rouge permanent sur /sante depuis le 26/09.
    #     Le jugement CONSOMME desormais le domicile de la zone et DIT ce qu il mesure
    #     sans le juger. Ce maillon MORD sur une ligne morte de la MATRICE et sur un nom
    #     nu absent, EPARGNE la zone des sources, refuse une exemption MUETTE, et
    #     EXECUTE le garde du depot : code 0, aucun ECART, exemption DITE.
    print("== 64. une citation de la zone des SOURCES est MESUREE et DITE, jamais accusee ==")
    ecarts_citation = _eprouver_citation_sources(zone.parent.parent)
    print("  citation-sources: " + ("OK" if not ecarts_citation else "KO"))
    if ecarts_citation:
        for ecart in ecarts_citation:
            print("    [KO] " + ecart)
        ko.append("citation-sources: " + "; ".join(ecarts_citation[:6]))

    # 65. LE PROCESSUS DES SUPER-COMBOS (MO-491 / EO-447) : le createur a demande un
    #     PROCESS INJECTE qui NOMME et LANCE les super-combos quand on corrige,
    #     ameliore ou modifie des fichiers et des flux, AVEC LA PREUVE du passage.
    #     Mesure : la Matrice possedait les combos et l agent savait quand les
    #     employer, mais rien ne FORCAIT leur passage -- et la PREUVE n existait pas
    #     (1 occurrence sur 65686 lignes de registre, aucune trace au lanceur). Ce
    #     round livre la TRACE (le lanceur NOTE chaque passage par la porte des
    #     usages), le JUGE (`--preuves <MO-XXX> --combos ...`, qui ACCUSE et NOMME)
    #     et le PROCESSUS injecte au demarrage. Ce maillon EPROUVE le cablage, JOUE
    #     le jugement (contre-temoin epargne, quatre cobayes mordants) et MESURE le
    #     lanceur du depot dans les deux sens.
    print("== 65. le processus des super-combos (nomme, lance, prouve) ==")
    ecarts_processus = _eprouver_processus_super_combos(zone.parent.parent)
    print("  processus-super-combos: " + ("OK" if not ecarts_processus else "KO"))
    if ecarts_processus:
        for ecart in ecarts_processus:
            print("    [KO] " + ecart)
        ko.append("processus-super-combos: " + "; ".join(ecarts_processus[:6]))

    # 66. LA PASSERELLE USER (MO-492 / EO-452) : la decision du createur (MO-475) etait
    #     ecrite DANS UN SEUL instrument, donc `garde-ascii` accusait la MEME zone que
    #     le controle d attribution exemptait : code 1 sur DEUX fichiers de
    #     `user-demandes/`, et un rouge permanent sur /sante pour une ecriture LEGITIME
    #     (la passerelle ou le user ecrit ses demandes en clair, que la Matrice suit et
    #     EXTRAIT). La declaration a desormais UN DOMICILE, consomme par les DEUX
    #     instruments, ECRIT dans la regle qui fait foi ; le garde DIT ce qu il met de
    #     cote. Ce maillon JOUE le jugement (mord sur la passerelle, epargne un homonyme
    #     profond), EPROUVE le cablage des deux consommateurs, et EXECUTE le garde du
    #     depot : code 0 sur la passerelle et sur la Matrice entiere, ACCUSATION sur un
    #     vrai non-ASCII hors zone.
    print("== 66. la passerelle user est hors jugement, au meme domicile pour tous ==")
    ecarts_passerelle = _eprouver_passerelle_user(zone.parent.parent)
    print("  passerelle-user: " + ("OK" if not ecarts_passerelle else "KO"))
    if ecarts_passerelle:
        for ecart in ecarts_passerelle:
            print("    [KO] " + ecart)
        ko.append("passerelle-user: " + "; ".join(ecarts_passerelle[:6]))

    # 67. LE SOCLE DE LA PASSERELLE (MO-504 / EO-481) : le createur a demande son
    #     README de dossier, son HEAD (carte d identite + mode d emploi) et son
    #     TEMPLATE de delimiteurs. Le socle est ecrit par la Matrice, en ASCII ; le
    #     canal porte les MOTS DU USER, jamais reecrits -- le head s AJOUTE en tete,
    #     la spec d origine reste dessous. Ce maillon JOUE les jugements sur des
    #     textes fabriques (head reconnu, canal sans head ACCUSE, canal qui a perdu
    #     la spec ACCUSE), MESURE le head en tete du canal reel, les trois pieces
    #     ASCII, et lit par AST la declaration du type `passerelle` au vocabulaire
    #     ferme des cartes d identite.
    print("== 67. le socle de la passerelle (readme, head, template des delimiteurs) ==")
    ecarts_socle = _eprouver_socle_passerelle(zone.parent.parent)
    print("  socle-passerelle: " + ("OK" if not ecarts_socle else "KO"))
    if ecarts_socle:
        for ecart in ecarts_socle:
            print("    [KO] " + ecart)
        ko.append("socle-passerelle: " + "; ".join(ecarts_socle[:6]))
    # 68. L EXTRACTION DES DEMANDES (MO-505 / EO-481) : le createur a demande de LIRE
    #     la passerelle du user, d en faire des ITEMS et de RETIRER du canal ce qui
    #     est servi. Mesure du 2026-09-29, premiere extraction reelle : les mots du
    #     user ont ete archives sous EO-476 -- l item d un AUTRE, cite par le verdict
    #     de DOUBLON POSSIBLE de l entonnoir -- alors que l entonnoir venait
    #     d attribuer EO-482, et ce verdict etait AVALE. Ce maillon JOUE le jugement
    #     de l identifiant sur la SORTIE REELLE qui a trompe la porte, la CHAINE
    #     ENTIERE dans un bac a sable jetable (item journalise sous l id de la PORTE,
    #     mots du user conserves, demande servie retiree, voisine INTACTE, doute DIT),
    #     le refus de retirer une demande sans item, et MESURE le canal vivant : LU,
    #     et rien d ecrit.
    print("== 68. l extraction des demandes de la passerelle (lire, item, retirer) ==")
    ecarts_extraction = _eprouver_extraction_passerelle(zone.parent.parent)
    print("  extraction-passerelle: " + ("OK" if not ecarts_extraction else "KO"))
    if ecarts_extraction:
        for ecart in ecarts_extraction:
            print("    [KO] " + ecart)
        ko.append("extraction-passerelle: " + "; ".join(ecarts_extraction[:6]))

    # 69. COMPOSER EN MERMAID, CONVERTIR EN SVG (MO-493 / EO-449) : le createur a
    #     demande de transformer N IMPORTE QUOI en MERMAID puis en SVG -- pour que
    #     l agent lise le MERMAID et que le createur lise le SVG, et que les
    #     incoherences cachees deviennent VISIBLES. Ce maillon joue la CHAINE
    #     REELLE (source -> mermaid -> svg, et le SVG s OUVRE), le MORDANT du juge
    #     sur des donnees FABRIQUEES, le rendu DETERMINISTE et le CYCLE, le DRAPEAU
    #     declare dans les DEUX listes (piege tombe ce round), et les VUES LIVREES
    #     (ASCII, ouvrables). Aucun compte de la donnee VIVANTE n est fige : exiger
    #     "le parcours reel a N incoherences" rendrait ROUGE le jour ou le createur
    #     les repare (famille R-008, deja payee au maillon 66).
    print("== 69. rendre un graphe : composer en mermaid, convertir en svg ==")
    ecarts_graphe = _eprouver_rendre_graphe(zone.parent.parent)
    print("  rendre-graphe: " + ("OK" if not ecarts_graphe else "KO"))
    if ecarts_graphe:
        for ecart in ecarts_graphe:
            print("    [KO] " + ecart)
        ko.append("rendre-graphe: " + "; ".join(ecarts_graphe[:6]))

    # 70. LA FENETRE D ABSORPTION (MO-494) : la suite a rendu KO sur
    #     `passe-absorbee-sur-le-service : 0 passe(s) sans fait absorbee(s)` alors
    #     que le service etait SAINT (replay direct deux minutes plus tard : VERDICT
    #     OK). La cause : la decision existait dans UN SEUL des deux gardes -- son
    #     voisin juge la MEME propriete et l ignorait. Ce maillon eprouve le
    #     domicile UNIQUE, le COBAYE (etat frais -> epargne), le CONTRE-TEMOIN
    #     (etat ancien -> accuse), le FAIL-CLOSED, et fait tourner les DEUX gardes
    #     sur le service reel.
    print("== 70. la fenetre d absorption (mesurer AVANT d accuser) ==")
    ecarts_recul = _eprouver_recul_absorbee(zone.parent.parent)
    print("  recul-absorbee: " + ("OK" if not ecarts_recul else "KO"))
    if ecarts_recul:
        for ecart in ecarts_recul:
            print("    [KO] " + ecart)
        ko.append("recul-absorbee: " + "; ".join(ecarts_recul[:6]))

    # 71. LE PERIMETRE D ECRITURE VOIT LA RACINE (MO-495) : le walk du garde elaguait
    #     la branche qui mene au perimetre PUIS sautait la boucle des fichiers du
    #     dossier courant -- la RACINE n etait donc JAMAIS jugee (l allowlist racine
    #     etait du CODE MORT), et la branche v1/v2 entiere etait hors de vue. Ce
    #     maillon joue la racine FICTIVE : le cobaye de la racine est ACCUSE, la
    #     branche v1/v2 aussi ; les contre-temoins (demarrage autorise, filet de la
    #     porte, PERIMETRE, cobaye hors fenetre) sont EPARGNES ; la sauvegarde d un
    #     nom interdit est ACCUSEE ; et la declaration de la porte est CONSOMMEE, sans
    #     aucune recopie (M-076).
    print("== 71. le perimetre d ecriture voit la RACINE (mesurer, pas supposer) ==")
    ecarts_perimetre = _eprouver_perimetre_racine(zone.parent.parent)
    print("  perimetre-racine: " + ("OK" if not ecarts_perimetre else "KO"))
    if ecarts_perimetre:
        for ecart in ecarts_perimetre:
            print("    [KO] " + ecart)
        ko.append("perimetre-racine: " + "; ".join(ecarts_perimetre[:6]))

    # 72. LA LOI PRESCRIT DES PORTES JOUABLES PAR CELUI QUI LES JOUE (MO-496) :
    #     ORDRE 4.6 prescrivait `vigie-portes tour --si-due`, porte du flux 1 : le
    #     flux 2 y etait refuse a chaque round, et rien dans la suite ne le voyait. Le
    #     cobaye exige que chaque porte PRESCRITE se laisse lire par le juge REEL du
    #     lanceur sous l identite du flux 2 ; le contre-temoin exige que l ACTE de la
    #     porte de l autre flux reste REFUSE (sinon le controle serait une tautologie).
    print("== 72. la loi prescrit des portes jouables par le flux qui les joue ==")
    ecarts_loi = _eprouver_portes_de_la_loi(zone.parent.parent)
    print("  portes-de-la-loi: " + ("OK" if not ecarts_loi else "KO"))
    if ecarts_loi:
        for ecart in ecarts_loi:
            print("    [KO] " + ecart)
        ko.append("portes-de-la-loi: " + "; ".join(ecarts_loi[:6]))

    # 73. LA BANQUE v1/v2 EST HORS JUGEMENT ASCII, ET ELLE SE DIT (MO-497) : le garde
    #     accusait 72 fichiers non-ASCII de la banque de ressources, qu AUCUN outil ne
    #     peut corriger (les corriger muterait le cerveau v1/v2, interdit). La banque a
    #     maintenant un DOMICILE et le garde la consomme. Le cobaye joue la garde REELLE
    #     sur une arborescence FICTIVE : le non-ASCII du PERIMETRE est accuse, le MEME
    #     contenu hors perimetre est epargne mais COMPTE et NOMME, et le perimetre
    #     reste controle (une zone ne contient pas son contenant).
    print("== 73. la banque v1/v2 est hors jugement, et elle se dit ==")
    ecarts_banque = _eprouver_banque_hors_jugement(zone.parent.parent)
    print("  banque-hors-jugement: " + ("OK" if not ecarts_banque else "KO"))
    if ecarts_banque:
        for ecart in ecarts_banque:
            print("    [KO] " + ecart)
        ko.append("banque-hors-jugement: " + "; ".join(ecarts_banque[:6]))

    # 74. L AGE D UNE MISSION SE MESURE SUR SA TRACE DE SERVICE (MO-501) : l age etait
    #     calcule sur `chargee_le`, qu un LOT ENTIER partage -- une mission servie depuis
    #     2 min se lisait < en cours depuis 2.4 j >, et la suite etait donc ROUGE du
    #     premier au dernier round d un lot arme. Le remede existait dans le fichier
    #     (`charges_tracees`) et ne consommait personne. Cobaye sur une vue FABRIQUE en
    #     memoire, contre-temoin sans trace (qui doit rester accuse), et l horloge mesuree
    #     nommee dans le fait.
    print("== 74. l age d une mission se mesure sur sa trace de service ==")
    ecarts_age = _eprouver_age_sur_trace_de_service(zone.parent.parent)
    print("  age-sur-trace: " + ("OK" if not ecarts_age else "KO"))
    if ecarts_age:
        for ecart in ecarts_age:
            print("    [KO] " + ecart)
        ko.append("age-sur-trace: " + "; ".join(ecarts_age[:6]))

    # 75. LES TROIS CASES EXIGEES SONT PRESENTES ET DANS L ORDRE (EO-475 / MO-506) : le
    #     miroir theme <-> table verifie l ACCORD, pas l EXISTENCE. Retiree des DEUX
    #     cotes, [expertise] rendait un miroir VERT et la chaine passait de 10 a 9
    #     maillons sans un mot. Cobaye sur une liste FABRIQUEE en memoire (le parcours du
    #     createur n est jamais ecrit pour prouver), contre-temoins : parcours reel
    #     epargne, desordre accuse, vide accuse les trois -- et la mission reste la
    #     derniere ligne dans les quatre cas.
    print("== 75. les trois cases exigees sont presentes et ordonnees ==")
    ecarts_cases = _eprouver_les_trois_cases_exigees(zone / "pilote")
    print("  cases-exigees: " + ("OK" if not ecarts_cases else "KO"))
    if ecarts_cases:
        for ecart in ecarts_cases:
            print("    [KO] " + ecart)
        ko.append("cases-exigees: " + "; ".join(ecarts_cases[:6]))


    # 76. LE PROFIL SE SERT EN DERNIER, AU COMPTE-RENDU (EO-480 / MO-507) : la fiche
    #     utilisateur etait remplie et le bloc voyageait, mais comme AJUSTABLE -- donc
    #     invisible par defaut. La donnee arrivait et rien ne disait ce qu on en
    #     faisait. Le profil est desormais servi en DERNIER de apres-mission, rendu par
    #     son MOTIF partage (jamais une copie), et le maillon signale s il s invite
    #     ailleurs -- le createur a dit < on ajustera l injection par la suite >.
    # 77. LES QUATRE PORTES ANTI-HEREDOC TIENNENT (demande createur 2026-09-30).
    #     Quatre dispositifs interdisaient deja le heredoc : la porte EXECUTER, le
    #     garde des commandes documentees, les transports de la porte d ecriture, et
    #     la loi du round. AUCUN maillon ne les jouait -- une porte qu on ne joue pas
    #     est une porte qu on ne sait pas fermer. Ce maillon les JOUE (contre-temoin
    #     sur un document construit pour l occasion), il ne les lit pas.
    # 78. LE JUGEMENT DES CITATIONS A UN SEUL DOMICILE (EO-479 / MO-508).
    #     Trois instruments de la meme maison jugeaient les citations d index, et
    #     les deux jumeaux de protocoles ACCUSAIENT une source du createur de mort
    #     -- un rouge que la porte ECRIRE interdit de reparer. La regle n a pas ete
    #     ajoutee aux jumeaux : elle a ete DEPLACEE dans un domicile unique
    #     (M-076) que les trois consomment, formulation de l exemption comprise.
    # 79. LA LIGNE DU HEAD DIT CE QU ELLE COMPTE (audit createur 2026-09-30).
    #     Trois chiffres sur une seule ligne, et ils ne parlaient pas du meme
    #     livre : `tracees` et `finies` comptaient le journal de suivi, `en
    #     attente` la file du pilote. Aucun n etait faux pris isolement -- c est ce
    #     qui rendait le defaut invisible. Et une mission REPORTEE (EO-190) n
    #     avait AUCUNE colonne : ni terminee, ni a faire, donc absente. Ce maillon
    #     nomme la population de chaque chiffre et tient l invariant
    #     tracees = finies + ouvertes, sur le fichier PUBLIE et sa source.
    print("== 79. la ligne du head dit ce qu elle compte ==")
    ecarts_head = _eprouver_la_ligne_du_head(zone)
    print("  head-coherent: " + ("OK" if not ecarts_head else "KO"))
    if ecarts_head:
        for ecart in ecarts_head:
            print("    [KO] " + ecart)
        ko.append("head-coherent: " + "; ".join(ecarts_head[:6]))

    # 80. LA PORTE DE REOUVERTURE (MO-548 / EO-553) : `fin` clos la mission EN
    #     COURS, le bilan est ecrit, et plus AUCUNE porte ne rend la main (mesure :
    #     la porte `fin` a clos MO-534 avec le bilan de MO-547, et le controle de
    #     coherence ne pouvait pas voir la difference). Le verbe `rouvrir` retire le
    #     bilan fautif sans l effacer. Ce maillon joue la DECISION pure sur huit
    #     cas, la PORTE sur une racine jetable (refus nommes, bilan retire ET
    #     conserve, date, compteur, acte a son action), puis fait trancher le
    #     CONTROLE REEL de coherence -- avec le contre-temoin decisive : sur le
    #     MEME etat, retirer la borne `rouverture` du journal fait REVENIR les
    #     deux ecarts. Eprouve EN MEMOIRE : aucune trace du depot n est touchee.
    print("== 80. la porte de rouverture retire le bilan fautif sans l effacer ==")
    ecarts_rouvrir = _eprouver_rouvrir(zone.parent.parent)
    print("  rouvrir: " + ("OK" if not ecarts_rouvrir else "KO"))
    if ecarts_rouvrir:
        for ecart in ecarts_rouvrir:
            print("    [KO] " + ecart)
        ko.append("rouvrir: " + "; ".join(ecarts_rouvrir[:6]))

    # 81. LES TROIS LISTES DU PARC OUTILS SE COMPARENT (MO-534). Le parc est
    #     decrit trois fois -- le registre (genere), le manuel (des fiches, dont
    #     des fiches de GROUPE) et le readme des outils transverses -- et AUCUNE
    #     ne se comparait : une divergence de documentation restait invisible.
    #     Le maillon joue la decision pure (quatre cas, deux contre-temoins --
    #     dont celui qui prouve que le groupe de fiches fait le travail, sans
    #     quoi 20 modules bien documentes seraient accuses a tort) puis rend la
    #     DONNEE REELLE visible : combien de briques sans mention, et OU.
    print("== 81. les trois listes du parc outils se comparent ==")
    ecarts_doc, faits_doc = _eprouver_doc_des_outils(zone.parent.parent)
    print("  doc-outils: " + ("OK" if not ecarts_doc else "KO"))
    for fait in faits_doc:
        print("    " + fait)
    if ecarts_doc:
        for ecart in ecarts_doc:
            print("    [KO] " + ecart)
        ko.append("doc-outils: " + "; ".join(ecarts_doc[:6]))

    # MAILLON 83 : apres le 81 (le parc se compare), avant le 82.
    print("== 83. une brique servie a l injection et introuvable est accusee ==")
    ecarts_servies, faits_servies = _eprouver_les_briques_servies_introuvables(
        zone.parent.parent)
    print("  servies-introuvables: " + ("OK" if not ecarts_servies else "KO"))
    for fait in faits_servies:
        print("    " + fait)
    if ecarts_servies:
        for ecart in ecarts_servies:
            print("    [KO] " + ecart)
        ko.append("servies-introuvables: " + "; ".join(ecarts_servies[:6]))

    # MAILLON 84 : apres le 83 (une brique servie doit etre joignable), avant
    # le 82. Le parc se compare, les briques se rejoignent, puis on verifie que
    # ses CONDITIONS testent quelque chose.
    print("== 84. une condition toujours vraie dans le parc est accusee ==")
    ecarts_nonsens, faits_nonsens = _eprouver_les_nonsens_bloquants(zone.parent.parent)
    print("  nonsens-bloquants: " + ("OK" if not ecarts_nonsens else "KO"))
    for fait in faits_nonsens:
        print("    " + fait)
    if ecarts_nonsens:
        for ecart in ecarts_nonsens:
            print("    [KO] " + ecart)
        ko.append("nonsens-bloquants: " + "; ".join(ecarts_nonsens[:6]))

    # MAILLON 85 : apres le 84 (les conditions testent quelque chose), avant
    # le 82. La doctrine du depot git (EO-529) n est un texte que si un
    # maillon la fait appliquer : sans ce controle, rien n empoisonne le
    # depot et la convention reste un texte lu par personne.
    print("== 85. le depot git abide de sa convention ==")
    ecarts_depot, faits_depot = _depot_git_contamine(zone.parent.parent)
    print("  depot-git: " + ("OK" if not ecarts_depot else "KO"))
    for fait in faits_depot:
        print("    " + fait)
    if ecarts_depot:
        for ecart in ecarts_depot:
            print("    [KO] " + ecart)
        ko.append("depot-git: " + "; ".join(ecarts_depot[:6]))
    # MAILLON 86 : apres le 85 (le depot abide de sa convention),
    #     avant le 82. LA FILE DE MISSIONS SE SUIT-ELLE ? Mesure du
    #     2026-10-04 : un `git checkout --` a efface cinq fiches et la
    #     non-regression est restee VERTE, parce qu aucun maillon ne
    #     lisait ce fichier. Un fichier que rien ne lit perd ce qu il
    #     contient en silence.
    print("== 86. la file de missions se suit-elle (continuite + compteur) ==")
    ecarts_file, faits_file = _file_de_missions_sans_trou(zone)
    print("  file-missions: " + ("OK" if not ecarts_file else "KO"))
    for fait in faits_file:
        print("    " + fait)
    if ecarts_file:
        for ecart in ecarts_file:
            print("    [KO] " + ecart)
        ko.append("file-missions: " + "; ".join(ecarts_file[:6]))


    # MAILLON 82 : apres le 81 (le parc outils se compare, donc on sait
    # nominate une porte transversale), avant le 78.
    print("== 82. une vue de suivi perimee est accusee avec sa porte ==")
    ecarts_vues = _eprouver_la_fraicheur_des_vues(zone)
    print("  vues-fraiches: " + ("OK" if not ecarts_vues else "KO"))
    for ecart in ecarts_vues:
        print("    [KO] " + ecart)
    if ecarts_vues:
        ko.append("vues-fraiches: " + "; ".join(ecarts_vues[:6]))

    print("== 78. le jugement des citations a un seul domicile ==")
    ecarts_citations = _eprouver_le_jugement_des_citations(zone)
    print("  jugement-unique: " + ("OK" if not ecarts_citations else "KO"))
    if ecarts_citations:
        for ecart in ecarts_citations:
            print("    [KO] " + ecart)
        ko.append("jugement-unique: " + "; ".join(ecarts_citations[:6]))

    print("== 77. les quatre portes anti-heredoc tiennent ==")
    ecarts_heredoc = _eprouver_les_quatre_portes_anti_heredoc(zone)
    print("  portes-heredoc: " + ("OK" if not ecarts_heredoc else "KO"))
    if ecarts_heredoc:
        for ecart in ecarts_heredoc:
            print("    [KO] " + ecart)
        ko.append("portes-heredoc: " + "; ".join(ecarts_heredoc[:6]))

    print("== 76. le profil se sert en dernier, au compte-rendu ==")
    ecarts_profil = _eprouver_profil_en_fin_de_compte_rendu(zone)
    print("  profil-en-fin: " + ("OK" if not ecarts_profil else "KO"))
    if ecarts_profil:
        for ecart in ecarts_profil:
            print("    [KO] " + ecart)
        ko.append("profil-en-fin: " + "; ".join(ecarts_profil[:6]))

    if ko:

        print(f"\nVERDICT KO : {len(ko)} echec(s) :")
        for x in ko:
            print(f"  - {x}")
        return 1
    print("\nVERDICT OK : non-regression verte (zone + flux).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
