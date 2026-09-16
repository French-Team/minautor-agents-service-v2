"""Fonctions simples de la categorie ecrire : une seule tache chacune.

Atomique, LF, .bak, SHA, validation, BDD-ready.
"""
from commun import (
    ecrire_atomique,
    lire_contenu_source,
    verifier_ascii,
)


def executer_ecrire(fichier, contenu, contenu_fichier, mode):
    """Execute l'ecriture. Retourne code 0/1/2."""
    try:
        texte_source = lire_contenu_source(contenu, contenu_fichier)
    except (FileNotFoundError, ValueError, OSError) as e:
        print("REFUS : " + str(e))
        return 2
    except UnicodeDecodeError as e:
        print("REFUS : source non-UTF8 : " + str(e))
        return 1

    code, sha_avant, sha_apres, bak_path, msg_val = ecrire_atomique(fichier, texte_source, mode)

    if code == 2:
        print(msg_val)
        return 2
    # Succes ou validation echouee mais ecrit
    if sha_avant:
        print("SHA avant : " + sha_avant[:16] + "...")
    else:
        print("SHA avant : (nouveau fichier)")
    if sha_apres:
        print("SHA apres : " + sha_apres[:16] + "...")
    if bak_path:
        print("Backup : " + bak_path.name)
    # ASCII
    try:
        from commun import resoudre_chemin
        chemin_abs = resoudre_chemin(fichier)
        nb, lignes = verifier_ascii(chemin_abs)
        if nb > 0:
            print("[ASCII] " + str(nb) + " caracteres non-ASCII en lignes " + ",".join(str(x) for x in lignes[:5]) + ("..." if len(lignes) > 5 else ""))
        else:
            print("[ASCII] 0 non-ASCII")
    except (OSError, RuntimeError):
        pass
    print(msg_val)
    if code == 1:
        print("ALERTE : validation echouee -- backup disponible pour revert (code 1, fichier ecrit).")
        return 1
    print("OK : " + fichier + " [" + mode + "]")
    return 0
