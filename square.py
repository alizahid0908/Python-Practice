import functions

for i in range(10):
    print(f"The sqaure of {i} is {functions.square(i)}")


from functions import square

for i in range(10):
    print(f"The sqaure of {i} is {square(i)}")
