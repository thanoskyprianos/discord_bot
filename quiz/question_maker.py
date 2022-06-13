from dataclasses import dataclass, field
from random import shuffle
from unicodedata import category

from discord import Embed

from quiz.quiz_api import QuizData


def json_fix(string: str) -> str:
    '''Replaces json special characters with normal characters'''
    return string.replace('&quot;', '"').replace('&#039;', "'")


@dataclass
class Quiz:

    category: str = ''
    _correct: Embed = field(init=False, default_factory=Embed)
    _incorrect: Embed = field(init=False, default_factory=Embed)

    def __post_init__(self):

        self._quiz = QuizData(category=self.category)

        if self._quiz.get_response() == 0:
            self._question = json_fix(self._quiz.get_question())

            self._category = json_fix(self._quiz.get_category())

            self._difficulty = self._quiz.get_difficulty().capitalize()

            #list so we can combine it with the inccorect choices
            self._correct_answer = [json_fix(self._quiz.get_correct_answer())]

            self._incorrect_answers = list(
                map(json_fix, self._quiz.get_incorrect_answers()))

    def choice_creator(self):
        '''Creates the choices'''
        self._correct_incorrect = self._correct_answer + self._incorrect_answers

        if len(self._correct_incorrect) > 2:
            shuffle(self._correct_incorrect)  #only if multiple choice
        else:
            self._correct_incorrect.sort(
                reverse=True)  #else have always True-False order

        __true_false_emojis = ['✅', '❌']
        __number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']

        #dictionary creation for the embed and the emoji reactions
        if len(self._correct_incorrect) == 2:
            self._choices = dict(
                zip(__true_false_emojis, self._correct_incorrect))
        else:
            self._choices = dict(zip(__number_emojis, self._correct_incorrect))

    def template_creation(self):
        '''Creates and returns the question template'''

        self.choice_creator()

        self._question_template = Embed(title='Question',
                                        description=self._question)
        self._question_template.add_field(name='Category',
                                          value=self._category)
        self._question_template.add_field(name='Difficulty',
                                          value=self._difficulty)
        self._question_template.add_field(
            name='Choices',
            value='\n'.join(f'{k} {v}' for k, v in self._choices.items()))
        return self._question_template

    def correct_embed(self):
        '''Returns the correct answer embed'''
        self._correct.title = 'Correct!'
        self._correct.description = 'Good job!'
        return self._correct

    def incorrect_embed(self):
        '''Returns the incorrect answer embed'''
        self._incorrect.title = 'Incorrect!'
        self._incorrect.description = 'Try again!'
        self._incorrect.add_field(name='Correct Answer',
                                  value=self._correct_answer[0])
        return self._incorrect

    def get_choices(self):
        '''Returns the choices'''
        return self._choices

    def get_correct_answer(self):
        '''Returns the correct answer'''
        return self._correct_answer[0]

    def difficulty_modifier(self):
        if self._difficulty == 'Easy':
            return 1
        if self._difficulty == 'Medium':
            return 2
        return 3

    def get_response(self):
        '''Returns the response'''
        return self._quiz.get_response()
