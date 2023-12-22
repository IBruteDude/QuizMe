from enum import EnumType

class Answer:
    def check(self, other) -> bool:
        pass


class TFQ(Answer):
    def __init__(self, answer: bool) -> None:
        self.__answer = answer

    def check(self, other) -> bool:
        if (type(other) is str):
            other = other.strip()
            if (other == '1') or other.lower() == 'true':
                return self.__answer == True
            elif other == '2' or other.lower() == 'false':
                return self.__answer == False
            else:
                raise ValueError(f"invalid input {other}")
        assert type(self) is type(other)
        if self.__answer == other.__answer:
            return True
        return False


class SCQ(Answer):
    def __init__(self, totalchoices: int, answer: int):
        assert answer <= totalchoices and answer > 0
        self.__totalchoices = totalchoices
        self.__answer = answer

    def check(self, other) -> bool:
        if (type(other) is str):
            return self.__answer == int(other)
        assert type(self) is type(other)
        if  self.__answer == other.__answer and\
            self.__totalchoices == other.__totalchoices:
            return True
        return False


class MCQ(Answer):
    def __init__(self, totalchoices: int, answers: list[int]):
        assert all(answer < totalchoices and answer >= 0 for answer in answers)
        self.__totalchoices = totalchoices
        self.__answers = sorted(answers)

    def check(self, other) -> bool:
        if (type(other) is str):
            return self.__answers == sorted([int(choice) for choice in other.split()])
        assert type(self) is type(other)
        if  self.__answers == other.__answers and\
            self.__totalchoices == other.__totalchoices:
            return True
        return False
