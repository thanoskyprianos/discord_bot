from dataclasses import dataclass, field
from random import shuffle

from discord import Embed

from quizApi import QuizData


@dataclass
class GenericQuiz:

    quiz: QuizData = field(init=False, default_factory=QuizData)
    correct: Embed = field(init=False, default_factory=Embed)
    incorrect: Embed = field(init=False, default_factory=Embed)

    def __post_init__(self):
        if self.quiz.get_response() == 0:
            self.question = self.quiz.get_question()
            self.difficulty = self.quiz.get_difficulty()
            self.correct_answer = self.quiz.get_correct_answer()

            self.correct.title = 'Correct!'
            self.correct.description = 'Good job!'

            self.incorrect.title = 'Incorrect!'
            self.incorrect.description = 'Try again!'


@dataclass
class TrueFalseQuiz(GenericQuiz):

    question_template: Embed = field(init=False, default_factory=Embed)

    def __post_init__(self):
        super().__post_init__()

        self.question_template.title = 'Question'
        self.question_template.description = self.question
        self.question_template.add_field(name='Difficutly',
                                         value=self.difficulty)
