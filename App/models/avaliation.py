class Avaliation:
    def __init__(self, id, name, subjectId):
        self.id = id
        self.name = name
        self.subjectId = subjectId

    def __str__(self):
        return f"{self.id} | {self.name}"