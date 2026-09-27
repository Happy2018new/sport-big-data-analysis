class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def set_name(self, name):
        self.name = name
        return self

    def set_age(self, age):
        self.age = age
        return self

if __name__ =="__main__":
    p = Person("John", 30)
    p.set_name("bruce").set_age(29)
    # p.set_name("bruce")
    # p.set_age(29)
    print(p.name, p.age)


