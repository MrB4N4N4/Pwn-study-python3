import re

res = """note created. no 254
 [e9a51000]- Select Menu -
1. create note
2. write note
3. read note
4. delete note
5. exit
"""

reg = re.compile(r"no.\d{1,3}")
print(reg.search(res).group().split()[1])
