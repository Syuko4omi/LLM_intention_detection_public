import json

# do this second (after executing convert_annotated_data_to_jsonl.py)
# concatenate short utterances that are annotated with same intention description


def load_data(path: str):
    out = []
    with open(path, "r") as f_r:
        for line in f_r:
            instance: dict = json.loads(line)
            out.append(instance)
    return out


id_to_speaker = {0: "ER", 1: "EE"}
SRC_PATH = "../raw_data.jsonl"
DST_PATH = "../concatenated_data.jsonl"
UTTERANCES = load_data(SRC_PATH)

L = []
temp = UTTERANCES[0]
temp["utterance"] = temp["utterance"].strip()
ALPHABET_LIST = [chr(i) for i in range(ord("a"), ord("a") + 26)]

for i in range(1, len(UTTERANCES)):
    flag_1 = temp["conversation_id"] == UTTERANCES[i]["conversation_id"]
    flag_2 = temp["speaker"] == UTTERANCES[i]["speaker"]
    flag_3 = temp["true_face"] == UTTERANCES[i]["true_face"]
    flag_4 = temp["description"] == UTTERANCES[i]["description"]
    if (
        flag_1 == flag_2 == flag_3 == flag_4 == True
    ):  # meets the requirement for concatenation
        if (
            temp["utterance"][-1] in ALPHABET_LIST
        ):  # if there is no periods in the first utterance, insert a period
            temp["utterance"] += ". " + UTTERANCES[i]["utterance"].strip()
        else:  # if there is a period in the first utterance, just add space
            temp["utterance"] += " " + UTTERANCES[i]["utterance"].strip()
        if i == len(UTTERANCES) - 1:
            L.append(
                {
                    "conversation_id": temp["conversation_id"],
                    "speaker": temp["speaker"],
                    "utterance": temp["utterance"],
                    "true_face": temp["true_face"],
                    "description": temp["description"],
                }
            )
    else:
        L.append(
            {
                "conversation_id": temp["conversation_id"],
                "speaker": temp["speaker"],
                "utterance": temp["utterance"],
                "true_face": temp["true_face"],
                "description": temp["description"],
            }
        )
        temp = UTTERANCES[i]
        temp["utterance"] = temp["utterance"].strip()
        if i == len(UTTERANCES) - 1:
            L.append(
                {
                    "conversation_id": UTTERANCES[i]["conversation_id"],
                    "speaker": UTTERANCES[i]["speaker"],
                    "utterance": UTTERANCES[i]["utterance"],
                    "true_face": UTTERANCES[i]["true_face"],
                    "description": UTTERANCES[i]["description"],
                }
            )

with open(DST_PATH, "w") as f_w:
    for item in L:
        json.dump(item, f_w, ensure_ascii=False)
        f_w.write("\n")
