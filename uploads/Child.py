class Father:
    def f(self):
        print("Father")
class Mother:
    def m(self):
        print("Mother")
class Child(Father,Mother):
    pass
c=Child()
c.f()
c.m()
