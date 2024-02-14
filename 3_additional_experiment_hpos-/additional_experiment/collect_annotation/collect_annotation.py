import pandas as pd

# do this first
# take majority vote on the annotated result


def extract_option(option_str):
    options = option_str.split("', '")
    options[0] = options[0][2:]
    options[-1] = options[-1][:-4]
    for i in range(len(options)):
        options[i] = options[i].replace("\\", "")

    return options


for conv_id in range(10, 30):
    src_file_name = "../annotated_utterances/result_conv_id_{}_extra.csv".format(
        conv_id
    )
    processed_result_file_name = (
        "../annotated_utterances/result_conv_id_{}_extra_summary.csv".format(conv_id)
    )
    src_df = pd.read_csv(src_file_name)

    whole_result = []
    whole_conversation = src_df.iloc[0]["Input.conversation"]

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

    for hitid in all_instances:
        cur_df = src_df[
            (src_df["HITId"] == hitid) & (src_df["AssignmentStatus"] != "Rejected")
        ]
        if len(cur_df) == 0:
            continue

        whole_conversation = cur_df.iloc[0]["Input.conversation"]
        speaker = cur_df.iloc[0]["Input.speaker"]
        utterance = cur_df.iloc[0]["Input.utterance"]
        current_options = extract_option(cur_df.iloc[0]["Input.categories"])
        worker_ids = list(cur_df["WorkerId"])
        answers = list(cur_df["Answer.intent.label"])
        reasons = list(cur_df["Answer.reason"])
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

        temp = (
            [whole_conversation, speaker, utterance]
            + worker_ids
            + answers
            + reasons
            + [majority_result]
        )

        whole_result.append(temp)

    result_df = pd.DataFrame(
        data=whole_result,
        columns=[
            "conversation",
            "speaker",
            "utterance",
            "worker_1",
            "worker_2",
            "worker_3",
            "answer_1",
            "answer_2",
            "answer_3",
            "reason_1",
            "reason_2",
            "reason_3",
            "majority_result",
        ],
    )

    result_df.to_csv(processed_result_file_name, index=False)
