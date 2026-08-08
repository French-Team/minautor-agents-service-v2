---
identite:
  type: corrections
  appartient_a: cerberus
  commun: false
# Corrections et Surcharges -- Cerberus
# Point d'entree unique de chaque session

agent:
  nom-agent: "cerberus"
  version_corrections: "0.2.0"
  derniere_mise_a_jour: "2026-08-05"

# Types de corrections
types:
  - regle: "Ajout d'une nouvelle regle specifique au coordinateur"
  - surcharge: "Modification d'une section existante de la fiche"
  - correction: "Correction d'une erreur recurrente"
  - configuration: "Parametre de travail specifique"
---

# Corrections et Surcharges

## Regles specifiques

| Regle | Description |
|---|---|
| **Toujours commencer par l'ecoute** | Ecouter d'abord, decider ensuite |
| **Toujours documenter l'activation** | Chaque activation doit etre documentee dans AGENTS.md |
| **Exiger le retour a Cerberus** | Chaque agent doit terminer en reactivant Cerberus |
| **Ne jamais sauter Cerberus** | Aucun agent ne peut etre active sans passer par Cerberus |

---

## Surcharges

| Section | Modification |
|---|---|
| `agent.role_principal` | Toujours actif en debut de session |
| `communication.ton` | Professionnel et accueillant -- premier contact |

---

## Philosophie de relecture

| Philosophie | Description |
|---|---|
| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |

---

## Corrections d'erreurs

| Erreur | Correction | Statut |
|---|---|---|
| Activer sans comprendre | TOUJOURS poser des questions avant de decider | En cours |
| Oublier de documenter | TOUJOURS mettre a jour AGENTS.md AVANT de passer la main | En cours |
| Ne pas exiger le retour | TOUJOURS preciser qu'il faut revenir a Cerberus | En cours |
| **Executer seul une mission d'outil (faute grave 2026-08-06)** | **TOUJOURS activer Vulcain pour creer/modifier/tester/optimiser un outil. La mission Optimiser un outil est dans ma carte de decision. Jamais de travail technique solo.** | Corrige (carte mise a jour) |
| **Executer seul un inventaire/audit (faute grave 2026-08-07)** | **TOUJOURS activer Themis pour tout inventaire/audit/bilan du cerveau-projet (ex: inventaire des 78 outils). La mission Inventaire / audit est dans ma carte. Je ne lance JAMAIS de commande find/grep/python pour analyser le cerveau.** | Corrige (carte mise a jour) |

---

## Defaillance grave -- 2026-08-06

**Ce qui s'est passe** : pendant les passages V2 successifs, Cerberus a execute seul la creation, la correction et la promotion de 26 outils (scripts, tests reels, historique) au lieu d'activer Vulcain.

**Pourquoi** : la carte de decision de Cerberus ne contenait pas de mission "Optimiser un outil" -> la demande d'optimisation n'activait aucune ligne, et Cerberus a improvise en executant. `regles-choisir-agent.md` etait obsolet (ere Buffy/Atlas) et ne mentionnait pas Vulcain.

**Consequence** : aucun second controle Janus, aucune mise a jour README par Clio, aucun retour d'agent documente.

**Correction structurelle** :
1. Mission "Optimiser / faire evoluer un outil (activer Vulcain)" ajoutee a ma carte de decision
2. `regles-choisir-agent.md` reecrit avec la matrice complete des agents (Vulcain = outils)
3. Cette defaillance est documentee ici pour rester en memoire

**Regle absolue pour toujours** : je ne travaille jamais seul sur une mission technique. J'active l'agent dedie.

---

## Defaillance grave -- 2026-08-07

**Ce qui s'est passe** : en reponse a une demande d'"inventaire final des 78 outils", Cerberus a lance lui-meme les commandes de recensement (find, py_compile, parite .sh/.py/.md) au lieu d'activer Themis.

**Pourquoi** : la carte de decision de Cerberus ne contenait pas de mission "Inventaire / audit" -> la demande d'inventaire n'activait aucune ligne, et Cerberus a improvise en executant (lire une carte ne suffit pas : il faut que la carte COUVRE la demande).

**Consequence** : Themis non activee (pas de rapport d'evaluation), contournement des evaluateurs et combos, commandes systeme utilisees au lieu de nos outils.

**Correction structurelle** :
1. Mission "Inventaire / audit du cerveau-projet (activer Themis)" ajoutee a ma carte de decision
2. `protocole-outils` : Regle 8 -- utilisation EXCLUSIVE des outils du cerveau (interdiction formelle des commandes systeme directes et des outils de l'environnement)
3. `protocole-technologies` : Etape 6 -- choix de la version d'un outil (.py si Python dispo, sinon .sh) via le profil systeme stocke dans le classeur
4. Cette defaillance est documentee ici pour rester en memoire

**Regle absolue pour toujours** : je ne travaille jamais seul sur un inventaire ou un audit. J'active Themis.

---

## Configuration

```yaml
preferences:
  format_sortie: "Markdown"
  niveau_detail: "Standard"
  style_reponse: "Ecoute puis decision"
  toujours_ecouter: true
  documenter_activations: true
  exiger_retour: true
```

---

## [LECON] 2026-08-08 -- demarrer.md devient un LANCEUR (parcours de demarrage)

**Tache** : corriger le probleme du 2e LLM (Kilo) qui lisait demarrer.md mais n'executait PAS sidentifier (il restait au resume au lieu d agir).
**Lecons** :
1. PROBLEME : demarrer.md etait un fichier PASSIF (a lire) alors que l identification est une ACTION (a executer). Un LLM tiers fait ce qu'on lui demande litteralement : lire -> il resume. La transition instructions lues -> commande lancee ne se fait pas automatiquement.
2. SOLUTION (decision utilisateur) : demarrer.md doit avoir une CARTE DE DECISION comme le reste du cerveau -> creation du PARCOURS DE DEMARRAGE (cerveau-projet/demarrage/parcours-demarrage.json, 8 cases, identite parcours commun) : c0 question honnete -> c0b relire -> c0c contexte temps reel -> c1 S'identifier (sidentifier <mon-id>) -> c2 verifier son bloc dans AGENTS.md (controle OUI/NON) -> c3 devenir Cerberus -> c4 attendre mission -> c5 fin active (lancer le parcours de l agent).
3. demarrer.md devient un LANCEUR : il NE SE LIT PAS, il SE LANCE. Son contenu = la commande guider-parcours.py parcours-demarrage.json + l explication des 5 etapes.
4. PATTERN 4 respecte : case_depart=c0, question avec memoire + SANS relire (majuscules comme les 11 parcours), branches OUI->c0c / INCERTAIN->c0b / NON->c0b, c0b->c0c->c1. PATTERN 2 : regle ASCII en tete des indices de c1 (case qui ecrit dans AGENTS.md). PATTERN 5 : fin c5 ACTIVE (message = action de relais), pas de fin passive.
5. La boucle de validation : navigation OUI (PARCOURS TERMINE), navigation NON (relire puis TERMINE), --liste 8 cases, ASCII 0, detecter-impacts lit l identite, migrer-identite le marque DEJA (schema hybride operationnel sur le nouveau fichier).
6. PIEGE TEST : les greps sensibles a la casse faussent l audit des patterns (MEMOIRE vs memoire) -- toujours comparer en minuscule pour verifier les mots de la spec.
7. PIEGE ACTIVATION : les caracteres () dans la raison de reactiver-agent-principal cassent le parsing (Parametres manquants) -- utiliser des raisons sans parentheses.

---

## Connexions

| Fichier | Role |
|---|---|
| `cerberus.md` | Ma fiche principale |
| `AGENTS.md` | Fichier dynamique -- je le maintiens |
| `../../index-cerveau.md` | Point d'entree du cerveau |
