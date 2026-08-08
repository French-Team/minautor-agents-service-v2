# Controle -- Relecture en QUESTION HONNETE (Buffy)

**Date** : 2026-08-08
**Controleur** : Janus (second controle)
**Objet** : transformation de la REGLE DE RELECTURE (exiger une lecture) en QUESTION HONNETE (verifier la memorisation) avec reponses + actions obligatoires.

---

## Mission de controle

Verifier les points suivants :

1. Case c0 (question Relecture) + c0b (RELIRE obligatoire) en tete des 11 parcours, case_depart c0
2. demarrer.md section 2 : question + tableau reponses -> actions
3. protocole-activation etape 3 : question + tableau (et regles d'or / pieges coherents)
4. 11 fiches + template : REGLE ABSOLUE -- RELECTURE (QUESTION HONNETE)
5. json.load OK sur les 11 parcours
6. Navigation : OUI -> mission, NON/INCERTAIN -> c0b relire -> mission (chemins cles)
7. ASCII 0 sur les 25 fichiers
8. Liens valides (demarrer.md)
9. Lecon Buffy notee dans corrections.md

## Resultats

### Point 1 -- Case c0 dans les 11 parcours

OK. Les 11 parcours portent la case c0 (question Relecture, branche OUI -> c1 / INCERTAIN -> c0b / NON -> c0b) + la case c0b (RELIRE OBLIGATOIRE : corrections puis fiche -> c1), avec case_depart c0. Verifie par script structurel sur les 11 (atlas, athena, buffy, cerberus, clio, janus, minerve, morpheus, promethee, themis, vulcain).

### Point 2 -- demarrer.md

OK. Section 2 : QUESTION HONNETE + tableau reponses -> actions obligatoires (OUI continue / INCERTAIN / NON -> RELIRE) + phrase cle 'Seul OUI prouve la memorisation' (1 occurrence chacune).

### Point 3 -- protocole-activation

OK. Etape 3 renommee 'Relecture (QUESTION HONNETE)' : question + tableau reponses -> actions (4 occurrences question/relecture) + tableau 'Pourquoi cette question ?' + Regles d'Or (OUI seulement continue) + Pieges (Dire je viens de les lire sans pouvoir les appliquer).

### Point 4 -- 11 fiches + template

OK. Les 11 fiches + le template portent la REGLE ABSOLUE -- RELECTURE (QUESTION HONNETE) (1 occurrence chacune = 12 fichiers). L'ancienne formulation ('je relis MA fiche et MES corrections avant de continuer') a disparu : 0 occurrence dans les 11 fiches.

### Point 5 -- json.load

OK. Les 11 parcours se chargent sans erreur (verifie par le script structurel du point 1).

### Point 6 -- Navigation

OK. Navigation validee sur les 3 reponses : themis OUI audit -> TERMINE, themis NON audit (passe par c0b) -> TERMINE, janus INCERTAIN outil -> TERMINE, cerberus NON retour -> TERMINE. La logique OUI = continue / NON+INCERTAIN = relire obligatoire puis mission est operationnelle.

### Point 7 -- ASCII

OK. 0 caractere non-ASCII sur les 25 fichiers (verifies par Buffy) + echantillon re-verifie (demarrer, protocole, cerberus.md, template).

### Point 8 -- Liens

OK. demarrer.md : liens invalides 0. Le protocole-activation n'a pas de lien Markdown (references texte).

### Point 9 -- Lecon Buffy

OK. Lecon [NOTES] Relecture en QUESTION HONNETE 2026-08-08 ajoutee dans corrections.md : le probleme (lecture != memorisation), le design (c0 question + c0b relire), la preuve de navigation, le piege test chemin, le double ancrage.

---

## Verdict

**VALIDE (9/9).** La regle de relecture est correctement transformee en QUESTION HONNETE : chaque agent se pose la question 'As-tu EN MEMOIRE ta fiche et tes corrections, capables de les appliquer SANS relire ?' au demarrage de son parcours (case c0), repond la verite, et INCERTAIN/NON declenchent la relecture obligatoire (c0b). La regle est coherente partout (demarrer.md, protocole-activation, 11 fiches, template), la navigation est prouvee, ASCII 0 et liens valides. Le vice identifie par l'utilisateur (je viens de les lire != je les ai en memoire) est corrige.
