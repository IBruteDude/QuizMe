from datetime import time
from enum import EnumType
from html import unescape
from json import load
import random
from uuid import uuid4, UUID

from Register import Register
from Answer import Answer
from Questions import Question
from User import User

from time import time


class Grading(EnumType):
    EXCELLENT = (95, 100)
    GOOD = (80, 95)
    MEDIUM = (65, 80)
    BAD = (50, 65)
    FAIL = (0, 50)

    def __call__(cls, grade: int | float):
        if grade == 0:
            return Grading.FAIL
        for g in Grading:
            if (g[0] < grade and grade <= g[1]):
                return g
        raise ValueError("invalid grade")

class Quiz:
    __no_of_instances = 0
    def __init__(self, questions: list[Question], category: str | None =None):
        questions = load(open('storagefiles/questionsbytopic.json'))

        self.id = Quiz.__no_of_instances
        Quiz.__no_of_instances += 1
        self.questions = random.choices(questions, 20)
        self.duration = sum(question.time for question in questions)
        self.__iterator = iter(self.questions)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.__iterator)


class QuizRegister(Register):
    storagefile = 'quizes.json'
    StoredType = Register


class QuizSession:
    def __init__(self, quiz: Quiz, user: User):
        timing = time()
        duration = quiz.duration
        while time() - timing < duration:
            pass



# from flet import Text, Column, Row, FilledTonalButton, colors, UserControl
# class QuizInterface(User):
#     Text(value="TEXT")
#     Text(value="TEXT").value
#     Text(value="TEXT")
#     FilledTonalButton(on_click=lambda : 0, text="TEXT").disabled
#     Text.color = colors
#     # Text.update()

#     def __init__(self, quiz: Quiz):
#         super().__init__()

#     def build(self):
#         return Column(controls=[
#             Row(controls=[self.score_text]),
#             self.question_text,
#             Row(controls=[self.true_button, self.false_button])
#         ])

# import asyncio
# from time import sleep
# import threading as th

# THEME_COLOR = "#375362"

# class QuizInterface(UserControl):
#     def __init__(self, quiz: Quiz):
#         super().__init__()
#         self.timer = Text(value=f"00:00")
#         self.text1 = Text(value=f"Score: {"24"}")
#         self.text2 = Text(value="")

#         self.true_button = FilledTonalButton(on_click=self.right_answer, text="True")
#         self.false_button = FilledTonalButton(on_click=self.wrong_answer, text="False")

#     def build(self):
#         return Column(controls=[
#             Row(controls=[self.score_text]),
#             self.question_text,
#             Row(controls=[self.true_button, self.false_button])
#         ])

#     def get_next_question(self):
#         if self.quizBrain.still_has_questions():
#             q_text = self.quizBrain.next_question()
#             self.question_text.value = q_text
#         else:
#             self.question_text.value = "You're have reached the end of question"
#             self.true_button.disabled = True
#             self.false_button.disabled = True

#     def change_color(self, color):
#         self.question_text.color = color
#         self.question_text.update()

#     def correct_answer_hint(self, is_correct):
#         # use threading to run this function in a new thread and wait for it to finish
#         self.change_color(colors.GREEN if is_correct else colors.RED_300)
#         self.get_next_question()
