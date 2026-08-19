# Rapport d education -- Themis : combos ASCII (Chiron)

- **Date** : 2026-08-18
- **Educateur** : Chiron (protocole-education-continue, declencheur "mise a
  jour d un outil")
- **Objet** : eduquer Themis a utiliser les combos/outils ASCII au lieu de
  scripts temporaires
- **Verdict** : A REVOIR (correction de carte a appliquer par Buffy)

## Diagnostic

1. **Carte de Themis** : 0 mention de "ascii", "corriger-ascii" ou
   "combos-corriger-non-ascii" dans parcours-themis.json. Les seuls combos
   references : combos-audit-themis, combos-audit-general,
   combos-valider-cerveau, combos-analyse-projet.
2. **Registre des usages** : combo-corriger-ascii = 0 usage (JAMAIS lance).
   combos-corriger-non-ascii = non utilise par Themis. executer-script-
   temporaire = 8 usages (Themis prefere les scripts temporaires aux combos).
3. **Fiche de Themis** : regle ABSOLUE 4 et 5 (outils du cerveau uniquement,
   outil exact assigne dans le parcours) -- mais AUCUN outil ASCII n est
   assigne dans son parcours, donc elle ne peut pas en utiliser.
4. **Outils disponibles** :
   - `combo-corriger-ascii` (definition-combo.json v0.1.0, via combos-moteur) :
     corriger-accents --all --recursive -> valider-conformite-ascii. Cible par
     defaut cerveau-projet/agents.
   - `combos-corriger-non-ascii` v0.3.0 : `--full` scanne le projet entier,
     DRY OBLIGATOIRE avant wet (preuve datee, wet refuse sans elle), rapport
     concis mais complet (tous fichiers, codes U+XXXX), wet cible uniquement
     les fichiers detectes (~3 s). Cree/ameliore par Vulcain le 2026-08-18.

## Corrections proposees (a appliquer par Buffy)

1. **Case c9** ("Ecrire le rapport dans themis/rapports/") : ajouter un indice
   OUTIL `combos-corriger-non-ascii` (commande --full --dry-run puis --full
   apres examen) + une regle : "APRES redaction du rapport, verifier l ASCII
   avec combos-corriger-non-ascii --full --dry-run ; corriger avec --full
   (dry obligatoire avant wet)".
2. **Case c12** ("Lecons et retour") : ajouter l indice OUTIL
   `combos-corriger-non-ascii` en rappel (rapports + corrections doivent etre
   ASCII purs).
3. **Fiche themis.md** : mentionner les 2 combos ASCII dans la table des
   outils de la fiche (combos-audit-general, combos-valider-cerveau, + les 2
   combos ASCII).

## Lecons pour Themis (documentees dans corrections.md + BDD)

1. LES RAPPORTS ASCII SE VERIFIENT AVEC UN COMBO, PAS UN SCRIPT TEMPORAIRE :
   apres chaque redaction de rapport (c9), lancer
   combos-corriger-non-ascii --full --dry-run pour verifier l ASCII du projet,
   puis --full pour corriger (dry OBLIGATOIRE avant wet : la preuve est
   verifiee par l outil, on ne peut pas corriger a l aveugle).
2. LES SCRIPTS TEMPORAIRES SONT UN DERNIER RECOURS : la regle ABSOLUE 4
   impose les outils du cerveau. Les combos ASCII existent et couvrent le
   besoin (verification + correction) : les utiliser, pas les contourner.
3. LE COMBO --full EST RAPIDE ET SUR : dry ~1 s (scan projet entier), wet ~3 s
   (correction ciblee uniquement des fichiers detectes). Pas besoin de
   scripts ad hoc.
