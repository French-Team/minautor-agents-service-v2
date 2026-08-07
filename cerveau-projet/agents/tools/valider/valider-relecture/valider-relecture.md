# valider-relecture

**Version :** 0.2.0-py
**Statut :** prepare
**Categorie :** Valider
**Chemin :** `agents/tools/valider/valider-relecture/`

## REGLE IMMUABLE : prefixe du dossier

> Le nom `valider-relecture` commence bien par le prefixe `valider-` de la categorie `valider/`.
> Controle au demarrage par le bloc `verifier_nommage`.

## REGLE IMMUABLE : compatibilite Git Bash (interdiction PCRE)

> L'outil n'utilise que `grep -qiE` (ERE compatible Git Bash). Aucun `grep -P`, aucun `\K`.
> Le script est en ASCII strict.

## Description

Verifie que **chaque agent du cerveau-projet porte la regle de relecture de sa fiche** :
quand un agent est active ou reactive, il doit relire SA fiche et SES corrections avant de continuer
(jamais celles des autres agents). L'outil controle les 2 fichiers de chaque agent :

1. La fiche `cerveau-projet/agents/[agent]/[agent].md` -- la regle dans la carte de decision
2. `cerveau-projet/agents/[agent]/corrections.md` -- la philosophie de relecture

Il ne modifie rien : il lit et verifie uniquement.

## Utilisation

```bash
# Verifier tous les agents
valider-relecture.sh

# Verifier un seul agent
valider-relecture.sh --agent buffy

# Avec le detail (numero de ligne des regles trouvees)
valider-relecture.sh --verbose
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--agent <nom>` | Verifier un seul agent | tous |
| `--verbose` | Afficher les numeros de ligne des regles trouvees | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. **[Lister]** - Parcourt les dossiers de `cerveau-projet/agents/` (exclusion : `tools/`)
2. **[Verifier]** - Controle la fiche `[agent].md` : mots-cles `RELECTURE`, `relis MA fiche`, `relire sa fiche`, `sa fiche et SES corrections`
3. **[Verifier]** - Controle `corrections.md` : mots-cles `Relire sa fiche`, `relecture`, `relis MA fiche`
4. **[Resumer]** - Compte les agents conformes / manquants
5. **[Decider]** - Code retour 0 si tout est conforme, 1 sinon

## Pourquoi des mots-cles multiples ?

Les fiches ont des formulations differentes de la regle (exemples reels) :

| Fiche | Formulation |
|---|---|
| cerberus.md | `REGLE ABSOLUE -- LECTURE` + `MA fiche et MES corrections` |
| buffy.md | `REGLE ABSOLUE -- RELECTURE` |
| corrections.md (tous) | `Relire sa fiche a chaque activation` |

L'outil reconnait les formulations equivalentes pour eviter les faux positifs.
Mots-cles couverts : `RELECTURE`, `relis MA fiche`, `relire sa fiche`, `sa fiche et SES corrections`, `MA fiche et MES corrections`, `relecture`.

## Exemples de sortie

```bash
$ valider-relecture.sh

=== valider-relecture ===
Agents : tous (dossier agents/)

[OK]     cerberus : fiche + corrections
[OK]     buffy    : fiche + corrections
[MANQUE] vulcain  : fiche=OK corrections=KO

=== Resume ===
Agents verifies : 11
Conformes : 10
[ERREUR] 1 agent(s) sans regle de relecture complete
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Apres modification de fiches agents** | Buffy verifie que la regle n'a pas ete cassee |
| **Controle d'une mission** | Janus l'utilise dans "Controler une modification" |
| **Audit du cerveau** | Avant de declarer le cerveau coherent |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `valider-nommage` | Verifie les noms des outils |
| `valider-cartes-decision` | Verifie les cartes des agents |
| `valider-conformite-ascii` | Verifie l'ASCII strict |

## Notes de creation

- [x] L'outil a ete teste en reel (cas conforme + cas manquant dans `exemples/`)
- [x] L'outil est conforme ASCII (aucun accent, aucun emoji) -- valide avec `valider-conformite-ascii`
- [x] L'outil est reference dans `index-tools.md`
- [x] L'outil est assigne a un agent dans sa carte de decision (protocole-outils Regle 6)
- [x] Le statut est passe de `ebauche` a `prepare` apres validation RVAV

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0 | 2026-08-06 | Creation : verification de la regle de relecture dans les fiches et corrections des agents |
