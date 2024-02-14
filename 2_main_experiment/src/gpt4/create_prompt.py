import json
import random


def load_data(path: str):
    out = []
    with open(path, "r") as f_r:
        for line in f_r:
            instance: dict = json.loads(line)
            out.append(instance)
    return out


def create_prompt(
    one_conversation: list[str],
    current_turn_num: int,
    history_len: int,
):
    speaker_list = []
    utterance_list = []
    for i in range(history_len - 1, -1, -1):
        if current_turn_num - i < 0:
            continue
        else:
            speaker_list.append(one_conversation[current_turn_num - i]["speaker"])
            utterance_list.append(one_conversation[current_turn_num - i]["utterance"])

    instruction = "Two individuals are participating in a crowdsourcing task.\nThey have been assigned the roles of persuader (ER) and persuadee (EE), and they are discussing Save the Children (STC), a charitable organization.\nSTC is an NGO founded in the UK in 1919 to improve children's lives globally.\nER is attempting to convince EE to make a donation to STC.\nYour task is to determine the real intention of the last utterance based on the conversation.\n\n"

    script = ""
    for i in range(len(speaker_list)):
        script += "{}: {}\n".format(
            speaker_list[i],
            utterance_list[i],
        )
    options = [
        one_conversation[current_turn_num]["option_a"],
        one_conversation[current_turn_num]["option_b"],
        one_conversation[current_turn_num]["option_c"],
        one_conversation[current_turn_num]["option_d"],
    ]
    answer_idx = one_conversation[current_turn_num]["answer_idx"]

    question = "Q: Explain whether the last utterance clearly conveys the speaker's intention. If the last utterance clearly conveys the speaker's intent, what was that? If not, why did the speaker say it that way, and what intention was implied through the utterance? Based on that premise, which option among A through D is the most appropriate option that represents the intention of the last utterance? Answer Choices: "

    prompt = (
        instruction
        + script
        + "\n"
        + question
        + f"(A) {options[0]} "
        + f"(B) {options[1]} "
        + f"(C) {options[2]} "
        + f"(D) {options[3]}\n"
        + "A: Let's think step by step."
    )
    return script, prompt, options, answer_idx


def save_prompt(
    conversation_num: int, history_len: int, uttr_num: int, uttr, dst_path: str
):
    id_list = []
    current_pos = 0
    current_conv_id = None

    with open(dst_path, "w") as f_w:
        for i in range(conversation_num):
            for j in range(current_pos, uttr_num):
                if uttr[current_pos]["conversation_id"] not in id_list:
                    current_conv_id = uttr[current_pos]["conversation_id"]
                    id_list.append(current_conv_id)
                    break
                current_pos += 1
            specific_utterances = []
            while uttr[current_pos]["conversation_id"] == current_conv_id:
                specific_utterances.append(uttr[current_pos])
                current_pos += 1
                if current_pos == uttr_num:
                    break
            for j in range(len(specific_utterances)):
                script, prompt, temp, _ = create_prompt(
                    specific_utterances,
                    j,
                    history_len,
                )
                prompt_dict = {
                    "conversation_id": current_conv_id,
                    "turn_num": j,
                    "speaker": specific_utterances[j]["speaker"],
                    "utterance": specific_utterances[j]["utterance"],
                    "true_face": specific_utterances[j]["true_face"],
                    "description": specific_utterances[j]["description"],
                    "option_a": temp[0],
                    "option_b": temp[1],
                    "option_c": temp[2],
                    "option_d": temp[3],
                    "answer_idx": specific_utterances[j]["answer_idx"],
                    "answer_char": specific_utterances[j]["answer_char"],
                    "script": script,
                    "first_prompt": prompt,
                }
                json.dump(prompt_dict, f_w, ensure_ascii=False)
                f_w.write("\n")


if __name__ == "__main__":
    random.seed(20221018)
    TEST_UTTERANCE_NUM = 924
    TEST_CONVERSATION_NUM = 30
    HISTORY_LEN = 10000
    SRC_PATH = "../../data/concatenated_data_with_four_options.jsonl"
    DST_PATH = "prompt_for_gpt4.jsonl"
    UTTERANCES = load_data(SRC_PATH)
    save_prompt(
        TEST_CONVERSATION_NUM, HISTORY_LEN, TEST_UTTERANCE_NUM, UTTERANCES, DST_PATH
    )
