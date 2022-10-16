'''
class Point():
    def __init__(self, a, b):
        self.x = a
        self.y = b

p = Point(2,8)
print(p.x)
print(p.y)

'''


class Flight():

    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []

    def add_Passengers(self, name):
        if not self.open_seats():
            return False
        self.passengers.append(name)
        return True

    def open_seats(self):
        return self.capacity - len(self.passengers)


flight = Flight(capacity=3)

people = ["Harry", "Ronn", "Hermoine", "Ginny"]
for person in people:
    if flight.add_Passengers(person):
        print(f"Added {person} to the fligth successfully.")
    else:
        print(f"No available seats {person}.")
