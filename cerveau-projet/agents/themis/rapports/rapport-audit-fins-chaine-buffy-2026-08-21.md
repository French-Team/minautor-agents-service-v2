# Rapport audit -- Fins de Buffy et boucle de chaine (2026-08-21)

**Agent auditrice** : Themis (demande Cerberus - demande utilisateur)
**Objet** : pourquoi les fins de Buffy n activent pas Vulcain (modif outil) / Morpheus
(correction suite) pour continuer la boucle ; ou inserer un message de relais
"commence ET finis ton travail puis active l agent suivant".
**Perimetre** : parcours-buffy.json + fins "Activer X" des 20 cartes + garde-fou
v0.5.19 de activer-agent-principal (croisement carte/outil).

---

## VERDICT : A REVOIR -- 5 constats (E1-E5)

| # | Constat | Gravite |
|---|---|---|
| E1 | Fins de Buffy : routage Vulcain/Morpheus ABSENT (toujours Janus) | MAJEUR |
| E2 | 3 chaines contradictoires pour "modif outil" entre les cartes | MAJEUR |
| E3 | GARDE-FOU v0.5.19 bloque TOUTE activation directe (cause racine) | CRITIQUE |
| E4 | Message de relais absent des 20 fins "Activer X" | MINEUR |
| E5 | buffy c15e reference c13 INEXISTANTE (defaut E1 du 20/08 non repare) | MAJEUR |

---

## E1 -- Les fins de Buffy activent TOUJOURS Janus, jamais Vulcain/Morpheus

- **c8 / c22 / c27** : "FIN - Activer Janus" -- quel que soit le travail effectue
  (creation d agent, de protocole, modification de fichier).
- **Flux creation** (c2 -> c8) : Buffy -> c8a (Activer Themis) -> c8b (retour) ->
  c8 (FIN - Activer Janus).
- **Flux modification** (c9 -> c16 -> c31/c17 -> c8a -> c8) : Buffy -> c31
  (Activer Vulcain) OU c17 (Activer Athena) -> c8a (Themis) -> c8 (Janus).
- **Morpheus n est JAMAIS active par Buffy** : aucune fin ni action de la carte
  ne l active. Le c35 (hors perimetre) mentionne "besoin de test -> Morpheus"
  mais uniquement pour les missions HORS perimetre, pas pour les missions
  normales de modification d outil.

**Reponse a la question utilisateur (pourquoi) - volet carte** : les fins de
Buffy ont ete concues avec UNE seule sortie (Janus, second controle), sans
branche selon le type de travail (outil -> Vulcain, tests -> Morpheus).

## E2 -- 3 chaines contradictoires pour le meme cas "modif outil"

La carte de Buffy documente 3 chaines differentes pour l activation de Vulcain :

| Source | Chaine documentee |
|---|---|
| Buffy c31 (indice regle) | Vulcain -> Janus (controle) -> Clio (README) -> Cerberus (SANS Morpheus) |
| Vulcain c9/c15 (fin) | Vulcain -> Morpheus (tests) -> Janus (controle) -> Cerberus (AVEC Morpheus, SANS Clio) |
| Buffy c35 (message) | "activer Vulcain directement - maillon de chaine, Vulcain reactive l agent precedent" (Vulcain RE-ACTIVE l agent precedent, ce qui contredit les 2 autres) |

La chaine ne converge pas : les agents ne savent pas qui activer apres Vulcain.
La chaine complete de reference (Pattern 8) est celle de Vulcain c9/c15 :
**Vulcain -> Morpheus -> Janus -> Cerberus**.

## E3 -- GARDE-FOU v0.5.19 bloque TOUTE activation directe (cause racine)

Croisement carte/outil (activer-agent-principal.py, lignes ~1089-1130) :

```
agent_actuel = agent_actif_bloc(...)
si agent_actuel != cerberus :
    cible = cerberus      -> AUTORISE (reactivation)
    cible = agent_actuel  -> AVERTISSEMENT + autorise (auto-reactivation)
    cible != actuel + --forcer -> AVERTISSEMENT + autorise
    cible != actuel (sans --forcer) -> BLOQUE (return 1)
```

Consequence : quand Buffy finit et lance `activer <session> janus "..."` (sa carte
c8), la session porte encore buffy comme agent actif -> cible janus != cerberus
et != buffy -> **BLOQUE**. Meme chose pour Vulcain -> Morpheus et
Morpheus -> Janus : **la chaine bout-en-bout (Pattern 8) est bloquee par l outil**.

La boucle reelle observee dans le round : chaque agent REACTIVE Cerberus (toujours
autorise), et Cerberus route l agent suivant. Les messages "J ACTIVE JANUS" des
fins ne peuvent donc PAS s executer tels quels -> **les cartes sont en decalage
avec l outil**.

**C est POURQUOI la boucle ne passe pas par Vulcain/Morpheus quand Buffy modifie
un outil : meme si la carte le disait, l outil bloquerait l activation.**

## E4 -- Message de relais absent des fins "Activer X" (20 fins)

- Les 20 fins "FIN - Activer X" des cartes disent "La chaine continue : X
  controle... sinon il REACTIVE Cerberus" mais AUCUNE ne dit explicitement au
  suivant : "COMMENCE et FINIS ton travail puis ACTIVE l agent suivant".
- Le message generique n existe qu UNE fois : buffy c36 "FIN - Delegation" :
  "L agent active execute sa mission puis active le maillon suivant de la chaine
  (ou reactive Cerberus si active directement par lui)."

**Endroit precis d insertion** : dans le champ `message` des fins qui activent un
agent suivant (buffy c8/c22/c27, morpheus c10/c14, themis c13, clio c12, vulcain
c9/c15, argus c13, athena c10, atlas c11, chiron c14, gardien c9, hermes c13,
hygie c13, minerve c10, promethee c10, janus cT6/cT7, ...). Ce message est la
RAISON que l agent suivant lit a son demarrage (bloc session AGENTS.md).

**Modele de message ASCII propose** (a ajouter dans chaque fin "Activer X") :

```
MESSAGE DE RELAIS A L AGENT SUIVANT : quand tu es active, COMMENCE ton travail
(relis ta fiche et tes corrections, suis ta carte case par case), FINIS-le
(RVAV + lecons), puis ACTIVE l agent suivant selon TA carte pour continuer la
boucle. Ne REACTIVE Cerberus QUE si tu es le DERNIER maillon de la chaine.
```

## E5 -- Defaut preexistant non repare (buffy c15e)

- buffy c15e "FIN - Reprise du parcours apres retour de l agent habilite" :
  message reference "ma fin normale c13 (FIN - Reactiver Cerberus)" mais la case
  **c13 n existe pas** dans parcours-buffy.json (cet ecart E1 de la verification
  des cases fin du 20/08 n a pas encore ete repare par Buffy).
- Meme famille que E3 : les references "FIN - Reactiver Cerberus" dans les
  messages de reprise sont obsoletes.

---

## DECISION A TRANCHER (utilisateur) -- 2 options

Le message de relais (E4) n a de sens QUE si la chaine bout-en-bout peut reelement
s executer. Deux options :

- **OPTION A -- Retour Pattern 8 (chaine bout-en-bout, conforme a la demande
  utilisateur)** : autoriser l activation directe du maillon suivant quand
  l agent actif termine SA mission selon SA carte. Implique : (1) adapter le
  garde-fou v0.5.19 dans activer-agent-principal (Vulcain) pour distinguer
  "activation de chaine legitime (fin de carte)" de "double activation sauvage" ;
  (2) Buffy ajoute le message de relais dans les fins "Activer X" + une fin de
  routage (Vulcain si outil / Morpheus si tests / Janus sinon) dans sa carte ;
  (3) harmoniser les 3 chaines contradictoires (E2) sur le modele
  Vulcain -> Morpheus -> Janus -> Cerberus.

- **OPTION B -- Aligner les cartes sur la realite (tout par Cerberus)** : garder
  le garde-fou actuel ; les fins "Activer X" deviennent "Reactiver Cerberus
  (bilan pour routage)" et c est Cerberus qui route vers Vulcain/Morpheus/Janus
  selon le type de mission. Implique : (1) remplacer les fins "Activer X" par
  "Reactiver Cerberus" dans toutes les cartes (Buffy) ; (2) le message de relais
  devient inutile (Cerberus route deja) ; (3) E2/E5 tombes d eux-memes.

La demande utilisateur ("l agent suivant doit activer l agent suivant pour
continuer la boucle") penche pour l OPTION A.

---

## Verifications complementaires

- Marbre : intact (exit 0), lock 20 cartes resynchronise (mission Buffy du 21/08).
- valider-case : 0 erreur liee aux fins (les NON CONFORME cerberus c45 / chiron
  c18 sont preexistants).
- ASCII 0 / CRLF 0 sur les cartes et fiches (mission Buffy du 21/08).

## Agent habilite pour la reparation

- **Buffy** : carte buffy (fins, routage E1/E2/E5) + message de relais dans les
  fins "Activer X" (E4).
- **Vulcain** : garde-fou activer-agent-principal si OPTION A choisie (E3).
