"""Indexer : rebuild index de recherche (palier 2 futur : FTS5)."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def indexer(arguments):
    """Verbe indexer : rebuild l'index de recherche (palier 2 futur).
    
    Pour l'instant (palier 1), c'est un stub qui indique que le scan
    JSON est suffisant. Le FTS5 sera active par auto-evolution.
    
    Codes retour :
      0 = succes (index reconstruit ou palier 1 = pas besoin)
      1 = erreur
    """
    print("INDEXER : palier 1 actif (scan JSON, pas de FTS5)")
    print("Le moteur de recherche fonctionne sans index SQLite.")
    print("Palier 2 (FTS5) sera active par auto-evolution quand")
    print("la friction 3/3 sera atteinte (lenteur scan sur grosses BDD).")
    print("")
    print("Pour l'instant, 'rechercher --requete <texte> --dans bdd'")
    print("fonctionne directement via scan JSON deterministe.")
    return 0
