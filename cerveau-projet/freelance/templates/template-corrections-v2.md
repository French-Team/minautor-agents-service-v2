---
identite:
  nom: <NomMarvel>
  version: 0.1.0
  type: corrections
  appartient_a: <agent>
  commun: false
  mot-cles: ["<agent>", "corrections", "<domaine>", "v2", "marvel"]
---
# Corrections -- <NomMarvel>

> Fenetre glissante des lecons et corrections de <NomMarvel>.
> Cree le YYYY-MM-DD. Aucune correction a ce jour.

## Contexte de creation

- **Role** : <Role de l'agent> (freelance).
- **Univers** : MARVEL -- <Personnage> (<Serie/Film>).
- **Mode conversation** : Stark active -> l'utilisateur guide ->
  FIN DE CYCLE -> retour a Stark (via JARVIS).
- **Perimetre** : <Domaine d'action dans freelance/>.
- **Predecesseurs v1** : <Agents v1 qui avaient un role similaire>.

---

## REGLES -- Regles specifiques

| Regle | Description |
|---|---|
| **<REGLE1>** | <Description> |
| **FIN DE CYCLE** | retour a Stark via JARVIS |

---

## PHILOSOPHIE

- <Principe de comportement 1>
- <Principe de comportement 2>

---

## LECONS

Aucune lecon a ce jour.


---

## REGLE RAPPEL (protocole 20)

Apres avoir enregistre une lecon ou corrige une erreur, consulter :
    python3 tools-commun/rappel/entry.py pour --contexte correction-regle
et SIGNALER dans la reponse les autres fichiers probablement concernes.
