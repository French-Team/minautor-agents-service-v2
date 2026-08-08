---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# nettoyer-sessions

**Version :** 0.1.0
**Statut :** prepare
**Categorie :** nettoyer
**Chemin :** `agents/tools/nettoyer/nettoyer-sessions/`
**Proprietaire :** Vulcain (outil partage)

---

## Objectif

Supprimer TOUTES les sessions LLM existantes (etats actifs uniquement) avant
une re-identification a neuf.

**Pourquoi cet outil ?**
- L'utilisateur peut vouloir repartir de zero : `nettoyer la session existante`
- Les sessions s'accumulent (sessions fantomes, collisions entre LLM)
- Apres nettoyage, le LLM s'identifie a neuf (`sidentifier`) et redevient Cerberus

**Perimetre (decision utilisateur) : etats actifs uniquement.**
- AGENTS.md : blocs `### Session : session-llm-N` + section `## Sessions connues`
- Classeur-variables : lignes `profil-session-*`
- **AGENTS-historique.md (le journal) n'est JAMAIS modifie** : c'est un temoignage,
  les traces et l'historique sont conserves

---

## Utilisation

Version Python (recommandee) :

```bash
python3 nettoyer-sessions.py [--dry-run] [--verbose]
```

Version bash equivalente : `nettoyer-sessions.sh` (meme logique).

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `--dry-run` | flag | Non | Afficher ce qui serait supprime sans ecrire |
| `--verbose` | flag | Non | Afficher les details |
| `--version` | flag | Non | Afficher la version |
| `--aide` / `-h` | flag | Non | Afficher l'aide |

**Variables d'environnement (tests sur copies, JAMAIS les vrais fichiers) :**

| Variable | Defaut | Description |
|---|---|---|
| `AGENTS_FILE` | `AGENTS.md` | Surcharger le chemin de AGENTS.md |
| `CLASSEUR_STOCKAGE` | `cerveau-projet/agents/classeur-variables/stockage/variables-actuelles.md` | Surcharger le chemin du classeur |

---

## Ce que fait l'outil

### 1. AGENTS.md

Supprime, en PRESERVANT le frontmatter `identite:` et le reste du fichier :
- tous les blocs `### Session : session-llm-N` (section `## Sessions LLM`)
- la section `## Sessions connues` (la table `| Session | Nom LLM | ... |`)

### 2. Classeur-variables

Supprime toutes les lignes `profil-session-*` (les variables de profil de session).

### 3. Jamais modifie

- `AGENTS-historique.md` (le journal d'activation : traces et temoignages)
- le frontmatter, l'entete et les sections non-session de AGENTS.md
- les autres variables du classeur

---

## Exemple

### Nettoyage complet (apres la phrase utilisateur `nettoyer la session existante`)

```bash
python3 nettoyer-sessions.py
```

Sortie :

```
AGENTS.md : 55 lignes supprimees (blocs session + Sessions connues)
Classeur : 5 lignes profil-session supprimees
Nettoyage termine : 60 lignes supprimees
```

### Verifier d'abord (dry-run)

```bash
python3 nettoyer-sessions.py --dry-run
```

### Test sur copies (ne jamais toucher les vrais fichiers)

```bash
AGENTS_FILE=/tmp/test/AGENTS.md CLASSEUR_STOCKAGE=/tmp/test/variables-actuelles.md \
  python3 nettoyer-sessions.py
```

---

## Idempotence

L'outil est idempotent : un second passage sans session existante ne supprime
rien et retourne `code 0` (les sections absentes ne sont pas recreees).

---

## Dependances

- Aucune dependance externe (stdlib Python / bash)

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-08 | Creation initiale : supprime les blocs session-llm + Sessions connues (AGENTS.md) et les lignes profil-session-* (classeur), preserve le frontmatter et le journal historique. Parite py/sh, --dry-run, --verbose |
