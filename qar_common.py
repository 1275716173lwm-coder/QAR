# coding: utf-8

from pathlib import Path

import pandas as pd


CSV_ENCODINGS = ("utf-8", "utf-8-sig", "gb18030", "cp936")
FONT_CANDIDATES = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]


def configure_matplotlib(plt):
    plt.rcParams["font.sans-serif"] = FONT_CANDIDATES
    plt.rcParams["axes.unicode_minus"] = False


def read_qar_csv(path):
    csv_path = Path(path)
    for encoding in CSV_ENCODINGS:
        try:
            return pd.read_csv(
                csv_path,
                header=1,
                encoding=encoding,
                low_memory=False,
            )
        except UnicodeDecodeError:
            continue
        except ValueError as exc:
            if "encoding" not in str(exc).lower():
                raise
            continue
    raise UnicodeDecodeError(
        "csv",
        b"",
        0,
        1,
        f"Unable to decode {csv_path} with supported encodings",
    )


def numeric_columns(dataframe, columns):
    return dataframe.loc[:, columns].apply(pd.to_numeric, errors="coerce")


def numeric_array(dataframe, columns):
    return numeric_columns(dataframe, columns).to_numpy()
