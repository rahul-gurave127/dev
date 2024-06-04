NAME = ["Rahul", "Nilesh", "Abhijit", "Girish"]

AGES = [32, 34, 36, 38, 40]

first_name = NAME[0]
last_name = NAME[-1]

print("First name in the list is ", first_name)
print("Last name in the list is ", last_name)

print("first two:", NAME[:2])
print("last two:", NAME[2:])

print("Reverese List:", NAME[::-1])

print("Alternate Names:", NAME[::2])

print("Sum of Age:", sum(AGES))
print("Minimum Age:", min(AGES))
print("Maximum Age:", max(AGES))

NAME.append("Deepak")
print(NAME)
NAME.pop()
print(NAME)
NAME.insert(0, "VIKAS")
print(NAME)
NAME.remove("VIKAS")
print(NAME)

