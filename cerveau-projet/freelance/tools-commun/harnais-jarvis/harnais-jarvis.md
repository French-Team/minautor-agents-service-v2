# harnais-jarvis -- Harnais de COMPORTEMENT du serveur JARVIS

> Le harnais de JARVIS est SUPER important : JARVIS est le systeme
> nerveux de la v2. Ce harnais ne se contente pas de la sante statique :
> il detecte CHAQUE ecart de comportement de JARVIS (oublis, messages
> bloques, activations non tracees, files corrompues...) et PREVIENT
> **Vision** -- le seul habilite a modifier JARVIS.

| Version | 0.1.0 | Destinataires des alertes | Vision (+ Stark si ERR/CRIT) |

## Principe

```
JARVIS fonctionne (ou oublie de fonctionner)
    |
    v
HARNAIS-JARVIS scanne les files (lecture seule)
    |   regles dans harnais-jarvis-data.json (D15)
    v
ECART detecte ? (message P1 bloque, hub non route, JSON corrompu,
                  activation sans trace, agent inconnu, ...)
    |
    v
ALERTE -> inbox/vision.jsonl (format JARVIS standard, priorite 1)
           Vision est prevenue automatiquement
```

**Lecture seule** : le harnais n ecrit QUE l alerte dans l inbox du
destinataire (+ l outbox du harnais) et son journal. Il ne modifie
JAMAIS le fonctionnement de JARVIS.

## Les ecarts detectes (config D15 -- editable sans toucher au code)

| Ecart | Famille | Severite | Pourquoi |
|---|---|---|---|
| `p1_non_lu` | messages | ERR | message P1 bloquant non lu -> agent BLOQUE, boucle cassee (lecon Stark) |
| `hub_non_route` | messages | ERR | message dans inbox/jarvis.jsonl jamais route (envoye SANS --activer) |
| `message_non_transmis` | messages | ERR | **JARVIS n a PAS transmis : message dans outbox/<de> mais ABSENT de inbox/<vers> -- le destinataire ne l a jamais recu (boucle/round brise)** |
| `message_non_trace` | messages | WARN | message dans inbox/<vers> mais ABSENT de outbox/<de> -- transmission non tracee cote expediteur (asymetrie) |
| `activation_demandee_non_traitee` | activations | **CRIT** | **JARVIS n active PAS : une DEMANDE d activation (type activation / objet ACTIVATION-MISSION / demandes EDITH type=reveil-evaluation ou objet 'demande activation EDITH' - v0.13.1) reste non lue dans le hub** |
| `mission_non_demarree` | activations | ERR | **activation ecrite pour un agent mais jamais livree (message non lu) : l agent n a pas pris le relais** |
| `activation_sans_historique` | activations | WARN | activation recente (14 j) sans trace dans l historique du serveur (maillons sautes) |
| `mission_abandonnee` | files | WARN | mission en file (EN_ATTENTE...) depuis > 7 j sans reprise : JARVIS ne reprend pas |
| `agent_inconnu` | messages | ERR | de/vers hors AGENTS_VALIDES (valeur codee en dur, lecon Forge) |
| `json_corrompu` | messages | CRIT | ligne JSON invalide -> le serveur la SAUTE silencieusement (perte) |
| `message_sans_id` / `message_sans_date` | messages | WARN | structure illisible, tracabilite perdue |
| `doublon_id` | messages | WARN | acquittement ambigu |
| `mission_sans_statut` | files | WARN | file illisible |
| `structure_manquante` | sante | CRIT | element critique absent (JARVIS incomplet) |
| `syntaxe_invalide` | sante | CRIT | JARVIS ne peut pas demarrer |
| `config_invalide` | sante | CRIT | jarvis-data.json casse ou fiche/corrections manquantes |
| `bak_accumules` | proprete | WARN | .bak qui s accumulent (nettoyage oublie) |
| `serveur_inactif` | sante | WARN | le serveur MCP n a pas journalise depuis N jours (historique gelee : down ou jamais lance) |
| `alerte_non_traitee` | surveillance | ERR | une alerte (EDITH [EDITH-REVEIL], harnais [HARNAIS-JARVIS]) reste NON LUE depuis N jours : la boucle de reparation ne se ferme pas |
| `demande_utilisateur_non_traitee` | surveillance | WARN/ERR | entree de USER-DEMANDES.md plus vieille que N jours ABSENTE de la section " Dernieres modifications " (urgent -> ERR) |
| `historique_agents_gele` | surveillance | ERR | JARVIS n a PAS historise les activites dans AGENTS-activite-recente-v2.md (encart session-freelance, fichier v2 separe) : derniere activite plus recente que la derniere trace -> la tracabilite des agents est en retard |
| `edith_silencieuse` | surveillance | ERR | **EDITH n emet plus de reveil depuis N jours (3 par defaut) : son serveur de routines ou detection.py ne tourne plus -- la cellule dormante est muette, plus personne ne detecte les modifications de perimetre** |

**USER-DEMANDES.md -- section " Dernieres modifications " (source de
verite du traitement)** : quand une demande est traitee, on AJOUTE UNE
LIGNE au journal : `- <date> -- Traitee: <titre ou partie significative>`.
Le harnais ne matche que les LIGNES DU JOURNAL (celles commencant par
`-`), jamais les instructions de la section. Une demande est consideree
traitee si son titre complet OU >= 2 mots significatifs (>= 5
caracteres) apparaissent dans le journal. Les mots-cles inline
(traite/fait/termine...) restent en repli.

> **Le coeur de la surveillance (decision utilisateur 2026-08-25)** :
> 1. JARVIS doit ACTIVER les agents : une demande d activation bloquee
>    dans le hub (CRIT) ou une activation jamais livree (ERR).
> 2. JARVIS doit TRANSMETTRE les informations : tout message dans une
>    outbox doit avoir son correspondant dans l inbox du destinataire
>    (contrat envoyer/activer). Message dans outbox sans inbox =
>    l information n est JAMAIS arrivee (boucle/round brise, ERR).
> 3. JARVIS ne doit pas briser la boucle/le round : P1 non lu,
>    hub non route, mission abandonnee, activation sans trace.
> 4. JARVIS doit HISTORISER a chaque action (pour lui et les agents)
>    dans AGENTS-activite-recente-v2.md (encart 50 lignes, fichier v2 separe) + historique.db
>    (BDD SQLite, 7 jours) : si la derniere activite est plus recente
>    que la derniere trace de l encart, la tracabilite est en retard (ERR).
> 5. EDITH doit continuer de SE REVEILLER (cellule dormante) : si aucun
>    signal de vie (type reveil, objet [EDITH-...]) n est emis depuis
>    N jours (3 par defaut), son serveur de routines ou detection.py ne
>    tourne plus -- qui detectera les modifications de perimetre ? (ERR)
> Les seuils (fenetres) vivent dans `seuils` de la config :
> `activation_recente_jours` (14), `mission_abandonnee_jours` (7),
> `historique_tolerance_minutes` (5).

**REGLE (anti-edition)** : ajouter/modifier un ecart = editer
`harnais-jarvis-data.json` UNIQUEMENT (nom, famille, severite, message,
actif). Jamais le code.

## Alerte : ROUTAGE PAR GRAVITE (qui est prevenu ?)

| Gravite max du lot | Destinataires |
|---|---|
| `WARN` | Vision |
| `ERR` | **Vision + Stark** (le coordinateur responsable de JARVIS, D16) |
| `CRIT` | **Vision + Stark** + mention " ESCALADE UTILISATEUR REQUISE " dans le corps |

- Chaque ecart detecte -> message format JARVIS standard ecrit dans les
  inbox des destinataires (`de: jarvis-harnais`, priorite 1, objet
  `[HARNAIS-JARVIS] N ecart(s) <GRAVITE>`, corps detaille, type
  harnais-jarvis) + l outbox du harnais garde la trace.
- **DEDUP** : journal `alertes-jarvis.jsonl` -- un meme ecart (type +
  cle) n est signale qu UNE fois. Pas de spam : quand le probleme est
  corrige, le prochain check ne re-alerte pas l historique.
- Vision lit l alerte via `jarvis.py lire --vers vision`, diagnostique,
  corrige, acquitte. Stark est informe des ERR/CRIT pour coordonner
  (il ne modifie pas JARVIS : il relaie a Vision).

## Usage

```
harnais-jarvis verifier    # detecte + ALERTE Vision (mode routine/CLI)
harnais-jarvis sante       # detecte SANS alerter (consultation)
harnais-jarvis journal     # alertes deja envoyees (dedup)
harnais-jarvis aide
```

## Declenchement

1. **A la demande** : `harnais-jarvis verifier` (par Stark, l utilisateur,
   ou tout agent habilite).
2. **Routine periodique** : routine `harnais` (ex-harnais-jarvis, renommee
   2026-08-26) dans
   `freelance/routines/manifest.json` (D15) -> detection + alerte
   automatiques a intervalle regle.

## Emplacement

```
cerveau-projet/freelance/tools-commun/harnais-jarvis/
  harnais-jarvis.md            <- ce document
  harnais-jarvis-data.json     <- CONFIG D15 (regles d ecarts : a editer)
  entry.py                     <- CLI (verifier / sante / journal)
  fonctions/harnais_jarvis.py  <- moteur (scan + detection + alerte + dedup)
  alertes-jarvis.jsonl         <- journal des alertes (dedup)
```

## Education

- **Vision** (reparatrice) : lit les alertes `[HARNAIS-JARVIS]` dans son
  inbox, diagnostique, corrige (elle seule), acquitte. Voir vision.md +
  vision/corrections.md.
- **Stark** (coordinateur, destinataire ERR/CRIT) : est informe quand
  JARVIS derape ; il coordonne (relaie a Vision), il ne corrige pas
  lui-meme (exclusivite Vision). Voir stark/corrections.md.
