---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# AUDIT -- MO-445 : L INSTRUMENT QUI NOMME LA FENETRE (suite de MO-413 / EO-428)

> Consigne (MO-445) : construire l instrument qui NOMME le coupable AU MOMENT ou la
> fenetre apparait, et couvrir la suite de controle. AUDIT = LECTURE SEULE : aucun
> fichier de service modifie, rien n est repare. Chaque point porte la commande qui
> le VERIFIE (a rejouer telle quelle).
> SUITE DE MO-413 (`audits/audit-lancements-a-nu.md`) : le controle seul est fait ;
> ce round LIVRE l instrument et re-mesure les axes.

## 1. LE LIVRABLE : `audits/piege-fenetre-cmd.py`

Instrument autonome, LECTURE SEULE, trois modes :

    python3 cerveau-projet/matrix/_operateur/optimus-prime/audits/piege-fenetre-cmd.py instant
    python3 _operateur/optimus-prime/audits/piege-fenetre-cmd.py piege [--duree 300] [--cadence 2] [--journal <fichier>]
    python3 _operateur/optimus-prime/audits/piege-fenetre-cmd.py auto-test

`instant` : une photo -- tout cmd.exe/conhost.exe vivant, avec sa CHAINE D ASCENDANCE
(le parent nomme le coupable). `piege` : surveille et rend chaque NOUVEAU cmd/conhost
au moment ou il nait (code retour 1 des qu une fenetre est attribuee ; journal JSONL
optionnel). `auto-test` : preuve deterministe (voir section 2). Toute option inconnue
est un REFUS NOMME (code 2), aucun mode ne s invente.

## 2. PREUVE DE L INSTRUMENT (nominal ET negatif)

Commande : `python3 cerveau-projet/matrix/_operateur/optimus-prime/audits/piege-fenetre-cmd.py auto-test`. Mesure du 2026-09-27 :

    PASS : contre-temoin (calme)     un cmd deja vu n est PAS resigne
    PASS : cobaye (mord)             le nouveau cmd est signale
    PASS : ascendance                cmd.exe <- python.exe <- python.exe <- explorer.exe
    PASS : parent hors snapshot      dernier maillon = inconnu (hors snapshot)
    PASS : cycle de pids             borne (3 maillons), pas de boucle infinie
    PASS : releve natif              ctypes rend 222 processus, 0 lance
    AUTO-TEST VERT : le detecteur mord ET epargne.

Le CONTRE-TEMOIN (le calme ne crie pas) est eprouve AVANT le cobaye (qui mord), et
deux cas limites sont couverts (parent disparu, cycle de pids).

## 3. MESURE AVANT/APRES : L EFFET OBSERVATEUR (defaut trouve et repare DANS l instrument)

Le premier instrument relevait les processus avec `wmic`. EPREUVE : `piege --duree 8
--cadence 2` a rendu **4 attributions de conhost.exe**, une par photo, dont le parent
etait `inconnu (hors snapshot)`.

DIAGNOSTIC : `wmic` est une application CONSOLE. Chaque appel cree un `conhost.exe`,
dont le parent (wmic) meurt aussitot -- donc absent du releve suivant. Le piege
ENGENDRAIT les conhost qu il surveillait, et son exclusion d auto-observation ne
pouvait pas remonter jusqu a lui (le maillon intermediaire etait deja mort).

REPARATION A LA SOURCE : le releve passe par l API NATIVE
`CreateToolhelp32Snapshot` (ctypes, bibliotheque standard) -- AUCUN processus n est
lance, donc aucune fenetre n est creee par l instrument. `--cmdline` (releve par wmic)
reste disponible pour un constat PONCTUEL, au prix avoue.

MESURE APRES (meme commande, 8 s, cadence 2) :

    avant  : 4 attribution(s)   <- auto-infligees par l instrument
    apres  : 0 attribution(s)   <- l instrument ne se regarde plus

## 4. CONSTAT LIVE (`instant`, 2026-09-27 14:07)

    Photo (ctypes) : 220 processus, 9 surveille(s) cmd.exe/conhost.exe

Les 9 surveilles sont des conhost.exe legitimes d applications tierces (LM Studio,
VS Code, TRCC/USBLCDNEW, HWINFO, pet.exe, et la chaine de l outil de travail), et UN
cmd.exe (pid 10880) dont le parent (pid 15988) a DISPARU. Aucun n est une fenetre
naissante : le symptome n etait pas en cours pendant la mesure.

CONSTATS :
1. Un conhost.exe accompagne CHAQUE application console (mecanisme normal) : le
   symptome est donc un conhost dont la console est MONTREE, pas un conhost en soi.
2. Le parent peut etre MORT avant la photo : l ascendance s arrete alors sur
   `inconnu (hors snapshot)`. C est une LIMITE de tout releve par instantane, DIRE et
   bornee (profondeur 12, marqueur explicite) -- elle se comble en capturant a
   cadence courte (`piege`), pendant que le parent vit.

## 5. LES LANCEMENTS A NU (autorite : le GARDE, pas mon heuristique)

Commande : `python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/outils/verifier-contrats-outils.py`
(depuis `cerveau-projet/matrix/`). Mesure du 2026-09-27 :

    [OK] boucles de fond : aucun lancement a nu (EO-428) : 13 site(s) de lancement
         dans les boucles, TOUS couverts | residu hors boucles MESURE : 18 a nu sur
         86 site(s), a vider par lots
    [OK] cycle de vie : une cadence ne nomme jamais un pid mort (EO-428)
    VERDICT OK : les contrats tiennent (9 controles).

LECTURE : les 8 sites de la CLASSE A RISQUE (les boucles de fond) sont couverts ;
il RESTE 18 sites a nu HORS boucles. OR ces 18 sites sont le SEUL endroit ou une
console peut naitre : un parent SANS console qui lance une application console sans
`drapeaux_invisibles()` fait allouer une console -- donc, potentiellement, une fenetre.
C est le seul chemin causal encore ouvert par le code.

NOTE DE METHODE : un scan brut (sans `drapeaux_popen` dans les motifs) rendait 73
sites a nu : c etait un FAUX POSITIF de l heuristique. L autorite est le garde, pas
le scan -- le dire evite d ouvrir un chantier sur une mesure fausse.

## 6. LA MATRICE VIT (tenue de vie)

Commande : `python3 cerveau-projet/matrix/lancer.py vie etat`. Mesure :

    serveur matrice : ACTIVE (PID 5276)
    7 routines : PASSE (eteintes, allumees par le service) -- veille-flux 300 s,
    espion-integrite 300 s, vigie-profil 900 s, suivi-sync 60 s, vigie-portes 900 s,
    routeur-maintenance 30 s, verifier-liens-cartes 3600 s
    La Matrice vit (serveur actif, 7 routines en passe servies par le service).

Le piege est donc ARMABLE des maintenant : le lancer pendant une session reelle, sans
autre geste, suffit a nommer la prochaine fenetre.

## 7. MATRICE DE COUVERTURE DE LA SUITE DE CONTROLE (les 5 axes demandes)

| Axe | Etat | Ou / preuve |
|---|---|---|
| lancements a nu | COUVERT (boucles) + RESIDU 18/86 | garde `verifier-contrats-outils` (section 5) |
| tenue de vie des boucles | COUVERT | porte `vie etat` + garde cycle-de-vie (section 6) |
| sante du serveur | COUVERT | `cockpit-matrice --route sante` (controle de 4.6) |
| ecritures de la zone de travail | COUVERT | gardes `garde-tmp`, `garde-residus-zone`, `perimetre` |
| attribution de la fenetre | PARTIEL : instrument LIVRE, maillon A CONSTRUIRE | ce round livre `piege-fenetre-cmd.py` ; le maillon de non-regression ne peut naitre qu UNE FOIS la fenetre prise et la cause confirmee |

L axe < attribution > est volontairement PARTIEL : un controle qui n a jamais vu la
fenetre ne peut pas la juger. Le prerequis (l instrument) est livre et prouve ; le
reste est a DECIDER apres une prise reelle.

## 8. CE QUI RESTE A DECIDER (l auditeur SIGNALE, il ne repare pas)

1. VIDER LE RESIDU 18/86 hors boucles (seul chemin causal encore ouvert) : c est un
   acte de REPARATION, deja nomme par le garde (< a vider par lots >).
2. ARMER LE PIEGE pendant une session reelle : `piege --duree 3600 --journal <fichier>`
   puis, quand une fenetre est prise, le journal NOMME l ascendance -- la cause se lit,
   elle ne s attend pas.
3. CONSTRUIRE LE MAILLON d attribution APRES une prise : il exige un temoin reel, donc
   il ne peut pas preceder la cause.
4. Le parent disparu (`inconnu`) reste une limite DITE de l instantane : la cadence
   courte la reduit, elle ne l annule pas.

---

*Mesure du 2026-09-27, lecture seule. Instrument livre :
`_operateur/optimus-prime/audits/piege-fenetre-cmd.py` (SHA apres publication :
bc3ae7847599c182...). Fichiers lus en entier : `matrice/data/commun/lancement.py`,
`audits/audit-lancements-a-nu.md`. Commandes rejouables citees en section 2, 4, 5, 6.*
