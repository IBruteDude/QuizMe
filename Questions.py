from uuid import uuid4
from Answer import TFQ, MCQ, SCQ
from Register import Register

# id: uuid
# statement: str
# answer: Answer
# *assets: list[Asset]
# points: Scoring
# duration: time


class Question:
    def __init__(self, *args, **kw):
        self.id = uuid4()
        self.statement = kw["name"]
        self.choices = kw.get("choices")
        self.score = kw["score"]
        self.time = kw["time"]
        Ty = kw["type"]
        match (Ty):
            case "TFQ": self.answer = TFQ(kw["correct_answer"])
            case "SCQ": self.answer = SCQ(len(self.choices), kw["correct_answer"])
            case "MCQ": self.answer = MCQ(len(self.choices), kw["correct_answer"])

    def check(self, user_answer):
        return self.answer.check(user_answer)

class QuestionRegister(Register):
    storagefile = "questions.json"
    StoredType = Question

#     def still_questions(self):
#         return self.count_questions < len(self.List)

#     def display_choices(self):
#         all_answers = self.List[self.count_questions]["answer"]["all_answers"]
#         for ans in all_answers:
#             print(ans, end=' ')

#     def display_questions(self):
#         statement = self.List[self.count_questions]["statement"]
#         print(f"{self.count_questions+1}- {statement}")
#         self.display_choices()
#         answer_user = str(input("\n    Enter Your Choice: "))
#         correct_answer = self.List[self.count_questions]["answer"]["correct_answer"]
#         self.count_questions += 1
#         if self.check(answer_user, correct_answer):
#             print("Accepted")
#             self.score += 1
#         else:
#             print("Wrong Answer")


# user = Question(questions)
# while user.still_questions():
#     user.display_questions()
