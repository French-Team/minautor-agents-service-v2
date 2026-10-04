---
identite:
  type: chaine
  appartient_a: optimus-prime
  commun: false
  titre: Bruit des documents sources de matrix/docs/ (transcripts JSONL)
  statut: todo
  pense-bete: PB-004
  nemesis: contre-analyse du 2026-09-23 (3 axes : volume contre valeur, le role tool n est pas un dechet, la preuve par le NET relu)
  spec: SP-004
  todo: TD-004
---

# Bruit des documents sources de matrix/docs/ (transcripts JSONL)

## Pense-bete -- la demande clarifiee

Crochet [preparation] du createur (EO-301) : CREER UN PARCOURS pour le BRUIT dans les fichiers de documentation de matrix/docs/. Le createur interroge un autre LLM, enregistre la conversation en JSON, et veut SUPPRIMER LE BRUIT pour clarifier et alleger proprement le fichier qui servira ensuite a la Matrice. CONTRAINTE NON NEGOCIABLE : docs/ est la ZONE DU CREATEUR -- la Matrice ne modifie JAMAIS un document source ; l outil PRODUIT un fichier NET A COTE (ou dans une zone declaree), le brut reste intact et sa trace est DITE.

## Ce qui est deja mesure

MATIERE REELLE (mesure du 2026-09-23, `matrix/docs/`, 6 fichiers) :
- `documentation-unsloth.jsonl` : 100 301 octets, 16 lignes JSONL, 0 illisible, ecrit le 2026-09-20 07:46. Roles : user 3, assistant 3, tool 10.
- `conversation-unslot-gemma-4.md` : 59 308 octets, modifie le 2026-09-20 19:33 -- il EXISTE. La premisse heritee de EO-299 (le fichier a disparu) est PERIMEE.
- Les 4 autres : `IMPERATIF.md` (SOURCE VIVANTE), `docs-readme.md`, `heritage-v1-v2-AGENTS.md`, `karpathy-guidelines.md`.

LE BRUIT, COMPTE PAR FAMILLE SUR LE VRAI FICHIER (93 985 caracteres, 16 lignes) :

| Famille | Mesure | Part |
|---|---|---|
| 1. REFLEXION (blocs thinking) | 10 blocs, 3 585 car | 3.8 % |
| 2. POLITESSE / AMORCE | 1 ligne, 22 car | 0.02 % |
| 3. DUPLICATION | 1 paire (lignes 13 et 15, similitude 85 %) : 7 719 car en 22 blocs communs de plus de 200 car | 8.2 % |
| 4. PRESENTATION SANS SUBSTANCE | 1 message entier (ligne 1, 780 car) ; les lignes 3 et 11 ANNONCENT puis DELIVRENT | 0.8 % |
| 5. PAGES WEB BRUTES (role tool) -- FAMILLE QUE L ENONCE NE NOMMAIT PAS | 10 messages, 73 633 car | 78.3 % |
| ... dont une recuperation en echec (HTTP 404) | 1 message, 39 car | 0.04 % |

PREUVE PAR ECHANTILLON (le brut est lisible, la mesure est refaisable) :
- famille 1 : ligne 3, bloc de 918 car ouvert par la balise de reflexion ;
- famille 2 : ligne 0, `bonjour, presente toi` (22 car, la SEULE du fichier) ;
- famille 3 : lignes 13 (15 754 car) et 15 (15 926 car) ouvrent toutes deux sur le meme index `llms.txt` ;
- famille 4 : ligne 1, presentation de l assistant (780 car) ; a l inverse les lignes 3 et 11 font 8 376 et 7 554 car HORS reflexion, et c est de la SUBSTANCE ;
- famille 5 : lignes 4 a 15, du README GitHub (16 046 car) a l index de documentation (15 926 car).

CE QUE LA MESURE DIT, ET QUI CORRIGE L ENONCE : les QUATRE familles nommees par la demande pesent ENSEMBLE 12.8 % du fichier. Le bruit DOMINANT (78.3 %) est une CINQUIEME famille que l enonce ne nommait pas : les pages web brutes recuperees par l outil. Un outil construit sur l intuition de l enonce aurait retire 3.8 % en croyant avoir fait le travail. C est exactement ce que N1 doit dire AVANT que N2 fabrique.

CORRECTION DE MA PROPRE AVANCE (2026-09-23 08:18:26, action `decouverte`) : j y avais ecrit `3 politesses, 4 % de reflexion, 96 % de substance`. C est FAUX -- 1 seule ligne de politesse, et le `96 % de substance` MASQUAIT les 78 % de pages web. Un compte qui n est pas DATE par famille se croit.

CONTRAINTE MESUREE ET JAMAIS FRANCHIE : aucune ecriture dans `matrix/docs/`. Les mesures ci-dessus sont des LECTURES, le brut est intact.

## NEMESIS -- avis contradictoire AVANT d ecrire

Trois attaques, et ce qu elles imposent.

1. AXE VOLUME CONTRE VALEUR. Le volume d une famille ne dit PAS sa valeur. Une page web brute peut porter LA reponse utile (le tutoriel est fait de ces pages) ; un bloc de reflexion peut porter une decision. Couper au pourcentage produirait un document propre et VIDE. Ce que l attaque impose : ne pas decider une famille par sa TAILLE mais par une REGLE DITE, et rendre chaque retrait RELISABLE (le retire est compte et conserve a part).
2. AXE : LE ROLE TOOL N EST PAS UN DECHET. Les 78.3 % sont la MATIERE PREMIERE du LLM, pas du bruit : c est ce qu il a lu pour repondre. Un outil qui les supprime par defaut fabrique un document ou la reponse ne s appuie sur rien. Ce que l attaque impose : distinguer le FETCH JETE (404, doublon) du FETCH CITANT (la source de la reponse), et que la POLITIQUE N4 tranche AVANT que N2 ne code.
3. AXE PREUVE. Le seul verdict acceptable est un compte AVANT et APRES sur le MEME fichier, double d une relecture d echantillon par un humain. Un outil qui sort un fichier plus PETIT s est declare gagnant : c est un faux vert. Ce que l attaque impose : le NET produit est RELU, et la part retiree est DITE (L-055), jamais silencieuse.

CE QUE LE NEMESIS IMPOSE, dans l ordre : (a) une REGLE DE RETRAIT ecrite, justifiee par famille, DECIDEE avec le createur ; (b) N2 ne produit RIEN avant que N4 ait tranche le sort du role tool ; (c) toute preuve est un compte AVANT et APRES, double d une relecture d echantillon.

## Ce qui reste a mesurer, et ce qui se DECIDE

- DECISION CREATEUR : le SORT de la famille 5. Les pages web brutes sortent-elles du document net (et vivent ailleurs), ou y restent-elles sous forme CITEE ? C est une decision, pas une deduction -- elle conditionne tout le reste.
- DECISION CREATEUR : la FORME de sortie. Ou vit le document net (a cote, dans un dossier declare), et sous quelle forme un transcript NET s ecrit (JSONL filtre, markdown, les deux).
- MESURE : l AUTRE forme de la matiere. `conversation-unslot-gemma-4.md` (59 308 car de markdown) porte le MEME travail -- mesurer son bruit par les MEMES familles avant de croire que l outil JSONL le couvre.
- MESURE : le NET, chiffre. Combien de caracteres restent, par famille retiree, sur les deux fichiers ? C est le chiffre qui fait decider.
- MESURE : ce que le createur appelle un document PROPRE -- un document que la Matrice peut RELIRE (index, citations) sans bruit.

## TODO (TD-004) -- le decoupage en ROUNDS (4 rounds, serie stricte)

N1 (FAIT, ce round) -- MESURER LE BRUIT SUR LA MATIERE REELLE : comptes par famille, preuve par echantillon, premisse re-mesuree. VERDICT : les 4 familles nommees pesent 12.8 %, une 5e famille non nommee en pese 78.3 %. Aucune ecriture dans docs/.

N2 -- L OUTIL qui lit le transcript et rend le document NET : il RETIRE selon la regle DECIDEE, il COMPTE et DIT ce qu il retire (L-055, jamais silencieux), il ecrit A COTE (le source reste INTACT), ecriture atomique, ASCII, zero valeur en dur. Preuve : nominal + negatif, compte AVANT et APRES.

N3 -- LE GARDE permanent : un document source declare NET ne porte plus de bruit, et le SOURCE n est JAMAIS modifie (docs-readme le dit). Preuve : un cobaye qui MORD (un bruit replante est accuse) et un contre-temoin qui EPARGNE.

N4 -- LA POLITIQUE, a DECIDER AVEC LE CREATEUR : ou vivent les transcripts bruts, quand ils sont archives, qui les relit, et le sort de la famille 5. AUCUN code avant cette decision.

CONTRAINTE RAPPELee : PREPARATION = discussion. Aucun fichier de la Matrice modifie hors `preparation/` + `suivi-optimus`, et aucun code avant le GO du createur.
