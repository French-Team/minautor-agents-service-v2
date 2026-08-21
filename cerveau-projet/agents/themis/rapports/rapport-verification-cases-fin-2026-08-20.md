# Verification Cases FIN - Vulcain / Buffy / Clio (2026-08-20)

**Agent auditrice** : Themis
**Demande utilisateur** : verifier que les cases FIN des cartes parcours-vulcain.json,
parcours-buffy.json et parcours-clio.json contiennent " activer agent suivant " (activer le
maillon suivant de la chaine) et NON " activer/ reactiver Cerberus " (sauf si l'agent est le
dernier maillon de sa chaine).
**Reference** : Pattern 13 -- LA FIN SUIT SA CARTE (activation directe par Cerberus ->
reactiver Cerberus ; maillon de chaine -> activer le suivant ; dernier maillon -> reactiver
avec bilan consolide).

---

## VERDICT : A REVOIR - 3 ecarts de contenu + 1 incoherence de version (Pattern 14)

Les fins PRINCIPALES de mission sont correctes (activer l'agent suivant). Les ecarts portent
sur des cases de REPRISE (messages obsoletes referencant " c13 (FIN - Reactiver Cerberus) ")
et la branche documentation de vulcain.

---

## CONFORME (fins principales = " activer agent suivant ")

### Buffy - c8 / c22 / c27 " FIN - Activer Janus "
- Commande exacte : `activer <session> janus '<raison>'`
- Message : " J ACTIVE JANUS (second controle) ... COMMANDE EXACTE (commandes activer, PAS
  reactiver - reactiver ramene toujours a Cerberus) "
- La chaine continue : Janus controle puis REACTIVE Cerberus avec son verdict
- **CONFORME** : Buffy active l'agent suivant (Janus), elle ne reactive PAS Cerberus

### Clio - c12 " FIN - Activer Janus "
- Commande exacte : `activer <session> janus '<raison>'`
- Message : " MA MISSION DE MISE A JOUR DU README EST TERMINEE ... J ACTIVE JANUS (second
  controle) ... reactiver ramene toujours a Cerberus "
- **CONFORME** : Clio active l'agent suivant (Janus)

### Vulcain - c9 / c15 " FIN - Construire / Modifier un outil "
- Message : " MORPHEUS ACTIVE pour les tests. La chaine continue : Morpheus teste puis ACTIVE
  Janus (controle) qui REACTIVE Cerberus avec le bilan consolide "
- La commande d'activation de Morpheus est portee par c8/c14 (controle " Deleguer les tests a
  Morpheus " : `activer <session> morpheus "TESTER ..."`)
- **CONFORME** : Vulcain active l'agent suivant (Morpheus), la chaine continue vers Janus

---

## ECARTS A CORRIGER (REGLE 4 - je signale, je ne corrige pas)

### E1. Buffy c15e " FIN - Reprise du parcours apres retour de l'agent habilite "
- Message obsolete : " je continue vers ma fin normale c13 (FIN - Reactiver Cerberus) "
- **La case c13 n'EXISTE PAS dans la carte buffy** (les fins sont c8/c22/c27 Activer Janus,
  c13d, c15e, c35, c35d, c36, c39, c41)
- La fin normale de Buffy est " Activer Janus " (c8/c22/c27), PAS " Reactiver Cerberus "
- **A corriger** : le message doit pointer vers la fin reelle (Activer Janus), pas vers une
  case inexistante " Reactiver Cerberus "

### E2. Clio c10e " FIN - Reprise du parcours apres retour de l'agent habilite "
- Message obsolete : " je continue vers ma fin normale c13 (FIN - Reactiver Cerberus) "
- **La case c13 de clio est " Mission hors parcours "** (question de redirection), PAS une fin
- La fin normale de Clio est c12 " Activer Janus ", PAS " Reactiver Cerberus "
- **A corriger** : meme probleme que E1 - reference a une c13 qui n'est pas une fin
  " Reactiver Cerberus "

### E3. Vulcain c9e / c15e " FIN - Reprise du parcours apres retour de l'agent habilite "
- Message obsolete : " je continue vers ma fin normale c13 (FIN - Reactiver Cerberus) "
- **La case c13 de vulcain est " Lancer le combo corriger-ascii "** (action), PAS une fin
- La fin normale de vulcain pour un outil est c9/c15 (chaine Morpheus -> Janus), PAS
  " Reactiver Cerberus "
- **A corriger** : meme probleme que E1/E2

### E4. Vulcain c16d " FIN - Documentation " (branche documentation c16b-c16c-c16d)
- Message : " Je REACTIVE Cerberus avec le bilan consolide : commande reactiver <session>
  <raison> <agent_precedent> "
- Selon la demande utilisateur, les fins de vulcain doivent " activer agent suivant ", pas
  " reactiver Cerberus " - sauf si vulcain est le dernier maillon de sa chaine
- **A verifier/corriger** : si la documentation est un maillon de chaine, la fin devrait
  activer l'agent suivant (Janus/Themis) ; si c'est une mission directe de Cerberus
  (activation directe), reactiver Cerberus est le bon Pattern 13. A trancher avec Cerberus.

### E5. VULCAIN - INCOHERENCE DE VERSION FICHE/CARTE (Pattern 14 - P10)
- **Fiche vulcain.md** : " REGLE ABSOLUE -- PARCOURS (v0.6.0) "
- **Carte parcours-vulcain.json** : `parcours.version` = 0.5.2
- Au HEAD git : fiche v0.5.2 == JSON 0.5.2 (coherent) - la fiche a ete bumpee a 0.6.0 dans
  le working tree SANS bumpe du JSON correspondant
- **A corriger** : synchroniser la fiche (v0.5.2) ou bumpe le JSON (0.6.0) - les deux doivent
  porter la meme version

---

## Points verifies conformes (sans defaut)

- **Cartes valides** : JSON parses OK, 0 non-ASCII, 0 CRLF sur les 3 cartes + 3 fiches
- **Lock** : les 3 cartes (vulcain, buffy, clio) sont presentes dans cartes-lock.json
- **Marbre** : 8/8 intact (exit 0)
- **Buffy c8/c22/c27, Clio c12** : les messages " commandes activer, PAS reactiver " sont
  deja conformes a la regle
- **Fin de chaine coherente** : Janus (controle) est le maillon qui REACTIVE Cerberus avec le
  verdict - conforme Pattern 13 pour les missions principales

---

## Agent habilite pour corriger
- **Buffy** (editer-parcours + mise a jour version fiche, comme pour les cartes themis/janus/
  socrate) : corriger les messages c15e (buffy), c10e (clio), c9e/c15e/c16d (vulcain) et
  synchroniser la version fiche vulcain.

---

## Lecon
Le Pattern 13 (fin suit SA carte) est la reference pour les cases FIN : " activer agent
suivant " pour les maillons de chaine, " reactiver Cerberus " uniquement pour les activations
directes ou le dernier maillon. Les messages de REPRISE (c15e/c10e/c9e) ont ete copies d'un
parcours a l'autre et referencent des cases c13 " FIN - Reactiver Cerberus " qui n'existent
pas dans les cartes cibles - verifier TOUJOURS que les references de cases dans les messages
pointent vers des cases reelles et vers la fin reelle de la carte.
