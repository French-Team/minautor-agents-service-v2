---
type: rapport-controle
appartient_a: janus
date: 2026-08-12
---

# Controle croise -- Round 5 COMBOS (2026-08-12)

**Controleur** : Janus (session-llm-1)
**Agent controle** : Vulcain (combos-moteur v0.3.2) + validation Morpheus
**Theme** : enchainements d outils fluides et sans friction

## Contexte

Le diagnostic reel de Cerberus a revele une faille critique du combos-moteur v0.3.1 :
le code retour des cases `outil` n etait JAMAIS verifie. Une case qui echouait
(exit != 0) laissait le moteur continuer jusqu a la case fin avec code retour 0 :
un agent lancant un combo croyait que tout avait reussi alors qu une etape avait
echoue (echec silencieux au niveau de l orchestration).

## Corrections de Vulcain

1. **combos-moteur v0.3.2** (py + sh, parite) : verification du returncode des
   cases outil -> arret immediat si echec (exit != 0) avec message clair
   (La commande de la case 'cX' a echoue (code N)).
2. **Champ optionnel `echec_ok: true`** : pour les cases dont le code non-nul est
   un resultat legitime (validateurs/detecteurs : valider-*, detecter-*).
3. **30 cases outil de controle marquees echec_ok** dans les 10 combos declaratifs
   de controle.
4. Doc combos-moteur.md mise a jour (section robustesse + version 0.3.2).

## Verifications (J1-J7)

| # | Verification | Resultat |
|---|---|---|
| J1 | Versions py/sh/md = 0.3.2 | OK |
| J2 | Arret sur echec reel (definition temporaire, exit 3) : rc=1 + message, pas de FIN | OK |
| J2b | echec_ok:true -> le combo continue jusqu a la FIN (rc=0) | OK |
| J3 | Parite .sh : meme arret sur echec | OK |
| J4 | Non-regression complete : 26/26 OK | OK |
| J5 | Normes ASCII/LF : 0 ecart sur 17 fichiers | OK |
| J6 | Catalogue : 0 a ajouter + 0 doublon | OK |
| J7 | Lecons Vulcain + Morpheus presentes | OK |

## Verdict

**VALIDE** -- J1-J7 tous verts. La propagation silencieuse des echecs dans les
combos est eliminee. L option echec_ok preserve l usage legitime des validateurs.

## Lecons Janus

1. RE-MESURER, NE PAS RELIRE : J2 a re-cree les deux scenarios (arret sur echec,
   echec_ok continue) avec des definitions temporaires reelles - le comportement
   est prouve, pas suppose.
2. LE FORMAT DES DEFINITIONS EST UN CONTRAT : ma premiere definition de test a
   ete refusee (cle 'combo' manquante, puis 'sortie' manquante sur la case outil) -
   le moteur valide le contrat strictement, ce qui est une bonne chose pour la
   robustesse des combos.
3. LE GARDE-FOU TEST-024 RESPECTE : scripts temporaires ranges dans .janus-r5/
   (jamais a la racine), supprimes en fin de mission, aucun residu.
