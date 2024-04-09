class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def __setattr__(self, name, value):
        if name not in {"name", "shares", "price"}:
            raise AttributeError("No attribute %s" % name)
        super().__setattr__(name, value)


# would have to override the setattr dunder to use it


class BlueChip(Stock):
    pass


# can still technically set the attribute on the subclass if you want to
# by accessing the private dict
class Readonly:
    def __init__(self, obj):
        self.__dict__["_obj"] = obj

    def __setattr__(self, name, value):
        raise AttributeError("Can't set attribute")

    def __getattr__(self, name):
        return getattr(self._obj, name)


class Spam:
    def a(self):
        print("Spam.a")

    def b(self):
        print("Spam.b")


class MySpam:
    def __init__(self):
        self._spam = Spam()

    def a(self):
        print("MySpam.a")
        self._spam.a()

    def c(self):
        print("MySpam.c")

    # called as a fallback if the attribute is not found via std means
    def __getattr__(self, name):
        print("getattr: %s" % name)
        return getattr(self._spam, name)
