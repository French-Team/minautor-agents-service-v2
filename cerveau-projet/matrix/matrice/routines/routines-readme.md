---
identite:
  type: readme
  appartient_a: matrice-routines
  commun: true
---

# routines : VIE DE LA MATRICE (DOUBLE FLUX)

> Routines de vie de la Matrice. Deux flux distincts, doctrine createur
> 2026-09-12 : Flux 1 (cameleon GUIDE) vs Flux 2 (Optimus SURVEILLE).

## Familles par flux (doctrine dual flux 2026-09-12)

| Flux | Famille | Dossier prevu | Role | Surveille |
|---|---|---|---|---|
| **1. CAMELEON** | vie | routines/vie/ | demarrage et arret PROPRES de la Matrice (zero processus fantome, zero machine instablee) | perennite des boucles cameleon |
| **1. CAMELEON** | securite | routines/securite/ | garde-fous FLUX 1 : verification d'integrite SHA-256, perimetre d'ecriture `matrix/`, etats des BDD | FLUX 1 (pilote, injections, processus fantomes) |
| **1. CAMELEON** | orchestration | routines/orchestration/ | chargement des themes du vivier, file en SERIE stricte, transmission au pilote | non-regression du FLUX cameleon |
| **1. CAMELEON** | observateurs FLUX 1 | routines/observateurs/ | espions cameleon : pistage temps/tokens, surveillance du FLUX (non-regression flux, pas fichiers) | performance et flux cameleon |
| **2. OPTIMUS** | surveillance OPTIMUS | `_operateur/optimus-prime/espions/` + `remorque/` + `suivi-optimus` | espions qui SIGNALENT Optimus (jamais reparent), trace append-only, inventaire | OPTIMUS dans son flux reserve et verrouille |

> Premier espion POSE le 2026-09-06 : `espion-integrite/` (tour + boucle, integrite
> de toutes les BDD du registre, journal en ajout seul, arret cooperatif par drapeau).
> Il vit directement dans routines/ ; les familles ci-dessus accueillront les suivantes.

## Regles (communes aux deux flux, serie stricte partout)

1. Chaque routine = un outil Python avec protections d'ouverture/fermeture propres
   (regles-immuables/python-seul.md) -- `tmp + replace`, LF forces, PID + arret cooperatif.
2. Non-regression : les suites surveillent le FLUX (pilote qui ne fonctionne plus,
   Matrice qui ne demarre plus, processus fantomes), pas les fichiers un par un
   (source : IMPERATIF). Flux 1 : non-regression du FLUX cameleon ; Flux 2 :
   espions signalent Optimus (integrite 71, activite, remorque 45).
3. Securite AVANT le reste : une routine qui detecte un defaut d'integrite signale
   et bloque, elle ne repare pas en douceur (Flux 1 comme Flux 2).
4. Demarrage dedie : `demarrer-optimus-prime.md` (racine) reste le point d'entree
   Flux 2 (Optimus, hors sessions). Le Flux 1 demarre via la Matrice
   (`routines/vie/main.py activer` -> `server_matrice.py`), jamais depuis
   le pilote.
5. Dual flux jamais melange : une routine/donnee/outil d'un flux n'est
   jamais importee ni lue comme ressource de l'autre sans porte officielle.
   Les espions d'un flux ne corrigent jamais l'autre.

## Statut : DOUBLE FLUX POSE (2026-09-12, M-126) -- veille PERMANENTE ACTIVE

### Flux 1 : CAMELEON (Matrice GUIDE)

Faits : `vigie-portes` (2026-09-13, MO-056 : surveille les PORTES et ceux qui
les utilisent -- recette, sante, verbes, MOTEUR DE RECHERCHE temoin, usage,
citations ; alerte par la porte `signaler`, anti-spam par signature), `espion-integrite` (surveillance BDD matrice), `veille-flux`
(veille en arriere-plan : corriger-ascii + py_compile + regeneration du journal
visuel (MO-366), marbre en VIGILE,
alertes graves -> intercom, correction sans interrompre le LLM --
doctrine auto-correction). Chaque passe `veille-flux` se note elle-meme
dans `usages-outils-combos` et dans `activites-recentes` (section passes)
-- tags `veille-flux,passe,auto`.
Prochaines routines FLUX 1 : garde-fous de securite, orchestration des
themes du vivier, espions temps/tokens du cameleon.

### Flux 2 : OPTIMUS (Matrice SURVEILLE, flux reserve et verrouille)

Faits : `espions-optimus/` (integrite 71 fichiers `_operateur/` +
activite : file, frictions, verrous) + `remorque` (45 equipements) +
`suivi-optimus` (trace append-only, vue regeneree, etancheite cameleon).
Tous vivent en `_operateur/optimus-prime/` (jamais `matrice/`), SIGNALENT
seulement (correction M-113 domiciliation respecte, convention
`separation-cameleon-optimus` dual flux).

### Socle commun : VIE (PLANNING + SERVEUR + SERVICE)

`vie/` -- la vie de fond de la Matrice (commun aux deux flux), en DEUX modes
depuis MO-429 (decisions createur D1-D5, 2026-09-26) :

- **LE PLANNING** (`vie/planning.json`) est la SOURCE : cadence, mode
  (`boucle` | `passe`), decalage initial (la rotation d allumage), priorite et
  commande de passe. Chaque routine LIT son renvoi dans ses constantes
  (`cadence_planning('<nom>')`) ; personne ne recopie une valeur, et
  `verifier-cadence` lit la meme source.
- **MODE BOUCLE** : supervisee en permanence par le serveur matrice
  (`vie activer`), lancement DETACHE (survit a la session), etat
  (ARRET/ACTIVE/fantome nettoye), garde double lancement (chaque routine
  porte SON PID et refuse le second), arret cooperatif par drapeau (zero
  processus tue).
- **MODE PASSE** : eteinte entre deux passes par conception, elle est ALLOUMEE
  individuellement par le SERVICE (`vie service tour`) quand sa cadence est
  echue -- une passe tourne, publie, puis la routine sort ; le service recoit
  le resultat (code, trace de lancement, passe publiee) et transforme un ecart
  en MESSAGE (portes `signaler` et `machine-defcon`, niveaux declares, montee
  defcon sur le critique -- D4b). `vie service etat` montre, sans rien attendre,
  la derniere passe et l echeance de chacune.

GENERALISATION POSEE le 2026-09-26 : les SEPT routines sont en mode `passe`
(decision D2a, apres la preuve de la routine pilote `vigie-profil`, D5b) --
plus de boucle residente, aucun pic des sept au demarrage, une rotation
d allumage (au plus 4 par tour pour couvrir les cadences declarees sans jamais
faire le pic des sept, decalage initial + priorite). Le serveur
matrice reste le superviseur de la chaine : il appelle le service a chaque
cycle, tient l etat et les fantomes, et ne garde en `boucle` que les routines
dont le planning le dit. Entree au demarrage :
`python3 cerveau-projet/matrix/lancer.py vie activer`
(raccord `demarrer-optimus-prime.md` a poser par le createur). Bug de
routage `veille arret` (routait vers passe, le drapeau n'etait jamais
pose) attrape et repare au passage (M-046).
