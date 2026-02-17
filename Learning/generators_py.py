


class Generator:

    def __init__(self,first,last) -> None:
        self.first = first
        self.last = last
        self.current = first

    def __iter__(self):
        return self

    def __next__(self):

        if self.current > self.last:
            raise StopIteration
        val = self.current
        self.current +=1
        return val

gen = Generator(1,10)

for number in gen:
    print(number)
