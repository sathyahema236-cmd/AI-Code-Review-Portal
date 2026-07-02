class Grandfather:
    def house(self):
        print("Grandfather owns a house")
class Father(Grandfather):
    def bike(self):
        print("Father owns a bike")
class Son(Father):
    def laptop(seelf):
        print("son owns a laptop")
s=Son()
s.house()
s.bike()
s.laptop()
