import pandas as pd
import re

fin = open("../../data/text_ro_new.txt")
text = fin.read()

pattern = r'<INST>(.*?)</INST><INP>(.*?)</INP><O>(.*?)</O>'
matches = re.findall(pattern, text, re.DOTALL)

matches_list = []
for match in matches:
    # print(f"INST: |{match[0].strip()}| INP: |{match[1].strip()}| OUT: |{match[2].strip()}|")
    row = (match[0].strip(), match[1].strip(), match[2].strip())
    matches_list.append(row)

prompt = '''<<SYS>> 
Sunteți un asistent util, respectuos și onest. Răspundeți întotdeauna cât mai util posibil, în siguranţă. Răspunsurile dvs. nu trebuie să includă niciun conţinut dăunător, lipsit de etică, rasist, sexist, toxic, periculos sau ilegal. Vă rugăm să vă asigurați că răspunsurile dvs. sunt imparţiale din punct de vedere social și de natură pozitivă. Dacă o întrebare nu are niciun sens sau nu este coerentă din punct de vedere factual, explicați de ce în loc să răspundeți la ceva incorect. Dacă nu știți răspunsul la o întrebare, vă rugăm să nu împărtășiți informaţii false. Trebuie sa răspundeți doar in limba română. Furnizați doar răspunsul și fără informaţii suplimentare.
<</SYS>>'''

columns = ['instruction', 'input', 'output']
df = pd.DataFrame(matches_list, columns=columns)
df = df.drop_duplicates()
df['text'] = df.apply(lambda row: f'[INST] {prompt}\n{row["instruction"]} {row["input"]}[/INST]\n{row["output"]}' 
                              if row['input'] != '' 
                              else f'[INST] {prompt}\n{row["instruction"]}[/INST]\n{row["output"]}', 
                     axis=1)
# print(df)
df.to_csv('../../data/text_ro.csv', index=False, encoding='utf-8')