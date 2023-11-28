from datetime import time
from enum import EnumType
from uuid import uuid4, UUID
from html import unescape


from Answer import Answer
from Questions import Question


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
    def __init__(self,
                 duration: str,
                 questions: list[Question]):
        self.id = uuid4()
        self.duration = time.fromisoformat('T' + duration)
        self.questions = questions
    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = unescape(self.current_question.statement)
        return f"Q.{self.question_number}: {q_text}"
        # user_answer = input(f"Q.{self.question_number}: {q_text} (True/False): ")
        # self.check_answer(user_answer)

    def check_answer(self, user_answer: Answer) -> bool:
        if self.current_question.answer.check(user_answer):
            self.score += 1
            return True
        else:
            return False

# import asyncio
# from time import sleep
# from flet import Text, Column, Row, FilledTonalButton, colors, UserControl
# from Quiz import Quiz
# import threading as th
# from Answer import Answer, MCQ, SCQ, TFQ

# THEME_COLOR = "#375362"

# class QuizInterface(UserControl):
#     def __init__(self, quiz: Quiz):
#         super().__init__()
#         self.timer = Text(value=f"00:00")
#         self.quizBrain = quiz
#         self.score_text = Text(value=f"Score: 0")
#         self.question_text = Text(value="")

#         self.true_button = FilledTonalButton(on_click=self.right_answer, text="True")
#         self.false_button = FilledTonalButton(on_click=self.wrong_answer, text="False")
#         self.get_next_question()

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
