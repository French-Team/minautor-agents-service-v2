"""Fonctions simples de la categorie lire : une seule tache chacune.

Lecture seule, jamais d'ecriture. Tout est annonce (total/lu).
"""
from pathlib import Path

from commun import (
    calculer_sha256,
    dans_perimetre,
    decoupage_lignes,
    lire_contenu,
    lister_fichiers,
    resoudre_chemin,
)
from constants import RACINE

# Le contrat d invisibilite L-016/CV-006 (plancher + zones DECLAREES V-003 du
# classeur) vit dans SON domicile : cette porte le CONSOMME (MO-152). Elle etait
# la SEULE des quatre portes de lecture sans AUCUNE garde d invisibilite : la
# zone suivi-optimus etait lisible alors que la decision M-084 l exclut.
from invisibilite import refus_invisible  # noqa: E402


def _afficher_resultat(chemin_relatif, lignes, total, lu, avec_hash, chemin_absolu, bom, fins, tranche):
    """Affiche UN fichier lu (en-tete + contenu tranche)."""
    sha = ""
    if avec_hash:
        try:
            sha = calculer_sha256(chemin_absolu)
        except OSError as e:
            print("  [hash] illisible : " + str(e))
            sha = ""
    annonce = str(total) + " total, " + str(lu) + " lus"
    if tranche:
        annonce += " (" + tranche + ")"
    if total != lu:
        annonce += " -- TRONQUE (demander --lignes pour la suite)"
    print("=== " + chemin_relatif + " [" + annonce + "] ===")
    if bom:
        print("[BOM UTF-8 detecte, retire a la lecture]")
    if fins != "LF":
        print("[fins de ligne : " + fins + " (attendu LF)]")
    if sha:
        print("[SHA-256] " + sha)
    if not lignes and total > 0:
        print("(tranche vide : hors bornes, total " + str(total) + ")")
        return 0
    for ligne in lignes:
        print(ligne)
    return 0


def lire_fichier(chemin_relatif, tranche, avec_hash, inclure_prive=False):
    """Lit UN fichier. Retourne code 0/1/2."""
    if not dans_perimetre(chemin_relatif):
        print("REFUS : hors perimetre lecture (matrix/ seul, allowlist AGENTS.md/demarrer-*.md) : " + chemin_relatif)
        return 2
    # Zone invisible L-016 (domicile) : fermee par defaut. Seule la Matrice ouvre
    # par --prive ; le cameleon, lui, n ouvre jamais (regle 9 de sa fiche).
    refus = refus_invisible(chemin_relatif)
    if refus and not inclure_prive:
        print(refus)
        return 2
    chemin_absolu = resoudre_chemin(chemin_relatif)
    if not chemin_absolu.exists():
        print("Fichier introuvable : " + chemin_relatif)
        return 1
    if not chemin_absolu.is_file():
        print("N'est pas un fichier : " + chemin_relatif)
        return 1
    try:
        texte, _, bom, fins = lire_contenu(chemin_absolu)
    except UnicodeDecodeError as e:
        print("REFUS : non-UTF8 ou binaire (" + str(e) + ") : " + chemin_relatif)
        return 1
    except OSError as e:
        print("Erreur lecture : " + str(e))
        return 1
    try:
        lignes, total, lu = decoupage_lignes(texte, tranche)
    except ValueError as e:
        print("REFUS : " + str(e))
        return 2
    # 2e canal L-009 : relecture croisee si tranche suspecte (total=0 sur fichier non vide).
    if total == 0 and chemin_absolu.stat().st_size > 0:
        try:
            raw = chemin_absolu.read_bytes()
            if raw.strip():
                print("[2e canal] Alerte : splitlines=0 mais fichier non vide (" + str(len(raw)) + " octets) -- possible encodage.")
        except OSError:
            pass
    return _afficher_resultat(chemin_relatif, lignes, total, lu, avec_hash, chemin_absolu, bom, fins, tranche)


def lire_fichiers(chemins_relatifs, tranche, avec_hash, inclure_prive=False):
    """Lit N fichiers dans l'ordre fourni. Code = max des codes."""
    code_max = 0
    for chemin in chemins_relatifs:
        code = lire_fichier(chemin, tranche, avec_hash, inclure_prive)
        if code > code_max:
            code_max = code
    return code_max


def lire_dossier(chemin_relatif, tranche, avec_hash, filtre, recursif, inclure_prive=False):
    """Liste puis lit chaque fichier du dossier (perimetre verifie)."""
    if not dans_perimetre(chemin_relatif):
        print("REFUS : hors perimetre lecture : " + chemin_relatif)
        return 2
    dossier_absolu = resoudre_chemin(chemin_relatif)
    try:
        fichiers = lister_fichiers(dossier_absolu, filtre, recursif)
    except NotADirectoryError as e:
        print(str(e))
        return 1
    except OSError as e:
        print("Erreur dossier : " + str(e))
        return 1
    if not fichiers:
        print("Aucun fichier dans " + chemin_relatif + (" (filtre " + filtre + ")" if filtre else ""))
        return 0
    print("Dossier " + chemin_relatif + " : " + str(len(fichiers)) + " fichier(s)" + (" [recursif]" if recursif else ""))
    code_max = 0
    for p in fichiers:
        # Chemin relatif pour l'affichage (depuis RACINE).
        try:
            rel = str(p.relative_to(RACINE)).replace("\\", "/")
        except ValueError:
            rel = str(p)
        # Perimetre fichier par fichier (un fichier du dossier peut etre hors allowlist si lien).
        code = lire_fichier(rel, tranche, avec_hash, inclure_prive)
        if code > code_max:
            code_max = code
    return code_max
