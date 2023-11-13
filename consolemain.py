from json import load

import Questions as qs
import Quiz as qz
import User as ur


if __name__ == '__main__':
    questions = qs.QuestionRegister.getAll()
    for question in questions:
        assert type(question) is qs.Question        
