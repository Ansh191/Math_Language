class Symbol:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.attributes = set()

    def setAttribute(self, attribute):
        self.attributes.add(attribute)

    def getAttribute(self, attribute):
        if attribute in self.attributes:
            return attribute
        else:
            return None


class Function(Symbol):
    def __call__(self, *args, **kwargs):
        return self.value(*args)


class Attribute:
    def __init__(self, type):
        """
        initialize Attribute
        :type type: int
        0 = Protected
        1 = Locked
        2 = ReadProtected
        3 = Constant
        """
        self.type = type

    def __repr__(self):
        if self.type == 0:
            return "Protected"
        elif self.type == 1:
            return "Locked"
        elif self.type == 2:
            return "ReadProtected"
        elif self.type == 3:
            return "Constant"


Attributes = [Attribute(0), Attribute(1), Attribute(2), Attribute(3)]
