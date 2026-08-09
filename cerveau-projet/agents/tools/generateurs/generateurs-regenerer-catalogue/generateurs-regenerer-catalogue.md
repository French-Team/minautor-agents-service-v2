# regenerer-catalogue

> Outil de maintenance du catalogue de commandes du generateur.
> **Categorie** : generateurs | **Type** : outil | **Statut** : ebauche
> **Version** : 1.1.0

---

## Role

Regenerer / synchroniser le fichier derive `catalogue-commandes.json` du
generateur de commandes (`generateurs-commande`) a partir des outils reels
de `cerveau-projet/agents/tools/`.

## Pourquoi cet outil existe

1. Le catalogue est un **fichier derive** : chaque commande (modele) doit
   correspondre a un outil reel de `agents/tools/`.
2. Lors de la piste A, une regeneration a ete faite avec un script
   **temporaire** qui a capture des fragments d'aide comme descriptions
   (63 entrees cosmetiques sur 105, corrigees a la main par Buffy).
3. Cet outil est le **remplacant permanent** : les nouvelles entrees sont
   generees avec la vraie description extraite de l'en-tete du `.py`,
   pour ne plus re-corriger a la main.

## Utilisation

```bash
# Mode SYNCHRONISATION (defaut) : preserve l'existant, ajoute les outils manquants
python3 cerveau-projet/agents/tools/generateurs/regenerer-catalogue/regenerer-catalogue.py

# Dry-run : affiche ce qui serait fait sans rien ecrire (+ rapport garde-fou)
python3 .../regenerer-catalogue.py --dry-run

# Force : reconstruit tout depuis les outils reels (originales + speciales + outils)
python3 .../regenerer-catalogue.py --force

# Catalogue alternatif (tests) : cible un autre fichier que le catalogue reel
python3 .../regenerer-catalogue.py --catalogue /chemin/test-catalogue.json --dry-run

# Version
python3 .../regenerer-catalogue.py --version
```

Wrapper bash equivalent : `regenerer-catalogue.sh` (parite py/sh).

## Source des descriptions

| Format | Structure | Outils concernes |
|---|---|---|
| A - docstring | `"""` / `nom.py` / `Description...` / `"""` | Outils avec en-tete docstring |
| B - commentaires | `# nom.py` puis `# Description` | Outils convertis depuis `.sh` |

- Jointure des lignes descriptives consecutives (phrases coupees par `:` ou `,`).
- Translitteration **ASCII stricte** (NFKD - regle immuable).
- Limite a ~90 caracteres en coupant a la derniere phrase.

## Entrees speciales

Certaines entrees ont un modele manuel (le parsing d'aide est imperfectible) :
`generateurs-carte` (sous-commandes), `combos-moteur`, `verifier-restauration-sure`
(aide custom sans `usage:`).

## Regles de securite

1. **JAMAIS** `git checkout` / `git restore` / `git reset --hard` sur un fichier
   non commite (lecon incident piste B, reproduit 2 fois).
2. **GARDE-FOU cles dupliquees** : avant toute ecriture, verification que chaque
   entree a des cles uniques dans `parametres` (collision de placeholder, lecon
   inserer-contenu-fichier). Si doublon : refus d'ecrire + liste des entrees
   fautives. En `--dry-run`, rapport sans ecriture.
3. ECRITURE : indentation 2 espaces + **LF pur** (standard projet, `.gitattributes
   eol=lf`) - le piege des CRLF parasites est evite (plus de reecriture CRLF).
4. ASCII strict sur toute sortie.

## Historique

| Version | Date | Changement |
|---|---|---|
| 1.1.0 | 2026-08-09 | GARDE-FOU cles dupliquees dans parametres (refus d'ecriture si doublon, rapport en dry-run) + option --catalogue <chemin> (tests) + ecriture LF pur (standard projet). |
| 1.0.0 | 2026-08-08 | Creation : remplacant durable du script temporaire regen-catalogue3.py (piste A). Extraction des descriptions depuis les en-tetes .py (2 formats), synchronisation preservant l'existant, entrees speciales, CRLF uniforme. |
