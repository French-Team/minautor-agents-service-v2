---
identite:
  type: outil
  appartient_a: commun
  commun: true
# Outil -- detecter-donnees-en-dur
---

# detecter-donnees-en-dur

**Version :** 0.1.1
**Statut :** ebauche
**Categorie :** detecter

## Pourquoi cet outil ?

Les **donnees en dur** sont des valeurs ecrites directement dans le code ou les
documents qui deviennent **fausses quand le projet evolue** : un nombre de
fichiers, un seuil de taille, un chemin de dossier, une version, un delai, une
URL. Elles provoquent des **bugs caches** : rien ne casse a l'ecriture, mais le
comportement devient obsolete sans que personne ne le voie.

La regle d'or : **ne JAMAIS coder en dur une valeur qui peut changer**. Quand un
doute est emis, l'agent doit se demander :

1. La valeur est-elle locale a ce fichier ? -> **constante nommee en haut du
   fichier** (convention MAJUSCULES, ex: `SEUIL_ALERTE = 30`).
2. La valeur est-elle partagee entre plusieurs fichiers ou change souvent ? ->
   **fichier de configuration JSON**.
3. S agit-il d une collection / liste ? -> **tableau ou liste dans un autre
   fichier** (JSON/CSV).
4. S agit-il d un SECRET (cle API, mot de passe, token) ? -> **variable
   d environnement (.env)** lue au demarrage - JAMAIS dans le code ni le git.
5. S agit-il d une valeur purement documentaire ? -> **documentation (.md)**.

Cet outil aide l agent a POSER LA QUESTION qui emet le doute : il detecte les
valeurs en dur probables et recommande le meilleur format de stockage.

## Detections

| Type | Description | Exemple |
|---|---|---|
| `NOMBRES_MAGIQUES` | Constante numerique dans une comparaison sans nom | `if taille > 2048:` |
| `COMPTEURS_SEUILS` | Affectation d un nom parametrable a un nombre | `timeout = 30` |
| `CHEMINS_EN_DUR` | Chemin de fichier/dossier ecrit en dur dans le code | `dossier = "cerveau-projet/agents"` |
| `URLS_EN_DUR` | URL / endpoint ecrit en dur | `url = "https://api.exemple.com/v2"` |
| `VERSIONS_EN_DUR` | Version repetee dans un message ou la doc | `"module v0.7.3 en cours"` |
| `SECRETS_EN_DUR` (v0.1.1) | Secret (cle API, mot de passe, token) affecte a un nom evoquant un secret | `API_KEY = "sk-..."` |

### Exclusions legitimes

- Les valeurs banales `0`, `1`, `-1`, `100` (index, booleens, pourcentage) ;
- Les dates (`2026-08-09`, `09/08/2026`) ;
- Les valeurs de test (fixtures) et les exemples de documentation ;
- Les fichiers `.md` et `.json` de parcours/configuration : leurs chemins et
  commandes sont DOCUMENTAIRES (liens relatifs, commandes `python3 ...`) ;
- Les commentaires (`#`, `//`) : pas une valeur active ;
- Les lectures d environnement (`os.environ.get`, `os.getenv`) : legitimes ;
- Les placeholders (`xxx`, `exemple`, `demo`, `TODO`, `changeme`) : pas un
  vrai secret.

## Usage

```bash
# Analyser un fichier
python3 detecter-donnees-en-dur.py chemin/fichier.py

# Analyser un dossier (recursif)
python3 detecter-donnees-en-dur.py chemin/dossier/

# Plusieurs chemins
python3 detecter-donnees-en-dur.py fichier1.py dossier2/

# Tout le projet (scan complet depuis la racine via AGENTS.md)
python3 detecter-donnees-en-dur.py --tous

# Avec rapport markdown et detail
python3 detecter-donnees-en-dur.py --tous --rapport rapport.md --verbose

# Version
python3 detecter-donnees-en-dur.py --version
```

## Options

| Option | Description |
|---|---|
| `chemins...` | Fichiers ou dossiers a analyser (un ou plusieurs) |
| `--tous` | Scan complet du projet (fichiers .py/.sh/.md/.json du cerveau) |
| `--rapport <fichier>` | Ecrit le rapport markdown (LF pur, ASCII) |
| `--verbose` | Detail des fichiers et des recommandations |
| `--version` | Affiche la version |

## Sortie

Pour chaque fichier douteux, la liste des doutes classes par type avec le
numero de ligne et la valeur. Chaque doute est accompagne d une
**recommandation de format de stockage** (constante nommee, JSON de
configuration, liste dediee).

Verdict final : `OK` si aucun doute, `SIGNAL - N doutes` sinon (code retour 1).

## Exemple de sortie

```
=== RESULTAT detecter-donnees-en-dur v0.1.1 ===
Fichiers analyses : 874 | fichiers avec doutes : 250 | total doutes : 954
Doutes par type :
  CHEMINS_EN_DUR     : 408
  COMPTEURS_SEUILS   : 108
  NOMBRES_MAGIQUES   : 283
  URLS_EN_DUR        : 2
  VERSIONS_EN_DUR    : 153

=== chemin/fichier.py (2 doutes) ===
  [COMPTEURS_SEUILS] ligne 6 : 2048
      -> Constante NOMMEE en haut du fichier (ex: SEUIL_ALERTE = 2048,
         MAJUSCULES). Si partagee : JSON de configuration.
  [CHEMINS_EN_DUR] ligne 9 : cerveau-projet/agents/traces
      -> Variable de chemin en haut du fichier ou JSON de configuration.

VERDICT : SIGNAL - 954 doutes de donnees en dur a examiner.
```

## Notes

- L outil est un **signal**, pas un jugement : il met en doute, l agent decide.
- Ne pas traiter le scan complet comme une dette urgente : les doutes du projet
  existant sont examines au fil des missions (un doute par mission suffit).
- L outil n est assigne a AUCUNE carte d agent pour l instant (decision
  utilisateur en attente).
