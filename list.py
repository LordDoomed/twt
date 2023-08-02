import json
import random
import os
from collections import OrderedDict

def load_keywords_from_json(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        keywords_dict = json.load(json_file, object_pairs_hook=OrderedDict)
    return keywords_dict

def load_used_keywords(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            used_keywords = set(line.split("\"")[1] for line in file if "\"" in line)
    except FileNotFoundError:
        used_keywords = set()
    return used_keywords

def generate_sentence_template():
    templates = [
        "Today is {}-day, the keyword is \"{}\".",
        "It's {}-day, and the keyword is \"{}\".",
        "Welcome to {}-day! The keyword for today is \"{}\".",
        "Let's celebrate {}-day with the keyword \"{}\".",
        "Happy {}-day! Today's keyword is \"{}\".",
        "{}-day is here, and the keyword is \"{}\".",
        "Time to create some art for {}-day, featuring the keyword \"{}\"!"
    ]
    return random.choice(templates)

def generate_sentences(keywords_dict, used_keywords, txt_file_path):
    sentences = []
    new_keywords = set()

    # Generate a list of all possible day letters from A to Z
    days = [chr(ord('A') + i) for i in range(26)]

    while True:
        new_keywords_found = False

        for day_letter in days:
            word_list = keywords_dict[day_letter.lower()]  # Use lowercase day_letter to get the word_list

            if word_list:  # Check if the word_list is not empty
                word = word_list.pop(0)  # Pop the first word from the word_list
                if word not in used_keywords:
                    new_keywords_found = True
                    new_keywords.add(word)
                    template = generate_sentence_template()
                    sentence = template.format(day_letter, word)  # Use day_letter (uppercase) here
                    sentences.append(sentence)
                    used_keywords.add(word)
                    # print(f"Processing line: {sentence}")

        # If no new keywords are found in this loop, exit the loop
        if not new_keywords_found:
            break

    return sentences, new_keywords

def save_sentences_to_file(sentences, file_path):
    with open(file_path, 'a', encoding='utf-8') as file:
        for sentence in sentences:
            file.write(sentence + '\n')

if __name__ == "__main__":
    try:
        json_file_path = "keyword.json"
        txt_file_path = "list.txt"

        if not os.path.exists(txt_file_path):
            with open(txt_file_path, 'w', encoding='utf-8'):
                pass

        keywords_dict = load_keywords_from_json(json_file_path)
        used_keywords = load_used_keywords(txt_file_path)

        sentences, new_keywords = generate_sentences(keywords_dict, used_keywords, txt_file_path)

        if new_keywords:
            print("Added new keywords:")
            for keyword in new_keywords:
                print(keyword)
            print(f"Total new keywords added: {len(new_keywords)}")
            save_sentences_to_file(sentences, txt_file_path)
        else:
            print("No new keywords added.")
    except Exception as e:
        print(f"An error occurred: {e}")
