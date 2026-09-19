"""Fonctions simples de la categorie editer : une seule tache chacune."""
from commun import editer_atomique, lire_contenu_source, resoudre_chemin, verifier_ascii


def executer_editer(fichier, ancien, nouveau, ancien_fichier, nouveau_fichier):
    """Execute l'edition. Retourne code 0/1/2."""
    # Resout ancien
    try:
        if ancien_fichier:
            # ancien depuis fichier
            ancien_texte = lire_contenu_source("", ancien_fichier)
        elif ancien.startswith("@"):
            # @file anti-heredoc
            ancien_texte = lire_contenu_source(ancien, "")
        else:
            ancien_texte = ancien
    except (FileNotFoundError, ValueError, OSError) as e:
        print("REFUS : ancien : " + str(e))
        return 2

    # Resout nouveau (peut etre vide = suppression)
    try:
        if nouveau_fichier:
            nouveau_texte = lire_contenu_source("", nouveau_fichier)
        elif nouveau and nouveau.startswith("@") and nouveau.strip().startswith("@"):
            # Si nouveau est @file et pas un contenu commencant par @ voulu
            # Heuristique : si le fichier @ existe, on le lit, sinon on garde le texte tel quel
            try:
                nouveau_texte = lire_contenu_source(nouveau, "")
            except FileNotFoundError:
                nouveau_texte = nouveau
        else:
            nouveau_texte = nouveau
    except (FileNotFoundError, ValueError, OSError) as e:
        print("REFUS : nouveau : " + str(e))
        return 2

    if not ancien_texte:
        print("REFUS : --ancien vide (rien a remplacer).")
        return 2

    code, sha_avant, sha_apres, bak_path, msg_val = editer_atomique(fichier, ancien_texte, nouveau_texte)

    if code == 2:
        print(msg_val)
        return 2
    if sha_avant:
        print("SHA avant : " + sha_avant[:16] + "...")
    if sha_apres:
        print("SHA apres : " + sha_apres[:16] + "...")
    if bak_path:
        print("Backup : " + bak_path.name)
    try:
        chemin_abs = resoudre_chemin(fichier)
        nb, lignes = verifier_ascii(chemin_abs)
        if nb > 0:
            print("[ASCII] " + str(nb) + " non-ASCII lignes " + ",".join(str(x) for x in lignes[:5]) + ("..." if len(lignes) > 5 else ""))
        else:
            print("[ASCII] 0 non-ASCII")
    except (OSError, RuntimeError):
        pass
    print(msg_val)
    if code == 1:
        # EO-129 : meme contrat que `ecrire` -- l'echec de validation laisse la
        # cible INTACTE, il n'y a rien a reverts.
        print("REFUS (code 1) : RIEN n'a ete ecrit -- la cible est INTACTE"
              + (", .bak de la tentative : " + bak_path.name if bak_path else "") + ".")
        return 1
    print("OK : " + fichier + " edite (1 occurrence)")
    return 0
