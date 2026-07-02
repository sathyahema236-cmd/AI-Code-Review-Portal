class Department:
    def __init__(self,n): self.name=n
class College:
    def __init__(self,d): self.d=d
    def show(self): print(self.d.name)
College(Department('ECE')).show() 
