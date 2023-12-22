from requests import get
from itertools import product
from json import dump
from random import randint
from html import unescape
from pprint import pp

################################################################################
# a useful functions for dealing with the different categories from the site
################################################################################

def category_to_topic(name=None):
    categories = [{"id": 9, "name": "General Knowledge"}, {"id": 10, "name": "Entertainment: Books"}, {"id": 11, "name": "Entertainment: Film"},{"id":12,"name":"Entertainment: Music"},{"id":13,"name":"Entertainment: Musicals & Theatres"},{"id":14,"name":"Entertainment: Television"},{"id":15,"name":"Entertainment: Video Games"},{"id":16,"name":"Entertainment: Board Games"},{"id":17,"name":"Science & Nature"},{"id":18,"name":"Science: Computers"},{"id":19,"name":"Science: Mathematics"},{"id":20,"name":"Mythology"},{"id":21,"name":"Sports"},{"id":22,"name":"Geography"},{"id":23,"name":"History"},{"id":24,"name":"Politics"},{"id":25,"name":"Art"},{"id":26,"name":"Celebrities"}, {"id": 27, "name": "Animals"}, {"id": 28, "name": "Vehicles"}, {"id": 29, "name": "Entertainment: Comics"}, {"id": 30, "name": "Science: Gadgets"}, {"id": 31, "name": "Entertainment: Japanese Anime & Manga"}, {"id": 32, "name": "Entertainment: Cartoon & Animations"}]
    if name is None:
        return [cat['id'] for cat in categories]
    else:
        for cat in categories:
            if cat['name'] == name:
                return cat['id']
        return -1

################################################################################
# download questions of all possible types and kinds as we want
################################################################################

question_data = []

number_of_questions = 10

question_combinations = product(
    ['boolean', 'multiple'],
    ['easy', 'medium', 'hard'],
    category_to_topic()
)

parameters = {
    "amount": number_of_questions,
    "type": "",
    "difficulty": "",
    "category": ""
}

for combination in question_combinations:
    # if combination in [('boolean', 'easy', 10),('boolean', 'easy', 11),('boolean', 'easy', 12),('boolean', 'easy', 13),('boolean', 'easy', 14),('boolean', 'easy', 16),('boolean', 'easy', 17),('boolean', 'easy', 18),('boolean', 'easy', 19),('boolean', 'easy', 20),('boolean', 'easy', 21),('boolean', 'easy', 22),('boolean', 'easy', 23),('boolean', 'easy', 25),('boolean', 'easy', 26),('boolean', 'easy', 27),('boolean', 'easy', 28),('boolean', 'easy', 29),('boolean', 'easy', 30),('boolean', 'easy', 31),('boolean', 'easy', 32),('boolean' , 'medium', 9),('boolean' , 'medium', 10),('boolean' , 'medium', 11),('boolean' , 'medium', 12),('boolean' , 'medium', 13),('boolean' , 'medium', 14),('boolean' , 'medium', 15),('boolean' , 'medium', 16),('boolean' , 'medium', 17),('boolean' , 'medium', 18),('boolean' , 'medium', 19),('boolean' , 'medium', 20),('boolean' , 'medium', 21),('boolean' , 'medium', 22),('boolean' , 'medium', 23),('boolean' , 'medium', 24),('boolean' , 'medium', 25),('boolean' , 'medium', 26),('boolean' , 'medium', 27),('boolean' , 'medium', 28),('boolean' , 'medium', 29),('boolean' , 'medium', 30),('boolean' , 'medium', 31),('boolean' , 'medium', 32),('boolean' , 'hard', 9),('boolean' , 'hard', 10),('boolean' , 'hard', 11),('boolean' , 'hard', 12),('boolean' , 'hard', 13),('boolean' , 'hard', 14),('boolean' , 'hard', 16),('boolean' , 'hard', 17),('boolean' , 'hard', 18),('boolean' , 'hard', 19),('boolean' , 'hard', 20),('boolean' , 'hard', 21),('boolean' , 'hard', 22),('boolean' , 'hard', 23),('boolean' , 'hard', 24),('boolean' , 'hard', 25),('boolean' , 'hard', 26),('boolean' , 'hard', 27),('boolean' , 'hard', 28),('boolean' , 'hard', 29),('boolean' , 'hard', 30),('boolean' , 'hard', 31),('boolean' , 'hard', 32),('multiple' , 'easy', 9),('multiple' , 'easy', 10),('multiple' , 'easy', 11),('multiple' , 'easy', 13),('multiple' , 'easy', 14),('multiple' , 'easy', 15),('multiple' , 'easy', 16),('multiple' , 'easy', 17),('multiple' , 'easy', 19),('multiple' , 'easy', 20),('multiple' , 'easy', 21),('multiple' , 'easy', 22),('multiple' , 'easy', 24),('multiple' , 'easy', 25),('multiple' , 'easy', 26),('multiple' , 'easy', 28),('multiple' , 'easy', 29),('multiple' , 'easy', 30),('multiple' , 'easy', 31),('multiple' , 'medium', 9),('multiple' , 'medium', 10),('multiple' , 'medium', 11),('multiple' , 'medium', 13),('multiple' , 'medium', 14),('multiple' , 'medium', 15),('multiple' , 'medium', 17),('multiple' , 'medium', 18),('multiple' , 'medium', 19),('multiple' , 'medium', 21),('multiple' , 'medium', 22),('multiple' , 'medium', 24),('multiple' , 'medium', 25),('multiple' , 'medium', 26),('multiple' , 'medium', 28),('multiple' , 'medium', 29),('multiple' , 'medium', 30),('multiple' , 'medium', 31),('multiple' , 'hard', 9),('multiple' , 'hard', 10),('multiple' , 'hard', 11),('multiple' , 'hard', 12),('multiple' , 'hard', 13),('multiple' , 'hard', 14),('multiple' , 'hard', 15),('multiple' , 'hard', 16),('multiple' , 'hard', 17),('multiple' , 'hard', 19),('multiple' , 'hard', 20),('multiple' , 'hard', 21),('multiple' , 'hard', 22),('multiple' , 'hard', 23),('multiple' , 'hard', 25),('multiple' , 'hard', 26),('multiple' , 'hard', 27),('multiple' , 'hard', 29),('multiple' , 'hard', 30),('multiple' , 'hard', 31),('multiple' , 'hard', 32)]:
    #     continue
    answertype, difficulty, category_id = combination
    parameters['type'] = answertype
    
    parameters['difficulty'] = difficulty
    parameters['category'] = category_id
    # print(parameters)
    downloaded_result = get(url="https://opentdb.com/api.php", params=parameters).json()
    if downloaded_result['response_code'] == 0:
        question_data += downloaded_result['results']
        # print(downloaded_result)
    else:
        # # print if no available questions with these parameters
        print(f'?amount={parameters['amount']}&type={parameters['type']}&difficulty={parameters['difficulty']}&category={parameters['category']}')

################################################################################
# convert the questions from their format to our format
# (questions are escaped with html url encoding, so we decode them)
################################################################################

# pp(question_data)

questions = []

for dc in question_data:
    ques = {}
    ques['id'] = len(questions)
    ques['type'] = "MCQ" if dc["type"] == "multiple" else "TFQ"
    ques['statement'] = unescape(dc["question"])
    ques['topic'] = category_to_topic(unescape(dc['category']))

    if dc['type'] == 'multiple':
        answers = dc['incorrect_answers']
        answers.insert(randint(0, len(answers)), dc['correct_answer'])
        ques['choices'] = [unescape(answer) for answer in answers]
        ques['correct_answer'] = [answers.index(dc['correct_answer'])]
    else:
        ques['choices'] = ['True', 'False']
        ques['correct_answer'] = True if dc['correct_answer'] == 'True' else False

    # time measured in seconds
    match dc['difficulty']:
        case 'easy':
            ques['score'] = randint(1, 2)
            ques['time'] = 60
        case 'medium':
            ques['score'] = randint(3, 6)
            ques['time'] = 90
        case 'hard':
            ques['score'] = randint(7, 10)
            ques['time'] = 120

    questions.append(ques)

################################################################################
# store the downloaded questions in the json file
################################################################################

dump(questions, open("storagefiles/questions.json", "w+"))

dic = {}
for key in [{"id": 9, "name": "General Knowledge"}, {"id": 10, "name": "Entertainment: Books"}, {"id": 11, "name": "Entertainment: Film"},{"id":12,"name":"Entertainment: Music"},{"id":13,"name":"Entertainment: Musicals & Theatres"},{"id":14,"name":"Entertainment: Television"},{"id":15,"name":"Entertainment: Video Games"},{"id":16,"name":"Entertainment: Board Games"},{"id":17,"name":"Science & Nature"},{"id":18,"name":"Science: Computers"},{"id":19,"name":"Science: Mathematics"},{"id":20,"name":"Mythology"},{"id":21,"name":"Sports"},{"id":22,"name":"Geography"},{"id":23,"name":"History"},{"id":24,"name":"Politics"},{"id":25,"name":"Art"},{"id":26,"name":"Celebrities"}, {"id": 27, "name": "Animals"}, {"id": 28, "name": "Vehicles"}, {"id": 29, "name": "Entertainment: Comics"}, {"id": 30, "name": "Science: Gadgets"}, {"id": 31, "name": "Entertainment: Japanese Anime & Manga"}, {"id": 32, "name": "Entertainment: Cartoon & Animations"}]:
    dic[str(key['id'])] = {'TFQ': [], 'MCQ': []}

for ques in questions:
    dic[str(ques['topic'])][ques['type']].append(ques)

# pp(dic)

dump(dic, open('storagefiles/questionsbytopic.json', '+w'))
