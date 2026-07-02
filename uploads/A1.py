class A:
    def show(self):
        print("Class A")
class B(A):
    def showB(self):
        print("Class B")
class C(A):
    def showC(self):
        print("Class C")
class D(B,C):
    def showD(self):
        print("class D")
d=D()
d.showA()
d.showB()
d.showC()
d.showD()
