---
identite:
  type: outil
  appartient_a: buffy
  version: "0.1.0"
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
| R7 | Apres FIN d un agent, le prochain agent est Cerberus ou Oracle (modele aero 2026-08-30) |

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
| 0.2.0 | 2026-08-30 | Modele aero : R7 accepte Cerberus OU Oracle apres une fin ; exclusion des blocs routines v1 (encart, flux, live, notation, verifier-statuts, vigie-perimetre) du scan |
| 0.1.0 | 2026-08-28 | Creation : 6 regles de securite, lecture du tableau v1 |
