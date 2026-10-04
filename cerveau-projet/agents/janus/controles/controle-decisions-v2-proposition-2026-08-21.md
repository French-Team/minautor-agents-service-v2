# Controle - Redaction des decisions v2 (proposition-v2.md)

**Agent controleur** : Janus
**Mission controlee** : Redaction des decisions utilisateur v2 (mode discussion + redaction)
**Fichiers concernes** : cerveau-projet/freelance/proposition-v2.md (+ rapports et lecons)
**Date** : 2026-08-21

---

## VERDICT : VALIDE

Non-regression complete : **97/97 OK (0 KO)**, rating test **98.9 EXCELLENT**.
Aucun defaut signale.

---

## 1. Contenu de la mission (CONFORME)

Les 4 decisions utilisateur sont capturees dans proposition-v2.md :

| Decision | Localisation | Verifie |
|---|---|---|
| D1 - Carte -> Arbre des decisions (systeme veineux) | Section 0 + section 4 | branche (theme) -> categories -> cases d'execution -> cases suivantes -> case de fin ; pas de depart unique ni de fin unique |
| D2 - Outils dynamiques + non-regression SEPAREE | Section 0 + section 6bis | Suite freelance independante de la suite actuelle (objectifs et contrats differents) |
| D3 - Activation + sauts de cases AUTOMATISES (transparent) | Section 0 + section 5 | Actions recurrentes de la v1 deviennent transparentes pour l'agent |
| D4 - Standard UTF-8 + CRLF + emojis | Section 0 + P9 (ligne 82) | Abandon ASCII + LF + bannir emojis ; standard actuel |

## 2. Corrections de la boucle KO (CONFORME)

Les 2 ecarts signales par Themis sont corriges :
- ECART 1 (annexe ligne 268) : "Regles immuables (ASCII, LF, veracite) | Conserves (P9)"
  -> "Regles immuables (veracite) | Conservees ; ASCII/LF REMPLACES par UTF-8 + CRLF + emojis (D4)"
- ECART 2 (ligne 43 liste a conserver) : mention "marbre, ASCII, LF, veracite"
  -> "marbre, veracite - avec abandon du standard ASCII/LF au profit de UTF-8 + CRLF + emojis (D4)"
- 0 mention incoherente restante (grep "ASCII, LF" / "Conserves (P9)" vide)

## 3. Validations

| Verification | Resultat |
|---|---|
| Non-regression complete | **97/97 OK (0 KO)** |
| Rating test | **98.9/100 EXCELLENT** |
| Marbre (--tous) | exit 0, 0 divergence |
| evaluer-processus global | 0 probleme |
| ASCII/LF proposition-v2.md | 0 non-ASCII, 0 CRLF |
| ASCII/LF fichiers touches (rapport Themis, corrections buffy/themis, AGENTS.md, AGENTS-historique) | 0/0 partout |
| Structure sections | 12 sections (0, 1, 2, 3, 4, 5, 6, 6bis, 7, 8, 9, Annexe) |
| Coherence encart/corps AGENTS-historique | 10/10 (aucune heure encart absente du corps) |
| Audit Themis | A REVOIR (2 ecarts) -> CORRIGES par Buffy, re-verifies ici |

## 4. Note sur la commande reactiver (reparation immediate)

Themis a lance une commande `reactiver` avec le mauvais outil (la fin c25b
utilise `activer`, pas `reactiver`), creant une entree parasite
(Cerberus 21:09) dans AGENTS-historique.md. Reparation immediate :
entree supprimee de l'encart ET du corps (grep 21:09 = 0), Buffy activee
correctement avec `activer`, la chaine a continue normalement. Lecon deja
documentee (controle precedent : apres une erreur d'activation, verifier
encart ET corps, supprimer les parasites, reactiver correctement).

## 5. Conclusion

La mission de redaction est VALIDE : les 4 decisions utilisateur sont
fidelement capturees, les 2 ecarts de la boucle KO sont corriges, la
non-regression est verte (97/97), tous les fichiers sont ASCII/LF purs.
La chaine est bouclee : Cerberus est reactive avec le bilan consolide.
