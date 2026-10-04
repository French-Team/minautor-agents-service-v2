---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# executer-formulaire

**Categorie** : Executer
**Version** : 0.1.0
**Statut** : prepare
**Date creation** : 2026-09-02
**Proprietaire** : Vulcain (outil partage, decision D6/D7 2026-08-21)

---

## Objectif

Appliquer la decision utilisateur **D6/D7 - OUTIL = FORMULAIRE** : l agent ne
compose plus jamais la syntaxe de commande. Il lance l outil, l outil lui
fournit le **formulaire** (mini-description + liste des champs/flags depuis le
catalogue `generateurs-commande`), l agent ecrit ses reponses dans un
**fichier JSON** (via `creer-fichier` -- jamais de ligne bash geante), l outil
**valide** (requis, types - un formulaire invalide n est JAMAIS execute) puis
**compose et execute** la commande a la place de l agent.

**Pourquoi cet outil ?**
- Le heredoc bash cedait pour les longues instructions (contenus tronques,
  quoting casse - vecu dans les rounds). Le fichier de reponses JSON supprime
  la limite : l agent ecrit son JSON avec `creer-fichier`, l outil le lit.
- Les outils simples (creer/ecrire/editer/ajouter/inserer-fichier) ont recu
  le mode fichier (`--contenu-chemin`, `--remplacements-chemin`, `--fichier
  SOURCE`) : executer-formulaire s appuie sur ces modes.

---

## Utilisation

```bash
# Version Python (recommandee)
python3 executer-formulaire.py --outil <nom> --schema
python3 executer-formulaire.py --outil <nom> --reponses <fichier.json>

# Version bash equivalente (wrapper)
bash executer-formulaire.sh --outil <nom> --schema
bash executer-formulaire.sh --outil <nom> --reponses <fichier.json>
```

**Arguments :**
| Argument | Description |
|---|---|
| `--outil <nom>` | Outil du catalogue a executer (ex: creer-fichier) |
| `--schema` | Afficher le formulaire : description + champs (cle, type, requis, flag, defaut) + exemple de fichier de reponses |
| `--reponses <fichier>` | Fichier JSON des reponses (ANTI-HEREDOC : jamais d argument bash geant) |
| `--dry-run` | Composer la commande sans l executer |
| `--version` | Afficher la version |
| `--aide, -h` | Afficher l aide |

**Exit code :**
| Code | Signification |
|---|---|
| `0` | Execution reussie (ou schema/dry-run/version) |
| `1` | Formulaire INVALIDE (refus avant execution), reponses illisibles, execution en erreur |
| `2` | --outil manquant/inconnu, catalogue introuvable, --reponses manquant |

---

## Le flux complet (l agent ne compose plus)

1. **L agent lance le formulaire** :
   `executer-formulaire.py --outil creer-fichier --schema`
   -> l outil affiche : description, champs (fichier REQUIS, contenu REQUIS,
   forcer [flag=--forcer]), exemple de fichier de reponses.

2. **L agent ecrit ses reponses avec creer-fichier** (jamais de ligne bash
   geante, meme pour des contenus longs) :
   ```json
   { "fichier": "rapport.md", "contenu": "<contenu long sur plusieurs lignes>", "forcer": false }
   ```

3. **L outil valide puis execute** :
   `executer-formulaire.py --outil creer-fichier --reponses reponses.json`
   - V A L I D A T I O N : champ requis manquant -> refus AVANT execution avec
     message clair (quels champs, pourquoi) - jamais de commande partielle.
   - COMPOSITION : la commande est composee depuis le modele du catalogue.
   - EXECUTION : automatique, a la place de l agent (D6).

---

## Les champs du formulaire (D7)

| Propriete | Role | Detail |
|---|---|---|
| `cle` | Identifie le champ | La cle du JSON de reponses |
| `type` | Contraint la valeur | texte / nombre / boolean (flag) |
| `obligatoire` | Requis ? | true = refus si absent |
| `flag` | Option a passer | ex: `--forcer` pour un champ boolean |
| `defaut` | Valeur pre-remplie | Optionnel |

Source des champs : le catalogue `generateurs-commande/catalogue-commandes.json`
(source de verite des parametres de chaque outil).

---

## Anti-heredoc : les outils simples compatibles

| Outil | Option anti-heredoc |
|---|---|
| `creer-fichier` | `--contenu-chemin <fichier>` (v0.3.3) |
| `ecrire-fichier` | `--contenu-chemin <fichier>` (v0.3.3) |
| `editer-fichier` | `--remplacements-chemin <json>` (v0.5.1) |
| `ajouter-contenu-fichier` | `--fichier SOURCE` (deja present) |
| `inserer-contenu-fichier` | `--fichier SOURCE` (deja present) |

Tous lisent le contenu depuis un fichier : jamais de contenu long dans une
ligne de commande. Modele a suivre pour les futurs outils.

---

## Integration

- **Le pilote (mission-ajouter)** : quand une mission mentionne un outil du
  catalogue, il peut injecter le bloc `[OUTIL]` (mini-description + liste des
  flags) pour que l agent sache quoi utiliser et pourquoi, sans lire le code.
- **Tous les agents** utilisent `--schema` comme point d entree memoire :
  au lieu de se demander "comment fonctionne l outil ?", ils affichent le
  formulaire (description + flags) puis renseignent le JSON.

---

## Notes

- Le catalogue est la source de verite des commandes : si un outil manque,
  l ajouter a `catalogue-commandes.json` d abord.
- Un formulaire invalide n est JAMAIS execute : refus avant execution (D7).
- Jouable en `--dry-run` avant execution reelle (verifier la commande composee).

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-09-02 | Creation initiale : formulaire D6/D7 (--schema : description + champs/flags depuis le catalogue, --reponses : fichier JSON anti-heredoc, validation requise avant execution, composition depuis le modele, execution automatique), wrapper .sh parite. |