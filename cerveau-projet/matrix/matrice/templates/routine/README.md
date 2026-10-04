---
identite:
  type: readme
  appartient_a: matrice
  commun: true
  version: 1
  date: 2026-09-23
  liens: matrice/data/outils/dupliquer-template/DESCRIPTION.md, matrice/data/outils/ecrire/DESCRIPTION.md, matrice/data/manuel-outils.md
---

# MOULE -- routine (squelette de routine supervisee conforme)

> Le modele-mere est `routines/suivi-sync/` : insertion unique de `data/commun`
> (motif M-076), PID ecrit par le demon seul (MO-053), arret cooperatif vu en
> 2 s, etat court de passe borne (temoin de cadence lu par `verifier-cadence`),
> cadence declaree une seule fois.
> Ce dossier en est le MOULE a jetons : il ne s'execute JAMAIS seul -- il est
> consomme par l'outil `dupliquer-template`.
> Les trois pieces de squelette (`constants.py.moule`, `main.py.moule`,
> `boucle/entry.py.moule`) sont EXTRAITES du modele-mere par `fragment.py`
> (jamais retapees a la main) ; la passe et la fiche sont neuves, en jetons.

## Les jetons (remplaces a la generation)

| Jeton | Signification | Exemple |
|---|---|---|
| `__NOM_ROUTINE__` | nom du dossier routine (sous routines/) | veille-flux |
| `__CADENCE_SECONDES__` | cadence declaree, en secondes | 300 |
| `__ROLE_ROUTINE__` | ce que la routine fait, en une phrase | Surveille X et signale Y |

## Duplication (l'unique porte : dupliquer-template)

```
python3 cerveau-projet/matrix/lancer.py dupliquer-template generer --moule routine \
       --nom veille-xyz --role "Surveille X et signale Y" [--cadence 300]
```

Le generateur : lit ce moule (JAMAIS une routine vivante), construit les sources
du clone EN MEMOIRE, verifie chaque fichier AVANT d'ecrire (py_compile + ASCII
strict + aucun jeton residuel), verifie le clone executable (`python main.py
--once` : une passe et sortie, sans PID), et n'ecrit sur disque QUE si tout est
vert.

## INVARIANT -- ce que le moule porte, et qu'une routine ne peut pas oublier

1. l'insertion de `data/commun` dans `sys.path`, avec garde (RuntimeError si le
   module partage est introuvable -- jamais un import silencieux) ;
2. le PID, ecrit par le demon SEUL (un `--once` n'est pas un demon : MO-053) ;
3. l'arret cooperatif : drapeau vu en 2 s (attente decoupee, pas d'attente nue) ;
4. l'ETAT court de la passe, borne par le moteur partage `battement.py` ;
5. la cadence DECLAREE AU PLANNING (`routines/vie/planning.json`, decision du
   createur D1/MO-429 : cadence ET mode `passe`/`boucle` -- les constantes ne
   portent que le RENVOI `INTERVALLE_DECLARE_SECONDES =
   cadence_planning('<nom>')`), plus son nom canonique lu par `vie etat` ;
6. la CASE DES PRODUCTIONS (`PRODUCTIONS = ()`, vide a la naissance) : les
   fichiers que la routine ECRIT et qui ne sont PAS des sources, ni ses etats
   courts de forme conventionnelle (un rapport, un inventaire, la memoire d'une
   passe). Un fichier dont le NOM echappe a la convention se declare ici : c'est
   le SEUL endroit ou le controle peut l'apprendre (mesure du 2026-09-23 :
   `veille-flux/alertes-emises.json`, un etat anti-spam anterieur a la convention,
   juge comme une source). Une production DECLAREE est hors
   du jugement du controle d'attribution (`controle-attribution.py`) ; une
   production NON declaree y est ACCUSEE a chaque passe, comme une ecriture hors
   de sa porte (friction du 2026-09-23 : `rapport-liens.json`, reecrit a chaque
   passe, a ete accuse des sa premiere reecriture -- et l'accusation serait
   revenue sans fin). Le controle CONSOMME la declaration : il ne recopie aucun
   nom (M-076).

## VARIABLE -- ce qui se remplit apres generation

- `passe/fonctions.passer()` : le travail (le squelette rend 0 et le DIT) ;
- `DESCRIPTION.md` : le role reel, les fichiers d'etat, les preuves ;
- l'ENTREE au PLANNING (`routines/vie/planning.json`) : cadence, mode
  (`passe` s eleve par le service, `boucle` par le serveur), decalage initial,
  priorite et commande de passe -- sans elle, la routine n'est jamais allumee
  et sa cadence se lit `ILLISIBLE` (MO-429) ;
- la declaration dans la liste des routines du serveur (`routines/vie/constants.py`) :
  une routine non declaree n'est jamais lancee.

6. le MARQUEUR DE PROVENANCE (`provenance.json`) : c est LUI qui ouvre la porte
   ECRIRE dans cette routine -- le garde refuse toute ecriture dans une routine
   qui n en porte pas, et NOMME les deux remedes (generer, ou se declarer
   anterieure avec un motif).

## Apres generation (obligatoire, dans cet ordre)

1. remplir `passe/fonctions.passer()` ;
2. inscrire l'entree au PLANNING (`routines/vie/planning.json`, MO-429) ;
3. declarer la routine dans `routines/vie/constants.py` ;
4. prouver : `python3 cerveau-projet/matrix/matrice/routines/<nom>/main.py --once` (une passe, aucun PID), puis un cycle
   (boucle supervisee ou passe servie par le service) + arret cooperatif, puis l'entree du temoin de cadence ;
5. reposer la fiche du manuel si la routine ajoute une porte.
