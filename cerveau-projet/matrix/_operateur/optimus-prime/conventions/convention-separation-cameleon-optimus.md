---
identite:
  type: convention
  appartient_a: optimus-prime
  commun: false
---

# CONVENTION -- SEPARATION CAMELEON / OPTIMUS (DOUBLE FLUX)

> Decretee avec le createur (2026-09-11, dual flux 2026-09-12).
> Deux flux distincts, jamais brises, jamais melanges.
> Seul point commun : la Matrice.

## Les deux flux (doctrine createur 2026-09-12)

| Flux | Qui guide qui | Canal | Verrou |
|---|---|---|---|
| **1. CAMELEON** | Matrice GUIDE le cameleon | Matrice -> theme -> pilote -> cameleon -> fin -> Matrice | perimetre `matrix/` seul, sac-a-dos, tmp-cameleon |
| **2. MAINTENANCE OPTIMUS** | Matrice SURVEILLE Optimus | user <-> Optimus direct, ou Matrice reveille Optimus -> suivi-optimus -> Matrice | flux reserve/verrouille, session-matrix pause, perimetre `matrix/` seul, tmp-optimus |

## Les roles

- **Optimus** CONSTRUIT et ENTRETIENT la Matrice (outils, themes,
  protocoles, BDD, reparations). Domicile : `_operateur/`.
- **Le cameleon** EST UTILISE par la Matrice (execute les missions
  injectees par le pilote). Il ne construit rien, ne repare rien.

## Les interdits

1. Aucun contenu Optimus (`_operateur/` : fiche, parcours,
   protocoles, conventions, outils, espions/, remorque/, tmp-optimus/,
   suivi-optimus) n est lisible par le cameleon (L-016). Les espions et
   la remorque d Optimus vivent DANS `_operateur/optimus-prime/`,
   jamais dans `matrice/` (correction M-113).
2. Aucun contenu cameleon (vivier d execution, inbox cameleon,
   tmp-cameleon, sac-a-dos) n est utilise comme ressource de
   construction par Optimus sans porte officielle.
3. Les deux ont leur equipement SEPARE : sac-a-dos = cameleon,
   remorque = Optimus. Jamais d outil commun non declare.

## La surveillance par flux

### Flux 1 : la Matrice guide le cameleon

- Surveillance **du flux** : `veille-flux` (py_compile, ASCII, marbres),
  `espion-integrite` (BDD matrice), `suivi-sync`, non-regression.
  Verifient que le pilote injecte, que la Matrice demarre, qu'aucun
  processus fantome ne persiste.
- Equipement cameleon : `sac-a-dos` (durees, codes), remis 45 via
  `tmp-cameleon/`, jamais `_operateur/`.

### Flux 2 : la Matrice surveille Optimus (flux reserve et verrouille)

- Surveillance **d'Optimus** DANS CE FLUX : `espions-optimus/`
  (integrite 71 fichiers `_operateur/` + activite : file, frictions,
  verrous) + `remorque` (45 equipements) + `suivi-optimus`
  (trace append-only, vue regeneree, etancheite cameleon) +
  `BDD modifications` (hashes, raisons, friction, statut verrouille).
- Flux **verrouille** : session-matrix en pause (`pause-session`,
  `machine-defcon` defcon 5), cameleon stoppe, perimetre reductible,
  notifications etanches (jamais la raison).
- Les espions SIGNALENT, ils ne reparent jamais. Le verrou BDD
  `verrouille->valide` est leve par Optimus APRES preuve.
