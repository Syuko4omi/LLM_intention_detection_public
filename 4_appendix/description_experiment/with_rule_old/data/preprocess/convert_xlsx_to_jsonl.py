# convert csv file to jsonl

import pandas as pd

# do this first
df = pd.read_excel("Persuasion Face Act Prediction.xlsx", engine="openpyxl")
df.to_json(
    "Persuasion Face Act Prediction.jsonl",
    orient="records",
    force_ascii=False,
    lines=True,
)
