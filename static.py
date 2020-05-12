class Example:
    name = "Example"

    @classmethod
    def static(asd):
        print("%s static() called" % asd.name)

class Offspring1(Example):
    name = "Offspring1"

class Offspring2(Example):
    name = "Offspring2"

    @classmethod
    def static(asd):
        print("%s static() called" % asd.name)

Example.static() # prints Example
Offspring1.static() # prints Example
Offspring2.static() # prints Offspring2
