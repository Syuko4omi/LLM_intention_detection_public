import glob
import json
import re


def load_data(path: str):
    out = []
    with open(path, "r") as f_r:
        for line in f_r:
            instance: dict = json.loads(line)
            out.append(instance)
    return out


def includes_alphabet(parts):
    temp = re.search(r"\w+", parts)
    return temp != None


def word_count_in_sentences(sentences):
    words = [part for part in sentences.split(" ") if includes_alphabet(part) is True]
    return len(words)


def count_num_of_question(dict_lists):
    counter = 0
    for item in dict_lists:
        if item["description"] != "-":
            counter += 1
    return counter


def average_word_num_per_uttr(dict_lists):
    word_num_per_uttr = []
    for item in dict_lists:
        word_num = word_count_in_sentences(item["utterance"])
        word_num_per_uttr.append(word_num)
    return sum(word_num_per_uttr) / len(word_num_per_uttr)


def average_word_num_per_option(dict_lists):
    question_num = count_num_of_question(dict_lists)
    option_num = question_num * 4
    counter = 0
    for item in dict_lists:
        if item["description"] != "-":
            counter += (
                word_count_in_sentences(item["option_a"])
                + word_count_in_sentences(item["option_b"])
                + word_count_in_sentences(item["option_c"])
                + word_count_in_sentences(item["option_d"])
            )
    return counter / option_num


src_file = "../concatenated_data_with_four_options.jsonl"
T = load_data(src_file)
print(count_num_of_question(T))
print(average_word_num_per_uttr(T))
print(average_word_num_per_option(T))
