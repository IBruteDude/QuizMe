from datetime import time
from enum import EnumType
from uuid import uuid4, UUID

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
                 questions: dict[UUID, Grading] = {}):
        self.id: UUID = uuid4()
        self.duration: time = time.fromisoformat('T' + duration)
        self.questions: dict[UUID, Grading] = questions
