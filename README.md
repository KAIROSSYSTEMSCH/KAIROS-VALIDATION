# KAIROS — Démonstration de reproductibilité (Acte 2)

Rejeu d'un artefact scellé le 2026-06-06, à partir d'un jeu de données public (BBBP, DeepChem).
Aucun composant propriétaire Kairos. Le replay s'appuie uniquement sur des bibliothèques open source.

## 1. Chemin principal — machine locale

C'est le chemin de référence : il ne dépend d'aucune infrastructure Kairos.

```bash
# 0 — récupérer les fichiers de ce dépôt (si pas déjà fait)
git clone https://github.com/KAIROSSYSTEMSCH/KAIROS-VALIDATION.git
cd KAIROS-VALIDATION

# 1 — micromamba (gestionnaire d'environnement Python, sans droits admin)
# déjà installé ? passez à l'étape 2. Sinon :
curl -Ls -o micromamba "https://github.com/mamba-org/micromamba-releases/releases/download/2.0.5-0/micromamba-linux-64"
chmod +x micromamba
# macOS (Apple Silicon) : remplacez "linux-64" par "osx-arm64" ci-dessus
# macOS (Intel)          : remplacez "linux-64" par "osx-64" ci-dessus

# 2 — environnement isolé, versions figées
./micromamba create -p ./env python=3.10.12 pip -c conda-forge
./env/bin/pip install pandas==1.5.3 pyarrow==23.0.0 "numpy<2"

# 3 — exécution
./env/bin/python kairos_replay_bbbp.py
```

Résultat attendu :
```
KAIROS REPLAY
----------------------------------------
Source SHA-256        MATCH
Reconstruction        MATCH
Sealed artifact        MATCH

RESULT                PASS
----------------------------------------
```

## 2. Véhicules alternatifs — environnements tiers

Utiles pour un premier aperçu ou en l'absence d'environnement local disponible.
Ne remplacent pas la valeur probatoire du replay local (voir section « Chemin principal »).

- **Colab** : `KAIROS_VALIDATION_Replay.ipynb` — Runtime → Run all
- **Codespaces** : une fois l'environnement ouvert, dans le terminal :
  ```bash
  bash .devcontainer/run_verifier.sh
  ```
- **Kaggle** : [kairos-validation-replay](https://www.kaggle.com/code/kairossystems/kairos-validation-replay) — nécessite un compte (gratuit) et de cliquer « Copy & Edit »

## 3. Si le résultat diverge

- **`Source SHA-256` ne correspond pas ?** Le fichier `BBBP.csv` ne correspond pas à l'empreinte de la source de référence — retéléchargez-le depuis la source indiquée.
- **`Reconstruction` ou `Sealed artifact` ne correspond pas ?** Vérifiez les versions exactes de pandas/pyarrow/numpy (l'empreinte dépend de la version précise, pas seulement de la version majeure) — comparez avec les versions indiquées à l'étape 2.
- **Le script échoue avant d'afficher un résultat ?** Vérifiez l'empreinte du script lui-même avant exécution (voir ci-dessous) — s'il ne correspond pas, ne l'exécutez pas, contactez-nous.

## Empreintes de référence

```
Script kairos_replay_bbbp.py : SHA-256 9a35c6fb53a1bf8f355946d6b4ac496691e047218ef8dffc43e30281dbf825a1
CSV source (BBBP.csv)        : d07a38487aeac5cee5508413e468043ef3097451d2a112701c2d60be9ec6b662
Parquet scellé (2026-06-06)  : 4621ac8d5d4a728a169fb4d5b8c35682b954928a019d575e3eca140cd563489f
```

## Contact

Question ou écart : security@kairossystems.ch
