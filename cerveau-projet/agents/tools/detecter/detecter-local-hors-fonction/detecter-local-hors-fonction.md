---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# detecter-local-hors-fonction

**Categorie** : Detecter
**Version** : 0.2.0
**Statut** : prepare
**Date creation** : 2026-08-07
**Proprietaire** : Vulcain (outil partage)

---

## Description

Detecte les declarations `local` utilisees **hors d'une fonction** dans les scripts bash.

**Pourquoi cet outil ?**
- En bash, `local` hors fonction provoque l'erreur `local: can only be used in a function`
- Cette erreur est cosmetique (le script continue) mais pollue la sortie et masque les vraies erreurs
- Un bug de ce type a ete detecte dans `valider-nommage.sh` (lignes 250-251) lors d'un audit
- Cet outil rend la detection **permanente** : il peut etre lance regulierement pour prevenir la reapparition

**Principe du parseur (brace-tracking)**
- Suit les definitions de fonctions (`name() {` ou `function name {`)
- Suit la profondeur d'accolades `{}`
- Signale toute declaration `local` qui se trouve a la profondeur hors fonction

---

## Utilisation

```bash
# Analyser un fichier
detecter-local-hors-fonction.sh outil.sh

# Analyser tous les .sh d'un dossier (recursif)
detecter-local-hors-fonction.sh --recursive cerveau-projet/agents/tools

# Version Python (recommandee)
python3 detecter-local-hors-fonction.py outil.sh
python3 detecter-local-hors-fonction.py --recursive cerveau-projet/agents/tools

# Options
detecter-local-hors-fonction.sh --aide
detecter-local-hors-fonction.sh --version
```

### Options

| Option | Description |
|---|---|
| `[CHEMIN]` | Fichier .sh ou dossier a analyser (defaut: `cerveau-projet/agents/tools`) |
| `--recursive, -r` | Scanner toute une arborescence |
| `--verbose, -v` | Afficher les details de scan |
| `--version` | Afficher la version |
| `--aide, -h` | Afficher l'aide |

---

## Resultat

Pour chaque fichier contenant des `local` hors fonction :
- Chemin du fichier
- Numero de ligne + contenu de chaque declaration fautive

En fin d'execution :
- Resume : Total / OK / Fichiers avec probleme
- Retour : `0` si conforme, `1` si des `local` hors fonction sont detectes

**Exemple de sortie :**
```
=== Resume ===
  Total : 81
  OK : 81
  Fichiers avec 'local' hors fonction : 0
[OK] Aucun 'local' hors fonction
```

---

## Notes

- **Dependance** : Python (3+). Le parseur est ecrit en Python pour une analyse fiable du brace-tracking.
- **Perimetre** : uniquement les fichiers `.sh` (scripts bash). Les `.md`, `.py` et autres ne sont pas analyses.
- **Fichier unique** : si le chemin est un fichier, il est analyse directement.
- **Dossier** : si le chemin est un dossier, tous les `.sh` de l'arborescence sont analyses (recursif).
- **Git Bash** : le script ne contient aucun `grep -P` ni `\K` (regle immuable de compatibilite Git Bash).
- **ASCII** : le script et cette documentation respectent la regle ASCII stricte.

---

## Liens

- [convention-outils-agents.md](../../../../pense-betes/conventions/outils/convention-outils-agents.md)
- [protocole-outils](../../../../pense-betes/regles-immuables/general/protocole-outils/protocole-outils.001.01.ebauche.md)
- [regles-emojis-ascii.md](../../../../pense-betes/regles-immuables/general/regles-emojis-ascii.md)

---

## Versionning

| Date | Version | Auteur | Description |
|---|---|---|---|
| 2026-08-07 | 0.2.0 | Vulcain | Creation de l'outil (detection des `local` hors fonction) |
| 2026-08-07 | 0.2.0-py | Vulcain | Version Python creee (parseur direct, plus de heredoc) |
