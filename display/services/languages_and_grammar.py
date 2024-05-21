languages_list_content = [{'language': 'French', 'grammarPoints': [{'id': 1, 'point': "savoir VS conaitre", 'verb': True}]}, 
                        {'language': 'Spanish', 'grammarPoints': [{'id': 2, 'point': 'saber VS conocer', 'verb': True}, {'id': 3, 'point': 'por VS para', 'verb': False}]},
                         {'language': 'Portuguese', 'grammarPoints': [{'id': 5, 'point': "saber VS connhecer", 'verb': True}, {'id': 6, 'point': "por VS para", 'verb': False}]},
                           {'language': 'Italian', 'grammarPoints': [{'id': 8, 'point': "sapere VS conoscere", 'verb': True}, {'id': 9, 'point': 'di VS da', 'verb': False}]}]

language_codes = {
    "Spanish": "es",
    "French": "fr",
    "English": "en",
    "Portuguese": "pt",
    "Italian": "it"
    # Add more languages as needed
}

def find_language_and_point(id_number):
    for language_item in languages_list_content:
        for grammar_point in language_item['grammarPoints']:
            if grammar_point['id'] == id_number:
                return language_item['language'], grammar_point['point'], grammar_point['verb']

    return None, None  # Return None if not found

def get_language_code(language_name):
    return language_codes.get(language_name, "Unknown")