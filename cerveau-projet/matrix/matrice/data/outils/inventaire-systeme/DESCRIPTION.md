# OUTIL -- inventaire-systeme

> La **FICHE MACHINE** (MO-251) : ce que la Matrice sait de la machine sur laquelle
> elle vit -- OS, architecture, hote, session, CAPACITES (CPU, RAM, disque, charge,
> GPU), RESEAU et OUTILS installes -- et la **PORTE** qui la tient a jour.
>
> Modele : la **v1** (`cerveau-projet/agents/tools/verifier/verifier-systeme`,
> v0.2.3-py). La mesure est la MEME ; ce qui est ajoute : la carte d identite, la
> section **RESUME MACHINE** servie a l injection, et la porte de verification.

## Pourquoi un fichier, et pas seulement une injection

L injection est un EVENEMENT : elle ne survit pas au redemarrage, et une mission
qui ne recoit rien ne peut pas demander ce qu elle ignore. La fiche est un ETAT
DURABLE : elle se relit hors mission, elle se verifie contre la machine, et
l injection en sert la seule section COURTE. Deux usages, une seule mesure.

## Une seule maison (EO-154)

La fiche vit dans `matrice/data/systeme-machine.md`, a cote des autres fiches de la
Matrice (`manuel-outils.md`, `data-readme.md`). Un seul ecrivain : cette porte.
L injection ne RECOPIE rien : elle LIT la section `RESUME MACHINE` de ce fichier
(l entree `contexte-machine` du catalogue `avant-mission`), et `verifier` exige que
ce contrat soit declare -- une relation ecrite dans un commentaire ne se
desynchronise pas tout de suite : elle se desynchronise en silence.

## Ce que la porte N EST PAS

Ce n est ni un benchmark de performance, ni un installateur : elle MESURE et elle
ECRIT une fiche. Aucune installation, aucune modification du systeme (la v1 disait
la meme chose : non-intrusif, lecture seule).

## Portes

```
python3 cerveau-projet/matrix/lancer.py inventaire-systeme mesurer
python3 cerveau-projet/matrix/lancer.py inventaire-systeme lire [--resume]
python3 cerveau-projet/matrix/lancer.py inventaire-systeme verifier
```

| Verbe | Ce qu il fait | Code |
|---|---|---|
| `mesurer` | Mesure la machine, COMPOSE la fiche et l ECRIT (atomique, LF forces) | 0 |
| `lire` | La fiche entiere ; `--resume` ne sert que la section de l injection | 0, ou 2 si la fiche ou la section manque |
| `verifier` | La fiche contre une mesure FRAICHE, et l entree d injection declaree | 0 sain, 1 ecart nomme, 2 fiche absente |

## Ce que `verifier` mesure (quatre controles)

1. **carte d identite** en tete de la fiche (le type `fiche` du vocabulaire ferme) ;
2. **section RESUME MACHINE** presente, et ses CASES (`CASES_RESUME`) -- sans elle,
   l entree d injection ferait un refus nomme a la source suivante ;
3. **champs COMPARES** (OS, architecture, hote, versions de python3, node, git)
   contre une mesure fraiche : c est la PREUVE que la fiche a pouri, ou qu elle tient ;
4. **catalogue d injection** : l entree `contexte-machine` declaree dans
   `avant-mission`, pointant CE fichier, demandant CETTE section.

## Protections

- **Un fait non mesure est un fait qui ment (L-055)** : une mesure impossible est DITE
  `-`, jamais `0` -- `0` serait un fait, et il serait faux.
- **Aucun shell** : les commandes systeme sont des LISTES d arguments ; un script
  Windows (`.cmd`, `.bat`) est lance par `cmd /c`, un `.ps1` par `powershell`
  (mesure du 2026-09-20 : `npm.CMD` rendait `Version inconnue` sans ce relais).
- **Ecriture ATOMIQUE** (tmp + remplacement, LF forces) : un lecteur ne voit jamais
  une fiche a moitie ecrite.
- **Dependance DOUCE** : `psutil` s il est present, sinon RAM et charge restent NON
  MESUREES ; le GPU est cherche au REGISTRE (nom + VRAM APPARIES), puis par `wmic`,
  `powershell` et `lspci` (le nom seul), et son silence est un `-`, jamais une
  absence de materiel inventee.
- **La VRAM vient du REGISTRE, pas d AdapterRAM** : `AdapterRAM` (wmic/powershell) est
  un DWORD SIGNE plafonne a 4 Go -- une carte de 12 Go y rendrait 4095 Mo, un faux fait
  plus trompeur qu une absence (L-055). La cle de classe des cartes graphiques porte
  `HardwareInformation.qwMemorySize`, une valeur 64 BITS posee par le pilote : mesure du
  2026-09-20, **12272 Mo** la ou `AdapterRAM` plafonne. Un adaptateur sans memoire
  lisible rend `-`, et un chemin de registre s ecrit par `SEPARATEUR = chr(92)` jamais
  par un antislash litteral (un antislash traverse le shell et se deforme, MO-286).
- **Le remede est NOMME** : un ecart de fiche se repare par `mesurer`, un ecart de
  catalogue par l entree `avant-mission` -- les deux sont dits separement.

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| DESCRIPTION.md | la facade (ce fichier) |
| main.py | point d entree global : DIRIGE (mesurer / lire / verifier) |
| constants.py | domicile de la fiche, carte d identite, table des sondes, champs compares |
| mesure.py | la MESURE : systeme, ressources, reseau, outils |
| fiche.py | la FICHE : composer, ecrire, lire, extraire une section |
| verif.py | les QUATRE controles de `verifier` |
