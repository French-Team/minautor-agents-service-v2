---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# `user-demandes/` -- la PASSERELLE USER (user <-> optimus)

> **Ce dossier n est pas un dossier de travail de la Matrice : c est le canal par
> lequel le USER parle a optimus.** Le user y ecrit ses demandes EN CLAIR, dans sa
> langue ; la Matrice les LIT, les SUIT et les EXTRAIT vers l entonnoir puis le
> pilote. Une demande EXTRAITE est RETIREE du fichier : le canal se VIDE de ce qui
> a ete servi, il ne grossit pas par accumulation.

## Les quatre pieces du dossier

| Piece | Ce qu elle est | Qui l ecrit |
|---|---|---|
| `user-demandes.md` | LE CANAL : les demandes du user, encadrees par les patternes de delimitation. Il ouvre sur son HEAD (carte d identite + mode d emploi + la LEGENDE des crochets, toujours sous les yeux du user) et se termine par les demandes NON ENCORE extraites | le USER (ses mots, jamais reecrits) |
| `le-vivier/le-vivier.md` | les FUTURS THEMES DU VIVIER : une reserve de mots et de structures que le vivier du cameleon tirera de la (meme discipline de delimitation) | le USER |
| `template-demande.md` | LE FORMULAIRE : le squelette a remplir, un exemple rempli, et comment inserer une demande | la Matrice (socle) |
| `README.md` | ce fichier : le role, le contenu, le cycle de vie | la Matrice (socle) |

Le socle (ce README, le template et le HEAD du canal) est ecrit en ASCII par la
Matrice ; les MOTS DU USER ne sont jamais reecrits.

## Le chemin d une demande (de bout en bout)

```
le user ecrit sa demande dans user-demandes.md, entre deux patternes
   -> la Matrice la LIT (la demande et son crochet d entree disent ce qu elle declenche)
   -> elle devient un ITEM de l entonnoir (classe, tisse, puis servi au pilote)
   -> le pilote la sert en ROUND : un agent la conduit jusqu a sa cloture
   -> la demande EXTRAITE est RETIREE du canal ; son avancement vit dans le suivi
```

Un pattern ne franchit JAMAIS deux etapes dans la meme mission : chaque etape
(a-faire -> fait -> a-controler -> certifier) est une INJECTION, donc une mission a
part entiere.

## HORS JUGEMENT (et ce n est pas un oubli)

Le dossier est ecrit par le user LUI-MEME, en continu, hors de toute porte de la
Matrice, et dans SA langue (accents, apostrophes, crochets). Ce n est pas une
source du projet : aucune porte ne le produit, aucune ne le repare. Le CORRIGER
mutilerait sa parole ; le juger comme une ecriture non attribuee accuserait une
ecriture LEGITIME a chaque passe.

La decision (createur, MO-475) vit a son DOMICILE UNIQUE :
`matrice/data/commun/passerelle_user.py` (nom, motif, predicat). Elle est
CONSOMMEE, jamais recopiee (M-076) :

- `controle-attribution.py` l exclut du jugement d attribution ;
- `garde-ascii.py` la met HORS CHAMP en la NOMMANT et en la COMPTANT ;
- la regle `regles-immuables/ascii-strict.md` ECRIT l exception a cote de celle de
  `docs/`.

## Ce que la Matrice ne fait JAMAIS ici

1. **Reecrire les mots du user** : ses demandes, ses accents, ses apostrophes et
   ses crochets sont intacts. L extraction RETIRE une demande servie, elle ne la
   reformule pas.
2. **Corriger l ASCII** de ses fichiers : la zone est exemptee (voir ci-dessus).
3. **Traiter le canal comme une source du projet** : aucune porte ne l ecrit ni ne
   le repare -- c est un CANAL, pas un livrable.
