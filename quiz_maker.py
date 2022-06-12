import requests


class QuizMaker:

    def __init__(self) -> None:
        self.response = requests.get(
            'https://opentdb.com/api.php?amount=1&type=boolean')

    def get_response(self) -> str:
        return self.response.json()['response_code']

    def get_question(self) -> str:
        question = self.response.json()['results'][0]['question']
        return question.replace('&quot;', '"').replace('&#039;', "'")

    def get_answer(self) -> bool:
        return self.response.json()['results'][0]['correct_answer']

    def get_difficulty(self) -> str:
        return self.response.json()['results'][0]['difficulty'].capitalize()
