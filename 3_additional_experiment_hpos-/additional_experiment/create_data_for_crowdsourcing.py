import json

import pandas as pd

from create_csv import prepare_csv_row

df = pd.read_excel("../create_story/conversation_data.xlsx")

for test_id in range(10, 30):
    utterances = df[df["conversation_id"] == test_id]
    (
        conversations,
        speakers,
        objective_utterances,
        categories,
        questions,
    ) = prepare_csv_row(test_id, utterances)
    L = []
    for i in range(len(speakers)):
        L.append(
            [
                conversations[i],
                speakers[i],
                objective_utterances[i],
                categories[i],
                questions[i],
            ]
        )
    dtfrm = pd.DataFrame(
        L, columns=["conversation", "speaker", "utterance", "categories", "question"]
    )
    dtfrm.to_csv(f"data_for_crowdsourcing/conv_id_{test_id}.csv", index=False)
