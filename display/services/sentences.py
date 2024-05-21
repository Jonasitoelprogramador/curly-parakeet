class Sentence:
    def __init__(self, text, fragments, keyword_objects):
        # Define the URL for the Wikimedia REST API for the 'Caramel' page
        self.text = text
        self.fragments = fragments
        self.keyword_objects = keyword_objects


def sentence_constructor(text, fragments, keyword_objects):
    return Sentence(text, fragments, keyword_objects)
