# verifier-coherence-agents

**Version :** 0.1.0
**Statut :** prepare
**Categorie :** verifier
**Chemin :** `agents/tools/verifier/verifier-coherence-agents/`

## Description

Verifie la coherence des blocs session d AGENTS.md (fichier racine commun)
contre les fichiers reels du projet, pour detecter au demarrage les ecarts
qui polluent les sessions LLM (themes perimes dans le bloc DEMARRAGE V2,
fiches/corrections introuvables, raisons tronquees, agents vides dans
jarvis-data.json, table Sessions connues desynchronisee).

Cree suite a l audit ferrari 2026-08-25 (rapport-audit-agents-md-2026-08-25.md) :
AGENTS.md est ecrit par DEUX ecrivains non synchronises (activer-agent-principal
cote v1, jarvis maj_bloc_session cote v2), ce qui a produit plusieurs ecarts
(themes JARVIS/LIRE/EXPLORER versus arbre a 1 theme, raison tronquee a 80
caracteres, corrections jarvis vide, themes orphelins). Cet outil est le
mecanisme de validation automatique cote v1.

## Utilisation

```bash
# Verifier la coherence (lecture seule)
python3 verifier-coherence-agents.py --confirme-doc

# Avec details sur les arbres analyses
python3 verifier-coherence-agents.py --confirme-doc --verbose

# Depuis un autre repertoire / avec un AGENTS.md specifique
python3 verifier-coherence-agents.py --confirme-doc --agents-md /chemin/AGENTS.md

# En dry-run (decouverte, sans confirmation doc requise)
python3 verifier-coherence-agents.py --dry-run

# Rendre le code de sortie non-nul si incoherences (pour CI)
python3 verifier-coherence-agents.py --confirme-doc --seuil 1
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--dry-run` | Simuler sans rien modifier | false |
| `--verbose` | Afficher les details (arbres analyses) | false |
| `--version` | Afficher la version | - |
| `--doc` | Afficher le .md complet et sortir | false |
| `--confirme-doc` | Confirmer la lecture de la documentation | false |
| `--agents-md` | Chemin vers AGENTS.md | racine projet |
| `--seuil` | Code de sortie si incoherences | 1 |

## Ce que l'outil verifie

1. **Fiches + corrections des blocs session** : chaque bloc (session-admin,
   session-freelance) doit referencer des fichiers existants sur disque.
2. **Coherence des arbres v2** : pour chaque bloc freelance, le texte
   `(themes : ...)` du bloc DEMARRAGE V2 ne doit jamais lister plus de themes
   que l arbre-<agent>.json n en reference (racine.suivant).
3. **Raisons non tronquees** : une raison de bloc ne doit pas se terminer par
   un mot inacheve (symptome d une troncature a 80 caracteres).
4. **jarvis-data.json** : chaque agent doit avoir fiche + corrections non vides
   et existantes.
5. **Table Sessions connues** : chaque session du tableau doit avoir un bloc
   correspondant et une derniere activite non vide.

## Exemples de sortie

```bash
$ python3 verifier-coherence-agents.py --confirme-doc
=== verifier-coherence-agents v0.1.0 ===
Racine projet : /chemin/analyste-in-console
AGENTS.md     : /chemin/analyste-in-console/AGENTS.md
Blocs session : 2
=== RESULTAT : 0 incoherence -- AGENTS.md COHERENT ===

$ python3 verifier-coherence-agents.py --confirme-doc --seuil 1
=== verifier-coherence-agents v0.1.0 ===
Racine projet : /chemin/analyste-in-console
AGENTS.md     : /chemin/analyste-in-console/AGENTS.md
Blocs session : 2
=== INCOHERENCES (1) ===
  1. [bloc session-freelance DEMARRAGE V2 pos=-] theme(s) non references :
     theme-explorer.json (arbre ne reference que {'theme-jarvis.json'})
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Au demarrage d une session LLM | Verifier que le bloc LU par le LLM est coherent |
| Apres tout changement d arbre v2 ou de blocs session | Controler la resynchronisation |
| En CI / non-regression | Detecter les incoherences (--seuil) |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `verifier-conformite-fiche` | Verifie la structure d UNE fiche d agent |
| `detecter-decalages-catalogue` | Detecte les decalages de versions/catalogue |
| `evaluer-processus` | Evalue la conformite des parcours/regles |

## Notes de creation

- [x] L'outil est en lecture seule (aucune ecriture) : les messages
      informationnels sont informatifs.
- [x] Bloc DOC OBLIGATOIRE embarque (verifier_doc_presente + exiger_confirmation_doc + --doc + --confirme-doc).
- [x] Teste en --dry-run puis en reel (--confirme-doc).
- [x] Conforme ASCII (valide avec valider-conformite-ascii).
- [ ] Reference dans `index-tools.md` (a faire via generateurs-regenerer-catalogue).
- [ ] Assignee a un agent dans sa carte de decision.
- [ ] Test dedie dans le dossier tester/ (Morpheus).