print("Frist task:")
dgr=int(input("Input degree:"))
import math
rads=dgr*math.pi/180
print(f"Output radian:{rads}")
print()
print("Second task")
height=float(input("height:"))
Base1=float(input("Base 1:"))
Base2=float(input("Base 2:"))
res=((Base1+Base2)/2)*height
print(res)

print()
print("Third task:")
n=int(input("Input number of sides:"))
s=float(input("Input the length of a side:"))
area=(n*s**2)/(4*math.tan(math.pi/n))
print(f"The area of the polygon is:{area}")


print()
print("Fourth task")
lob=int(input("Length of base:"))
hei=int(input("Height of parralelogram:"))
parea=lob*hei
print(float(parea))
