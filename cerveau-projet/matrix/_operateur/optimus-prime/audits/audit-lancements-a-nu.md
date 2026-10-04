---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# AUDIT -- LES LANCEMENTS A NU ET L ETAT DE VIE DES BOUCLES (EO-428 / MO-413)

> Consigne du createur (2026-09-25) : < Fais d abord le controle seul : liste ce qui
> reste a nu et l etat de vie de chaque boucle, avant toute reparation. >
> AUDIT = LECTURE SEULE : aucun fichier de service modifie, rien n est repare.
> Chaque point porte la commande qui le VERIFIE (a rejouer telle quelle).
> Symptome constate par le createur : le shell windows se coupe et reapparait, avec un
> cmd.exe vide qui contient le CLI de travail. Demande : la serie de controles.

## 1. INVENTAIRE : 163 SITES DE LANCEMENT, 139 A NU, 24 COUVERTS

Commande (a rejouer) : le scanner ci-dessous parcourt TOUT le Python de la Matrice
(`matrice/` ET `_operateur/`), retient chaque appel de processus
(`subprocess.run|Popen|call|check_output|check_call|getoutput`, `os.system`, `os.popen`)
et le classe COUVERT si la fenetre de 12 lignes qui suit porte les drapeaux du domicile
partage (`creationflags`, `CREATE_NO_WINDOW`, `CREATE_NEW_PROCESS_GROUP`, `startupinfo`,
`SW_HIDE`, `drapeaux_invisibles`, `lancer_invisible`, `lancement`).

    python3 - <<'EOF'
    import os,re
    RAC=os.getcwd()
    COUV=re.compile(r"creationflags|CREATE_NO_WINDOW|CREATE_NEW_PROCESS_GROUP|startupinfo|SW_HIDE|drapeaux_invisibles|lancer_invisible|lancement")
    APPEL=re.compile(r"subprocess\.(run|Popen|call|check_output|check_call|getoutput)\s*\(|os\.system\s*\(|os\.popen\s*\(")
    sites=[]
    for base,dirs,fs in os.walk(RAC):
        dirs[:]=[d for d in dirs if d not in ('.git','__pycache__','tmp-optimus','.venv','node_modules')]
        for f in fs:
            if not f.endswith('.py'): continue
            p=os.path.join(base,f); rel=os.path.relpath(p,RAC).replace(os.sep,'/')
            L=open(p,encoding='utf-8',errors='replace').read().split('\n')
            for i,l in enumerate(L):
                if not APPEL.search(l): continue
                ctx='\n'.join(L[i:i+12])
                cov=bool(COUV.search(ctx)) or rel.endswith('commun/lancement.py')
                sites.append((rel,i+1,cov))
    nu=[s for s in sites if not s[2]]
    print(len(sites),len(nu),len(sites)-len(nu))
    for rel,i,c in nu: print(rel+":"+str(i))
    EOF

MESURE : 163 sites | **139 A NU** | 24 couverts.

Repartition des 139 a nu, par zone :

| Zone | A nu | Dont le lancement part d un daemon (sans console visible) |
|---|---|---|
| racine `lancer.py` (porte d entree interactive) | 1 | non |
| `matrice/data/commun/` | 2 | non |
| `matrice/data/outils/` (12 outils) | 10 | non |
| `matrice/pilote/` | 3 | non |
| **`matrice/routines/` (serveur + boucles)** | **8** | **OUI** |
| `_operateur/optimus-prime/` (super-combos, outils) | 115 | non |

Les 8 sites de `matrice/routines/` -- le seul sous-ensemble atteint par un processus
de fond :

| Site | Ce qui est lance |
|---|---|
| `routines/vie/server_matrice.py:79` | `tasklist` (requete) |
| `routines/vie/server_matrice.py:114` | **`powershell`** |
| `routines/veille-flux/commun.py:484, 538, 594` | 3 lancements, routine de **cadence 300 s** |
| `routines/suivi-sync/commun.py:205, 252` | 2 lancements, routine de **cadence 60 s** |
| `selecteur-flux/verifier-selecteur.py:46` | `tasklist` |

Les 24 sites couverts vivent dans 9 fichiers : `matrice/data/commun/lancement.py`,
`matrice/data/outils/{benchmark,dialoguer,executer}/commun.py`, `matrice/pilote/commun.py`,
`matrice/routines/vigie-portes/commun.py`, `matrice/routines/vigie-profil/tour/fonctions.py`,
`_operateur/.../espions/espion-tracebacks-optimus.py`, `_operateur/.../pilote/commun.py` (16 sites).

## 2. LE DISCRIMINANT NEGATIF : RIEN NE DEMANDE UNE CONSOLE NEUVE

Commande (a rejouer) :
    grep -rn --include=*.py -F "CREATE_NEW_CONSOLE" .
    grep -rn --include=*.py -F "DETACHED_PROCESS" .
    grep -rn --include=*.py -F "shell=True" .
    grep -rn --include=*.py -F "os.startfile" .
    find . -maxdepth 3 \( -name "*.bat" -o -name "*.cmd" -o -name "*.ps1" -o -name "*.vbs" \)

MESURE : **0** occurrence de `CREATE_NEW_CONSOLE`, **0** de `DETACHED_PROCESS`,
**0** de `shell=True` (une seule mention est un commentaire d interdiction dans
`outils/executer`), **0** de `os.startfile`, **0** de `GenerateConsoleCtrlEvent`,
**0** fichier `.bat` / `.cmd` / `.ps1` / `.vbs` / `.lnk` dans le workspace.
Aucun lanceur hors Python. Le serveur lui-meme n est pas demarre a la main : il passe
par `routines/vie/activer.py:44-47` -> `lancer_invisible(..., script="server_matrice.py")`.

## 3. VERDICT SUR LA CAUSE : L ACCUSATION PRECEDENTE EST DEMOTEE

`matrice/data/commun/lancement.py` (lu en entier) : `drapeaux_invisibles()` rend, sous
Windows, `CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP` + `STARTUPINFO` avec
`SW_HIDE`. **`CREATE_NO_WINDOW` ne supprime pas la console : il en donne une SANS
fenetre.** Le daemon lance par `vie activer` POSSEDE donc une console (invisible), et un
enfant lance ensuite sans drapeau **herite de cette console** -- il n en recoit pas une
nouvelle. Le mecanisme qui produirait une fenetre (parent SANS console -> enfant console
nu -> Windows alloue une console VISIBLE) exige `DETACHED_PROCESS` ou une console
supprimee : **il n existe nulle part dans ce code (point 2).**

CE QUI EST PROUVE : les 139 appels a nu **enfreignent la convention** (< tout relancement
de processus de fond passe par ICI >, en-tete de `lancement.py`), et 8 d entre eux
partent d un processus de fond.
CE QUI N EST PAS PROUVE : le lien causal entre ces 8 appels et la fenetre `cmd.exe`
vide observee. L hypothese posee pendant la cadrage de MO-412 (< detaches, donc sans
console >) est **CONTREDITE par la lecture du domicile** : elle est demotee ici, et la
reparation MO-412 ne doit PAS etre lancee sur cette base.

## 4. ETAT DE VIE DES BOUCLES (mesure a l instant du controle)

Commande (a rejouer) :
    python3 cerveau-projet/matrix/lancer.py vie etat

| Boucle | Etat | Cadence declaree | Cause du dernier lancement |
|---|---|---|---|
| veille-flux | ARRET | 300 s | Veille terminee proprement. |
| espion-integrite | ARRET | 300 s | Boucle terminee proprement. |
| vigie-profil | ARRET | 900 s | Boucle terminee proprement. |
| suivi-sync | ARRET | 60 s | `[08:32:04] suivi-sync : arret cooperatif` |
| vigie-portes | ARRET | 900 s | Boucle terminee proprement. |
| routeur-maintenance | ARRET | 30 s | Arret cooperatif. |
| verifier-liens-cartes | ARRET | 3600 s | `[08:32:06] verifier-liens-cartes : arret cooperatif` |
| serveur matrice | ARRET | -- | -- |

`La Matrice dort (serveur et routines arretes).` Cet etat est **voulu** : l arret
cooperatif du round precedent (demande du createur, pour faire cesser les fenetres).

FRAICHEUR, PID et TRACES, mesures fichier par fichier :

| Boucle | Fichier `.pid` | Age etat (min) | Age trace (min) | Cadence json : pid inscrit |
|---|---|---|---|---|
| routeur-maintenance | absent | 2.3 | -- | **18192** (2026-09-24 22:22:38) |
| suivi-sync | absent | 2.4 | -- | -- |
| espion-integrite | absent | 5.4 | 2.1 | -- |
| vigie-portes | absent | 14.9 | 2.1 | **4764** (2026-09-24 22:18:36) |
| vigie-profil | absent | 15.4 | 2.1 | **13940** (2026-09-24 22:18:35) |
| verifier-liens-cartes | absent | 15.4 | -- | -- |
| veille-flux | absent | -- | -- | **6424** (2026-09-25 08:31:50) |

## 5. ECARTS MESURES (dits, non repares)

1. **139 lancements a nu** contre une convention qui en exige le passage par le
   domicile unique ; 8 d entre eux partent d un processus de fond. Aucun n est prouve
   cause du symptome.
2. **Residu d arret** : apres un arret cooperatif, le `.pid` disparait mais le fichier
   `*-cadence.json` continue de nommer un **pid mort** (18192, 4764, 13940, 6424). Un
   controle ne peut donc pas distinguer < proprietaire declare de la cadence > de
   < proprietaire courant > : la lecture est **ambigue apres arret**.
3. **Le controle ne peut pas ETRE tenu vivant** : les boucles etant arretees, la
   mesure d etat ci-dessus ne peut pas montrer un faux vivant. Un controle de tenue de
   vie n a de valeur que **Matrice allumee** (cadence 30 s pour `routeur-maintenance`,
   60 s pour `suivi-sync`).

## 6. CE QUI RESTE OUVERT (pour la reparation MO-412)

- La cause de la fenetre `cmd.exe` vide reste **NON ETABLIE**. Deux instruments
  discriminants, a choisir AVANT toute reparation :
  (a) **le piege a l instant** : au moment ou la fenetre apparait, capturer l ascendance
  reelle du processus (`wmic process where "name like '%cmd%' or name like '%conhost%'"
  get ProcessId,ParentProcessId,CommandLine`) -- le parent nomme le coupable ;
  (b) **le banc un-par-un** : rallumer UNE boucle seule (la plus suspecte : `veille-flux`,
  cadence 300 s) et observer ; puis la suivante. Le symptome etant < regulier >, une
  boucle de cadence courte le reproduit vite.
- Les points 1 et 2 ci-dessus sont reels et reparables **sans attendre** (convention +
  residu d arret) : ce sont des ecarts, pas des hypotheses.

---

*Mesure du 2026-09-25, lecture seule. Fichiers lus en entier pour ce constat :
`matrice/data/commun/lancement.py`, `matrice/routines/vie/server_matrice.py` (sites),
`routines/veille-flux/commun.py` (sites), `routines/suivi-sync/commun.py` (sites),
`routines/selecteur-flux/verifier-selecteur.py` (sites), `routines/vie/activer.py` (sites).*
