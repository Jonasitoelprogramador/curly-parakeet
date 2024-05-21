from mlconjug3 import Conjugator


unwanted_es_tenses = ['Indicativo Pretérito imperfecto', 'Indicativo Pretérito pluscuamperfecto', 'Subjuntivo Pretérito imperfecto 1', 'Subjuntivo Pretérito pluscuamperfecto 1',
                    'Subjuntivo Futuro', 'Subjuntivo Futuro perfecto', 'Subjuntivo pretérito perfecto', 'Subjuntivo futuro perfecto', 'Subjuntivo futuro', 'Imperativo Afirmativo',
                    'Imperativo Afirmativo', 'Imperativo non', 'Condicional perfecto']

class ConjugationFormatter:
    def __init__(self, data, past_participle_name, expected_length, missing_person_names=None, specified_tenses=None,):
        self.data = data
        self.past_participle_name = past_participle_name
        self.expected_length = expected_length
        self.specified_tenses = specified_tenses
        self.missing_person_names = missing_person_names

    # Check if there are tuples with 'past_participle_name' as index [1], if so create a list of the tuples
    def check_tuple_x(self):
        self.participle_tuples = [x for x in self.data if x[1] == self.past_participle_name]
        if self.participle_tuples is None:
            raise ValueError(f"No tuple with {self.past_participle_name} found")

    # get all the past participles into one list
    def get_past_participles(self):
        self.past_participles = [x[-1] for x in self.participle_tuples]

    # Remove all tuples whose final index matches with tuple X's final index (but do not remove tuple X)
    # this is to ensure that we can easily index the correct tuple once we have the matches
    def remove_past_participle_matches(self):
        self.data = [x for x in self.data if x[-1] not in self.past_participles or x in self.participle_tuples]
    
    def check_length(self):
        # Check that all tuples have the given length
        for x in self.data:
            if len(x) != self.expected_length:
                raise ValueError(f"Tuple {x} has length {len(x)} != {self.expected_length}")
            
    def remove_specified_form(self, form):
        self.data = [x for x in self.data if x[-1] != form]

    def remove_specified_tenses(self):
        if self.specified_tenses:
            for specified_tense in self.specified_tenses:
                self.data = [x for x in self.data if x[1] != specified_tense]

    def get_irreg_length_tuples(self):
        if self.missing_person_names:
            missing_person_tuples = [x for x in self.data if x[1] in self.missing_person_names]
            return missing_person_tuples
        else:
            return None

    # If the only tuple with a length of less than given length is tuple X, remove it and create a new tuple with an empty string inserted at index [2]
    def create_new_tuple(self):
        missing_person_tuples = self.get_irreg_length_tuples()
        if missing_person_tuples:
            for t in missing_person_tuples:
                self.data.remove(t)
                new_tuple = t[:2] + ('',) + t[2:]
                self.data.append(new_tuple)


class FrenchConjugationFormatter(ConjugationFormatter):
    # "connaitre" only has one "N" for some reason
    def add_extra_n(self):
        corrected_conjugations = []
        for conjugation in self.data:
            # Reconstruct the tuple with corrected spelling in the last element
            corrected_tuple = tuple(
                elem.replace('con', 'conn') if isinstance(elem, str) else elem 
                for elem in conjugation
            )
            corrected_conjugations.append(corrected_tuple)
        self.data = corrected_conjugations


class PortugueseConjugationFormatter(ConjugationFormatter):
    # "conhecer" for some reason there have added extra "N" into it
    def remove_extra_n(self):
        corrected_conjugations = []
        for conjugation in self.data:
            # Reconstruct the tuple with corrected spelling in the last element
            corrected_tuple = tuple(
                elem.replace('connhe', 'conhe') if isinstance(elem, str) else elem 
                for elem in conjugation
            )
            corrected_conjugations.append(corrected_tuple)
        self.data = corrected_conjugations


class ItalianConjugationFormatter(ConjugationFormatter):
    def format_multiple_past_participles(self):
        self.remove_specified_form("conoscente")
        incorrect_format = False
        multiple_participles = [x for x in self.data if x[1] == self.past_participle_name]
        if len(multiple_participles) > 1:
            for p in multiple_participles:
                if p[2] == 0:
                    incorrect_format = True
        if incorrect_format:
            self.data = [x for x in self.data if x[1] != self.past_participle_name]
            for p in multiple_participles:
                new_tuple = (p[0], p[1], p[2]+1, p[3])
                self.data.append(new_tuple)


def get_formatter(data, language_code):
    # make the formatters into a dictionary and get them via indexing to above all this unecessary code
    if language_code == "es":
        spanish_conjugation_formatter = ConjugationFormatter(data, 'Participo Participo', 4, ['Participo Participo'], unwanted_es_tenses)
        return spanish_conjugation_formatter
    
    if language_code == "pt":
        portuguese_conjugation_formatter = PortugueseConjugationFormatter(data, 'Particípio Particípio', 4, ['Particípio Particípio'])
        return portuguese_conjugation_formatter
    
    if language_code == "it":
        italian_conjugation_formatter = ItalianConjugationFormatter(data, 'Participio Participio', 4)
        return italian_conjugation_formatter
    
    if language_code == "fr":
        french_conjugation_formatter = FrenchConjugationFormatter(data, 'Participe Passé', 4, ['Infinitif Présent', 'Participe Présent'])
        return french_conjugation_formatter


def get_conjugations(key_word, language_code):
        # initialize the conjugator
        conjugator = Conjugator(language=language_code)
        conjugations = conjugator.conjugate(key_word)
        return conjugations


def format_conjugations(conjugations, get_formatter, language_code):
        format_conjugation_object = get_formatter(conjugations, language_code)
        format_conjugation_object.check_tuple_x()
        format_conjugation_object.get_past_participles()
        format_conjugation_object.remove_past_participle_matches()
        format_conjugation_object.create_new_tuple()
        try: 
            format_conjugation_object.remove_specified_tenses()
        except AttributeError:
            pass
        try:
            format_conjugation_object.format_multiple_past_participles()
        except AttributeError:
            pass
        try:
            format_conjugation_object.remove_extra_n()
        except AttributeError:
            pass
        try:
            format_conjugation_object.add_extra_n()
        except AttributeError:
            pass
        format_conjugation_object.check_length()
        return format_conjugation_object.data


if __name__ == "__main__":
    #words_for_matching = GetAndFormatConjugations(['saber', 'conocer'], 'es', True, get_formatter).process()
    #print(words_for_matching)
    conjugator = Conjugator(language='es')
    verb = conjugator.conjugate('saber')
    
