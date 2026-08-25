# -*- coding: ascii -*-
"""tic.py - UNE tache : emettre des signaux periodiques (threads daemon).

Decision utilisateur 2026-08-24 :
  - l'horloge demarre AVEC le serveur jarvis ;
  - CHAQUE routine possede SON PROPRE tic (declenchement a son propre
    rythme, a des moments differents des autres) ;
  - un CONSTRUCTEUR (construire_tic) et un DECORATEUR (@periodique)
    facilitent la creation des prochains tics.
"""

import json
import threading
from datetime import datetime, timezone
from pathlib import Path

# Registre global : nom -> Tic (observable / pilotable d'un seul endroit)
TICS_ACTIFS = {}


class Tic(threading.Thread):
    """Emet self.rappel() toutes les self.intervalle secondes.

    Thread daemon : il meurt avec le processus qui l'heberge (le serveur).
    Un crash du rappel ne tue JAMAIS le tic (trace + continue).
    decalage : attente AVANT le premier cycle - permet de desenlever les
    tics entre eux (declenchements a des moments differents).
    """

    def __init__(self, intervalle_secondes, rappel, nom="tic", journal=None,
                 decalage=0):
        super().__init__(daemon=True, name=nom)
        self.intervalle = max(5, int(intervalle_secondes))
        self.decalage = max(0, int(decalage))
        self.rappel = rappel
        self.nom = nom
        self.journal = Path(journal) if journal else None
        self._arret = threading.Event()

    def run(self):
        self._tracer("demarrage",
                     f"intervalle={self.intervalle}s decalage={self.decalage}s")
        if self.decalage and self._arret.wait(self.decalage):
            return
        while not self._arret.wait(self.intervalle):
            try:
                self.rappel()
                self._tracer("signal")
            except Exception as e:
                self._tracer("erreur", repr(e)[:120])

    def stop(self):
        """Arret propre : le thread se termine avant la prochaine emission."""
        self._arret.set()

    def _tracer(self, evenement, detail=""):
        """Tracer chaque evenement dans signaux.jsonl (observable H24)."""
        if not self.journal:
            return
        try:
            entree = {
                "date": datetime.now(timezone.utc).strftime(
                    "%Y-%m-%dT%H:%M:%S"),
                "tic": self.nom,
                "evenement": evenement,
            }
            if detail:
                entree["detail"] = detail
            self.journal.parent.mkdir(parents=True, exist_ok=True)
            with open(self.journal, "a", encoding="utf-8") as f:
                f.write(json.dumps(entree, ensure_ascii=False) + "\n")
        except OSError:
            pass


# --- CONSTRUCTEUR -------------------------------------------------------

def construire_tic(intervalle_secondes, rappel, nom="tic", journal=None,
                   decalage=0, demarrer=True):
    """CONSTRUCTEUR de tic : cree, enregistre et (par defaut) demarre un
    tic dedie. C'est LE moyen canonique de creer un signal periodique."""
    tic = Tic(intervalle_secondes, rappel, nom=nom, journal=journal,
              decalage=decalage)
    TICS_ACTIFS[tic.nom] = tic
    if demarrer:
        tic.start()
    return tic


def arreter_tous():
    """Arreter proprement tous les tics du registre."""
    for tic in list(TICS_ACTIFS.values()):
        tic.stop()


def etat_tics():
    """Etat observable du registre : {nom: vivant}."""
    return {nom: tic.is_alive() for nom, tic in TICS_ACTIFS.items()}


# --- DECORATEUR ---------------------------------------------------------

def periodique(intervalle_secondes, nom=None, journal=None, decalage=0):
    """Decorateur : dote une fonction de SON PROPRE tic.

    La fonction reste appelable normalement (execution synchrone).
    Elle gagne deux methodes :
      f.tic_demarrer()  -> construit + demarre le tic dedie
      f.tic_arreter()   -> arrete le tic dedie
    """
    def decorateur(fonction):
        nom_tic = nom or f"tic-{fonction.__name__}"

        def tic_demarrer():
            existant = TICS_ACTIFS.get(nom_tic)
            if existant and existant.is_alive():
                return existant
            return construire_tic(intervalle_secondes, fonction,
                                  nom=nom_tic, journal=journal,
                                  decalage=decalage)

        def tic_arreter():
            existant = TICS_ACTIFS.get(nom_tic)
            if existant:
                existant.stop()
                return True
            return False

        fonction.tic_demarrer = tic_demarrer
        fonction.tic_arreter = tic_arreter
        fonction.tic_nom = nom_tic
        return fonction
    return decorateur
