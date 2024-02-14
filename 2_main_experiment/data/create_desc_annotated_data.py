import glob
import re

import pandas as pd


def remove_escape(raw_text: str):
    processed_text = raw_text.replace("&pound;", "£")
    processed_text = processed_text.replace("&quot;", '"')
    processed_text = processed_text.replace("&#39;", "'")
    processed_text = processed_text.replace("&gt;", ">")
    processed_text = processed_text.replace("&lt;", "<")
    processed_text = processed_text.replace("&amp;", "&")
    return processed_text


def return_face_act(dtfrm):
    desc_to_face_act = {}
    for face_act, description in zip(dtfrm["true_face"], dtfrm["description"]):
        desc_to_face_act[description] = face_act
    return desc_to_face_act


def extract_utterance_description_faceacts(dtfrm, desc_to_face_act):
    """
    # speakers: 一発話ごとの話者
    # utterances: 各発話
    # majority_vote_descriptions: 3人のアノテーターの多数決の結果（全員割れた場合と、何もついていない場合は"-"）
    # face_acts: 発話ごとのface act（フェイスアクトなしは"other"）
    """
    all_speaker_and_utterance = dtfrm.iloc[0]["conversation"].split("<%%>")
    speakers = [
        speaker_and_utterance[:2] for speaker_and_utterance in all_speaker_and_utterance
    ]
    utterances = [
        remove_escape(speaker_and_utterance[3:])
        for speaker_and_utterance in all_speaker_and_utterance
    ]

    utterances_with_majority_vote_and_possible_description = [
        [remove_escape(utterance), description, answer_1]
        for (utterance, description, answer_1) in zip(
            dtfrm["utterance"], dtfrm["majority_result"], dtfrm["answer_1"]
        )
    ]

    majority_vote_descriptions = []
    face_acts = []

    for utterance in utterances:
        majority_vote_description = "-"
        face_act = "other"
        for i in range(len(utterances_with_majority_vote_and_possible_description)):
            if (
                utterances_with_majority_vote_and_possible_description[i][0]
                == utterance
            ):
                majority_vote_description = (
                    utterances_with_majority_vote_and_possible_description[i][1]
                )
                face_act = desc_to_face_act[
                    utterances_with_majority_vote_and_possible_description[i][2]
                ]
                break
        majority_vote_descriptions.append(majority_vote_description)
        face_acts.append(face_act)

    return (speakers, utterances, majority_vote_descriptions, face_acts)


L = (
    glob.glob("annotated_test_data/result_conv_id_[0-9]_summary.csv")
    + glob.glob("annotated_test_data/result_conv_id_[1-9][0-9]_summary.csv")
    + glob.glob("annotated_test_data/result_conv_id_[1-9][0-9][0-9]_summary.csv")
)

desc_table = pd.read_excel("description_table.xlsx")
desc_to_face_act = return_face_act(desc_table)

ret_df = None

for file_name in L:
    conv_id = re.search(r"\d+", file_name).group()
    df = pd.read_csv(file_name)
    (
        all_speaker,
        all_utterance,
        all_descriptions,
        all_face_act,
    ) = extract_utterance_description_faceacts(df, desc_to_face_act)

    temp_df = pd.DataFrame(
        data=[
            [conv_id, speaker, utterance, face_act, description]
            for (speaker, utterance, face_act, description) in zip(
                all_speaker, all_utterance, all_face_act, all_descriptions
            )
        ],
        columns=["conversation_id", "speaker", "utterance", "true_face", "description"],
    )

    if ret_df is None:
        ret_df = temp_df
    else:
        ret_df = pd.concat([ret_df, temp_df])

ret_df.to_excel(
    "test_data_annotated_by_human.xlsx",
    index=False,
)
