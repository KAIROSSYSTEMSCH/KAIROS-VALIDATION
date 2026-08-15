#!/usr/bin/env bash
set -e
echo "=============================================================================="
echo "KAIROS — Demonstration de reproductibilite (Acte 2) — replay automatique"
echo "=============================================================================="

curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba > /dev/null 2>&1
./bin/micromamba create -y -p ./env python=3.10.12 pip -c conda-forge > /dev/null 2>&1
./env/bin/pip install -q pandas==1.5.3 pyarrow==23.0.0 "numpy<2"

./env/bin/python kairos_replay_bbbp.py
