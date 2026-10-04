---
identite:
  type: outil
  appartient_a: matrice
  commun: true
  version: 1
  date: 2026-10-03
  statut: a-jour
  liens: matrice/data/outils/registre-outils/DESCRIPTION.md, _operateur/optimus-prime/super-combos/combos/outils/garde-ascii.py
---

# benchmark -- la mise a l epreuve d un fichier

> Mesure du 2026-10-03 : cet outil n avait **aucune** `DESCRIPTION.md`, alors
> qu il est au registre et qu il sert. Le lanceur le disait a chaque appel --
> `[SANS CARTE] benchmark : carte absente` -- et personne ne l avait lu comme
> un manque de documentation plutot que comme un bruit d affichage. La carte
> est posee ici.

## Porte unique

`benchmark` met un fichier (ou un dossier) a l epreuve **avant** qu une mission
ne se termine. Toute mission qui touche un fichier passe benchmark.

## Les neuf epreuves

| Epreuve | Ce qu elle interroge |
|---|---|
| perimetre | le fichier est-il dans le perimetre d ecriture autorise ? |
| lf | les fins de ligne sont-elles bien LF ? |
| sha | l empreinte correspond-elle a ce qui est attendu ? |
| validation | le fichier se charge-t-il (JSON, Python) ? |
| ascii | reste-t-il un caractere hors de la carte ASCII ? |
| bdd | la modification est-elle tracee dans la BDD ? |
| relecture | le fichier a-t-il ete relu apres ecriture ? |
| bak | y a-t-il un point de restauration exploitable ? |
| invisibilite | la zone est-elle bien hors jugement ou dedans ? (MO-487) |

## Verbes

| Verbe | Usage |
|---|---|
| `benchmark --fichier <chemin>` | met un fichier a l epreuve |
| `benchmark --dossier <chemin> [--recursif] [--filtre *.py]` | met un dossier a l epreuve |
| `benchmark --integration` | l integration complete du projet |

## Codes retour

| code | signification |
|---|---|
| 0 | tout passe |
| 1 | au moins une epreuve echoue |
| 2 | refus de perimetre |

## Ce que cet outil ne fait pas

Il ne repare rien : il **constate**. La reparation passe par sa porte, et son
verdict ne dispense d'aucune trace.
