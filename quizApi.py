import requests


class QuizData:

    def __init__(self) -> None:
        self.response = requests.get('https://opentdb.com/api.php?amount=1')

    def get_response(self) -> str:
        return self.response.json()['response_code']

    def get_question(self) -> str:
        question = self.response.json()['results'][0]['question']
        return question.replace('&quot;', '"').replace('&#039;', "'")

    def get_correct_answer(self):
        return self.response.json()['results'][0]['correct_answer']

    def get_incorrect_answers(self) -> list:
        return self.response.json()['results'][0]['incorrect_answers']

    def get_difficulty(self) -> str:
        return self.response.json()['results'][0]['difficulty'].capitalize()

    def get_category(self) -> str:
        return self.response.json()['results'][0]['category']
