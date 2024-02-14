import json
import random

import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows

# do this first (chect the correspondence between annotated description and the speaker)

corres = {"ER": 0, "EE": 1}
df = pd.read_excel("../description_annotated_data.xlsx", engine="openpyxl")
mistaken_flag = False
for i in range(len(df)):
    if str(df["description"][i]) != "nan":
        speaker = df["speaker"][i]
        description_subject = df["description"][i][:2]
        if speaker != corres[description_subject]:
            mistaken_flag = False
            print(f"id:{i}")
            print(f"speaker: {speaker}")
            print(df["utterance"][i])
            print(df["description"][i])
if not mistaken_flag:
    print("NO ERRORS DETECTED!")
