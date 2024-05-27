import tkinter as tk
import psycopg2
from tkinter import Button
from tkinter import messagebox
from tkinter import ttk
from models.student import Student
from models.subject import Subject
from models.avaliation import Avaliation
from models.studentgrade import StudentGrade
from psycopg2 import sql

class StudentManagementApp:
    def __init__(self, master):
        self._connectDatabase()
        
        self.master = master
        self.master.title("UniGrade")
        
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        widthScreen = 50

        # Titulo
        self.mainTitle = tk.Label(self.frame, text="Bem-vindo ao UniGrade! Selecione uma opção abaixo:")
        self.mainTitle.pack()
        
        # Botão para o caso de uso "Gerenciar Alunos"
        self.btnManageStudents = tk.Button(self.frame, text="Gerenciar Alunos", command=self.manageStudents, width=widthScreen)
        self.btnManageStudents.pack()

        # Botão para o caso de uso "Gerenciar Disciplinas"
        self.btnManageSubjects = tk.Button(self.frame, text="Gerenciar Disciplinas", command=self.manageSubjects, width=widthScreen)
        self.btnManageSubjects.pack()
        
        # Botão para o caso de uso "Gerenciar Avaliações"
        self.btnManageAvaliations = tk.Button(self.frame, text="Gerenciar Avaliações", command=self.manageAvaliations, width=widthScreen)
        self.btnManageAvaliations.pack()
        
        # Botão para o caso de uso "Registrar Nota"
        self.btnRegisterGrade = tk.Button(self.frame, text="Registrar Nota", command=self.studentGradeForm, width=widthScreen)
        self.btnRegisterGrade.pack()

        # Botão para sair da aplicação
        self.btnQuit = tk.Button(self.frame, text="Sair", command=self.master.quit, width=widthScreen)
        self.btnQuit.pack()

    def registerGrade(self):
        screenRegisterGrade = tk.Toplevel(self.master)
        screenRegisterGrade.title("UniGrade - Registrar Nota")

        self.mainTitle = tk.Label(self.frame, text="Bem-vindo ao UniGrade! Selecione uma opção abaixo:")
        
        # Button Save
        screenRegisterGrade.btnSave = tk.Button(screenRegisterGrade, text="Salvar", command=self.manageSubjects, width=50, height=2)
        screenRegisterGrade.btnSave.pack()
        
        self.master.title("UniGrade - Cadastrar Nota")
        
    def viewGrades(self):
        # Lógica para consultar notas
        messagebox.showinfo("Consultar Notas", "Funcionalidade de Consultar Notas")

    def manageStudents(self):
        screenRegisterStudents = tk.Toplevel(self.master)
        screenRegisterStudents.title("UniGrade - Registrar Alunos")
    
        self._createTitle(screenRegisterStudents, "Gerencie seus alunos", "Adicionar", self.studentForm)

        students = self._get_students()
        
        def removeStudent(self, student, listBox):
            id = student.split("|")[0].strip()
            
            self.cursor.execute("DELETE FROM Students Where Id = %s", (id,))
            self.connection.commit()
            
            # Reseta lista
            listBox.delete(0, tk.END)
            students = self._get_students()
            for student in students:
                listBox.insert(tk.END, str(student))
                
        def updateStudent(self, studentSelected, listBox):
            id = int(studentSelected.split("|")[0].strip())
            
            studentFinded = None
            
            for student in students:   
                if student.id == id:       
                    studentFinded = student
                    break
            
            self.studentForm(studentFinded)
        
        self._createListBox(screenRegisterStudents, students, removeStudent, updateStudent)
    
    def studentForm(self, studentEdit=None):
        
        def createStudent(name, email, subjectSelected):
            subjectId = subjectSelected.split("-")[0].strip()
            
            self.cursor.execute("INSERT INTO students (name, email, gradeId) VALUES (%s, %s, %s)", (name, email, subjectId))
            self.connection.commit()

            messagebox.showinfo("Sucesso", "Estudante cadastrado com sucesso!")
        
        def updateStudent(id, name, email, subjectSelected):
            subjectId = subjectSelected.split("|")[0].strip()
            
            self.cursor.execute("UPDATE students SET name = %s, email = %s, gradeId = %s WHERE id = %s", (name, email, subjectId, id))
            self.connection.commit()

            messagebox.showinfo("Sucesso", "Estudante atualizado com sucesso!")
            
        width = 100
        screenStudentForm = tk.Toplevel(self.master)
        screenStudentForm.title("UniGrade - Registrar Alunos")
        
        self._createTitle(screenStudentForm, "Novo Aluno", "", lambda: print(""))
        self._divider(screenStudentForm)
        
        subjects = self._get_subjects()

        # Name
        label_nome = tk.Label(screenStudentForm, text="Nome:", width=width)
        label_nome.pack()
        nameEntry = tk.Entry(screenStudentForm, width=width)
        nameEntry.pack()
        
        if studentEdit is not None:
            nameEntry.insert(tk.END, studentEdit.name)

        # Email
        label_email = tk.Label(screenStudentForm, text="Email:", width=width)
        label_email.pack()
        emailEntry = tk.Entry(screenStudentForm, width=width)
        emailEntry.pack()
        
        if studentEdit is not None:
            emailEntry.insert(tk.END, studentEdit.email)

        # Subject
        subjectLabel = tk.Label(screenStudentForm, text="Grade:", width=width)
        subjectLabel.pack()
        
        formattedSubjects = [f"{subject.id} | {subject.name}" for subject in subjects]
        comboboxSelectSubject = ttk.Combobox(screenStudentForm, values=formattedSubjects, width=width)
        comboboxSelectSubject.pack()
        
        if studentEdit is not None:
            subjectFinded = self._find_subject(studentEdit.subjectId)
            
            if subjectFinded:
                comboboxSelectSubject.set(subjectFinded.name)
            
        # Submit
        button_submit = tk.Button(screenStudentForm, 
                                  text="Salvar", 
                                  width=50,
                                  command=lambda: createStudent(nameEntry.get(),
                                                                emailEntry.get(),
                                                                comboboxSelectSubject.get()) if studentEdit is None 
                                          else updateStudent(studentEdit.id,
                                                             nameEntry.get(), 
                                                             emailEntry.get(), 
                                                             comboboxSelectSubject.get()))
        button_submit.pack(pady=5)
    
    def manageSubjects(self):
        screenRegisterSubjects = tk.Toplevel(self.master)
        screenRegisterSubjects.title("UniGrade - Registrar Alunos")
    
        self._createTitle(screenRegisterSubjects, "Gerencie suas disciplinas", "Adicionar", self.subjectForm)
        
        def updateSubject(self, subjectSelected, listBox):
            id = int(subjectSelected.split("|")[0].strip())
            
            subjectFinded = self._find_subject(id)
            
            self.subjectForm(subjectFinded)
            
        subjects = self._get_subjects()
        subjectList = [f"{subject.id} | {subject.name}" for subject in subjects]
        
        self._createListBox(screenRegisterSubjects, subjectList, lambda: print(""), updateSubject, useRemoveButton=False)
        
    def subjectForm(self, subjectEdit=None):
        def createSubject(self, name):
            self.cursor.execute("INSERT INTO subjects (name) VALUES (%s)", (name,))
            self.connection.commit()

            messagebox.showinfo("Sucesso", "Matéria cadastrada com sucesso!")
        
        def updateSubject(id, name):
            self.cursor.execute("UPDATE subjects SET name = %s WHERE id = %s", (name, id))
            self.connection.commit()

            messagebox.showinfo("Sucesso", "Matéria atualizada com sucesso!")
            
        width = 100
        screenSubjectForm = tk.Toplevel(self.master)
        screenSubjectForm.title("UniGrade - Registrar Alunos")
        
        self._createTitle(screenSubjectForm, "Matéria", "", lambda: print(""))
        self._divider(screenSubjectForm)
        
        # Nome
        labelName = tk.Label(screenSubjectForm, text="Nome:", width=width)
        labelName.pack()
        nameEntry = tk.Entry(screenSubjectForm, width=width)
        nameEntry.pack()
        
        if subjectEdit is not None:
            nameEntry.insert(tk.END, subjectEdit.name)
        
        # Submit
        button_submit = tk.Button(screenSubjectForm, 
                                  text="Salvar", 
                                  width=50,
                                  command=lambda: createSubject(nameEntry.get()) if subjectEdit is None else updateSubject(subjectEdit.id, nameEntry.get()))
        
        button_submit.pack(pady=5)
        
    def manageAvaliations(self):
        screenRegisterAvaliations = tk.Toplevel(self.master)
        screenRegisterAvaliations.title("UniGrade - Registrar Avaliaçoes")
    
        self._createTitle(screenRegisterAvaliations, "Gerencie suas avaliações", "Adicionar", self.avaliationForm)
        
        def updateAvaliation(self, avaliationSelected, listBox):
            id = int(avaliationSelected.split("|")[0].strip())
            
            avaliationFinded = self._find_avaliation(id)
            
            self.avaliationForm(avaliationFinded)
            
        avaliations = self._get_avaliations()
        avaliationList = [f"{avaliation.id} | {avaliation.name}" for avaliation in avaliations]
        
        self._createListBox(screenRegisterAvaliations, avaliationList, lambda: print(""), updateAvaliation, useRemoveButton=False)
    
    def avaliationForm(self, avaliationEdit=None):
        def createAvaliation(name, subjectId):
            self.cursor.execute("INSERT INTO avaliations (name, subjectId) VALUES (%s, %s)", (name, subjectId))
            self.connection.commit()

            messagebox.showinfo("Sucesso", "Avaliação cadastrada com sucesso!")
        
        def updateAvaliation(id, name, subjectId):
            self.cursor.execute("UPDATE avaliations SET name = %s, subjectId = %s WHERE id = %s", (name, subjectId, id))
            self.connection.commit()

            messagebox.showinfo("Sucesso", "Avaliação atualizada com sucesso!")
            
        width = 100
        screenAvaliationForm = tk.Toplevel(self.master)
        screenAvaliationForm.title("UniGrade - Registrar Avaliações")
        
        self._createTitle(screenAvaliationForm, "Avaliação", "", lambda: print(""))
        self._divider(screenAvaliationForm)
        
        # Nome
        labelName = tk.Label(screenAvaliationForm, text="Nome:", width=width)
        labelName.pack()
        nameEntry = tk.Entry(screenAvaliationForm, width=width)
        nameEntry.pack()
        
        if avaliationEdit is not None:
            nameEntry.insert(tk.END, avaliationEdit.name)
            
        # Subject
        subjects = self._get_subjects()

        subjectLabel = tk.Label(screenAvaliationForm, text="Disciplina:", width=width)
        subjectLabel.pack()
        
        formattedSubjects = [f"{subject.id} | {subject.name}" for subject in subjects]
        comboboxSelectSubject = ttk.Combobox(screenAvaliationForm, values=formattedSubjects, width=width)
        comboboxSelectSubject.pack()
        
        if avaliationEdit is not None:
            subjectFinded = self._find_subject(avaliationEdit.subjectId)
            
            if subjectFinded:
                comboboxSelectSubject.set(str(subjectFinded))
        
        # Submit
        button_submit = tk.Button(screenAvaliationForm, 
                                  text="Salvar", 
                                  width=50,
                                  command=lambda: createAvaliation(nameEntry.get(), comboboxSelectSubject.get().split("|")[0].strip()) if avaliationEdit is None 
                                                  else updateAvaliation(avaliationEdit.id, nameEntry.get(), comboboxSelectSubject.get().split("|")[0].strip()))
        
        button_submit.pack(pady=5)
    
    def studentGradeForm(self):
        def createStudentGrade(studentId, subjectId, grade):
            self.cursor.execute("INSERT INTO studentGrades (studentId, subjectId, grade) VALUES (%s, %s, %s)", (studentId, subjectId, grade))
            self.connection.commit()

            messagebox.showinfo("Sucesso", "Nota cadastrada com sucesso!")
            
        width = 100
        screenStudentGradeForm = tk.Toplevel(self.master)
        screenStudentGradeForm.title("UniGrade - Registrar Avaliações")
        
        self._createTitle(screenStudentGradeForm, "Registrar Nota", "", lambda: print(""))
        self._divider(screenStudentGradeForm)
        
        # Students
        students = self._get_students()

        studentLabel = tk.Label(screenStudentGradeForm, text="Aluno:", width=width)
        studentLabel.pack()
        
        formattedStudents = [f"{student.id} | {student.name}" for student in students]
        comboboxSelectStudent = ttk.Combobox(screenStudentGradeForm, values=formattedStudents, width=width)
        comboboxSelectStudent.pack()
        
        # Subject
        subjects = self._get_subjects()

        subjectLabel = tk.Label(screenStudentGradeForm, text="Disciplina:", width=width)
        subjectLabel.pack()
        
        formattedSubjects = [f"{subject.id} | {subject.name}" for subject in subjects]
        comboboxSelectSubject = ttk.Combobox(screenStudentGradeForm, values=formattedSubjects, width=width)
        comboboxSelectSubject.pack()
        
        # Grade
        labelGrade = tk.Label(screenStudentGradeForm, text="Nota:", width=width)
        labelGrade.pack()
        gradeEntry = tk.Entry(screenStudentGradeForm, width=width)
        gradeEntry.pack()
        
        # Submit
        button_submit = tk.Button(screenStudentGradeForm, 
                                  text="Salvar", 
                                  width=50,
                                  command=lambda: createStudentGrade(comboboxSelectStudent.get().split("|")[0].strip(), 
                                                                     comboboxSelectSubject.get().split("|")[0].strip(), 
                                                                     gradeEntry.get()))
        
        button_submit.pack(pady=5)
    
    #region Private Methods
    def _createTitle(self, topLevelReference, title, textButton, callBack):
         # Título
        titleFrame = tk.Frame(topLevelReference)
        titleFrame.pack(fill=tk.X, pady=10)

        registerTitle = tk.Label(titleFrame, text=title, font=("Helvetica", 16))
        registerTitle.pack(side=tk.LEFT, padx=10)

        if textButton.strip():
            addButton = tk.Button(titleFrame, text=textButton, command=callBack)
            addButton.pack(side=tk.RIGHT, padx=10)
        
    def _createListBox(self, topLevelReference, data, removeCallBack, editCallBack, useRemoveButton=True):
        
        def removeSelected():
            selectedIndex = listbox.curselection()
            
            if selectedIndex:
                selectedItem = listbox.get(selectedIndex)
                removeCallBack(self, selectedItem, listbox)
        
        def updateSelected():
            selectedIndex = listbox.curselection()
            
            if selectedIndex:
                selectedItem = listbox.get(selectedIndex)
                
                editCallBack(self, selectedItem, listbox)
                
        
                
        listbox = tk.Listbox(topLevelReference, width=50)
        listbox.pack()

        for item in data:
            listbox.insert(tk.END, str(item))
            
        # Remover
        if useRemoveButton:
            removeButton = tk.Button(topLevelReference, text="Remover", command=removeSelected)
            removeButton.pack(side=tk.RIGHT, padx=2, pady=5)
        
        # Editar
        editButton = tk.Button(topLevelReference, text="Editar", command=updateSelected)
        editButton.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def _divider(self, topLevelReference):
        divider = tk.Frame(topLevelReference, height=2, bd=1, relief=tk.SUNKEN)
        divider.pack(fill=tk.X, padx=5, pady=5)
    
    def _connectDatabase(self):
        self.connection = psycopg2.connect(
            dbname="postgres",
            user="admin",
            password="123456",
            host="localhost",
            port="5432"
        )
        
        self.cursor = self.connection.cursor()
        
        # Criar tabela de estudantes
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            gradeId INTEGER
        );
        ''')
        
        # Criar tabela de grades
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Subjects (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
        ''')
        
        # Criar tabela de avaliações
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Avaliations (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            subjectId INTEGER
        )
        ''')
        
        # Criar tabela de notas dos alunos
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS StudentGrades (
            id SERIAL PRIMARY KEY,
            studentId INTEGER,
            subjectId INTEGER,
            grade INTEGER
        )
        ''')
        
        self.connection.commit()
    
    def _get_students(self):
        self.cursor.execute("SELECT * FROM students")
        rows = self.cursor.fetchall()
        return [Student(row[0], row[1], row[2], row[3]) for row in rows]
    
    def _get_subjects(self):
        self.cursor.execute("SELECT * FROM subjects")
        rows = self.cursor.fetchall()
        
        return [Subject(row[0], row[1]) for row in rows]
    
    def _get_avaliations(self):
        self.cursor.execute("SELECT * FROM avaliations")
        rows = self.cursor.fetchall()
        
        return [Avaliation(row[0], row[1], row[2]) for row in rows]
    
    def _get_students_grades(self):
        self.cursor.execute("SELECT * FROM StudentGrades")
        rows = self.cursor.fetchall()
        
        return [StudentGrade(row[0], row[1], row[2], row[3]) for row in rows]
    
    def _find_subject(self, subjectId):
        subjectFinded = None
        
        subjects = self._get_subjects()
        
        for subject in subjects:   
            if subject.id == subjectId:       
                subjectFinded = subject
                break
            
        return subjectFinded
    
    def _find_avaliation(self, avaliationId):
        avaliationFinded = None
        
        avaliations = self._get_avaliations()
        
        for avaliation in avaliations:   
            if avaliation.id == avaliationId:       
                avaliationFinded = avaliation
                break
            
        return avaliationFinded
    
    def _find_studentGrade(self, studentGradeId):
        studentGradeFinded = None
        
        studentGrades = self._get_students_grades()
        
        for studentGrade in studentGrades:   
            if studentGrade.id == studentGradeId:       
                studentGradeFinded = studentGrade
                break
            
        return studentGradeFinded
    #endregion

def main():
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()