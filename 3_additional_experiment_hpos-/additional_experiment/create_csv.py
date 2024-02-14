import json
import random

import pandas as pd

random.seed(20221018)


def load_data(path: str):
    out = []
    with open(path, "r") as f_r:
        for line in f_r:
            instance: dict = json.loads(line)
            out.append(instance)
    return out


def preprocess_text_for_disp_in_html(raw_text: str):
    processed_text = raw_text.replace("&", "&amp;")
    processed_text = processed_text.replace("<", "&lt;")
    processed_text = processed_text.replace(">", "&gt;")
    processed_text = processed_text.replace("'", "&#39;")
    processed_text = processed_text.replace('"', "&quot;")
    processed_text = processed_text.replace("£", "&pound;")
    return processed_text


def prepare_csv_row(conv_id, uttr_df):
    conversations = []
    speakers = []
    objective_utterances = []
    categories = []
    questions = []

    cur_conversation = ""

    for i in range(len(uttr_df)):
        uttr = uttr_df.iloc[i]
        processed_utterance = preprocess_text_for_disp_in_html(str(uttr["utterance"]))
        if uttr["conversation_id"] == conv_id:
            if cur_conversation == "":
                cur_conversation += uttr["speaker"] + ":" + processed_utterance
            else:
                cur_conversation += "<%%>" + uttr["speaker"] + ":" + processed_utterance

            if uttr["true_face"] != "other":
                conversations.append(cur_conversation)
                speakers.append(uttr["speaker"])
                objective_utterances.append(processed_utterance)
                questions.append(
                    "What is the intention of the {}'s utterance: '{}' ? Choose one option and provide the reason for your choice in the space below.".format(
                        uttr["speaker"], processed_utterance
                    )
                )

                candidate_options = [
                    "ER criticizes EE.",
                    "ER expresses their preference for charities or the targets they want to help.",
                    "ER motivates EE to donate to STC, such as by explaining the essential role their donation plays in helping children or highlighting the suffering children endure due to war, poverty, and other hardships.",
                    "ER asks or confirms the amount that EE is donating to STC.",
                ]
                options = "["
                for candidate_option in candidate_options:
                    options += "'" + candidate_option + "'" + ", "
                options += "]"
                categories.append(options)

    return (
        conversations,
        speakers,
        objective_utterances,
        categories,
        questions,
    )
