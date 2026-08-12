---
identite:
  type: rapport-controle
  appartient_a: janus
  commun: false
---
# Controle croise -- Round 4 Robustesse

**Date :** 2026-08-12
**Controleur :** Janus (controle croise, dernier maillon)
**Chaine :** Cerberus -> Vulcain -> Morpheus -> Janus -> Cerberus
**Objet :** correction des echecs silencieux (messages d'erreur, dry-run, cas limites)

---

## Verdict : VALIDE (J1-J7 verts)

## Verifications

### J1 -- Versions py/sh/md coherentes : OK (9/9 apres correction)

lire-fichier 0.4.2 (py/sh/md), ecrire-fichier 0.3.2 (py/sh/md), supprimer-ligne
0.3.2 (py/sh/md).

**Ecart trouve et corrige en cours de controle** : ecrire-fichier.sh etait reste
en 0.3.1 (le corps avait ete corrige mais pas la version). Corrige en 0.3.2,
bash -n OK, normes OK. Le controle croise a rempli son role : verifier que la
REGLE DES 5 FICHIERS est respectee.

### J2 -- Les 3 corrections reelement en place : OK (4/4)

Re-mesure reelle (pas seulement le rapport) :
- ecrire vide -> fichier tronque a zero octet + message INFO (exit 0)
- lire --debut 5 --fin 2 -> exit 1 "[ERREUR] Plage invalide : --debut (5) > --fin (2)"
- supprimer-ligne ligne inexistante sur fichier 1 ligne -> "n'a que 1 ligne"
- lire plage valide (--debut 2 --fin 2) -> toujours OK (sortie "2")

### J3 -- Dry-run toujours non destructif : OK (2/2)

ecrire --dry-run et supprimer-ligne --dry-run : contenu inchange (exit 0).

### J4 -- Non-regression : OK (26/26)

Aucun test ne verifiait --lignes 0 (desormais exit 1) ni le comportement
contenu vide : les changements silencieux -> explicites sont compatibles.

### J5 -- Normes ASCII/LF : OK (0/0)

11 fichiers (3 py + 3 sh + 3 md + corrections Vulcain + corrections Morpheus).

### J6 -- Catalogue : OK

regenerer-catalogue --dry-run : 0 cle dupliquee, 0 a ajouter.

### J7 -- Lecons documentees : OK

- vulcain/corrections.md : "ROUND 4 ROBUSTESSE"
- morpheus/corrections.md : "APRES ROUND 4 ROBUSTESSE"

---

## Details des corrections (Vulcain)

1. **ecrire-fichier v0.3.2** : contenu vide = troncature explicite a zero octet
   + message INFO (parite py/sh : open "w" vs ": > fichier"). Plus de no-op
   silencieux : un agent peut desormais vider un fichier et savoir ce qui
   s'est passe.
2. **lire-fichier v0.4.2** : validation de plage AVANT lecture (--debut > --fin,
   ou borne < 1 pour --debut/--fin/--lignes) -> erreur explicite exit 1.
   Fin du 0 silencieux avec sortie vide.
3. **supprimer-ligne v0.3.2** : pluriel correct ("1 ligne" vs "N lignes").

## Lecons du controle

1. LA REGLE DES 5 FICHIERS EST VERIFIEE PAR LE CONTROLE, PAS PAR LA CONFIANCE :
   l'ecart ecrire-fichier.sh (0.3.1 vs 0.3.2) n'a ete vu par aucun test mais a
   ete attrape par J1 - la parite py/sh/md doit etre controlee a chaque round.
2. LE CONTROLE RE-MESURE, IL NE RELIT PAS : J2 a re-cree les cas limites
   (fichier vide, plage inverse, fichier 1 ligne) au lieu de croire le rapport.
3. LE 0 SILENCIEUX EST L'ENNEMI DE L'AGENT : les 3 corrections transforment des
   comportements muets en comportements explicites - c'est le sens meme de la
   robustesse pour un agent autonome.
