#!/usr/bin/env python3
"""verifier-contrats-outils.py -- Garde : les contrats gagnes le 2026-09-19 tiennent encore.

POURQUOI CE GARDE (MO-214 / EO-204, 2026-09-19) : les preuves d'une mission vivaient
dans `tmp-optimus`, que le pilote PURGE a chaque cloture. Les 17 controles de MO-210
(la porte corrige l'ASCII et refuse le reste) et les 29 de MO-211/MO-212 (l'aide de la
porte dit son contrat) ont donc disparu AVEC leur mission : verifie aujourd'hui, pas
surveille demain. Un controle qui meurt a la cloture ne protege rien.

CE QU'IL EXIGE (ce que ces missions ont gagne) :
  1. LA CARTE ASCII A UN SEUL DOMICILE (MO-210) : l'outil de maintenance et la porte
     `ecrire` lisent la MEME carte (identite d'objet) -- une copie recopiee serait deux
     verites, dont l'une corrigerait ce que l'autre ignore.
  2. LA PORTE `ecrire` CORRIGE LES FAUTES FUTILES ET REFUSE LE RESTE (MO-210) : ce que
     la carte connait est corrige ET DIT ; ce qu'elle ignore est REFUSE en NOMMANT le
     caractere et sa ligne -- jamais un fichier non-ASCII qui aurait l'air propre.
  3. L'AIDE DE LA PORTE DIT SON CONTRAT (MO-212) : les douze groupes de garanties de sa
     DESCRIPTION.md sont AUSSI dans l'aide affichee. Deux documents d'un meme contrat ne
     peuvent plus deriver chacun de son cote.
  4. L'ENTONNOIR REPARE LA CATEGORIE COMME LE ROLE (MO-213) : un item classe repare sa
     categorie (validee contre SA liste, TRACEE), une categorie hors liste est refusee en
     NOMMANT la liste, un item au vrac est refuse en NOMMANT le geste, et le role
     declare n'est jamais reecrit en silence.
  5. AUCUNE PORTE MUETTE AU JOURNAL D'USAGES (MO-219) : chaque outil de data/outils pose
     le sac a dos dans sa porte. Sinon son usage est INVISIBLE au journal -- mesure du
     2026-09-19 : 5 outils a 0 ligne sur 10 478, dont le moteur de recherche que sa PROPRE
     vigie appelle -- et toute mesure d'usage les condamne a l'aveugle (donc on archive
     des outils qui marchent). LIMITE ASSUMEE : ce controle lit la SOURCE (le sac a dos
     est pose) ; la preuve que son import SE RESOUT a l'execution reste au cobaye de
     MO-219. `bdd-usages` est exclu par construction (anti-recursion du sac a dos).

  6. UN OUTIL SE LIVRE AVEC SON MODE D EMPLOI (revision createur 2026-09-20, MO-313) :
     le catalogue servait un os.listdir -- des NOMS, __pycache__ et les .bak compris, et
     AUCUN usage -- alors que proto-6 etape 2 PROMET deja "les interfaces fermees des
     outils que la mission va appeler (usage main.py, codes 0/1/2)". Le createur l a dit :
     fournir un outil SANS explication "n est pas productif et genere des actions
     inutiles". Ce controle exige DEUX choses : aucune carte servie n est trouee (toute
     brique dit son usage DANS la brique elle-meme, jamais dans une fiche recopiee) et
     AUCUN dossier de briques n est plus servi en liste nue.

  7. LA PORTE pause-session clore SE PROUVE SUR DES FONCTIONS PURES (EO-412) : la
     regularisation d une pause orpheline ne se couvre plus par un cobaye jetable
     qui meurt a la cloture. La DECISION (diagnostiquer) et la TRACE
     (evenement_regularisation) sont PURES ; ce controle les eprouve -- 5 decisions
     et 1 trace -- SANS toucher au journal reel : une regularisation ACCEPTEE, et
     motif manquant / etat present / rien a regulariser REFUSES chacun par son code.

  8. LA REGLE DE L ALLOWLIST RACINE (MO-411 / MO-452) : le PERIMETRE et la CLE
     ATTESTABLE ont UN domicile (matrice/data/commun/cible.py) ; ce controle les
     eprouve EN MEMOIRE -- il MORD sur un fichier de la RACINE HORS allowlist
     (perimetre REFUSE ET aucune cle inventee) et EPARGNE le fichier allowliste de
     la racine (cle = NOM NU, re-ancre sur la RACINE DU WORKSPACE) comme un fichier
     de la Matrice (cle = forme canonique).

L AUTOTEST LE PIEGE (lecon L-032) : chaque juge est eprouve sur une donnee SAINE (qui
doit passer) ET sur une donnee CASSEE (qui doit crier) -- voir `--autotest`. Un
detecteur jamais vu crier ne prouve rien.

CE QU'IL NE FAIT PAS : lecture seule. Il lit des fichiers et lance, en SOUS-PROCESSUS
ISOLES, les fonctions pures des outils -- aucun item cree, aucune mission, aucune
ecriture. L'isolement n'est pas un confort : DEUX outils ont chacun un module
`constants`, et les charger ensemble les ferait collisionner (mesure MO-213).

Usage: python verifier-contrats-outils.py [--racine <path>] [--autotest]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = zone introuvable.
"""

import argparse
import importlib.util
import json
import subprocess

import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-414, vague 5 du lot) -----------------
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


def popen_enfant(*arguments, **options):
    """Le lancement DETACHE de cet outil : jamais de fenetre."""
    return subprocess.Popen(*arguments, **options, **drapeaux_popen())
import sys
from pathlib import Path

# Les temoins du contrat de la porte `ecrire` : douze groupes, cherches dans les DEUX
# documents (l'aide affichee ET la DESCRIPTION.md). Meme liste que le cobaye de MO-212,
# qui meurt a la cloture de sa mission -- ici elle est PERMANENTE.
GROUPES_CONTRAT = (
    ("ATOMIQUE", ("os.replace",)),
    ("LF FORCES", ("lf forces", "l-001", "mo-173")),
    ("REVERSIBLE", (".bak",)),
    ("PROUVE", ("sha-256",)),
    ("VALIDE AVANT PUBLICATION", ("py_compile", "json.load", "eo-129")),
    ("PERIMETRE RESOLU", ("allowlist", "mo-183")),
    ("OCCURRENCE UNIQUE", ("occurrence",)),
    ("MODE FERME ET OPTION SANS VALEUR", ("creer|remplacer|ajouter", "eo-156")),
    ("TRANSPORT SUR", ("@fichier", "--contenu-base64")),
    ("GARDE D ORDRE", ("importerror", "eo-159")),
    ("ASCII CORRIGE PUIS REFUSE", ("carte_ascii.py", "mo-210")),
    ("CODES DE SORTIE", ("code 1", "code 2")),
)

# Une faute futile (accents) et ce que la doctrine en fait ; un caractere HORS carte,
# que personne ne doit deviner.
TEXTE_FUTILE = "Le caf\u00e9 est pr\u00eat\n"
TEXTE_FUTILE_ATTENDU = "Le cafe est pret\n"
TEXTE_HORS_CARTE = "Temperature : 20\u00b0C\n"
CODE_POINT = "U+00B0"

RESULTATS = []


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def trouver_zone(racine):
    """Retourne le dossier _operateur/optimus-prime/, ou None."""
    candidats = [racine,
                 racine / "cerveau-projet" / "matrix" / "_operateur" / "optimus-prime",
                 racine / "_operateur" / "optimus-prime"]
    for candidat in candidats:
        if (candidat / "pilote" / "entonnoir" / "listes.py").is_file():
            return candidat
    return None


def dans_un_sous_processus(code):
    """Lance un fragment Python ISOLE et rend l'objet JSON qu'il imprime (None si echec)."""
    r = lancer_enfant([sys.executable, "-c", code], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        return None
    for ligne in reversed(r.stdout.strip().splitlines()):
        try:
            return json.loads(ligne)
        except ValueError:
            continue
    return None


def relever_carte(matrice):
    """Les deux consommateurs lisent-ils la MEME carte ? (un seul sous-processus)."""
    code = (
        "import json, sys\n"
        "sys.path.insert(0, " + ascii(str(matrice / "data" / "commun")) + ")\n"
        "sys.path.insert(0, " + ascii(str(matrice / "data" / "outils" / "corriger-ascii")) + ")\n"
        "import carte_ascii\n"
        "import constants as const_ascii\n"
        "import commun as comm_ascii\n"
        "print(json.dumps({'carte': const_ascii.CARTE_CONVERSION is carte_ascii.CARTE_CONVERSION,\n"
        "  'fonction': comm_ascii.convertir_texte is carte_ascii.convertir_texte,\n"
        "  'convertit': carte_ascii.convertir_texte(" + ascii(TEXTE_FUTILE) + ")[0]}))\n")
    return dans_un_sous_processus(code)


def relever_porte(matrice):
    """La porte corrige-t-elle les futiles, et refuse-t-elle le reste ? (sous-processus)."""
    code = (
        "import contextlib, io, json, sys\n"
        "sys.path.insert(0, " + ascii(str(matrice / "data" / "outils" / "ecrire")) + ")\n"
        "import commun\n"
        "tampon = io.StringIO()\n"
        "with contextlib.redirect_stdout(tampon):\n"
        "    texte, refus = commun.corriger_contenu(" + ascii(TEXTE_FUTILE) + ")\n"
        "journal_futile = tampon.getvalue()\n"
        "tampon2 = io.StringIO()\n"
        "with contextlib.redirect_stdout(tampon2):\n"
        "    texte2, refus2 = commun.corriger_contenu(" + ascii(TEXTE_HORS_CARTE) + ")\n"
        "print(json.dumps({'futile': texte, 'futile_journal': journal_futile,\n"
        "  'futile_refus': refus, 'hors': texte2, 'hors_refus': refus2}))\n")
    return dans_un_sous_processus(code)


def relever_aide(matrice):
    """L'aide affichee par la porte, et le contrat ecrit a cote (lecture seule)."""
    porte = matrice / "data" / "outils" / "ecrire"
    r = lancer_enfant([sys.executable, str(porte / "main.py")], capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    contrat = porte / "DESCRIPTION.md"
    return {"aide": r.stdout,
            "contrat": contrat.read_text(encoding="utf-8") if contrat.is_file() else ""}


def relever_clore(matrice):
    """La porte clore : decision PURE + trace PURE, eprouvees SANS disque.

    Importe clore.fonctions dans un sous-processus ISOLE (comme les autres
    releves) et appelle les fonctions PURES sur des cas synthetiques : aucune
    ecriture, aucun journal reel touche. C est ce qui rend la regularisation
    couverte par un controle PERMANENT, jamais par un cobaye jetable.
    """
    outil = matrice / "data" / "outils" / "pause-session"
    code = (
        "import importlib, json, sys\n"
        "sys.path.insert(0, " + ascii(str(outil)) + ")\n"
        "m = importlib.import_module('clore.fonctions')\n"
        "pause = {'type': 'pause', 'mission': 'MO-X'}\n"
        "reprise = {'type': 'reprise', 'mission': 'MO-X'}\n"
        "cas = {}\n"
        "cas['ok'] = list(m.diagnostiquer('motif', False, pause))\n"
        "cas['motif'] = list(m.diagnostiquer('', False, pause))\n"
        "cas['etat'] = list(m.diagnostiquer('motif', True, pause))\n"
        "cas['rien'] = list(m.diagnostiquer('motif', False, reprise))\n"
        "cas['vide'] = list(m.diagnostiquer('motif', False, None))\n"
        "type_ev, details = m.evenement_regularisation('MO-X', 'm')\n"
        "cas['trace'] = [type_ev, details]\n"
        "print(json.dumps(cas))\n")
    return dans_un_sous_processus(code)


def relever_categorie(zone):
    """L'entonnoir repare-t-il la categorie ? (fonction pure, sous-processus isole)."""
    entonnoir = zone / "pilote" / "entonnoir"
    code = (
        "import importlib, json, sys\n"
        "sys.path.insert(0, " + ascii(str(entonnoir)) + ")\n"
        "sys.path.insert(0, " + ascii(str(zone / "pilote")) + ")\n"
        "m = importlib.import_module('retiqueter.fonctions')\n"
        "base = {'id': 'EO-000', 'categorie': 'pilote', 'role': 'ROUTINE'}\n"
        "mission = dict(base)\n"
        "c_repare, _m1 = m.reparer_categorie(mission, 'dev', 'EO-000', 'routine')\n"
        "hors = dict(base)\n"
        "c_hors, msg_hors = m.reparer_categorie(hors, 'dev', 'EO-000', 'hors-liste')\n"
        "vrac = dict(base)\n"
        "c_vrac, msg_vrac = m.reparer_categorie(vrac, '', 'EO-000', 'routine')\n"
        "print(json.dumps({'repare': [c_repare, mission.get('categorie'),\n"
        "  mission.get('categorie_avant'), mission.get('role')],\n"
        "  'hors': [c_hors, msg_hors], 'vrac': [c_vrac, msg_vrac]}))\n")
    return dans_un_sous_processus(code)


# --- Les juges : ils ne lisent que le RELEVE, donc ils sont eprouvables a vide -----

def juger_carte(ev):
    if not ev:
        return False, "releve impossible (sous-processus en echec : l'outil ne s'importe plus)"
    if not ev.get("carte"):
        return False, "l'outil de maintenance lit une AUTRE carte que le domicile"
    if not ev.get("fonction"):
        return False, "convertir_texte de l'outil n'est pas celui du domicile"
    if ev.get("convertit") != TEXTE_FUTILE_ATTENDU:
        return False, "le domicile ne corrige plus : " + repr(ev.get("convertit"))
    return True, "une seule carte, deux consommateurs"


def juger_porte(ev):
    if not ev:
        return False, "releve impossible (sous-processus en echec : la porte ne s'importe plus)"
    if ev.get("futile") != TEXTE_FUTILE_ATTENDU:
        return False, "la faute futile n'est plus corrigee : " + repr(ev.get("futile"))
    if "CORRIGE" not in ev.get("futile_journal", ""):
        return False, "la correction n'est pas DITE (aucun CORRIGE au journal)"
    if ev.get("futile_refus"):
        return False, "une faute FUTILE a ete refusee au lieu d'etre corrigee"
    if not ev.get("hors_refus"):
        return False, "le hors-carte n'est plus refuse : un fichier non-ASCII passerait"
    if CODE_POINT not in ev["hors_refus"]:
        return False, "le refus ne NOMME pas le caractere (attendu " + CODE_POINT + ")"
    if "carte_ascii.py" not in ev["hors_refus"]:
        return False, "le refus ne NOMME pas le remede (le domicile de la carte)"
    return True, "corrige et DIT, refuse et NOMME le caractere"


def juger_aide(ev):
    if not ev:
        return False, "releve impossible"
    aide, contrat = ev.get("aide", ""), ev.get("contrat", "")
    if not aide.strip():
        return False, "l'aide de la porte ne s'affiche pas (le contrat n'est plus lisible)"
    if not contrat.strip():
        return False, "DESCRIPTION.md est absent : le contrat n'existe plus"
    absents_aide = [nom for nom, temoins in GROUPES_CONTRAT
                    if any(t not in aide.lower() for t in temoins)]
    absents_contrat = [nom for nom, temoins in GROUPES_CONTRAT
                       if any(t not in contrat.lower() for t in temoins)]
    if absents_aide:
        return False, "garanties absentes de l'AIDE : " + ", ".join(absents_aide)
    if absents_contrat:
        return False, "garanties absentes du CONTRAT : " + ", ".join(absents_contrat)
    return True, str(len(GROUPES_CONTRAT)) + " groupes dans les DEUX documents"


def juger_clore(ev):
    """La regularisation est decidee et tracee par des fonctions PURES conformes."""
    if not ev:
        return False, "releve impossible (sous-processus en echec : clore ne s'importe plus)"
    attendus = {
        "ok": [0, "regularisation"],
        "motif": [2, "motif-manquant"],
        "etat": [1, "etat-present"],
        "rien": [1, "rien-a-regulariser"],
        "vide": [1, "rien-a-regulariser"],
    }
    for nom, attendu in attendus.items():
        if ev.get(nom) != attendu:
            return False, ("decision " + nom + " : attendu " + repr(attendu)
                           + ", mesure " + repr(ev.get(nom)))
    if ev.get("trace") != ["reprise", {"mission": "MO-X", "regularisation": "m"}]:
        return False, "trace de regularisation non conforme : " + repr(ev.get("trace"))
    return True, "5 decisions + trace de regularisation, toutes conformes"


def juger_categorie(ev):
    if not ev:
        return False, "releve impossible (sous-processus en echec : l'entonnoir ne s'importe plus)"
    repare = ev.get("repare") or []
    if len(repare) != 4:
        return False, "releve de la reparation incomplet"
    if repare[0] != 0:
        return False, "une categorie VALIDE est refusee (code " + str(repare[0]) + ")"
    if repare[1] != "routine":
        return False, "la categorie n'a pas ete posee : " + repr(repare[1])
    if repare[2] != "pilote":
        return False, "l'ancienne categorie n'est plus TRACEE : " + repr(repare[2])
    if repare[3] != "ROUTINE":
        return False, "le ROLE a ete reecrit en silence : " + repr(repare[3])
    hors = ev.get("hors") or [0, ""]
    if hors[0] != 2:
        return False, "une categorie HORS liste est acceptee (code " + str(hors[0]) + ")"
    if "categories fermees de dev" not in str(hors[1]).lower():
        return False, "le refus ne NOMME pas la liste du type"
    vrac = ev.get("vrac") or [0, ""]
    if vrac[0] != 2:
        return False, "la categorie d'un item AU VRAC est acceptee (code " + str(vrac[0]) + ")"
    if "classer --id" not in str(vrac[1]):
        return False, "le refus ne NOMME pas le geste (classer d'abord)"
    return True, "reparation tracee, refus directionnels"


# --- 5. AUCUNE PORTE MUETTE -------------------------------------------------------

# L'outil exclu par construction : le sac a dos ne se note pas lui-meme (anti-recursion).
OUTILS_EXCLUS = ("bdd-usages",)


def relever_muet(matrice):
    """Chaque porte de data/outils pose-t-elle le sac a dos (donc SE NOTE-t-elle) ?"""
    racine_outils = matrice / "data" / "outils"
    outils = {}
    if racine_outils.is_dir():
        for porte in sorted(racine_outils.iterdir()):
            if not porte.is_dir() or porte.name.startswith("__"):
                continue
            main = porte / "main.py"
            if not main.is_file():
                continue
            source = main.read_text(encoding="utf-8", errors="replace")
            outils[porte.name] = "envelopper(principal" in source
    return {"outils": outils}


def juger_muet(ev):
    """Toute porte se NOTE-t-elle ? Une porte muette rend son usage INVISIBLE."""
    outils = ev.get("outils") or {}
    attendues = {nom: pose for nom, pose in outils.items() if nom not in OUTILS_EXCLUS}
    if not attendues:
        return False, "aucune porte lue sous data/outils"
    muettes = sorted(nom for nom, pose in attendues.items() if not pose)
    if muettes:
        return False, ("portes MUETTES (usage invisible, mesure aveugle) : " + ", ".join(muettes)
                       + " -- pose le sac a dos comme lire/ecrire/lister :"
                       " from sac_a_dos import envelopper ;"
                       " sys.exit(envelopper(principal, sys.argv[1:]))")
    return True, str(len(attendues)) + " portes notent leur usage (bdd-usages exclu : anti-recursion)"




def relever_modes_emploi(zone):
    """Ce que le pilote SERT comme mode d emploi, et ce qu il sert encore en liste nue.

    Deux mesures dans UN seul releve : les CARTES servies par l extracteur (avec les
    briques qu elles laissent MUETTES) et le CATALOGUE d injection -- une entree
    `dossier` dont la source est un dossier de BRIQUES est l ecart que cette revision
    ferme (c est ce que l agent recevait : des noms, et rien d autre).
    """
    pilote = zone / "pilote"
    chemin_extracteur = pilote / "injection" / "modes_emploi.py"
    chemin_catalogue = pilote / "injection" / "config.json"
    releve = {"extracteur": chemin_extracteur.is_file(), "declarees": [],
              "listes_nues": [], "manquantes": {}, "sans_usage": {},
              "plancher_absent": {}, "plancher_non_servi": {},
              "briques": 0, "silencieuses": []}
    if not releve["extracteur"]:
        return releve
    specification = importlib.util.spec_from_file_location(
        "modes_emploi_garde", str(chemin_extracteur))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    for cle in sorted(module.RACINES):
        racine = (module.PILOTE / module.RACINES[cle]).resolve()
        texte, absentes = module.carte(racine)
        briques = module.lister_briques(racine)
        releve["briques"] += len(briques)
        if absentes:
            releve["manquantes"][cle] = absentes
        # LE BUT SANS L USAGE EST UN TROU (mesure du 2026-09-25) : un mode d emploi qui
        # dit a quoi sert la brique mais PAS comment l appeler laisse l agent devant une
        # porte fermee. Le cas mesure : 7 portes de la Matrice (dont bdd-conservation)
        # servaient leur but et rien d autre, et AUCUN garde ne le disait -- le
        # recensement ne comptait que les briques ENTIEREMENT vides (`manquantes`).
        sans_usage = [brique.name for brique in briques
                      if module.extrait(brique)[0].strip()
                      and not module.extrait(brique)[1].strip()]
        if sans_usage:
            releve["sans_usage"][cle] = sorted(sans_usage)
        # LE PLANCHER (2026-09-25) : une carte ne cache JAMAIS ses essentielles -- et un
        # nom de plancher qui ne nomme RIEN (faute de frappe) est une PROTECTION
        # FANTOME : elle se lit comme une garantie et ne protege personne.
        noms_presents = {brique.name for brique in briques}
        plancher = module.plancher_de(racine)
        absents = [nom for nom in plancher if nom not in noms_presents]
        if absents:
            releve["plancher_absent"][cle] = absents
        non_servis = [nom for nom in plancher
                      if nom in noms_presents and nom + " :" not in texte]
        if non_servis:
            releve["plancher_non_servi"][cle] = non_servis
        # LA COUPE DOIT SE DIRE (MO-314) : une carte qui depasse le plafond declare et ne
        # le dit pas se lit comme une carte complete -- la MEME faute que le plafond
        # existe pour empecher, deplacee de la donnee vers la lecture.
        if len(briques) > module.PLAFOND_BRIQUES_CARTE and "NON AFFICHEE" not in texte:
            releve["silencieuses"].append(cle)
    if not chemin_catalogue.is_file():
        return releve
    try:
        donnees = json.loads(chemin_catalogue.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return releve
    entrees = [entree for phase in (donnees.get("injections") or {}).values()
               for entree in phase]
    releve["declarees"] = sorted(str(e.get("id", "?")) for e in entrees
                                 if e.get("type") == "modes-emploi")
    for entree in entrees:
        if entree.get("type") != "dossier":
            continue
        source = (pilote / str(entree.get("source", ""))).resolve()
        if source.is_dir() and module.lister_briques(source):
            releve["listes_nues"].append(str(entree.get("id", "?")))
    releve["listes_nues"] = sorted(releve["listes_nues"])
    releve.update(relever_outils_prepares(pilote, module))
    return releve


def relever_outils_prepares(pilote, module):
    """Les LISTES D OUTILS PREPAREES (EO-313) portees par les missions, et leurs ecarts.

    Cote MISSION de la meme promesse que les cartes (cote ITEM : la porte `preparer`
    valide a la pose). Sans ce releve, une liste ecrite A LA MAIN dans le fichier des
    missions -- ou preparee AVANT que le plafond change -- passerait sans temoin, et
    l injection servirait en silence une partie de ce qui a ete declare.

    DEUX ECARTS, ceux qui font mal : un nom que l injection ne SAIT PAS servir, et une
    liste plus longue que le PLAFOND d outils joints.
    """
    chemin_file = pilote / "file-missions-optimus.json"
    chemin_constantes = pilote / "constants.py"
    releve = {"missions": 0, "preparees": 0, "inservables": [], "hors_plafond": [],
              "plafond": 0}
    plafond = 0
    if chemin_constantes.is_file():
        specification = importlib.util.spec_from_file_location("constants_garde",
                                                               str(chemin_constantes))
        constantes = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(constantes)
        plafond = int(getattr(constantes, "PLAFOND_OUTILS_MODE_EMPLOI", 0) or 0)
    releve["plafond"] = plafond
    if not chemin_file.is_file():
        return releve
    try:
        donnees = json.loads(chemin_file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return releve
    for mission in donnees.get("missions", []):
        releve["missions"] += 1
        outils = [str(nom) for nom in (mission.get("outils") or []) if str(nom).strip()]
        if not outils:
            continue
        releve["preparees"] += 1
        for nom in outils:
            if module.trouver_brique(nom) is None:
                releve["inservables"].append(str(mission.get("id", "?")) + ":" + nom)
        if plafond and len(outils) > plafond:
            releve["hors_plafond"].append(str(mission.get("id", "?")) + " ("
                                          + str(len(outils)) + "/" + str(plafond) + ")")
    return releve


def juger_modes_emploi(ev):
    """Un outil se livre AVEC son mode d emploi : jamais des noms, jamais un trou tu."""
    if not ev.get("extracteur"):
        return False, "extracteur de modes d emploi ABSENT : le pilote ne peut plus servir un usage"
    if not ev.get("declarees"):
        return False, "aucune entree `modes-emploi` au catalogue : l agent ne recoit que des NOMS"
    if ev.get("listes_nues"):
        return False, ("dossier(s) de briques servi(s) en LISTE DE NOMS (aucun usage) : "
                       + ", ".join(ev["listes_nues"])
                       + " -- servir une entree `modes-emploi` a la place")
    if ev.get("silencieuses"):
        return False, ("carte(s) COUPEE(S) EN SILENCE (plafond atteint, rien de dit) : "
                       + ", ".join(ev["silencieuses"])
                       + " -- dire les briques non affichees ET le geste qui les rend")
    if not ev.get("briques"):
        return False, ("AUCUNE brique lue sous les racines declarees : une carte vide ne prouve"
                       " rien (racines du domicile a reparer, ou arbre incomplet)")
    if ev.get("inservables"):
        return False, ("mission(s) qui DECLARENT un outil NON SERVABLE : "
                       + ", ".join(ev["inservables"])
                       + " -- la liste se prepare a SA porte (preparer) : un nom accepte"
                       " a la pose est un nom que l injection sait servir")
    if ev.get("hors_plafond"):
        return False, ("mission(s) au-dela du PLAFOND d outils joints ("
                       + str(ev.get("plafond", "?")) + ") : " + ", ".join(ev["hors_plafond"])
                       + " -- l injection n en servirait qu une PARTIE : la liste se borne"
                       " a la PREPARATION, pas a l injection")
    plancher_absent = ev.get("plancher_absent") or {}
    if plancher_absent:
        detail = " ; ".join(cle + " -> " + ", ".join(noms)
                            for cle, noms in sorted(plancher_absent.items()))
        return False, ("plancher DECLARE qui ne nomme RIEN sous sa racine (protection"
                       " fantome) : " + detail + " -- corriger le nom au domicile de"
                       " l extracteur (une faute de frappe ne protege personne)")
    plancher_non_servi = ev.get("plancher_non_servi") or {}
    if plancher_non_servi:
        detail = " ; ".join(cle + " -> " + ", ".join(noms)
                            for cle, noms in sorted(plancher_non_servi.items()))
        return False, ("essentielle(s) du PLANCHER non SERVIE(S) : la carte les a coupees"
                       " malgre la declaration (le plancher se place EN TETE, le plafond"
                       " coupe par la fin) : " + detail)
    sans_usage = ev.get("sans_usage") or {}
    if sans_usage:
        detail = " ; ".join(cle + " -> " + ", ".join(noms)
                            for cle, noms in sorted(sans_usage.items()))
        return False, ("brique(s) au BUT SEUL, sans USAGE : le mode d emploi ne dit pas"
                       " COMMENT l appeler (poser un bloc `Usage :` DANS le docstring de"
                       " la brique, son domicile) : " + detail)
    manquantes = ev.get("manquantes") or {}
    if manquantes:
        detail = " ; ".join(cle + " -> " + ", ".join(noms)
                            for cle, noms in sorted(manquantes.items()))
        return False, ("brique(s) SANS mode d emploi (le poser DANS la brique, son domicile) : "
                       + detail)
    return True, (str(len(ev["declarees"])) + " carte(s) servie(s), "
                  + str(ev.get("preparees", 0)) + " liste(s) d outils preparee(s) sur "
                  + str(ev.get("missions", 0)) + " mission(s), aucune brique muette"
                  " ni non servable")


# --- GARDE DES LANCEMENTS A NU (EO-428 / MO-413) --------------------------
# Mesure du 2026-09-25 : 163 sites de lancement dans tout le Python de la Matrice,
# 139 A NU, dont 8 atteints par un processus de fond (le serveur et les boucles).
# Le createur a tranche : traiter d abord la classe a RISQUE (les boucles de fond),
# puis vider le reste par lots. Ce controle MORD sur tout lancement a nu DANS les
# boucles et MESURE le residu hors boucles SANS le juger : un controle qui crie en
# permanence cesse de garder (mesure d audit consignee dans
# _operateur/optimus-prime/audits/audit-lancements-a-nu.md).
APPELS_PROCESSUS = ("subprocess.run(", "subprocess.Popen(", "subprocess.call(",
                    "subprocess.check_output(", "subprocess.check_call(",
                    "subprocess.getoutput(", "os.system(", "os.popen(",
                    # Les VERBES du domicile comptent AUSSI : un appel qui passe par eux
                    # EST un lancement. Sans eux, le compte deviendrait aveugle au fur et
                    # a mesure que le lot avance (mesure du 2026-09-25 : le balayage avait
                    # remplace les deux premiers litteraux par le nom du verbe).
                    "lancer_enfant(", "popen_enfant(")
MARQUES_INVISIBLES = ("creationflags", "CREATE_NO_WINDOW", "CREATE_NEW_PROCESS_GROUP",
                      "startupinfo", "SW_HIDE", "drapeaux_invisibles",
                      "drapeaux_popen", "lancer_invisible", "lancement")
# Un appel LONG (liste d arguments sur 16 lignes) sort de la fenetre de 12 lignes :
# mesure du 2026-09-25 sur suivi-sync/commun.py, ou le splat tombait au-dela.
FENETRE_LANCEMENT = 30


def _sites_de_lancement(fichiers, racine):
    """(sites vus, sites A NU) d une liste de .py -- en fichier:ligne, jamais devine."""
    vus, a_nu = [], []
    for chemin in fichiers:
        if chemin.name == "lancement.py":
            continue  # le domicile lui-meme : c est LUI qui porte les drapeaux
        try:
            lignes = chemin.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        relatif = chemin.relative_to(racine).as_posix()
        for indice, ligne in enumerate(lignes):
            if not any(appel in ligne for appel in APPELS_PROCESSUS):
                continue
            fenetre = "\n".join(lignes[indice:indice + FENETRE_LANCEMENT])
            emplacement = relatif + ":" + str(indice + 1)
            vus.append(emplacement)
            if not any(marque in fenetre for marque in MARQUES_INVISIBLES):
                a_nu.append(emplacement)
    return vus, a_nu


def relever_lancements_a_nu(matrice):
    """Les boucles de fond lancent-elles SANS aucune fenetre ? Et quel residu ailleurs ?"""
    toutes = [chemin for chemin in sorted(matrice.rglob("*.py"))
              if "__pycache__" not in chemin.parts]
    boucles = [chemin for chemin in toutes if "routines" in chemin.parts]
    hors = [chemin for chemin in toutes if "routines" not in chemin.parts]
    vus_boucles, a_nu_boucles = _sites_de_lancement(boucles, matrice)
    vus_hors, a_nu_hors = _sites_de_lancement(hors, matrice)
    return {"boucles": len(vus_boucles), "a_nu": a_nu_boucles,
            "hors": len(a_nu_hors), "vus_hors": len(vus_hors)}


def juger_lancements_a_nu(ev):
    """Vert seulement si AUCUN lancement a nu dans les boucles ET si le scan a VU."""
    if not ev.get("boucles"):
        return False, ("scan creux : aucun site de lancement vu dans les boucles -- "
                       "un releve qui ne voit rien ne prouve rien (L-100)")
    if ev.get("a_nu"):
        return False, ("lancement a nu dans les boucles : " + ", ".join(ev["a_nu"][:6])
                       + " -- le fils doit passer par lancement.drapeaux_popen()")
    return True, (str(ev["boucles"]) + " site(s) de lancement dans les boucles, tous couverts"
                  + " | residu hors boucles MESURE : " + str(ev.get("hors", 0))
                  + " a nu sur " + str(ev.get("vus_hors", 0)) + " site(s), a vider par lots")


# --- GARDE DU CYCLE DE VIE : UNE CADENCE NE NOMME JAMAIS UN PID MORT (EO-428) ---
# Mesure du 2026-09-25 : apres un arret cooperatif, le .pid disparaissait mais la
# cadence continuait de nommer un pid mort (18192, 4764, 13940, 6424). Le remede
# vit chez le serveur (nettoyer_cadences_mortes). Ce controle le JOUE sur un
# dossier JETABLE : il MORD si le pid mort reste, si l intervalle declare se perd,
# si un pid VIVANT est efface, et si le nettoyage n est plus cable au cycle de vie.

def relever_cadences_mortes(matrice):
    """Le nettoyage des cadences est-il CABLE et fait-il son travail ? (cobaye isole)."""
    code = (
        "import json, os, sys, tempfile\n"
        "from pathlib import Path\n"
        "sys.path.insert(0, " + ascii(str(matrice / "routines" / "vie")) + ")\n"
        "import server_matrice as module\n"
        "resultat = {}\n"
        "with tempfile.TemporaryDirectory() as tmp:\n"
        "    dossier = Path(tmp)\n"
        "    morte = dossier / 'cobaye-cadence.json'\n"
        "    morte.write_text(json.dumps({'type': 'demarrage', 'intervalle': 42,\n"
        "        'pid': 999999}), encoding='utf-8')\n"
        "    vivante = dossier / 'cobaye2-cadence.json'\n"
        "    vivante.write_text(json.dumps({'type': 'demarrage', 'intervalle': 42,\n"
        "        'pid': os.getpid()}), encoding='utf-8')\n"
        "    module.BOUCLES = [('cobaye', dossier)]\n"
        "    resultat['messages'] = module.nettoyer_cadences_mortes()\n"
        "    resultat['morte'] = json.loads(morte.read_text(encoding='utf-8'))\n"
        "    resultat['vivante'] = json.loads(vivante.read_text(encoding='utf-8'))\n"
        "print(json.dumps(resultat))\n"
    )
    releve = dans_un_sous_processus(code) or {}
    try:
        source = (matrice / "routines" / "vie" / "server_matrice.py")
        texte = source.read_text(encoding="utf-8", errors="replace")
    except OSError:
        texte = ""
    releve["appels"] = texte.count("nettoyer_cadences_mortes")
    return releve


def juger_cadences_mortes(ev):
    """Vert si la cadence MORTE est nettoyee, la VIVANTE intacte et le cablage present."""
    morte, vivante = ev.get("morte") or {}, ev.get("vivante") or {}
    if not morte or not vivante:
        return False, "cobaye impossible : le nettoyage des cadences n a pas pu etre joue"
    if morte.get("pid") is not None or morte.get("type") != "arret":
        return False, ("la cadence d une boucle MORTE nomme encore un pid ("
                       + str(morte.get("pid")) + ") : le pid mort n est pas retire")
    if morte.get("intervalle") != 42:
        return False, "le nettoyage a perdu l intervalle declare de la cadence"
    if vivante.get("pid") is None:
        return False, "la cadence d une boucle VIVANTE a ete effacee -- un pid vivant est intouchable"
    if ev.get("appels", 0) < 3:
        return False, ("le nettoyage n est pas cable au cycle de vie (" + str(ev.get("appels", 0))
                       + " mention(s) -- attendu : definition + demarrage + arret)")
    return True, ("cadence morte nettoyee (pid mort retire, intervalle garde), cadence vivante"
                  " intacte, nettoyage cable en " + str(ev["appels"]) + " points")


NOM_FICHIER_RACINE_HORS_ALLOWLIST = "AGENTS-historique.md"


def relever_perimetre(matrice):
    """Le PERIMETRE et la CLE ATTESTABLE : la regle de cible.py, eprouvee EN MEMOIRE.

    Domicile : `matrice/data/commun/cible.py` (M-076). On interroge les MEMES fonctions
    que la porte ECRIRE et la BDD, sur TROIS temoins REELS (aucun disque touche) : un
    fichier ALLOWLISTE de la racine du workspace (demarrer-optimus-prime.md), un fichier
    de la racine HORS allowlist (AGENTS-historique.md), et un fichier de la Matrice
    (cible.py lui-meme). Un releve IMPOSSIBLE rend {} et se DIT au juge (L-055).
    """
    try:
        import cible
        racine = Path(cible.detecter_racine(str(matrice)))   # la racine du WORKSPACE
    except Exception:  # noqa: BLE001 -- un releve impossible se DIT, il ne crashe pas
        return {}
    allowliste = racine / "demarrer-optimus-prime.md"
    hors = racine / NOM_FICHIER_RACINE_HORS_ALLOWLIST
    dedans = matrice / "data" / "commun" / "cible.py"
    cle_allowliste = cible.cle_attestable(str(allowliste))
    return {
        "racine": str(racine),
        "allowliste_existe": allowliste.is_file(),
        "hors_existe": hors.is_file(),
        "dedans_existe": dedans.is_file(),
        "allowliste_perimetre": cible.est_dans_perimetre(str(allowliste)),
        "allowliste_cle": cle_allowliste,
        "allowliste_chemin": (str(cible.chemin_de_cle(cle_allowliste))
                              if cle_allowliste else ""),
        "hors_perimetre": cible.est_dans_perimetre(str(hors)),
        "hors_cle": cible.cle_attestable(str(hors)),
        "dedans_perimetre": cible.est_dans_perimetre(str(dedans)),
        "dedans_cle": cible.cle_attestable(str(dedans)),
    }


def juger_perimetre(ev):
    """Vert seulement si le hors-allowlist est REFUSE et les deux autres EPARGNES."""
    if not ev:
        return False, ("releve impossible : la regle du perimetre ne s importe plus"
                       " (cible.py)")
    if not (ev.get("allowliste_existe") and ev.get("hors_existe") and ev.get("dedans_existe")):
        return False, ("cobaye incomplet : un fichier temoin est ABSENT (allowliste de la"
                       " racine, fichier hors allowlist, ou fichier de la Matrice)")
    if ev.get("hors_perimetre"):
        return False, ("MORDANT : un fichier de la RACINE HORS ALLOWLIST est accepte dans le"
                       " perimetre -- une porte l ecrirait et la BDD l attesterait")
    if ev.get("hors_cle") is not None:
        return False, ("MORDANT : une cle attestable est INVENTEE pour un fichier HORS"
                       " perimetre : " + repr(ev.get("hors_cle")))
    if not ev.get("allowliste_perimetre"):
        return False, "EPARGNE : le fichier ALLOWLISTE de la racine du workspace est REFUSE"
    if ev.get("allowliste_cle") != "demarrer-optimus-prime.md":
        return False, ("EPARGNE : la cle de l allowlist n est plus le NOM NU : "
                       + repr(ev.get("allowliste_cle")))
    try:
        chemin = Path(str(ev.get("allowliste_chemin", "")))
        attendu = Path(str(ev.get("racine", ""))) / "demarrer-optimus-prime.md"
    except (TypeError, ValueError):
        return False, "releve illisible : chemin de l allowlist non conforme"
    if chemin != attendu:
        return False, ("EPARGNE : chemin_de_cle ne RE-ANCRE pas l allowlist sur la RACINE DU"
                       " WORKSPACE (mesure " + repr(str(chemin)) + ", attendu "
                       + repr(str(attendu)) + ")")
    if not ev.get("dedans_perimetre"):
        return False, "EPARGNE : un fichier de la MATRICE est refuse dans son propre perimetre"
    if ev.get("dedans_cle") != "matrice/data/commun/cible.py":
        return False, ("EPARGNE : la cle d un fichier de la Matrice n est plus sa forme"
                       " canonique : " + repr(ev.get("dedans_cle")))
    return True, ("hors allowlist REFUSE (aucune cle inventee) ; allowlist de la racine et"
                  " fichier de la Matrice EPARGNES")


def releves_sains():
    tout = " ".join(t for _n, temoins in GROUPES_CONTRAT for t in temoins)
    return {
        "carte": {"carte": True, "fonction": True, "convertit": TEXTE_FUTILE_ATTENDU},
        "lancements-a-nu": {"boucles": 8, "a_nu": [], "hors": 131, "vus_hors": 139},
        "cadences-mortes": {"messages": ["cadence nettoyee : cobaye (pid mort 999999)"],
                            "morte": {"type": "arret", "intervalle": 42, "pid": None},
                            "vivante": {"type": "demarrage", "intervalle": 42, "pid": 4242},
                            "appels": 3},
        "clore": {"ok": [0, "regularisation"], "motif": [2, "motif-manquant"],
                  "etat": [1, "etat-present"], "rien": [1, "rien-a-regulariser"],
                  "vide": [1, "rien-a-regulariser"],
                  "trace": ["reprise", {"mission": "MO-X", "regularisation": "m"}]},
        "porte": {"futile": TEXTE_FUTILE_ATTENDU,
                  "futile_journal": "[ASCII] CORRIGE : 3 caractere(s) en lignes 1,2\n",
                  "futile_refus": "", "hors": TEXTE_HORS_CARTE,
                  "hors_refus": "REFUS (code 2) : 1 caractere(s) ... ligne 1 : " + CODE_POINT
                                + " ... matrice/data/commun/carte_ascii.py (CARTE_CONVERSION)."},
        "aide": {"aide": "Point d'entree\n" + tout, "contrat": tout},
        "muet": {"outils": {"lire": True, "ecrire": True, "bdd-usages": False}},
        "modes": {"extracteur": True, "declarees": ["modes-emploi-outils"],
                  "listes_nues": [], "manquantes": {}, "sans_usage": {},
                  "plancher_absent": {}, "plancher_non_servi": {},
                  "briques": 51, "silencieuses": [],
                  "missions": 89, "preparees": 1, "inservables": [], "hors_plafond": [],
                  "plafond": 8},
        "perimetre": {"racine": "/faux/workspace",
                      "allowliste_existe": True, "hors_existe": True, "dedans_existe": True,
                      "allowliste_perimetre": True,
                      "allowliste_cle": "demarrer-optimus-prime.md",
                      "allowliste_chemin": "/faux/workspace/demarrer-optimus-prime.md",
                      "hors_perimetre": False, "hors_cle": None,
                      "dedans_perimetre": True, "dedans_cle": "matrice/data/commun/cible.py"},
        "categorie": {"repare": [0, "routine", "pilote", "ROUTINE"],
                      "hors": [2, "REFUS : categorie inconnue pour le type dev : 'x'\n"
                                  "  Categories fermees de dev : outil, routine, bdd, pilote"],
                      "vrac": [2, "REFUS : EO-000 est encore AU VRAC\n"
                                  "  Classe-le d'abord :  python main.py classer --id EO-000"]},
    }


def releves_casses():
    """Chaque cas casse DOIT faire crier le juge (sinon le controle est creux)."""
    return (
        ("cadences-mortes", "un pid mort laisse dans la cadence",
         {"messages": [], "morte": {"type": "demarrage", "intervalle": 42, "pid": 999999},
          "vivante": {"type": "demarrage", "intervalle": 42, "pid": 4242}, "appels": 3}),
        ("cadences-mortes", "un pid VIVANT efface par le nettoyage",
         {"messages": ["cadence nettoyee : cobaye"],
          "morte": {"type": "arret", "intervalle": 42, "pid": None},
          "vivante": {"type": "demarrage", "intervalle": 42, "pid": None}, "appels": 3}),
        ("cadences-mortes", "un nettoyage plus cable au cycle de vie",
         {"messages": [], "morte": {"type": "arret", "intervalle": 42, "pid": None},
          "vivante": {"type": "demarrage", "intervalle": 42, "pid": 4242}, "appels": 1}),
        ("lancements-a-nu", "une boucle qui lance a nu", {"boucles": 8,
                                                      "a_nu": ["matrice/routines/veille-flux/commun.py:484"],
                                                      "hors": 131, "vus_hors": 139}),
        ("lancements-a-nu", "un releve creux (scan sans rien voir)", {"boucles": 0, "a_nu": [],
                                                                     "hors": 0, "vus_hors": 0}),
        ("carte", "une copie de carte", {"carte": False, "fonction": True,
                                        "convertit": TEXTE_FUTILE_ATTENDU}),
        ("carte", "une fonction recopiee", {"carte": True, "fonction": False,
                                           "convertit": TEXTE_FUTILE_ATTENDU}),
        ("carte", "une carte qui ne convertit plus", {"carte": True, "fonction": True,
                                                     "convertit": "Le caf\u00e9 est pr\u00eat\n"}),
        ("porte", "une faute futile non corrigee", {"futile": TEXTE_FUTILE, "futile_journal": "",
                                                   "futile_refus": "", "hors": "",
                                                   "hors_refus": "x carte_ascii.py " + CODE_POINT}),
        ("porte", "une correction MUETTE", {"futile": TEXTE_FUTILE_ATTENDU, "futile_journal": "",
                                           "futile_refus": "", "hors": "",
                                           "hors_refus": "x carte_ascii.py " + CODE_POINT}),
        ("porte", "un hors-carte accepte", {"futile": TEXTE_FUTILE_ATTENDU,
                                            "futile_journal": "CORRIGE", "futile_refus": "",
                                            "hors": TEXTE_HORS_CARTE, "hors_refus": ""}),
        ("porte", "un refus qui ne nomme pas le caractere",
         {"futile": TEXTE_FUTILE_ATTENDU, "futile_journal": "CORRIGE", "futile_refus": "",
          "hors": TEXTE_HORS_CARTE, "hors_refus": "REFUS (code 2) carte_ascii.py"}),
        ("porte", "un refus sans remede",
         {"futile": TEXTE_FUTILE_ATTENDU, "futile_journal": "CORRIGE", "futile_refus": "",
          "hors": TEXTE_HORS_CARTE, "hors_refus": "REFUS (code 2) " + CODE_POINT}),
        ("aide", "une garantie oubliee dans le CONTRAT",
         {"aide": "x os.replace lf forces", "contrat": "os.replace"}),
        ("muet", "une porte qui ne se note pas", {"outils": {"lire": True, "muette": False}}),
        ("muet", "aucune porte lue", {"outils": {}}),
        ("categorie", "une categorie valide refusee", {"repare": [2, "routine", "pilote", "ROUTINE"],
                                                      "hors": [2, "categories fermees de dev"],
                                                      "vrac": [2, "classer --id"]}),
        ("categorie", "un avant non trace", {"repare": [0, "routine", None, "ROUTINE"],
                                            "hors": [2, "categories fermees de dev"],
                                            "vrac": [2, "classer --id"]}),
        ("categorie", "un role reecrit en silence", {"repare": [0, "routine", "pilote", "PILOTE"],
                                                    "hors": [2, "categories fermees de dev"],
                                                    "vrac": [2, "classer --id"]}),
        ("categorie", "un refus qui ne nomme pas la liste", {"repare": [0, "routine", "pilote", "ROUTINE"],
                                                            "hors": [2, "REFUS"], "vrac": [2, "classer --id"]}),
        ("categorie", "un vrac accepte", {"repare": [0, "routine", "pilote", "ROUTINE"],
                                          "hors": [2, "categories fermees de dev"], "vrac": [0, ""]}),
        ("modes", "un extracteur ABSENT", {"extracteur": False, "declarees": ["x"],
                                           "listes_nues": [], "manquantes": {}, "briques": 0}),
        ("modes", "aucune entree au catalogue", {"extracteur": True, "declarees": [],
                                                 "listes_nues": [], "manquantes": {}, "briques": 3}),
        ("modes", "une liste de NOMS servie", {"extracteur": True, "declarees": ["x"],
                                               "listes_nues": ["outils-disponibles"],
                                               "manquantes": {}, "briques": 3}),
        ("modes", "une brique MUETTE (aucun usage)",
         {"extracteur": True, "declarees": ["x"], "listes_nues": [],
          "manquantes": {"outils": ["muet.py"]}, "briques": 3}),
        ("modes", "une brique au BUT SEUL (usage absent)",
         {"extracteur": True, "declarees": ["x"], "listes_nues": [],
          "manquantes": {}, "briques": 3,
          "sans_usage": {"outils-matrice": ["porte-sans-usage"]}}),
        ("modes", "un plancher qui ne nomme RIEN (protection fantome)",
         {"extracteur": True, "declarees": ["x"], "listes_nues": [], "manquantes": {},
          "briques": 3, "plancher_absent": {"outils-matrice": ["brique-fantome"]}}),
        ("modes", "une essentielle du PLANCHER coupee par la carte",
         {"extracteur": True, "declarees": ["x"], "listes_nues": [], "manquantes": {},
          "briques": 51, "plancher_non_servi": {"outils-matrice": ["suivi-optimus"]}}),
        ("modes", "une carte VIDE (racines mortes)",
         {"extracteur": True, "declarees": ["x"], "listes_nues": [],
          "manquantes": {}, "briques": 0, "silencieuses": []}),
        ("modes", "une carte COUPEE EN SILENCE",
         {"extracteur": True, "declarees": ["x"], "listes_nues": [],
          "manquantes": {}, "briques": 51, "silencieuses": ["outils"]}),
        ("modes", "une mission qui DECLARE un outil NON SERVABLE",
         {"extracteur": True, "declarees": ["x"], "listes_nues": [], "manquantes": {},
          "briques": 51, "silencieuses": [], "missions": 3, "preparees": 1,
          "inservables": ["MO-900:outil-fantome.py"], "hors_plafond": [], "plafond": 8}),
        ("modes", "une liste preparee AU-DELA du plafond",
         {"extracteur": True, "declarees": ["x"], "listes_nues": [], "manquantes": {},
          "briques": 51, "silencieuses": [], "missions": 3, "preparees": 1,
          "inservables": [], "hors_plafond": ["MO-900 (9/8)"], "plafond": 8}),
        ("clore", "une regularisation acceptee SANS motif",
         {"ok": [0, "regularisation"], "motif": [0, "regularisation"],
          "etat": [1, "etat-present"], "rien": [1, "rien-a-regulariser"],
          "vide": [1, "rien-a-regulariser"],
          "trace": ["reprise", {"mission": "MO-X", "regularisation": "m"}]}),
        ("clore", "une trace OUBLIANT le motif",
         {"ok": [0, "regularisation"], "motif": [2, "motif-manquant"],
          "etat": [1, "etat-present"], "rien": [1, "rien-a-regulariser"],
          "vide": [1, "rien-a-regulariser"],
          "trace": ["reprise", {"mission": "MO-X"}]}),
        ("perimetre", "un fichier de la racine HORS allowlist ACCEPTE",
         {"racine": "/faux/workspace", "allowliste_existe": True, "hors_existe": True,
          "dedans_existe": True, "allowliste_perimetre": True,
          "allowliste_cle": "demarrer-optimus-prime.md",
          "allowliste_chemin": "/faux/workspace/demarrer-optimus-prime.md",
          "hors_perimetre": True, "hors_cle": None,
          "dedans_perimetre": True, "dedans_cle": 'matrice/data/commun/cible.py'}),
        ("perimetre", "une cle INVENTEE pour un fichier hors perimetre",
         {"racine": "/faux/workspace", "allowliste_existe": True, "hors_existe": True,
          "dedans_existe": True, "allowliste_perimetre": True,
          "allowliste_cle": "demarrer-optimus-prime.md",
          "allowliste_chemin": "/faux/workspace/demarrer-optimus-prime.md",
          "hors_perimetre": False, "hors_cle": 'AGENTS-historique.md',
          "dedans_perimetre": True, "dedans_cle": 'matrice/data/commun/cible.py'}),
        ("perimetre", "l allowlist de la racine REFUSEE",
         {"racine": "/faux/workspace", "allowliste_existe": True, "hors_existe": True,
          "dedans_existe": True, "allowliste_perimetre": False,
          "allowliste_cle": "demarrer-optimus-prime.md",
          "allowliste_chemin": "/faux/workspace/demarrer-optimus-prime.md",
          "hors_perimetre": False, "hors_cle": None,
          "dedans_perimetre": True, "dedans_cle": 'matrice/data/commun/cible.py'}),
        ("perimetre", "la cle de la Matrice pas canonique",
         {"racine": "/faux/workspace", "allowliste_existe": True, "hors_existe": True,
          "dedans_existe": True, "allowliste_perimetre": True,
          "allowliste_cle": "demarrer-optimus-prime.md",
          "allowliste_chemin": "/faux/workspace/demarrer-optimus-prime.md",
          "hors_perimetre": False, "hors_cle": None,
          "dedans_perimetre": True, "dedans_cle": 'cerveau-projet/matrix/data/commun/cible.py'}),
    )


JUGES = {"carte": juger_carte, "porte": juger_porte, "aide": juger_aide,
         "clore": juger_clore,
         "categorie": juger_categorie, "muet": juger_muet, "modes": juger_modes_emploi,
         "lancements-a-nu": juger_lancements_a_nu,
         "cadences-mortes": juger_cadences_mortes,
         "perimetre": juger_perimetre}


def autotest():
    """Epreuve du PIEGE : chaque donnee saine doit PASSER, chaque donnee cassee CRIER."""
    print("== autotest du garde (L-032) ==")
    echecs = 0
    for nom, releve in releves_sains().items():
        ok, detail = JUGES[nom](releve)
        if not ok:
            echecs += 1
        print("[" + ("OK" if ok else "KO") + "] sain accepte : " + nom + " -- " + detail)
    for nom, motif, releve in releves_casses():
        ok, _detail = JUGES[nom](releve)
        if ok:
            echecs += 1
        print("[" + ("OK" if not ok else "KO") + "] casse accuse : " + nom + " (" + motif + ")")
    print("\n" + ("PIEGE OK : chaque juge accepte le sain et crie sur le casse." if not echecs
                  else "PIEGE KO : " + str(echecs) + " verdict(s) faux."))
    return 1 if echecs else 0


def main():
    analyseur = argparse.ArgumentParser()
    analyseur.add_argument("--racine", default=".")
    analyseur.add_argument("--autotest", action="store_true")
    arguments = analyseur.parse_args()
    if arguments.autotest:
        return autotest()
    racine = Path(arguments.racine).resolve()
    zone = trouver_zone(racine)
    if zone is None:
        print("Zone optimus-prime introuvable sous " + str(racine))
        return 2
    matrice = zone.parent.parent / "matrice"
    controler("carte ascii : un seul domicile", *juger_carte(relever_carte(matrice)))
    controler("porte ecrire : corrige et refuse", *juger_porte(relever_porte(matrice)))
    controler("aide <-> contrat de la porte", *juger_aide(relever_aide(matrice)))
    controler("porte pause-session clore : regularisation couverte",
              *juger_clore(relever_clore(matrice)))
    controler("entonnoir : la categorie se repare", *juger_categorie(relever_categorie(zone)))
    controler("outils : aucune porte muette au journal", *juger_muet(relever_muet(matrice)))
    controler("boucles de fond : aucun lancement a nu (EO-428)",
              *juger_lancements_a_nu(relever_lancements_a_nu(matrice)))
    controler("cycle de vie : une cadence ne nomme jamais un pid mort (EO-428)",
              *juger_cadences_mortes(relever_cadences_mortes(matrice)))
    controler("modes d emploi : un outil se livre avec son usage",
              *juger_modes_emploi(relever_modes_emploi(zone)))
    controler("perimetre : la regle de l allowlist racine (MO-411)",
              *juger_perimetre(relever_perimetre(matrice)))
    ko = [nom for nom, ok, _detail in RESULTATS if not ok]
    if ko:
        print("\nECART CONTRATS : " + str(len(ko)) + " controle(s) en echec : " + ", ".join(ko))
        return 1
    print("\nVERDICT OK : les contrats tiennent (" + str(len(RESULTATS)) + " controles).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
