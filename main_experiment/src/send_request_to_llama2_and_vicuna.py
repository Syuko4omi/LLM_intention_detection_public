import json
import os
import time

import torch
import transformers
from transformers import AutoTokenizer


def load_specific_conversation(path: str, conv_id):
    out = []
    with open(path, "r", encoding="utf-8") as f_r:
        for line in f_r:
            instance: dict = json.loads(line)
            if instance["conversation_id"] == int(conv_id):
                out.append(instance)
    return out


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
    model = "meta-llama/Llama-2-70b-chat-hf"
    # model = "meta-llama/Llama-2-13b-chat-hf"
    # model = "meta-llama/Llama-2-7b-chat-hf"
    # model = "lmsys/vicuna-13b-v1.5"
    # model = "lmsys/vicuna-7b-v1.5"
    tokenizer = AutoTokenizer.from_pretrained(model)
    pipeline = transformers.pipeline(
        task="text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto",
    )

    SRC_PATH = "prompt_for_llama2_and_vicuna.jsonl"
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
        DST_PATH = f"result/result_conv_no_{conv_id}.jsonl"
        UTTERANCES = load_specific_conversation(SRC_PATH, conv_id)
        UTTERANCE_NUM = len(UTTERANCES)
        for i in range(UTTERANCE_NUM):
            if UTTERANCES[i]["description"] != "-":
                first_response = pipeline(
                    UTTERANCES[i]["first_prompt"],
                    do_sample=False,  # beam search
                    max_length=1024,
                    return_full_text=False,  # return only generated text
                    num_return_sequences=1,
                    eos_token_id=tokenizer.eos_token_id,
                )
                UTTERANCES[i]["first_response"] = first_response[0]
            else:
                UTTERANCES[i]["first_response"] = {}

            if UTTERANCES[i]["first_response"] != {}:
                second_request = create_prompt_for_second_request(
                    UTTERANCES[i]["script"],
                    UTTERANCES[i]["first_response"]["generated_text"],
                    [
                        UTTERANCES[i]["option_a"],
                        UTTERANCES[i]["option_b"],
                        UTTERANCES[i]["option_c"],
                        UTTERANCES[i]["option_d"],
                    ],
                )
                UTTERANCES[i]["second_prompt"] = second_request
                second_response = pipeline(
                    UTTERANCES[i]["second_prompt"],
                    do_sample=False,
                    max_length=1024,
                    return_full_text=False,
                    num_return_sequences=1,
                    eos_token_id=tokenizer.eos_token_id,
                )
                UTTERANCES[i]["second_response"] = second_response[0]
            else:
                UTTERANCES[i]["second_prompt"] = ""
                UTTERANCES[i]["second_response"] = {}

        with open(DST_PATH, "w", encoding="utf-8") as f_w:
            for i in range(UTTERANCE_NUM):
                json.dump(UTTERANCES[i], f_w, ensure_ascii=False)
                f_w.write("\n")
