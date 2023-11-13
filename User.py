from uuid import uuid4, UUID
import json

class Topic:
    def __init__(self, name : str, questionids : list[UUID] = []):
        self.id = str(uuid4())
        self.name = name
        self.questionids = questionids

class User:
    topics = ["OOP", "CPP", "CSharp"]

    def __init__(self, userName, password, topics: list[Topic] = []):
        self.id = str(uuid4())
        self.userName = userName
        self.password = password
        self.topics = topics
        self.score = 0

    @classmethod
    def CreateUserInstanceForLogIn(cls, UserName, Password, Topic):
        with open("UserData.json", "r") as File:
            jsonData = json.load(File)
        score = 0

        for person in jsonData:
            x = 0
            for key, value in person.items():
                if key == "userName" and value == UserName:
                    x = 1

                if x == 1 and key == "questionTopics":

                    for _key, _value in value.items():

                        if _key == "OOP":
                            oop = _value

                        elif _key == "CPP":
                            cpp = _value

                        else:
                            csharp = _value

                if x == 1 and key == "score":
                    score = value

        return User(UserName, Password, oop, csharp, cpp, Topic)

    @classmethod
    def CreateUserInstanceForRegister(cls, UserName, Password, Topic):

        oop = 1
        csharp = 1
        cpp = 1
        score = 0

        return User(UserName, Password, oop, csharp, cpp, Topic)

    @classmethod
    def checkOnUserNameForLogin(cls, _userName):
        with open("UserData.json", "r") as File:
            jsonData = json.load(File)

        for person in jsonData:
            for key, value in person.items():
                if key == "userName" and value == _userName:
                    return True
        return False

    @classmethod
    def checkOnPasswordForLogin(cls, _userName, _password):
        with open("UserData.json", "r") as File:
            jsonData = json.load(File)

        for person in jsonData:
            x = 0
            for key, value in person.items():
                if key == "userName" and value == _userName:
                    x += 1
                if key == "password" and value == _password:
                    x += 1
                if x == 2:
                    return True
        return False

    @classmethod
    def checkOnUserNameForRegister(cls, _userName):
        with open("UserData.json", "r") as File:
            jsonData = json.load(File)

        for person in jsonData:
            for key, value in person.items():
                if key == "userName" and value == _userName:
                    return False
        return True


    def addUser(self):
        with open("UserData.json", "r") as File:
            jsonData = json.load(File)

        dic = {
            "id": len(jsonData) + 1,
            "userName": self.userName,
            "password": self.password
        }
        jsonData.append(dic)
        with open("UserData.json", "w") as File:
            json.dump(jsonData, File, indent=4)


class UserRegister:
    @classmethod
    def validName(str):
        pass

    @classmethod
    def save(User):
        pass

    @classmethod
    def checkPassword(User, password: str):
        pass
