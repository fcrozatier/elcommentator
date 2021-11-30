import os
import re
from os import listdir, remove

year = 2021


def remove_from_list(my_list):
    for f in my_list:
        path = f"../Bulletins/{year}/{f}"
        if os.path.isfile(path):
            remove(path)
            print(f"removed: {path}")
        else:
            print(f"not found: {path}")


# Find all pdf in ./Bulletins/year
all_pdf = listdir(f"../Bulletins/{year}")
print(f"Total: {len(all_pdf)}")

# Filter the Semeter ones
semestre_pdf = [f for f in all_pdf if re.search("Semestre", f)]
print(f"Semester pdf: {len(semestre_pdf)}")

# Remove Semester files
remove_from_list(semestre_pdf)

# Remove duplicate files:
duplicates = [f for f in all_pdf if re.search(r"\(\d\)\.pdf$", f)]
print(f"Duplicates: {len(duplicates)}")
remove_from_list(duplicates)
