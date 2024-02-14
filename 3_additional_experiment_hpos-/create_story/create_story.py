import os
import time

import pandas as pd
from openai import OpenAI
from tqdm import tqdm

MODEL_NAME = "gpt-4-0613"
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
all_conversation_df = None

for instruction_pattern in range(1, 3):
    f = open(
        "instructions/instruction_{}.txt".format(instruction_pattern),
        "r",
    )
    datalist = f.readlines()
    prompt = "".join(datalist)

    for i in tqdm(range(10)):
        response = openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
        )
        temp = response.choices[0].message.content.split("\n")
        L = []
        for item in temp:
            if item != "":
                L.append(
                    [
                        int(str(instruction_pattern) + str(i)),
                        item[:2],
                        item[4:],
                        "other",
                        "-",
                        "-",
                    ]
                )
        df = pd.DataFrame(
            data=L,
            columns=[
                "conversation_id",
                "speaker",
                "utterance",
                "true_face",
                "description",
                "hpos-_type",
            ],
        )
        if all_conversation_df is None:
            all_conversation_df = df
        else:
            all_conversation_df = pd.concat([all_conversation_df, df])

        time.sleep(10)

all_conversation_df.to_excel("conversation_data.xlsx", index=False)
