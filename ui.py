import asyncio
from time import sleep
from flet import Text, Column, Row, FilledTonalButton, colors, UserControl
import threading as th

THEME_COLOR = "#375362"


class QuizInterface(UserControl):
    def __init__(self, quiz):
        super().__init__()
        self.timer = Text(value=f"00:00")
        self.quizBrain = quiz
        self.score_text = Text(value=f"Score: 0")
        self.question_text = Text(value="something")

        self.ture_button = FilledTonalButton(on_click=self.right_answer, text="True")
        self.false_button = FilledTonalButton(on_click=self.wrong_answer, text="False")
        self.get_next_question()

    def build(self):
        return Column(controls=[
                Row(controls=[
                    self.score_text,

                ]), self.question_text,
                Row(
                    controls=
                    [self.ture_button, self.false_button]
                )])

    def get_next_question(self):
        if self.quizBrain.still_has_questions():
            q_text = self.quizBrain.next_question()
            self.question_text.value = q_text
        else:
            self.question_text.value = "You're have reached the end of question"
            self.ture_button.disabled = True
            self.false_button.disabled = True

    def change_color(self, color):
        pass

    def right_answer(self, e):
        is_correct = self.quizBrain.check_answer("True")
        self.score_text.value = f"Score: {self.quizBrain.score}"
        self.correct_answer_hint(is_correct=is_correct)

    def wrong_answer(self, e):
        is_correct = self.quizBrain.check_answer("False")
        self.correct_answer_hint(is_correct)

    def correct_answer_hint(self, is_correct):
        if is_correct:
            # use threading to run this function in a new thread and wait for it to finish
            th.Thread(target=self.change_color(colors.GREEN)).start()
            self.question_text.color = colors.GREEN
            self.get_next_question()
            self.question_text.update()
        else:
            th.Thread(target=self.change_color(colors.RED_300)).start()
            self.question_text.color = colors.RED_300
            self.get_next_question()
            self.question_text.update()
