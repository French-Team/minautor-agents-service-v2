# Audit des besoins -- Purification RVAV (Buffy, 2026-08-15)

## Contexte

Le protocole rvav-workflow.md a une etape 5 [purifier] mais il a ete ABANDONNE
pendant le developpement et n est PLUS DU TOUT A JOUR (decision utilisateur :
lister les besoins reels et reconstruire l outil, pas reactiver le protocole tel quel).

## Constat (detecter-surcharge-fichier --recursive, seuil 250 lignes)

40+ fichiers en surcharge. Les plus critiques sont les CORRECTIONS.MD des agents
(accumulation de lecons sans purification) et AGENTS-historique.md.

| Fichier | Lignes | Lecons/entrees | Lignes/lecon |
|---|---|---|---|
| janus/corrections.md | 4736 | 275 | 17 |
| buffy/corrections.md | 3421 | 182 | 19 |
| vulcain/corrections.md | 3328 | 161 | 21 |
| morpheus/corrections.md | 2826 | 153 | 18 |
| themis/corrections.md | 1096 | 66 | 17 |
| cerberus/corrections.md | 846 | 27 | 31 |
| promethee/corrections.md | 334 | 14 | 24 |
| AGENTS-historique.md | 1565 | 150 | 10 |

Autres types en surcharge (moins critiques) : fiches agents (255-314 lignes,
structure template), protocoles (262-384, structure documentaire), 1 rapport Clio
(389), spec activer-agent-principal (297).

## Types de fichiers a purifier + quotas proposes

| Type | Motif de croissance | Quota (lignes) | Action de purification |
|---|---|---|---|
| `corrections.md` d agent | lecons cumulees (section ## [LECON]) | 1000 | archiver les lecons les plus anciennes dans `<agent>-historique.md` (nouveau fichier, cote a cote) |
| `AGENTS-historique.md` | entrees cumulees (lignes | 2026-) | 800 | archiver les entrees les plus anciennes dans AGENTS-historique-archive.md |
| fiches agents | template (8 sections + variante) | 320 | signaler seulement (structure template, pas une croissance) |
| protocoles | documentaire (7-8 sections) | 400 | signaler seulement (structure documentaire) |

## Principe de purification (anti-perte)

**On ne supprime JAMAIS d information.** Les lecons sont la memoire des erreurs
(anti-repetition). La purification DEPLACE vers un fichier d historique a cote
(archive), elle ne tronque pas. Le fichier principal garde les lecons les plus
RECENTES (les plus pertinentes pour le travail courant) ; les plus anciennes
vont dans l archive.

Ordre chronologique : le fichier corrections.md est ecrit du plus ancien (haut)
au plus recent (bas) -- les sections ## [LECON] s ajoutent en bas. L archive
recupere donc les sections du HAUT.

## Spec de l outil purifier (pour Vulcain)

Nom : `purifier-rvav` (categorie Purifier -- NOUVELLE categorie d action)
Emplacement : cerveau-projet/agents/tools/purifier/purifier-rvav/purifier-rvav.py
(+ .md documentation, + entree catalogue generateurs-commande, + entree index-tools.md)

Options :
- `--tous` : purifier tous les fichiers en surcharge du repertoire courant
- `--agent <nom>` : purifier les corrections.md d un agent (ex: --agent janus)
- `--fichier <chemin>` : purifier un fichier precis (ex: AGENTS-historique.md)
- `--seuil <n>` : seuil de lignes (defaut 1000 pour corrections, 800 pour historique)
- `--dry-run` : DEFAULT OBLIGATOIRE -- afficher le plan sans rien modifier
- `--rapport <fichier>` : ecrire le plan de purification en markdown
- `--executer` : appliquer reellement (TOUJOURS apres un --dry-run valide)
- `--version`, `--verbose`

Comportement :
1. Detecter les fichiers en surcharge (meme logique que detecter-surcharge-fichier)
2. Pour chaque fichier : calculer combien de sections/entrees archiver pour
   repasser sous le quota
3. Afficher le PLAN : fichier, lignes avant, lignes apres, nb sections archivees,
   fichier d archive cree
4. --executer : deplace les sections du haut vers l archive (nouveau fichier
   cote a cote, meme en-tete), conserve le reste, garantit LF pur + ASCII strict
5. Verifier apres : le fichier principal est sous le quota, l archive est creee,
   aucun contenu perdu (somme des lignes conservee)

Contraintes : ASCII strict (aucun accent), LF, argparse, modele de
detecter-usage-scripts-temporaires (en-tete avec usage, detection racine projet
via AGENTS.md), pas de script tiers, dry-run obligatoire par defaut (aucune
ecriture sans --executer).
