# -*- coding: ascii -*-
# hook_tokens.py -- hook de comptage de tokens pour JARVIS
# Wrapppe l'execution de jarvis.py pour compter les tokens entree/sortie.
# Importable et utilisable par n'importe quel outil.
#
# Usage dans un outil :
#   from hook_tokens import hook_jarvis
#   result = hook_jarvis(cmd_args)
import sys
import time
from pathlib import Path


def _import_compteur():
    """Importe le module compteur (evite les imports circulaires)."""
    racine = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(racine / "cerveau-projet" / "freelance" / "tools-commun" / "compter" / "fonctions"))
    from compteur import Compteur, mesurer_entree, ecrire_etat, ajouter_ligne, lire_etat
    return Compteur, mesurer_entree, ecrire_etat, ajouter_ligne, lire_etat


def hook_jarvis(args, func_main):
    """Hook qui wrapppe func_main avec comptage de tokens.

    Args:
        args: arguments de la commande (pour le nom)
        func_main: fonction principale a executer (doit retourner un int)

    Returns:
        int: code de retour de func_main
    """
    Compteur, mesurer_entree, ecrire_etat, ajouter_ligne, lire_etat = _import_compteur()

    nom = "jarvis " + (args.commande if hasattr(args, 'commande') else " ".join(args) if args else "???")

    # --- AVANT ---
    c = Compteur()
    c.debut(nom)

    # --- EXECUTION ---
    try:
        rc = func_main()
    except SystemExit as e:
        rc = e.code if isinstance(e.code, int) else 1
    except Exception as e:
        print("[HOOK-TOKENS] Erreur: %s" % e)
        rc = 1

    # --- APRES ---
    c.fin()

    # Mettre a jour tokens-historique.md
    try:
        etat = lire_etat(c.racine)
        delta_e = c.fin_tokens - etat.get("entree", 0)
        ecrire_etat(c.racine, c.fin_tokens, etat.get("sortie", 0))
        ajouter_ligne(c.racine, c.fin_tokens, etat.get("sortie", 0),
                       delta_e, 0, nom)
    except Exception:
        pass

    # Afficher le bilan en mode verbose ou si delta significatif
    if c.delta() > 100:
        print("[HOOK-TOKENS] %s" % c.bilan())

    return rc


def hook_simple(nom, func):
    """Hook simple pour n'importe quelle fonction.

    Usage :
        from hook_tokens import hook_simple
        rc = hook_simple("mon_outil", lambda: mon_outil_main())

    Returns:
        int: code de retour
    """
    Compteur, mesurer_entree, ecrire_etat, ajouter_ligne, lire_etat = _import_compteur()

    c = Compteur()
    c.debut(nom)

    try:
        result = func()
        rc = result if isinstance(result, int) else 0
    except SystemExit as e:
        rc = e.code if isinstance(e.code, int) else 1
    except Exception as e:
        print("[HOOK-TOKENS] Erreur: %s" % e)
        rc = 1

    c.fin()

    try:
        etat = lire_etat(c.racine)
        delta_e = c.fin_tokens - etat.get("entree", 0)
        ecrire_etat(c.racine, c.fin_tokens, etat.get("sortie", 0))
        ajouter_ligne(c.racine, c.fin_tokens, etat.get("sortie", 0),
                       delta_e, 0, nom)
    except Exception:
        pass

    if c.delta() > 100:
        print("[HOOK-TOKENS] %s" % c.bilan())

    return rc
