---
identite:
  nom: regles-immuables
  version: 0.4.0-marbre
  cree: 2026-08-22
  type: reference
  appartient_a: rogers
  commun: false
  tags: regles, immuables, freelance, v2
  mot-cles: ["regles", "immuables", "principes", "decisions", "securite", "v2"]
  session: freelance
# Regles Immuables -- Equipe Freelance (v2)
# Source : proposition-v2.md (decisions D1-D18 + principes P1-P9)

> Rogers est le gardien de ces regles. Aucune exception.

---

## LES REGLES GRAVEES DANS LE MARBRE (2026-08-23, suite DEFCON 5)

> Ces regles sont les fondations. Elles ont ete payees par des echecs reels
> et leur modification sans controle ferait effondrer le systeme.

## LA PORTE DE MARBRE

**Aucune regle du marbre ne peut etre modifiee, affaiblie ou supprimee
sans l'accord EXPLICITE de l'utilisateur, OU l'accord exclusif de Stark**
(donne clairement, trace dans un message JARVIS).

Toute proposition de modification passe par Rogers -> JARVIS -> Stark ->
utilisateur si necessaire. Un agent qui modifie une regle du marbre sans
cette chaine commet la violation la plus grave du projet.

### Regles gravees

| # | Regle gravee | Payee par |
|---|---|---|
| M1 | Tout passe par JARVIS : aucun travail sans message tracé (proto 8) | DEFCON 5 du 2026-08-23 |
| M2 | Aucun agent n'execute les missions d'un autre : l'habilite travaille lui-meme, apres activation tracée | 3 ruptures de flux le 2026-08-23 |
| M3 | V1-V4 : je ne mens pas, je n'invente pas, je ne suppose pas, affirmatif seulement si sur | discipline permanente |
| M4 | P10 : la racine se detecte via os_path, elle ne se compte pas | 4 bugs de chemin le 2026-08-23 |
| M5 | Zero valeur en dur (P4/D15) | bug freebuff + sessions en dur |
| M6 | La porte du marbre elle-meme : modification seulement avec accord utilisateur OU accord exclusif de stark | DEFCON 5 du 2026-08-23 |
| M7 | Tout nouveau script python inclut le bootstrap de detection (remonte jusqu'a AGENTS.md) des sa creation ; l usage d os_path est verifie a la livraison | 4 bugs de chemin + 1 bug de comptage dans le correctif lui-meme (2026-08-23) |



---

## REGLES DE VERACITE (V1-V4, decision utilisateur 2026-08-23)

> Portee : rapports, bilans, tests, reponses a l'utilisateur, messages JARVIS.
> Une affirmation non verifiee est une HYPOTHESE et doit etre presentee
> comme telle.

| # | Regle | Application |
|---|---|---|
| V1 | **Je ne mens pas** | Jamais de faux verdict, de test simule presente comme reel, de succes invente. |
| V2 | **Je n'invente pas** | Pas de fichier, chiffre, citation ou resultat sorti de l'imagination. Si je ne l'ai pas lu/mesure, je ne l'affirme pas. |
| V3 | **Je ne suppose pas** | Une deduction non confirmee reste une hypothese explicite ("je suppose que..."), jamais un fait affirme. |
| V4 | **Affirmatif seulement si sur** | Je dis "c'est fait/valide/conforme" UNIQUEMENT si je viens de le verifier moi-meme. Sinon : "non verifie" ou "a confirmer". |

---

## PRINCIPES FONDAMENTAUX (P1-P9)

| # | Principe | Regle |
|---|---|---|
| P1 | **Point d'entree unique** | Chaque outil = 1 fichier explicatif + 1 entry + fonctions simples par dossier. |
| P2 | **Modularite stricte (SRP)** | Une categorie = un dossier autonome, isole. |
| P3 | **Separation des preoccupations** | Structure / presentation / comportement separes. |
| P4 | **Zero valeur en dur** | Le code ne connait pas les valeurs, il sait ou les trouver (.env, config.json, constantes.json). |
| P5 | **SSOT (source unique de verite)** | Avant de creer, chercher dans l'existant. Une donnee = un seul endroit. |
| P6 | **Diagnostic avant creation** | Un bug = audit de l'existant, jamais "il manque quelque chose". |
| P7 | **Action minimale (anti code fantome)** | Ne coder QUE ce qui est demande. Tout superflu = dette technique. |
| P8 | **Integrite par SHA-256** | Toute donnee critique porte une empreinte verifiee. |
| P9 | **UTF-8 + CRLF + emojis** | Standard v2/freelance uniquement. La v1 garde ASCII/LF. |
| P10 | **os_path : detection de racine obligatoire** | TOUT outil detecte le workspace via `os_path.fonctions.racine.trouver_racine(__file__)` (cherche AGENTS.md en remontant). INTERDIT de compter les niveaux en dur (`"../.."`) - cause de bugs recurrents. Outil : `tools-commun/os_path/`. |

---

## DECISIONS IMMUABLES (D1-D18)

### Cycle fondamental
- **D1** : Arbre des decisions (pas carte lineaire). Systeme veineux.
- **D3** : Activation automatisee et transparente. L'agent ne voit plus la plomberie.
- **D11** : Flux ROUND / INTER-ROUND / REPRISE. Un round lance est fini.
- **D12** : Tracabilite R/IR. Chacun n'edite que son perimetre.

### Standard
- **D4** : UTF-8 + CRLF + emojis (perimetre freelance SEULEMENT).
- **D17** : Cartes d'identite enrichies (grade, medaille, notation, mot-cles).

### Separation
- **D15** : Separation code/donnees. Chaque outil stocke ses donnees dans des fichiers distincts.
- **D2** : Non-regression separee. La suite freelance est INDEPENDANTE de la v1.

### Communication
- **D16** : JARVIS. Outil de communication inter-agents. Messages signales dans la case de debut.
- **D9** : Historique par agent (PAS de trace unique).

### Nommage
- **D14** : Theme MARVEL pour les agents freelance.
- **D5** : Arbres = redirections vers fichiers separes.

### Documentation
- **D10** : BDD des lecons classee, categorisee, consultable comme une bible.
- **D18** : Outil markers (debut-fin) pour isoler des fragments.

### Outillage
- **D6** : Commande simple cache plusieurs outils (transparence).
- **D7** : Formulaire d'outil = contrat declaratif (champs, validation).
- **D8** : Themes de l'arbre (CREER, MODIFIER, LIRE, VALIDER, TESTER, REDIGER, NETTOYER, COORDONNER, EXPLORER, LECONS).

---

## REgles de securite

| Regle | Detail |
|---|---|
| **Pas de session croisee** | Un agent n'appartient QU'A SA session. session-admin et session-freelance ne se melangent JAMAIS. |
| **Pas de modification hors perimetre** | Chaque agent n'edite que les fichiers de SON perimetre. |
| **Nom canonique partout** | Le catalogue est la SSOT. Les alias sont INTERDITS dans les usages. |
| **REACTIVER = Cerberus** | `reactiver` va toujours vers le principal de session (Cerberus). Pour aller vers un autre agent, utiliser `activer`. |
| **JARVIS = seul canal** | Aucun agent ne communique directement vers un autre. Tout passe par JARVIS. **Rien ne passe sans JARVIS.** |
| **Autonomie v2** | La v2 n'utilise AUCUN outil v1. Ses propres outils dans tools-commun/ et <agent>/tools/. |
| **Interdiction v1** | Aucun agent freelance ne modifier JAMAIS les outils v1 (cerveau-projet/agents/tools/). Seul Stark est dans activer-agent-principal. Les autres agents sont actives par Stark via JARVIS. |
| **PAS DE PARCOURS V1** | Les parcours V1 (parcours-*.json lineaires) sont INTERDITS pour les agents freelance. Chaque agent a un ARBRE DES DECISIONS (arbre-*.json + theme-*.json + fins.json). |

---

## GRADES ET HABILITATIONS (D17)

| Grade | Niveau | Habilitation |
|---|---|---|
| **copper** | 0 | Agent debutant. Aucune habilitation speciale. |
| **iron** | 1 | Agent fonctionnel. Peut lire/crire dans son perimetre. |
| **silver** | 2 | Agent confirme. Peut modifier les regles de son domaine. |
| **gold** | 3 | Agent expert. Peut creer des outils et des agents. |
| **platinum** | 4 | Agent maitre. Peut modifier les protocoles et conventions. |
| **diamond** | 5 | Agent supreme. Acces total (Cerberus uniquement). |

**REGLE** : le grade determine CE QUE l'agent peut faire. Un agent copper ne peut PAS modifier les regles. Un agent silver ne peut PAS creer un outil.

---

## MEDAILLES

| Medaille | Condition | Effet |
|---|---|---|
| **pionnier-marvel** | Premier agent MARVEL cree | Symbole honorifique |
| **constructeur-outils** | A cree au moins 1 outil | Permission de creer des outils |
| **gardien-regles** | A cree les regles/conventions | Permission de modifier les regles |
| **outil-nevralgique** | Outil central (JARVIS) | Permission de gerer la communication |
| **zero-defaut** | 10 audits consecutifs sans defaut | Permission de modifier les protocoles |
| **veteran-100-rounds** | 100 rounds executes | Permission de modifier les conventions |
