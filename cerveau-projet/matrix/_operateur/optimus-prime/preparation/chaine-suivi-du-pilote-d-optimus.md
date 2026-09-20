---
identite:
  type: chaine
  appartient_a: optimus-prime
  commun: false
  titre: Suivi du pilote d Optimus
  statut: todo
  pense-bete: PB-003
  nemesis: contre-analyse du 2026-09-19 (4 axes : panne muette, sixieme copie, colonnes, invisibilite)
  spec: SP-003
  todo: TD-003
---

# Suivi du pilote d Optimus

## Pense-bete -- la demande clarifiee

Voir les problemes DU PILOTE (pas ceux des missions : suivi-optimus s en charge). Quatre exigences
du createur : (1) des TABLEAUX, un par PARTIE du pilote ; (2) chaque tableau REFLECHI
individuellement -- aucune colonne inutile, aucune colonne constante, aucune duree sur un
evenement ; (3) des TEMPLATES de ce qu on met en place, sur le patron du cameleon ; (4) Optimus
etant INVISIBLE, le dossier des templates vit dans _operateur/optimus-prime/. Une panne du
pilote : une mission close sans fin, un lot perdu ou non termine, une injection refusee, un
enchainement casse, une file qui ne bouge plus, une pause armee et oubliee.

## Ce qui est deja mesure

- PARTIES DU PILOTE : 8 dossiers (checklist, entonnoir, file, filtrer, fin, injection, profil,
  reporter) + les modules commun.py, constants.py, personnalites.py, main.py, verifier-profil.py,
  et les etats JSON (file-missions-optimus.json, entonnoir-files-optimus.json, cycle-historique).
- LES FAITS DU PILOTE SONT DEJA ECRITS mais disperses : outbox.jsonl (481 lignes), suivi-optimus
  (717 evenements), defcon-historique (12 transitions), le journal du MARBRE. Aucun instrument ne
  les rassemble sous l angle PILOTE.
- PATRON DES TEMPLATES (matrice/templates) : un DOSSIER par nature d artefact, des .moule qui
  MIRRORENT l arborescence cible, des TROUS (__HUMAIN__) et un README.
- LECON DES COLONNES payee le 2026-09-19 : une duree sur un evenement n a pas de sens ; une
  colonne a 0 declare etait un placeholder qui mentait (144 missions) ; une colonne constante vaut
  - pour tout le monde.
- Le GARDE DES CARTES scanne TOUT .md sous _operateur/optimus-prime : chaque README de template
  devra porter sa carte, sinon la suite passe au rouge.
- L-016 : un template invisible ne peut servir qu un artefact INVISIBLE (le pilote).

## Ce qui reste a mesurer

- La liste FERMEE des pannes du pilote et celle qui n est detectable par PERSONNE aujourd hui.
- Le format du suivi (vue derivee + journal des verdicts ?) et la porte qui le recalcule.

## NEMESIS -- avis contradictoire AVANT d ecrire

1. PANNE MUETTE : un suivi bati sur les fichiers ne voit que ce qui est ecrit ; un pilote arrete
   produit des tableaux VIDES, et un vide se lit calme. Il faut une colonne ATTENDU et crier sur
   le SILENCE.
2. SIXIEME COPIE : un suivi qui ECRIT les memes faits serait une copie de plus, donc une
   divergence de plus (L-055). Le suivi doit etre une VUE DERIVEE.
3. COLONNES : une colonne se garde si elle VARIE ou si elle PORTE UN VERDICT. Sur un evenement,
   jamais de duree ; un vide se dit (inconnu), jamais 0.
4. INVISIBILITE : des moules que personne ne lit pourrissent. Il faut une PORTE qui les lit et un
   README a carte qui les declare.

## SPEC (SP-003) -- le suivi du pilote et ses tableaux

### Domicile et nature

- Dossier invisibilite : _operateur/optimus-prime/suivi-pilote/.
- suivi-pilote.md : la VUE, DERIVEE et regenerable (recalculee par la porte, jamais editee a la
  main) -- c est le fichier a lire pour voir l etat du pilote.
- suivi-pilote.jsonl : les VERDICTS de panne seulement (date, partie, gravite, motif), append-only
  -- on ne recopie AUCUN fait deja ecrit ailleurs : on ecrit ce que l instrument a JUGE.
- Sources, jamais recopiees : outbox.jsonl, suivi-optimus.jsonl, file-missions-optimus.json,
  entonnoir-files-optimus.json, defcon-historique.jsonl, journal du MARBRE.

### Table 0 -- PANNES (la seule qui CRIE, en tete de vue)

| Gravite | Partie | Fait attendu | Constat | Silence | Porte qui repare |
|---|---|---|---|---|---|

- Elle n existe que s il y a une panne ; sinon la vue dit AUCUNE PANNE CONSTATEE. La colonne
  Silence est un ECART date : c est elle qui crie quand le pilote ne fait plus rien.
- Refuse : une colonne Etat (CONSTAT est l etat, dit en clair) ; aucun tableau vide affiche.

### Table 1 -- INJECTION (partie injection/)

| Mission | Injectee le | Poids (tok) | Lecons inj./ecartees | Refus |
|---|---|---|---|---|

- Poids et lecons : mesures a la source, elles montrent la derive du sac-a-dos (EO-270).
- Refuse : Duree (une injection est un INSTANT) et Fichiers (vide a l injection).

### Table 2 -- FILE (partie file/)

| Mission | Statut | Dans le lot | En attente depuis | Dernier fait | Silence |
|---|---|---|---|---|---|

- Silence : l ecart entre la promesse (mission en cours) et le dernier fait -- c est la colonne
  qui voit une mission ouverte qui n avance pas.
- Refuse : Theme (il vit dans suivi-optimus, on ne le recopie pas) et Fichiers (bruit).

### Table 3 -- LOT (partie file/, un tableau a part)

| Lot | Arme le | Portee | Ecoulees | Retirees | Tete | Retour consolide | Enchainement |
|---|---|---|---|---|---|---|---|

- Enchainement dit auto / STOP, et le MOTIF du STOP : c est la table qui repond au bug du
  createur (le pilote qui s arrete apres chaque mission).
- Panne lue : portee sans tete, retour consolide absent alors que tout est ecoule, STOP sans motif.

### Table 4 -- ENTONNOIR

| File | Items | Tete | Urgence de la tete | Age de la tete |
|---|---|---|---|---|

- Age : un item qui vieillit est un travail qui dort.

### Table 5 -- BRIN

| Rang | Item | Urgence | Categorie | Depose le | Age |
|---|---|---|---|---|---|

- Plus une LIGNE de coherence (pas une colonne) : brin = somme des files ? tisse le ... -- la
  divergence du maillon 5 est ainsi vue ICI, en un mot.

### Table 6 -- CLOTURES ET ENCHAINEMENT (partie fin/)

| Mission close | Fin a | Bilan | Enchainement | Motif du STOP |
|---|---|---|---|---|

- Bilan dit pose / ABSENT : une trace muette se voit. La DUREE de la mission vit dans
  suivi-optimus (intervalle) et n est PAS recopiee ici.

### Table 7 -- DEMANDES FILTREES (partie filtrer/)

| Crochet | Recu le | Porte visee | Action posee | Refus |
|---|---|---|---|---|

- Panne lue : une demande recue et jamais deposee.

### Table 8 -- GARDES (pause de session, defcon)

| Garde | Etat | Depuis | Motif |
|---|---|---|---|

- Panne lue : une pause armee et oubliee -- l agent s arrete et personne ne le voit.

### La regle des colonnes, ecrite UNE fois

Une colonne se garde si elle VARIE (deux valeurs au moins observees sur le reel) ou si elle PORTE
UN VERDICT. Sinon, elle monte en resume au-dessus du tableau. Sur un EVENEMENT : jamais de duree.
Un VIDE se dit (inconnu) ; il ne s affiche JAMAIS 0.

### TEMPLATES (exigence 4)

- Dossier : _operateur/optimus-prime/templates/ -- un sous-dossier par nature d artefact
  INVISIBLE (ex. suivi-pilote-bdd, porte-pilote), des fichiers .moule qui MIRRORENT
  l arborescence cible, des TROUS (__PARTIE__, __COLONNE__), et un README A CARTE
  (type readme, appartient_a optimus-prime, commun false) qui DECLARE qui lit ces moules.
- Regle L-016 : un moule invisible ne fabrique que de l INVISIBLE. Le visible garde
  matrice/templates (patron outil-bdd / theme-bdd).
- Une PORTE lit les moules et pose l artefact : sans elle, le dossier invisible est un cimetiere
  (axe 4 de la contre-analyse).


## TODO (TD-003) -- le decoupage, une mission par objet, avec sa preuve

REGLE COMMUNE : chaque mission livre par la PORTE, compile (py_compile), trace en BDD, repose
l integrite, et passe la non-regression. Toute mesure est faite AVANT d ecrire.

- T1 -- LA LISTE FERMEE DES PANNES DU PILOTE (la mesure qui manque avant tout code). Nommer
  chaque panne : le fait attendu, la source qui le porte, le seuil de silence, la gravite, et la
  porte qui repare. Dire surtout celle que PERSONNE ne detecte aujourd hui (candidate : une
  mission en cours qui n avance plus, et une pause armee puis oubliee). Livrable : un fichier de
  declaration dans le domicile du suivi. Preuve exigee : la liste confrontee aux 4 maillons de la
  non-regression (quelle panne est deja vue, ou, et laquelle ne l est pas).

- T2 -- LA PORTE suivi-pilote (le coeur). Domicile _operateur/optimus-prime/suivi-pilote/ : la
  vue DERIVEE suivi-pilote.md (Table 0 a Table 8), le journal des VERDICTS suivi-pilote.jsonl
  (append-only, aucune recopie de fait), et le verbe qui recalcule la vue depuis les sources.
  Preuve exigee : la vue sur le reel ; un COBAYE de panne (file figee ou mission en cours sans
  fait) qui fait CRIER la Table 0 avec sa colonne Silence ; un CONTRE-TEMOIN sain ou la vue dit
  AUCUNE PANNE CONSTATEE ; et la preuve que la vue ne recopie rien (aucun fait ecrit deux fois).

- T3 -- LES TEMPLATES INVISIBLES (exigence 4). Dossier _operateur/optimus-prime/templates/ : un
  sous-dossier par nature d artefact du pilote, des .moule qui mirrorrent l arborescence cible
  avec leurs TROUS, et un README A CARTE (type readme, appartient_a optimus-prime, commun false)
  qui DECLARE qui lit ces moules. Une PORTE lit les moules et pose l artefact. Preuve exigee : le
  gabarit pose un artefact de bout en bout dans une zone jetable ; le garde des cartes reste OK ;
  contre-temoin : un moule SANS trou refuse (un moule sans trou fabrique de la copie morte).

- T4 -- LE CONTROLE PERMANENT. Une etape du lanceur de non-regression lit la porte suivi-pilote et
  CRIE si la Table 0 n est pas vide. Preuve exigee : la suite reste verte quand le pilote est sain,
  et passe au rouge, nommement, quand une panne est posee dans un cobaye.

ORDRE : T1 (mesurer) -> T2 (la porte) -> T3 (les templates) -> T4 (le controle permanent). T2 ne
peut pas se decouper avant T1 : une porte qui crie sans liste fermee crie au hasard.
