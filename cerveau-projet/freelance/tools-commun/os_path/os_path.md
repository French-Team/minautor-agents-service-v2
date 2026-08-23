# os_path

> "Le chemin juste, au bon niveau, du premier coup."

| Champ | Valeur |
|---|---|
| **Version** | 0.1.0 |
| **Type** | outil commun (P1 : entry.py + fonctions/) |
| **Proprietaire** | Forge |
| **Cree** | 2026-08-23 |

---

## Pourquoi

Les bugs de resolution de chemin sont recurrents : chaque outil recalculait
sa racine avec des `"../.."` comptes a la main -> 4 bugs de niveau le seul
2026-08-23. `os_path` centralise et FIABILISE.

## Les 3 fonctions

| Fonction | Role |
|---|---|
| `racine()` | DETECTE la racine en remontant depuis le fichier appelant jusqu'a trouver `AGENTS.md`. Ne compte jamais les niveaux. |
| `resoudre(chemin)` | Chemin relatif -> absolu. Refus hors workspace. |
| `localiser(nom)` | Retrouve un fichier par nom dans tout le workspace. |

## Contrat

```
python3 entry.py racine
python3 entry.py resoudre <chemin-relatif>
python3 entry.py existe   <chemin-relatif>
python3 entry.py localiser <nom-fichier>
```

Depuis Python :
```python
from racine import trouver_racine
from resoudre import resoudre, existe
from localiser import localiser
```

## Roadmap

- v0.2.0 : `resoudre_robuste` -- si introuvable, retente automatiquement
  depuis la racine, le cwd, puis chaque niveau parent (idee utilisateur)
- roadmap : wrapper d'execution qui relance une commande avec le chemin corrige
