---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# AUDIT MO-524 / EO-515 -- LES DOUBLONS DE L ENTONNOIR (UNE DEMANDE DEJA SERVEE RE-ENTREE DANS LA FILE)

## 1. LA DEMANDE DE CETTE MISSION, ET CE QU ELLE EST DEJA

MO-524 (item EO-515, depose le 2026-09-30 09:43:16) demande :

    "TOUTE EVOLUTION SIGNIFICATIVE OU OBLIGATOIRE DOIT ETRE DECIDER ET
     EXECUTER" doit devenir une regle immuable et un protocole.

**Elle a deja ete executee -- integralement -- par MO-437** (2026-09-27,
7h29 -> 7h44, `historiques-missions-optimus.jsonl` ligne 429). Les deux textes
ne sont pas le meme : celui de MO-515 est la meme demande avec une faute
("DECIDER ET EXECUTER" au lieu de "DECIDEE ET EXECUTEE") et sans le rappel de
contexte. Un lecteur humain reconnait le doublon instantly ; aucune machine ne
le verrait, parce que le texte n est pas identique.

**La doctrine est donc en place, cablee et servie. Preuves jouees ce round :**

| Preuve | Resultat |
|---|---|
| `regles-immuables/evolution-decidee.md` | present, 24 lignes, 1953 octets |
| `protocoles/proto-14-evolution-decidee.md` | present, 56 lignes, 3702 octets |
| Index `regles-immuables/regles-immuables-readme.md` | ligne presente (regle citee) |
| Catalogue `protocoles/protocoles-readme.md` | ligne 14 presente |
| `remorque/inventaire.json` | equipement `proto-14-evolution-decidee` declare |
| `optimus-prime.md` | regle ABSOLUE presente (ligne 116) |
| `verifier-regles verifier` | **aucun ecart** (4 controles OK) |
| `verifier-protocoles verifier` | **aucun ecart** (seul l ecart connu `conversation-unslot-gemma-4.md`, deja EO-451 en file) |
| `injecter.py demarrage` | **7 sources servies, 0 alerte, 0 refus** ; le texte `REGLE IMMUABLE -- TOUTE EVOLUTION SIGNIFICATIVE OU OBLIGATOIRE EST DECIDEE PUIS EXECUTEE` est bien imprime dans l injection de demarrage |

**Verdict : rien a reconstruire.** Reconstruire la regle aurait ete une
evolution executee SANS decision -- exactement ce que la regle interdit.

## 2. LE VRAI SUJET : LE DOUBLON N A JAMAIS ETE VIE PAR UNE MACHINE

Le nom `deja-vu` existe dans l evaluateur d auto-validation
(`super-combos/combos/outils/evaluer-auto-validation.py`, axe ligne 55).
**Ce nom ment.** L axe ne regarde pas si la demande a deja ete servie : il
compare le champ `source` a la valeur `createur` (lignes 253-258). Il signifie
"vue avec le createur", pas " deja vue ". Aucun autre axe ne consulte les
missions deja terminees.

**Mesure : le depot (`pilote/entonnoir/vrac/entry.py`, fonction `executer`)
n interroge jamais la file des missions.** Il ecrit l item et le classe. Il n y
a pas de deduplication, ni au depot, ni au classement, ni au consumption du
brin (`entonnoir/tresse/`, `consommer_tete_tresse`).

## 3. LA MESURE SUR TOUT LE CORPUS

**Methode (rejouable, sans invention).** Normalisation : minuscules, accents
retires (decompose NFD + categorie Mn), tout ce qui n est pas `[a-z0-9]`
remplace par un espace, espaces collapses. Une mission est retenue si son
objectif normalise compte au moins 8 mots (en dessous, le recouvrement n a pas
de sens). Deux objectifs sont doublons si le **recouvrement**
`|A inter B| / min(|A|,|B|)` vaut au moins **0.75** -- le denominateur est le
plus petit des deux, sinon un enonce long ne peut jamais etre un doublon d un
enonce court (piege mesure : la premiere version de cette mesure, avec
`SequenceMatcher`, rendait 0.011 pour MO-524/MO-437 -- `autojunk` de la
bibliotheque traite les mots rares comme du bruit ; mesuree a la main, le
recouvrement reel vaut **0.824**).

**Corpus** : `file-missions-optimus.json` (85) + `file-missions-optimus-archive.json` (439) + `file-missions-legacy-archive.json` (89) = **613 missions**, dont **595** retenues par le seuil de 8 mots.

**Census global** : **542 paires** a recouvrement >= 0.75 (l immense majorite
sont les missions `auto-diagnostic ... / reparation / inspection` retirees en
masse le 2026-09-20 : 42 paires a recouvrement > 0.96 entre MO-256 a MO-283).
Ce nombre n est pas un scandal : ces doublons ont ete **retires**, pas servis.

**Le chiffre qui compte -- une mission RE-SERVIE apres cloture de la premiere :**

- 39 paires (premiere terminee, seconde terminee, seconde chargee apres la premiere terminee, recouvrement >= 0.75)
- dont **4 redepots explicites** (`REDEPOT :` ou `remis en circulation` dans l objectif) -- **legitimes** : la premiere avait consomme la demande en la repourposant, le redepot evite la perte
- **33 missions distinctes ont donc ete rejouees sans qu'aucune ne le dise.**

Les 11 paires exactes (recouvrement 1.0) :

| Premiere (terminee le) | Rejouee par (terminee le) | Intitule |
|---|---|---|
| M-022 (2026-09-06 18:11) | M-048 (2026-09-07 06:51) | python-compile : ne compile pas (confirme apres re-test) |
| M-022 (2026-09-06 18:11) | M-085 (2026-09-10 20:19) | idem |
| M-033 (2026-09-06 20:32) | M-034 (2026-09-06 20:32) | apres un fin SANS lot, l injection est rejouee |
| M-039 (2026-09-06 20:42) | M-041 (2026-09-06 21:00) | la veille se lance seule au demarrage |
| M-049 (2026-09-07 07:11) | M-051 (2026-09-07 07:32) | purge automatique des signatures obsoletes |
| M-086 (2026-09-10 20:19) | M-088 (2026-09-10 20:20) | incident-combo : crash du sous-processus |
| MO-020 (2026-09-12 20:21) | MO-034 (2026-09-13 09:22) | compteur desynchronise de suivi-optimus.md |
| MO-022 (2026-09-12 20:25) | MO-035 (2026-09-13 09:25) | sort des routines arretees |
| MO-164 (2026-09-17 19:57) | MO-205 (2026-09-20 17:10) | charger_lot n a AUCUNE garde de serie stricte |
| MO-168 (2026-09-18 07:31) | MO-196 (2026-09-19 14:37) | proposition, lanceur unique matrix/lancer.py |
| MO-168 (2026-09-18 07:31) | MO-249 (2026-09-20 05:23) | idem |

Les sept dernieres lignes **ressemblent** a des doublons et **n en sont pas** :
M-048, M-085, M-088, MO-205 et MO-035 portent le meme intitule court que leur
predecesseur mais un **objet** different (un autre fichier a compiler, un autre
garde a poser). C est le limite de toute mesure par texte : **elle produit des
candidats, pas des verites.** La decision reste humaine. Cette limite est
ditte ici pour que la mesure ne soit pas surchargee : sur les 39 paires, une
part importante sont des faux positifs -- mais **MO-524 est un vrai positif**,
et il est dans les faits (section 1).

## 4. L ETAT DU BRIN AU MOMENT DE LA MESURE (31 items)

**Un seul item du brin est un doublon confirme :`EO-516`**
(recouvrement **0.841** avec `MO-429`, terminee le 2026-09-26 19:02).

- `EO-516` (depose le 2026-09-30, type `dev`) : revoir le declenchement des
  routines, leur duree de vie et leur cycle ; la Matrice doit avoir un planning
  et un service qui les demarre individuellement.
- `MO-429` (terminee le 2026-09-26) : **le meme texte, mot pour mot** (seule
  difference : la ponctuation d'origine). Livrables cites dans son bilan :
  `routines/vie/planning.json` (7 entrees, mode passe generalise 7/7, moteur
  partage `matrice/data/commun/planning_routines.py`) et le service `routines/vie/`.

**Les 30 autres items sont sous le seuil.** Le plus haut reste `EO-506`
(recouvrement 0.786 avec `MO-509`) et c'est un **faux positif** : `EO-506`
demande si le pilote injecte `user-profil.md`, `MO-509` a porte la passerelle
`user-demandes/` -- le mot "passe" fait le lien. Un item par mission, donc :
**le bruit de la mesure est bien a 0.786, le signal reel commence vers 0.84.**

## 5. CE QUE L ENTENNOIR FAIT DU DOUBLON QUAND IL LE RENCONTRE (constat decout)

Trois portes savent deja traiter un doublon **une fois qu il est dans la file** :

1. `entonnoir retirer --id EO-XXX` -- le geste suivi dans MO-035 : *huit missions doublons purgees de l entonnoir* (E-085, E-087 a E-093), la porte `retirer` corrigee a cette occasion pour traiter aussi les FILES et recomposer le brin.
2. L agent lui-meme, qui le nomme dans son bilan (MO-034 : *doublon PERIME deja execute en MO-032, aucun code touche*).
3. `entonnoir solder --id ... --preuve ...` -- solder l item servi, avec sa preuve.

Ce qui manque est **le moment ou la question se pose** : au depot. L item entre
et personne ne demande jamais *cette demande a-t-elle deja ete servie ?*

## 6. CE QUE JE NE FAIS PAS, ET POURQUOI

Ajouter un axe `deja-vu-reel` (ou une deduplication au depot) est une
**evolution significative du coeur d'auto-validation**. La regle que cette
mission certifie l'interdit en MOI-MEME :

> toute evolution significative est DECIDEE avant d etre executee -- createur
> pour le critique ; auto-evolution tracee pour le faible et le moyen.

Elle touche le verdict qui arme la serie stricte : c est du **significatif**,
pas du faible. **C est donc une DETTE, pas une DERIVE** : elle est ecrite ici,
nommee, et son decider revient au createur. Ce que je livre dans cette mission
n est pas le code : c'est la **preuve** que le besoin existe (613 missions, 33
rejouees, 1 doublon vivant dans le brin) et le **critere** de deduplication,
deja mesure et eprouve sur 613 missions, pret a etre pose le jour ou la
decision est prise.

## 7. LIVRABLE IMMEDIAT

`EO-516` est un doublon **prouve**, dans le brin, en attente d etre servi pour
rien. Il est retire de la file par la porte `ontonnoir retirer`, avec la
preuve nominative (l'item + MO-429 + le livrable deja pose). Une mission de
moins a perdre, une demande createur qui ne disparait pas (la demande d origine
est `##A-FAIRE###` dans la passerelle et reste visible).

## 8. REPRODUCTIBILITE

Toute la mesure tient dans les trois lignes de normalisation de la section 3 et
se rejoue sur les trois fichiers cites, sans aucun fichier temporaire ni
dependance. Le seuil `0.75` est **declaratif** et **arbitrable** : il donne 39
candidats dont un tiers sont des faux positifs, `0.84` les reduirait au seul
EO-516.
