---
identite:
  nom: bilan-strategique-v1
  version: 0.1.0
  cree: 2026-08-22
  type: rapport
  appartient_a: themis
  commun: false
  tags: bilan, v1, v2, strategie, lecons
---
# BILAN STRATEGIQUE v1 : ce qui merite vraiment d etre dans la v2

**Agent** : Themis (evaluatrice croisee)
**Date** : 2026-08-22 (relance 2026-08-24, demande utilisateur)
**Methode** : 212 lecons en BDD (buffy 46, janus 45, themis 39, vulcain 33, morpheus 27, chiron 7, clio 3, hygie 3, redacteur-v2 3, cerberus 2, gardien 2, socrate 2) + AGENTS-historique.md + audit croise (combos-audit-themis) + experience des rounds.
**Honnetete brutale, pas de politesse.**

---

## 1. Ce qui a ete VRAIMENT benefique (a garder ABSOLUMENT en v2)

### 1.1 Les lecons en BDD (lecons.db) -- LE meilleur investissement de la v1
- **212 lecons** produites en ~3 semaines, structurees par agent + domaine + verdict. C est la memoire reelle du projet : chaque erreur, chaque contournement, chaque pattern decouvert y est.
- Sans la BDD, la v1 aurait repete ses erreurs 10 fois. Elle est la PREUVE que le systeme apprend.
- **A garder tel quel en v2** : schema, anti-usurpation (chaque agent n ecrit que ses lecons), fenetre glissante corrections.md.

### 1.2 Les cartes de decision (parcours JSON) -- le guidage qui tient
- Les 11 parcours (cerberus, buffy, vulcain, morpheus, clio, janus, themis, atlas, socrate, chiron, hygie + secondaires) sont la SOURCE DE VERITE du comportement des agents. L agent ne decide plus : il SUIT.
- Pattern 14 (fiche = parcours en version) et valider-cartes-decision CONFORME ont rendu la coherence verifiable.
- **A garder** : le principe "la carte guide, jamais l improvisation". C est ce qui a fait tenir les rounds.

### 1.3 Le cycle Cerberus -> Agent -> Cerberus + chaines de controle
- L activation documentee (AGENTS.md + historique + classeur) et la fin qui suit SA carte (Pattern 13) ont cree une discipline reelle.
- Themis (audit) + Janus (controle) en maillon automatique ont attrape des dizaines de defauts AVANT qu ils ne deviennent des incidents.
- **A garder** : la double verification (audit + controle) sur les missions a risque.

### 1.4 Les outils de validation automatique
- valider-cartes-decision, valider-conformite-ascii, valider-nommage, detecter-residus, evaluer-processus, verifier-role-fichier : la v1 a appris que TOUT doit etre verifiable par un outil, pas par la bonne volonte.
- **A garder** : le principe "chaque regle a un outil qui la verifie".

### 1.5 Le classeur de variables (profil systeme, profil sessions)
- Stocker l OS, la session, l agent actif a elimine les confusions multi-sessions (id llm-N -> session-llm-N).
- **A garder** : le MODE ID (sidentifier) et le classeur.

---

## 2. Ce qui a ete NEFASTE (a NE PAS reproduire en v2)

### 2.1 La sur-ingenierie de la gouvernance
- Regles sur regles : immuables, absolues, garde-fous, patterns 1 a 14, protocoles, conventions. A la fin de la v1, un agent doit LIRE une fiche enorme + des corrections + des cartes + des protocoles AVANT de travailler.
- **Cout reel** : temps de relecture massif, corrections.md de janus = 6000+ lignes, fiches qui se contredisent (ex : regle 'UNIQUE outil' de Clio vs habilitation editer-fichier), lecons de re-education en cascade (chiron).
- **Verdict brut** : la gouvernance a DEPASSE le travail qu elle protegeait.

### 2.2 Les fausses exclusions / habilitations derivees
- Le verrou d habilitation (proteger-verrou-habilitation.py) derive des CARTES : si un agent n a pas l indice outil dans sa carte, l outil le BLOQUE. Resultat : Clio (muse du README) bloquee sur editer-fichier, redirections systematiques vers buffy, inter-rounds en cascade.
- Ce n est pas le verrou qui est mauvais : c est la DECOUVERTE TARDIVE que les cartes devaient porter les indices outils. On a du re-eduquer 3+ agents apres coup.

### 2.3 L historique qui s empile sans se nettoyer
- AGENTS-historique.md grossit a chaque activation. Corrections.md aussi (fenetre glissante mal appliquee). Les lecons .db doublonnent des corrections.md. 3 memoires qui se recouvrent sans se synchroniser.
- **Cout** : confusions, entrees parasites apres erreurs de commande reactiver (corrigees a la main), temps de grep pour retrouver l information.

### 2.4 Les rounds trop longs / enchainements d agents
- Certaines missions ont enchaine Cerberus -> Agent -> Themis -> Agent -> Janus -> Cerberus -> Clio -> ... avec des inter-rounds (D1, P-A, P-B). Chaque maillon relit SA fiche + SES corrections : le cout de contexte explose.
- **Verdict** : la chaine de controle est saine, mais elle doit etre PROPORTIONNEE a la taille de la modification (une ligne de tableau ne justifie pas 6 activations).

### 2.5 Les outils crees puis abandonnes
- Plusieurs outils de la v1 (nettoyer-sessions, convertir-mermaid, etc.) ont ete crees pour des besoins ponctuels puis plus utilises. 165 outils dont une partie dormante.
- **Cout** : maintenance, catalogue, compteurs README a jour, non-regression a chaque bump.

---

## 3. Les regles qui fonctionnent VRAIMENT (a garder telles quelles)

1. **REGLE DE RELECTURE** : a chaque activation, relire SA fiche et SES corrections (jamais celles des autres). Simple, efficace, non negociable.
2. **REGLE REGISTRE** : chaque outil utilise est declare dans le registre JSONL. Quand elle a ete respectee (apres la lecon D1), les controles sont passes sans boucle KO.
3. **DRY-RUN OBLIGATOIRE avant ecriture** : a evite des dizaines d ecrasements. (Incident double README du 14/08 : la preuve de ce qui arrive SANS dry-run.)
4. **ASCII strict + LF pur** : la norme qui evite les fichiers illisibles et les faux positifs de detecteurs.
5. **RVAV (Rechercher-Verifier-Analyser-Valider)** avant de conclure une maj README.
6. **Le verifier comme juge de verite** : mettre-a-jour-readme --verifier (ou equivalent) decide, pas la memoire.
7. **La fin suit SA carte (Pattern 13)** : une regle unique "toujours reactiver Cerberus" etait fausse ; la carte dit qui activer.
8. **Anti-usurpation des lecons** : chaque agent n ecrit que SES lecons. Fiable.
9. **La double verification (Themis + Janus)** sur les missions qui modifient outils/cartes : a attrape les vrais bugs.

---

## 4. Le versionning : utile ou fardeau ?

**Verdict : UTILE comme signal, FARDEAU comme discipline.**

- **Utile** : bumpper les versions des outils/cartes (mettre-a-jour-versions) a permis de detecter les fichiers oublies (spec vs py vs md) et de tracer les evolutions. Le bump 0.4.4 -> 0.4.5 de mettre-a-jour-readme a force la coherence py/sh/md.
- **Fardeau** : la synchronisation versionnaire est devenue une fin en soi. Chaque bump exige de verifier N fichiers (spec, ref, md, lecons.db, fiches, tests pins). Les faux positifs (lecons.db qui reference une ancienne version sans que ce soit un defaut) coutent du temps. Le test-004 (pin de version de carte) a casse une non-regression pour un bump legitime.
- **Recommandation v2** : garder le versionning POUR LES OUTILS (semver reel, source de verite unique spec), SUPPRIMER le versionning croise fiche/carte (Pattern 14) ou le rendre automatique (le bump met a jour la fiche sans action manuelle).

---

## 5. Les lecons les plus importantes (a NE PAS oublier)

1. **Une regle sans outil qui la verifie est une regle morte** : chaque garde-fou doit avoir son test/outil (test-038 pour le badge, valider-cartes pour les parcours).
2. **Un agent de redaction lie a un fichier unique ne peut pas couvrir un nouveau fichier sans re-education** : la lecon Chiron/Clio/readme-v2. Toute nouvelle cible de documentation exige branche de carte + sources de verite AVANT la mission.
3. **Apres une decision qui assouplit une regle, verifier TOUTES les occurrences de l ancienne regle** (pas seulement la fiche : les corrections, les cartes, les lecons). Pattern 14 sync la version, PAS les regles.
4. **Le registre d usages est la memoire de l execution** : un registre incomplet = boucle KO = cout double. Toujours declarer TOUS les outils, y compris ceux du demarrage (guider-parcours, lire-fichier).
5. **Les habilitations doivent se decider AVANT, pas se decouvrir pendant** : verifier les indices outils de la carte AVANT de confier une mission.
6. **editer-fichier ne remplace que la PREMIERE occurrence** : sans --global, on corrige une fois sur deux (badge README affichage vs href).
7. **Le dry-run est la seule protection reelle contre l ecrasement** : l incident double README (14/08) l a prouve.

---

## 6. Ce qu on ne refera PAS dans la v2

1. **PAS de gouvernance qui double le travail** : la v2 doit avoir MOINS de regles, plus d outils. Une regle qui demande de lire 3 fichiers pour agir est supprimee.
2. **PAS de verrou d habilitation derive des cartes sans audit prealable** : les indices outils des cartes sont verifies AVANT chaque nouvelle mission, pas apres.
3. **PAS de re-education en cascade (chiron)** pour des defauts de cartes : les cartes sont controlees a la conception, pas re-enseignees a l usage.
4. **PAS de 3 memoires non synchronisees** : une SEULE source de verite pour l historique (ou des liens, jamais des copies).
5. **PAS de versionning croise fiche/carte manuel** : automatise ou supprime.
6. **PAS de chaines de controle disproportionnees** : une modification d une ligne = un controle simple, pas 6 activations.
7. **PAS d outils jetables** : un outil n est cree que si 3 usages prevus ou un besoin recurrent prouve.
8. **PAS d historique infini** : rotation automatique / archivage par periode.

---

## CONCLUSION

La v1 a prouve UNE chose enorme : un collectif d agents pilote par des cartes + des lecons APPREND et se corrige. Les 212 lecons et les 165 outils sont un capital reel.

Mais la v1 a aussi montre sa limite : la gouvernance est devenue plus lourde que le travail. La v2 doit garder LE CYCLE (Cerberus -> agent -> controles), LES LECONS, LES CARTES et LES OUTILS DE VALIDATION -- et jeter la bureaucratie qui les entoure.

**En une phrase : la v2 doit etre la v1 SANS la paperasse, AVEC la memoire.**
