# Rapport d'audit -- Janus, controleur des statuts (conformite + utilisation)

**Date** : 2026-08-09
**Evaluatrice** : Themis (procedure 4i complete)
**Agent audite** : Janus (controleur des statuts)
**Question utilisateur** : Janus est-il utilise QUAND IL FAUT ?

---

## 1. Structure du parcours Janus (v0.2.1)

| Point | Resultat |
|---|---|
| valider-cartes-decision --agent janus | **CONFORME** (JSON valide, c0 question relecture, references valides) |
| Cases | 27 (19 indice, 3 question, 3 fin, 2 controle) |
| Chemins | c2 outil / c11 statut / c18 modification (c1 Mission a 4 branches) |
| Combos branches | c5 combo-controle-outil, c22 combo-controle-modification (definitions existent) |
| Fiche | Reference le parcours (source de verite) |
| index-agents | Janus present (fiche + corrections) |
| ASCII | 0 |

**Patterns** : P1 multi-missions OK, P2 ASCII OK, P4 c0 question honnete OK, P6 contexte temps reel OK, P3 combos OK, reactiver OK.

## 2. Point 6 -- Reactivation (critere reactiver R1-R5)

| Mission Janus | Trace reactivation | Point 6 |
|---|---|---|
| 2026-08-09 08:26 controle detecter-impacts | 08:27 MISSION TERMINEE (Janus) sous Cerberus | CONFORME |
| 2026-08-09 08:35 scan regle des 5 fichiers | 08:38 MISSION TERMINEE (Janus) sous Cerberus | CONFORME |
| 2026-08-08 21:46 controle generateurs-carte (chaine bout-en-bout) | Reactivation Cerberus avec bilan consolide | CONFORME |

**VERDICT POINT 6 : CONFORME (3/3 missions, R1-R5 verifies via traces + bloc + profil).**

## 3. Conformite d'execution (Pattern 11) -- croisement mission/carte/deroulement

| Mission | Carte ordonnait | Realite | Statut |
|---|---|---|---|
| 08:26 controle detecter-impacts | chemin statut/outil : lire doc, verifier, verdict | Controleur qui SIGNALE sans corriger : verdict NON VALIDE (1 impact reel : la spec generateurs-commande) + analyse des artefacts. AUCUNE correction faite (domaine Vulcain) | OK |
| 08:35 scan regle des 5 fichiers | chemin statut : lister, verifier, verdict | Scan des 12 spec, croisement manuel (formats varies), verdict 5 ALIGNEES / 6 DIVERGENTES, aucune correction | OK |
| 21:46 controle generateurs-carte | chemin outil : lire, verifier tests, verdict | Controle du squelette cree par Vulcain apres verdict Morpheus 8/8, verdict conforme | OK |

**Verdict conformite d'execution : CONFORME** -- Janus joue son role de controleur (signale sans corriger, croise les preuves, lecons documentees).

## 4. Utilisation QUAND IL FAUT (question utilisateur)

### Janus est-il branche ?

| Point d'ancrage | Preuve | Statut |
|---|---|---|
| Carte de Cerberus | c14 Activer Janus (second controle), c15 Traiter le verdict de Janus | BRANCHE |
| Parcours Janus | 3 chemins (outil/statut/modification) + combos controle-* | BRANCHE |
| Combos | combo-controle-outil, combo-controle-modification, combo-controle-impacts | BRANCHE |
| Fiche + index-agents | Reference complete | BRANCHE |
| Chaine bout-en-bout (Pattern 8) | Janus = dernier maillon qui reactiver Cerberus (21:46) | BRANCHE |

### Janus a-t-il ete active pour les controles majeurs ?

| Controle majeur | Date | Janus active ? |
|---|---|---|
| Controle detecter-impacts generateurs-commande.sh | 08:26 | OUI (verdict NON VALIDE -> impact spec corrige) |
| Scan regle des 5 fichiers (12 spec) | 08:35 | OUI (6 divergences -> outil detecter-divergences-version cree) |
| Controle generateurs-carte v0.2.0 | 21:46 (08-08) | OUI (chaine bout-en-bout Morpheus -> Janus) |
| Controles historiques (parcours-atlas, corrections Pattern 2) | 08-07/08-08 | OUI |

### Cas de contournement identifies

- **Lecon Vulcain c14 (2026-08-09 08:25, rapport Themis)** : Vulcain a fait SES PROPRES validations (parite, ASCII, scan) au lieu d'activer Morpheus puis Janus -- l'audit a conclu NON CONFORME. La correction demandee : activer les agents habilites (Morpheus pour les tests, Janus pour le controle) au lieu de s'auto-valider. Ce cas confirme le RISQUE de contournement mais il a ete DETECTE et DOCUMENTE.
- Depuis cette lecon, les missions recentes respectent la delegation (ex: mission spec-guider-parcours v0.2.21 -> Buffy n'a pas fait de controle Janus mais c'etait une documentation, pas un controle de statut).

## 5. VERDICT GLOBAL

**CONFORME** -- Janus est structurellement conforme (parcours v0.2.1), execute ses missions conformement (controleur qui signale sans corriger), se reactive correctement (point 6 : 3/3), et est BRANCHE dans le systeme (carte Cerberus c14/c15, combos, fiche, index, chaine bout-en-bout).

**REPONSE A LA QUESTION : OUI, Janus est utilise quand il faut.** Il a ete active pour tous les controles majeurs du 2026-08-08/09 (detecter-impacts, scan spec, generateurs-carte). Le seul risque identifie (auto-validation de Vulcain c14) a ete detecte par l'audit de conformite et corrige dans les pratiques.

## 6. Recommandations

1. **Poursuivre** : maintenir le second controle Janus systematique apres les missions de modification (c14 carte Cerberus) -- c'est le garde-fou contre l'auto-validation.
2. **Surveiller** : les missions de documentation pure (comme celle de la spec v0.2.21) ne necessitent pas de controle Janus -- ne pas surcharger. Le critere : controle necessaire si MODIFICATION de fichiers outils/statuts.
3. **A generaliser** : la lecon c14 (Vulcain s'est auto-valide) devrait etre rappelee dans les cartes des agents qui modifient (meme approche que c14 parcours Vulcain).
