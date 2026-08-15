# KAIROS — Démonstration de reproductibilité (Acte 2)

Rejeu d'un artefact scellé le 2026-06-06, à partir d'un jeu de données public (BBBP, DeepChem).
Aucun composant propriétaire Kairos. Trois appels de bibliothèques open source (pandas, pyarrow).

Ce dépôt est diffusé sous accord de confidentialité (NDA). Voir NOTICE.md.

## 1. Chemin principal — machine locale

C'est le replay qui a la plus grande valeur probatoire : il ne dépend d'aucune infrastructure Kairos.

```bash
# Python 3.10 requis (via micromamba, sans droits admin, ou tout autre gestionnaire d'environnement)
micromamba create -p ./env python=3.10.12 pip -c conda-forge
./env/bin/pip install pandas==1.5.3 pyarrow==23.0.0 "numpy<2"
./env/bin/python kairos_replay_bbbp.py
```

R�sultat attendu :
```
parquet scelle : 4621ac8d5d4a728a169fb4d5b8c35682b954928a019d575e3eca140cd563489f
PASS — YOUR REPLAY
```

## 2. Véhicules alternatifs — environnements tiers

Utiles pour un premier aperçu ou en l'absence d'environnement local disponible.
Ne remplacent pas la valeur probatoire du replay local (voir dossier complet, section "Chemin principal").

- **Colab** : `KAIROS_DEMO2_Replay.ipynb` — Runtime → Run all
- **Codespaces** : ouverture automatique, replay lancé dès la création de l'environnement (voir `.devcontainer/`)
- **Kaggle** : voir dossier complet, section "Véhicules alternatifs"

## Empreintes de référence

```
Script kairos_replay_bbbp.py : voir dossier complet, SHA-256 2a9ac46c...065fce
CSV source (BBBP.csv)        : d07a38487aeac5cee5508413e468043ef3097451d2a112701c2d60be9ec6b662
Parquet scellé (2026-06-06)  : 4621ac8d5d4a728a169fb4d5b8c35682b954928a019d575e3eca140cd563489f
```

## Contact

Question ou écart : security@kairossystems.ch
