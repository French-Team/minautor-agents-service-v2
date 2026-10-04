---
identite:
  type: outil
  appartient_a: buffy
  version: "0.2.2"
  description: "Routine de securite : verifie que le flux Oracle > Agent > Oracle est respecte"
---

# verifier-flux-securite

Routine de securite qui verifie que le flux est respecte dans le tableau AGENTS-activite-recente.md.

## Le flux correct

```
Oracle active Cerberus (DEBUT Oracle)
Oracle active un agent (DEBUT Oracle)
L agent travaille
Oracle historise FIN (FIN Oracle)
Oracle re-active Cerberus (DEBUT Oracle)
```

**Regle absolue** : entre chaque DEBUT et FIN d un agent, Oracle DOIT apparaitre.
Oracle est le SEUL a historiser DEBUT/FIN.

## Regles verifiees

| Regle | Description |
|---|---|
| R1 | Chaque agent (hors Oracle, hors citations) a un DEBUT + FIN |
| R2 | DEBUT d un agent precede d une entree Oracle |
| R3 | FIN d un agent suivi d une entree Oracle |
| R4 | Agent ne historise pas son propre DEBUT/FIN |
| R5 | Oracle present entre DEBUT et FIN de chaque agent |
| R6 | Citations ont toujours "instant" comme Debut/Fin |
| R7 | Apres FIN d un agent, le prochain evenement est l aeroport (Oracle/pilote, modele aero R1/R3) - la fin de tout agent va vers Oracle, RIEN vers Cerberus (atterrissage terminal sur Cerberus = decision du pilote en fin de round, pas une fin d agent). Le largage du pilote apres une fin (RECUPERE/RETOUR puis agent suivant) est un flux NORMAL |

## Utilisation

```bash
# Verifier le flux
python3 cerveau-projet/agents/tools/verifier/verifier-flux-securite/verifier-flux-securite.py

# Afficher le flux detecte
python3 cerveau-projet/agents/tools/verifier/verifier-flux-securite/verifier-flux-securite.py --flux
```

## Sortie

- **FLUX OK** : toutes les regles sont respectees
- **FLUX KO** : N anomalie(s) detectee(s) avec details

## Historique

| Version | Date | Changements |
|---|---|---|
| 0.2.2 | 2026-09-02 | FIX faux positif R7 sur largage (mission 31fe865e) : le scan cherchait le prochain agent en SAUTANT la coordination (oracle/pilote/cerberus) -> apres une FIN, il sautait RECUPERE/RETOUR et trouvait l agent LARGUE (ex: FIN vulcain 15:03:35 -> morpheus ACTIF 15:05:51 = largage du pilote) -> FLUX KO a tort. Desormais le scan s arrete au premier evenement non-routine : aeroport (oracle/pilote) = OK, cerberus = OK seulement si atterrissage terminal, agent metier direct sans aeroport = violation |
| 0.2.0 | 2026-08-30 | Modele aero : R7 accepte Cerberus OU Oracle apres une fin ; exclusion des blocs routines v1 (encart, flux, live, notation, verifier-statuts, vigie-perimetre) du scan |
| 0.2.1 | 2026-09-02 | Directive utilisateur : R7 passe a ORACLE UNIQUEMENT (la fin de tout agent va vers Oracle, rien vers Cerberus ; Cerberus = atterrissage terminal du pilote en fin de round, pas une fin d agent) |
| 0.1.0 | 2026-08-28 | Creation : 6 regles de securite, lecture du tableau v1 |
