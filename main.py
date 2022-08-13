def fib_gen(n):  # generator function to provide first n fib numbers
    #TODO
    pass


#test:
n = int(input("please enter a positive integer: n= "))
for num in fib_gen(n):
    print(num, end=",")
print()
print(f"sum of first {n} fib number is: {sum(x for x in fib_gen(n))}")
