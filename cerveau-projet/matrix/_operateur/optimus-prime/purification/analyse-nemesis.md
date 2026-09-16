---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# ANALYSE NEMESIS -- SUITE DE PURIFICATION (a lire AVANT d'ajouter)

> Demande createur 2026-09-14 : "ajouter une suite de parcours dans optimus
> pour la purification de nos fichiers, nos BDD (elles doivent etre
> controler et purifier dans une routine) -- avoir une analyse (nemesis)
> avant cette ajout."
> Methode : theme CONTRE-ANALYSE (Nemesis incarnee en THEME, jamais un
> agent). Trois axes. Reponse obligatoire : "Oui, mais...".
> Statut : lecture seule, aucune correction.

## La proposition attaquee (une phrase testable)

"On ajoute une SUITE DE PARCOURS `[purification]` (demande -> audit ->
nemesis -> decision -> ajouter) ET une ROUTINE qui controle et purifie
periodiquement les fichiers et les BDD de la Matrice."

## Axe 1 -- CAS LIMITES

- **Une purification qui SUPPRIME est irreversible.** Que se passe-t-il si
  la ligne retiree etait encore LUE ? C'est la panne nommee L-040 : un
  controle cherche ce que le nettoyage a deplace, et il devient AVEUGLE --
  *neutralise par le nettoyage qu'il surveille*.
- **Les journaux sont en AJOUT SEUL.** La doctrine du projet est : on
  ARCHIVE (rotation), on ne supprime jamais. Une "purification" qui
  reecrirait un `.jsonl` casserait le contrat de trois routines.
- **Bords non traites** : fichier vide, BDD absente, empreinte `.sha256`
  cassee, doublon a l'octet pres, ligne illisible (moitie de JSON).
- **Concurrence** : la routine tourne pendant qu'un demon ecrit. Deux
  ecrivains sur un fichier = lignes fragmentees (95 lignes cassees du
  2026-09-10, deja payees).
- **Defcon 5 / pause** : une purification qui tourne pendant la maintenance
  touche les fichiers que l'operateur est en train de reparer.

> **Oui**, une suite de purification est utile, **MAIS** toute etape qui
> RETIRE doit etre precedee de la recension de ce qui LIT ce qu'elle
> retire, et le retrait doit etre un ARCHIVAGE, jamais une suppression.

## Axe 2 -- OPTIMISATION

- **L'outillage existe deja.** Mesure : `rotation_journal` (borner sans
  rien perdre), `bdd-*` verifier (empreinte), `verifier-exemptions-visibles`,
  `scan-valeurs-en-dur`, `garde-tmp`, `garde-perimetre-write`,
  `espion-integrite`, `verifier-cadence`, `verifier-passe*`.
  Reconstruire ces gestes dans une routine neuve = **5e copie** d'un meme
  motif (L-029 : un moteur recopie N fois diverge N fois).
- **Le cout d'une routine de plus est DEJA MESURE, et il est lourd** :
  un demon, un journal (donc une borne), une cadence a declarer, publier
  ET mesurer. C'est exactement le chantier que MO-077 a MO-086 viennent de
  solder (5 journaux bornes, 6 cadences mesurees, sur-sollicitation
  traitee). Une 7e routine rouvre ce chantier.
- **Aucun critere GO chiffre** n'est propose : quelle mesure prouve que la
  purification sert (lignes retirees ? octets ? gardes repasses verts ?).

> **Oui**, controler et purifier est necessaire, **MAIS** la forme
> "nouvelle routine" est la plus chere et la plus risquee : le meme effet
> s'obtient en BRANCHANT les gardes existants sur une cadence (le
> routeur-maintenance passe deja toutes les 30 s) et en exposant UN VERBE
> de purification. Une routine neuve ne se justifie que par un besoin que
> le routeur ne peut pas porter.

## Axe 3 -- SECURITE / INTEGRITE

- **Perimetre** : purifier "nos fichiers" touche TOUT le workspace. Le
  perimetre d'ecriture d'Optimus est `matrix/` seulement -- une
  purification hors `matrix/` est une violation (regle immuable).
- **Suppression** : dans ce projet, **Hygie est le SEUL habilite a
  supprimer sans demande prealable**. Une routine qui supprime se
  substituerait a elle.
- **Porte unique** : toute ecriture doit passer par une PORTE (rotation,
  `bdd-* purger`, revert), jamais par une reecriture a la main.
- **Reversibilite** : avant/apres, empreinte, trace BDD obligatoire.

> **Oui**, il faut purifier, **MAIS** la purification doit etre LECTURE
> SEULE et SIGNALER ; ses ecritures passent par les portes existantes ;
> elle n'a JAMAIS le droit de supprimer (archive ou signale).

## Verdict, axe par axe

| Axe | Verdict |
|---|---|
| Cas limites | **A VALIDER AVEC RESERVE** -- possible seulement si le retrait est un archivage et si tout lecteur est recense AVANT |
| Optimisation | **CONTRE la routine neuve en l'etat** -- le geste doit etre teste avant d'etre industrialise ; un VERBE porte par le routeur coute 10 fois moins |
| Securite | **A VALIDER AVEC RESERVE** -- lecture seule + signalement + portes existantes + aucune suppression |

## La correction que le Nemesis impose (avant tout ajout)

1. **La suite de parcours** `[purification]` est ajoutee telle que demandee
   (demande -> audit -> nemesis -> decision -> ajouter) : elle ne coute
   rien, elle ORDONNE.
2. **La case [decision] est obligatoire et bloquante** : chaque ecart
   d'audit recoit UN verdict -- `purger` (par la porte d'archivage),
   `reparer` (par la porte du fichier), ou `declarer dette` (BDD frictions).
   Sans verdict, la purification ne touche rien.
3. **Pas de routine neuve pour commencer** : le geste est d'abord servi par
   les GARDES EXISTANTS, orchestres a la demande. La routine (demon
   periodique) ne sera ajoutee que si la mesure le justifie -- et ce sera
   une DECISION tracee, pas une evidence.
4. **Lecture seule par defaut** : la purification AUDITE et PROPOSE ; elle
   n'ecrit que par les portes ; elle ne supprime jamais.

> C'est le sens de la case [decision] : elle existe precisement pour que
> l'ajout d'une routine ne soit pas un reflexe.
