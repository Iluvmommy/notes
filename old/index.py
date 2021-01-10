import re

file = open("/Users/anminhu/code/python/notes/old/text.txt")
result = file.read().split('. ')
print(result)

i = 0
notes = open('/Users/anminhu/code/python/notes/old/notes.txt', "w")
answers = open('/Users/anminhu/code/python/notes/old/answers.txt', "w")
while i < len(result)-1:
  if i % 2 == 0:
    notes.write(result[i] + "\n \n")
  else:
    answers.write("1. " + result[i] + " " + result[i+1] + "\n")
  i += 3

file.close()
notes.close()
answers.close()
print('Done')
