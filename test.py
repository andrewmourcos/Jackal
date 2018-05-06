import os

file = open('lily.ly', 'w')

x = ["a", "b", "g"]

file.write('\\version "2.18.2" \n \language "english" \n \\relative{\n \clef treble\n')

for i in x:
	file.write(i)
	file.write("\n")

file.write("}")

file.close()

os.system("lilypond lily.ly")
os.system("open lily.pdf")



