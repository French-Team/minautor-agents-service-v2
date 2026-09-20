# CONCEPTION -- SUIVI-OPTIMUS (M-084 / E-054)

> VALIDEE par le createur (GO 2026-09-09) : construction livree -- outil
> `data/outils/suivi-optimus/` (noter/lire/vue/verifier), trace
> `data/suivi-optimus.jsonl` (append-only + etalon SHA-256), vue markdown
> dediee `matrice/suivi-optimus.md` (tableaux par action), registre espion,
> zones `suivi-optimus` + `suivi-optimus.md` exclues du perimetre-cameleon
> (regle 9 de sa fiche).
> EVOLUTION 2026-09-09 (decision createur) : optimus n'a PLUS d'encart au
> journal multi-encarts -- il reste INVISIBLE, SON fichier dedie est la
> seule vue de son travail.
> Contexte : optimus-prime est INVISIBLE dans la v3 (regle versions-intangibles,
> domicile `_operateur/` hors de la portee de la Matrice). Le createur veut le
> suivre en live. Cette trace note L'AGENT, pas les outils.

## 1. La trace

| Propriete | Choix |
|---|---|
| Fichier | `matrice/data/suivi-optimus.jsonl` (append-only, LF, une ligne par evenement) |
| Format ligne | JSON : `date`, `mission`, `theme`, `action`, `detail`, `fichiers[]`, `portes[]`, `duree_s` (optionnel) |
| Ecriture | via l'outil dedie SEUL (porte unique, jamais d'echo direct) ; empreinte SHA-256 (CV-003) -> registre espion |
| Lecture | verbe `lire` a la demande + verbe `vue` qui genere `matrice/suivi-optimus.md` (fichier dedie, UN TABLEAU PAR ACTION) -- PAS d'encart au journal multi-encarts (invisibilite) |

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
les zones de la trace, de l'outil et de la vue sont EXCLUES du perimetre-cameleon ;
regle gravee dans la fiche cameleon, regle 9).

> AUDIT PROTECTIONS 2026-09-09 (decision createur) : la cle `perimetre-cameleon`
> du classeur ne porte PLUS les noms revelateurs -- une zone NEUTRE `maintenance`
> est resolue vers les chemins reels par `pause-session/lire_perimetre` (chemins
> listes dans `CHEMINS_MAINTENANCE`, constants.py de pause-session). Les sorties
> console de la Matrice (machine-defcon, pause-session, pilote, verifier-*) sont
> neutralisees : terme "maintenance" uniquement, jamais le nom interne. Bug
> attrape en reel : `bdd-variables lire` plantait (KeyError) sur l'entree
> perimetre-cameleon sans champ `id` -- corrige (defaut V-???).

## 5bis. Philosophie d'invisibilite (CV-006 / L-016, decision createur 2026-09-09)

Si optimus est invisible aux yeux du cameleon, il ne doit JAMAIS etre nomme
(nom, domicile, trace, zone exclue) dans CE QUE LE CAMELEON LIT : fiche,
personnalites (vivier), lecons injectees, marbre (regles/conventions/protocoles),
injection (objectif, checklist, themes). Tout contenu valide passe un AUDIT
avant validation. Attrape en reel (2026-09-09) : fiche cameleon (3 mentions),
TH-012, TH-021, R-002, L-016 -- corriges via les portes `modifier` ajoutees
(bdd-regles-matrice, theme-vivier, bdd-lecons). Perimetre-cameleon etendu a
toutes les zones internes revelatrices (archives pilote, modifications, usages,
activites, journal multi-encarts, intercom, routines, docs, outils internes,
_operateur).

## 6. Outil prevu

`data/outils/suivi-optimus/` (ne du moule, sac-a-dos embarque) :
- `noter --mission M-XXX --action <enum> --detail "..." [--fichiers "a,b"] [--portes "a,b"] [--duree-s N]`
- `lire [--mission M] [--action a] [--n N]`
- `verifier`

## 7. Questions ouvertes pour le createur

1. Le format des champs convient-il (ajouter/retirer un champ) ?
2. La liste des evenements declencheurs convient-elle (trop / pas assez) ?
3. GO pour construire (outil + encart + raccords) ?
