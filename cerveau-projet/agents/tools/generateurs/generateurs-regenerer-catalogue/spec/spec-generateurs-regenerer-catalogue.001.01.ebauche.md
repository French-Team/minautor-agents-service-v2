---
# Spec: regenerer-catalogue
# Version : 1.0.0
# Statut : ebauche

spec:
  nom: "spec-regenerer-catalogue"
  version: "1.0.0"
  statut: "ebauche"
  classe: "01"
  numero: "01"
  domaine: "outil"
  concerne: "generateurs/generateurs-regenerer-catalogue"
  date: "2026-08-08"
  auteur: "Vulcain"
---

# Spec generateurs-regenerer-catalogue v1.0.0

## Objectif

Regenerer / synchroniser le fichier derive `catalogue-commandes.json` du
generateur de commandes a partir des outils reels de `agents/tools/`, avec
des descriptions fiables extraites de l'en-tete des `.py` (2 formats).

## Contexte

- La regeneration piste A a utilise un script temporaire qui a capture des
  fragments d'aide comme descriptions (63 cosmetiques sur 105).
- Le catalogue est un fichier **derive** : il doit etre regenerable par script.
- Lecon incident piste B : garder le script de generation des fichiers derives.
- Les 13 commandes originales ne sont jamais regenerees (preservees intactes).

## Exigences

### E1. Scan des outils reels

- Parcourt `cerveau-projet/agents/tools/<cat>/<outil>/<outil>.py`.
- Exclusions : `tester/`, `combos/`, `templates/`, `spec/`, `outil-template`,
  `regenerer-catalogue` (auto-exclusion).

### E2. Preserver les commandes existantes

- Mode defaut (synchronisation) : les entrees deja presentes dans le catalogue
  sont **preservees** (descriptions corrigees intactes).
- Les 13 commandes originales ne sont jamais regenerees.
- `--force` : reconstruction complete (originales + speciales + outils).

### E3. Descriptions depuis l'en-tete des .py

- Format A (docstring) : `"""` / `nom.py` / `Description` / `"""`.
- Format B (commentaires) : `# nom.py` puis `# Description` (outils convertis).
- Jointure des lignes consecutives (phrases coupees par `:` ou `,`).
- Translitteration ASCII (NFKD), limite ~90 caracteres.

### E4. Modeles et parametres

- Parsing de l'aide (`--aide`) : `usage:` + continuation stricte + filtrage du
  nom du script + flags entre crochets.
- Entrees speciales manuelles : `generateurs-carte`, `combos-moteur`,
  `verifier-restauration-sure`.

### E5. Ecriture

- Indentation 2 espaces, **CRLF uniforme** (normaliser LF en memoire, reecrire
  CRLF - piege des CRLF parasites).
- JSON valide, ASCII strict.

### E6. Securite

- JAMAIS `git checkout`/`restore`/`reset --hard` sur fichier non commite.
- Dry-run obligatoire avant application.

## Criteres de validation

| # | Critere | Methode |
|---|---|---|
| V1 | 0 regression sur catalogue existant | dry-run : 0 outil a ajouter |
| V2 | Description correcte pour les 2 formats | extraction sur echantillon (docstring + commentaires) |
| V3 | JSON valide apres ecriture | json.load |
| V4 | ASCII 0 | valider-conformite-ascii |
| V5 | CRLF uniforme | comptage LF = CR = CRLF |
| V6 | Non-regression generateur | generateurs-commande --liste + generation reelle |
