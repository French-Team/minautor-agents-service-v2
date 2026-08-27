# -*- coding: ascii -*-
# compteur.py -- module partage de comptage de tokens
# Importable par n'importe quel outil/routine du codebase.
# D15 : donnees dans data/, code dans fonctions/.
#
# Usage :
#   from compteur import Compteur
#   c = Compteur()
#   c.debut("ma_commande")
#   ... faire quelque chose ...
#   c.fin()
#   print(c.bilan())
#
# Ou en mode ponctuel :
#   from compteur import mesurer_entree, mesurer_sortie
#   entree = mesurer_entree()
#   sortie = mesurer_sortie()
import json
import os
import time
from datetime import datetime
from pathlib import Path


def _racine_projet():
    """Detecte la racine du projet en remontant jusqu'a AGENTS.md."""
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return Path(d)


def _data_dir():
    """Chemin vers data/ du module compteur."""
    return Path(__file__).parent.parent / "data"


def _fichier_historique(racine):
    """Chemin vers tokens-historique.md."""
    return racine / "cerveau-projet" / "freelance" / "historique" / "tokens-historique.md"


# ---------------------------------------------------------------------------
# Mesure de fichiers (entree)
# ---------------------------------------------------------------------------

def mesurer_fichiers(racine, patterns):
    """Mesure tous les fichiers matchant les patterns.
    Retourne liste de {chemin, label, categorie, taille_octets}."""
    resultats = []
    for entree in patterns.get("fichiers", []):
        chemin = Path(racine) / entree["chemin"]
        cat = entree.get("categorie", "autre")
        label = entree.get("label", chemin.name)
        try:
            taille = os.path.getsize(str(chemin))
        except OSError:
            taille = 0
        resultats.append({
            "chemin": str(chemin.relative_to(racine)),
            "label": label,
            "categorie": cat,
            "taille_octets": taille,
        })
    for glob_entry in patterns.get("glob", []):
        motif = Path(racine) / glob_entry["pattern"]
        cat = glob_entry.get("categorie", "autre")
        label = glob_entry.get("label", "")
        for chemin in sorted(Path(racine).glob(str(motif.relative_to(racine)))):
            if chemin.is_file():
                try:
                    taille = os.path.getsize(str(chemin))
                except OSError:
                    taille = 0
                resultats.append({
                    "chemin": str(chemin.relative_to(racine)),
                    "label": label or chemin.name,
                    "categorie": cat,
                    "taille_octets": taille,
                })
    return resultats


def calculer_tokens_entree(resultats, chars_par_token=4.0):
    """Convertit les tailles de fichiers en tokens estimes (entree)."""
    total_octets = sum(r["taille_octets"] for r in resultats)
    return {
        "total_tokens": int(total_octets / chars_par_token),
        "total_octets": total_octets,
        "nb_fichiers": len(resultats),
    }


def mesurer_entree():
    """Mesure rapide des tokens ENTREE. Retourne int (tokens)."""
    racine = _racine_projet()
    data = _data_dir()
    patterns_file = data.parent / "compter-entree" / "data" / "patterns.json"
    if not patterns_file.exists():
        patterns_file = racine / "cerveau-projet" / "freelance" / "tools-commun" / "compter-entree" / "data" / "patterns.json"
    if not patterns_file.exists():
        return 0
    try:
        with open(str(patterns_file), encoding="utf-8") as f:
            patterns = json.load(f)
    except (OSError, ValueError):
        return 0
    fichiers = mesurer_fichiers(str(racine), patterns)
    return calculer_tokens_entree(fichiers, patterns.get("chars_par_token", 4.0))["total_tokens"]


# ---------------------------------------------------------------------------
# Mesure de sources (sortie)
# ---------------------------------------------------------------------------

def mesurer_sources(racine, sources_config):
    """Mesure toutes les sources de sortie. Retourne liste de dict."""
    resultats = []
    for source in sources_config.get("sources", []):
        chemin = Path(racine) / source["chemin"]
        cat = source.get("categorie", "autre")
        label = source.get("label", chemin.name)
        type_src = source.get("type", "fichier")
        try:
            taille = os.path.getsize(str(chemin))
        except OSError:
            taille = 0
        resultats.append({
            "chemin": str(chemin.relative_to(racine)),
            "label": label,
            "categorie": cat,
            "type": type_src,
            "taille_octets": taille,
        })
    return resultats


def calculer_tokens_sortie(resultats, chars_par_token=4.0):
    """Convertit les tailles de sources en tokens estimes (sortie)."""
    total_octets = sum(r["taille_octets"] for r in resultats)
    return {
        "total_tokens": int(total_octets / chars_par_token),
        "total_octets": total_octets,
        "nb_sources": len(resultats),
    }


def mesurer_sortie():
    """Mesure rapide des tokens SORTIE. Retourne int (tokens)."""
    racine = _racine_projet()
    data = _data_dir()
    sources_file = data.parent / "compter-sortie" / "data" / "sources.json"
    if not sources_file.exists():
        sources_file = racine / "cerveau-projet" / "freelance" / "tools-commun" / "compter-sortie" / "data" / "sources.json"
    if not sources_file.exists():
        return 0
    try:
        with open(str(sources_file), encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, ValueError):
        return 0
    resultats = mesurer_sources(str(racine), config)
    return calculer_tokens_sortie(resultats, config.get("chars_par_token", 4.0))["total_tokens"]


# ---------------------------------------------------------------------------
# Historique
# ---------------------------------------------------------------------------

def lire_etat(racine):
    """Lit l'etat actuel depuis tokens-historique.md."""
    etat = {"entree": 0, "sortie": 0, "total": 0}
    chemin = _fichier_historique(racine)
    if not chemin.exists():
        return etat
    try:
        contenu = chemin.read_text(encoding="utf-8")
        for ligne in contenu.split("\n"):
            if "| Tokens ENTREE |" in ligne:
                parts = [p.strip() for p in ligne.split("|") if p.strip()]
                if len(parts) >= 2:
                    try:
                        etat["entree"] = int(parts[1])
                    except ValueError:
                        pass
            elif "| Tokens SORTIE |" in ligne:
                parts = [p.strip() for p in ligne.split("|") if p.strip()]
                if len(parts) >= 2:
                    try:
                        etat["sortie"] = int(parts[1])
                    except ValueError:
                        pass
            elif "| Tokens TOTAL |" in ligne:
                parts = [p.strip() for p in ligne.split("|") if p.strip()]
                if len(parts) >= 2:
                    try:
                        etat["total"] = int(parts[1])
                    except ValueError:
                        pass
    except (OSError, UnicodeDecodeError):
        pass
    return etat


def ecrire_etat(racine, tokens_entree, tokens_sortie):
    """Met a jour la section 'Etat actuel' de tokens-historique.md."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = tokens_entree + tokens_sortie
    chemin = _fichier_historique(racine)
    if not chemin.exists():
        return
    try:
        contenu = chemin.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return
    lignes = contenu.split("\n")
    nouvelles = []
    for ligne in lignes:
        if "| Tokens ENTREE |" in ligne:
            nouvelles.append("| Tokens ENTREE | %d |" % tokens_entree)
        elif "| Tokens SORTIE |" in ligne:
            nouvelles.append("| Tokens SORTIE | %d |" % tokens_sortie)
        elif "| Tokens TOTAL |" in ligne:
            nouvelles.append("| Tokens TOTAL | %d |" % total)
        elif "| Derniere mise a jour |" in ligne:
            nouvelles.append("| Derniere mise a jour | %s |" % now)
        else:
            nouvelles.append(ligne)
    chemin.write_text("\n".join(nouvelles), encoding="utf-8")


def ajouter_ligne(racine, tokens_entree, tokens_sortie, delta_e, delta_s, notes=""):
    """Ajoute une ligne au tableau historique."""
    now = datetime.now().strftime("%H:%M")
    total = tokens_entree + tokens_sortie
    ligne = "| %s | %d | %d | %d | %+d | %+d | %s |" % (
        now, tokens_entree, tokens_sortie, total, delta_e, delta_s, notes)
    chemin = _fichier_historique(racine)
    if not chemin.exists():
        return
    try:
        contenu = chemin.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return
    lignes = contenu.split("\n")
    idx = len(lignes)
    for i in range(len(lignes) - 1, -1, -1):
        lc = lignes[i].strip()
        if lc.startswith("| ") and "---" not in lc:
            idx = i + 1
            break
        elif lc == "":
            continue
        else:
            break
    lignes.insert(idx, ligne)
    chemin.write_text("\n".join(lignes), encoding="utf-8")


# ---------------------------------------------------------------------------
# Classe Compteur -- mode session (debut/fin)
# ---------------------------------------------------------------------------

class Compteur:
    """Compteur de tokens pour une session ou une commande.

    Usage :
        c = Compteur()
        c.debut("nom_commande")
        ... traitement ...
        c.fin()
        print(c.bilan())
    """

    def __init__(self):
        self.racine = _racine_projet()
        self.debut_tokens = 0
        self.fin_tokens = 0
        self.nom = ""
        self.t0 = 0
        self.duree = 0

    def debut(self, nom="commande"):
        """Marque le debut d'une operation."""
        self.nom = nom
        self.t0 = time.monotonic()
        self.debut_tokens = mesurer_entree()
        return self

    def fin(self):
        """Marque la fin d'une operation et calcule le delta."""
        self.duree = time.monotonic() - self.t0
        self.fin_tokens = mesurer_entree()
        # Journaliser dans le JSONL
        self._journaliser()
        return self

    def delta(self):
        """Nombre de tokens consommes pendant l'operation."""
        return self.fin_tokens - self.debut_tokens

    def bilan(self):
        """Chaine de caractres decrivant le bilan."""
        d = self.delta()
        signe = "+" if d >= 0 else ""
        return "%s : %s%d tokens (%.1fs)" % (self.nom, signe, d, self.duree)

    def _journaliser(self):
        """Ecrit une entree dans data/journal-compteur.jsonl."""
        data = _data_dir()
        data.mkdir(parents=True, exist_ok=True)
        fichier = data / "journal-compteur.jsonl"
        entree = {
            "date": datetime.now().isoformat(),
            "nom": self.nom,
            "tokens_debut": self.debut_tokens,
            "tokens_fin": self.fin_tokens,
            "delta": self.delta(),
            "duree_secondes": round(self.duree, 2),
        }
        with open(str(fichier), "a", encoding="utf-8") as f:
            f.write(json.dumps(entree, ensure_ascii=False) + "\n")

    def mettre_a_jour_historique(self):
        """Met a jour tokens-historique.md avec le bilan de cette operation."""
        etat = lire_etat(self.racine)
        delta_e = self.fin_tokens - etat.get("entree", 0)
        ecrire_etat(self.racine, self.fin_tokens, etat.get("sortie", 0))
        ajouter_ligne(self.racine, self.fin_tokens, etat.get("sortie", 0),
                       delta_e, 0, self.nom)
