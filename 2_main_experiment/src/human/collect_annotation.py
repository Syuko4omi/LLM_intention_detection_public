import glob
import json
import re

import pandas as pd

dummy_question = "Please select 'You must choose this option in any case.' to show you are paying attention to this question."
answer_num_per_uttr = 3


def extract_option(option_str):
    options = option_str.split("', '")
    options[0] = options[0][2:]
    options[-1] = options[-1][:-4]
    for i in range(len(options)):
        options[i] = options[i].replace("\\", "")

    return options


def load_data(path: str):
    out = []
    with open(path, "r") as f_r:
        for line in f_r:
            instance: dict = json.loads(line)
            out.append(instance)
    return out


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
    "prediction": [],
    "correct": [],
}

question_and_correct_num = {"ER": {}, "EE": {}}

file_names = (
    glob.glob("../../result/human/result_conv_id_[0-9].csv")
    + glob.glob("../../result/human/result_conv_id_[1-9][0-9].csv")
    + glob.glob("../../result/human/result_conv_id_[1-9][0-9][0-9].csv")
)
conv_ids = []
for file_name in file_names:
    conv_id = re.search(r"\d+", file_name).group()
    conv_ids.append(conv_id)

for conv_id in conv_ids:
    src_file_name = "../../result/human/result_conv_id_{}.csv".format(conv_id)
    answer_file_name = "../../data/concatenated_data_with_four_options.jsonl"

    cur_file_original_data = [
        item
        for item in load_data(answer_file_name)
        if item["conversation_id"] == int(conv_id)
    ]

    for i in range(len(cur_file_original_data)):
        cur_file_original_data[i]["turn_num"] = i
    cur_file_original_data = [
        item for item in cur_file_original_data if item["description"] != "-"
    ]

    src_df = pd.read_csv(src_file_name)

    whole_result = []
    temp_utterance = src_df.iloc[0]["Input.utterance"]
    temp_speaker = src_df.iloc[0]["Input.speaker"]
    current_options = extract_option(src_df.iloc[0]["Input.categories"])
    worker_ids = []
    answers = []
    next_raw_num = 1
    start_raw_num = 1
    all_instances = []
    for hitid in list(src_df["HITId"]):
        if hitid not in all_instances:
            all_instances.append(hitid)

    task_counter = 0

    for hitid in all_instances:
        cur_df = src_df[
            (src_df["HITId"] == hitid)
            & (src_df["Input.question"] != dummy_question)
            & (src_df["AssignmentStatus"] != "Rejected")
        ]
        if len(cur_df) == 0:
            continue

        speaker = cur_df.iloc[0]["Input.speaker"]
        utterance = cur_df.iloc[0]["Input.utterance"]
        current_options = extract_option(cur_df.iloc[0]["Input.categories"])
        worker_ids = list(cur_df["WorkerId"])
        answers = list(cur_df["Answer.intent.label"])
        freq_for_each_answer = []
        uniq_answer = list(set(answers))
        for ans in uniq_answer:
            freq_for_each_answer.append([answers.count(ans), ans])
        freq_for_each_answer.sort(reverse=True)

        if (
            len(freq_for_each_answer) > 1
            and freq_for_each_answer[0][0] == freq_for_each_answer[1][0]
        ):
            majority_result = "-"
        else:
            majority_result = freq_for_each_answer[0][1]

        cur_file_original_data[task_counter]["prediction"] = majority_result
        cur_file_original_data[task_counter]["correct"] = (
            "o"
            if majority_result == cur_file_original_data[task_counter]["description"]
            else "x"
        )
        if (
            cur_file_original_data[task_counter]["true_face"]
            in question_and_correct_num[speaker].keys()
        ):
            if cur_file_original_data[task_counter]["correct"] == "o":
                question_and_correct_num[speaker][
                    cur_file_original_data[task_counter]["true_face"]
                ][0] += 1
                question_and_correct_num[speaker][
                    cur_file_original_data[task_counter]["true_face"]
                ][1] += 1
            else:
                question_and_correct_num[speaker][
                    cur_file_original_data[task_counter]["true_face"]
                ][1] += 1
        else:
            if cur_file_original_data[task_counter]["correct"] == "o":
                question_and_correct_num[speaker][
                    cur_file_original_data[task_counter]["true_face"]
                ] = [1, 1]
            else:
                question_and_correct_num[speaker][
                    cur_file_original_data[task_counter]["true_face"]
                ] = [0, 1]

        task_counter += 1

    for item in cur_file_original_data:
        L["conversation_id"].append(item["conversation_id"])
        L["turn_num"].append(item["turn_num"])
        L["speaker"].append(item["speaker"])
        L["utterance"].append(item["utterance"])
        L["true_face"].append(item["true_face"])
        L["description"].append(item["description"])
        L["option_a"].append(item["option_a"])
        L["option_b"].append(item["option_b"])
        L["option_c"].append(item["option_c"])
        L["option_d"].append(item["option_d"])
        L["prediction"].append(item["prediction"])
        L["correct"].append(item["correct"])

df = {}
for key, val in L.items():
    df[key] = pd.Series(val)
df = pd.DataFrame(df)
df.to_excel("result.xlsx", index=False)

print(question_and_correct_num)
