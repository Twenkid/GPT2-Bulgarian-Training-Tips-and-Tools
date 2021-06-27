# Author (C): Todor Arnaudov/Twenkid, 27.6.2021
# Convert texts with a nasty mixed-alphabet encodin
# Non-"normal" Unicode same-looking characters (searching doesn't find them with keyboard input)
# Also Latin looking like Cyrillic in Cyrillic words and vice verse instead of latin
# y->у, o->о, etc.
# Found in the Bulgarian IT news site Kaldata - the reason for that encoding is unknown, it probably confuses Search engines.
# This is a quick and partial solution (I stopped, because it happened to be more messy than I first thought, cyrillic nad latin are messed-up).
# The idea is:
# 1. Collect sample texts by copying them, type the translation
# 2. Scan the examples and collect the mapping into a hash table (dictionary)
# 3. Replace
# Source of the nasty texts: https://www.kaldata.com/
# Sample text: kaldata.txt


import os

path = "J:\\convert.txt"
src = r"Z:\CLEAN\computers\IT_Kaldata-razdel-bez-html.txt"

print("READING?")
f = open(path, "rt", encoding='utf-8')
#tt = f.read()
raw = f.read()
f.seek(0,0)
tt = f.readlines()  
#lines = tt.splitlines()
for n,l in enumerate(tt):
  print(n,l)
  
#skip first two

mapping = {}

i=2
end = len(tt)
skip = ['\n',' ', '1','2','3','4','5','6','7','8','9','0']
while i < end-1:
  bad, good = tt[i], tt[i+1]
  for badSymbol, goodSymbol in zip(bad,good):
    if badSymbol not in mapping and badSymbol not in skip:
      mapping[badSymbol] = goodSymbol
  i+=2
  
print("MAPPING?")
for k in mapping.keys():
  print(k+":["+mapping[k]+"]")
  
out = ''
for s in raw:
  #if mapping[s]: # != None
  if s in mapping: # != None
    out+=mapping[s]
  else: out+=s

print("CONVERTED?")  
print(out)
print("Mapped: ", len(mapping))
  

m = ''
for i in mapping:
  m+=i
  
s = ''  
for i in mapping.keys():
  s+=mapping[i]  
print("ALL:",s)
#for n,s in enumerate(raw):
sr = sorted(s)
print(sr)

# J

f = open(src,"rt", encoding='utf-8')
raw = f.read()
f.close()
out = ''
for s in raw:
  #if mapping[s]: # != None
  if s in mapping: # != None
    out+=mapping[s]
  else: out+=s
  

o = open('out-Kaldata.txt',"wt", encoding='utf-8') 
o.write(out)
o.close()
