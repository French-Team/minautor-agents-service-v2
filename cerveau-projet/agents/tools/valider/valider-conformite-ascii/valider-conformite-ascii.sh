#!/bin/bash
# valider-conformite-ascii.sh
# Outil pour valider la conformite ASCII stricte du projet.
# Regle : AUCUN caractere non-ASCII n'est tolere (accents, emojis, symboles).
# Seules exceptions : le dossier exemples/ (zone de test volontaire) et les
# dictionnaires fonctionnels (corriger-dictionnaire-accents, dictionnaire-emojis) qui
# DOIVENT contenir les caracteres qu'ils mappent (exceptions declarees).
# Version : 0.3.0-beta

# Configuration
VERSION="0.3.0"
STATUT="prepare"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

afficher_aide() {
    echo "=== valider-conformite-ascii v${VERSION} ==="
    echo ""
    echo "Usage: $0 [OPTIONS] [DOSSIER]"
    echo ""
    echo "Valide que TOUT le contenu est ASCII pur (regle immuable : aucun"
    echo "accent, emoji ou symbole Unicode). Les seules exceptions sont le"
    echo "dossier exemples/ (test volontaire) et les dictionnaires fonctionnels."
    echo ""
    echo "Options :"
    echo "  --dry-run       Afficher les erreurs sans corriger"
    echo "  --corriger      Corriger automatiquement (via corriger-accents-zones-sensibles --all)"
    echo "  --exclure       Exclure des motifs supplementaires"
    echo "  --help          Afficher cette aide"
    echo ""
    echo "Exemples :"
    echo "  $0 cerveau-projet/"
    echo "  $0 --dry-run cerveau-projet/"
    echo "  $0 --corriger cerveau-projet/"
    echo ""
}

main() {
    local dossier="."
    local dry_run="false"
    local corriger="false"
    local exclude=""

    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run) dry_run="true"; shift ;;
            --corriger) corriger="true"; shift ;;
            --exclure) exclude="$2"; shift 2 ;;
            --help) afficher_aide; exit 0 ;;
            *) dossier="$1"; shift ;;
        esac
    done

    echo "=== Valider conformite ASCII stricte ==="
    echo "Version : ${VERSION}"
    echo "Dossier : ${dossier}"
    echo ""

    if [ ! -e "$dossier" ]; then
        echo -e "${RED}[ERREUR] Le chemin n'existe pas : $dossier${NC}"
        exit 1
    fi

    # Detection via Python (fiable, independante de grep)
    RESULTAT=$(python - "$dossier" "$exclude" <<'PYEOF'
import io, os, sys

cible = sys.argv[1]
exclure_extra = sys.argv[2] if len(sys.argv) > 2 else ""
motifs_exclus = ["exemples", "corriger-dictionnaire-accents", "dictionnaire-emojis", ".git", ".agents", ".backup", ".tmp"]
if exclure_extra:
    motifs_exclus += [m.strip() for m in exclure_extra.split(",") if m.strip()]

fichiers = []
if os.path.isfile(cible):
    fichiers = [cible]
else:
    for r, d, fs in os.walk(cible):
        if any(m in r for m in [".git", ".agents"]):
            continue
        for f in fs:
            fichiers.append(os.path.join(r, f))

rapports = []
for fichier in fichiers:
    if any(m in fichier for m in motifs_exclus):
        continue
    ext = os.path.splitext(fichier)[1].lower()
    if ext not in (".md", ".sh", ".py", ".txt", ".json", ".yaml", ".yml", ".js"):
        continue
    try:
        with io.open(fichier, encoding="utf-8") as fh:
            lignes = fh.read().split("\n")
    except Exception:
        continue
    lignes_bad = []
    for i, ligne in enumerate(lignes, 1):
        mauvais = [ch for ch in ligne if ord(ch) > 127]
        if mauvais:
            # Caracteres uniques et leur nombre
            uniq = {}
            for ch in mauvais:
                uniq[ch] = uniq.get(ch, 0) + 1
            detail = ", ".join("%s(x%d)" % (ch, n) for ch, n in list(uniq.items())[:5])
            lignes_bad.append((i, len(mauvais), detail))
    if lignes_bad:
        rapports.append((fichier, lignes_bad))

nb_fichiers = len(rapports)
nb_lignes = sum(len(lb) for _, lb in rapports)
nb_caracteres = sum(n for _, lb in rapports for _, n, _ in lb)

for fichier, lignes_bad in rapports:
    print("  [%s]" % fichier)
    for i, n, detail in lignes_bad[:5]:
        print("      ligne %d : %d caractere(s) (%s)" % (i, n, detail))
    if len(lignes_bad) > 5:
        print("      ... et %d autre(s) ligne(s)" % (len(lignes_bad) - 5))

print("=== Resume ===")
print("Fichiers non conformes : %d" % nb_fichiers)
print("Lignes concernees : %d" % nb_lignes)
print("Caracteres non-ASCII : %d" % nb_caracteres)
PYEOF
)
    echo "$RESULTAT"

    NB_FICHIERS=$(echo "$RESULTAT" | tr -d '\r' | grep -oE 'Fichiers non conformes : [0-9]+' | grep -oE '[0-9]+')
    NB_FICHIERS="${NB_FICHIERS:-0}"

    if [ "$NB_FICHIERS" -eq 0 ]; then
        echo -e "${GREEN}[OK] Conformite ASCII stricte validee${NC}"
        exit 0
    fi

    if [ "$corriger" = "true" ]; then
        echo ""
        echo -e "${BLUE}--- Correction automatique (--all) ---${NC}"
        CORRIGER="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/corriger/corriger-accents-zones-sensibles/corriger-accents-zones-sensibles.sh"
        bash "$CORRIGER" --recursive --all "$dossier" 2>&1 | tail -6
        echo ""
        echo "Relancez la validation pour confirmer."
        exit 1
    fi

    if [ "$dry_run" = "false" ]; then
        echo ""
        echo -e "${YELLOW}[ATTENTION] Des caracteres non-ASCII ont ete detectes${NC}"
        echo "Regle immuable : aucun accent, emoji ou symbole Unicode n'est tolere."
        echo "Utilisez --corriger pour corriger, ou combos-corriger-non-ascii (combo)."
    fi
    exit 1
}

# Executer
main "$@"
