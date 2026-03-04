with open("raw.txt", "r", encoding="utf-8") as file:
    content=file.read()

import re

#1
x=re.search(r"ab*", content)
if x:
    print("1. Match found")
else:
    print("1. No match found")

#2
x1=re.search(r"ab{2,3}", content)
if x1:
    print("2. Match found")
else:
    print("2. No match found")
print()

#3
x2=re.findall(r"[a-z]+(?:_[a-z]+)+", content)
print(f"3. {x2}")
print()

#4
x3=re.search(r"[A-Z][a-z]*", content)
print(4., x3.group())
print()

#5
x4=re.search(r"[a.*b]", content)
print(5., x4.group())
print()

#6
sstr="some_string ,hello"
x5=re.sub(r"[ ,\.]", ":", sstr)
print(x5)
print()

#7
sstr="some_snake_string"
x6=re.sub(r'_([a-z])', lambda x:x.group(1).upper(), sstr)
print(x6)

#8
s="AnotherExampleString"
x7=re.findall(r"[A-Z][a-z]*", s)
print(x7)

#9

x8=re.sub(r'([A-Z])', r' \1', s)
print(x8)

#10
cml="CamelStringHere"

x9=re.sub(r'([A-Z][a-z]*)', r'_\1', cml).lstrip('_')
print(x9)
