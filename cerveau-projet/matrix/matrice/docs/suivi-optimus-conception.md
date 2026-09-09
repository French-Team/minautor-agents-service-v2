# CONCEPTION -- SUIVI-OPTIMUS (M-084 / E-054)

> VALIDEE par le createur (GO 2026-09-09) : construction livree -- outil
> `data/outils/suivi-optimus/` (noter/lire/verifier), trace
> `data/suivi-optimus.jsonl` (append-only + etalon SHA-256), encart
> `optimus` au journal multi-encarts, registre espion, zone
> `suivi-optimus` exclue du perimetre-cameleon (regle 9 de sa fiche).
> Contexte : optimus-prime est INVISIBLE dans la v3 (regle versions-intangibles,
> domicile `_operateur/` hors de la portee de la Matrice). Le createur veut le
> suivre en live. Cette trace note L'AGENT, pas les outils.

## 1. La trace

| Propriete | Choix |
|---|---|
| Fichier | `matrice/data/suivi-optimus.jsonl` (append-only, LF, une ligne par evenement) |
| Format ligne | JSON : `date`, `mission`, `theme`, `action`, `detail`, `fichiers[]`, `portes[]`, `duree_s` (optionnel) |
| Ecriture | via l'outil dedie SEUL (porte unique, jamais d'echo direct) ; empreinte SHA-256 (C-003) -> registre espion |
| Lecture | verbe `lire` a la demande + encart `optimus` au journal multi-encarts (8 dernieres, tableau Entree/Heure/Date + ligne Flux) |

## 2. Exemple de ligne

```json
{"date": "2026-09-09 10:05:12", "mission": "M-084", "theme": "SUIVI-OPTIMUS",
 "action": "decision", "detail": "format valide par le createur",
 "fichiers": [], "portes": ["ask_user"], "duree_s": null}
```

## 3. Ce qui declenche une entree (anti-bruit : par EVENEMENT, pas par fichier)

| Action | Exemple |
|---|---|
| `debut` / `fin` | debut de mission ; fin avec bilan |
| `porte` | fin du pilote, armer lot, consommer tresse, defcon monter/descendre, pause/reprise |
| `depot` | mission deposee au vrac (E-XXX) |
| `decision` | GO / arbitrage du createur |
| `decouverte` | constat d'audit interne (ex : E-057 angle mort) |
| `bilan` | bilan-periode demande et rendu |

PAS d'entree pour chaque fichier edite : le sac-a-dos (outils) et bdd-modifications
(fichiers) couvrent deja ce niveau. Doublon interdit.

## 4. Difference avec le sac-a-dos (pas de recouvrement)

| | sac-a-dos | suivi-optimus |
|---|---|---|
| Sujet | les OUTILS (invocations, codes, durees) | L'AGENT (decisions, pourquoi, mission) |
| Ecrit par | tout appel d'outil (automatique) | optimus lui-meme (conscient) |
| Granularite | par invocation | par evenement d'agent |

## 5. Etancheite

Le cameleon n'accede JAMAIS a cette trace (perimetre reducible de pause-session :
la zone `suivi-optimus` sera excluable ; regle gravee dans la fiche cameleon).

## 6. Outil prevu

`data/outils/suivi-optimus/` (ne du moule, sac-a-dos embarque) :
- `noter --mission M-XXX --action <enum> --detail "..." [--fichiers "a,b"] [--portes "a,b"] [--duree-s N]`
- `lire [--mission M] [--action a] [--n N]`
- `verifier`

## 7. Questions ouvertes pour le createur

1. Le format des champs convient-il (ajouter/retirer un champ) ?
2. La liste des evenements declencheurs convient-elle (trop / pas assez) ?
3. GO pour construire (outil + encart + raccords) ?
