class A:
    def spam(self):
        print("A.spam")


class B(A):
    def spam(self):
        print("B.spam")
        super().spam()


class C(B):
    def spam(self):
        print("C.spam")
        super().spam()


print(C.__mro__)
c = C()
# walks class-by-class up the hierarchy
c.spam()
