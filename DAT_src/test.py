class Parent():
    def __init__(self, a, b):
        print('a', a)
        print('b', b)

class Child(Parent):
    def __init__(self, c, d, *args, **kwargs):
        print('c', c)
        print('d', d)
        super(Child, self).__init__(*args, **kwargs)

test = Child(1,2,3,4)