class A:
    def show(self):
        print("A")
class B(A):
    pass
class C(B):
    pass
C().show()
