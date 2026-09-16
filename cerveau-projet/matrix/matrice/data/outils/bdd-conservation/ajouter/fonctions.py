"""Fonctions metier du registre de conservation."""
from datetime import datetime

from constants import CATEGORIES, PREFIXE_ID, STATUTS, VERDICTS


def prochain_id(donnees):
    maximum = 0
    for entree in donnees.get("elements", []):
        identifiant = str(entree.get("id") or "")
        if identifiant.startswith(PREFIXE_ID):
            suffixe = identifiant[len(PREFIXE_ID):]
            if suffixe.isdigit():
                maximum = max(maximum, int(suffixe))
    return PREFIXE_ID + str(maximum + 1).zfill(3)


def separer_liste(texte):
    if not texte:
        return []
    return [part.strip() for part in texte.split(",") if part.strip()]


def trouver(donnees, identifiant):
    for entree in donnees.get("elements", []):
        if entree.get("id") == identifiant:
            return entree
    return None


def creer_entree(donnees, options):
    categorie = options.get("categorie", "")
    if categorie and categorie not in CATEGORIES:
        return None, "Categorie inconnue : " + categorie
    entree = {
        "id": prochain_id(donnees),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mission": options.get("mission", ""),
        "source": options.get("source", ""),
        "destination": options.get("destination", ""),
        "categorie": categorie or "HISTORIQUE",
        "statut": "propose",
        "verdict": "",
        "raison": options.get("raison", ""),
        "lecteurs": separer_liste(options.get("lecteurs", "")),
        "ecrivains": separer_liste(options.get("ecrivains", "")),
        "index": separer_liste(options.get("index", "")),
        "sha_avant": options.get("sha-avant", ""),
        "sha_apres": options.get("sha-apres", ""),
        "octets_avant": options.get("octets-avant", ""),
        "octets_apres": options.get("octets-apres", ""),
        "lignes_avant": options.get("lignes-avant", ""),
        "lignes_apres": options.get("lignes-apres", ""),
        "restaurable": options.get("restaurable", "false").lower() == "true",
        "operation": "proposer",
        "archive": options.get("archive", ""),
        "preuve": options.get("preuve", ""),
        "tags": separer_liste(options.get("tags", "")),
    }
    if not entree["source"] or not entree["raison"] or not entree["tags"]:
        return None, "source, raison et tags sont obligatoires"
    donnees["compteur"] = max(donnees.get("compteur", 0), int(entree["id"][len(PREFIXE_ID):]))
    donnees.setdefault("elements", []).append(entree)
    return entree, ""


def classer_entree(donnees, identifiant, categorie, raison):
    entree = trouver(donnees, identifiant)
    if entree is None:
        return None, "Element inconnu : " + identifiant
    if categorie not in CATEGORIES:
        return None, "Categorie inconnue : " + categorie
    if entree.get("statut") not in ("propose", "classe"):
        return None, "Transition refusee depuis le statut " + str(entree.get("statut"))
    if not raison:
        return None, "Raison obligatoire"
    entree["categorie"] = categorie
    entree["raison"] = raison
    entree["statut"] = "classe"
    entree["operation"] = "classer"
    entree["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return entree, ""


def decider_entree(donnees, identifiant, verdict, destination, preuve):
    entree = trouver(donnees, identifiant)
    if entree is None:
        return None, "Element inconnu : " + identifiant
    if verdict not in VERDICTS:
        return None, "Verdict inconnu : " + verdict
    if entree.get("statut") != "classe":
        return None, "Decision refusee : statut attendu classe"
    if not preuve:
        return None, "Preuve obligatoire"
    if verdict == "archiver" and not destination:
        return None, "Destination obligatoire pour archiver"
    entree["verdict"] = verdict
    entree["destination"] = destination
    entree["preuve"] = preuve
    entree["statut"] = "decide"
    entree["operation"] = "decider"
    entree["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return entree, ""
