#!/usr/bin/env python3
"""
KAIROS — Demonstration de reproductibilite (Acte 2)
Rejeu d'un artefact enregistre, a partir d'une source publique.

Aucun composant proprietaire Kairos. Trois appels de bibliotheques open source.
L'empreinte produite doit correspondre a celle scellee le 2026-06-06.

Prerequis :
    pip install "pandas==1.5.3" "pyarrow==23.0.0" "numpy<2"
Usage :
    python3 kairos_replay_bbbp.py
"""
import hashlib
import urllib.request
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

SOURCE = "https://deepchemdata.s3.us-west-1.amazonaws.com/datasets/BBBP.csv"
CSV_SHA256_ATTENDU = "d07a38487aeac5cee5508413e468043ef3097451d2a112701c2d60be9ec6b662"
PARQUET_SHA256_SCELLE = "4621ac8d5d4a728a169fb4d5b8c35682b954928a019d575e3eca140cd563489f"


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    checks = []

    # 1. Telecharger le dataset depuis sa source publique
    urllib.request.urlretrieve(SOURCE, "BBBP.csv")
    csv_h = sha256("BBBP.csv")
    checks.append(("Source SHA-256", csv_h == CSV_SHA256_ATTENDU))

    # 2. Transformation : trois appels de bibliotheques open source
    df = pd.read_csv("BBBP.csv", low_memory=False)
    t = pa.Table.from_pandas(df)
    pq.write_table(t, "bbbp.parquet", compression="snappy")

    # 3. Empreinte et comparaison avec l'artefact scelle
    obtenu = sha256("bbbp.parquet")
    checks.append(("Reconstruction", len(df) == 2050))
    checks.append(("Sealed artifact", obtenu == PARQUET_SHA256_SCELLE))

    result = all(ok for _, ok in checks)

    print()
    print("KAIROS REPLAY")
    print("-" * 40)
    for label, ok in checks:
        print(f"{label:<22}{'MATCH' if ok else 'DIVERGE'}")
    print()
    print(f"{'RESULT':<22}{'PASS' if result else 'FAIL'}")
    print("-" * 40)
    print()
    if not result:
        print("DIVERGENCE — ne pas interpreter silencieusement.")
        print("Voir le dossier complet, section Lecture des ecarts.")
        print()
    print("Detail :")
    print("  parquet obtenu :", obtenu)
    print("  parquet scelle :", PARQUET_SHA256_SCELLE)
    print()
    print("Ce resultat provient d'un vehicule d'execution (Colab/Codespaces/Kaggle).")
    print("La preuve est le resultat deterministe et son empreinte, pas la plateforme utilisee.")


if __name__ == "__main__":
    main()
