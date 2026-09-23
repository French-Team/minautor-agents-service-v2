---
identite:
  type: fiche
  appartient_a: matrice
  commun: true
---

# SYSTEME DE LA MACHINE -- fiche de la Matrice

> Fiche UNIQUE de la machine sur laquelle vit la Matrice : elle dit
> sur quel SYSTEME nous sommes, ce que la machine SAIT FAIRE, et
> quels OUTILS sont installes. Elle est TENUE A JOUR par la porte
> inventaire-systeme -- jamais a la main : un fait non mesure est
> un fait qui ment (L-055).

> Modele : la v1 (cerveau-projet/agents/tools/verifier/verifier-systeme).

## RESUME MACHINE

- **Machine** : Windows 10.0.19044 (AMD64) -- hote Optimus, utilisateur Optimus, session Console
- **CPU** : coeurs 16 (AMD64 Family 25 Model 33 Stepping 2, AuthenticAMD)
- **RAM** : 49072 Mo (disponible 30998 Mo au moment de la mesure)
- **Disque libre** : 43.7 Go -- charge CPU 11.2 %
- **GPU** : AMD Radeon RX 6700 XT (VRAM 12272 Mo)
- **Reseau** : hote Optimus [192.168.1.70]
- **Outils** : python3 3.14.4, node 24.14.1, git 2.53.0, bash 5.2.37, npm 11.16.0
- **Racine de la Matrice** : Z:\analyste-in-console\cerveau-projet\matrix

> Mesure du 2026-09-20 18:54:18 par la porte inventaire-systeme -- fiche complete : matrice/data/systeme-machine.md.

## SYSTEME

| Element | Valeur |
|---|---|
| OS | Windows |
| Version | 10.0.19044 |
| Architecture | AMD64 |
| Hote | Optimus |
| Utilisateur | Optimus |
| Session | Console |
| Python d execution | 3.14.4 |
| Racine de la Matrice | Z:\analyste-in-console\cerveau-projet\matrix |

## CAPACITES

| Capacite | Valeur |
|---|---|
| CPU -- coeurs logiques | 16 |
| CPU -- modele | AMD64 Family 25 Model 33 Stepping 2, AuthenticAMD |
| RAM -- totale (Mo) | 49072 |
| RAM -- disponible (Mo) | 30998 |
| Disque libre (Go) | 43.7 |
| Charge CPU (%) | 11.2 |
| GPU -- modele | AMD Radeon RX 6700 XT |
| GPU -- VRAM (Mo) | 12272 |

> Le tiret veut dire NON MESURE (dependance absente ou mesureur muet),
> jamais une valeur nulle : 0 serait un fait, et il serait faux.

## RESEAU

| Element | Valeur |
|---|---|
| Hote | Optimus |
| Adresses IPv4 | 192.168.1.70 |

## OUTILS INSTALLES

| Outil | Disponible | Version | Chemin |
|---|---|---|---|
| python3 | Oui | Python 3.14.4 | C:\Program Files\PyManager\python3.EXE |
| pip3 | Oui | pip 26.2.1 from C:\Users\Optimus\AppData\Local\Programs\Python\Python313\Lib\site-packages\pip (python 3.13) | C:\Users\Optimus\AppData\Local\Programs\Python\Python313\Scripts\pip3.EXE |
| node | Oui | v24.14.1 | C:\Program Files\nodejs\node.EXE |
| npm | Oui | 11.16.0 | C:\Program Files\nodejs\npm.CMD |
| git | Oui | git version 2.53.0.windows.2 | C:\Program Files\Git\mingw64\bin\git.EXE |
| bash | Oui | GNU bash, version 5.2.37(1)-release (x86_64-pc-msys) | C:\Program Files\Git\usr\bin\bash.EXE |
| rg | Non | - | - |

## TENUE A JOUR

| Geste | Commande |
|---|---|
| MESURER la machine et reecrire la fiche | python3 cerveau-projet/matrix/lancer.py inventaire-systeme mesurer |
| LIRE la fiche | python3 cerveau-projet/matrix/lancer.py inventaire-systeme lire |
| LIRE le resume seul | python3 cerveau-projet/matrix/lancer.py inventaire-systeme lire --resume |
| VERIFIER la fiche contre la machine | python3 cerveau-projet/matrix/lancer.py inventaire-systeme verifier |

Derniere mesure : 2026-09-20 18:54:18.
