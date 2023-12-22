from json import dump, load

categories = [{"id": 9, "name": "General Knowledge"}, {"id": 10, "name": "Entertainment: Books"}, {"id": 11, "name": "Entertainment: Film"},{"id":12,"name":"Entertainment: Music"},{"id":13,"name":"Entertainment: Musicals & Theatres"},{"id":14,"name":"Entertainment: Television"},{"id":15,"name":"Entertainment: Video Games"},{"id":16,"name":"Entertainment: Board Games"},{"id":17,"name":"Science & Nature"},{"id":18,"name":"Science: Computers"},{"id":19,"name":"Science: Mathematics"},{"id":20,"name":"Mythology"},{"id":21,"name":"Sports"},{"id":22,"name":"Geography"},{"id":23,"name":"History"},{"id":24,"name":"Politics"},{"id":25,"name":"Art"},{"id":26,"name":"Celebrities"}, {"id": 27, "name": "Animals"}, {"id": 28, "name": "Vehicles"}, {"id": 29, "name": "Entertainment: Comics"}, {"id": 30, "name": "Science: Gadgets"}, {"id": 31, "name": "Entertainment: Japanese Anime & Manga"}, {"id": 32, "name": "Entertainment: Cartoon & Animations"}]

def f(id):
	for dict in categories:
		if str(dict.get('id')) == str(id):
			return dict.get('name')

print(f(9))

topics = load(open('storagefiles/questionsbytopic.json'))

print(topics)
print((80 * '*' + '\n') * 5)

new_dict = {}

for key, value in topics.items():
    print(f"Key {key}: Value: {value}")
    new_dict[f(key)] = value

print(new_dict)

dump(new_dict, open('storagefiles/questionsbytopic1.json', '+w'))

