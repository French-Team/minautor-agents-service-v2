# rappel

> "Quand tu corriges quelque part, il y a probablement ailleurs a corriger."

| Champ | Valeur |
|---|---|
| **Version** | 0.1.0 |
| **Type** | outil commun (P1/P10/D15) |
| **Proprietaire** | Forge |
| **Cree** | 2026-08-23 |

---

## Pourquoi

Les corrections appliquees dans UN fichier oublient souvent leurs soeurs :
le meme probleme existe ailleurs (autres corrections.md, le serveur miroir,
les templates, les conventions). Ce combo met l'agent sur la piste AVANT
qu'il ne clore.

## Contrat

```
python3 entry.py pour --contexte correction-regle
python3 entry.py lister
```

Retourne la liste des rappels pertinents. L'agent doit les SIGNALER dans
sa reponse (V1-V4) : "il y a probablement d'autres fichiers a corriger".

## Donnees (D15)

`rappels.json` : [{contexte, message}] - ajouter un rappel = editer le
JSON, jamais le code.

## Pratique generalisee

Tout agent qui applique une correction CONSULTE rappels pour son contexte
et mentionne les pistes dans sa reponse finale. A documenter dans le
protocole de correction et les templates.
