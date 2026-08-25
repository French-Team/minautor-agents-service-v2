# Verrou sur les outils

> Le verrou APPLIQUE. Le lecteur DECIDE.

| Champ | Valeur |
|---|---|
| **Version** | 0.1.0 |
| **Type** | outil v2 (D15 : code + donnees) |
| **Proprietaire** | Forge |
| **Cree** | 2026-08-23 |

---

## Description

Le verou controle l'acces a tout outil ou combo PROTEGE avant son usage.
Il fonctionne AVEC le lecteur-de-carte :

```
agent -> outil protege -> VERROU -> LECTEUR DE CARTE -> ACCEDE -> execution
                                                     -> REFUSE  -> blocage + trace
```

- Habilitation **exclusive** possible (ex: Vision seul sur JARVIS)
- Journal JSONL : TOUT acces trace (decision utilisateur 2026-08-23)

---

## Contrat

```
python3 entry.py controler --agent <agent> --cible <chemin|nom> [--type outil|combo]
python3 entry.py lister
```

- OUVERT (code 0) / REFUSE <raison> (code 1) / erreur (code 2)

## Integration

Tout outil/combo protege DOIT appeler le verrou AVANT de s'executer.
Un outil qui ne passe pas par le verrou = violation de perimetre
(signalee a Vision pour JARVIS, a Rogers pour les regles).

## Donnees (D15)

`verrous-data.json` :
- `journal` : nom du fichier journal JSONL
- `tracer` : "tout" | "refus" | "aucun"
- `proteges` : cible -> {niveau, habilite_unique?, habilites?}
  - cibles avec wildcard (`*`) supportees

Journal : `journal-acces.jsonl` (une ligne JSON par acces).
