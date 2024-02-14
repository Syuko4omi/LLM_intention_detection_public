import json
import random

random.seed(20221018)

# need not to use this script


def load_data(path: str):
    out = []
    with open(path, "r") as f_r:
        for line in f_r:
            instance: dict = json.loads(line)
            out.append(instance)
    return out


utterances = load_data("../Persuasion Face Act Prediction.jsonl")

persuasion_outcome = [
    -1 for _ in range(299)
]  # Whether persuasion was success(1), failed(0), or missing(-1) according to id
for line in utterances:
    if line["actual_donation"] == 1:
        persuasion_outcome[int(line["conversation_id"])] = 1
    else:
        persuasion_outcome[int(line["conversation_id"])] = 0

DONOR_CONV_IDS = [
    i for i, x in enumerate(persuasion_outcome) if x == 1
]  # "Donor": succeeded to persuade
NON_DONOR_CONV_IDS = [
    i for i, x in enumerate(persuasion_outcome) if x == 0
]  # "Non-donor": failed to persuade
dev_and_test_donor_conv_ids = random.sample(DONOR_CONV_IDS, 46)
train_donor_conv_ids = list(set(DONOR_CONV_IDS) - set(dev_and_test_donor_conv_ids))
dev_and_test_non_donor_conv_ids = random.sample(NON_DONOR_CONV_IDS, 13)
train_non_donor_conv_ids = list(
    set(NON_DONOR_CONV_IDS) - set(dev_and_test_non_donor_conv_ids)
)
dev_donor_conv_ids = random.sample(dev_and_test_donor_conv_ids, 23)
test_donor_conv_ids = list(set(dev_and_test_donor_conv_ids) - set(dev_donor_conv_ids))
dev_non_donor_conv_ids = random.sample(dev_and_test_non_donor_conv_ids, 6)
test_non_donor_conv_ids = list(
    set(dev_and_test_non_donor_conv_ids) - set(dev_non_donor_conv_ids)
)

train_conv_ids = train_donor_conv_ids + train_non_donor_conv_ids
dev_conv_ids = dev_donor_conv_ids + dev_non_donor_conv_ids
test_conv_ids = test_donor_conv_ids + test_non_donor_conv_ids

print(dev_conv_ids + test_conv_ids)

"""
with open("train.jsonl", "w") as f_w:
    for line in utterances:
        if int(line["conversation_id"]) in train_conv_ids:
            json.dump(line, f_w, ensure_ascii=False)
            f_w.write("\n")

with open("dev.jsonl", "w") as f_w:
    for line in utterances:
        if int(line["conversation_id"]) in dev_conv_ids:
            json.dump(line, f_w, ensure_ascii=False)
            f_w.write("\n")

with open("test.jsonl", "w") as f_w:
    for line in utterances:
        if int(line["conversation_id"]) in test_conv_ids:
            json.dump(line, f_w, ensure_ascii=False)
            f_w.write("\n")
"""


"""
# analysis for basic informations
persuasion_outcome = [-1 for i in range(299)]
utterances = load_data("Persuasion Face Act Prediction.jsonl")
max_num = 0
min_num = 0
for line in utterances:
    if line["actual_donation"] == 1:
        persuasion_outcome[int(line["conversation_id"])] = 1
    else:
        persuasion_outcome[int(line["conversation_id"])] = 0
    max_num = max(max_num, int(line["conversation_id"]))
    min_num = min(min_num, int(line["conversation_id"]))
print(min_num)  # minimum_conversation_id = 0
print(max_num)  # maximum_conversation_id = 298
print(persuasion_outcome.count(1))  # Donor conversation num = 231
print(persuasion_outcome.count(0))  # Non-donor conversation num = 65
print(persuasion_outcome.count(-1))  # missing conversation num = 3
print([i for i, x in enumerate(persuasion_outcome) if x == -1])  # missing conversation ids = [119, 179, 239]
"""
