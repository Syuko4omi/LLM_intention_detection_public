import json
import os
import time

import openai
from tqdm import tqdm


def load_specific_conversation(path: str, conv_id: int):
    out = []
    with open(path, "r") as f_r:
        for line in f_r:
            instance: dict = json.loads(line)
            if instance["conversation_id"] == conv_id:
                out.append(instance)
    return out


def post_req_first(index, model, uttr):
    if uttr[index]["true_face"] != "other":
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": uttr[index]["first_prompt"]}],
            temperature=0,
        )
        time.sleep(2)
        return response
    else:
        return {}


def post_req_second(model, second_request):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": second_request}],
        temperature=0,
    )
    time.sleep(2)
    return response


def create_prompt_for_second_request(script, response_of_the_first_prompt, options):
    instruction = "Two individuals are participating in a crowdsourcing task.\nThey have been assigned the roles of persuader (ER) and persuadee (EE), and they are discussing Save the Children (STC), a charitable organization.\nSTC is an NGO founded in the UK in 1919 to improve children's lives globally.\nER is attempting to convince EE to make a donation to STC.\nYour task is to determine the real intention of the last utterance based on the conversation.\n\n"
    question = "Q: Explain whether the last utterance clearly conveys the speaker's intention. If the last utterance clearly conveys the speaker's intent, what was that? If not, why did the speaker say it that way, and what intention was implied through the utterance? Based on that premise, which option among A through D is the most appropriate option that represents the intention of the last utterance? Answer Choices: "
    prompt_for_second_request = (
        instruction
        + script
        + "\n"
        + question
        + f"(A) {options[0]} "
        + f"(B) {options[1]} "
        + f"(C) {options[2]} "
        + f"(D) {options[3]}\n"
        + "A: Let's think step by step."
        + response_of_the_first_prompt
        + "\n"
        + "Therefore, among A through D, the answer is"
    )
    return prompt_for_second_request


if __name__ == "__main__":
    openai.api_key = os.environ["OPENAI_API_KEY"]
    SRC_PATH = "../../data/prompt_for_chatgpt_detailed.jsonl"
    MODEL_NAME = "gpt-3.5-turbo-0613"
    conv_ids = [
        132,
        136,
        152,
        154,
        161,
        177,
        60,
        63,
        66,
        70,
        74,
        86,
        108,
        263,
        266,
        275,
        280,
        286,
        287,
        189,
        200,
        201,
        221,
        12,
        15,
        16,
        22,
        23,
        56,
    ]

    for conv_id in conv_ids:
        DST_PATH = f"../../result/chatgpt_detailed/result_conv_no_{conv_id}.jsonl"
        UTTERANCES = load_specific_conversation(SRC_PATH, conv_id)
        UTTERANCE_NUM = len(UTTERANCES)
        for i in tqdm(range(UTTERANCE_NUM)):
            first_response = post_req_first(index=i, model=MODEL_NAME, uttr=UTTERANCES)
            UTTERANCES[i]["first_response"] = first_response

            if UTTERANCES[i]["first_response"] != {}:
                second_request = create_prompt_for_second_request(
                    UTTERANCES[i]["script"],
                    UTTERANCES[i]["first_response"]["choices"][0]["message"]["content"],
                    [
                        UTTERANCES[i]["option_a"],
                        UTTERANCES[i]["option_b"],
                        UTTERANCES[i]["option_c"],
                        UTTERANCES[i]["option_d"],
                    ],
                )
                UTTERANCES[i]["second_prompt"] = second_request
                second_response = post_req_second(
                    model=MODEL_NAME, second_request=second_request
                )
                UTTERANCES[i]["second_response"] = second_response
            else:
                UTTERANCES[i]["second_prompt"] = ""
                UTTERANCES[i]["second_response"] = {}

        with open(DST_PATH, "w", encoding='utf-8') as f_w:
            for i in range(UTTERANCE_NUM):
                json.dump(UTTERANCES[i], f_w, ensure_ascii=False)
                f_w.write("\n")

        time.sleep(20)
