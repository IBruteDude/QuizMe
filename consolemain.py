import Questions as qs
import Quiz as qz
import User as ur
from sys import stdin


if __name__ == '__main__':
    questions = qs.QuestionRegister.getAll()
    for question in questions:
        assert type(question) is qs.Question
        print(f"Q: {question.statement}")
        for i, choice in enumerate(question.choices):
            print(f"\t{i + 1} - {choice}")
        print("answer: ", end="", flush=True)
        answer = stdin.readline()
        if question.answer.check(answer):
            print("Right answer")
        else:
            print("Wrong answer")
