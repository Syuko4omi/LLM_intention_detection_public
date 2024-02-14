import json
import random

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


def escape_apostrophe(text):
    temp = ""
    for chr in text:
        if chr == "'":
            temp += "\\" + "'"
        else:
            temp += chr
    return temp


def prepare_csv_row(conv_id, uttr_list):
    conversations = []
    speakers = []
    objective_utterances = []
    categories = []
    questions = []

    for_dummy = (
        []
    )  # ダミー問題の候補を入れる（後でそのうちのいくつかを選んでダミー問題とする）
    cur_conversation = ""

    for uttr in uttr_list:
        processed_utterance = preprocess_text_for_disp_in_html(str(uttr["utterance"]))
        if uttr["conversation_id"] == conv_id:
            if cur_conversation == "":
                cur_conversation += uttr["speaker"] + ":" + processed_utterance
            else:
                cur_conversation += "<%%>" + uttr["speaker"] + ":" + processed_utterance

            if uttr["description"] != "-":
                conversations.append(cur_conversation)
                speakers.append(uttr["speaker"])
                objective_utterances.append(processed_utterance)
                questions.append(
                    "What is the intention of the {}'s utterance: '{}' ?".format(
                        uttr["speaker"], processed_utterance
                    )
                )

                candidate_options = [
                    escape_apostrophe(uttr["option_a"]),
                    escape_apostrophe(uttr["option_b"]),
                    escape_apostrophe(uttr["option_c"]),
                    escape_apostrophe(uttr["option_d"]),
                ]
                options = "["
                for candidate_option in candidate_options:
                    options += "'" + candidate_option + "'" + ", "
                options += "]"
                categories.append(options)

                insert_id = random.choice(
                    [idx for idx in range(len(candidate_options) + 1)]
                )
                candidate_options = (
                    candidate_options[:insert_id]
                    + ["You must choose this option in any case."]
                    + candidate_options[insert_id:]
                )
                options = "["
                for candidate_option in candidate_options:
                    options += "'" + candidate_option + "'" + ", "
                options += "]"
                for_dummy.append(
                    {
                        "conversation": cur_conversation,
                        "speaker": uttr["speaker"],
                        "utterance": processed_utterance,
                        "options": options,
                        "question": "",
                    }
                )

    dummy_num = len(speakers) // 4
    dummy_inst = random.sample(for_dummy, dummy_num)
    for i in range(len(dummy_inst)):
        dummy_inst[i][
            "question"
        ] = "Please select 'You must choose this option in any case.' to show you are paying attention to this question."

    return (
        conversations,
        speakers,
        objective_utterances,
        categories,
        questions,
        dummy_inst,
    )
