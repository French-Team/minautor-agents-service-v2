# Lecteur de carte

> "Ta carte, s'il te plait." -- Controle d'acces de la securite v2.

| Champ | Valeur |
|---|---|
| **Version** | 0.1.0 |
| **Type** | outil v2 (D15 : code + donnees) |
| **Proprietaire** | Forge |
| **Cree** | 2026-08-23 |

---

## Description

Le lecteur de carte verifie si un agent est HABILITE a utiliser un outil
ou un combo. Il DECIDE (ACCEDE / REFUSE) ; le verrou APPLIQUE.

**Politique** : tout agent non liste dans `cartes-data.json` est REFUSE
(politique_defaut = refuser).

---

## Contrat

```
python3 entry.py verifier --agent <agent> --cible <nom> [--type outil|combo]
python3 entry.py lister   --agent <agent>
```

- Sortie ACCEDE (code 0) ou REFUSE <raison> (code 1)
- Erreur de donnees : code 2

## Donnees (D15)

`cartes-data.json` :
- `politique_defaut` : "refuser"
- `agents.<agent>.outils` : liste des outils autorises (`*`, `prefixe*`, `*contient*`)
- `agents.<agent>.combos` : liste des combos autorises

Editer ce fichier suffit pour changer une habilitation : AUCUNE modification
de code necessaire.

## Integration

Utilise par `verrou-outils/` qui l'interroge a chaque acces a un outil
protege. Ne pas appeler directement depuis un arbre : passer par le verrou.
