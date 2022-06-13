from dataclasses import dataclass, field
from enum import Enum, auto

import requests


class Category(Enum):
    '''Enum for the categories'''
    GENERAL = 9
    BOOKS = auto()
    FILM = auto()
    MUSIC = auto()
    MNT = auto()
    TV = auto()
    VIDEO = auto()
    BOARD = auto()
    SCIENCE = auto()
    PC = auto()
    MATH = auto()
    MYTHOLOGY = auto()
    SPORTS = auto()
    GEOGRAPHY = auto()
    HISTORY = auto()
    POLITICS = auto()
    ART = auto()
    CELEB = auto()
    ANIMALS = auto()
    CARS = auto()
    COMICS = auto()
    GADGETS = auto()
    JP = auto()
    CARTOONS = auto()


@dataclass
class QuizData:

    category: str = field(default='')
    link: str = f'https://opentdb.com/api.php?amount=1'

    def __post_init__(self):
        if self.category != '':
            self.link += f'&category={Category[self.category].value}'
        self.response = requests.get(self.link)

    def get_response(self) -> str:
        return self.response.json()['response_code']

    def get_question(self) -> str:
        question = self.response.json()['results'][0]['question']
        return question.replace('&quot;', '"').replace('&#039;', "'")

    def get_correct_answer(self) -> str:
        return self.response.json()['results'][0]['correct_answer']

    def get_incorrect_answers(self) -> list:
        return self.response.json()['results'][0]['incorrect_answers']

    def get_difficulty(self) -> str:
        return self.response.json()['results'][0]['difficulty'].capitalize()

    def get_category(self) -> str:
        return self.response.json()['results'][0]['category']
