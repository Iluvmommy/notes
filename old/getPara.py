import re


file = open("/Users/anminhu/code/python/notes/text.txt")
reg = re.compile(r"\n+")
file = reg.split(file.read())

print(file)