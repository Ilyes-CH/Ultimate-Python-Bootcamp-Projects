def multiply(x):
    def inner(y):
        return x*y
    return inner

double = multiply(2)
triple = multiply(3)

print(double(5))
print(triple(5))