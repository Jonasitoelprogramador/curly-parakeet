class Keyword():
    def __init__(self, form, verb):
        self.form = form
        self.verb = verb


class ConjugationKeyword(Keyword):
    def __init__(self, form, verb, infinitive, mood, tense, person):
        super().__init__(form, verb)
        self.infinitive = infinitive
        self.mood = mood
        self.tense = tense
        self.person = person


class CreateKeywordObjects():
    """
    """
    def __init__(self, key_words, language_code, verb, get_formatter, get_conjugations_func, format_conjugations):
        self.key_words = key_words
        self.language_code = language_code
        self.verb = verb
        self.get_formatter = get_formatter
        self.conjugation_objects = []
        self.get_conjugations_func = get_conjugations_func
        self.format_conjugations = format_conjugations

    def keyword_constructor(self, form):
        return Keyword(form, False)
    
    def conjugation_keyword_constructor(self, form, infinitive, mood, tense, person):        
        return ConjugationKeyword(form, True, infinitive, mood, tense, person)
    
    def process(self):
        if not self.verb:
            keyword_objects = []
            for key_word in self.key_words:
                keyword_objects.append(self.keyword_constructor(key_word))
            return keyword_objects
        else:    
            for key_word in self.key_words:
                conjugations = self.get_conjugations_func(key_word, self.language_code).iterate()
                formatted_conjugations = self.format_conjugations(conjugations, self.get_formatter, self.language_code)
                

                temp_conj_objs = [self.conjugation_keyword_constructor(conjugation[-1], key_word, conjugation[0], conjugation[1], conjugation[2]) for conjugation in formatted_conjugations if conjugation[-1]]
                self.conjugation_objects.extend(temp_conj_objs)

            return self.conjugation_objects
    

class AddContrastiveForms():
    def __init__(self, matching_objects, keywords, language_code, get_conjugations_func, format_conjugations, get_formatter):
        self.matching_objects = matching_objects
        self.keywords = keywords
        self.language_code = language_code
        self.get_conjugations_func = get_conjugations_func
        self.format_conjugations = format_conjugations
        self.get_formatter = get_formatter
    
    def get_contrastive_forms(self):
        self.matching_objects_with_contrastive_forms = []
        for matching_object in self.matching_objects:    
            if isinstance(matching_object, ConjugationKeyword):
                matching_object = self.update_conjugation_keyword_object(matching_object)
            elif isinstance(matching_object, Keyword):
                matching_object = self.update_keyword_object(matching_object)
            else:
                raise TypeError("Object type not recognised")
            self.matching_objects_with_contrastive_forms.append(matching_object)
        return self.matching_objects_with_contrastive_forms

    def update_conjugation_keyword_object(self, matching_object):
        contrastive_infinitives = [constrastive_keyword for constrastive_keyword in self.keywords if constrastive_keyword != matching_object.infinitive]
        contrastive_forms = []
        # this gets the conjugations of the contrasting infinitive
        for contrastive_infinitive in contrastive_infinitives:
            contrastive_conjugations = self.get_conjugations_func(contrastive_infinitive, self.language_code)
            formatted_contrastive_conjugations = self.format_conjugations(contrastive_conjugations, self.get_formatter, self.language_code)
            try:
                mood, tense, person = matching_object.mood, matching_object.tense, matching_object.person
                contrastive_form = [t[-1] for t in formatted_contrastive_conjugations if (t[0], t[1], t[2]) == (mood, tense, person)][0]
            except TypeError:
                mood, tense = matching_object.mood, matching_object.tense
                contrastive_form = [t[-1] for t in formatted_contrastive_conjugations if (t[0], t[1]) == (mood, tense)][0]
            contrastive_forms.append(contrastive_form)
        matching_object.contrastive_forms = contrastive_forms
        return matching_object
    
    def update_keyword_object(self, matching_object):
        contrastive_forms = [form for form in self.keywords if form != matching_object.form]
        matching_object.contrastive_forms = contrastive_forms
        return matching_object