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


def post_req(index, model, uttr):
    if uttr[index]["true_face"] != "other":
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": uttr[index]["prompt"]}],
            temperature=0,
        )
        return response
    else:
        return {}


if __name__ == "__main__":
    openai.api_key = os.environ["OPENAI_API_KEY"]
    SRC_PATH = "../../data/prompt_for_gpt-4_succinct.jsonl"
    MODEL_NAME = "gpt-4-0613"
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
        DST_PATH = f"../../result/gpt-4_succinct/result_conv_no_{conv_id}.jsonl"
        UTTERANCES = load_specific_conversation(SRC_PATH, conv_id)
        UTTERANCE_NUM = len(UTTERANCES)
        for i in tqdm(range(UTTERANCE_NUM)):
            response = post_req(index=i, model=MODEL_NAME, uttr=UTTERANCES)
            UTTERANCES[i]["response"] = response
            time.sleep(2)

        with open(DST_PATH, "w") as f_w:
            for i in range(UTTERANCE_NUM):
                json.dump(UTTERANCES[i], f_w, ensure_ascii=False)
                f_w.write("\n")

        time.sleep(20)
