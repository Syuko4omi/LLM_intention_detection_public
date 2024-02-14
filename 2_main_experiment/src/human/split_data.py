import json

import pandas as pd

from create_csv import prepare_csv_row


def load_data(path: str):
    out = []
    with open(path, "r") as f_r:
        for line in f_r:
            instance: dict = json.loads(line)
            out.append(instance)
    return out


utterances = load_data("../../data/concatenated_data_with_four_options.jsonl")
test_conv_ids = list(set([utterance["conversation_id"] for utterance in utterances]))

for test_id in test_conv_ids:
    (
        conversations,
        speakers,
        objective_utterances,
        categories,
        questions,
        dummy_inst,
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
    for dummy_question in dummy_inst:  # add dummy questions
        L.append(
            [
                dummy_question["conversation"],
                dummy_question["speaker"],
                dummy_question["utterance"],
                dummy_question["options"],
                dummy_question["question"],
            ]
        )
    df = pd.DataFrame(
        L, columns=["conversation", "speaker", "utterance", "categories", "question"]
    )
    df.to_csv(f"test_data/conv_id_{test_id}.csv", index=False)
