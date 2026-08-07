# valider-numerotation

| Champ | Valeur |
|---|---|
| **Version** | 0.2.0-py |
| **Statut** | prepare |
| **Categorie** | valider |
| **Derniere mise a jour** | 2026-08-06 |

---

## Description

Verifie que les tableaux d'etapes de mission des fiches agents n'ont pas de
**doublons de numerotation** (etape X x2).

Une mission avec une etape dupliquee (ex : deux "etape 5") peut faire sauter
une etape a l'agent qui la lit, ou lui faire executer la meme action deux fois.
Cet outil detecte ce defaut silencieux.

---

## Utilisation

```bash
bash valider-numerotation.sh [OPTIONS] [FICHIER|DOSSIER]
```

| Argument | Description |
|---|---|
| `[FICHIER]` | Verifier un fichier fiche agent (ex: `buffy.md`) |
| `[DOSSIER]` | Verifier toutes les fiches d'un dossier (defaut : `agents/`) |

| Option | Description |
|---|---|
| `--agent <nom>` | Verifier un seul agent (ex: `--agent buffy`) |
| `--verbose` | Afficher les missions sans doublon |
| `--help` | Afficher l'aide |

---

## Logique de detection

L'outil parse chaque fiche agent et isole les tableaux d'etapes de mission :

1. **Repere les sections** `### Mission : <nom>` dans la fiche
2. **Detecte le tableau d'etapes** par son en-tete `| Etape | Action |`
3. **Compte les numeros** dans chaque tableau (formats `| 5 |` et `| **5** |`)
4. **Signale tout numero present plus d'une fois** dans la meme mission

Les numeros des autres tableaux (RVAV, points de controle, verdicts) sont
exclus : seuls les tableaux d'etapes de mission sont analyses.

---

## Sortie

```
=== valider-numerotation v0.1.0 ===
Cible : .../cerveau-projet/agents

[OK] cerberus
[OK] buffy
[DOUBLON] janus
    - Controler une modification : etape 8 x2
[OK] vulcain
---
Fichiers analyses : 11 | Doublons detectes : 1
=== Resultat : DOUBLONS DETECTES ===
```

### Code retour

| Situation | Code retour |
|---|---|
| Aucun doublon | 0 |
| Au moins un doublon | 1 |

---

## Compatibilite

- Git Bash : la detection se fait en Python (regex fiable), le script bash
  embarque le code via heredoc -- aucune dependance `grep -P` ou `\K`
- ASCII strict : aucun caractere non-ASCII dans le script
- Retours codes 0/1 exploitables en chaine (combo dans combo)

---

## Assignation

| Agent | Mission |
|---|---|
| **Buffy** | Controler le cerveau-projet : verifier les fiches agents apres ses modifications |
| **Janus** | Second controle : verifier qu'une modification de fiche n'a pas introduit de doublon |
| **Themis** | Audit general : inclure la verification des doublons dans son evaluation |

---

## Versionning

| Version | Statut | Changements |
|---|---|---|
| 0.1.0 | ebauche | Creation : detection des doublons d'etapes dans les tableaux de mission des fiches agents |
| 0.2.0 | prepare | Promotion apres tests reels : 11/11 fiches conformes, cas doublon detecte (etape 2 x2, code 1), bug chemin RACINE corrige, --agent corrige |
