# Controle -- protocole-creation-combos (Buffy)

**Date** : 2026-08-08
**Controleur** : Janus (second controle)
**Objet** : protocole-creation-combos cree par Buffy (protocole + spec + todo) + conventions de creation des combos + corrections doc/spec moteur.

---

## Mission de controle

Verifier les points suivants :

1. Cycle complet present : pense-bete / spec / todo dans `protocole-creation-combos/`
2. Conventions figees : emplacement canonique (cerveau-projet/combos/ = definitions vs agents/tools/combos/ = outils), nommage combo-<action>, titres de cases, sorties cmdN/resultat_<action>, cibles par defaut, outils contextuels exclus, regles de decision (quand creer)
3. Doc moteur bumpee 0.1.1 + spec-combos-moteur corrigee (ambiguite emplacement)
4. Index-regles-general.md : ligne protocole-creation-combos ajoutee
5. ASCII 0 sur les 7 fichiers modifies/crees
6. Liens valides : protocole 6/6, spec 7/7, spec-combos-moteur 1/1
7. Lecon Buffy notee dans corrections.md

## Resultats

### Point 1 -- Cycle complet

OK. Les 3 fichiers du cycle sont presents dans
`pense-betes/regles-immuables/general/protocole-creation-combos/` :
- protocole-creation-combos.001.01.ebauche.md (pense-bete)
- spec/spec-protocole-creation-combos.001.01.ebauche.md (spec technique, 8 exigences EX-01 a EX-08)
- todo/todo-protocole-creation-combos.001.01.ebauche.md (taches 1-7 en cours, 8-10 futures)

### Point 2 -- Conventions

OK. Le protocole fige :
- Emplacement canonique : `cerveau-projet/combos/<combo-nom>/definition-combo.json` (definitions, Buffy) vs `agents/tools/combos/` (outils, Vulcain) -- distinction OUTIL/DEFINITION regle immuable
- Nommage : combo-<action> (dossier = champ nom), fichier TOUJOURS definition-combo.json, version 0.1.0, case_depart c1
- Titres de cases : Generer la commande X / Executer X / FIN - resume
- Sorties : cmd1.. / resultat_<action>
- Cibles par defaut : cerveau-projet/agents (validation) / cerveau-projet (audit)
- Outils contextuels EXCLUS du combo (indices de la case du parcours)
- Regles de decision : suite LINEAIRE repetee (>=2) ou longue (>=3) -> OUI ; arbre de decision / protections embarquees / suite specifique non repetee -> NON
- Processus en 11 etapes + checklist integration Pattern 3 + validation 7 points
La spec porte les 8 exigences fonctionnelles (EX-01 a EX-08) avec criteres d'acceptation.

### Point 3 -- Doc moteur + spec-combos-moteur

OK.
- combos-moteur.md : version bumpee 0.1.0 -> 0.1.1 (ligne versionning ajoutee), section Emplacement des combos corrigee avec la regle OUTIL/DEFINITION + reference au protocole (4 mentions)
- spec-combos-moteur : ligne Livrables corrigee (ancienne ambiguite `agents/<agent>/combos/definition-combo.json` OU `cerveau-projet/combos/` supprimee, 0 occurrence restante) + reference au protocole
- L'ambiguite d'emplacement documentee dans la mission est resolue.

### Point 4 -- Index-regles-general

OK. Ligne ajoutee dans la table Protocoles :
`| [protocole-creation-combos/](protocole-creation-combos/) | Creation et mise en place des combos (quand/ou/comment, Pattern 3) | ebauche |`

### Point 5 -- ASCII

OK. 0 caractere non-ASCII sur les 7 fichiers (protocole, spec, todo, index, doc moteur, spec-combos-moteur, corrections Buffy).

### Point 6 -- Liens

OK. Liens invalides : 0 sur les 4 fichiers a liens (protocole 6/6, spec 7/7, doc moteur 2/2, spec-combos-moteur 1/1). 5 liens relatifs faux ont ete corriges par Buffy (piege des niveaux de remontee).

### Point 7 -- Lecon Buffy

OK. Lecon `[NOTES] Protocole-creation-combos 2026-08-08` ajoutee dans corrections.md : 2 niveaux documentaires, distinction OUTIL/DEFINITION, conventions figees, regles de decision, PIEGE chemins relatifs (valider-liens --racine), PIEGE ASCII repetitif.

---

## Verdict

**VALIDE (7/7).** Le protocole-creation-combos est complet (cycle pense-bete/spec/todo), les conventions de creation des combos sont figees et coherentes avec les 6 combos existants, la doc et la spec moteur sont corrigees (ambiguite d'emplacement resolue), l'index est a jour, ASCII 0 et liens valides. Le processus documente (regles de decision + 11 etapes + checklist Pattern 3) rend les prochaines creations de combos reproductibles.
