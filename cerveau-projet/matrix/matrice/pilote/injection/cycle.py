#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cycle.py -- Cycle d'injections du pilote cameleon (porte injection/)

Orchestre les injections automatiques au bon moment : demarrage, puis les
phases de la mission (avant / pendant / apres).

Il vit DANS la porte qu'il sert : c'est la porte (`injection/entry.py`) qui
l'importe, en nom qualifie (`from injection.cycle import ...`) -- sans aucune
insertion dans sys.path. Un module a la racine du pilote qui ne sert qu'une
porte n'est pas dans la table d'architecture (lecon L-057).

DECISION (2026-09-15) : L'ETAT DISPARAIT ; L'HISTORIQUE EST ARCHIVE.

`cycle-state.json` enregistrait `phase`, `mission courante` et `dernier
injection` -- une COPIE de ce que la file dit deja. Mesure du 2026-09-15 avant
suppression :
  - l'etat annoncait `phase: mission` et une mission `M-CAM` "en cours" depuis le
    2026-09-13T06:30:20, alors que la file du cameleon portait 0 mission (compteur
    89) et que `M-CAM` n'existe dans AUCUN journal (147 lignes relues) : un id
    fabrique, gele deux jours, qu'un operateur lit en premier ;
  - l'historique etait tronque EN SILENCE a ses 100 dernieres entrees ;
  - `demarrer()` EFFACAIT la mission courante de l'etat, donc la trace d'une
    session pouvait disparaitre sans un mot.
C'est le meme defaut que le Flux 2, corrige le meme jour (EO-119 / MO-110) : deux
proprietaires d'etat coexistent, et le plus menteur est celui qu'on ouvre en
premier.

Ce qui remplace quoi :
  - la VERITE est la FILE (`file-missions.json`) : `statut` la lit, et une mission
    que la file ne connait pas ne peut plus naitre dans un etat (garde ci-dessous) ;
  - l'HISTORIQUE vit dans `cycle-historique-archive.json`, EN AJOUT SEUL, sans
    troncature (les 2 entrees de l'ancien etat et son temoignage y sont verses) ;
  - les INJECTIONS ne changent pas : elles lancent le catalogue `injecter.py`.

PERIMETRE (L-016) : ce module est celui du cameleon. Il n'importe RIEN du contenu
d'Optimus (`_operateur/`) : il utilise les outils de SON domicile (`commun`,
`constants`). La deuxieme face du meme defaut ne se repare pas en faisant lire au
cameleon les coulisses de la maintenance.

Usage:
  python injection/cycle.py demarrer
  python injection/cycle.py mission --action <debut|pendant|fin>
  python injection/cycle.py statut
"""

import sys
import json
import argparse
import os
from pathlib import Path
from datetime import datetime
from typing import Optional


PILOTE = Path(__file__).resolve().parent.parent   # le pilote : dossier parent de la porte
INJECTION_DIR = Path(__file__).resolve().parent   # la porte elle-meme (un seul dossier d'injection)

# Le dossier du pilote doit etre importable : la porte qui tourne l'a deja en
# sys.path, l'insertion ne sert qu'a l'EXECUTION DIRECTE du CLI (diagnostic).
if str(PILOTE) not in sys.path:
    sys.path.insert(0, str(PILOTE))

from commun import charger_file, mission_en_cours  # noqa: E402
from constants import STATUT_TERMINEE  # noqa: E402

# L'HISTORIQUE du cycle : en AJOUT SEUL, jamais reecrit, jamais tronque.
NOM_ARCHIVE = "cycle-historique-archive.json"
CHEMIN_ARCHIVE = PILOTE / NOM_ARCHIVE


def charger_archive() -> dict:
    """L'historique du cycle -- archive en AJOUT SEUL.

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
              + " illisible -- archive vide pour cette lecture (le fichier n'est pas ecrase).")
        return {"historique": [], "archive_le": None}
    if not isinstance(donnees, dict) or not isinstance(donnees.get("historique"), list):
        print("ALERTE archive cycle : forme inattendue dans " + str(CHEMIN_ARCHIVE)
              + " -- archive vide pour cette lecture.")
        return {"historique": [], "archive_le": None}
    return donnees


def archiver(evenement: dict) -> int:
    """Ajoute UN evenement a l'historique du cycle. Retourne le total archive.

    ECRITURE ATOMIQUE (tmp + remplacement) : une coupure en cours d'ecriture ne
    doit pas amputer l'histoire. Rien n'est jamais supprime, rien n'est tronque.
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


class CycleCameleon:
    """Le cycle : il LANCE le catalogue et ARCHIVE ce qu'il fait. AUCUN ETAT.

    La mission en cours n'est pas stockee : elle est LUE dans la file
    (`commun.charger_file` + `mission_en_cours`), seule source de verite.
    """

    def lire_file(self) -> dict:
        """La file du cameleon -- tolerance : une file illisible ne bloque pas, elle est DITE."""
        try:
            return charger_file()
        except Exception as erreur:  # noqa: BLE001 -- jamais bloquant sur un journal
            print("ALERTE file des missions illisible : " + str(erreur)[:120])
            return {"missions": [], "compteur": 0}

    def lire_mission_en_cours(self) -> Optional[dict]:
        """La mission EN COURS, lue dans la FILE -- jamais une copie."""
        return mission_en_cours(self.lire_file())

    def derniere_terminee(self) -> Optional[dict]:
        """La derniere mission TERMINEE de la file (ou None).

        Sert a la seule tolerance de `mission_fin` : si la mission a deja ete
        cloturee dans la file (`main.py fin`), les injections apres-mission
        doivent encore pouvoir se rattacher a ELLE au lieu de refuser.
        """
        terminees = [m for m in self.lire_file().get("missions", [])
                     if m.get("statut") == STATUT_TERMINEE]
        if not terminees:
            return None
        return max(terminees, key=lambda m: m.get("terminee_le") or "")

    def injecter(self, categorie: str, format_sortie: str = "texte"):
        """Executer une injection du CATALOGUE et l'ARCHIVER."""
        injecter_script = INJECTION_DIR / "injecter.py"

        import subprocess
        cmd = [sys.executable, str(injecter_script), categorie, "--format", format_sortie]
        resultat = subprocess.run(cmd, capture_output=True, text=True)

        if resultat.returncode == 0:
            print(resultat.stdout)
        else:
            # Jamais de degradation silencieuse : une injection ratee se DIT.
            print("[ERREUR] Injection " + categorie + " echouee :")
            print(resultat.stderr)

        archiver({
            "action": "injection",
            "categorie": categorie,
            "timestamp": datetime.now().isoformat()
        })

    def demarrer(self):
        """Demarrer le cycle (injections de demarrage). Aucun etat ecrit.

        L'ancien `demarrer` EFFACAIT la mission courante de l'etat : il ne peut
        plus rien effacer (il n'y a plus d'etat), mais il DIT ce que la file porte.
        """
        print("=" * 60)
        print("DEMARRAGE DU CYCLE CAMELEON")
        print("=" * 60)
        print()

        en_cours = self.lire_mission_en_cours()
        if en_cours is not None:
            print("ATTENTION : la file porte deja une mission EN COURS ("
                  + str(en_cours.get("id")) + ") : le demarrage n'y touche pas.")

        self.injecter("demarrage")

        print()
        print("=" * 60)
        if en_cours is None:
            print("CYCLE PRET - En attente de mission (phase deduite de la file)")
        else:
            print("CYCLE EN MISSION : " + str(en_cours.get("id")) + " (phase deduite de la file)")
        print("=" * 60)

    def mission_debut(self, mission_id: str, theme: str = None):
        """Debut de mission : injections avant-mission. REFUS si l'id n'est pas celui de la file.

        C'est LA garde qui manquait : l'etat a enregistre le 2026-09-13 une mission
        `M-CAM` qu'aucune file ni aucun journal ne connaissait, et cette mission a
        survecu deux jours dans l'etat. L'identite d'une mission vient de la FILE --
        jamais d'un etat, jamais d'un argument. Une mission que la file ne connait
        pas ne peut donc plus naitre ici (refus, aucune injection, aucune ecriture).
        """
        print("=" * 60)
        print("DEBUT DE MISSION: " + str(mission_id))
        print("=" * 60)
        print()

        en_cours = self.lire_mission_en_cours()
        identifiant_file = en_cours.get("id") if en_cours else None
        if identifiant_file != mission_id:
            print("REFUS : la file ne declare PAS cette mission en cours"
                  " (mission en cours de la file : "
                  + (str(identifiant_file) if identifiant_file else "aucune") + ").")
            print("  L'identite d'une mission vient de la FILE, jamais d'un etat :"
                  " un cycle ne peut pas ouvrir une mission que la file ignore.")
            print("  Injectez la mission d'abord : python3 main.py injecter")
            return 1

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

    def mission_pendant(self):
        """Pendant la mission : injections pendant-mission. La mission vient de la FILE."""
        en_cours = self.lire_mission_en_cours()
        if en_cours is None:
            print("REFUS : aucune mission EN COURS dans la file. Le cycle ne tient plus"
                  " d'etat : la file est la seule source. Injectez la mission d'abord.")
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

    def mission_fin(self, bilan: str = None):
        """Fin de mission : injections apres-mission + trace archivee.

        Rattachement : la mission EN COURS de la file, sinon la DERNIERE TERMINEE
        (protocole possible : `main.py fin` cloture la file avant l'appel au cycle).
        Rien n'est invente : le rattachement est DIT.
        """
        en_cours = self.lire_mission_en_cours()
        rattachement = "mission en cours"
        if en_cours is None:
            en_cours = self.derniere_terminee()
            rattachement = "derniere mission terminee de la file"

        if en_cours is None:
            print("Injections apres-mission : AUCUNE mission dans la file, donc aucune"
                  " trace rattachee (le cycle ne fabrique pas de mission).")
            self.injecter("apres-mission")
            return 1

        mission_id = en_cours.get("id")
        print("=" * 60)
        print("FIN DE MISSION: " + str(mission_id) + "  (" + rattachement + ")")
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
            "rattachement": rattachement,
            "timestamp": datetime.now().isoformat()
        })

        print()
        print("Mission " + str(mission_id) + " terminee (trace : " + NOM_ARCHIVE
              + ", " + str(total) + " entrees).")
        return 0

    def statut(self):
        """Afficher le statut du cycle : la PHASE est DEDUITE de la file."""
        en_cours = self.lire_mission_en_cours()
        archive = charger_archive()
        injections = [e for e in archive.get("historique", []) if e.get("action") == "injection"]

        print("=" * 60)
        print("STATUT DU CYCLE CAMELEON")
        print("=" * 60)
        print()

        print("Phase: " + ("mission" if en_cours is not None else "pret") + " (deduite de la file)")

        if en_cours is not None:
            print("Mission courante: " + str(en_cours.get("id")))
            print("  Theme: " + str(en_cours.get("theme", "non defini")))
            print("  Injectee le: " + str(en_cours.get("injectee_le", "inconnu")))
            print("  Statut: " + str(en_cours.get("statut", "inconnu")))
        else:
            print("Mission courante: aucune")

        if injections:
            derniere = injections[-1]
            print("Derniere injection: " + str(derniere.get("categorie"))
                  + " a " + str(derniere.get("timestamp")))
        else:
            print("Derniere injection: aucune trace")

        print()
        print("Historique ARCHIVE: " + str(len(archive.get("historique", [])))
              + " entrees (ajout seul, aucune troncature)")
        return 0


def main():
    parser = argparse.ArgumentParser(description="Gestionnaire de cycle pour le Cameleon")
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

    cycle = CycleCameleon()

    if args.commande == "demarrer":
        cycle.demarrer()
    elif args.commande == "mission":
        if args.action == "debut":
            if not args.id:
                print("[ERREUR] --id requis pour le debut de mission")
                return 1
            return cycle.mission_debut(args.id, args.theme)
        elif args.action == "pendant":
            return cycle.mission_pendant()
        elif args.action == "fin":
            return cycle.mission_fin(args.bilan)
        else:
            print("[ERREUR] Action requise: debut, pendant, ou fin")
            return 1
    elif args.commande == "statut":
        return cycle.statut()
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
