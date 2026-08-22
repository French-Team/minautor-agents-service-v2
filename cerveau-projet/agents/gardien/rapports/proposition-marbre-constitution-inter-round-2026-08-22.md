# Proposition de modification de marbre -- zone CONSTITUTION (2026-08-22)

**Agent** : Gardien
**Zone** : AGENTS.md / `<!-- MARBRE:DEBUT constitution -->` / table "Le cycle fondamental", ligne etape 5
**Contexte** : decision utilisateur 2026-08-22 (flux ROUND / INTER-ROUND / REPRISE,
protocole-fin-mission v0.2.0, spec-guider-parcours v0.6.3 Pattern 13 regle 5).
L'etape 5 du cycle fondamental est restee a l'ancienne formulation.

## AVANT

| 5 | Agent termine : la fin suit SA carte (activation directe -> reactiver Cerberus ; maillon de chaine -> activer le suivant) |

## APRES

| 5 | Agent termine : la fin suit SA carte (activation directe -> reactiver Cerberus ; maillon de chaine -> activer le suivant) ; ERREUR HORS-PERIMETRE -> INTER-ROUND : l'agent active l'AGENT HABILITE avec le rapport de l'erreur, la fin de l'inter-round reactive l'appelant qui REPREND son round principal (protocole-fin-mission v0.2.0) |

## Impact

- Coherence : aligne la zone MARBRE sur l'item 3 de la section "Fin de mission"
  (deja modifie hors marbre) et sur protocole-fin-mission v0.2.0.
- Perimetre : UNE seule ligne de la zone constitution. Aucune autre zone touchee.
- Procedure apres validation utilisateur :
  1. Buffy modifie le CONTENU de la ligne (SEULE habilitee aux fichiers structurels)
  2. Le Gardien execute la porte : `proteger-modifier-marbre --zone constitution
     --raison ... --autorisation UTILISATEUR-2026-08-22`
  3. Re-empreinte + journal marbre-log.jsonl + verrou `proteger-verrou-marbre --tous`

## Statut

EN ATTENTE DE VALIDATION UTILISATEUR - aucune ecriture effectuee.
