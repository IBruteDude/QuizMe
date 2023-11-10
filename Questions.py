from data import questions

class Question:
    def __init__(self, ques):
        self.score = 0
        self.count_questions = 0
        self.List = ques

    def still_questions(self):
        return self.count_questions < len(self.List)

    def check(self, answer_user, correct_answer):
        if answer_user == correct_answer:
            return True
        return False

    def display_choices(self):
        all_answers = self.List[self.count_questions]["answer"]["all_answers"]
        for ans in all_answers:
            print(ans, end=' ')

    def display_questions(self):
        statement = self.List[self.count_questions]["statement"]
        print(f"{self.count_questions+1}- {statement}")
        self.display_choices()
        answer_user = str(input("\n    Enter Your Choice: "))
        correct_answer = self.List[self.count_questions]["answer"]["correct_answer"]
        self.count_questions += 1
        if self.check(answer_user, correct_answer):
            print("Accepted")
            self.score += 1
        else:
            print("Wrong Answer")


user = Question(questions)
while user.still_questions():
    user.display_questions()
