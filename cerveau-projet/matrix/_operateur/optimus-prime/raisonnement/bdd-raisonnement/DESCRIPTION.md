---
identite:
  type: outil
  appartient_a: optimus-prime
  commun: false
---

# OUTIL -- bdd-raisonnement (zone INVISIBLE)

> Outil Python dedie a la BDD `segments.json`, dans la ZONE INVISIBLE d Optimus
> (L-016 : le cameleon ne le lit jamais). Genere depuis le moule templates/outil-bdd
> avec la SURCHARGE PRIVEE templates/outil-bdd-prive (modele-mere : bdd-lecons).

## Options

```
python3 cerveau-projet/matrix/lancer.py bdd-raisonnement ajouter --segment "..." --tags "tag1,tag2" [--source "..."]
python3 cerveau-projet/matrix/lancer.py bdd-raisonnement lire [--tag <tag>]
python3 cerveau-projet/matrix/lancer.py bdd-raisonnement corriger --id RS-XXX --tags "tag1,tag2" [--motif "..."]
python3 cerveau-projet/matrix/lancer.py bdd-raisonnement retirer --id RS-XXX [--index N] [--motif "..."]
python3 cerveau-projet/matrix/lancer.py bdd-raisonnement verifier
```

- `--segment` : segment (le contenu lui-meme, obligatoire).
- `--tags` : liste separee par des virgules -- obligatoire : pas d'element orphelin.
- `--source` : mission, outil ou fichier d'origine (facultatif).
- `lire --tag X` : filtre les entrees portant le tag X.
- `corriger --id RS-XXX --tags "a,b"` : corrige les TAGS d UNE entree EN PLACE. L id, la
  date, le segment et la source ne bougent pas ; les ANCIENS tags sont TRACES dans
  l entree (`corrections`) avec la date et le motif. L empreinte est RECALCULEE.
  Deux REFUS nommes : un id inconnu (l outil dit ce que la BDD porte) et des tags
  IDENTIQUES (une correction qui ne corrige rien n ecrit RIEN).
- `retirer --id RS-XXX [--index N]` : RETIRE une entree dont l EXISTENCE est fautive
  (mesure 2026-09-30 : cinq segments deposes deux fois par un script de depot relance).
  Elle survit ENTIEREMENT dans `retraits` (date + motif + entree), donc le retrait est
  REVERSIBLE. Refus nommes : un id inconnu, une id AMBIGUE (`--index` exige), un
  `--index` hors plage ou illisible. Le compteur n est JAMAIS remis en arriere : un id
  retire ne revient pas, donc une trace qui le cite ne designera pas un autre segment.

## Deux garde-fous que la porte se porte a elle-meme (EO-537)

- **`ajouter` REFUSE LE DOUBLON** : meme contenu ET meme source que l entree active,
  c est un refus qui NOMME l id deja present, et il intervient AVANT le compteur -- donc
  il ne consomme aucun id et ne laisse pas de trou dans la numerotation. Le meme TEXTE
  sous une source DIFFERENTE reste accepte : deux missions peuvent produire le meme
  raisonnement, et c est la source qui les distingue, jamais le texte.
- **`retirer` : un retrait sans temoin serait un effacement** (lecon L-055), donc
  l entree sortie de la liste est recopiee entiere. Un retrait muet se lirait comme
  une entree jamais nee.

## Format de la BDD

`{"identite": {...}, "segments": [{"id", "date", "segment", "tags", "source"}, ...]}`

Une entree CORRIGEE porte en plus `corrections` : la liste des corrections, chacune avec
sa `date`, ses `anciens_tags` et son `motif` -- une correction qui effacerait sa trace se
lirait comme une entree nee juste. Une entree RETIREE ne disparait pas : elle vit dans
`retraits`, a la racine de la BDD.

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| DESCRIPTION.md | la facade (ce fichier) |
| main.py | point d'entree global : DIRIGE |
| constants.py | chemins, valeurs (variante PRIVEE) |
| commun.py | fonctions communes : charger, enregistrer (atomique, LF), empreinte, options |
| ajouter/ | ajouter une segment taguee |
| corriger/ | corriger les tags d une entree EN PLACE (anciens tags traces) |
| retirer/ | retirer une entree fautive (temoin `retraits`, reversible) |
| lire/ | lister (tout ou par tag) |
| verifier/ | integrite SHA-256 (etalon-or) |

## Protections

- Ecriture atomique (tmp + remplacement), fins de ligne LF forcees (determinisme).
- Empreinte SHA-256 recalculee et enregistree A CHAQUE ecriture.
- Contenu et tags obligatoires : pas d'entree orpheline sans tag.
- Correction EN PLACE seulement : id, date, segment et source CONSERVES, anciens tags TRACES.
- Un id inconnu et des tags identiques sont REFUSES sans rien ecrire.
- Un DOUBLON (meme contenu, meme source) est REFUSE sans rien ecrire et sans consommer
  d id ; un retrait est TRACE dans `retraits` et donc reversible.
- ZONE INVISIBLE : jamais servie au flux cameleon (L-016).
