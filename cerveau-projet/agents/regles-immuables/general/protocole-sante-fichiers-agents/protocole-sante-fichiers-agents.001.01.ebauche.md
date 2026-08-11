---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole de Sante des Fichiers Agents

**Version** : 0.1.2
**Statut** : Ebauche
**Date creation** : 2026-08-10
**Agent** : Janus (controleur des statuts)
**Historique** : v0.1.2 (renforcement E5d : le bloc FINS REELLES devient OBLIGATOIRE sur CHAQUE fiche avec croisement bidirectionnel fiche/parcours - lecon de l'audit Themis du 2026-08-11 : le trio athena/minerve/promethee n'avait aucun bloc alors que les 8 autres agents l'avaient) -> v0.1.1 (E5b croisement Pattern 13, lecon re-audit 2026-08-10) -> v0.1.0 (creation, 2026-08-10)

---

## Objectif

Definir comment Janus verifie REGULIEREMENT l etat des fichiers des agents du
cerveau-projet (fiches .md, parcours .json, corrections.md), pour detecter la
derive silencieuse : a mesure que le cerveau-projet evolue (patterns, protocoles,
migrations, versions), les fichiers des agents sont souvent negliges et ne
refletent plus l etat reel.

**Pourquoi ce protocole ?**
- L utilisateur a constate que les fichiers des agents sont negliges a mesure
  que l on ameliore le cerveau-projet : les fiches ne sont pas systematiquement
  alignees sur les parcours (versions, regles, outils)
- Etat des lieux initial (2026-08-10) : 6 parcours sur 11 sont encore en v0.2.0
  (athena, atlas, clio, minerve, morpheus, promethee) pendant que 5 sont migres
  (buffy v0.3.3, cerberus v0.3.1, janus v0.3.1, themis v0.3.0, vulcain v0.3.0)
- Ce protocole rend le controle PERIODIQUE de l etat des fichiers agents
  automatique et contractuel : Janus le lance regulierement et rapporte ce qui
  ne va pas

---

## Prerequis

| # | Condition | Detail |
|---|---|---|
| 1 | Activation par Cerberus ou branche du parcours-janus | Je ne m active jamais moi-meme (independance du controle) |
| 2 | Relecture de ma fiche et de mes corrections | Garde-fou relecture avant de commencer |
| 3 | Le protocole est reference dans ma fiche | janus.md section protocoles + index-regles-general |
| 4 | Outils disponibles | lister-fichiers, valider-conformite-ascii, valider-liens, evaluer-coherence, valider-cartes-decision, detecter-divergences-version |

---

## Etapes

```
INVENTAIRE -> COHERENCE FICHE/PARCOURS -> FORMAT -> NORMES
    1                2                      3        4
-> REGLES A JOUR -> RAPPORT -> VERDICT
       5              6          7
```

| Etape | Action | Detail | Outils |
|---|---|---|---|
| E1 | Inventaire des 11 agents | Lister les 3 fichiers de chaque agent : fiche `<agent>.md`, parcours `parcours-<agent>.json`, `corrections.md`. Verifier leur existence | lister-fichiers, glob |
| E2 | Coherence fiche/parcours | La fiche reference-t-elle la BONNE version du parcours ? La section PARCOURS de la fiche est a jour ? Detecter les fiches qui disent v0.2.0 pendant que le parcours est v0.3.x, ou l inverse (fiche a jour mais parcours migre non reference) | lecture, detecter-divergences-version, valider-cartes-decision |
| E3 | Format des fiches | Frontmatter present (identite) + sections standard (identite, role, parcours, regles, outils, limites) | lecture |
| E4 | Normes | ASCII strict, LF pur, liens internes valides (toutes formes : markdown + backticks) sur fiche + parcours + corrections | valider-conformite-ascii, valider-liens, evaluer-coherence |
| E5 | Regles a jour | Les REGLES ABSOLUES des fiches refletent-elles les patterns actuels de la spec-guider-parcours ? Pattern 13 verifie par CROISEMENT fiche/parcours (sous-criteres E5a/E5b/E5c/E5d : la fiche formule la fin-suit-SA-carte, cite les fins REELLES via leurs identifiants cX ET porte le bloc FINS REELLES obligatoire sur CHAQUE fiche, croise en bidirectionnel avec le parcours) et Pattern 14 (version du parcours presente dans la fiche) | lecture, spec-guider-parcours, parcours-<agent>.json |
| E6 | Rapport | Synthese par agent : A JOUR / A METTRE A JOUR / A MIGRER + verdict global. Rapport depose dans janus/controles/ | - |
| E7 | Verdict | VALIDE (tout A JOUR) / A REVOIR (des fichiers a mettre a jour ou migrer) / REJETE | - |

---

### Detail E5 : verifier le Pattern 13 par croisement fiche/parcours

> Le Pattern 13 (la fin suit SA carte) se verifie en CROISANT la fiche avec la
> carte reelle de l'agent, pas seulement par une mention textuelle (lecon du
> re-audit du 2026-08-10 : la fiche morpheus contenait le concept sans le
> formuler ; la correction a du citer les fins reelles c10/c14).

> **E5a (mention textuelle)** : la fiche formule explicitement "la fin suit SA carte" (Pattern 13), pas seulement le concept.
> **E5b (croisement fiche/parcours -- LEVER DE LA LECON DU RE-AUDIT)** : pour CHAQUE fin citee dans la fiche (retour a X, activer Y, reactiver Z), verifier que l identifiant cX correspond a une case de type `fin` dans `parcours-<agent>.json` et que le titre de la case (ex : "FIN - Activer Janus") correspond au sens declare. Une mention textuelle sans identifiant reel est INSUFFISANTE.
> **E5c (conformite du sens)** : la fin declaree correspond a la fin reelle : activation directe par Cerberus -> reactiver Cerberus ; maillon d'une chaine -> activer le suivant (ex : c10 FIN - Activer Janus, retour Vulcain) ; seul le DERNIER maillon reactiver Cerberus.
> **E5d (bloc FINS REELLES OBLIGATOIRE sur CHAQUE fiche -- LEVER DE LA LECON THEMIS 2026-08-11)** : le bloc `FINS REELLES DE MA CARTE vX` doit etre PRESENT sur CHAQUE fiche d'agent (les 11), pas seulement sur celles qui en ont deja un (l'audit Themis a revele que le trio athena/minerve/promethee n'avait aucun bloc alors que les 8 autres agents l'avaient). Verification en CROISEMENT BIDIRECTIONNEL avec `parcours-<agent>.json` :
>   (1) la version du bloc (`vX` apres "FINS REELLES DE MA CARTE") == version reelle du parcours ;
>   (2) CHAQUE case de type `fin` du parcours est citee dans le bloc (aucune fin reelle absente) ;
>   (3) CHAQUE fin citee dans le bloc existe dans le parcours et est de type `fin` (aucune fin fantome) ;
>   (4) le titre declare (ex : "FIN - Activer Janus") correspond au titre reel de la case.
>   Attention aux IDs a prefixe thematique MAJUSCULE : la regex de scan doit etre `[a-zA-Z]*[0-9]+[a-z]*` (ex : `cT6`..`cT10` de la ligne trio Janus) -- une regex `[a-z]?` cree des faux negatifs.

---

## RVAV

| Lettre | Action | Detail |
|---|---|---|
| [R]elete | Relire ma fiche et mes corrections | Avant tout controle |
| [V]erifier | Appliquer E1 a E6 : checklist de sante complete | Tous les agents |
| [A]gir | Corriger les ecarts OU rapporter a l agent habilite | Fiches -> Buffy ; parcours v0.2.0 -> migration ; tests -> Morpheus |
| [V]alider | Verdict + rapport | E7 |

---

## Exemples

### Exemple 1 : etat des lieux initial (2026-08-10)

  E1 : inventaire -> 11 fiches + 11 parcours + 11 corrections presents
  E2 : coherence -> 6 fiches/pour 6 parcours v0.2.0 non migres ; 5 fiches alignees
       sur des parcours migres (buffy v0.3.3, cerberus v0.3.1, janus v0.3.1,
       themis v0.3.0, vulcain v0.3.0)
  E3 : format -> frontmatter present sur les 11 fiches
  E4 : normes -> ASCII 0, LF pur, liens valides
  E5 : regles -> certaines fiches portent encore l ancienne philosophie
       (reactiver Cerberus) sans la condition Pattern 13
  E6 : rapport -> synthese par agent A JOUR / A METTRE A JOUR / A MIGRER
  E7 : verdict -> A REVOIR (migrations de parcours en attente)

---

## Notes

- Le protocole est PERIODIQUE : Janus le lance regulierement (sur demande ou via
  sa carte), pas seulement apres une mission specifique.
- Les corrections sont deleguees : fiches -> Buffy (responsable du cerveau-projet),
  parcours v0.2.0 -> migration (Vulcain/Buffy), tests -> Morpheus.
- Ne pas modifier les fichiers des agents directement pendant l etat des lieux :
  le rapport est la base des missions suivantes.
