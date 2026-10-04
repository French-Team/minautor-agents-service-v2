---
identite:
  type: protocole
  appartient_a: optimus-prime
  commun: false
  liens: _operateur/optimus-prime/protocoles/protocoles-readme.md
---

# PROTOCOLE 14 -- L EVOLUTION DECIDEE PUIS EXECUTEE

> Demande du createur (2026-09-24, user-demandes/user-demandes.md) :
> "TOUTE EVOLUTION SIGNIFICATIVE OU OBLIGATOIRE DOIT ETRE DECIDER ET EXECUTER".
> Regle jumelle (servie A L ALLUMAGE) : regles-immuables/evolution-decidee.md.
> Ce protocole est la ROUTE ; la regle est l ENONCE que le pilote sert a chaque demarrage.

## ETAPE 1 -- QUALIFIER (avant tout code)

- SIGNIFICATIVE : un changement de regle, de comportement core, de mecanisme partage, de frontiere de perimetre, ou toute suppression.
- OBLIGATOIRE : exigee par le createur, par une garde, par une convention, ou par une decision deja prise.
- REVERSIBLE ou non : le revert est la condition du risque faible/moyen (proto-2).
- Non qualifie -> on NE PASSE PAS a la suite en sautant l etape : la non-qualification se DIT.

## ETAPE 2 -- DECIDER (jamais execute d abord)

- FAIBLE ou MOYEN reversible -> auto-evolution tracee (proto-2) : la decision est ECRITE dans le bilan, avec sa portee et son revert.
- SIGNIFICATIF, OBLIGATOIRE ou CRITIQUE (regle, comportement core, suppression, perimetre) -> CREATEUR AVANT, par le dialogue ou l entonnoir : AUCUN code ecrit avant sa decision.
- La decision porte : QUOI (portee exacte), QUI (decideur), REVERSIBLE (oui/non et comment), QUAND (la mission qui l execute).
- Une decision NON ECRITE n existe pas : elle part en item (entonnoir) ou en note -- jamais en memoire d agent.

## ETAPE 3 -- EXECUTER (la decision devient une mission)

- Depot par la porte entonnoir (source et type declares) puis pilote : serie stricte, une mission a la fois.
- Une decision qui dort plus d une session est un ITEM DEPOSE, pas un souvenir (regle immuable entonnoir-des-demandes).
- Jamais de contournement : une porte refuse en nommant, on applique le remede (loi du round, ORDRE 5).

## ETAPE 4 -- PROUVER (avant de dire termine)

- Cobaye qui MORD + contre-temoin qui EPARGNE -- les deux, toujours (un cobaye qui ne peut pas dire non ne prouve rien).
- py_compile ; si le round ajoute une garde, la suite est MISE A JOUR D ABORD puis lancee (loi du round, 4.4) ; non-regression verte.

## ETAPE 5 -- TRACER

- bdd-modifications pour CHAQUE fichier touche (porte unique, jamais le commentaire dans le fichier) ; suivi-optimus (1 debut + 1 fin) ; lecon si le diagnostic a porte un enseignement.

## ETAPE 6 -- GARDE (ce qui rend la regle reelle, pas un voeu)

- LECTURE A L ALLUMAGE : la regle jumelle est une source OBLIGATOIRE du catalogue du pilote (pilote/injection/config.json, phase demarrage) -- source absente = REFUS NOMME a chaque demarrage (injecter.py : aucune degradation silencieuse, la fiche technique compte les sources et leur obligation).
- INDEX : verifier-regles et verifier-protocoles accusent tout fichier absent de l index et toute ligne morte. MESURE sur cette livraison : les deux gardes ont MORDU (ECART nomme, code 1) tant que la piece existait SANS sa ligne d index, puis sont revenus VERTS l index pose -- le garde discrimine, il ne crie pas toujours.
- L execution de l etape 2 sur le REEL reste le createur et l auto-audit (proto-4) : ce protocole QUALIFIE, TRACE et RAPPELLE, il ne devine rien a la place du createur.

## INTERDICTIONS

- Executer une evolution significative ou obligatoire SANS decision.
- Decider sans trace : ce qui ne vit que dans la memoire d un agent est une discipline, pas un process (L-165).
- Laisser une decision dormir sans item ni mission.
- Modifier la regle jumelle sans le createur (elle est immuable : regles-immuables/evolution-decidee.md).
