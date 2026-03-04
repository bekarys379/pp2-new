with open("raw.txt", "r", encoding="utf-8") as file:
    content=file.read()

import re

#1
x=re.search(r"ab*", content)
print(x)