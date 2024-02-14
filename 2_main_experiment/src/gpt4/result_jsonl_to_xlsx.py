import glob
import json
import re

import pandas as pd


def load_data(path: str):
    out = []
    with open(path, "r") as f_r:
        for line in f_r:
            instance: dict = json.loads(line)
            out.append(instance)
    return out


def convert_to_pd_format(responses_list, consider_other):
    L = {
        "conversation_id": [],
        "turn_num": [],
        "speaker": [],
        "utterance": [],
        "true_face": [],
        "description": [],
        "option_a": [],
        "option_b": [],
        "option_c": [],
        "option_d": [],
        "answer_idx": [],
        "answer_char": [],
        "first_prompt": [],
        "script": [],
        "first_response": [],
        "second_prompt": [],
        "second_response": [],
        "cleaned_response": [],
        "prediction": [],
        "correct": [],
        "convincing": [],
    }

    for item in responses_list:
        if not consider_other:
            if item["description"] == "-":
                continue
        for key in item.keys():
            L[key].append(item[key])
        cleaned_response = re.findall(r"A|B|C|D", item["second_response"])
        cleaned_response = "-" if cleaned_response == [] else cleaned_response[0]
        correct = "o" if cleaned_response == item["answer_char"] else "x"
        L["cleaned_response"].append(cleaned_response)
        L["correct"].append(correct)

    df = {}
    for key, val in L.items():
        df[key] = pd.Series(val)

    return df


if __name__ == "__main__":
    L = (
        glob.glob("../../data/annotated_test_data/result_conv_id_[0-9]_summary.csv")
        + glob.glob(
            "../../data/annotated_test_data/result_conv_id_[1-9][0-9]_summary.csv"
        )
        + glob.glob(
            "../../data/annotated_test_data/result_conv_id_[1-9][0-9][0-9]_summary.csv"
        )
    )

    conv_ids = []
    for file_name in L:
        conv_id = re.search(r"\d+", file_name).group()
        conv_ids.append(conv_id)
    all_response = []
    for conv_id in conv_ids:
        src_path = f"../../result/gpt4/result_conv_no_{conv_id}.jsonl"
        responses_list = load_data(src_path)
        for i in range(len(responses_list)):
            if responses_list[i]["description"] != "-":
                temp = responses_list[i]["first_response"]
                responses_list[i]["first_response"] = temp
                temp = responses_list[i]["second_response"]
                responses_list[i]["second_response"] = temp
            else:
                responses_list[i]["first_response"] = ""
                responses_list[i]["second_response"] = ""
        all_response.extend(responses_list)
    ret_df = convert_to_pd_format(all_response, consider_other=False)
    df = pd.DataFrame(ret_df)
    df.to_excel("result.xlsx", index=False)
