import math

print("y = a^x + b")
a = float(input("a: "))
#x = input("x: ")
b = int(input("b: "))
iterate = int(input("how many times: "))

for i in range(iterate):
  y = math.pow(a, i) + b
  print(y)