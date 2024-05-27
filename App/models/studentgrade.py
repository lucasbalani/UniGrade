class StudentGrade:
    def __init__(self, id, studentId, subjectId, avaliationId, grade):
        self.id = id
        self.studentId = studentId
        self.subjectId = subjectId
        self.avaliationId = avaliationId
        self.grade = grade

    def __str__(self):
        return f"{self.id} | {self.studentId}"