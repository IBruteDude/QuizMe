import Questions as qs
import Quiz as qz
import User as ur
from sys import stdin

questions = qs.QuestionRegister.getAll()


# print(questions)

if __name__ == '__main__':
    try:
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
    except Exception as e:
        print(f'[{e.__class__.__name__}]: {e}')



# UserRegister.add(User("Hamas", "Ketfom Israel"))
# UserRegister.saveAll()
# print(UserRegister.loadAll())
