import argparse

import pandas as pd

# do this third


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", default="extra_data_annotated_by_human.xlsx")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    my_args = get_args()
    df = pd.read_excel(my_args.file_path, engine="openpyxl")
    df.to_json(
        "raw_data.jsonl",
        orient="records",
        force_ascii=False,
        lines=True,
    )
