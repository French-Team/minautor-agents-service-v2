# detecter-convention-nommage

Garde-fou automatique ANTI-RECURRENCE (audit Themis 2026-08-11) : detecte les
mentions de la convention de nommage des ids de cases `c<numero>[a-z]?` **HORS
contexte etendu** `cT*` dans les fichiers du cerveau-projet.

| Champ | Valeur |
|---|---|
| **Version** | 0.1.0 |
| **Statut** | ebauche |
| **Categorie** | detecter |
| **Python** | detecter-convention-nommage.py |
| **Bash** | detecter-convention-nommage.sh (parite) |

---

## Description

La convention de nommage ETENDUE des ids de cases est
`c[<prefixe-alpha-maj>]<numero>[a-z]?` (valider-case v1.0.2, spec-guider-parcours
v0.6.2 regle 11) :
- cas normal : `c<numero>[a-z]?` (`c0`, `c12b`, `c29d`) ;
- prefixe thematique MAJUSCULE optionnel d'UNE lettre : `cT1`..`cT10`
  (T = ligne Trio de Janus, decision utilisateur 2026-08-11).

Une mention `c<numero>[a-z]?` est **CONFORME** si elle est dans une fenetre de
**+/- 2 lignes** contenant `c[<prefixe-alpha-maj>]` ou `cT1`..`cT10` (le cas
normal documente comme PARTIE de la convention etendue). Sinon elle est un
**ECART** : un fichier qui cite l'ancienne convention sans l'extension.

### Exclusions par defaut (`--tout` pour lever)
- **corrections.md** : les lecons historiques citent legitiment l'ancienne forme.
- **tests/** : les tests verifient les ids GENERES par les outils (jamais cT* a la
  generation) -- verification de comportement, pas documentation de convention.

---

## Utilisation

```bash
python3 detecter-convention-nommage.py --racine cerveau-projet
python3 detecter-convention-nommage.py --racine cerveau-projet --tout
python3 detecter-convention-nommage.py --racine <chemin> --rapport rapport.md
```

Options :
| Option | Role |
|---|---|
| `--racine <chemin>` | Racine du scan recursif (defaut : `cerveau-projet`) |
| `--tout` | Lever les exclusions (scanner aussi corrections.md et tests/) |
| `--rapport <fichier>` | Ecrire un rapport markdown au chemin fourni (jamais par defaut) |
| `--version` / `--aide` | Version / aide |

Verdict : **CONFORME** (code 0, aucune mention hors contexte) ou
**ECART(S) DETECTE(S)** (code 1, liste fichier:ligne).

---

## Lien avec le cerveau

- **Source de verite de la convention** : valider-case v1.0.2 (regex
  `^c[A-Z]?\d+[a-z]*$`) + spec-guider-parcours v0.6.2 regle 11.
- **Anti-recurrence** : lance ce scan apres toute modification d'un .md/spec
  mentionnant la convention, ou dans un audit de conformite (Themis / Janus).
