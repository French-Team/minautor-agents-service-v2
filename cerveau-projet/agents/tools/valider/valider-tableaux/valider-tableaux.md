---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# valider-tableaux
# Verifie la coherence des tableaux des fiches agents

**Categorie** : Valider
**Version** : 0.2.0-py
**Statut** : prepare
**Proprietaire** : Vulcain (outil partage)

---

## Objectif

Verifier automatiquement la coherence des tableaux des fiches agents, en 3 points :

1. **Nombres annonces vs lignes reelles** : chaque mission du tableau "Missions disponibles" annonce un nombre d'etapes ("X etapes") qui doit correspondre exactement au nombre de lignes de la section "### Mission : ..." correspondante.
2. **Numerotation continue** : les tableaux numerotes (etapes de mission, points de controle, etc.) doivent etre numerotes 1..N sans doublon ni trou.
3. **Completude des listes** : le tableau "Agents disponibles" de Cerberus doit lister TOUS les agents du projet (dossiers agents/ contenant une fiche), sans agent fantome.

---

## Utilisation

```bash
valider-tableaux.sh [OPTIONS] [FICHIER|DOSSIER]
```

### Arguments

| Argument | Description |
|---|---|
| `[FICHIER]` | Verifier un fichier fiche agent (ex : `buffy.md`) |
| `[DOSSIER]` | Verifier toutes les fiches d'un dossier (defaut : `agents/`) |

### Options

| Option | Description |
|---|---|
| `--agent <nom>` | Verifier la fiche d'un agent precis |
| `--detail` | Afficher le detail complet des verifications |
| `--help` | Afficher l'aide |

---

## Ce que l'outil verifie

### 1. Nombres annonces vs lignes reelles

Pour chaque fiche, l'outil :
- Lit le tableau "Missions disponibles" et extrait chaque mission avec son nombre annonce
- Trouve la section "### Mission : X" correspondante (nom exact ou nom + suffixe "(activer Y)")
- Compte les lignes d'etapes (numeros 1..N et lignes FIN/`**FIN**`)
- Compare : annonce == reel ?

**Erreur signalee** si un nombre annonce ne correspond pas, ou si une mission annoncee n'a aucune section.

### 2. Numerotation continue

Pour chaque tableau dont la premiere colonne contient des numeros :
- **Doublons** : un numero present plusieurs fois est signale ("numero N en double")
- **Trous** : si la sequence commence a 1, tout numero manquant entre 1 et le max est signale

### 3. Completude des listes d'agents

Pour la fiche de Cerberus uniquement :
- La liste "Agents disponibles" est comparee aux dossiers `agents/*/` contenant une fiche `X.md`
- **Agents absents** : un agent existant mais non liste est signale
- **Agents fantomes** : un agent liste mais sans dossier/fiche est signale

> Note : Cerberus ne se liste pas lui-meme (il est le coordinateur) -- c'est l'attendu, pas une erreur.

---

## Code retour

| Code | Signification |
|---|---|
| **0** | CONFORME -- aucun probleme |
| **1** | NON CONFORME -- au moins un probleme detecte |

---

## Exemples

### Verifier toutes les fiches agents

```bash
valider-tableaux.sh
```

Sortie :
```
=== valider-tableaux : rapport ===
Fichiers analyses : 11 | Conformes : 11 | Problemes : 0

=== Resultat : CONFORME ===
```

### Verifier une fiche precise

```bash
valider-tableaux.sh --agent buffy
```

### Verifier un fichier dans exemples/ (cas d'erreur)

```bash
valider-tableaux.sh exemples/test-tableaux/faux-agent/faux-agent.md
```

---

## Regles

1. **Prefixe dossier** : le nom commence par `valider-` (dossier valider/)
2. **ASCII strict** : aucun caractere non-ASCII dans le script ou la doc
3. **Git Bash** : pas de `grep -P` ni `\K` (incompatibles) -- parsing Python
4. **Python requis** : detection du systeme via `verifier-systeme` avant usage

---

## Dependances

| Outil | Usage | Statut |
|---|---|---|
| `verifier-systeme` | Verifier que Python est disponible | Cree |
| `valider-numerotation` | Complement : doublons dans les seuls tableaux d'etapes de mission | Cree |

> **Complementarite** : `valider-numerotation` se concentre sur les doublons d'etapes des missions.
> `valider-tableaux` va plus loin : nombres annonces vs lignes reelles, trous de numerotation,
> et completude des listes d'agents. Les deux peuvent etre lances separement ou via un combo.

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0 | 2026-08-07 | Creation : 3 verifications (nombres annonces, numerotation, completude) |
| 0.2.0-py | 2026-08-07 | Portage Python : version autonome (meme logique que le .sh) |

---
