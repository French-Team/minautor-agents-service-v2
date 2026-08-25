---
identite:
  type: controle
  appartient_a: janus
  commun: false
---
# Controle -- corrections de formation de Clio pour readme-v2 (Janus)

**Date** : 2026-08-23
**Active par** : Buffy (maillon de chaine, dernier maillon)
**Objet** : second controle final de la chaine : Buffy (corrections fiche+carte Clio pour readme-v2) -> Themis (audit) -> Janus (controle final).

## Verdict

**VALIDE** -- apres inter-round : le defaut D1 (OUTIL_HORS_CARTE themis -> valider-conformite-ascii) a ete CORRIGE par Buffy (carte themis v0.5.9, case c9 enrichie avec l indice valider-conformite-ascii, fiche sync Pattern 14). Re-controle : evaluer-processus 0 probleme. La mission Buffy (corrections Clio pour readme-v2) est CONFORME, tous les points verts.

## Verifications

| # | Point | Resultat |
|---|---|---|
| C1 | valider-cartes-decision --agent clio : CONFORME 10/10 (JSON, references, Pattern 14 fiche v0.6.5 == parcours 0.6.5, commandes fins) | OK |
| C2 | Navigation reelle readme-v2 : c1 -> readme-v2 -> c22 (Rediger dry-run) -> c23 (Validation utilisateur) | OK |
| C3 | E1-E4 Chiron corriges : branche readme-v2, cases c22/c23, EXCEPTION REDACTION V2, SOURCES DE VERITE V2 (bloc + Connexions), ton v2 badges | OK |
| C4 | Lecons : Buffy (corrections.md + BDD 287, verdict VALIDE), Themis (corrections.md + BDD 288, verdict CONFORME) | OK |
| C5 | Registre usages : Buffy 12 outils declares (editer-parcours, editer-fichier, valider-cartes-decision, valider-case, valider-conformite-ascii, combos-moteur, guider-parcours, lire-fichier, lire-activite-recente, consulter-lecons, ajouter-contenu-fichier, enregistrer-lecon, activer-agent-principal), Themis outils declares | OK |
| C6 | ASCII 0/0 sur clio.md + parcours-clio.json + buffy/corrections.md + rapport Themis | OK |
| C7 | Combo controle-modification : termine sans erreur (nommage, liens, separation, sante, tableaux, surcharge, traces) | OK |
| C8 | Coherence rapport Themis vs sources : exact (12 points verifies, verdict CONFORME justifie) | OK |
| C9 | detecter-residus : 9 residus PRE-EXISTANTS (5 .bak + registre.bak + tmp-buffy/tmp-vulcain/.tmp-test004) - deja signales au controle precedent 20:59, domaine Hygie | PRE-EXISTANT |
| C10 | detecter-divergences-version : 1 DIVERGENT (activer-agent-principal spec 0.5.23 vs py 0.5.30) - deja connu (P2), Vulcain, mission separee | PRE-EXISTANT |
| C11 | evaluer-processus : 1 OUTIL_HORS_CARTE : themis -> valider-conformite-ascii declare au registre mais absent des indices de la carte themis (la carte ordonne combos-corriger-non-ascii en c9) | **DEFAUT** |

## Defaut signale (correction par Buffy, SEULE habilitee sur les cartes)

**D1 -- carte themis ne couvre pas valider-conformite-ascii** : pendant MON audit (Themis), j'ai utilise valider-conformite-ascii pour verifier l'ASCII du rapport, alors que la carte themis ordonnait combos-corriger-non-ascii (c9). L'usage est reel et declare au registre, mais evaluer-processus le signalait OUTIL_HORS_CARTE. Meme pattern que la lecon du 2026-08-20 (themis -> evaluer-processus) : un controleur qui utilise des outils d'audit manuels cree des usages qui doivent etre couverts par SA carte.

**RESOLUTION (inter-round)** : Buffy a ajoute l'indice outil valider-conformite-ascii (commande sur <fichier-rapport>) dans la case c9 de la carte themis via editer-parcours --modifier-case, bump 0.5.8 -> 0.5.9, sync fiche (Pattern 14), lock resync. Verifie : valider-cartes-decision themis CONFORME 10/10, evaluer-processus 0 probleme, ASCII 0/0. Lecon Buffy BDD id 289. Re-controle Janus : evaluer-processus 0 probleme -> D1 CLOS.

## Points hors perimetre deja signales (non imputables a la mission)

- P1 : clio/corrections.md 383 CRLF pre-existants (Hygie)
- P2 : 3 divergences d'outils (activer-agent-principal, editer-fichier, valider-cartes-decision) -> Vulcain (mission separee)

## Conclusion

La mission Buffy (corrections Clio pour readme-v2) est CONFORME : tous les points C1-C10 de la mission sont verts. Le seul defaut (D1) est un ecart de processus de Themis, hors perimetre de la mission auditee, correction via la boucle KO -> Buffy (carte themis).
