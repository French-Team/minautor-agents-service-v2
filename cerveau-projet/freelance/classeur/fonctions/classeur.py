# -*- coding: utf-8 -*-
"""fonctions/classeur.py - Classeur v2 (BDD SQLite, parite fonctionnelle
avec le classeur v1 mais stockage/consultation plus rapides).

Tables :
  - variables  : variable cle/valeur (nom, valeur, source, date, statut)
  - sessions   : profil des sessions v2 (session, id_llm, agent, date)
  - agents     : etat des agents v2 (nom, statut, derniere_activite, mission)
  - utilisateur : carte d identite de l utilisateur (reserve, structure prete)

Regles :
  - La BDD est le SEUL stockage du classeur v2 (pas de fichier markdown).
  - Chemins relatifs a la racine projet (D15, zero valeur en dur).
  - Conventions v2 : UTF-8, emojis autorises, CRLF (D4).
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

_sys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "tools-commun", "os_path", "fonctions")
sys.path.insert(0, _sys_dir)
from racine import trouver_racine

RACINE = trouver_racine(__file__)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "classeur.db")
DB_PATH = os.path.abspath(DB_PATH)

SCHEMA = """
CREATE TABLE IF NOT EXISTS variables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE,
    valeur TEXT DEFAULT '',
    source TEXT DEFAULT '',
    date TEXT DEFAULT '',
    statut TEXT DEFAULT '[OK]'
);
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session TEXT NOT NULL UNIQUE,
    id_llm TEXT DEFAULT '',
    agent TEXT DEFAULT '',
    date TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE,
    statut TEXT DEFAULT '',
    derniere_activite TEXT DEFAULT '',
    mission TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS utilisateur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    champ TEXT NOT NULL UNIQUE,
    valeur TEXT DEFAULT ''
);
"""


def connexion():
    """Ouvrir une connexion (creer la BDD + schema si absents)."""
    dossier = os.path.dirname(DB_PATH)
    if not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def timestamp():
    """Horodatage millisecondes (3 chiffres, parite v0.7.3 v1)."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


# ------------------------------------------------------------------
# variables (cle/valeur)
# ------------------------------------------------------------------

def variable_set(nom, valeur, source="classeur-v2"):
    """Ecrire/metre a jour une variable cle/valeur."""
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO variables (nom, valeur, source, date, statut) "
            "VALUES (?,?,?,?,?) "
            "ON CONFLICT(nom) DO UPDATE SET valeur=excluded.valeur, "
            "source=excluded.source, date=excluded.date, statut=excluded.statut",
            (nom, valeur, source, timestamp(), "[OK]"))
        conn.commit()
    finally:
        conn.close()
    return True


def variable_get(nom):
    """Lire une variable (None si absente)."""
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute("SELECT valeur, source, date FROM variables WHERE nom=?",
                    (nom,))
        ligne = cur.fetchone()
        if ligne is None:
            return None
        return {"nom": nom, "valeur": ligne[0], "source": ligne[1],
                "date": ligne[2]}
    finally:
        conn.close()


def variable_list():
    """Lister toutes les variables."""
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute("SELECT nom, valeur, source, date, statut FROM variables "
                    "ORDER BY nom")
        return [{"nom": r[0], "valeur": r[1], "source": r[2], "date": r[3],
                 "statut": r[4]} for r in cur.fetchall()]
    finally:
        conn.close()


# ------------------------------------------------------------------
# sessions (profil-session-*)
# ------------------------------------------------------------------

def session_set(session, id_llm="", agent="", date=None):
    """Ecrire/metre a jour le profil d une session v2."""
    if date is None:
        date = timestamp()
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sessions (session, id_llm, agent, date) "
            "VALUES (?,?,?,?) "
            "ON CONFLICT(session) DO UPDATE SET id_llm=excluded.id_llm, "
            "agent=excluded.agent, date=excluded.date",
            (session, id_llm, agent, date))
        conn.commit()
    finally:
        conn.close()
    return True


def session_get(session):
    """Lire le profil d une session (None si absente)."""
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute("SELECT session, id_llm, agent, date FROM sessions "
                    "WHERE session=?", (session,))
        ligne = cur.fetchone()
        if ligne is None:
            return None
        return {"session": ligne[0], "id_llm": ligne[1], "agent": ligne[2],
                "date": ligne[3]}
    finally:
        conn.close()


def session_list():
    """Lister toutes les sessions."""
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute("SELECT session, id_llm, agent, date FROM sessions "
                    "ORDER BY session")
        return [{"session": r[0], "id_llm": r[1], "agent": r[2], "date": r[3]}
                for r in cur.fetchall()]
    finally:
        conn.close()


# ------------------------------------------------------------------
# agents (etat des agents v2)
# ------------------------------------------------------------------

def agent_set(nom, statut="", mission="", activite=None):
    """Ecrire/metre a jour l etat d un agent v2."""
    if activite is None:
        activite = timestamp()
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO agents (nom, statut, derniere_activite, mission) "
            "VALUES (?,?,?,?) "
            "ON CONFLICT(nom) DO UPDATE SET statut=excluded.statut, "
            "derniere_activite=excluded.derniere_activite, "
            "mission=excluded.mission",
            (nom, statut, activite, mission))
        conn.commit()
    finally:
        conn.close()
    return True


def agent_get(nom):
    """Lire l etat d un agent (None si absent)."""
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute("SELECT nom, statut, derniere_activite, mission "
                    "FROM agents WHERE nom=?", (nom,))
        ligne = cur.fetchone()
        if ligne is None:
            return None
        return {"nom": ligne[0], "statut": ligne[1],
                "derniere_activite": ligne[2], "mission": ligne[3]}
    finally:
        conn.close()


def agent_list():
    """Lister l etat de tous les agents v2."""
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute("SELECT nom, statut, derniere_activite, mission "
                    "FROM agents ORDER BY nom")
        return [{"nom": r[0], "statut": r[1], "derniere_activite": r[2],
                 "mission": r[3]} for r in cur.fetchall()]
    finally:
        conn.close()


# ------------------------------------------------------------------
# utilisateur (carte d identite, reserve)
# ------------------------------------------------------------------

def utilisateur_set(champ, valeur):
    """Ecrire/metre a jour un champ de la carte d identite utilisateur."""
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO utilisateur (champ, valeur) VALUES (?,?) "
            "ON CONFLICT(champ) DO UPDATE SET valeur=excluded.valeur",
            (champ, valeur))
        conn.commit()
    finally:
        conn.close()
    return True


def utilisateur_get(champ):
    """Lire un champ utilisateur (None si absent)."""
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute("SELECT valeur FROM utilisateur WHERE champ=?", (champ,))
        ligne = cur.fetchone()
        return ligne[0] if ligne else None
    finally:
        conn.close()


def utilisateur_list():
    """Lister tous les champs utilisateur."""
    conn = connexion()
    try:
        cur = conn.cursor()
        cur.execute("SELECT champ, valeur FROM utilisateur ORDER BY champ")
        return [{"champ": r[0], "valeur": r[1]} for r in cur.fetchall()]
    finally:
        conn.close()


# ------------------------------------------------------------------
# vue d ensemble (consultation rapide)
# ------------------------------------------------------------------

def etat_complet():
    """Vue d ensemble : sessions + agents + variables (consultation)."""
    return {
        "sessions": session_list(),
        "agents": agent_list(),
        "variables": variable_list(),
    }


def exporter_json():
    """Exporter tout le classeur en JSON (sauvegarde/portabilite)."""
    conn = connexion()
    try:
        cur = conn.cursor()
        return {
            "variables": variable_list(),
            "sessions": session_list(),
            "agents": agent_list(),
            "utilisateur": utilisateur_list(),
        }
    finally:
        conn.close()