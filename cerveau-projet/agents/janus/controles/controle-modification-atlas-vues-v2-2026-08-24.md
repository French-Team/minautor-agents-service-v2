# Controle de la mission education Atlas arbres v2 (Chiron + Buffy)

- **Date** : 2026-08-24
- **Agent controle** : Chiron (education) + Buffy (inter-round, corrections carte)
- **Mission** : eduquer Atlas pour generer le dossier .md + .svg des agents v2
  (ARBRES de decision, pas des cartes v1)

## Points a verifier (AVANT verdict)

1. **Carte Atlas** : parcours-atlas.json v0.5.6 -> v0.5.7, branche `vues-v2`
   dans c1 -> case c35 (action : convertir-carte-mermaid --arbres + dossier
   dedie atlas/rapports/vues-v2-<AAAAMMJJ>/), suivant -> c10.
2. **Fiche Atlas** : atlas.md PARCOURS v0.5.7 + REGLE MISSION VUES V2
   (difference arbre v2 vs carte v1) + METHODE RIGOUREUSE v0.5.7.
3. **Conformite carte** : valider-cartes-decision --agent atlas CONFORME.
4. **Lock marbre** : cartes-lock.json empreinte parcours-atlas.json a jour.
5. **Livrable** : dossier atlas/rapports/vues-v2-2026-08-24/
   (dossier-complet-vues-v2-2026-08-24.md, 9 agents, 19 liens OK).
6. **Outils sous-jacents** : convertir-carte-mermaid v0.3.0 (--arbres),
   test-101 11/11 OK (verifie precedemment par Janus, VALIDE).
7. **Normes** : ASCII 0/0 sur carte, fiche, dossier, rapport Chiron,
   corrections chiron/buffy.
8. **Perimetre** : seuls les fichiers de la mission modifies.

## VERDICT : VALIDE (0 defaut)

**Verifications** :
- Carte Atlas v0.5.7 : branche `vues-v2` dans c1 -> case c35 (action : convertir-carte-mermaid --arbres + dossier dedie atlas/rapports/vues-v2-<AAAAMMJJ>/), suivant -> c10. valider-cartes-decision CONFORME.
- Fiche Atlas : PARCOURS v0.5.7 + REGLE MISSION VUES V2 (difference arbre v2 vs carte v1) + METHODE RIGOUREUSE v0.5.7 (3 occurrences v0.5.7).
- Lock marbre : empreinte parcours-atlas.json a jour (anti-contournement OK).
- Livrable : atlas/rapports/vues-v2-2026-08-24/dossier-complet-vues-v2-2026-08-24.md (9 agents, 19 liens OK, ASCII 0/0).
- Navigation c1 -> c35 fonctionnelle (guider).
- Sous-jacents : convertir-carte-mermaid v0.3.0 (--arbres) + test-101 11/11 OK (controle Janus precedent VALIDE).
- Combo controle-modification : termine (nommage, liens, separation, sante, tableaux, surcharge, traces externes valides).
- Normes : ASCII 0/0 sur carte, fiche, rapport Chiron, controle, dossier.
- Perimetre : seuls les fichiers de la mission modifies (les autres fichiers atlas/chiron/janus modifies sont des missions anterieures de la journee).

**Lecons** :
1. UNE EDUCATION D AGENT (Chiron) PASSE PAR LE VERROU HABILITATION : Chiron diagnostique et propose (rapport), Buffy applique (inter-round) - la carte d'un agent est EXCLUSIVE a Buffy, meme pour l'educateur.
2. LA FICHE DOIT SUIVRE LE BUMP DE CARTE (Pattern 14) : valider-cartes-decision exige fiche PARCOURS == parcours.version - ici 3 occurrences v0.5.7 synchronisees + nouvelle REGLE MISSION VUES V2 documentee.
3. LE DOSSIER DEDIE (METHODE RIGOUREUSE) S'APPLIQUE AUSSI AUX VUES V2 : le dossier complet vues-v2-<AAAAMMJJ>/ contient la documentation, les .mmd/.svg vivent dans cartes-vues/arbres/ (source outil) - separation documentation (atlas) / generation (outil).

**Preuves** : controle-modification-atlas-vues-v2-2026-08-24.md, valider-cartes-decision CONFORME, lock marbre OK, dossier vues-v2 19 liens OK, test-101 11/11, ASCII 0/0.
