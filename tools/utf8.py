# 19-6-2021
# For GPT2 training etc. - ensure the encoding is correct
# (Sometimes the tokenizer complains about the encoding of files for example from books from "Chitanka" which are UTF8-BOM)
# By Twenkid

def ensure_utf(path = "."):
    #if path = None:
    #path = r'Z:/knigi/'
    import os
    import glob
    ls = os.listdir(path)
    print(ls)
    os.chdir(path)
    print("========")
    ls = glob.glob("*.txt")
    print(ls)
    try:
      os.mkdir('UTF8')
    except:
           print("Dir already exists")
    for i in ls:
      print(i)
      f = open(i, "rt", encoding='utf-8')
      r = f.read()
      f2 = open(path+"/UTF8/"+i, "wt", encoding='utf-8')
      f2.write(r)
      f.close()
      f2.close()
     
ensure_utf()
