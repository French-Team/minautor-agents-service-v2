# purifier-rvav

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** Purifier
**Proprietaire :** Vulcain (outil partage)

## Pourquoi cet outil ?

Le protocole RVAV (etape 5 [purifier]) avait ete abandone pendant le
developpement et n etait plus a jour (decision utilisateur 2026-08-15). Besoins
listes par Buffy dans `spec-purification-rvav.md` : les `corrections.md` des
agents accumulent les lecons (janus 4735 lignes !) et `AGENTS-historique.md`
grossit sans fin.

**Principe anti-perte : on ne supprime JAMAIS d information.** Les lecons sont
la memoire des erreurs (anti-repetition). La purification DEPLACE les
lecons/entrees les plus anciennes vers un fichier d archive cote a cote, elle
ne tronque pas.

## Quotas par type

| Type | Quota (lignes) | Archive creee |
|---|---|---|
| `corrections.md` d agent | 1000 | `<agent>-historique.md` |
| `AGENTS-historique.md` | 800 | `AGENTS-historique-archive.md` |

Les fiches agents (template) et protocoles (documentaire) sont signales
seulement par detecter-surcharge-fichier : leur taille est structurelle, pas
une croissance.

## Usage

```bash
# Plan sans rien modifier (mode par defaut)
python3 purifier-rvav.py --tous --dry-run --rapport plan.md
python3 purifier-rvav.py --agent janus --dry-run

# Appliquer (TOUJOURS apres un dry-run valide)
python3 purifier-rvav.py --agent janus --executer
python3 purifier-rvav.py --fichier AGENTS-historique.md --executer

# Autres options
python3 purifier-rvav.py --tous --seuil 1500 --dry-run   # seuil personnalise
python3 purifier-rvav.py --version
```

## Options

| Option | Effet |
|---|---|
| `--tous` | Purifier tous les fichiers en surcharge (corrections.md des agents + AGENTS-historique.md) |
| `--agent <nom>` | Purifier les corrections.md d un agent |
| `--fichier <chemin>` | Purifier un fichier precis |
| `--seuil <n>` | Seuil de lignes (defaut 1000 corrections / 800 historique) |
| `--dry-run` | Mode par defaut : afficher le plan sans rien modifier |
| `--executer` | Appliquer reellement (TOUJOURS apres un dry-run valide) |
| `--rapport <fichier>` | Ecrire le plan de purification en markdown |
| `--verbose` | Detail par fichier |
| `--version` | Afficher la version |
| `--aide`, `-h` | Afficher cette aide |

## Comportement

1. Detecte les fichiers en surcharge (meme logique que detecter-surcharge-fichier)
2. Pour chaque fichier : calcule combien de blocs archiver pour repasser sous
   le quota (on archive TANT QUE le fichier reste au-dessus du seuil, en
   gardant toujours au moins un bloc)
3. Affiche le plan : fichier, lignes avant/apres, nb blocs a archiver, fichier
   d archive cree
4. `--executer` : deplace les blocs du HAUT (les plus anciens) vers l archive
5. **Accumulation anti-perte** : si l archive existe deja, les nouveaux blocs
   (plus anciens) sont PREFIXES devant le contenu existant (jamais ecrases)
6. **Garantie anti-perte** : l archive est ecrite EN PREMIER, le fichier
   principal ensuite (si l archive echoue, le principal reste intact)
7. Verifie apres : fichier principal sous le seuil, aucune perte (somme des
   blocs conservee), LF pur + ASCII strict

## Retour

- `0` : tout va bien (dry-run ou execute sans probleme)
- `1` : des fichiers restent en surcharge ou probleme
- `2` : usage invalide

## Connexions

- Protocole : `cerveau-projet/agents/regles-immuables/general/rvav-workflow.md`
  (etape 5 [purifier], mise a jour 2026-08-15)
- Spec des besoins : `cerveau-projet/agents/regles-immuables/general/spec-purification-rvav.md`
- Detecteur complementaire : `detecter-surcharge-fichier` (detecte, ne deplace pas)
