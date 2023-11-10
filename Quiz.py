from enum import EnumType
from datetime import time
from uuid import uuid4, UUID

class Answer:
    def check(self, other) -> bool:
        pass

class TFQ(Answer):
    def __init__(self, answer: bool) -> None:
        self.__answer = answer

    def check(self, other) -> bool:
        assert type(self) is type(other)
        if self.__answer == other.__answer:
            return True
        return False

class SCQ(Answer):
    def __init__(self, totalchoices: int, answer: int) -> None:
        assert answer <= totalchoices
        self.__totalchoices = totalchoices
        self.__answer = answer

    def check(self, other) -> bool:
        assert type(self) is type(other)
        if  self.__answer == other.__answer and\
            self.__totalchoices == other.__totalchoices:
            return True
        return False

class MCQ(Answer):
    def __init__(self, totalchoices: int, answers: list[int]) -> None:
        assert all(answer <= totalchoices for answer in answers)
        self.__totalchoices = totalchoices
        self.__answers = sorted(answers)

    def check(self, other) -> bool:
        assert type(self) is type(other)
        if  self.__answers == other.__answers and\
            self.__totalchoices == other.__totalchoices:
            return True
        return False

class Grading(EnumType):
    EXCELLENT = (95, 100) # "excellent"
    GOOD = (80, 95) # "good"
    MEDIUM = (65, 80) # "meduim"
    BAD = (50, 65) # "bad"
    FAIL = (0, 50) # "fail"

    @classmethod
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
                 questions: dict[UUID, Grading] | None = {}) -> None:
        self.id: UUID = uuid4()
        self.duration: time = time.fromisoformat('T' + duration)
        self.questions: dict[UUID, Grading] = questions
