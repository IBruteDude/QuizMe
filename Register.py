from json import load, dump

class Register:
    storagedir : str = "storagefiles/"
    storagefile : str = ""
    StoredType : type = None
    __loadedobjects : list[StoredType] = []

    @classmethod
    def add(cls, obj):
        cls.__loadedobjects.append(obj)

    @classmethod
    def saveAll(cls):
        dict_objects = [obj.__dict__ for obj in cls.__loadedobjects]
        with open(cls.storagedir + cls.storagefile, "w") as f:
            dump(dict_objects, f)

    @classmethod
    def loadAll(cls):
        with open(cls.storagedir + cls.storagefile, "r") as f:
            dicts = load(f)
        cls.__loadedobjects = [cls.StoredType(**dict) for dict in dicts]
        cls.StoredType.__no_of_instances = len(cls.__loadedobjects)

    @classmethod
    def getAll(cls) -> list[StoredType]:
        if cls.__loadedobjects == []:
            cls.loadAll()
        return cls.__loadedobjects
