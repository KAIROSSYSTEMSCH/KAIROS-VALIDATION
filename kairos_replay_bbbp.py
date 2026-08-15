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
    print("pandas", pd.__version__, "| pyarrow", pa.__version__)

    # 1. Telecharger le dataset depuis sa source publique
    urllib.request.urlretrieve(SOURCE, "BBBP.csv")
    csv_h = sha256("BBBP.csv")
    print("CSV telecharge :", csv_h)
    print("CSV attendu    :", CSV_SHA256_ATTENDU)
    assert csv_h == CSV_SHA256_ATTENDU, "Le CSV source ne correspond pas."

    # 2. Transformation : trois appels de bibliotheques open source
    df = pd.read_csv("BBBP.csv", low_memory=False)
    print("lignes :", len(df))
    t = pa.Table.from_pandas(df)
    pq.write_table(t, "bbbp.parquet", compression="snappy")

    # 3. Empreinte et comparaison avec l'artefact scelle
    obtenu = sha256("bbbp.parquet")
    print("parquet obtenu :", obtenu)
    print("parquet scelle :", PARQUET_SHA256_SCELLE)
    print(">>> MATCH" if obtenu == PARQUET_SHA256_SCELLE else ">>> DIVERGE")


if __name__ == "__main__":
    main()
