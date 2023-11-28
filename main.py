from Questions import QuestionRegister

from question_model import Question
from data import question_data
from Quiz import Quiz, QuizInterface
from flet import app, Page

question_bank = []
# question_data = QuestionRegister.loadAll()

for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)
    print(question_answer)


def main(page: Page):
    page.window_width = 400
    page.window_height = 600
    page.title = "Quiz"
    quiz = Quiz(question_bank)
    quiz_ui = QuizInterface(quiz)
    page.add(quiz_ui)


app(target=main)
