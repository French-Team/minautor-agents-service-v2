---
identite:
  type: rapport-controle
  appartient_a: janus
  commun: false
---
# Controle croise -- Round 3 Securite

**Date :** 2026-08-12
**Controleur :** Janus (controle croise, dernier maillon)
**Chaine :** Cerberus -> Vulcain -> Morpheus -> Janus -> Cerberus
**Objet :** renforcement securite de 9 outils fichiers/edition (encodages, symlinks, chemins non surs)

---

## Verdict : VALIDE (J1-J7 verts)

## Verifications

### J1 -- Versions py/sh/md coherentes : OK (10/10)

| Outil | Version attendue | Resultat |
|---|---|---|
| lire-fichier (py/sh/md) | 0.4.1 | OK |
| editer-fichier (py/sh/md) | 0.4.1 | OK |
| ecrire-fichier, creer-fichier, deplacer-fichier | 0.3.1 | OK |
| remplacer-texte (sh) | 0.3.1 | OK |

### J2 -- Crashs d'encodage reelement elimines : OK (5/5)

Re-mesure reelle (pas seulement le rapport) : BOM UTF-8, latin-1, octets invalides
sur lire-fichier, editer-fichier sur BOM et latin-1 -> plus AUCUN traceback,
tous exit 0. Le BOM est nettoye (pas de U+FEFF dans la sortie).

### J3 -- Octet nul refuse : OK (3/3)

lire-fichier, editer-fichier, supprimer-fichier : chemin contenant \x00 ->
exit 1 avec message propre "[ERREUR] Chemin non sur (octet nul present)",
aucun traceback.

### J4 -- Non-regression : OK (26/26)

Deux passages : le premier a revele 1 KO (test-024 scripts-temporaires) car le
controleur lui-meme avait laisse 2 fichiers .tmp-janus-* a la racine. Apres
nettoyage : 26/26 OK. **Le garde-fou test-024 a detecte nos propres scripts
temporaires : preuve reelle de fonctionnement en conditions reelles.**

### J5 -- Normes ASCII/LF : OK (0/0)

28 fichiers (9 py + 9 sh + 9 md + spec remplacer-texte) : 0 non-ASCII, 0 CRLF.

### J6 -- Catalogue : OK

regenerer-catalogue --dry-run : 0 cle dupliquee, 0 a ajouter (aucun nouvel outil,
aucun changement de reference).

### J7 -- Lecons documentees : OK

- vulcain/corrections.md : "ROUND 3 SECURITE"
- morpheus/corrections.md : "APRES ROUND 3 SECURITE"

---

## Details des corrections (Vulcain)

1. **stdout force en UTF-8** (sys.stdout.reconfigure, protege par try) : fin des
   UnicodeEncodeError cp1252 sous Windows.
2. **Lecture robuste** : utf-8-sig (BOM nettoye) puis fallback latin-1 dans
   lire/editer/inserer/supprimer-ligne/remplacer.
3. **Refus octet nul** : tout chemin contenant \x00 -> exit 1 explicite (9 outils).
4. **Refus symlink** sur les outils d'ecriture (ecrire, editer, creer, deplacer
   source+dest, inserer, supprimer-ligne) ; remplacer-texte ignore les liens ;
   lire et supprimer peuvent traverser (lecture seule / os.remove ne touche que
   le lien).
5. **Backup binaire** (shutil.copy2) dans ecrire-fichier : une copie texte
   corrompait les fichiers latin-1.

## Lecons du controle

1. Le controle re-mesure, il ne relit pas : J2 a re-cree les fichiers BOM/latin-1
   au lieu de croire le rapport de Vulcain.
2. Le garde-fou test-024 fonctionne : il a attrape les scripts temporaires du
   controleur lui-meme -- la non-regression est un filet qui ne distingue pas
   l'auteur de l'erreur.
3. Les outils d'ecriture securises (symlink + octet nul) protegent aussi les
   futurs tests de la non-regression.
