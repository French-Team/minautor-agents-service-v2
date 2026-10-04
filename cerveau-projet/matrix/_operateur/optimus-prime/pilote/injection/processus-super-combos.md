---
identite:
  type: processus
  appartient_a: optimus-prime
  commun: false
---

# PROCESSUS -- LES SUPER-COMBOS SE PASSENT, ET LEUR PASSAGE SE PROUVE

POURQUOI CE PROCESSUS EXISTE (demande du createur, 2026-09-26, crochet [tache])
La Matrice POSSEDE les super-combos, et l agent SAIT quand les employer : leurs
modes d emploi voyagent avec chaque mission (catalogue avant-mission). Mais RIEN
ne FORCAIT leur passage quand un round corrige, ameliore ou modifie des fichiers
et des flux -- ils dependaient de la MEMOIRE, et une consigne qu on peut oublier
est une discipline, pas un processus (L-165). Mesure du 2026-09-29 : le registre
des usages ne portait qu UNE occurrence d un super-combo sur 65686 lignes, et le
lanceur n ecrivait aucune trace -- il n existait donc AUCUNE preuve de passage.

QUAND CE PROCESSUS S APPLIQUE
Des qu un round CORRIGE, AMELIORE ou MODIFIE des fichiers ou des flux : missions
dev, reparation, outil, bdd, pilote. AVANT de rendre le bilan, et AVANT de
declarer la non-regression verte.

QUI : LES SUPER-COMBOS (le registre fait foi, jamais cette liste)
  sc-001-auto-xxx        -- enchaine les themes AUTO-XXX : preparation,
                            auto-correction, auto-testing, auto-optimisation,
                            auto-performance, auto-audit-nemesis ;
  sc-002-auto-evolution  -- le cycle d une evolution : detecter, qualifier,
                            cibler, modifier, valider ;
  sc-003-auto-suivi      -- le suivi du pilote ;
  sc-004-auto-diagnostic -- le diagnostic des outils ;
  sc-005-moules          -- les moules de la Matrice;
  sc-006-lacunes         -- retrouver une lacune (le signal qui dort, la
                            repetition, la racine) puis la combler par une porte ;
  sc-007-table-ronde     -- 5 facons de penser, 3 rounds sur le contenu de la
                            table, puis ARBITRE qui synthetise EN GARDANT LE
                            DESACCORD des 5 profils.
L AUTORITE est `super-combos/registry.json` (id, nom, fichier, phases, verbes).
Cette liste le NOMME, elle ne le remplace pas : un ecart du registre se repare au
registre (l inventaire du lanceur rend les ecarts, champ par champ). Un maillon de
la non-regression verifie que les deux ne DIVERGENT pas : ajouter un super-combo
au registre sans le nommer ici est un ECART, et en nommer un qui n existe plus en
est un aussi.

COMMENT PASSER UN SUPER-COMBOS
    python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/lancer-super-combos.py
            --numero <sc-NNN> --mission <MO-XXX> [--verbe <verbe>] [--fichier <cible>]
Le lanceur lit le registre, resout le verbe (un verbe hors contrat est REFUSE et
NOMME), lance le combo, puis NOTE le passage -- c est le lanceur qui ecrit la
preuve, jamais la memoire de l agent.

LA PREUVE DE PASSAGE (elle se lit, elle se juge)
Chaque passage ecrit UNE LIGNE dans le registre UNIQUE des usages
(`matrice/data/usages-outils-combos.jsonl`, par sa porte `bdd-usages`) : le combo,
le verbe, le code, la duree, la cible et la MISSION. Elle se juge :
    python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/lancer-super-combos.py
            --preuves <MO-XXX> --combos sc-001,sc-002
  -> code 0 : chaque combo DEMANDE a son passage (ou rien n a ete demande) ;
  -> code 1 : les combos demandes SANS aucun passage sont ACCUSES et NOMMES ;
  -> code 2 : le registre est INTROUVABLE -- on ne conclut JAMAIS < aucun passage >
     sur un fichier qu on n a pas lu.

CE QUI EST UN ECHEC
Un round qui a modifie des fichiers ou des flux et qui ne peut PAS montrer ses
passages n est PAS fini : son bilan DIT les passes (avec leur code) ou DIT
pourquoi il n y en a pas. Un silence ne prouve rien, et une preuve ne se suppose
pas. Le choix des combos PERTINENTS reste un JUGEMENT du round : ce processus ne
demande pas de tout lancer, il demande de PROUVER ce qui a ete juge utile.
