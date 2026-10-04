---
identite:
  type: pattern
  appartient_a: optimus-prime
  commun: false
---

# TEMPLATE -- le formulaire de la demande

Ce fichier est le MODE D EMPLOI du canal `user-demandes/user-demandes.md`. Il est
ecrit par la Matrice, en ASCII ; tes mots, eux, ne sont jamais reecrits.

La LEMENDE (les 10 mots entre crochets, les 4 patterns d etape, ce qui bloque)
vit dans le HEAD du canal, juste au-dessus de tes demandes : elle est donc
toujours sous tes yeux, sans que tu aies un autre fichier a ouvrir. Ce template
ne fait que le FORMULAIRE.

## 1. LE FORMULAIRE VIERGE (a copier, puis a remplir)

    ##A-FAIRE################################
    ##FAIT###################################
    ##A-CONTROLER############################
    [<crochet>] <ta demande, en une phrase>

    pourquoi : <la raison, si tu en as une>

    resultat attendu : <ce que tu verras quand ce sera fait>

Tu supprimes les lignes dont tu n as pas besoin. Le seul element OBLIGATOIRE est
le CROCHET entre crochets.

## 2. LE MEME FORMULAIRE, REMPLI (un exemple)

    ##A-FAIRE################################
    ##FAIT###################################
    ##A-CONTROLER############################
    [mission] transformer le fichier de suivi des outils en page unique

    pourquoi : il est eparpille sur six dossiers, on ne le lit jamais en entier

    resultat attendu : une page qui tient en un ecran et qui renvoie a sa source

Trois choses a voir dans cet exemple :

  - les trois patterns de tete sont laits VIDES : c est l etat par defaut, une
    demande qui n a pas encore ete servie. Tu les supprimes si tu preferes n en
    garder qu un ;
  - le crochet `[mission]` vient COLLE a la demande, sur la meme ligne, un espace
    apres. C est lui qui dit ce que la demande declenche, donc c est lui qui
    place la demande dans la file ;
  - `pourquoi` et `resultat attendu` sont facultatifs, mais `resultat attendu`
    est celui qui te sert le plus : c est lui qui permet de verifier, plus tard,
    que c est bien fini.

## 3. OU INSERER UNE DEMANDE

Une demande se colle entre deux patterns : les patterns de tete qu elle
rencontre sont les SIENS, et le dernier avant elle gagne. Concretement :

    ...fin de la demande precedente...
    ##A-FAIRE################################     <- tete de la demande suivante
    ##FAIT###################################
    ##A-CONTROLER############################
    [ta demande]

Autrement dit : tu ajoutes tes patterns PUIS ta demande, en fin de fichier. Tu
n as pas a chercher ou elle va.

## 4. UNE DEMANDE = UN CROCHET = UN TYPE

Le crochet est un mot de la liste du HEAD. Il est converti en TYPE, puis en file
de travail, sans jamais etre devine. Un crochet hors liste n est pas rejete
avec un bruit : la demande reste dans le canal, telle que tu l as ecrite, et
c est toi qui choisis.

## 5. CE QUE LA PORTE DE CONFORMITE PEUT TE RENVOYER

Avant tout depot, le canal est passe au crible. Trois verdicts, un seul refus
suffit a arreter le depot (le detail des trois verdicts est dans le HEAD) :

  - rien a corriger : elle ne dit rien, et le canal reste intact ;
  - un geste MECANIQUE : le rapport nomme la ligne, tu relances, c est corrige ;
  - une DECISION qui te revient : c est toi qui corriges, la demande reste ici.

Dans les trois cas, le canal n est JAMAIS modifie par la Matrice : ni tes
accents, ni ton orthographe, ni tes crochets ne sont touches.
