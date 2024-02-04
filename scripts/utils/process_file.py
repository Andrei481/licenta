import re


fin = open("../../../data/processed_file.txt")
text = fin.read()

text = re.sub(r'<INP>\s*</INP>\s*</INP>', '<INP> </INP>', text)
fout = open("text_ro_new.txt")
fout.write(text)
