class StudentGrade:
    def __init__(self, id, studentId, subjectId, grade):
        self.id = id
        self.studentId = studentId
        self.subjectId = subjectId
        self.grade = grade

    def __str__(self):
        return f"{self.id} | {self.studentId}"