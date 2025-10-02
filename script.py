import math

x1 = float(input("Enter value for x1  "))
y1 = float(input("Enter value for y1  "))
x2 = float(input("Enter value for x2  "))
y2 = float(input("Enter value for y2  "))

sideA = x2 - x1
sideB = y2 - y1
sideC = math.sqrt(sideA*sideA+sideB*sideB)
print(f"The distance between the two points {(x1, y1)} and {(x2, y2)} is {sideC}")


