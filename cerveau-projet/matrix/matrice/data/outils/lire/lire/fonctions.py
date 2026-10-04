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
    motif_hors_perimetre,
    resoudre_chemin,
)
from constants import RACINE, TETE_INCONNUE

# Le contrat d invisibilite L-016/CV-006 (plancher + zones DECLAREES V-003 du
# classeur) vit dans SON domicile : cette porte le CONSOMME (MO-152). Elle etait
# la SEULE des quatre portes de lecture sans AUCUNE garde d invisibilite : la
# zone suivi-optimus etait lisible alors que la decision M-084 l exclut.
from invisibilite import refus_invisible  # noqa: E402


def front_matter_fini(lignes):
    """L indice de la ligne qui CLOT le front matter, ou -1 (pas de front matter)."""
    if not lignes or lignes[0].strip() != "---":
        return -1
    for indice in range(1, len(lignes)):
        if lignes[indice].strip() == "---":
            return indice
    return -1


def tete_docstring(lignes):
    """La fin du docstring de TETE, ou 0 (le fichier n en a pas).

    Un module sans docstring n est pas un fichier casse : le caller tombe alors
    sur la regle des declarations.
    """
    debut = 0
    while debut < len(lignes) and not lignes[debut].strip():
        debut += 1
    if debut >= len(lignes) or not lignes[debut].lstrip().startswith(('"""', "'''")):
        return 0
    if "language=python" in lignes[debut]:
        return debut + 1
    fin_ici = debut
    while fin_ici < len(lignes):
        position = lignes[fin_ici].rfind('"""')
        if position > (debut if fin_ici == debut else -1) or (
                fin_ici > debut and '"""' in lignes[fin_ici]):
            return fin_ici + 1
        fin_ici += 1
    return debut + 1


def tete_automatique(lignes, extension):
    """La TETE d un fichier -- celle qu on veut lire -- SANS DEVINER UN NOMBRE.

    Trois formes reconnues, dans cet ordre, chacune mesuree sur le corpus :
      1. le FRONT MATTER (`---` ... `---`), suivi du titre et de son chapeau ;
      2. le DOCSTRING de tete d un module ;
      3. a defaut : les DECLARATIONS d ouverture (commentaires, imports).

    Le front matter se mesure sur les cartes (carte_identite) et le docstring
    sur les modules : ce sont les DEUX formes que la lecture humaine demande
    reellement. Une forme inconnue ne se devine pas -- elle rend ce qu elle a
    jusqu au premier titre de section, et c'est dit.
    """
    if not lignes:
        return 0
    depart = 0
    clot = front_matter_fini(lignes)
    if clot >= 0:
        depart = clot + 1
        # AVEC front matter, la tete est le PREMIER CHAPITRE : ses sections
        # (`##`) en font partie. Mesure : sur le canal du createur, chercher la
        # prochaine section `##` rendait le FICHIER ENTIER (271/271) -- le
        # `## Mode d emploi` appartient justement a la tete qu on veut lire.
        return depart + _jusqu_au_prochain_titre(lignes, depart, niveau=1)
    if extension == ".py":
        fin_doc = tete_docstring(lignes)
        if fin_doc:
            return fin_doc
        return _jusqu_aux_declarations(lignes, 0)
    return _jusqu_au_prochain_titre(lignes, depart, niveau=1)


def _jusqu_au_prochain_titre(lignes, depart, niveau=1):
    """Le nombre de lignes de l ouverture : jusqu au titre de niveau `niveau`."""
    prefixe = "#" * (niveau + 1) + " "
    for indice in range(depart, len(lignes)):
        if lignes[indice].startswith(prefixe):
            return indice - depart
    return len(lignes) - depart


def _jusqu_aux_declarations(lignes, depart):
    """L ouverture d un module sans docstring : commentaires et imports."""
    fin = depart
    for indice in range(depart, len(lignes)):
        ligne = lignes[indice]
        if ligne.strip() and not ligne.startswith(("#", "from ", "import ")):
            break
        fin = indice + 1
    return fin - depart


def _afficher_resultat(chemin_relatif, lignes, total, lu, avec_hash, chemin_absolu, bom, fins, tranche, tete="", forme=""):
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
    if tete and forme == "inconnue":
        # La forme n a pas ete reconnue : la lecture rend un bloc nomme, et le
        # DIT. Sans cette ligne, l appelant lirait un fichier partiel en croyant
        # avoir lu une tete -- la panne que la mesure du 2026-09-30 a montree.
        annonce += (" -- TETE INCONNUE (--tete auto : aucune forme reconnue pour "
                   + (chemin_absolu.suffix or "ce fichier") + " ; "
                   + str(TETE_INCONNUE) + " lignes rendues -- nommer --tete <N>"
                   + " pour une tranche fixee)")
    elif total != lu:
        # `--tete` n a PAS tronque : il a rendu la tete ENTIERE, mesuree sur la
        # forme du document. L'annoncer comme une troncature renverrait
        # l'appelant chercher la suite d une tete qui est deja finie -- c est
        # exactement le "il manque toujours des lignes" qu aucune annonce ne
        # doit laisser croire.
        if tete:
            annonce += " -- TETE COMPLETE (--tete " + tete + ")"
        else:
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


def forme_de_tete(lignes, extension):
    """La FORME de tete reconnue, ou "" si la forme est INCONNUE.

    Une forme inconnue ne se devine pas. Rendre le fichier entier en laissant
    croire que c est sa tete, c est le pire des deux mondes -- et la mesure le
    montre : sur un `.json`, `--tete auto` rendait le fichier ENTIER, et rien
    dans l annonce ne le disait puisque rien n avait ete tronque. Le nom de la
    forme est donc dit, y compris son absence.
    """
    if not lignes:
        return "vide"
    if front_matter_fini(lignes) >= 0:
        return "front-matter"
    if extension in (".md", ".markdown"):
        return "chapitre"
    if extension == ".py":
        if tete_docstring(lignes):
            return "docstring"
        return "declarations"
    return ""


def tranche_de_tete(texte, chemin_absolu, valeur):
    """(tranche, forme) : ce que vaut une demande de tete.

    `--tete auto` : la tete est SEMANTIQUE -- front matter et premier chapitre,
    ou docstring de module, ou declarations d ouverture. C est la forme qui
    supprime la DEVINE : on ne demande plus un nombre de lignes, on demande la
    tete, et l outil la mesure.
    `--tete <N>`   : les N premieres lignes, la forme historique, nommee comme
    telle pour ne pas confondre les deux lectures.

    Une FORME INCONNUE (un `.json`, un fichier sans marqueur) ne rend pas le
    fichier entier en silence : elle rend une tranche nommee et le DIT, car un
    appel qui croit avoir lu une tete a lu le fichier complet.
    """
    lignes = texte.splitlines()
    if not lignes:
        return "1:0", "vide"
    if valeur.strip().lower() == "auto":
        forme = forme_de_tete(lignes, chemin_absolu.suffix)
        if not forme:
            return "1:" + str(TETE_INCONNUE), "inconnue"
        return ("1:" + str(max(tete_automatique(lignes, chemin_absolu.suffix), 1)),
                forme)
    try:
        nombre = int(valeur.strip())
    except ValueError:
        raise ValueError("--tete attend 'auto' ou un nombre, pas : " + valeur)
    if nombre < 1:
        raise ValueError("--tete attend un nombre POSITIF, pas : " + valeur)
    return "1:" + str(nombre), "nombre"


def lire_fichier(chemin_relatif, tranche, avec_hash, inclure_prive=False, tete=""):
    """Lit UN fichier. Retourne code 0/1/2.

    `tete` prime sur `tranche` quand les deux sont demandes : c est la tete
    SEMANTIQUE qui a ete demandee, et deviner un nombre irait contre la demande.
    """
    if not dans_perimetre(chemin_relatif):
        print(motif_hors_perimetre(chemin_relatif, usage="lecture"))
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
    forme = ""
    if tete:
        try:
            tranche, forme = tranche_de_tete(texte, chemin_absolu, tete)
        except ValueError as e:
            print("REFUS : " + str(e))
            return 2
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
    return _afficher_resultat(chemin_relatif, lignes, total, lu, avec_hash,
                              chemin_absolu, bom, fins, tranche, tete, forme)


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
        print(motif_hors_perimetre(chemin_relatif, usage="lecture"))
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
