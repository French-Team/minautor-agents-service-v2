# Controle -- Generalisation du jeu de piste (Buffy) 2026-08-07

**Objet controle** : demarrer.md (CASE 0 du jeu) + protocole-carte-decision.001.01.ebauche.md (v0.2.0, evolution parcours)
**Mission controlee** : generaliser le concept PARCOURS (jeu de piste) dans demarrer.md et le protocole-carte-decision
**Agent auteur** : Buffy (developpeur principal -- fichiers du cerveau)
**Date du controle** : 2026-08-07

---

## Mission de controle

Verifier independamment (je ne fais pas confiance) :

| # | Point a verifier | Methode |
|---|---|---|
| 1 | demarrer.md : section CASE 0 du jeu de piste ajoutee (apres l'identification) | inspection |
| 2 | demarrer.md : workflow (section 7) mis a jour -- chaque agent lance SON parcours apres identification | inspection |
| 3 | demarrer.md : section 6 renommee Parcours (jeu de piste), pas de casse des sections existantes | inspection |
| 4 | demarrer.md : fichiers cles (section 7) avec parcours JSON + guider-parcours | inspection |
| 5 | protocole-carte-decision : v0.2.0, section EVOLUTION en tete, carte SUPERSEDEE par parcours | inspection |
| 6 | protocole : 5 modeles de cases documentes (question, indice-outil, indice-fichier, regle, controle) + format JSON | inspection |
| 7 | protocole : historique conserve (sections originales intactes, marqueur IMMUABLE mis a jour) | inspection |
| 8 | Coherence : les commandes guider-parcours references sont les bons chemins (agents/tools/guider/guider-parcours/) | inspection |
| 9 | Conformite ASCII des 2 fichiers modifies | valider-conformite-ascii |
| 10 | Aucune trace d'outil externe | detecter-usage-outils-externes |

---

## Verdict

- **Verdict** : CONFORME (10/10 apres correction)
- **Points valides** : 10/10
- **Problemes detectes** :
  1. **PT9 ASCII NON CONFORME (corrige)** : `demarrer.md` ligne 13 contenait 2
     caracteres non-ASCII (guillemets francais doubles introduits par la mission).
     -> CORRIGE par Buffy : remplaces par des guillemets ASCII ("...").
     -> RECONTROLE le 2026-08-07 : valider-conformite-ascii = 0 non-conforme.
- **Historique** : premier controle NON CONFORME (9/10) -> correction Buffy ->
  recontrole du point 9 -> CONFORME (10/10). Le cycle controle-correction-recontrole
  fonctionne comme prevu.

---

## Lecons

1. Le controle ASCII doit verifier CHAQUE fichier separement : l'outil
   valider-conformite-ascii ne prend qu'un fichier par appel (mon premier appel
   ne validait que le protocole, pas demarrer.md).
2. detecter-usage-outils-externes est plus strict que valider-conformite-ascii
   et a signale le probleme en premier -- toujours croiser les deux outils.
3. Les caracteres typographiques francais (guillemets doubles) sont des pieges :
   ils passent dans une phrase en apparence anodine et cassent la regle ASCII.
   MEME J'AI COMMIS CETTE ERREUR EN REDIGEANT CE RAPPORT (corrige).
4. La mission Buffy est globalement conforme (9/10) : CASE 0, workflow parcours,
   section 6 Parcours, fichiers cles, protocole v0.2.0 avec EVOLUTION en tete,
   historique conserve, spec de reference correcte, traces externes 0 (protocole).
5. Suite du cycle : Cerberus doit reactiver Buffy pour corriger la ligne 13 de
   demarrer.md (2 guillemets non-ASCII), puis Janus recontrole rapidement le point 9.
6. PRE-EXISTANTS hors perimetre (non commites, de controles Janus anterieurs,
   non corriges ici) : corrections.md ligne 238 (un mot avec accent) et
   ligne 252 (guillemets doubles non-ASCII) -- a traiter dans un nettoyage ulterieur.
