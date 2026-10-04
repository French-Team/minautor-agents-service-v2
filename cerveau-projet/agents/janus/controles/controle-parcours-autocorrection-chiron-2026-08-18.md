# Controle -- Parcours d auto-correction de Chiron (Janus)

- **Date** : 2026-08-18
- **Controleur** : Janus (second controle, active par Buffy c8)
- **Objet** : controle final de la mission auto-correction Chiron
  (parcours-chiron.json v0.3.0)
- **Verdict** : **VALIDE**

## Contexte

Demande utilisateur : Chiron pilote unique d auto-correction de SA carte
(detecter -> se re-eduquer -> corriger -> Themis verifie -> reprendre).
Pre-requis de la chaine : marbre exception pilote (Gardien, porte re-empreinte),
verrou cle exclusive chiron par cible v0.4.0 (Vulcain), editer-parcours v0.1.7
(cible transmise au verrou), test-056 + test-058 adaptes (Morpheus).

## Verifications sous session Janus

1. **valider-cartes-decision --agent chiron** : CONFORME (fiche PARCOURS
   v0.3.0 == parcours 0.3.0).
2. **Cycle d auto-correction** : c11b (question MA carte ?) -> c15 (se
   re-eduquer) -> c16 (corriger via editer-parcours) -> c17 (activer Themis)
   -> c18 (reprise, question d attente). Referents 0 manquant, budgets <= 3.0,
   textes nouveaux < 160.
3. **Verrou pilote** : chiron sur parcours-chiron.json -> OK ; chiron sur
   parcours-atlas.json -> BLOQUE (exclusif buffy). L auto-correction est
   strictement limitee a SA carte.
4. **test-058** : 6/6 CONFORME (exception chiron coherente : indices OUTIL
   + boucle texte).
5. **test-006** : 19/19. **test-027** : 11/11 (les KO 5-8 sous Morpheus
   etaient des artefacts de verrou : le lanceur est reserve a Janus).
6. **test-056** : 17/17 (verrou v0.4.0). **test-093** : 17/17 (combo --full
   ASCII, mission precedente).
7. **Bumper** : 0 outil incoherent. **Marbre** : 8/8 conforme.
8. **Evaluateur** : 15 liens preexistants (0 nouveau). **Registre JSONL** :
   682/682 valide. **Residus** : 0.
9. **Lock cartes** : hash parcours-chiron.json MATCH.

## Point d attention (preexistant, non bloquant)

- Textes de regles > 160 caracteres dans les cases c1-c14 de la carte chiron
  (preexistants a la mission, non modifies). Test-016 ne controle que la carte
  de Buffy : aucun impact.

## Verdict

**VALIDE** -- le parcours d auto-correction de Chiron est complet, le verrou
pilote le limite a SA carte, tous les tests et garde-fous sont verts sous la
session habilitee. La chaine est terminee : je REACTIVE Cerberus avec le bilan
consolide.
