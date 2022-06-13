from dataclasses import dataclass, field
from random import shuffle

from discord import Embed
from matplotlib.pyplot import title

from quizApi import QuizData


@dataclass
class Quiz:

    quiz: QuizData = field(init=False, default_factory=QuizData)
    correct: Embed = field(init=False, default_factory=Embed)
    incorrect: Embed = field(init=False, default_factory=Embed)

    def __post_init__(self):
        if self.quiz.get_response() == 0:
            self.question = self.quiz.get_question()
            self.category = self.quiz.get_category()
            self.difficulty = self.quiz.get_difficulty()
            self.correct_answer = [self.quiz.get_correct_answer()]
            self.incorrect_answers = self.quiz.get_incorrect_answers()

            self.correct.title = 'Correct!'
            self.correct.description = 'Good job!'

            self.incorrect.title = 'Incorrect!'
            self.incorrect.description = 'Try again!'

            self.cor_inc = self.correct_answer + self.incorrect_answers
            shuffle(self.cor_inc)

            true_false_emojis = ['✅', '❌']
            number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']

            if len(self.cor_inc) == 2:
                self.choices = dict(zip(true_false_emojis, self.cor_inc))
            else:
                self.choices = dict(zip(number_emojis, self.cor_inc))

            self.question_template = Embed(title='Question',
                                           description=self.question)
            self.question_template.add_field(name='Category',
                                             value=self.category)
            self.question_template.add_field(name='Difficulty',
                                             value=self.difficulty)
            self.question_template.add_field(
                name='Choices',
                value='\n'.join(f'{k} {v}' for k, v in self.choices.items()))
