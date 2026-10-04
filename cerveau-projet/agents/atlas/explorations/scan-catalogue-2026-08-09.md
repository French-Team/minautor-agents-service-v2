# Scan Systematique du Catalogue vs Interfaces Reelles

**Date** : 2026-08-09 | **Catalogue** : v0.2.1 | **Entrees** : 106

## Synthese

| Classe | Nombre |
|---|---|
| CONFORME | 105 |
| DECALAGE | 0 |
| NON TESTABLE | 1 |

## DECALAGES (0)

Aucun decalage detecte.

## NON TESTABLES (1)

- **test-001-evaluer-agents-coherence** : PAS D AIDE RECONNUE (--aide et --help rejetes ou sortie vide) (cerveau-projet/agents/tools/tester/tests/test-001-evaluer-agents-coherence/test-001-evaluer-agents-coherence.py)
  - JUSTIFICATION : c est un TEST FORMELL (dossier tester/tests/), pas un outil - il s execute directement sans interface d aide (normal). Son modele est `{chemin}` (placeholder uniquement, AUCUN flag) : le generateur compose une commande positionnelle sans risque. Risque nul.

## Alertes (placeholder obligatoire absent du modele)

Aucune alerte.

## Fiabilite du scan (methode)

- Methode : pour CHAQUE entree, lancement du script avec `--aide` puis `--help` en fallback (timeout 8s), extraction des options reelles (regex `--[a-z][a-z0-9-]*`), comparaison avec les flags en dur du modele du catalogue. Verification complementaire : chemin du script existe, placeholders obligatoires presents dans le modele.
- PIEGE CORRIGE EN COURS DE SCAN : la regex des placeholders `{cle}` utilisait `[a-z_]+` qui n inclut pas les CHIFFRES -> `{paire1}`/`{paire2}` (remplacer-texte) n etaient pas detectes = FAUX POSITIF. Corrige en `[a-z_0-9]+`. Resultat apres correction : 0 alerte (remplacer-texte est conforme).
- Un outil n est declare CONFORME que si une aide RECONNUE (contenant usage/Options/--) a ete obtenue. Les outils sans aide sont classes NON TESTABLE (honnete) plutot que conforme par defaut.
- Echantillon manuel verifie : valider-nommage (--aide, --recursive...), verifier-systeme, valider-relecture (--agent --verbose), combos-moteur, guider-parcours, lire-fichier (--debut --fin --lignes), detecter-impacts (--racine), ecrire-fichier (--backup --dry-run) - tous conformes.
- CONCLUSION : le catalogue v0.2.1 est ALIGNE sur les interfaces reelles des outils (0 decalage confirme). La generalisation du pilote strict aux 10 autres parcours peut etre lancee en toute confiance.

## Conformes (105)

- activer-activer
- activer-agent-principal
- activer-reactiver
- activer-sessions
- activer-sidentifier
- ajouter-contenu-fichier
- analyser-dependances
- analyser-structure
- audit-general
- changer-statut
- combos-audit-general
- combos-corriger-non-ascii
- combos-moteur
- combos-valider-cerveau
- condenser-fichier
- copier-dossier
- copier-fichier
- corriger-accents
- corriger-accents-zones-sensibles
- corriger-dictionnaire-accents
- corriger-emojis
- corriger-liens
- corriger-nommage
- creer-fichier
- creer-remplir-pense-bete
- creer-remplir-spec
- creer-remplir-todo
- decomposer-fichier
- deplacer-fichier
- detecter-divergences-version
- detecter-erreur-statut
- detecter-impacts
- detecter-local-hors-fonction
- detecter-surcharge-fichier
- detecter-usage-outils-externes
- ecrire-fichier
- editer-fichier
- evaluer-agents
- evaluer-coherence
- evaluer-conventions
- evaluer-structure
- generateurs-carte
- generateurs-case
- generateurs-commande
- generateurs-squelette-pense-bete
- generateurs-squelette-spec
- generateurs-squelette-todo
- generer-squelette-pense-bete
- gerer-sous-mission
- guider-parcours
- inserer-contenu-fichier
- lire-activite-recente
- lire-fichier
- lire-frontmatter
- lire-lignes
- lister-agents
- lister-appels
- lister-dossiers
- lister-fichiers
- lister-fonctions
- lister-outils
- lister-prepares
- lister-statuts
- mettre-a-jour-readme
- migrer-identite
- nettoyer-fichier
- nettoyer-sessions
- rechercher-accents-sensibles
- rechercher-dossier
- rechercher-extension-fichier
- rechercher-fichier
- rechercher-fichiers-vides
- rechercher-pense-betes
- rechercher-specs
- rechercher-templates
- rechercher-texte
- rechercher-todos
- remplacer-texte
- remplir-pense-bete
- supprimer-dossier
- supprimer-fichier
- supprimer-ligne
- test-002-combos-moteur
- test-003-combos-creer
- tester-protection-blocage
- tester-protection-boucles-infinies
- tester-protection-erreurs-silencieuses
- valider-cartes-decision
- valider-conformite-ascii
- valider-conventions
- valider-ebauche
- valider-liens
- valider-nommage
- valider-nommage-recursif
- valider-numerotation
- valider-pense-bete
- valider-relecture
- valider-spec
- valider-tableaux
- valider-todo
- verifier-documents-manquants
- verifier-restauration-sure
- verifier-role-fichier
- verifier-separation-preoccupations
- verifier-systeme
