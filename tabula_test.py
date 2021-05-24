import os
import re
import tabula
import pandas as pd

files = os.listdir('./Bulletins')

# Liste des prénoms des élèves
students = []
for filename in files:
  str = re.search("(\w+)-Trimestre", filename)
  students.append(str.group(1))

def get_datastream_from_file(path):
  df = tabula.read_pdf(
      path,
      pages=1,
      stream=False,
      lattice=True,
      guess=True,
      )[0]

  df = df.drop([df.columns[0], df.columns[6]], axis=1)
  df = df.dropna()

  df.columns = ['Moyenne élève', 'Moyenne classe', "min", "max", "Appréciation"]
  df = df.replace('\r',' ', regex=True)

  return df

print(files[0:2])
files_subset = files[0:2]
file1 = files_subset[0]
file2 = files_subset[1]

df1 = get_datastream_from_file(file1)
df2 = get_datastream_from_file(file2)
