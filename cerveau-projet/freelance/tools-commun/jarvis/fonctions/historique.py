# -*- coding: ascii -*-
"""fonctions/historique.py v0.17.0 - Trois destinations (fichiers V2 separes,
   decision utilisateur 2026-08-26 : la v2 est l evolution de la v1, chaque
   session a SES fichiers - plus aucun partage v1/v2) :
1. AGENTS-activite-recente-v2.md : vue rapide (encart session-freelance,
   50 entrees max, format 3 colonnes, UTF8+CRLF)
2. AGENTS-historique-v2.md : chronologie body v2 (100 dernieres actions,
   UTF8+CRLF)
3. historique.db (SQLite) : journal chronologique complet (texte integral,
   purge automatique apres 7 jours)
Les fichiers v1 (session-admin) sont geres par activer-agent-principal
(AGENTS-activite-recente.md + AGENTS-historique.md, ASCII+LF).
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# P10 : la racine se DETECTE via os_path, elle ne se compte pas
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "os_path", "fonctions"))
from racine import trouver_racine

RACINE = Path(trouver_racine(__file__))
ACTIVITE_FILE = RACINE / "AGENTS-activite-recente-v2.md"
GRADES_FILE = RACINE / "cerveau-projet" / "freelance" / "tools-commun" \
    / "grades" / "grades-v2.json"
AGENTS_FILE = Path(os.environ.get("AGENTS_FILE", str(RACINE / "AGENTS.md")))

# Import de la BDD (lazy pour ne pas casser si sqlite3 absent)
_bdd = None


def _get_bdd():
    global _bdd
    if _bdd is None:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import historique_bdd as _hb
            _bdd = _hb
        except ImportError:
            pass
    return _bdd


MAX_ENTREES = 50  # entrees par encart
MAX_CORPS = 100  # entrees max dans le corps AGENTS-historique-v2.md
TRONCATURE_ENCART = 70  # raison tronquee dans l encart (3 colonnes = plus de place)
HISTORIQUE_FILE = RACINE / "AGENTS-historique-v2.md"


def _couleur_agent(agent: str) -> str:
    """Emoji couleur du grade d un agent ou d une routine (grades-v2.json)."""
    try:
        data = json.loads(GRADES_FILE.read_text(encoding="utf-8"))
    except Exception:
        return "\u26aa"
    grade = data.get("agents", {}).get(agent)
    if grade is None:
        grade = data.get("routines", {}).get(agent)
    if grade is None:
        return data.get("defaut", {}).get("emoji", "\u26aa")
    for e in data.get("echelle", []):
        if e.get("grade") == grade:
            return e.get("emoji", "\u26aa")
    return data.get("defaut", {}).get("emoji", "\u26aa")


def _secteur_agent(agent: str) -> str:
    """Determiner le secteur d un agent/routine depuis ses mots-cles."""
    try:
        data = json.loads(GRADES_FILE.read_text(encoding="utf-8"))
    except Exception:
        return data.get("secteurs", {}).get("defaut", "\U0001f4cb")
    mapping = data.get("secteurs", {}).get("mapping", {})
    defaut = data.get("secteurs", {}).get("defaut", "\U0001f4cb")
    agent_dir = RACINE / "cerveau-projet" / "freelance" / agent
    if not agent_dir.exists():
        routines_dir = RACINE / "cerveau-projet" / "freelance" / "routines"
        for subdir in ["surveillance", "demarrage", "arret"]:
            script = routines_dir / subdir / f"{agent}.py"
            if script.exists():
                contenu = script.read_text(encoding="utf-8")[:500]
                for mot, emoji in mapping.items():
                    if mot in contenu:
                        return emoji
                break
        return defaut
    fiche = agent_dir / f"{agent}.md"
    if fiche.exists():
        contenu = fiche.read_text(encoding="utf-8")[:1000]
        m_tags = re.search(r"tags:\s*(.+)", contenu)
        if m_tags:
            tags = [t.strip().lower() for t in m_tags.group(1).split(",")]
            for tag in tags:
                if tag in mapping:
                    return mapping[tag]
        m_mc = re.search(r'mot-cles:\s*\[(.+?)\]', contenu)
        if m_mc:
            mots = [m.strip().strip('"').lower() for m in m_mc.group(1).split(",")]
            for mot in mots:
                if mot in mapping:
                    return mapping[mot]
    return defaut


def _lire(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except FileNotFoundError:
        return ""


def _ecrire(path: Path, contenu: str):
    """Ecriture ATOMIQUE."""
    contenu = contenu.replace("\r\n", "\n").replace("\n", "\r\n")
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        with open(tmp, "w", encoding="utf-8", newline="") as fh:
            fh.write(contenu)
        os.replace(str(tmp), str(path))
    except Exception:
        try:
            tmp.unlink(missing_ok=True)
        except Exception:
            pass
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(contenu)


def lire_nom_llm(session: str = "") -> str:
    """Lit le champ 'Nom LLM' du bloc session dans AGENTS.md."""
    try:
        contenu = AGENTS_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        return "inconnu"
    lignes = contenu.split("\n")
    if session:
        debut = None
        for i, ligne in enumerate(lignes):
            if ligne.strip() == f"### Session : {session}":
                debut = i
                break
        if debut is None:
            return "inconnu"
        fin = debut
        while fin < len(lignes) and not lignes[fin].startswith("## "):
            fin += 1
        bloc = lignes[debut:fin]
    else:
        bloc = lignes
    for ligne in bloc:
        if "**Nom LLM**" in ligne:
            parties = [p.strip() for p in ligne.split("|")]
            for j, p in enumerate(parties):
                if p == "**Nom LLM**" and j + 1 < len(parties):
                    return parties[j + 1]
    return "inconnu"


def session_courante() -> str:
    try:
        _dir = os.path.join(RACINE, "cerveau-projet", "freelance",
                            "classeur", "fonctions")
        sys.path.insert(0, _dir)
        import classeur as c
        sessions = c.session_list()
        if sessions:
            return str(sessions[0].get("session", "")) if isinstance(
                sessions[0], dict) else str(sessions[0])
    except Exception:
        pass
    return ""


def normaliser_session(session: str) -> str:
    if session and not session.startswith("session-"):
        return f"session-{session}"
    return session


def historiser(agent: str, raison: str, type_action: str = "R", session: str = ""):
    now = datetime.now()
    heure = now.strftime("%H:%M:%S.%f")[:-3]
    if not session:
        session = session_courante()
    session = normaliser_session(session)
    llm = lire_nom_llm(session)

    _ecrire_encart(session, heure, agent, llm, type_action, raison)
    _ecrire_corps(now, agent, llm, type_action, raison)

    bdd = _get_bdd()
    if bdd:
        bdd.ecrire(
            racine=str(RACINE),
            agent=agent,
            llm=llm,
            type_action=type_action,
            raison=raison,
            date_iso=now.strftime("%Y-%m-%dT%H:%M:%S")
        )

    print(f"[JARVIS] Historique: {agent} a {heure}")
    return True


def _ecrire_encart(session, heure, agent, llm, type_action, raison):
    """Ecrire dans l encart au format tableau simple (1 ligne par entree)."""
    contenu = _lire(ACTIVITE_FILE)
    if not contenu:
        contenu = (
            "---\n"
            "identite:\n"
            '  nom: "Activites recentes v2"\n'
            '  type: "tableau"\n'
            "  appartient_a: jarvis\n"
            "  commun: false\n"
            '  description: "Vue rapide des 50 dernieres actions de la session-freelance (grades, secteurs, raisons, UTF8+CRLF)."\n'
            "---\n\n"
            "## Activites recentes -- session-freelance\n\n"
            "| Grade | Agent | Secteur | Raison | Heure | id | Type |\n"
            "|-------|-------|---------|--------|-------|----|------|\n"
        )
        _ecrire(ACTIVITE_FILE, contenu)

    lignes = contenu.split("\n")

    # Trouver l encart de la session
    entete_encart = f"## Activites recentes -- {session}"
    zone_debut = 0
    trouve_encart = False
    for i, ligne in enumerate(lignes):
        if ligne.strip() == entete_encart:
            zone_debut = i
            trouve_encart = True
            break
    if not trouve_encart:
        print(f"[JARVIS] ATTENTION: encart '{session}' introuvable - premiere table utilisee")

    # Trouver la ligne separateur de la table (|-------|...)
    idx_sep = -1
    for i in range(zone_debut + 1, len(lignes)):
        if lignes[i].startswith("|---"):
            idx_sep = i
            break
    if idx_sep == -1:
        idx_sep = zone_debut + 2

    # Construction de l entree (1 ligne)
    raison_texte = raison if len(raison) <= 100 else raison[:97] + "..."
    raison_texte = raison_texte.replace("|", "-")
    couleur = _couleur_agent(agent)
    secteur = _secteur_agent(agent)
    ligne = f"| {couleur} | {agent} | {secteur} | {raison_texte} | {heure} | {llm} | {type_action} |"

    # Inserer APRES le separateur
    lignes.insert(idx_sep + 1, ligne)

    # Compter les entrees (apres le separateur)
    idx_debut = idx_sep + 1
    nb_entrees = len(lignes) - idx_debut
    if nb_entrees > MAX_ENTREES:
        a_supprimer = nb_entrees - MAX_ENTREES
        del lignes[idx_debut:idx_debut + a_supprimer]

    contenu = "\n".join(lignes)
    _ecrire(ACTIVITE_FILE, contenu)
    return True


def _ecrire_corps(maintenant, agent, llm, type_action, raison):
    contenu = _lire(HISTORIQUE_FILE)
    if not contenu:
        return
    date_jour = maintenant.strftime("%d/%m/%Y")
    heure = maintenant.strftime("%H:%M:%S.%f")[:-3]
    ligne_entree = f"- {heure} | {llm} | {type_action} | {raison}"
    marqueur_jour = f"## {date_jour}"
    marqueur_agent = f"### {agent}"
    lignes = contenu.split("\n")

    idx_jour = -1
    for i, ligne in enumerate(lignes):
        if ligne.strip() == marqueur_jour:
            idx_jour = i
            break

    if idx_jour == -1:
        idx_ins = 0
        m_entete = re.search(r"^---\n.*?\n---\n", contenu, re.MULTILINE | re.DOTALL)
        if m_entete:
            idx_ins = m_entete.end()
        else:
            m_section = re.search(r"^## \d{2}/\d{2}/\d{4}", contenu, re.MULTILINE)
            if m_section:
                idx_ins = m_section.start()
        bloc_jour = ["", marqueur_jour, "", marqueur_agent, ligne_entree]
        for k, b in enumerate(bloc_jour):
            lignes.insert(idx_ins + k, b)
        contenu = "\n".join(lignes)
    else:
        fin_jour = len(lignes)
        for i in range(idx_jour + 1, len(lignes)):
            if lignes[i].strip().startswith("## ") and lignes[i].strip() != marqueur_jour:
                fin_jour = i
                break
        idx_agent = -1
        for i in range(idx_jour + 1, fin_jour):
            if lignes[i].strip() == marqueur_agent:
                idx_agent = i
                break
        if idx_agent == -1:
            idx_ins = fin_jour
            while idx_ins > idx_jour + 1 and lignes[idx_ins - 1].strip() == "":
                idx_ins -= 1
            bloc = ["", marqueur_agent, ligne_entree]
            for k, b in enumerate(bloc):
                lignes.insert(idx_ins + k, b)
        else:
            idx_ins = idx_agent + 1
            while idx_ins < fin_jour and lignes[idx_ins].strip() == "":
                idx_ins += 1
            lignes.insert(idx_ins, ligne_entree)
        contenu = "\n".join(lignes)

    contenu = _limiter_corps(contenu)
    _ecrire(HISTORIQUE_FILE, contenu)


def _limiter_corps(contenu):
    lignes = contenu.split("\n")
    idx_debut_corps = 0
    for i, ligne in enumerate(lignes):
        if ligne.strip().startswith("## ") and not ligne.strip().startswith("## Activites") and not ligne.strip().startswith("---"):
            if "/" in ligne:
                idx_debut_corps = i
                break
    idx_entrees = []
    for i in range(idx_debut_corps, len(lignes)):
        if lignes[i].strip().startswith("- ") and " | " in lignes[i]:
            idx_entrees.append(i)
    if len(idx_entrees) <= MAX_CORPS:
        return contenu
    a_supprimer = len(idx_entrees) - MAX_CORPS
    indices_a_supprimer = sorted(idx_entrees[-a_supprimer:], reverse=True)
    for idx in indices_a_supprimer:
        del lignes[idx]
    return "\n".join(lignes)


def cmd_historiser(args):
    historiser(args.agent, args.raison, args.type,
               session=getattr(args, "session", ""))
