# domicilier -- aligner une CLASSE de copies sur son DOMICILE (MO-172, EO-160)

> Une CLASSE est un motif RECOPIE : une meme fonction vivant dans plusieurs
> fichiers. Mesure fondatrice : **40 copies vivantes du parseur d options**, en
> **22 textes DIFFERENTS** -- elles avaient diverge en silence, sans qu aucun
> controle ne le voie (MO-169 puis MO-171). Le **DOMICILE** est le module qui
> porte le CONTRAT ; les copies doivent le CONSOMMER, jamais le recopier (M-076).
>
> Nom : la < remorque > est deja l inventaire de l operateur. Ici le geste est de
> **DOMICILIER** une classe -- d ou le nom de l outil.

## Usage

| Verbe | Commande |
|---|---|
| `auditer` | `python3 cerveau-projet/matrix/lancer.py domicilier auditer [--plan <chemin>] [--perimetre <dossier>] [--json]` |
| `aligner` | `python3 cerveau-projet/matrix/lancer.py domicilier aligner [--plan <chemin>] [--perimetre <dossier>] [--simuler\|--publier]` |

**`--simuler` est le DEFAUT** : sans `--publier`, la remorque DIT ce qu elle ferait
et n ecrit rien (dry-run). Sans `--plan`, elle consomme le plan livre dans
`plans/parseur-options.json`. `--perimetre` borne la fouille (et fouille ce
perimetre EN ENTIER, hors caches) : c est ce qui permet une epreuve dans un bac a
sable, sans jamais toucher la classe reelle.

## Le PLAN -- contrat FERME

Un plan qui ne dit pas tout ne peut pas tout aligner : il est REFUSE (code 2).

| Champ | Role | Obligatoire |
|---|---|---|
| `classe` | nom humain de la classe | oui |
| `fonction` | la fonction qui identifie la classe | oui |
| `domicile` | le module qui porte le CONTRAT (racine-relative) | oui |
| `marqueur` | la preuve qu une copie CONSOMME deja le domicile | oui |
| `docstring`, `import`, `appel` | les 3 lignes de la DELEGATION (`{extras}` = suffixe d appel) | oui |
| `exclus` | les homonymes DECLARES (qui portent le nom, pas de la classe) | non |
| `attendu` | le PERIMETRE DECLARE : les copies que le plan liste | non |
| `extras` | le suffixe d appel par copie (le plan GAGNE sur la deduction) | non |
| `derive` | deduire le suffixe du TEXTE ANCIEN (drapeaux, sans_tirets) | non |

**Exclusions** : une exclusion qui n exclut RIEN (le fichier n existe pas ou ne
porte pas la fonction) est REFUSEE -- dire une exclusion fausse est un mensonge.

**Perimetre declare (`attendu`)** : une copie que le plan ne LISTE pas est un
**TROU** (le plan doit etre mis a jour) et l alignement est REFUSE ; une copie
listee qui ne porte plus la fonction dit que le plan est **PERIME**. Sans
`attendu`, le plan travaille en perimetre OUVERT -- et le rapport le DIT.

## Verdicts

| Code | Sens |
|---|---|
| 0 | la classe est entierement alignee |
| 1 | ECART : des copies ne consomment pas le domicile, ou le plan est perime |
| 2 | REFUS : plan incomplet, premisse fausse, exclusion fausse, ou copie HORS PLAN |

En `--json`, la sortie ne porte QUE le rapport (aucune prose) : un consommateur
machine n a pas a decouper du texte -- c est le CODE qui porte le verdict.

## Securite

- **La remorque n ecrit JAMAIS elle-meme** : chaque ecriture (fragments compris)
  passe par la PORTE `ecrire` -- garde, validation, `.bak`, SHA. Si la validation
  refuse, la cible reste **INTACTE** (garantie EO-129).
- Le TEXTE ANCIEN n est jamais redevine : le bloc de la fonction est LU dans le
  fichier, ligne a ligne, puis remplace exactement.
- Le DOMICILE n est jamais compte comme une copie de lui-meme.
- Un plan dont une PREMISSE est fausse ne lit ni n ecrit rien.

## Ce qu il n est PAS

- Ce n est pas un formateur ni un linter : il ne touche QUE le bloc de la
  fonction de la classe.
- Ce n est pas un outil d ecriture directe : sans `--publier`, il ne peut
  structurellement rien ecrire.
- Ce n est pas un detecteur d homonymes automatique : les exclusions sont
  DECLAREES par l humain qui connait la classe (mesure MO-171 : un balayage doit
  DIRE ses exclusions, pas les oublier).

## Epreuve

Bac a sable complet (MO-172) : **18 controles OK** -- plan incomplet/domicile
absent/exclusion vide refuses, TROU signale et alignement refuse, simulation sans
ecriture (SHA), publication avec drapeaux DERIVES, publication invalide refusee
cible INTACTE, `--publier`+`--simuler` refuses, option privee de valeur DITE,
et le plan REEL qui ressort **41 alignees / 1 exclue / 0 trou**.
