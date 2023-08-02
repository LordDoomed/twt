import json

def load_keywords_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    keywords = [word.strip() for word in content.split(',') if word.strip()]
    return keywords

def save_keywords_to_json(keywords, json_file_path):
    keywords_dict = {}
    for word in keywords:
        first_letter = word[0].lower()
        if first_letter not in keywords_dict:
            keywords_dict[first_letter] = []
        keywords_dict[first_letter].append(word)

    # Add empty arrays for letters without keywords
    for letter in map(chr, range(97, 123)):  # ASCII codes for 'a' to 'z'
        if letter not in keywords_dict:
            keywords_dict[letter] = []

    # Save the dictionary to JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(keywords_dict, json_file, ensure_ascii=False)

if __name__ == "__main__":
    keywords_file_path = "keyword.txt"
    json_file_path = "keyword.json"

    keywords = load_keywords_from_file(keywords_file_path)

    # No need to sort keywords here, as we want to preserve the original order

    save_keywords_to_json(keywords, json_file_path)
