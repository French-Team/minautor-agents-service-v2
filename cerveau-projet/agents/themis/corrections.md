---
identite:
  type: corrections
  appartient_a: themis
  commun: false
---

# Corrections -- Themis

> Fichier de suivi des corrections et lecons apprises par Themis.
> Chaque entree contient : date, contexte, erreur detectee, correction appliquee, lecon.

---

## Historique des corrections

| Date | Contexte | Erreur | Correction | Lecon |
|---|---|---|---|---|
| 2026-08-07 09:00 | Test Audit general en conditions reelles (9 etapes) | AGENTS-historique.md (racine) contenait U+00E9 corrompu dans 'cosmetique' -- detecte par combos-valider-cerveau (valider-conformite-ascii sans argument = scan racine) | Remplace par 'e' simple -- ASCII OK | Le combo scanne la racine (fichiers hors cerveau-projet/ inclus). Apres toute modification d'AGENTS-historique.md, verifier ASCII.
| 2026-08-07 09:00 | Test Audit general en conditions reelles (9 etapes) | evaluer-coherence a 50/100 : 10 liens 'casses' signales | Les 10 liens sont des exemples de documentation (blocs de code, exemples de resultat, syntaxe expliquee), pas des liens reels | Amelioration a planifier : evaluer-coherence doit ignorer les liens dans les blocs de code et les motifs generiques (ancien.md, texte, chemin, .*)
| 2026-08-07 | Inventaire des 78 outils | valider-tableaux signale 1 probleme : themis.md annonce 'Audit general (dont inventaires)' dans la table mais la section s'appelle encore '### Mission : Audit general' | Incoherence de nommage : suffixe ajoute a la table sans renommer le titre de section | Quand on renomme une mission dans la table, renommer AUSSI le titre de la section detaillee (### Mission : X) pour que valider-tableaux trouve la correspondance
| 2026-08-07 | Verification croisee Morpheus / protocole-tests | 2 incoherences mineures : lien frontmatter 'tools/tests/' casse (renommage en 'tester/' non reporte) + motif generique 'protection-*' vs noms reels 'tester-protection-*' dans les etapes | Rapport : themis/rapports/coherence-morpheus-protocole-tests-2026-08-07.md | Lors d'un renommage de dossier d'outils, verifier les fichiers_lies des fiches (frontmatter) et les motifs generiques des etapes
| 2026-08-07 14:21 | Audit general post-activation | evaluer-agents signale 79 faux erreurs '__pycache__' comme des outils manquants (dossiers d'artefacts Python comptes comme des outils) | Rapport : themis/rapports/audit-general-2026-08-07-14-21.md | CORRIGER evaluer-agents: exclure __pycache__ et les dossiers de categorie (parents des outils) | CORRIGER evaluer-agents pour exclure __pycache__ et les dossiers de categorie
| 2026-08-07 14:21 | Audit general post-activation | evaluer-coherence signale un lien casse faux positif: `../agents/conventions/protocoles/convention-protocoles.md` dans `recherches-web/badges-github-shields/badges-README-github.md` -- le fichier existe mais l'outil calcule cible_racine depuis cerveau-projet/ au lieu de la racine du projet | Rapport : themis/rapports/audit-general-2026-08-07-14-21.md | CORRIGER evaluer-coherence: utiliser le projet root comme racine pour cible_racine
| 2026-08-07 14:21 | Audit general post-activation | evaluer-coherence signale 4 faux outils casses (cat, grep, sed, basher) reference par athena -- commandes systeme listees en exemple dans la regle 'OUTILS EXCLUSIFS', pas des outils reels | Rapport : themis/rapports/audit-general-2026-08-07-14-21.md | CORRIGER evaluer-coherence: exclure les commandes systeme connues du scan des outils casses
| 2026-08-08 | Mise a jour du rapport serie parcours (decision utilisateur) | Le prototype vulcain (fins independantes par chemin) est passe de observation-a-corriger a CAS LEGITIME ASSUME | Rapport : themis/rapports/rapport-evaluation-serie-parcours-2026-08-08.md | Une observation d audit peut devenir un cas assume par decision utilisateur : mettre a jour le rapport (observation + recommandation + synthese) et la spec (v0.2.3) de facon SYNCHRONISEE pour garder la coherence audit/spec
| 2026-08-08 | Audit serie 11 parcours (conformite spec v0.2.0) | 2 ecarts MINEURS Pattern 2 : minerve c8 et promethee c8 (mise a jour d'index via editer-fichier) n'ont pas le rappel ASCII en tete de leurs indices + 1 caractere non-ASCII dans MON rapport (le mot 'anterieur' ecrit avec un accent) | Rapport : themis/rapports/rapport-evaluation-serie-parcours-2026-08-08.md | L'audit des 2 patterns est reproductible : (1) Pattern 1 = case Mission question + branches + convergence (--liste + lecture structurelle), (2) Pattern 2 = pour chaque case avec outil d'ecriture (creer/ecrire/editer/ajouter-contenu-fichier), verifier que le PREMIER indice est la regle ASCII. Les parcours de ROUTAGE (cerberus : 0 case d'ecriture) et le PROTOTYPE (vulcain : fins par chemin) sont des cas legitimes documentes. PIEGE RECURRENT : meme moi, evaluatrice, j'ai introduit un accent (anterieur) dans le rapport -- TOUJOURS re-valider l'ASCII du rapport APRES sa redaction, pas seulement le contenu audite. |

## [NOTES] Audit 2026-08-08 -- relecture QUESTION HONNETE dans les 11 parcours

**Audit** : verification que les lecons de la transformation de la relecture en QUESTION HONNETE (case c0 + c0b) sont appliquees dans les 11 parcours.
**Verdict** : CONFORME (100/100, 6/6 points sur les 11 parcours).
**Lecons** :
1. Le referentiel d'audit decoule des lecons de l'auteur (Buffy corrections.md) : 6 points verifiables mecaniquement (case_depart c0, question memoire, branches OUI/INCERTAIN/NON, c0b RELIRE + corrections + fiche, navigation OUI->c1 et c0b->c1, c1 mission presente)
2. PIEGE CRITERE D'AUDIT : le premier script cherchait le mot RELIRE dans le TEXTE de l'indice regle de c0b, alors qu'il est dans le TITRE de la case -- faux negatif sur les 11 parcours ; toujours verifier OU le motif attendu est stocke (titre vs texte) avant de conclure a un ecart
3. La navigation prouve la logique de la decision utilisateur : OUI passe a la mission, NON et INCERTAIN passent par c0b (relire obligatoire) puis la mission -- l echantillon themis + atlas (6 chemins) confirme PARCOURS TERMINE
4. Le rapport ne recommande AUCUNE correction : les 11 parcours sont conformes au referentiel

## [RAPPORT] Audit 2026-08-08 -- Conformite 5 patterns (spec v0.2.6), suite chasse aux intentions passives

**Audit** : verifier la conformite globale des 11 parcours aux 5 patterns de la spec-guider-parcours v0.2.6, avec la PROCEDURE D AUDIT 4b (Pattern 5 -- chaine de delegation ACTIVE) fraichement documentee.
**Verdict** : CONFORME (11/11 parcours, 3 ecarts Pattern 2 CORRIGES pendant l'audit).
**Resultats par pattern** :
1. PATTERN 5 -- SCAN PASSIF : 11/11 parcours, 0 case fin avec formulation passive bloquante (te reactive / j attends / attend le retour / il me reactive / tu seras reactive) -- scan des messages de TOUTES les cases fin, 0 resultat
2. PATTERN 5 -- BOUCLE MATERIALISEE : vulcain porte la boucle complete RELAIS c9a/c15a -> RETOUR c9b/c15b -> CLOTURE c9c/c15c -> FIN c9/c15 (navigation --reponses des 2 chemins : PARCOURS TERMINE) ; athena c10 et promethee c10 portent le message RELAIS ACTIF (je ne m arrete pas en attente, la chaine continue jusqu au retour a Cerberus) ; les 8 autres parcours n ont PAS de delegation (leurs fins sont des ACTIONS finales : Reactiver Cerberus / Reactiver Vulcain / coordination terminee / signaler le besoin) -> aucune fin passive, le Pattern 5 est conforme
3. PATTERN 4 -- QUESTION HONNETE : 11/11 parcours, case_depart c0, c0 question honnete (MEMOIRE + SANS relire), branches OUI->c1 / INCERTAIN->c0b / NON->c0b, c0b RELIRE OBLIGATOIRE (lire corrections.md + fiche, suivant c1)
4. PATTERN 1 -- MULTI-MISSIONS : 11/11, case c1 Mission question avec 3 a 6 branches par parcours
5. PATTERN 2 -- RAPPEL ASCII POSITION 1 : 10/11 OK, VULCAIN 3 ECARTS DETECTES ET CORRIGES pendant l audit (c4 copier-fichier, c6 creer/ecrire-fichier, c12 editer-fichier : le rappel ASCII n etait pas en position 1, texte non uniforme REGLE IMMUABLE : ASCII strict au lieu de REGLE IMMUABLE ASCII) -> texte uniforme insere en position 1, re-verification OK
6. PATTERN 3 -- COMBO : 6 cases combo (buffy c28, janus c5/c22, themis c3, vulcain c7/c13) referencent toutes combos-moteur + definition-combo.json
7. VALIDATIONS TECHNIQUES : json.load 11/11 OK, guider-parcours --liste 11/11 charge, ASCII 0 sur les 11
**Lecons** :
1. Le Pattern 5 est la CLE de la non-coupure de chaine : une delegation sans boucle materialisee OU sans message RELAIS ACTIF cree une fin passive qui bloque l execution. La regle de la spec v0.2.6 est confirmee par l audit : sur 11 parcours, seuls les 3 qui deleguent (vulcain boucle, athena/promethee relais actif) en ont besoin -- les 8 autres se terminent par des actions finales de reactivation
2. PIEGE CRITERE D AUDIT (deja note au rapport precedent) : un test trop strict peut produire des faux ecarts -- ici le test cherchait 'memoire' en minuscules alors que la question porte 'EN MEMOIRE' en MAJUSCULES (faux ecart sur les 11) ; toujours verifier la casse et le format reel avant de conclure
3. PATTERN 2 NON UNIFORME CHEZ VULCAIN : les cases d ecriture portaient REGLE IMMUABLE : ASCII strict (ancien format) au lieu du texte uniforme REGLE IMMUABLE ASCII (spec v0.2.0) -- la procedure d audit 4b ne testait que Pattern 5, c est la procedure d audit 2 (position 1) qui a revele les 3 ecarts ; re-auditer les 5 patterns, pas seulement le nouveau
4. L audit croise confirme : la chasse aux intentions passives (Buffy) a atteint son objectif -- 0 formulation passive dans les 11 parcours, la chaine ne peut plus se couper par une fin passive

## [RAPPORT] Re-audit 2026-08-08 -- Conformite 8 patterns (spec v0.2.15) + chaine bout-en-bout

**Objet** : re-audit complet des 11 parcours apres la migration vers la CHAINE BOUT-EN-BOUT (Pattern 8, spec v0.2.15) et l'ajout des regles immuables dans les generateurs (generateurs-case v0.2.1 + generateurs-carte v0.1.1).
**Verdict** : CONFORME -- 11/11 parcours OK, 0 ecart.

**Points verifies (procedure re-audit complet v0.2.7 + 4f)** :
1. PATTERN 4 (question honnete) : 11/11 case_depart = c0, question contenant memoire + SANS relire, c0b RELIRE, c0c CONTEXTE -- OK
2. PATTERN 2 (rappel ASCII position 1) : toutes les cases d ecriture portent un indice regle ASCII en position 1 (formulation REGLE IMMUABLE ASCII ou REGLE WORKSPACE ... ASCII 2 ALTERNATIVES, spec v0.2.0) -- 11/11 OK. ATTENTION AUDIT : un detecteur trop strict exigeant le PREFIXE EXACT 'REGLE IMMUABLE ASCII' produit des faux positifs (les cases portent REGLE WORKSPACE ... ASCII 2 ALTERNATIVES, qui est le rappel ASCII en position 1) -- verifier la PRESENCE du rappel ASCII en position 1, pas le prefixe exact
3. PATTERN 7 (modele compose) : aucune decision a branche unique -- OK
4. PATTERN 5/8 (fins actives + chaine bout-en-bout) : 0 formulation passive (grep te reactive/j attends/attend le retour/il me reactive) ; la chaine outil -> tests -> controle est migree : Vulcain fins c9/c15 (MORPHEUS ACTIVE), cases RVAV c7b/c13b avant activation, Morpheus fin c10 (ACTIVE JANUS avec le rapport), Janus fin c10 (REACTIVE CERBERUS avec BILAN CONSOLIDE + RVAV c9), Cerberus c7 (flux chaine bout-en-bout) -- CONFORME
5. LE DERNIER MAILLON de la chaine (Janus) REACTIVE Cerberus avec le bilan consolide -- CONFORME (Janus c10)
6. REGLES IMMUABLES DANS LES GENERATEURS : generateurs-case v0.2.1 (garde-fou RVAV + delegation + ASCII, non bloquant) + generateurs-carte v0.1.1 (squelette c2b RVAV avant fin + rappel ASCII + fin chaine bout-en-bout) -- les prochaines cartes/cases ne naitront plus sans regles immuables

**Lecons** :
1. Le re-audit complet (regle v0.2.7) reste la seule preuve de conformite globale : 8 procedures rejouees (1, 2, 3, 4, 4b, 4d, 4e, 4f), jamais la nouvelle seule
2. L audit structurel automatique (python) est utile en PREMIERE PASSE, mais un audit croise manuel sur un echantillon (c0, c5 buffy, c12 vulcain) evite de declarer des faux ecarts sur des formulations legitimes
3. La chaine bout-en-bout (Vulcain -> Morpheus -> Janus -> Cerberus) verrouille la delegation : aucun maillon ne repasse par Cerberus au milieu, chaque maillon passe RVAV avant d activer le suivant

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |
