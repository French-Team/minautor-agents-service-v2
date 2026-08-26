# -*- coding: ascii -*-
"""historique_bdd.py - BDD SQLite pour l'historique chronologique (v1 + v2).

Stocke chaque entree dans une table SQLite (historique.db) avec :
- date ISO, agent, llm, type_action, raison (texte complet)
- Purge automatique : les entrees de plus de JOURS_VALIDITE sont supprimees
  a chaque ecriture (lazy cleanup).

Utilise par :
- v2 : historique.py (jarvis/fonctions/)
- v1 : activer-agent-principal.py (tools/activer/)

Avantages vs le corps de AGENTS-historique.md :
- Consultation rapide (SELECT, WHERE, ORDER BY)
- Pas de parsing markdown fragile
- Nettoyage automatique (pas de fichier qui grossit a l'infini)
- Entree/texte complet preserves (pas de troncature)
"""

import os
import sqlite3
from datetime import datetime, timedelta

# Defaults (D15 : modifiables via config si besoin)
JOURS_VALIDITE = 7
DB_FILENAME = "historique.db"


def _db_path(racine: str) -> str:
    """Chemin vers la BDD dans un dossier dedie."""
    dossier = os.path.join(racine, "cerveau-projet", "freelance",
                           "tools-commun", "jarvis", "historique")
    os.makedirs(dossier, exist_ok=True)
    return os.path.join(dossier, DB_FILENAME)


def _connecter(racine: str) -> sqlite3.Connection:
    """Connecter a la BDD, creer la table si absente."""
    chemin = _db_path(racine)
    conn = sqlite3.connect(chemin)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS historique (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_iso TEXT NOT NULL,
            agent TEXT NOT NULL,
            llm TEXT NOT NULL,
            type_action TEXT NOT NULL DEFAULT 'R',
            raison TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_date ON historique(date_iso DESC)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_agent ON historique(agent)
    """)
    conn.commit()
    return conn


def ecrire(racine: str, agent: str, llm: str, type_action: str,
           raison: str, date_iso: str = None) -> bool:
    """Ecrire une entree dans la BDD + purger les entrees expirees.

    Args:
        racine: chemin racine du projet
        agent: nom de l agent
        llm: id du LLM
        type_action: R, IR, etc.
        raison: texte complet (pas de troncature)
        date_iso: date ISO (defaut = maintenant UTC)

    Returns:
        True si succes
    """
    if date_iso is None:
        date_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    try:
        conn = _connecter(racine)
        conn.execute(
            "INSERT INTO historique (date_iso, agent, llm, type_action, raison)"
            " VALUES (?, ?, ?, ?, ?)",
            (date_iso, agent, llm, type_action, raison)
        )
        # Purge des entrees expirees (comparaison substr pour ignorer les microsecondes)
        borne = datetime.utcnow() - timedelta(days=JOURS_VALIDITE)
        borne_str = borne.strftime("%Y-%m-%dT%H:%M:%S")
        conn.execute(
            "DELETE FROM historique WHERE substr(date_iso,1,19) < ?",
            (borne_str,))
        conn.commit()
        conn.close()
        return True
    except (sqlite3.Error, OSError) as exc:
        print("[HISTORIQUE-BDD] ERREUR: %s" % str(exc)[:80])
        return False


def consulter(racine: str, agent: str = None, jours: int = None,
              limite: int = 50) -> list:
    """Consulter l'historique (lecture seule).

    Args:
        racine: chemin racine du projet
        agent: filtre par agent (None = tous)
        jours: filtre par nombre de jours (None = tous, max JOURS_VALIDITE)
        limite: nombre max de resultats

    Returns:
        Liste de dicts [{date_iso, agent, llm, type_action, raison}, ...]
    """
    try:
        conn = _connecter(racine)
        query = "SELECT date_iso, agent, llm, type_action, raison FROM historique"
        params = []
        conditions = []
        if agent:
            conditions.append("agent = ?")
            params.append(agent)
        if jours:
            borne = (datetime.utcnow() - timedelta(days=jours))
            conditions.append("substr(date_iso,1,19) >= ?")
            params.append(borne.strftime("%Y-%m-%dT%H:%M:%S"))
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY date_iso DESC LIMIT ?"
        params.append(limite)
        cursor = conn.execute(query, params)
        colonnes = ["date_iso", "agent", "llm", "type_action", "raison"]
        resultats = [dict(zip(colonnes, row)) for row in cursor.fetchall()]
        conn.close()
        return resultats
    except (sqlite3.Error, OSError):
        return []


def compter(racine: str) -> int:
    """Nombre total d'entrees dans la BDD."""
    try:
        conn = _connecter(racine)
        cursor = conn.execute("SELECT COUNT(*) FROM historique")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except (sqlite3.Error, OSError):
        return 0


def purger(racine: str) -> int:
    """Purger manuellement les entrees expirees.

    Returns:
        Nombre d'entrees supprimees
    """
    try:
        conn = _connecter(racine)
        borne = datetime.utcnow() - timedelta(days=JOURS_VALIDITE)
        borne_str = borne.strftime("%Y-%m-%dT%H:%M:%S")
        cursor = conn.execute(
            "DELETE FROM historique WHERE substr(date_iso,1,19) < ?",
            (borne_str,))
        supprimees = cursor.rowcount
        conn.commit()
        conn.close()
        return supprimees
    except (sqlite3.Error, OSError):
        return 0
