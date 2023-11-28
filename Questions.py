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
        self.id = str(uuid4())
        self.statement = kw["statement"]
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
