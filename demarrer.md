---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Demarrage -- la porte d'entree de session

> Ce fichier sert UNIQUEMENT a lancer la session : le LLM s'identifie et devient
> Cerberus. Tout le reste (protocoles, conventions, inventaire) vit dans le
> cerveau : pointez `cerveau-projet/index-cerveau.md`.

---

## 1. LANCER LE PARCOURS DE DEMARRAGE (OBLIGATOIRE)

> **CE FICHIER NE SE LIT PAS : IL SE LANCE.** Le demarrage est une carte de
> decision (jeu de piste) comme le reste du cerveau. Lire ce fichier et s'arreter
> = NE PAS demarrer. Il faut EXECUTER la commande ci-dessous :

```
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \
  cerveau-projet/demarrage/parcours-demarrage.json
```

Le parcours guide case par case :
1. **c0** : question honnete de relecture (fiche Cerberus en memoire ?)
2. **c1** : S'identifier -- lancer `sidentifier <mon-id>` (l'id est donne par
   l'utilisateur ; sans id, le DEMANDER avant toute action)
3. **c2** : Verifier que MON bloc existe dans AGENTS.md (champ **Id LLM**)
4. **c3** : Devenir Cerberus et se presenter
5. **c4/c5** : Attendre la mission, puis lancer le parcours de l'agent habilite

---

## 2. Quand une mission arrive -> lancer SON parcours

```
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \
  cerveau-projet/agents/<agent>/parcours/parcours-<agent>.json
```

Le parcours donne a chaque etape l'indice exact (outil, fichier, regle, controle)
et les branches selon la reponse. Liste des parcours + spec :
[guider-parcours.md](cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.md).

---

## 3. Pour tout le reste

-> [cerveau-projet/index-cerveau.md](cerveau-projet/index-cerveau.md) : protocoles
   cles, conventions, regles immuables, fichiers cles, classeur de variables.
