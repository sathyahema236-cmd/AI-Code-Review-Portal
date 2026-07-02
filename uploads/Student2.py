class Student2:
    def display(self):
        print("student details")
class Teacher:
    def display(self):
        print("Teacher Details")
def show(obj):
    obj.display()
s=Student2()
t=Teacher()
show(s)
show(t)
