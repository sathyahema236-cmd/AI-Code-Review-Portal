class Teacher1:
    def __init__(self,n):self.name=n
class Student:
    def study(self,t):
        print("studying with",t.name)
Teacher1=Teacher1("anita")
Student().study(Teacher1)
