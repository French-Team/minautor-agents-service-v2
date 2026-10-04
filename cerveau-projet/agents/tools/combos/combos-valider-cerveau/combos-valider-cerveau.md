---
identite:
  type: outil
  appartient_a: commun
  commun: true
  combos:
    - combo-audit-themis
    - combo-controle-modification
    - combo-sante-tableaux
---
# combos-valider-cerveau

| Champ | Valeur |
|---|---|
| **Version** | 0.2.0 |
| **Statut** | prepare |
| **Categorie** | combos |
| **Derniere mise a jour** | 2026-08-06 |

---

## Description

Combo de validation du cerveau-projet : enchaine 3 validateurs et fusionne leurs
resultats en **un seul rapport combine** avec verdict global et code retour.

Les 3 validateurs couvrent 3 piliers independants :

1. **Philosophie** : `valider-relecture` -> la regle de relecture tient dans les 11 fiches + 11 corrections
2. **Structure** : `valider-cartes-decision` -> les 11 cartes sont conformes au format
3. **Purete** : `valider-conformite-ascii` -> 0 caractere non-ASCII dans le dossier cible
   (note : le dossier `exemples/` est volontairement EXCLU -- c'est la zone de test)

---

## Principe

1 commande -> 1 rapport -> 1 verdict global.

| | A la main | Avec le combo |
|---|---|---|
| Commandes | 3 a lancer, assembler soi-meme | 1 seule |
| Lecture | 3 sorties separees a comparer | 1 rapport structure |
| Verdict | A calculer soi-meme | Combine automatiquement + code retour |

---

## Utilisation

### CLI Python (version 0.2.0-py)

```
python3 combos-valider-cerveau.py [options]

Options :
  --detail      Afficher la sortie complete des 3 outils
  --stop        Arreter au premier echec
  --version     Afficher la version
```

### CLI bash (version originale)

```bash
bash combos-valider-cerveau.sh [dossier] [options]
```

| Argument | Description |
|---|---|
| `[dossier]` | Dossier a valider (defaut : `cerveau-projet/agents`) |
| `--detail` | Inclure la sortie complete des 3 outils, pas seulement le verdict |
| `--stop` | Arreter au premier echec (si la relecture casse, inutile de verifier l'ASCII) |
| `--help` | Afficher l'aide |

---

## Sortie

```
=== COMBO : Valider le cerveau ===
Date : 2026-08-06

--- 1/3 valider-relecture ---
[OK] 11/11 agents portent la regle de relecture

--- 2/3 valider-cartes-decision ---
[OK] 11/11 cartes conformes

--- 3/3 valider-conformite-ascii ---
[OK] 0 caractere non-ASCII

=== VERDICT GLOBAL ===
Relecture     : OK
Cartes        : OK
ASCII         : OK
RESULTAT      : CONFORME
Code retour   : 0
```

### Code retour

| Situation | Code retour |
|---|---|
| Les 3 outils passent | 0 |
| Au moins un echoue | 1 |

Le rapport indique **exactement lequel** a echoue : l'agent sait immediatement
quoi corriger sans relire tout le detail.

---

## Dependances

Les 3 outils appeles doivent exister :

| Outil | Chemin |
|---|---|
| `valider-relecture` | `valider/valider-relecture/valider-relecture.sh` |
| `valider-cartes-decision` | `valider/valider-cartes-decision/valider-cartes-decision.sh` |
| `valider-conformite-ascii` | `valider/valider-conformite-ascii/valider-conformite-ascii.sh` |

---

## Compatibilite

- Git Bash : uniquement `grep -oE` / sed BRE, **interdiction de `grep -P` et `\K`**
- ASCII strict : aucun caractere non-ASCII dans le script
- Retours codes 0/1 exploitables en chaine (combo dans combo)

---

## Assignation

| Agent | Mission |
|---|---|
| **Themis** | Audit general : verifier l'etat de sante du cerveau en 1 commande |
| **Janus** | Second controle : valider une modification avant de la declarer conforme |
| **Buffy** | Controler le cerveau-projet apres ses modifications |

---

## Versionning

| Version | Statut | Changements |
|---|---|---|
| 0.2.0-py | prepare | Version Python creee (orchestrateur subprocess des 3 validateurs, verdict combine, options --detail/--stop, base sur outil-template.py) |
| 0.1.0 | ebauche | Creation du combo : 3 validateurs, rapport combine, options --detail/--stop |
| 0.2.0 | prepare | Promotion apres tests reels : 3/3 OK, cas NON CONFORME detecte (code 1), integration index-tools + cartes Buffy/Themis/Janus |
