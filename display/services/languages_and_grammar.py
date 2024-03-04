languages_list_content = [{'language': 'French', 'grammarPoints': [{'id': 1, 'point': "savoir VS conaitre"}]}, 
                        {'language': 'Spanish', 'grammarPoints': [{'id': 2, 'point': 'saber VS conocer'}, {'id': 3, 'point': 'por VS para'}]},
                         {'language': 'Portuguese', 'grammarPoints': [{'id': 5, 'point': "saber VS connhecer"}, {'id': 6, 'point': "por VS para"}]},
                           {'language': 'Italian', 'grammarPoints': [{'id': 8, 'point': "sappere VS conoscere"}, {'id': 9, 'point': 'di VS da'}]}]

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
                return language_item['language'], grammar_point['point']

    return None, None  # Return None if not found

def get_language_code(language_name):
    return language_codes.get(language_name, "Unknown")