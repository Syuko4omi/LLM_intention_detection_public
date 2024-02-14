import json

import pandas as pd

# do this fourth
# create query for gpt-4


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
) -> tuple[list[str], int]:

    candidate_description_list = [
        "ER criticizes EE.",
        "ER expresses their preference for charities or the targets they want to help.",
        "ER motivates EE to donate to STC, such as by explaining the essential role their donation plays in helping children or highlighting the suffering children endure due to war, poverty, and other hardships.",
        "ER asks or confirms the amount that EE is donating to STC.",
    ]
    if str(true_description) == "-":
        options = ["-", "-", "-", "-"]
        answer_idx = -1
        return (options, answer_idx)
    if true_face != "other" and true_description == "-":
        options = ["-", "-", "-", "-"]
        answer_idx = -1
        return (options, answer_idx)

    answer_idx = 0
    candidate_description_list.remove(true_description)
    candidate_description_list.insert(answer_idx, true_description)
    return (candidate_description_list, answer_idx)


def save_new_options(uttr, dst_path: str):
    face_act_list = ["spos+", "hpos+", "spos-", "hpos-", "sneg+", "hneg+", "hneg-"]

    id_to_char = ["A", "B", "C", "D"]

    with open(dst_path, "w") as f_w:
        for utterance in uttr:
            options, answer_idx = pickup_random_option(
                utterance["true_face"],
                utterance["description"],
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
    SRC_PATH = "raw_data.jsonl"
    DST_PATH = "concatenated_data_with_four_options.jsonl"
    UTTERANCES = load_data(SRC_PATH)
    save_new_options(UTTERANCES, DST_PATH)
