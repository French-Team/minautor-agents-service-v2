---
identite:
  type: rapport
  appartient_a: commun
  commun: true
---
# Rapport d'audit Themis -- conformite pedagogique des cartes des agents secondaires

**Date** : 2026-08-18
**Demande** : Cerberus - verifier si les agents secondaires (Atlas, Argus,
Hygie, Clio, Hermes, Gardien, Chiron, Athena, Promethee, Minerve) ont leur
carte conforme au modele pedagogique (re-education Themis v0.4.10 / Janus
v0.5.0 / 3 cartes principales v0.5.0).

## Modele de conformite pedagogique (reference)

1. **GARDE-FOU C1** : indice regle en c1 qui force la classification (branches
   explicites + cas "aucune branche -> autre"). Pour les agents a mission
   unique (c1 de type action), l equivalent est un indice qui dit quoi faire
   si la mission est hors perimetre.
2. **Redirection outil bloque** : quand le verrou bloque un outil (message
   BLOQUE), la carte ordonne de signaler et d activer l agent habilite.
3. **AGENTS HABILITES** : liste des agents habilites par domaine dans la case
   d activation.

## Verifications (10 cartes secondaires)

| Agent | Version | sync fiche | c1 indices | GARDE-FOU C1 | Redirection outil bloque | AGENTS HABILITES | Eduque par Chiron |
|---|---|---|---|---|---|---|---|
| **atlas** | 0.4.9 | OK | 0 | KO | KO | KO | JAMAIS |
| **argus** | 0.1.12 | OK | 0 | KO | KO | KO | JAMAIS |
| **hygie** | 0.1.8 | OK | 0 | KO | KO | KO | JAMAIS |
| **clio** | 0.5.13 | OK | 0 | KO | KO | KO | JAMAIS |
| **hermes** | 0.1.5 | OK | 0 | KO | KO | KO | JAMAIS |
| **gardien** | 0.1.3 | OK | 0 | KO | KO | KO | JAMAIS |
| **chiron** | 0.1.2 | OK | 1 (action) | NA (c1 action) | OK (c10/c11 signalent a Buffy/Vulcain) | KO (pas de liste) | NA (l educateur) |
| **athena** | 0.3.6 | OK | 0 | KO | KO | KO | JAMAIS |
| **promethee** | 0.3.7 | OK | 0 | KO | KO | KO | JAMAIS |
| **minerve** | 0.3.7 | OK | 0 | KO | KO | KO | JAMAIS |

Toutes les cartes sont **structurellement saines** : versions sync (carte =
fiche PARCOURS), cases "Mission hors parcours" presentes (argus/gardien/
hermes/hygie c29, clio c13, atlas c26, athena/promethee/minerve c18), cases
d activation presentes (atlas c27, athena/promethee/minerve c19, clio c14,
hygie c7/c9, argus c7/c8).

MAIS elles sont **pedagogiquement en retard**, exactement comme les cartes
principales avant re-education :
1. **c1 sans indice GARDE-FOU C1** : 0 indice pour 9 cartes sur 10 (seule
   exception : chiron, dont c1 est une ACTION a mission unique avec un indice
   "mission pas claire -> demander a Cerberus").
2. **Aucune redirection outil bloque** : si le verrou bloque un outil, la
   carte ne dit pas d activer l agent habilite (sauf chiron c10/c11 qui
   signalent a Buffy/Vulcain).
3. **Aucun indice AGENTS HABILITES** : les cases d activation n ont pas la
   liste des agents habilites par domaine.

Historique d education (BDD lecons) : Chiron n a eduque que Themis (#23) et
Janus (#34). Aucune lecon d education pour les agents secondaires.

## Verdict

**A REVOIR** -- les 10 cartes secondaires sont structurellement saines mais
pedagogiquement en retard : aucune n a le modele complet (GARDE-FOU C1,
redirection outil bloque, AGENTS HABILITES). Chiron est un cas particulier
(carte a mission unique, redirections c10/c11 presentes) mais sans liste
AGENTS HABILITES.

## Recommendation

Re-education des 10 cartes secondaires sur le modele etabli, avec adaptation
pour chaque carte (les branches de c1 et les cases cibles different) :
1. c1 : ajouter l indice GARDE-FOU C1 (classification) - ou pour chiron,
   completer l indice existant.
2. Ajouter la redirection "outil bloque" -> activer l agent habilite.
3. Ajouter l indice AGENTS HABILITES dans la case d activation.
4. Bump de version + synchronisation fiche (Pattern 14) + resync lock.
