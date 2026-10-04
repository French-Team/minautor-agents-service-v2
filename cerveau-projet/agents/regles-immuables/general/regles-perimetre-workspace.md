---
identite:
  type: regle
  appartient_a: commun
  commun: true
---
# Regle Immuable -- Perimetre du Workspace

> **Cette regle est IMMUABLE et PRIORITAIRE.** Elle s'applique a tout agent,
> tout outil et toute session. La sortie du workspace en ecriture est une
> **faute grave**.

---

## Le workspace

Le workspace est le dossier racine du projet : `Z:/analyste-in-console`
(racine du cerveau-projet). Tout ce qui est modifie vit **dans** ce dossier.

---

## Regle 1 -- Ecriture : workspace uniquement

**Il est interdit de creer, modifier ou supprimer un fichier hors du
workspace.** Cela inclut :

- Les fichiers temporaires (scripts, tests, captures, brouillons)
- Les fichiers de debug ou d'analyse ponctuelle
- Les fichiers de migration ou de transformation
- Tout autre fichier produit pendant une mission

Le workspace est la **seule zone d'ecriture**. Un fichier temporaire de test
ou de script se cree **dans** le workspace (ex: dossier `.tmp-test/` local)
puis se **supprime apres usage**. Il ne sort jamais du workspace.

## Regle 2 -- Lecture : autorisee hors workspace

La **lecture** d'un fichier hors du workspace reste autorisee (consultation
d'une reference, d'un exemple, d'un systeme distant). Mais meme en lecture,
l'agent ne doit **jamais ecrire** la ou il lit hors workspace.

## Regle 3 -- Chemins de sortie interdits

Les dossiers suivants sont **hors limites** pour toute ecriture :

| Zone | Statut |
|---|---|
| `C:/Users/*/AppData/Local/Temp/` (et tout `/tmp` systeme) | INTERDIT a l'ecriture |
| `Z:/tmp/`, `Z:/Temp/` | INTERDIT a l'ecriture |
| Tout chemin hors de la racine du workspace | INTERDIT a l'ecriture |
| Les zones systemes (Program Files, etc.) | INTERDIT |

Les outils qui produisent des rapports, des captures ou des fichiers de
travail doivent les placer dans le workspace (ex: un sous-dossier dedie) et
les nettoyer en fin de mission.

---

## Pourquoi ?

| Probleme | Solution |
|---|---|
| Fichiers temporaires eparpilles hors projet | Tout vit dans le workspace, rien ne se perd |
| Confusion entre le projet et le systeme | Une seule zone d'ecriture, claire |
| Nettoyage impossible a suivre | Le workspace est controle, le reste est propre |
| Risque d'ecrasement de fichiers systeme | Jamais d'ecriture hors workspace |

---

## Verification

Avant de creer ou modifier un fichier :

- [ ] Le chemin cible est dans le workspace (`Z:/analyste-in-console/...`)
- [ ] Aucun fichier temporaire n'est cree hors du workspace
- [ ] Les fichiers temporaires du workspace sont supprimes en fin de mission
- [ ] La sortie du workspace ne se fait qu'en lecture

---

## Liens

- [regles-general-global.md](regles-general-global.md) -- regles globales
- [regles-emojis-ascii.md](regles-emojis-ascii.md) -- ASCII strict
- [regles-veracite.md](regles-veracite.md) -- veracite

---

## Navigation

- **Parent** : [index-regles-general.md](index-regles-general.md)
- **Regles** : [index-regles-immuables.md](../index-regles-immuables.md)
