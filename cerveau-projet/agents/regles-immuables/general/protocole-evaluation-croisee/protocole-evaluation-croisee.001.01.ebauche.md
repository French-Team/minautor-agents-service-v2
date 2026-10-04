---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole d Evaluation Croisee (v1)

**Version** : 0.1.0
**Statut** : Ebauche
**Date creation** : 2026-09-05
**Agent** : Buffy (documentation de la reference verbale, suite rapport
Themis evaluation-croisee-periodique-2026-09-05-1835.md)

> **Pourquoi ce protocole ?** Le protocole evaluation croisee v1 etait une
> reference VERBALE (aucun fichier dedie). Les rapports
> [evaluation-croisee-periodique-2026-09-02-2035.md](../../../themis/rapports/evaluation-croisee-periodique-2026-09-02-2035.md),
> [evaluation-croisee-periodique-2026-09-02-2045.md](../../../themis/rapports/evaluation-croisee-periodique-2026-09-02-2045.md)
> et
> [evaluation-croisee-periodique-2026-09-05-1835.md](../../../themis/rapports/evaluation-croisee-periodique-2026-09-05-1835.md)
> en etaient les instances reelles. Ce document officialise le declenchement,
> le format du rapport et les regles de l evaluation croisee periodique.
**Historique** : v0.1.0 (creation, 2026-09-05)

---

## Objectif

Definir la procedure d EVALUATION CROISEE PERIODIQUE des agents actifs d un
round : declenchement automatique, format du rapport, regles de l evaluatrice
(Themis) et lien avec le modele aero (fin vers ORACLE).

**Pourquoi ce protocole ?**
- L evaluation croisee se repete (routine notation toutes les 960s +
  consommateur [NOTATION]) : le declenchement doit etre standardise
- Les rapports suivent deja un format stable (tableau agents + verdicts +
  coherence + verdict global + points d attention) : il doit etre documente
- Themis a des regles specifiques (ne corrige jamais, verdict avec preuves,
  rapport = seul ecrit) : elles doivent etre graves

---

## Prerequis

| # | Condition | Detail |
|---|---|---|
| 1 | Routine notation active | `cerveau-projet/agents/tools/oracle/routines/notation.py` depose une demande `[NOTATION]` dans l inbox d Oracle toutes les 960s |
| 2 | Consommateur [NOTATION] | `oracle.py` v0.5.9+ : `_consommer_notation()` convertit chaque demande non-acquittee en mission Themis (EVALUATION CROISEE) via `files.ajouter(mission, file=asap, agent=themis)` |
| 3 | Anti-inondation | Pas de depot si une mission Themis d evaluation est deja EN_ATTENTE OU si un depot a eu lieu il y a moins de 60 min (fichier `.notation_consommation.txt`) |
| 4 | Agent Themis actif | Fiche + corrections lues, carte theme-audit suivie (pilote) |
| 5 | Rapports precedents disponibles | `themis/rapports/evaluation-croisee-periodique-*.md` (instances reelles du format) |

---

## Etapes

```
DECLENCHEMENT -> MISSION THEMIS -> PARCOURS AUDIT -> RAPPORT -> FIN
      1              2               3               4         5
```

| Etape | Action | Detail | Outils |
|---|---|---|---|
| E1 | Declencher | La routine `notation.py` depose `[NOTATION]` dans l inbox d Oracle toutes les 960s | routine notation (oracle/routines/notation.py) |
| E2 | Convertir en mission | Le consommateur `_consommer_notation()` convertit la demande en mission Themis `EVALUATION CROISEE` (file asap, agent themis) -- anti-inondation 60 min | oracle.py cmd_lire / cmd_acquitter |
| E3 | Suivre le parcours audit | Themis relit SA fiche + SES corrections, puis suit SON arbre (theme AUDIT) : lecons domaine audit, activite recente, combo audit-general, conformite d execution, impacts, fins Pattern 13 | guider-arbre / pilote, consulter-lecons, lire-activite-recente, combos-audit-general, detecter-impacts |
| E4 | Produire le rapport | Ecrire le rapport dans `themis/rapports/evaluation-croisee-periodique-<AAAA-MM-JJ>-<HHMM>.md` au format ci-dessous (section "Format du rapport") | write, valider-conformite-ascii |
| E5 | Terminer | La fin de Themis suit SA carte (Pattern 13, modele aero R1/R3) : `oracle.py reactiver-fin themis --cible oracle` -- JAMAIS cerberus directement | oracle reactiver-fin |

---

## Format du rapport

Le rapport d evaluation croisee periodique contient obligatoirement les
sections suivantes (dans l ordre) :

| # | Section | Contenu |
|---|---|---|
| 1 | Frontmatter | `identite: type rapport, appartient_a themis, commun false` |
| 2 | En-tete | Titre, Date, Source (routine notation / mission), Type (evaluation croisee periodique) |
| 3 | Contexte | Ce qui s est passe dans le round evalue (reprise, migration, clotures...) |
| 4 | Agents actifs evalues | Tableau `| Agent | Travail du round | Verdict |` : une ligne par agent actif, verdict `+ Conforme (...)`. / `- Non conforme (...)`. avec justification |
| 5 | Verification de coherence des livrables | Tableau `| Point | Resultat |` : croisement des livrables annonces vs reels (rapports presents, etats cartes, fins, historique) |
| 6 | Resultat du combo audit-general (si lance) | Score global /100 + analyse des familles d erreurs (vrais ecarts vs faux positifs structurels documentes) |
| 7 | Verdict global | **AGENTS ACTIFS CONFORMES (+) / NON CONFORMES (-)** + justification courte |
| 8 | Points d attention | Liste numerotee des recommandations / surveillances |

---

## Regles de l evaluatrice (Themis)

| # | Regle | Detail |
|---|---|---|
| R1 | Ne corrige JAMAIS | Themis DETECTE et SIGNALE ; elle ne modifie aucun fichier de travail des autres agents |
| R2 | Verdict avec preuves | Chaque verdict +/- s appuie sur des preuves concretes (rapports, etats, fins, historique) -- jamais une impression |
| R3 | Rapport = seul ecrit | Le rapport dans `themis/rapports/` est SON SEUL ecrit (hors lecons BDD v1, corrections.md gele) |
| R4 | Distinguer vrais ecarts / faux positifs | Le combo audit-general remonte des faux positifs structurels connus (tests .py purs, dossiers non-agents, options CLI reelles, placeholders `protocole-X/` dans les tableaux de versioning) : les analyser, ne pas les compter comme ecarts reels |
| R5 | Fins Pattern 13 | La fin de Themis va vers ORACLE (modele aero R1/R3) -- le pilote decide du suivant |

---

## RVAV

| Etape RVAV | Action pour ce protocole |
|---|---|
| [R]echercher | Rassembler les rapports precedents (3 instances), le mecanisme de declenchement (notation.py + oracle.py v0.5.9+), la carte themis (theme-audit), la convention-protocoles |
| [V]erifier | Le format du rapport documente correspond aux 3 rapports reels ; le declenchement documente correspond au code (consommateur + anti-inondation) ; les regles R1-R5 sont celles appliquees par Themis |
| [A]nalyser | Le protocole doit rester un DOCUMENT de reference (pas un doublon du code) : decrire le mecanisme, pas reimplementer la logique |
| [V]alider | Verdict VALIDE si E1-E5 documentes, format du rapport complet, regles R1-R5 graves |

---

## Exemples

### Exemple 1 : declenchement automatique (2026-09-02, 20:35)

```
Routine notation -> demande [NOTATION] dans inbox Oracle
Consommateur _consommer_notation() -> mission Themis 0d3992df (EVALUATION CROISEE)
Themis suit theme-audit -> rapport evaluation-croisee-periodique-2026-09-02-2035.md
Preuve bout en bout : la boucle [NOTATION] est fermee (v0.5.9)
```

### Exemple 2 : 2e passe sur un nouveau livrable (2026-09-02, 20:45)

```
Vulcain termine le cablage nemesis (mission 8074e47a)
Le consommateur re-convertit une demande -> mission Themis 6dd150d2
Themis evalue UNIQUEMENT le nouveau livrable (tableau Point/Resultat, verdict VULCAIN +)
Format allonge : verdict cible par livrable au lieu de la grille agents complete
```

### Exemple 3 : reprise post-redemarrage + migration v1->v2 (2026-09-05, 18:35)

```
Redemarrage de session : 8 etats-cartes reinitialises par Cerberus
Oracle cloture 4 alertes obsoletes + relaie l evaluation (mission 6df6adb8)
Themis : grille agents complete (Cerberus/Oracle/Morpheus/Janus tous +)
Combo audit-general 58/100 analyse : 100% faux positifs structurels connus
Rapport -> points d attention : affiner evaluer-coherence + documenter ce protocole
```

---

## Pieges courants

| Piege | Consequence | Parade |
|---|---|---|
| Compter les faux positifs du combo comme ecarts | Verdict - injustifie | Analyser chaque famille d erreurs (R4) : tests .py purs, dossiers non-agents, options CLI, placeholders protocole-X |
| Evaluer des agents non actifs du round | Rapport hors sujet | N evaluer QUE les agents avec DEBUT/FIN dans le round (lire-activite-recente) |
| Verdict sans preuve | Credibilite de l evaluation | Toujours citer le livrable concret (rapport, etat carte, fin, historique) |
| Corriger au lieu de signaler | Violation perimetre Themis | R1 : DETECTER et SIGNALER, ne JAMAIS corriger |
| Fin vers Cerberus | Violation modele aero R1/R3 | R5 : fin vers ORACLE via reactiver-fin --cible oracle |
| Oublier l anti-inondation | Missions Themis en rafale | Le consommateur ne depose pas si mission EN_ATTENTE ou depot < 60 min |

---

## Liens

| Reference | Usage |
|---|---|
| [convention-protocoles](../../../conventions/protocoles/convention-protocoles.md) | Structure des protocoles (en-tete + 7 sections) |
| [rvav-workflow](../rvav-workflow.md) | Boucle obligatoire avant verdict |
| [regles-veracite](../regles-veracite.md) | Ne jamais mentir ou inventer |
| [regles-emojis-ascii](../regles-emojis-ascii.md) | ASCII strict |
| [theme-audit themis](../../../themis/parcours/theme-audit.json) | Carte du parcours AUDIT suivi par Themis |
| [rapport 2026-09-02 20:35](../../../themis/rapports/evaluation-croisee-periodique-2026-09-02-2035.md) | Instance reelle 1 (declenchement [NOTATION] + grille agents) |
| [rapport 2026-09-02 20:45](../../../themis/rapports/evaluation-croisee-periodique-2026-09-02-2045.md) | Instance reelle 2 (verdict cible par livrable) |
| [rapport 2026-09-05 18:35](../../../themis/rapports/evaluation-croisee-periodique-2026-09-05-1835.md) | Instance reelle 3 (reprise + migration, points d attention) |
| [notation.py](../../../tools/oracle/routines/notation.py) | Routine de depot des demandes [NOTATION] (toutes les 960s) |
| [oracle.py](../../../tools/oracle/oracle.py) | Consommateur [NOTATION] v0.5.9+ (conversion demande -> mission Themis) |
| [protocole-verification-coherence](../protocole-verification-coherence/) | Protocole voisin : verification de coherence (Themis) |