# Rapport d'audit -- Reparation Buffy (2026-08-21)

**Date** : 2026-08-21
**Auditrice** : Themis (evaluatrice croisee)
**Mission auditee** : Reparation Buffy (boucle KO Janus) -- carte cerberus c45b/c46b non conformes + integration socrate (fins Activer Janus, c1b, cerberus.md, cartes mermaid) + correctif outil convertir-carte-mermaid multi-parcours + pins de tests adaptes.
**Active par** : Buffy (relais de chaine, carte Buffy c8a)

---

## VERDICT : CONFORME apres correction (D1 corrige par Buffy en boucle KO)

**Mise a jour (meme jour, boucle KO)** : Buffy a resynchronise
cartes-lock.json pour parcours-cerberus.json (fonction officielle
empreinte_fichier d'editer-parcours) - 20/20 cartes synchronisees,
ASCII 0 CRLF 0, lecon ajoutee dans buffy/corrections.md
("REPARATION D1"). Le defaut D1 est CORRIGE et re-verifie independamment.

La reparation est globalement CONFORME (structure, contenu, normes, execution) mais un defaut d'integration est reste : la carte cerberus a ete modifiee hors editer-parcours (description ecrite en write_bytes direct) apres la derniere resynchronisation du lock, ce qui a desynchronise cartes-lock.json pour parcours-cerberus.json.

## Points verifies (re-executes independamment)

1. **Carte cerberus (c45/c45b/c46/c46b)** : CONFORME -- version 0.5.9,
   c45 et c46 sont des actions avec `suivant` (c45b / c46b), c45b et c46b
   sont des controles avec `branches[]` (OUI -> c24, NON -> c45/c46).
   Plus AUCUNE case avec branche_vraie/branche_fausse dans la carte.
2. **Integration socrate (4 parcours)** : CONFORME -- parcours-socrate,
   revision-audit, revision-generale, revision-urgence tous en version 0.1.2,
   fins principales "FIN - Activer Janus" (REGLE IMMUABLE JANUS : seule la
   carte janus a la fin Reactiver Cerberus). Case orpheline c1b recablee :
   c1.suivant = c1b, c1b branches OUI -> c2 / NON -> c1.
3. **cerberus.md tableau des agents** : CONFORME -- ligne 221 : Socrate
   ajoute (role, statut). valider-tableaux : 24 fichiers / 24 conformes.
4. **Outil convertir-carte-mermaid** : CONFORME -- v0.2.1, correctif
   multi-parcours : nom_fichier_parcours() derive le nom du fichier source
   (parcours-<agent>.json -> <agent>, sous-parcours -> <agent>-<sous>),
   filtre --agent conserve appartient_a. --verifier : 20 cartes
   synchronisees (.mmd + .svg). 8 fichiers socrate generes sans collision
   (socrate + 3 sous-parcours x .mmd/.svg).
5. **Pins de tests** : CONFORME -- test-013 22/22 (version 0.5.9),
   test-072 10/10 (agent resolu via identite.appartient_a), test-070 13/13,
   test-094 7/7, test-096 11/11.
6. **Normes** : 52 fichiers du perimetre (cartes, .md, .py, tests, .mmd,
   .svg) ASCII strict + LF purs (0 CRLF).
7. **Marbre** : proteger-verrou-marbre --tous : 8 zones conformes.
8. **Pattern 14** : fiche cerberus.md PARCOURS (v0.5.9) == parcours 0.5.9 ;
   fiche socrate.md PARCOURS (v0.1.2) == parcours 0.1.2.
9. **Conformite d'execution (c8b)** : Buffy a suivi sa carte -- traces au
   registre : editer-parcours (correction cases cerberus + c1b socrate),
   valider-cartes-decision, valider-case, valider-tableaux,
   convertir-carte-mermaid, mettre-a-jour-versions (bump 0.2.1), lecon
   ajoutee dans buffy/corrections.md. Outils conformes a la carte Buffy.
10. **Verification d'impact (c8c)** : le correctif convertir-carte-mermaid
    a change les 20 sorties .mmd/.svg + index.md -- toutes regenerees et
    synchronisees (--verifier rc=0). Pins des tests impactes (test-013,
    test-072) adaptes.

## DEFAILLANCE D1 : cartes-lock.json desynchronise pour parcours-cerberus.json

**Constat** : l'empreinte SHA-256 de parcours-cerberus.json dans
cartes-lock.json (35c83e9a...) ne correspond pas a l'empreinte actuelle du
fichier (49b211c3...) calculee avec la fonction officielle d'editer-parcours
(empreinte_fichier : LF + rstrip par ligne).

**Cause** : la description de la carte a ete modifiee par ecriture directe
(write_bytes) APRES le bump via editer-parcours (qui resynchronise le lock a
chaque ecriture). La carte (18:33) est plus recente que le lock (18:11).

**Impact** : la prochaine modification de la carte cerberus via
editer-parcours sera REFUSEE (anti-contournement, barrage n3) -- le lock
divergent bloque l'ecriture.

**Agent habilite** : Buffy (editer-parcours est exclusif buffy/chiron).
Correction : resynchroniser l'empreinte de parcours-cerberus.json dans
cartes-lock.json (via editer-parcours ou mettre-a-jour-versions
resynchroniser_cartes_lock).

## Points conformes en detail

- les 20 cartes du lock : 19 synchronisees, 1 divergente (cerberus, D1)
- test-057 marbre garde-fou : 24/24 OK (il verifie l'existence du lock,
  pas la synchronisation des empreintes -- d'ou le defaut non detecte)
- valider-case sur parcours-themis : CONFORME (0 erreur, 0 a alleger,
  0 avertissement)

## Lecons

1. UNE ECRITURE DIRECTE (write_bytes) SUR UNE CARTE VERROUILLEE
   DESYNCHRONISE LE LOCK SANS LE SIGNALER : editer-parcours resynchronise a
   CHAQUE ecriture, mais une ecriture hors outil ne met pas a jour
   cartes-lock.json. Apres TOUTE modification directe d'une carte, verifier
   l'empreinte du lock (fonction officielle : LF + rstrip par ligne) avant
   de conclure.
2. LES GARDE-FOUS EXISTANTS (test-057, valider-cartes-decision) NE
   VERIFIENT PAS LA SYNCHRONISATION DES EMPREINTES : ils verifient
   l'existence du manifeste et la conformite structurelle, pas la
   correspondance lock <-> fichier. Un audit croise doit recalculer les
   empreintes avec la fonction d'editer-parcours.
3. LA MISSION DE REPARATION BUFFY EST CONFORME DANS SON CONTENU : les
   corrections de fond (format branches[], fins socrate, multi-parcours
   mermaid) sont exactes et validees par les tests dedies -- le seul ecart
   est un defaut d'integration (resync lock oubliee).

---

**Rapport** : cerveau-projet/agents/themis/rapports/rapport-audit-reparation-buffy-2026-08-21.md
