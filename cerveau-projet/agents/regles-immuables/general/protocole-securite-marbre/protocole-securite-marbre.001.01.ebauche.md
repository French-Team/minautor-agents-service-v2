---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Protocole de Securite du Marbre
**Version** : 0.1.1
**Statut** : ebauche
**Categorie** : General
**Agent** : Gardien
**Date** : 2026-08-15
Cadre la **protection du noyau** : certaines regles et cases sont GRAVEES
DANS LE MARBRE et ne peuvent plus etre modifiees sans autorisation
explicite de l utilisateur. Deux outils mecanisent ce protocole :
`proteger-verrou-marbre` (verrou avant + detection apres) et
`proteger-modifier-marbre` (porte de modification legitime).
---
## Pourquoi ce protocole ?
Pendant 7 jours, le comportement de coordination a ete casse a plusieurs
reprises (Cerberus travaille seul, chaines rompues, AGENTS.md corrompu deux
fois, doublons dans l historique). Les tests en aval (garde-fous) detectent
la casse APRES coup, mais rien n empechait la modification du noyau AVANT.
La demande utilisateur : "graver dans le marbre des regles qui nous
empechent de les modifier sans passer par un protocole de securite du code".
Ce protocole est la reponse : le marbre, sa verification, et sa porte de
modification controlee.
## Les zones du marbre (manifeste marbre.json)
Le manifeste `cerveau-projet/agents/regles-immuables/marbre/marbre.json`
liste les zones protegees avec leur empreinte SHA-256 :
- `constitution` : la zone Constitution d AGENTS.md (Configuration Active +
  cycle fondamental, entre les marqueurs `<!-- MARBRE:DEBUT/FIN -->`) ;
- `regles-groupes-agents` : la regle immuable des groupes d agents ;
- `cerberus.c0`, `cerberus.c0b`, `cerberus.c10`, `cerberus.c14`,
  `cerberus.c20` : les cases critiques de la carte de Cerberus (relecture,
  anti-arret, activation, chaine de fin, fin de coordination).
Chaque zone a une RAISON documentee dans le manifeste.
## Les deux temps de la protection
1. **AVANT (verrou a la source)** : les outils du noyau qui ecrivent dans
   les fichiers proteges verifient le marbre avant d ecrire
   (activer-agent-principal : zone `constitution` ; editer-parcours : les
   cases protegees de l agent edite). Zone divisee = ecriture REFUSEE, la
   chaine s arrete immediatement.
2. **APRES (garde-fou)** : la non-regression lance `proteger-verrou-marbre
   --tous` (test-057). Toute divergence = KO = le marbre est brise.
## Le flux de modification legitime (la porte)
Un agent qui a besoin de modifier une zone du marbre ne la modifie JAMAIS
directement. Le flux impose :
1. **L agent s ARRETE** : il signale le besoin sans rien ecrire.
2. **Le GARDIEN propose** : zone concernee, raison, impact, alternative.
3. **L UTILISATEUR valide** explicitement (aucun agent ne peut se
   debloquer seul).
4. **RELECTURE OBLIGATOIRE (v0.1.1, demande utilisateur 2026-08-16)** :
   pour toute zone de REGLES (fichier dans `regles-immuables/`), la porte
   lance AUTOMATIQUEMENT `detecter-contradictions --regles` (audit Argus :
   doublons de titres, references cassees, concordance source/protocole)
   AVANT d accepter l autorisation. Non PROPRE = REFUS (code 1), meme avec
   `--autorisation` : corriger les contradictions, relancer l audit, puis
   repasser la porte. Le champ `relecture: Argus PROPRE` est journalise.
5. **Le gardien execute** :
   `python3 proteger-modifier-marbre.py --zone <nom> --raison "<...>" --autorisation <cle>`
6. L empreinte est mise a jour dans marbre.json + la modification est
   journalisee dans `marbre-log.jsonl` (date, zone, raison, autorise_par).
## Regles d or
- Une zone du marbre modifiee SANS passer par la porte = VIOLATION :
  verrou bloque + test-057 KO + la chaine s arrete.
- Le manifeste ne se modifie que par la porte. Jamais a la main.
- L autorisation est HUMAINE : un agent ne peut pas re-empreinter une zone
  qu il vient de modifier lui-meme sans validation de l utilisateur.
- Ajouter une NOUVELLE zone au marbre = meme porte : le gardien propose,
  l utilisateur valide, la zone est ajoutee avec sa raison (une zone de
  regles exige aussi la relecture Argus PROPRE).
- Une nouvelle regle immuable qui n est pas gravee n a AUCUNE protection :
  toute regle immuable majeure DOIT entrer au marbre via cette porte,
  apres relecture Argus PROPRE.
## Raccords
- Outils : `proteger-verrou-marbre`, `proteger-modifier-marbre`
  (categorie Proteger, assignes au Gardien).
- Garde-fou : test-057 (marbre intact dans la non-regression).
- Regle immuable : regles-groupes-agents.md (groupes et domaines separes).
- Relecture : `detecter-contradictions` (audit Argus, outil Argus) - doublons,
  contradictions, concordance source/protocole.
- Garde-fou : test-084 (relecture obligatoire avant gravure) - la porte
  exige l audit Argus PROPRE pour les zones de regles.
