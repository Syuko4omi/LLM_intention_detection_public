import glob
import json
import os
import re
import time

import openai
from openai import OpenAI
from tqdm import tqdm


def load_specific_conversation(path: str, conv_id: str):
    out = []
    with open(path, "r") as f_r:
        for line in f_r:
            instance: dict = json.loads(line)
            if instance["conversation_id"] == int(conv_id):
                out.append(instance)
    return out


def post_req_first(index, client, model_name, uttr):
    if uttr[index]["description"] != "-":
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": uttr[index]["first_prompt"]}],
            temperature=0,
        )
        time.sleep(2)
        return response.choices[0].message.content
    else:
        return ""


def post_req_second(client, model_name, second_request):
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": second_request}],
        temperature=0,
    )
    time.sleep(2)
    return response.choices[0].message.content


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
    SRC_PATH = "../../data/prompt_for_gpt4_and_chatgpt.jsonl"
    MODEL_NAME = "gpt-3.5-turbo-0613"
    # MODEL_NAME = "gpt-4-0613"
    openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    conv_ids = [
        "3",
        "47",
        "37",
        "69",
        "91",
        "42",
        "97",
        "99",
        "68",
        "53",
        "62",
        "35",
        "45",
        "214",
        "233",
        "199",
        "250",
        "117",
        "235",
        "130",
        "202",
        "217",
        "267",
        "198",
        "269",
        "191",
        "265",
        "244",
        "297",
        "187",
    ]

    for conv_id in conv_ids:
        DST_PATH = f"../../result/chatgpt/result_conv_no_{conv_id}.jsonl"
        # DST_PATH = f"../../result/gpt4/result_conv_no_{conv_id}.jsonl"
        UTTERANCES = load_specific_conversation(SRC_PATH, conv_id)
        UTTERANCE_NUM = len(UTTERANCES)
        for i in tqdm(range(UTTERANCE_NUM)):
            first_response = post_req_first(
                index=i, client=openai_client, model_name=MODEL_NAME, uttr=UTTERANCES
            )
            UTTERANCES[i]["first_response"] = first_response

            if UTTERANCES[i]["first_response"] != "":
                second_request = create_prompt_for_second_request(
                    UTTERANCES[i]["script"],
                    first_response,
                    [
                        UTTERANCES[i]["option_a"],
                        UTTERANCES[i]["option_b"],
                        UTTERANCES[i]["option_c"],
                        UTTERANCES[i]["option_d"],
                    ],
                )
                UTTERANCES[i]["second_prompt"] = second_request
                second_response = post_req_second(
                    client=openai_client,
                    model_name=MODEL_NAME,
                    second_request=second_request,
                )
                UTTERANCES[i]["second_response"] = second_response
            else:
                UTTERANCES[i]["second_prompt"] = ""
                UTTERANCES[i]["second_response"] = ""

        with open(DST_PATH, "w") as f_w:
            for i in range(UTTERANCE_NUM):
                json.dump(UTTERANCES[i], f_w, ensure_ascii=False)
                f_w.write("\n")

        time.sleep(20)
