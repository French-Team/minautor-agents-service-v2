---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# lire-head

**Version :** 0.1.1
**Statut :** ebauche
**Categorie :** lire
**Chemin :** `agents/tools/lire/lire-head/`
**Proprietaire :** Vulcain (constructeur d'outils)

## Description

Lire le **head** (en-tete) de un ou plusieurs fichiers **sans configurer le
nombre de lignes** : l'outil detecte automatiquement la fin du head et affiche
systematiquement TOUT son contenu, qu'il fasse 10 ou 50 lignes. Trois modes de
detection, dans l'ordre :

1. **Front-matter YAML** : si le fichier commence par `---`, le head va
   jusqu'a la ligne de fermeture `---` ou `...`
2. **Bloc de commentaires** : si le fichier commence par des commentaires
   (`#`, `//`, `;`, `*`, `--`, `%`), le head continue tant que les lignes
   sont des commentaires (une ligne vide est toleree si la suivante l'est
   encore)
3. **Premiere ligne vide** : sinon, le head = les lignes jusqu'a la premiere
   ligne vide (titre + description)

Borne de securite : `--max-lignes` (defaut 100) empeche de lire tout un
fichier geant si aucune fin de head n'est detectee.

L'outil accepte **plusieurs fichiers** et peut **comparer** leurs heads :
avec `--info-commune <motif>`, il cherche l'information commune dans chaque
head et affiche `PRESENT`/`ABSENT` par fichier -- celui qui est `ABSENT`
est probablement le fichier qui n'est pas a jour.

## Utilisation

```bash
# Lire le head d'un fichier (detection automatique de la fin)
lire-head.sh fichier.md

# Version Python (recommandee)
python3 lire-head.py fichier.md

# Lire les heads de plusieurs fichiers (comparaison visuelle)
lire-head.sh fichier1.md fichier2.md fichier3.md

# Verifier qu'une information commune est presente dans tous les heads
lire-head.sh fichier1.md fichier2.md fichier3.md --info-commune "version : 0.2.0"

# Forcer un nombre de lignes (derogation a la detection automatique)
lire-head.sh --lignes 15 fichier.md

# Simuler (decouverte, sans afficher le contenu)
lire-head.sh --dry-run fichier.md
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--info-commune <motif>` | Chercher un motif dans chaque head (PRESENT/ABSENT) | - |
| `--lignes <N>` | Forcer la lecture de N lignes (derogation) | auto |
| `--max-lignes <N>` | Borne de securite de la detection | 100 |
| `--verbose` | Afficher les details (mode de detection, lignes) | false |
| `--dry-run` | Simuler sans afficher le contenu | false |
| `--version` | Afficher la version | - |
| `--help` / `-h` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie que chaque fichier existe
2. Lit les lignes (decodage robuste UTF-8 puis latin-1, jamais de crash)
3. Detecte automatiquement la fin du head (front-matter / commentaires /
   premiere ligne vide) OU applique `--lignes N` si fourni
4. Affiche le head complet de chaque fichier (avec son chemin)
5. Si `--info-commune` : cherche le motif dans chaque head et affiche
   PRESENT (avec numeros de lignes) / ABSENT par fichier

## Exemples de sortie

```bash
$ lire-head.sh AGENTS.md --info-commune "Session :"

=== HEAD : AGENTS.md ===
---
identite:
  type: racine
  appartient_a: commun
  commun: true
---

=== COMPARAISON : information commune 'Session :' ===
  [PRESENT] AGENTS.md (lignes 26)
=> Tous les heads contiennent l'information.
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Lire l'en-tete d'un fichier sans connaitre sa taille | `lire-head.sh fichier.md` |
| Verifier que plusieurs fichiers ont le meme en-tete (meme info) | `lire-head.sh f1.md f2.md f3.md --info-commune "Version :"` |
| Reperer le fichier qui n'est pas a jour parmi plusieurs | `lire-head.sh f1.md f2.md f3.md --info-commune "statut: prepare"` |
| Lire le frontmatter de plusieurs fichiers d'un coup | `lire-head.sh f1.md f2.md` |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `lire-fichier` | Lire tout le contenu d'un fichier (avec options de plage) |
| `lire-frontmatter` | Extraire le frontmatter YAML seul (mode `--champ`) |
| `lire-lignes` | Lire des lignes specifiques par numero |
| `rechercher-texte` | Trouver les numeros de lignes d'un motif dans des fichiers |

## Notes de creation

- [x] L'outil a ete teste en reel (head simple, front-matter, comparaison)
- [ ] L'outil est conforme ASCII (aucun accent, aucun emoji)
- [ ] L'outil est reference dans `index-tools.md`
- [ ] L'outil est assigne a un agent dans sa carte de decision (protocole-outils Regle 6)
- [ ] Le statut est passe de `ebauche` a `prepare` apres validation RVAV

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-18 | Creation initiale (detection auto de la fin du head, comparaison multi-fichiers, --info-commune) |

---
