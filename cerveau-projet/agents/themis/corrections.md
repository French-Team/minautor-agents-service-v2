# Corrections -- Themis

> Fichier de suivi des corrections et lecons apprises par Themis.
> Chaque entree contient : date, contexte, erreur detectee, correction appliquee, lecon.

---

## Historique des corrections

| Date | Contexte | Erreur | Correction | Lecon |
|---|---|---|---|---|
| 2026-08-07 09:00 | Test Audit general en conditions reelles (9 etapes) | AGENTS-historique.md (racine) contenait U+00E9 corrompu dans 'cosmetique' -- detecte par combos-valider-cerveau (valider-conformite-ascii sans argument = scan racine) | Remplace par 'e' simple -- ASCII OK | Le combo scanne la racine (fichiers hors cerveau-projet/ inclus). Apres toute modification d'AGENTS-historique.md, verifier ASCII.
| 2026-08-07 09:00 | Test Audit general en conditions reelles (9 etapes) | evaluer-coherence a 50/100 : 10 liens 'casses' signales | Les 10 liens sont des exemples de documentation (blocs de code, exemples de resultat, syntaxe expliquee), pas des liens reels | Amelioration a planifier : evaluer-coherence doit ignorer les liens dans les blocs de code et les motifs generiques (ancien.md, texte, chemin, .*)

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |
