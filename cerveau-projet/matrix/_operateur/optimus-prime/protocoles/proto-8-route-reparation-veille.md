---
identite:
  type: protocole
  appartient_a: optimus-prime
  commun: false
---

# PROTOCOLE 8 -- ROUTE REPARATION VEILLE (de l'alerte au retour vert)

> Source : preuves M-047/M-048 (boucle securite prouvee de bout en bout) +
> M-052 (predicat bugue : lecon L-012 zombie) + L-013 (chemins). Cette route
> est celle de l'agent qui RECOIT une mission bloquante deposee par la veille.

## La route (6 etapes)

1. **Reconnaitre l'alerte** : mission au vrac (theme `reparer <cible>`,
   urgence bloquante, source veille) + message alerte-grave dans la boite
   Matrice (etat exact : detection, fichier, signature anti-spam).
2. **Reproduire AVANT de reparer** : relancer la detection cible a la main
   (passe veille, py_compile du fichier) et confirmer le meme ecart. Une
   detection non reproduite est soit reparee, soit un faux positif a
   documenter -- dans les deux cas on ne "repare" pas a l'aveugle.
3. **Diagnostiquer a la racine** (proto-3) : lire le fichier casse EN ENTIER,
   chercher la CAUSE (syntaxe ? import ? chemin ? code zombie -- process
   vivant qui garde son ancien code ?). Chercher dans le code AVANT de creer.
4. **Reparer a la source, un changement minimum** : pas de rustine autour du
   symptome. Tests reels : positif (le cas reussit) ET negatif (le garde
   refuse toujours le cas invalide).
5. **Retour vert** : passe veille manuelle 0 detection + py_compile + note
   BDD modifications (action corrige) + fin avec la preuve.
6. **Si le perimetre depasse la mission** (marbre, protocoles, boucles
   vivantes, gardes du pilote) : ne PAS improviser -- signaler vers
   optimus-prime (mission au vrac / boite Matrice) et finir honnetement.

## Interdits

- Supprimer le fichier casse pour "faire taire" l'alerte (l'anti-spam purge
  seul les signatures mortes -- purger a la main est un ecart).
- Redemarrer une boucle sans le motif d'arret cooperatif (lecon L-012 :
  drapeau + activer, jamais de processus tue).
- "Reparer" deux fichiers en meme temps : serie stricte, un a la fois.
