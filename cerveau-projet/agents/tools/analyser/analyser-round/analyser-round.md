---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# analyser-round

**Categorie** : Analyser
**Version** : 0.1.0
**Statut** : ebauche

---

## Objectif

Resumer l activite d un "round" de travail (fenetre de temps) a partir des
traces du cerveau-projet : agents actives, outils utilises, tests lances et
duree totale. C est la base des futurs indicateurs de productivite d un round.

Un round = la periode pendant laquelle Cerberus active des agents qui
utilisent des outils et lancent des tests, jusqu au retour au point d entree.

---

## Pourquoi cet outil ?

- Les registres (usages d outils, lancements de tests) accumulent la matiere
  premiere, mais rien ne la CROISE pour repondre "qui a travaille, avec quoi,
  combien de temps ?".
- Alimente la future evaluation par grade (novice/acquis/professionnel/senior)
  annoncee : la frequence et la diversite d usage des outils sont des criteres.

---

## Utilisation

```bash
# Round des 60 dernieres minutes (defaut)
python3 analyser-round.py

# Fenetre plus courte (un round precis)
python3 analyser-round.py --fenetre-minutes 30

# Rapport markdown
python3 analyser-round.py --rapport rapport-round.md

# Version
python3 analyser-round.py --version
```

## Options

| Option | Description |
|---|---|
| `--fenetre-minutes <N>` | Fenetre du round (defaut 60 min) |
| `--rapport <f>` | Ecrit le rapport markdown |
| `--verbose` | Detail : outils par agent, tests par agent |
| `--dry-run` | Affiche sans ecrire le rapport |
| `--no-chrono` | Coupe le chrono de l outil |
| `--version` | Affiche la version |

---

## Sources (lecture seule)

- `traces/registre-usages-outils.jsonl` : (date, agent, outil, mode)
- `traces/registre-tests.jsonl` : (date, agent, test, verdict, duree)

Aucune de ces sources n est modifiee : l outil est en lecture seule.

---

## Sortie

```
=== ANALYSE DU ROUND (fenetre 60 min) ===
Derniere activite : 2026-08-17 19:45:00
Agents actives : 3
Usages d outils : 21 (14 outils distincts)
Tests lances : 86 (duree totale 137.8 s)

=== OUTILS PAR AGENT ===
...
```

---

## Historique

| Version | Date | Description |
|---|---|---|
| 0.1.0 | 2026-08-17 | Creation : croisement registres usages/tests sur une fenetre, rapport markdown |
