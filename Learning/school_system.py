# School System OOP Simulation

class Entity:
    creations = 0
    def __init__(self, name):
        self.name = name
        Entity.creations += 1
       
    def __str__(self):
        return f'{self.name} Base Class Entity'
   
    @classmethod
    def get_creations(cls):
        return cls.creations

    @staticmethod
    def welcome():
        """
        
        """
        print("Welcome to the School System Base Program!")


class Student(Entity):
    def __init__(self, student_id, name):
        self.student_id = student_id
        super().__init__(name)
        self.courses = {}  # course: grade

    def enroll(self, course):
        if course.name not in self.courses:
            self.courses[course.name] = None
            course.add_student(self)
            print(f"{self.name} enrolled in {course.name}")
        else:
            print(f"{self.name} is already enrolled in {course.name}")


    def assign_grade(self, course_name, grade):
        if course_name in self.courses:
            self.courses[course_name] = grade
        else:
            print(f"{self.name} is not enrolled in {course_name}")

    def get_report_card(self):
        print(f"\nReport Card for {self.name}")
        for course, grade in self.courses.items():
            status = grade if grade is not None else "Not Graded"
            print(f"{course}: {status}")

class Course(Entity):
    def __init__(self, name, instructor):
        super().__init__(name)
        self.instructor = instructor
        self.students = []

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)

    def list_students(self):
        print(f"\nStudents in {self.name}:")
        for s in self.students:
            print(f"- {s.name}")

class School(Entity):
    def __init__(self, name):
        super().__init__(name) 
        self.students = {}
        self.courses = {}

    def register_student(self, student_id, name):
        if student_id not in self.students:
            student = Student(student_id, name)
            self.students[student_id] = student
            print(f"Student {name} registered.")
        else:
            print(f"Student ID {student_id} is already registered.")

    def create_course(self, name, instructor):
        if name not in self.courses:
            course = Course(name, instructor)
            self.courses[name] = course
            print(f"Course {name} created.")
        else:
            print(f"Course {name} already exists.")

    def enroll_student_in_course(self, student_id, course_name):
        student = self.students.get(student_id)
        course = self.courses.get(course_name)

        if student and course:
            student.enroll(course)
        else:
            print("Invalid student or course.")

    def assign_grade(self, student_id, course_name, grade):
        student = self.students.get(student_id)
        if student:
            student.assign_grade(course_name, grade)
        else:
            print("Student not found.")

    def student_report_card(self, student_id):
        student = self.students.get(student_id)
        if student:
            student.get_report_card()
        else:
            print("Student not found.")



# === Test the System ===

school = School("Green Valley High")


school.welcome()
# Register students
school.register_student(1, "Alice")
school.register_student(2, "Bob")

# Create courses
school.create_course("Math", "Dr. Smith")
school.create_course("History", "Ms. Brown")

# Enroll students
school.enroll_student_in_course(1, "Math")
school.enroll_student_in_course(1, "History")
school.enroll_student_in_course(2, "Math")

# Assign grades
school.assign_grade(1, "Math", "A")
school.assign_grade(1, "History", "B")
school.assign_grade(2, "Math", "C")

# Print report cards
school.student_report_card(1)
school.student_report_card(2)

print("Creations: ",Entity.get_creations())