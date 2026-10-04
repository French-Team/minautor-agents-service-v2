---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole de Controle du Travail de Buffy

**Version** : 0.1.0
**Statut** : Ebauche
**Date creation** : 2026-08-10
**Agent** : Janus (controleur croise)

---

## Objectif

Definir comment Janus effectue le second controle (controle croise) du travail de
Buffy, developpeur principal des fichiers du cerveau-projet (protocoles,
conventions, fiches, lecons, index, parcours JSON, liens).

**Pourquoi ce protocole ?**
- Janus etait calibre pour le controle des OUTILS de Vulcain (combo-controle-outil)
- Le travail de Buffy est DOCUMENTAIRE : il n y a pas de code a tester, mais des
  documents a verifier (liens, format, conventions, coherence, lecons)
- Les controles croises du travail de Buffy existaient deja en pratique (15 liens
  corriges, garde-fou format des lecons, migration des parcours) mais avec des
  scripts ad hoc, sans protocole durable
- Ce protocole capitalise les lecons de ces controles passes

---

## Prerequis

| # | Condition | Detail |
|---|---|---|
| 1 | Mission de Buffy terminee | Les fichiers ont ete modifies et sa lecon est ajoutee dans corrections.md |
| 2 | Activation par Cerberus | Je ne m active jamais moi-meme (independance du controle) |
| 3 | Relecture de ma fiche et de mes corrections | Garde-fou relecture avant de commencer |
| 4 | Contexte de la mission | Je connais la mission confiee a Buffy pour recouper les fichiers touches |
| 5 | Etat git de reference | Le recoupement git status est l outil principal d identification |

---

## Etapes

```
MISSION DE BUFFY -> IDENTIFIER LES FICHIERS -> INTEGRITE -> DOCUMENTAIRE
      1                   2                    3           4
-> LE CONS -> CONVENTIONS -> PARCOURS/FICHES -> VERDICT -> RAPPORT
    5            6               7             8         9
```

| Etape | Action | Detail | Outils |
|---|---|---|---|
| E1 | Identifier les fichiers modifies | Recouper la mission de Buffy avec git status : seuls les fichiers attendus sont modifies | git status, lister-fichiers |
| E2 | PREUVE D INTEGRITE | git status VIDE sur les fichiers NON concernes par la mission - preuve plus fiable qu un contenu attendu | git status |
| E3 | Verification documentaire | ASCII strict + LF pur + tableaux valides + liens internes sur TOUS les fichiers modifies | valider-conformite-ascii, valider-tableaux, valider-liens, evaluer-coherence |
| E4 | TOUTES les formes de liens | Verifier les liens markdown (texte entre crochets suivi d une cible entre parentheses) ET les chemins entre backticks : un chemin entre backticks n est pas detecte par les validateurs mais reste un faux-fuyant a corriger | valider-liens, evaluer-coherence, lecture |
| E5 | PIEGE markdown dans les lecons | Un exemple de syntaxe de lien ecrit litteralement DANS une lecon est interprete par evaluer-coherence comme un VRAI lien casse - les backticks INLINE ne protegent pas, seuls les blocs fenced | evaluer-coherence, lecture |
| E6 | Format des lecons | Les lecons de Buffy suivent le format [LECON] conforme au garde-fou (protocole-auto-correction, corrections-template) | lecture, valider-conformite-ascii |
| E7 | Conventions respectees | convention-protocoles (en-tete + 7 sections), convention-structures, convention-renommage | lecture, verifier-separation-preoccupations |
| E8 | Separation + surcharge | Les fichiers modifies respectent la separation des preoccupations et ne sont pas en surcharge | verifier-separation-preoccupations, detecter-surcharge-fichier |
| E9 | Parcours et fiches | Validite JSON des parcours modifies, cartes de decision valides, Pattern 14 (version du parcours presente dans la fiche), pas de divergence de version spec/py | valider-cartes-decision --tous, detecter-divergences-version |
| E10 | Verdict + rapport | Verdict VALIDE / A REVOIR / REJETE, rapport documente dans janus/controles/ | - |

---

## RVAV

| Etape RVAV | Action pour ce protocole |
|---|---|
| [R]echercher | Lister les fichiers modifies par Buffy et les fichiers de reference (git status) |
| [V]erifier | Appliquer E1 a E9 : la checklist documentaire complete |
| [A]nalyser | Distinguer les VRAIS ecarts des faux positifs (fichiers d exemples de doc, citations sans version) |
| [V]alider | Donner le verdict (VALIDE / A REVOIR / REJETE) et documenter le rapport |

> **REGLE ABSOLUE** : Je ne donne JAMAIS de verdict sans avoir verifie la boucle
> RVAV complete. Je ne CORRIGE pas, je SIGNALE.

---

## Exemples

### Exemple 1 : correction de liens (mission 15 liens casses)

```
Mission : Buffy corrige 15 liens casses (observation Themis)
Controle Janus :
  E1 : git status -> 10 fichiers modifies (attendus)
  E2 : git status sur valider-liens.md, corriger-liens.md, convention-liens.md
       -> VIDE (preuve d integrite : les fichiers d exemples n ont pas ete touches)
  E4 : lecture -> decouverte d un chemin entre backticks inexact (ligne 271 de
       fiche-agent-template.md) invisible pour les validateurs -> signale
  E5 : evaluer-coherence -> detection d un motif parasite dans la lecon Janus
       elle-meme (exemple de syntaxe de lien litteral) -> reformule en description
  E10 : VERDICT VALIDE (10/10)
```

### Exemple 2 : creation de protocole (mission garde-fou format des lecons)

```
Mission : Buffy ajoute un garde-fou dans protocole-auto-correction et
          corrections-template
Controle Janus :
  E5 : verifier que le garde-fou LUI-MEME ne produit pas le motif qu il interdit
       (regex sur les 2 fichiers modifies) -> OK
  E3 : evaluer-coherence global -> 0 lien casse (le garde-fou ne casse rien)
  E10 : VERDICT VALIDE (11/11)
```

---

## Pieges courants

| Piege | Consequence | Parade |
|---|---|---|
| **Fichiers d exemples de doc** | valider-liens.md, corriger-liens.md, convention-liens.md utilisent des cibles FICTIVES (fichier1.md, ancien.md, chemin/fichier.md) : un controle generique les signalerait a tort | Verifier LEUR motif caracteristique, pas un motif generique ; git status vide = intacts |
| **Chemins entre backticks** | Invisibles pour evaluer-coherence et valider-liens, mais inexacts = faux-fuyant de coherence | Les verifier par lecture systematique, pas seulement par outils |
| **Exemple de syntaxe de lien dans une lecon** | Un exemple litteral (texte entre crochets suivi d une cible entre parentheses) est lu comme un VRAI lien par evaluer-coherence | Decrire la syntaxe en toutes lettres ou utiliser un bloc fenced - jamais en litteral inline |
| **Citations sans version** | detecter-impacts signale des fichiers qui CITENT l outil sans version (lecons historiques, rapports dates, fiches) : faux positifs | Verifier si la mention porte une version a mettre a jour : non = pas un impact |
| **Correction au lieu de signalement** | Je ne suis pas habilite a corriger | Je documente uniquement les problemes, Buffy ou l agent habilite corrige |

---

## Liens

| Reference | Usage |
|---|---|
| [convention-protocoles](../../../conventions/protocoles/convention-protocoles.md) | Structure des protocoles (en-tete + 7 sections) |
| [protocole-auto-correction](../protocole-auto-correction/) | Format des lecons + garde-fou [LECON] |
| [corrections-template](../../../corrections-template.md) | Template des lecons + garde-fou |
| [protocole-controle-statuts](../protocole-controle-statuts/) | Protocole historique de Janus (statuts) |
| [protocole-audit-buffy](../protocole-audit-buffy/) | Protocole de Themis (audit de conformite du travail de Buffy) |
| [rvav-workflow](../rvav-workflow.md) | Boucle obligatoire avant verdict |
| [combo-controle-modification](../../../tools/combos/combo-controle-modification/) | Suite de validation d une modification |
| [combo-controle-outil](../../../tools/combos/combo-controle-outil/) | Suite de validation d un outil |
| [regles-validation-rigoureuse](../regles-validation-rigoureuse.md) | Validation rigoureuse |
