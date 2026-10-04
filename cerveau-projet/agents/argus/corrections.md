> MEMOIRE GELEE le 2026-09-04 - decision utilisateur v1->v2 : les
> nouvelles lecons vont dans bdd-lecons (outil v2). Historique conserve
> pour relecture - AUCUN [LECON] supplementaire.
## [LECON] 2026-09-04 -- AUDIT CONSTAT : BDD DES CORRECTIONS v1 vs v2 (mission 82151e40, Argus)

**Contexte** : demande utilisateur [attention] - verifier comment les agents utilisent la bdd des corrections. Dans freelance (v2), corrections.md ne contient plus tout : les agents se partagent les corrections (corrections.jsonl + bdd-lecons partagees). Verifier ce qui est en place encore en v1.

**Resultat (rapport classe par gravite livre en FIN)** :
- V2 : 2 systemes partages distincts = (1) corrections.jsonl/corrections.py (retro-correction automatique traitee en priorite par JARVIS, 1653 entrees dont 1650 EN_ATTENTE = backlog non traite) et (2) bdd-lecons (lecons partagees, doctrine D10 "plus de lecons dans corrections.md", mais seulement 6 lecons enregistrees alors que les corrections.md v2 contiennent ENCORE des [LECON] jusqu au 2026-08-26 - la bascule est restee incomplete).
- V1 : infra triple existante et documentee (corrections-db.md) : corrections.md = memoire courte ~10 dernieres lecons ; lecons/lecons.db = memoire longue (255 lecons, 13 agents) ; corrections.db = index de compatibilite (360 lignes, 19 agents, import UNIQUE le 2026-09-01 jamais re-importe).
- ECART 1 (majeur) : la doctrine v1 (corrections-db.md : corrections.md = fenetre courte ~10 lecons) n est PAS respectee en pratique : corrections.md reels accumulent TOUT l historique (vulcain 27 [LECON]/644 lignes, morpheus 26/609, themis 12/310, buffy 15/289...) - le --trim n a jamais ete lance (corrections-db.py : 0 usage declare au registre).
- ECART 2 (majeur) : double ecriture protocole-fin-mission E2 (corrections.md + enregistrer-lecon vers lecons.db) NON FAITE depuis le 2026-08-18 (dernier usage reel d enregistrer-lecon hors verrou-auto : 2026-08-18 ; les 4 lecons du 09-04 de ce round : 0 usage enregistrer-lecon) - les lecons restent dans corrections.md sans aller en memoire longue partagee.
- ECART 3 (mineur) : 3 agents ont des [LECON] dans corrections.md mais AUCUNE lecon dans lecons.db (argus 4, hermes 1, promethee 10).
- ECART 4 (mineur) : corrections.db (index) importe UNE fois (2026-09-01, 09:38) puis plus JAMAIS re-importe - index fige.
- ECART 5 (mineur) : v2 corrections.jsonl = 1650 entrees EN_ATTENTE sur 1653 (backlog retro-correction non traite depuis aout).

**Lecons** :
- Une doctrine documentee (corrections-db.md) peut etre en decalage total avec la pratique : croiser la doctrine avec les fichiers REELS et le registre des usages distingue le theorique du reel.
- Deux modeles ont ete batis en parallele (v1 triple infra vs v2 corrections.jsonl+bdd-lecons) sans convergence : le risque est la double infrastructure et la perte des lecons hors corrections.md.
- Le protocole E2 impose la double ecriture (corrections.md + lecons.db) mais rien ne la verifie en pratique depuis le 08-18 : un garde-fou (test) manque pour controler que chaque lecon de corrections.md part bien dans lecons.db (et inversement).

## [LECON] 2026-08-16 -- PREMIERE ACTIVATION : TEST DE COMPORTEMENT (Argus)

**Contexte** : premiere activation reelle apres branchement a la liste AGENTS (etait inactivable depuis la creation 2026-08-15). Mission : tester le comportement pour rediger ensuite protocoles et parcours.

**Deroule** : fiche + doc outil lues ; detecter-contradictions lance dans 4 modes (--tous/--cases/--regles/--git) = 0 contradiction sur l etat reel ; preuve negative (copie parcours + REF_MORTE + CAS_ORPHELINE injectees) = detection 100% via auditer_parcours ; CLI --cases ne voit pas le fichier hors chemin standard.

**Limites de mon outil** (a ameliorer, Vulcain) : 1) scan fixe des parcours (pas d option --fichier/--parcours pour cibler une copie), 2) audit regles superficiel (liens casses + doublons de titres seulement, PAS de croisement de contenu entre 2 regles - ecart doc vs realite), 3) audit git limite (log -n 50 + residus temp dans messages, pas d analyse des evolutions), 4) libelle du rapport = champ nom du JSON (confusion si copie), 5) double source non mecanisee (comportement d agent).

**Lecons** :
- La detection de cases est fiable (preuve negative 100%) ; le reste de la mission est a construire.
- Toujours faire une preuve negative pour valider une detection (et non se fier au verdict PROPRE seul).
- Un outil peut etre documente pour une mission large mais n en couvrir qu une fraction : verifier le code reel, pas la doc.

## [LECON] 2026-08-16 -- RE-TEST v0.1.1 : 3 LIMITES RESOLUES (Argus)

**Contexte** : re-test de detecter-contradictions apres les ameliorations v0.1.1 (option --fichier, audit regles croise, audit git enrichi), verrouillees par test-069.

**Resultats** : --version 0.1.1 ; --cases PROPRE ; --regles PROPRE avec audit CROISE actif (72 affirmations comparees, 0 faux positif) ; --git : 2 GIT_RESIDU_TEMP historiques, 0 GIT_RESIDU_ACTUEL (le nettoyage Hygie a porte) ; --fichier : preuve negative a 100% (CAS_ORPHELINE + REF_MORTE detectees, libelle = nom reel du fichier).

**Statut des 5 points du premier rapport** : 1) scan fixe RESOLU (--fichier), 2) audit regles superficiel RESOLU (croisement inter-fichiers, regle DOUBLE SOURCE), 3) audit git limite RESOLU (GIT_RESIDU_ACTUEL), 4) libelle champ nom RESOLU (nom reel), 5) double source NON MECANISEE -> reste un comportement d agent (amelioration possible : preuve double source dans le rapport).

**Lecons** :
- Le cycle de vie d un outil passe par : test reel (limites) -> ameliorations -> garde-fou (test-069) -> re-test qui confirme. La boucle est complete.
- Un outil qui detecte 0 sur l etat reel n est pas forcement inutile : c est le signal que les regles du projet sont coherentes ; la preuve negative prouve qu il sait detecter quand il y a un vrai probleme.
- Le rapport de comportement evolue avec l outil (v0.1.0 -> v0.1.1) : garder la trace avant/apres.
## [LECON] 2026-08-16 -- PREMIERE MISSION REELLE COMPLETE : LE PARCOURS v0.1.3 GUIDE PARFAITEMENT (Argus)

**Contexte** : test reel en mission complete (demande Cerberus) - lancer detecter-contradictions --tous sur l etat reel et suivre le parcours v0.1.3 case par case.

**Deroulement** : c0/c0b relecture -> c0c contexte (historique + registre) -> c2 audit --tous -> 2 GIT_RESIDU_TEMP mineurs -> c3 lecture git -> c4 controle croisement DOUBLE SOURCE : les 2 traces sont des commits de SUPPRESSION de residus (49e966e, 22c10c7) - HISTORIQUE LEGITIME, 0 anomalie actuelle -> c30 preuve negative --fichier (copie + REF_MORTE cZZ + CAS_ORPHELINE c99 injectees -> detection 100%) -> c31 nettoyage tmp-argus (declaration registre mode script-temporaire + suppression, 0 residu) -> c13 FIN.

**Ce que le parcours a bien guide** : 1) le controle c4 force le croisement 2 sources avant de signaler (regle double source) - sans lui, j aurais signale 2 faux positifs, 2) la preuve negative c30 empeche de conclure 'rien a signaler' sans preuve - l outil detecte bien les contradictions reelles, 3) le nettoyage c31 est automatique en fin de mission (0 residu verifie).

**Ce qui a bloque (aucun)** : le parcours a couvert 100% du cas. Le seul point d attention : l audit git signale TOUTE trace historique de suppression de residu comme GIT_RESIDU_TEMP (mineur) - il faut le croisement manuel avec git log pour ecarter les historiques legitimes.

**Lecon de conception** : le croisement DOUBLE SOURCE (outil + source de verite) est le coeur du metier d Argus - le parcours l impose au bon endroit (c4 avant c5/c30).
## [LECON] 2026-08-16 -- CONTROLE CROISE RELIRE SA FICHE AVANT MISSION (Argus)

**Controle croise** (mission Cerberus) : coherence entre la regle gravee dans regles-groupes-agents.md (RELIRE SA FICHE AVANT MISSION), le protocole-activation et les cases c0/c0b des 15 parcours. RESULTAT : 15/15 cartes conformes (c0 question + branches OUI->c0c/INCERTAIN->c0b/NON->c0b, c0b RELIRE + 2 lire-fichier corrections puis fiche), ordre corrections-puis-fiche coherent dans les 3 sources. MAIS 1 CONTRADICTION SIGNALEE (ecart de formulation) : la regle gravee dit "OUI = memorisation prouvee -> mission" alors que le protocole-activation et les 15 cartes disent "OUI -> c0c (contexte obligatoire) -> mission" - la regle omet le passage par c0c pour la branche OUI. CORRECTION NON EFFECTUEE (regle Argus : detecter et signaler, l agent habilite corrige - ici Buffy via la porte du marbre).

**Lecon** : un controle croise texte/texte revele des ecarts de formulation que les tests structurels ne voient pas : test-072 verifie la STRUCTURE des cartes (c0/c0b conformes) mais pas la COHERENCE du texte grave avec le mecanisme reel. La regle gravee doit decrire le flux COMPLET (OUI -> c0c -> mission), pas une version simplifiee qui contredit le parcours.
