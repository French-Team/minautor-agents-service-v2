# CONTROLE P-A + P-B : EDITER-FICHIER POUR CLIO - 2026-08-24

## Mission de controle (ecrite AVANT, regle 1)
Controle de la reparation (decision utilisateur) :
1. **P-A** : indice editer-fichier ajoute en c20 carte clio (bump 0.6.5 -> 0.6.6), Pattern 14 fiche sync.
2. **P-B** (audit Themis) : fiche Clio alignee - 3 occurrences 'UNIQUE outil mettre-a-jour-readme' (l.48/124/282) assouplies pour editer-fichier (corrections ciblees readme-dev).

## Verifications prevues
- Carte clio : indice c20 present, version 0.6.6, valider-cartes-decision CONFORME
- Fiche clio : PARCOURS v0.6.6 + regles alignees (plus de contradiction)
- Verrou editer-fichier : source = cartes -> clio habilitee
- ASCII carte + fiche
- Registre buffy

## Verdict : (a remplir)

## VERDICT FINAL : VALIDE

### Verifications executees
1. **Carte clio** : CONFORME (valider-cartes-decision 10/10), version 0.6.6, indice outil editer-fichier present en c20 (avec lire-fichier + valider-conformite-ascii) - OK
2. **Fiche clio** : PARCOURS v0.6.6 (Pattern 14 sync), regle "README UNIQUEMENT" assouplie - 3 occurrences (l.48/124/282) alignees sur la decision utilisateur 2026-08-24 (editer-fichier autorise pour corrections ciblees readme-dev) - OK
3. **ASCII** : carte + fiche 0/0 non conforme - OK
4. **Registre buffy** : usages complets (editer-fichier x3, valider-cartes-decision, enregistrer-lecon, editer-parcours) - OK

### Conclusion
Reparation P-A (indice editer-fichier en c20 carte clio, decision utilisateur) et P-B (fiche clio alignee, audit Themis) : 0 defaut. Le verrou editer-fichier (source = cartes) habilite desormais Clio. AUCUN inter-round necessaire.
