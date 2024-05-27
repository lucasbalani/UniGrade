class Student:
    def __init__(self, id,  name, email, subjectId):
        self.id = id
        self.name = name
        self.email = email
        self.subjectId = subjectId

    def __str__(self):
        return f"{self.id} | {self.name} | {self.email}"