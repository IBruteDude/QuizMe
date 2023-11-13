from json import load, dump

class Register:
    storagedir : str = "storagefiles/"
    storagefile : str = ""
    StoredType : type = None
    __loadedobjects : list[StoredType] = []

    @classmethod
    def add(cls, obj : StoredType):
        cls.__loadedobjects.append(obj)

    @classmethod
    def saveAll(cls):
        dict_objects = [obj.__dict__ for obj in cls.__loadedobjects]
        with open(cls.storagefile, "w") as f:
            dump(dict_objects, f)

    @classmethod
    def loadAll(cls) -> None:
        with open(cls.storagedir + cls.storagefile, "r") as f:
            objs = load(f)
        cls.__loadedobjects = [cls.StoredType(**obj) for obj in objs]

    @classmethod
    def getAll(cls) -> list[StoredType]:
        if cls.__loadedobjects == []:
            cls.loadAll()
        return cls.__loadedobjects.copy()
