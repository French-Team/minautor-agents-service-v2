#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cycle.py -- Cycle de vie d'Optimus : le CATALOGUE d'injections et les phases.

DECISION CREATEUR (2026-09-15, EO-119 / MO-110) : L'ETAT DISPARAIT ; L'HISTORIQUE
EST ARCHIVE (jamais supprime).

`cycle-state.json` portait `phase`, `mission courante` et `dernier injection`.
Aucun outil ne le lisait, et il MENTAIT : il annoncait `phase: pret` et
`mission courante: null` alors que la file portait MO-110 en cours (mesure du
2026-09-15). Deux proprietaires d'etat coexistaient, et le plus menteur etait
celui qu'un operateur ouvre en premier.

Ce qui remplace quoi :
  - la VERITE est la FILE (`file-missions-optimus.json`) : `statut` la lit ;
  - l'HISTORIQUE vit dans `cycle-historique-archive.json`, EN AJOUT SEUL
    (les 59 entrees de l'ancien etat y ont ete versees, plus celles a venir) ;
  - les INJECTIONS ne changent pas : elles lancent le catalogue `injecter.py`.

Usage:
  python cycle.py demarrer
  python cycle.py mission --action <debut|pendant|fin>
  python cycle.py statut
  python cycle.py verifier-profil
"""


import subprocess  # autosuffisant : ce module n importait subprocess qu EN LOCAL
import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-414, vague 5 du lot) -----------------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu) : on remonte
# jusqu au dossier `matrix`, et on REFUSE plutot que de deviner (garde-foi L-006).
# Pose en TETE de module : `import subprocess` de ce fichier est LOCAL a une
# fonction -- une ancre indented aurait casse le fichier (mesure du 2026-09-25).
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
import json
import argparse
import os
from pathlib import Path
from datetime import datetime
from typing import Optional


# Ce module vit DANS la porte qu'il sert (`pilote/injection/`) depuis le
# desenchevetrement : ses chemins se derivent de CETTE position, jamais de
# l'ancienne (racine du pilote). Trois chemins etaient restes calibres sur
# l'ancienne profondeur et creaient un dossier FANTOME `pilote/pilote/` (trouve
# le 2026-09-13 en declarant le debut de MO-057 : l'injection avant-mission
# appelait `injection/injection/injecter.py`).
#
# UN SEUL dossier d'injection : la porte `injection/`. Le dossier `injections/`
# (moteur de catalogue parallelle) a ete fusionne dedans le 2026-09-13.
# `CONFIG_PATH` (declare et jamais lu) a ete retire : le catalogue se lit dans
# le moteur, a cote de son `config.json`.
PILOTE = Path(__file__).resolve().parent.parent      # la porte -> le pilote
INJECTION_DIR = Path(__file__).resolve().parent      # la porte elle-meme

# La porte du pilote, quand elle tourne, a deja ce dossier en sys.path[0]
# (main.py vit a la racine du pilote) : l'insertion n'est la que pour
# l'EXECUTION DIRECTE (`python injection/cycle.py`), et elle est conditionnelle.
if str(PILOTE) not in sys.path:
    sys.path.insert(0, str(PILOTE))

from commun import charger_file, mission_en_cours  # noqa: E402

# L'HISTORIQUE du cycle : en AJOUT SEUL, jamais reecrit, jamais supprime.
NOM_ARCHIVE = "cycle-historique-archive.json"
CHEMIN_ARCHIVE = PILOTE / NOM_ARCHIVE

# La fiche profil vit a la RACINE du matrix (`matrix/USER-PROFIL.md`), jamais
# dans la zone operateur (chemin mythique corrige en MO-051). Garde-fou L-006 :
# le dossier cible est VERIFIE par son nom avant de servir d'ancre.
# Racine DETECTEE par le marqueur partage (M-076), jamais comptee (L-013).
BORNES_REMONTEE = 30


def _racine_matrix(depart: Path) -> Optional[Path]:
    """Remonte jusqu'au dossier nomme `matrix` (garde-fou L-006 : c'est le NOM qui decide)."""
    courant = depart
    for _ in range(BORNES_REMONTEE):
        if courant.name == "matrix":
            return courant
        if courant.parent == courant:
            break
        courant = courant.parent
    return None


RACINE = _racine_matrix(PILOTE)

if RACINE is None:
    PROFIL_PATH = None
else:
    PROFIL_PATH = RACINE / "USER-PROFIL.md"

# Le questionnaire du profil vit DANS sa categorie (`pilote/profil/`), pas a la
# racine du pilote : la porte `profil` le lance, ce module s'y adresse par son
# vrai chemin (MO-051).
QUESTIONNAIRE_PATH = PILOTE / "profil" / "questionnaire.py"


def charger_archive() -> dict:
    """L'historique du cycle -- ARCHIVE en ajout seul (EO-119).

    Tolerance : archive absente ou illisible -> archive vide (un historique
    manquant ne doit JAMAIS bloquer un demarrage), mais on le DIT (L-037) : un
    historique ampute en silence serait pire que pas d'historique.
    """
    if not CHEMIN_ARCHIVE.exists():
        return {"historique": [], "archive_le": None}
    try:
        with open(CHEMIN_ARCHIVE, "r", encoding="utf-8") as flux:
            donnees = json.load(flux)
    except (OSError, ValueError):
        print("ALERTE archive cycle : " + str(CHEMIN_ARCHIVE)
              + " illisible -- on repart sur une archive vide (l'histoire existante"
              " n'est pas ecrasee, elle est seulement pas lue).")
        return {"historique": [], "archive_le": None}
    if not isinstance(donnees, dict) or not isinstance(donnees.get("historique"), list):
        print("ALERTE archive cycle : forme inattendue dans " + str(CHEMIN_ARCHIVE)
              + " -- archive vide utilisee.")
        return {"historique": [], "archive_le": None}
    return donnees


def archiver(evenement: dict) -> int:
    """Ajoute UN evenement a l'historique du cycle. Retourne le total archive.

    ECRITURE ATOMIQUE (tmp + remplacement) : une coupure en cours d'ecriture ne
    doit pas amputer l'histoire. Rien n'est jamais supprime ici.
    """
    donnees = charger_archive()
    donnees["historique"].append(evenement)
    donnees["archive_le"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temporaire = CHEMIN_ARCHIVE.with_name(NOM_ARCHIVE + ".tmp")
    with open(temporaire, "w", encoding="utf-8", newline="\n") as flux:
        json.dump(donnees, flux, ensure_ascii=True, indent=2)
        flux.write("\n")
    os.replace(temporaire, CHEMIN_ARCHIVE)
    return len(donnees["historique"])


class CycleOptimus:
    """Le cycle : il LANCE le catalogue et ARCHIVE ce qu'il fait. AUCUN ETAT.

    La mission en cours n'est pas stockee : elle est LUE dans la file
    (`commun.charger_file` + `mission_en_cours`), seule source de verite.
    """

    def lire_mission_en_cours(self) -> Optional[dict]:
        """La mission EN COURS, lue dans la FILE -- jamais une copie (EO-119)."""
        return mission_en_cours(charger_file())

    def injecter(self, categorie: str, format_sortie: str = "texte"):
        """Executer une injection du CATALOGUE et l'ARCHIVER."""
        injecter_script = INJECTION_DIR / "injecter.py"

        import subprocess

        cmd = [sys.executable, str(injecter_script), categorie, "--format", format_sortie]
        resultat = lancer_enfant(cmd, capture_output=True, text=True)

        if resultat.returncode == 0:
            print(resultat.stdout)
        else:
            # Doctrine 2026-09-13 : jamais de degradation silencieuse.
            print("[ERREUR] Injection " + categorie + " echouee :")
            print(resultat.stderr)

        archiver({
            "action": "injection",
            "categorie": categorie,
            "timestamp": datetime.now().isoformat()
        })

    def fiche(self, categorie: str):
        """IMPRIME la FICHE TECHNIQUE BORNEE d'une categorie (moule a jetons, MO-471).

        Meme porte que l injection (injecter.py, verbe `fiche`) et meme lancement
        (lancer_enfant) : la fiche se lit donc SANS COMMANDE, la ou l agent commence
        -- le demarrage. NON bloquant : un echec se DIT (le refus de la porte), il ne
        tue jamais un demarrage.
        """
        injecter_script = INJECTION_DIR / "injecter.py"
        resultat = lancer_enfant(
            [sys.executable, str(injecter_script), "fiche", categorie],
            capture_output=True, text=True)
        if resultat.returncode == 0:
            print()
            print("--- FICHE TECHNIQUE BORNEE : sources de la phase " + categorie + " ---")
            print(resultat.stdout, end="")
            print("--- fin fiche (injection entiere : injecter.py " + categorie + ") ---")
        else:
            detail = (resultat.stdout or resultat.stderr or "").strip().splitlines()
            print("[fiche] non servie pour " + categorie + " : "
                  + (detail[0] if detail else "raison non dite par la porte"))

    def verifier_profil(self) -> bool:
        """Verifier si le profil utilisateur est rempli."""
        if PROFIL_PATH is None or not PROFIL_PATH.exists():
            return False

        with open(PROFIL_PATH, "r", encoding="utf-8") as f:
            contenu = f.read()

        # Verifier si le pseudo est rempli
        for ligne in contenu.split("\n"):
            if "**Pseudo**" in ligne:
                parties = ligne.split("|")
                if len(parties) >= 3:
                    valeur = parties[2].strip()
                    if valeur and valeur != "A remplir":
                        return True
        return False

    def demarrer(self):
        """Demarrer le cycle (injections de demarrage). Aucun etat ecrit."""
        print("=" * 60)
        print("DEMARRAGE DU CYCLE OPTIMUS PRIME")
        print("=" * 60)
        print()

        # Verifier le profil utilisateur
        if not self.verifier_profil():
            print("PROFIL UTILISATEUR NON REMPLI")
            print("Lancement du questionnaire de remplissage...")
            print()
            import subprocess
            if not QUESTIONNAIRE_PATH.is_file():
                # Aucune degradation silencieuse : un questionnaire introuvable
                # est DIT, il ne passe pas pour un lancement reussi.
                print("  [ERREUR] questionnaire introuvable : " + str(QUESTIONNAIRE_PATH))
            else:
                lancer_enfant([sys.executable, str(QUESTIONNAIRE_PATH)])
            print()

        self.injecter("demarrage")

        # FICHE TECHNIQUE (MO-471, decisions D1/D5) : la fiche bornee des sources du
        # DEMARRAGE est servie AVEC l injection -- l agent la lit sans commande. Non
        # bloquant (doctrine du sac-a-dos) : un echec se DIT, il ne tue pas le demarrage.
        self.fiche("demarrage")

        # Reprise de session (MO-092) : le pilote guide aussi la REPRISE.
        # La BDD sessions est la trace persistante du travail deja fait ; l'agent
        # doit lire la session precedente AVANT de repartir (le createur a demande
        # que la session precedente soit RECUPERABLE). Non bloquant.
        try:
            from commun import annoncer_reprise

            code_reprise, sortie_reprise = annoncer_reprise()
            if code_reprise == 0 and sortie_reprise:
                print()
                print("--- REPRISE DE SESSION (BDD sessions, lecture bornee) ---")
                print(sortie_reprise)
                print("--- fin reprise : reprendre le chantier la ou il s'arrete ---")
        except Exception as erreur:  # noqa: BLE001 -- jamais bloquant au demarrage
            print("[reprise] trace de session non lue (" + str(erreur)[:120] + ")")

        # CREDIBILITE DES MISSIONS RESTAUREES (process automatique, MO-387) : une
        # mission ancienne (chargee un jour anterieur) est JUGEe avant d etre executee.
        # Le process est JOUE ICI parce que le pilote ne doit pas dependre de la MEMOIRE
        # de l agent : ce qui se joue a chaque reprise se joue au demarrage. Il REND le
        # verdict, le TRACE, et APPLIQUE l obsolescence -- retirer du lot ce qui est
        # deja fait ou perime -- sans createur et sans question. NON bloquant (doctrine
        # du sac-a-dos) : un echec se DIT, il ne tue jamais un demarrage.
        try:
            from commun import annoncer_credibilite

            code_credibilite, sortie_credibilite = annoncer_credibilite()
            if sortie_credibilite:
                print()
                print(sortie_credibilite)
            if code_credibilite != 0:
                print("[credibilite] une action n a pas abouti : elle sera rejouee au"
                      " prochain demarrage.")
        except Exception as erreur:  # noqa: BLE001 -- jamais bloquant au demarrage
            print("[credibilite] process non joue (" + str(erreur)[:120] + ")")

        # Contrat ECRIT/LU (MO-121) : le pilote OUVRE la session dans la BDD
        # sessions -- la trace automatique doit porter le TAG que la reprise
        # LIT (session-ouverte), jamais un tag qu'elle ignore (friction 41).
        # L'etat est lu AVANT d'ecrire : une ouverture deja posee n'est pas
        # doublee. Non bloquant : une trace ratee ne tue jamais un demarrage.
        try:
            from commun import ouvrir_session

            code_ouverture, sortie_ouverture = ouvrir_session()
            if code_ouverture != 0:
                print("[session] ouverture non tracee (" + sortie_ouverture[:120] + ")")
            elif sortie_ouverture:
                print("[session] " + sortie_ouverture)
        except Exception as erreur:  # noqa: BLE001 -- jamais bloquant au demarrage
            print("[session] ouverture non tracee (" + str(erreur)[:120] + ")")

        print()
        print("=" * 60)
        print("CYCLE PRET - En attente de mission")
        print("=" * 60)

    def mission_debut(self, mission_id: str, theme: str = None) -> int:
        """Debut de mission : injections avant-mission + TRACE du debut.

        La file est la seule verite (EO-119), et un debut se REFUSE comme une fin
        (MO-551) : si la mission declaree n'est pas la mission EN COURS de la file,
        le geste s'arrete ICI, en code 2, SANS rien archiver.

        POURQUOI (mesure du 2026-10-03) : la porte VOYAIT l'ecart, l'AFFICHAIT, puis
        archivait quand meme et rendait 0. Trois traces fausses ont ete ecrites ainsi
        dans l'historique du cycle -- `MO-535` (mission close deux jours plus tot) et
        `MO-551` deux fois (mission chargee mais jamais conduite) -- et l'historique
        est la seule chose qui survive a la disparition de l'etat : un historique
        qui dit "MO-551 a demarre" alors qu'aucune mission n'a existe est un mensonge
        durable. La porte jumelle `mission_fin` refuse depuis EO-356 ; l'asymetrie
        debut/fin etait le defaut.
        """
        en_cours = self.lire_mission_en_cours()
        identifiant_file = en_cours.get("id") if en_cours else None
        if identifiant_file != mission_id:
            print("REFUS : " + str(mission_id) + " n'est pas la mission EN COURS de la file"
                  " (" + (str(identifiant_file) if identifiant_file else "aucune") + ")."
                  " La file est la seule source de verite, rien n'est archive.")
            print("  Remede : une mission chargee devient COURANTE par"
                  " python main.py conduire --id " + str(mission_id)
                  + " (une mission 'en-attente' n'est pas en cours).")
            if identifiant_file:
                print("  Soit on declare le debut de " + str(identifiant_file)
                      + ", soit on termine celle-la d'abord (serie stricte).")
            else:
                print("  Soit on charge une mission : python main.py charger"
                      " --theme <nom> --type <type> --objectif \"...\"")
            return 2

        print("=" * 60)
        print("DEBUT DE MISSION: " + str(mission_id))
        print("=" * 60)
        print()

        # Injections avant mission
        self.injecter("avant-mission")

        total = archiver({
            "action": "mission_debut",
            "mission": mission_id,
            "theme": theme,
            "timestamp": datetime.now().isoformat()
        })

        print()
        print("Mission " + str(mission_id) + " demarree (trace : " + NOM_ARCHIVE
              + ", " + str(total) + " entrees).")
        print("Utilisez 'mission --action pendant' pour les injections en cours de mission.")
        return 0

    def mission_retracter(self, mission_id: str, motif: str, horodatage: str = None) -> int:
        """Retire une trace de debut FAUSSE sans l effacer (MO-551).

        L'archive du cycle est en AJOUT SEUL ("rien n'est jamais supprime ici") :
        une trace fausse ne se supprime donc pas, elle se RETIRE -- on append un
        evenement de retrait qui la NOMME, sur le modele du `bilan_retire` que la
        porte `rouvrir` pose deja pour un bilan fautif. La trace porte le retrait,
        elle n'efface rien.

        Trois refus, tous nommes : un motif vide (un retrait muet ne se distingue pas
        d'une panne), une mission absente de la FILE (on ne retire pas l'histoire
        d'une mission que la file ignore), et une mission dont l'archive ne porte
        AUCUN `mission_debut` (rien a retirer : le geste serait muet).
        """
        if not mission_id:
            print("REFUS : --id est OBLIGATOIRE -- un retrait nomme ce qu'il retire.")
            return 2
        motif = str(motif or "").strip()
        if not motif:
            print("REFUS : --motif est OBLIGATOIRE -- une trace ne se retire jamais en"
                  " silence : le motif dit CE QUI est faux et pourquoi.")
            return 2

        file_missions = charger_file()
        connue = any(str(mission.get("id", "")) == mission_id
                     for mission in file_missions.get("missions", []))
        if not connue:
            print("REFUS : " + mission_id + " est INCONNUE de la file ACTIVE -- on ne"
                  " retire pas l'histoire d'une mission que la file ignore.")
            print("  Remede : verifier l'id dans python main.py statut")
            return 2

        donnees = charger_archive()
        historique = [evenement for evenement in donnees.get("historique", [])
                      if isinstance(evenement, dict)]
        # L archive est en AJOUT SEUL : rien ne marque l evenement d origine. Ce qui
        # dit QUELS evenements sont deja retires, ce sont les retraits precedents, qui
        # en portent les horodatages. On apparie donc par horodatage -- sinon un
        # second retrait retrouverait les memes evenements et les declarerait deux fois.
        deja_retires = set()
        for evenement in historique:
            if evenement.get("action") != "mission_debut_retracte":
                continue
            # ATTENTION : la variable de boucle ne s'appelle PAS `horodatage` --
            # elle masquerait le PARAMETRE du meme nom (mesure du 2026-10-03 : le
            # filtre comparait donc toujours au dernier retrait deja ecrit, et
            # refusait meme l horodatage qu on venait de passer).
            for deja_couvert in (evenement.get("premiers_retires") or []):
                deja_retires.add(str(deja_couvert))
        visees = [evenement for evenement in historique
                  if evenement.get("action") == "mission_debut"
                  and str(evenement.get("mission", "")) == mission_id
                  and str(evenement.get("timestamp", "")) not in deja_retires]
        # VISER UN EVENEMENT : une mission peut porter une trace LEGITIME ET des
        # traces fausses (mesure du 2026-10-03 : MO-551 en portait deux fausses --
        # mission chargee mais jamais conduite -- puis une vraie, la prise de round
        # ayant ete faite entre-temps). Retirer "toutes les traces de MO-551" y
        # aurait efface la bonne. `--horodatage` designe donc celle qu on vise.
        if horodatage:
            visees = [evenement for evenement in visees
                      if str(evenement.get("timestamp", "")) == horodatage]
            if not visees:
                print("REFUS : " + mission_id + " n'a aucun evenement 'mission_debut'"
                      " ACTIF a l'horodatage " + horodatage + ".")
                print("  Les traces actives de " + mission_id + " :")
                for evenement in historique:
                    if evenement.get("action") == "mission_debut" \
                            and str(evenement.get("mission", "")) == mission_id:
                        print("    " + str(evenement.get("timestamp", "?"))
                              + (" (DEJA RETIREE)" if str(
                                  evenement.get("timestamp", "")) in deja_retires else ""))
                return 2
        if not visees:
            print("REFUS : l'archive ne porte AUCUN 'mission_debut' actif pour "
                  + mission_id + " -- rien a retirer (les traces de cette mission sont"
                  " deja retirees, ou elle n'en a jamais eu).")
            return 2

        horodatage = datetime.now().isoformat()
        total = archiver({
            "action": "mission_debut_retracte",
            "mission": mission_id,
            "motif": motif,
            "evenements_retires": len(visees),
            "premiers_retires": [evenement.get("timestamp") for evenement in visees],
            "timestamp": horodatage,
        })
        print("Trace(s) mission_debut de " + mission_id + " RETIREE(S) : "
              + str(len(visees)) + " evenement(s).")
        print("  Motif : " + motif)
        print("  Les evenements d'origine RESTENT dans l'archive (ajout seul) : la trace"
              " porte le retrait, elle n'efface rien.")
        print("  Nouvelle taille : " + str(total) + " entrees.")
        return 0

    def mission_pendant(self):
        """Pendant la mission : injections pendant-mission. La mission vient de la FILE."""
        en_cours = self.lire_mission_en_cours()
        if en_cours is None:
            print("REFUS : aucune mission EN COURS dans la file. Le cycle ne tient plus"
                  " d'etat (EO-119) : la file est la seule source. Charge et injecte"
                  " la mission d'abord.")
            return 1

        mission_id = en_cours.get("id")
        print("=" * 60)
        print("INJECTIONS PENDANT MISSION: " + str(mission_id))
        print("=" * 60)
        print()

        self.injecter("pendant-mission")

        print()
        print("Injections mises a jour pour la mission " + str(mission_id) + ".")
        return 0

    def mission_fin(self, bilan: str = None, mission_id: str = None):
        """Fin de mission : injections apres-mission + TRACE de la fin (archivee).

        `mission_id` est FACULTATIF et VERIFIE (mesure du 2026-09-25 : `pilote
        mission --action fin --id MO-412` a clos MO-408, l id etant ignore par
        l appelant). Quand il est donne, il doit NOMMER la mission EN COURS de la
        file : un id different est REFUSE (code 2) sans rien archiver -- une cloture
        ne s ecrit JAMAIS sous le nom d une autre mission (EO-356). Sans `--id`, le
        geste garde son sens ancien : il clot la mission EN COURS.
        """
        en_cours = self.lire_mission_en_cours()
        if en_cours is None:
            print("REFUS : aucune mission EN COURS dans la file. Le cycle ne tient plus"
                  " d'etat (EO-119) : la file est la seule source.")
            return 1

        courante = en_cours.get("id")
        if mission_id and mission_id != courante:
            print("REFUS : --id " + str(mission_id) + " n est pas la mission EN COURS de la"
                  " file (" + str(courante) + "). Une cloture ne s ecrit jamais sous le nom"
                  " d une autre mission : conduis d abord la mission voulue"
                  " (`pilote conduire --id " + str(mission_id) + "`).")
            return 2

        mission_id = courante
        print("=" * 60)
        print("FIN DE MISSION: " + str(mission_id))
        print("=" * 60)
        print()

        # Injections apres mission
        self.injecter("apres-mission")

        total = archiver({
            "action": "mission_terminee",
            "mission": {
                "id": mission_id,
                "theme": en_cours.get("theme"),
                "bilan": bilan,
                "timestamp": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat()
        })

        print()
        print("Mission " + str(mission_id) + " terminee (trace : " + NOM_ARCHIVE
              + ", " + str(total) + " entrees).")
        # La phase n'est PAS annoncee ici : elle se LIT sur la file, et la file
        # porte encore la mission tant que sa cloture n'est pas passee.
        print("Cloture la mission dans la file (main.py fin --bilan \"...\") :"
              " la phase du cycle se lit la, elle ne s'ecrit plus.")
        return 0
        return 0

    def statut(self):
        """Statut du cycle : la PHASE se LIT sur la file (aucun etat stocke).

        Le detail de la mission en cours n'est pas repete ici : `afficher_statut`
        le donne depuis la file (une seule voix pour une seule verite).
        """
        en_cours = self.lire_mission_en_cours()
        historique = charger_archive().get("historique", [])

        print("=" * 60)
        print("CYCLE OPTIMUS : phase LUE sur la file (aucun etat stocke)")
        print("=" * 60)
        print()

        print("Phase : " + ("mission" if en_cours else "pret")
              + "   (deduite de la file)")

        derniere = None
        for evenement in reversed(historique):
            if evenement.get("action") == "injection":
                derniere = evenement
                break
        if derniere:
            print("Derniere injection : " + str(derniere.get("categorie"))
                  + " a " + str(derniere.get("timestamp")))

        print("Historique ARCHIVE : " + str(len(historique)) + " entrees ("
              + NOM_ARCHIVE + ", ajout seul)")


def main():
    parser = argparse.ArgumentParser(description="Gestionnaire de cycle pour Optimus")
    subparsers = parser.add_subparsers(dest="commande", help="Commande a executer")

    # Commande: demarrer
    subparsers.add_parser("demarrer", help="Demarrer le cycle")

    # Commande: mission
    p_mission = subparsers.add_parser("mission", help="Gerer une mission")
    p_mission.add_argument("--action", choices=["debut", "pendant", "fin"],
                          help="Action a effectuer")
    p_mission.add_argument("--id", help="ID de la mission")
    p_mission.add_argument("--theme", help="Theme de la mission")
    p_mission.add_argument("--bilan", help="Bilan de fin de mission")

    # Commande: statut
    subparsers.add_parser("statut", help="Afficher le statut")

    args = parser.parse_args()

    cycle = CycleOptimus()

    if args.commande == "demarrer":
        cycle.demarrer()
    elif args.commande == "mission":
        if args.action == "debut":
            if not args.id:
                print("[ERREUR] --id requis pour le debut de mission")
                return 1
            cycle.mission_debut(args.id, args.theme)
        elif args.action == "pendant":
            cycle.mission_pendant()
        elif args.action == "fin":
            cycle.mission_fin(args.bilan)
        else:
            print("[ERREUR] Action requise: debut, pendant, ou fin")
            return 1
    elif args.commande == "statut":
        cycle.statut()
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
