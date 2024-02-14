import json
import random

import pandas as pd

# do this fourth (after concatenating utterances)


def load_data(path: str):
    out = []
    with open(path, "r") as f_r:
        for line in f_r:
            instance: dict = json.loads(line)
            out.append(instance)
    return out


def pickup_random_option(
    true_face: str,
    true_description: str,
    true_speaker: str,
    description_dict: dict[str, dict[str, list[str]]],
    prohibited_description_dict,
    alternative_descriptions,
) -> tuple[list[str], int]:
    candidate_description_list = []
    if (
        str(true_description) == "None"
    ):  # these are not counted as problems (utterances whose face act is other)
        options = ["-", "-", "-", "-"]
        answer_idx = -1
        return (options, answer_idx)

    for (
        key
    ) in (
        description_dict.keys()
    ):  # extract descriptions which will be candidate as distractors
        for description in description_dict[key][true_speaker]:
            if (
                (description != true_description)
                and (key != true_face)
                and (
                    description
                    not in prohibited_description_dict[true_description]
                    + alternative_descriptions
                )
            ):
                candidate_description_list.append(description)
    options = random.sample(candidate_description_list, 3)
    answer_idx = random.randint(0, 3)
    options.insert(answer_idx, true_description)
    return (options, answer_idx)


def save_new_options(uttr, dst_path: str):
    prohibited_description_1 = [
        "ER motivates EE to donate to STC, such as by explaining the essential role their donation plays in helping children or highlighting the suffering children endure due to war, poverty, and other hardships.",
        "ER encourages EE to do good deeds, other than donating to STC.",
        "ER tries to minimize the financial burden on EE.",
        "ER makes donating easy and simple, reducing any inconvenience for EE.",
        "ER states that STC provides information on donations or other related matters, implying that STC engages in beneficial activities for society.",
        "ER praises or promotes the good deeds of STC.",
    ]
    prohibited_description_2 = [
        "EE claims that they want to do something good, such as helping children.",
        "EE doubts or criticizes STC or ER.",
        "EE is either hesitant or unwilling to donate to STC.",
        "EE refuses to donate to STC or increase the donation amount without even giving a reason.",
        "EE cites reason for not donating at all or not donating more.",
        "EE expresses their preference for charities or the targets they want to help.",
        "EE asks ER questions about STC.",
        "EE asks ER how ER themselves are involved in STC.",
    ]
    prohibited_description_3 = [
        "EE shows willingness to donate or to discuss the charity.",
        "EE expresses their preference for charities or the targets they want to help.",
    ]
    prohibited_description_4 = [
        "EE asks ER for donation.",
        "EE shows willingness to donate or to discuss the charity.",
    ]
    prohibited_description_5 = [
        "EE either knows nothing about STC or is not interested in STC.",
        "EE asks ER questions about STC.",
    ]
    prohibited_description_dict = {}

    df = pd.read_excel("../description_table.xlsx", engine="openpyxl")
    face_act_list = ["spos+", "hpos+", "spos-", "hpos-", "sneg+", "hneg+", "hneg-"]
    description_dict = {}
    for face_act in face_act_list:
        description_dict[face_act] = {
            "ER": [],
            "EE": [],
        }
    for i in range(len(df)):
        true_face, speaker, description = (
            df.loc[i]["true_face"],
            df.loc[i]["speaker"],
            df.loc[i]["description"],
        )
        description_dict[true_face][speaker].append(description)
        prohibited_description_dict[description] = []

    for key in prohibited_description_dict.keys():
        if key in prohibited_description_1:
            for item in prohibited_description_1:
                if key != item:
                    prohibited_description_dict[key].append(item)
        if key in prohibited_description_2:
            for item in prohibited_description_2:
                if key != item:
                    prohibited_description_dict[key].append(item)
        if key in prohibited_description_3:
            for item in prohibited_description_3:
                if key != item:
                    prohibited_description_dict[key].append(item)
        if key in prohibited_description_4:
            for item in prohibited_description_4:
                if key != item:
                    prohibited_description_dict[key].append(item)
        if key in prohibited_description_5:
            for item in prohibited_description_5:
                if key != item:
                    prohibited_description_dict[key].append(item)

    id_to_char = ["A", "B", "C", "D"]
    id_to_speaker = ["ER", "EE"]

    with open(dst_path, "w") as f_w:
        for utterance in uttr:
            if utterance["alternative_description"] is not None:
                alternative_descriptions = utterance["alternative_description"].split(
                    "\n"
                )
            else:
                alternative_descriptions = []
            options, answer_idx = pickup_random_option(
                utterance["true_face"],
                utterance["description"],
                id_to_speaker[utterance["speaker"]],
                description_dict,
                prohibited_description_dict,
                alternative_descriptions,
            )
            utterance["option_a"] = options[0]
            utterance["option_b"] = options[1]
            utterance["option_c"] = options[2]
            utterance["option_d"] = options[3]
            utterance["answer_idx"] = answer_idx
            utterance["answer_char"] = (
                id_to_char[answer_idx] if answer_idx != -1 else "Z"
            )
            json.dump(utterance, f_w, ensure_ascii=False)
            f_w.write("\n")


if __name__ == "__main__":
    random.seed(20221018)
    SRC_PATH = "../concatenated_data.jsonl"
    DST_PATH = "../concatenated_data_with_four_options.jsonl"
    UTTERANCES = load_data(SRC_PATH)
    save_new_options(UTTERANCES, DST_PATH)
