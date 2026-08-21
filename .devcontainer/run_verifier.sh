#!/usr/bin/env bash
set -e

fail() {
  echo ""
  echo "------------------------------------------------------------------"
  echo "  EXÉCUTION INTERROMPUE"
  echo "------------------------------------------------------------------"
  echo "  $1"
  echo ""
  echo "  Aucune mesure n'a pu être effectuée à cette étape."
  echo "------------------------------------------------------------------"
  exit 1
}

echo "------------------------------------------------------------------"
echo "  KAIROS VERIFIER — replay guidé"
echo "------------------------------------------------------------------"

EXPECTED="e2f6cd4b4e67e98d19adbd76e9e8c12eae0276cca3755b324e55f3b966525be4"
OBTAINED=$(sha256sum determinism_ladder.py 2>/dev/null | cut -d' ' -f1) || fail "determinism_ladder.py introuvable dans ce dossier."

if [ "$OBTAINED" != "$EXPECTED" ]; then
  fail "Empreinte du script non conforme.
  attendu : $EXPECTED
  obtenu  : $OBTAINED
  Ne pas exécuter — contacter security@kairossystems.ch"
fi
echo "  Empreinte du script : IDENTIQUE"

if [ ! -d "env" ]; then
  echo "  Création de l'environnement..."
  python3 -m venv env || fail "Impossible de créer l'environnement virtuel (python3 -m venv env)."
fi

echo "  Installation des dépendances..."
./env/bin/pip install -q -r requirements.txt || fail "Échec de l'installation des dépendances (pip install). Relancez ce script — l'environnement partiellement installé sera complété."

echo "  Exécution dans l'enveloppe déclarée..."
echo ""
OPENBLAS_CORETYPE=Haswell \
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
PYTHONHASHSEED=0 ./env/bin/python3 determinism_ladder.py || fail "Le script s'est arrêté avant de produire un résultat complet."
