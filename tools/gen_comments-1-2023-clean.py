#-*- coding: utf-8 -*-
import os
#from tokenise import BPE_token
from tokenizers.models import BPE
from tokenizers import Tokenizer
from tokenizers.decoders import ByteLevel as ByteLevelDecoder
from tokenizers.normalizers import NFKC, Sequence
from tokenizers.pre_tokenizers import ByteLevel
from tokenizers.trainers import BpeTrainer

import tensorflow as tf
from transformers import GPT2Config, TFGPT2LMHeadModel, GPT2Tokenizer

from transformers import pipeline, set_seed 
from datetime import datetime
import random

"""
Author: Todor Arnaudov, "Sacred Computer":
http://artificial-mind.blogspot.com
http://github.com/Twenkid - Looking for partners for my AGI Research Institute and other projects. Check it out!
https://youtu.be/V1eO2OpsXBE
https://github.com/Twenkid/GPT2-Bulgarian-Training-Tips-and-Tools

A method for:

Chained Unlimited Directed GPT2 Generation by overlapping prompts-injection and Removing the Injected Beginning of the Following Generated Sequence

Created in June-July 2021 while training GPT2-Medium on Colab.

Published in 1.2023

"""


os.environ['CUDA_VISIBLE_DEVICES'] = '-1' #Can't fit MEDIUM in GPU - can't train even small?

#LOAD
model_dir = r"Z:\gpt2"

tokenizer = None; model = None

#tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
#model = TFGPT2LMHeadModel.from_pretrained(model_dir)


def generate(tokenizer, text=None):
  if text == None:
    text = "Той каза на жена си, че много я обича и винаги след нея ще тича, а тя се разсмя."
    text = "Какво му трябва на човек? Парите, колите, жените и песните!"
    text = "Той каза на жена си, че много я обича и винаги след нея ще тича, а тя се разсмя: Иване, купи ми кола или ще си намеря друг!"
  # encoding the input text
  input_ids = tokenizer.encode(text, return_tensors='tf')
  # getting out output
  beam_output = model.generate(
    input_ids,
    max_length = 100,
    num_beams = 16,
    temperature = 1.0,
    no_repeat_ngram_size=2,
    num_return_sequences=1
  )   
  for i in range(0,1):
    print(tokenizer.decode(beam_output[i]))    
  now = datetime.now()
  date_time = now.strftime("%d-%m-%Y_%H-%M-%S")
  #f = open("gen.txt", "wt", encoding='utf-8') #date etc.
  fname = "gen" +  date_time + ".txt"
  f = open(fname, "wt", encoding='utf-8') #date etc.
  f.write(tokenizer.decode(beam_output[i]))
  f.close()


def gen_return(tokenizer, length=100, beams=16, t=1.0, ngram=2, seq=1, top_k=40, text=None):
  if text == None:
    text = "Той каза на жена си, че много я обича и винаги след нея ще тича, а тя се разсмя."
    text = "Какво му трябва на човек? Парите, колите, жените и песните!"
    #text = "Той каза на жена си, че много я обича и винаги след нея ще тича, а тя се разсмя."
  # encoding the input text
  input_ids = tokenizer.encode(text, return_tensors='tf')
  # getting out output
  beam_output = model.generate(
    input_ids,
    max_length = length, #150,
    num_beams = beams, #16,
    temperature = t, #1.0,
    no_repeat_ngram_size=ngram, #2,
    num_return_sequences=seq, #1
    top_k =   beam_output = model.generate(
    input_ids,
    max_length = length, #150,
    num_beams = beams, #16,
    temperature = t, #1.0,
    no_repeat_ngram_size=ngram, #2,
    num_return_sequences=seq, #1
    top_k =   beam_output = model.generate(
    input_ids,
    max_length = length, #150,
    num_beams = beams, #16,
    temperature = t, #1.0,
    no_repeat_ngram_size=ngram, #2,
    num_return_sequences=seq, #1
    top_k = top_k
  ) 
  ret = []  
  for i in range(0,seq):
    print(tokenizer.decode(beam_output[i]))    
    ret.append(beam_output[i])
  print(len(ret))
  
  now = datetime.now()
  date_time = now.strftime("%d-%m-%Y_%H-%M-%S")
  #f = open("gen.txt", "wt", encoding='utf-8') #date etc.
  fname = "gen-" +  date_time + ".txt"
  f = open(fname, "wt", encoding='utf-8') #date etc.
  f.write(tokenizer.decode(beam_output[i]))
  f.close()
  return(ret)

def basic():  
  print('Generating...')
  generate(tokenizer)    

def advanced(tokenizer, text=None):
  now = datetime.now()
  date_time = now.strftime("%d-%m-%Y_%H-%M-%S")
  #f = open("gen.txt", "wt", encoding='utf-8') #date etc.
  fname = "gen-" +  date_time + ".txt"
  f = open(fname, "wt", encoding='utf-8') #date etc.
  f.write("gn = gen_return(tokenizer, length=200, beams=16, t=1.0, ngram=2, seq=1, text=None)")
  print("Generating..." )  
  beams = 16  
  for b in [16, 8, 4, 2, 1]:
    f.write("BEAMS="+str(b)+"\r\n")
    gn = gen_return(tokenizer, length=200, beams=b, t=1.2, ngram=2, seq=1, text=text)
    for nm, item in enumerate(gn):
      output = "\r\n" + str(nm) + "\r\n" + tokenizer.decode(item)      
    f.write(output)
    f.write("\r\n")
  f.close()  
  

def advancedMany(tokenizer, text=None):
  length = 200 #280 # 200#125 #250 #250 #400 #150 #200
  now = datetime.now()
  date_time = now.strftime("%d-%m-%Y_%H-%M-%S")
  #f = open("gen.txt", "wt", encoding='utf-8') #date etc.
  fname = "gen-" +  date_time + ".txt"
  f = open(fname, "wt", encoding='utf-8') #date etc.  
  beams = 16 #16 #8 #16 # 8 #16  
  t = 1.1 #3 #1.2 #not 1.5 #.2 #until 24.6. incl. was 1.2 then a run ~ 20:00 25.6 =1; now 1.5
  n = 0
  ngram = 2 #2 #3 - not good # was 2 until 25.6 20:hh
  f.write("gn = gen_return(tokenizer, " + "length="+str(length)+" , beams= " + str(beams) + ", t=" +str(t) + ", ngram=" + str(ngram))
  print("Generating...")  
  #
  texts = ["Барам си хуя и му късам главата! Свършвам във банята, свършвам на земята! Барам си хуя и му късам главата!", "Банките спират депозитите на граждани. Вече ще се плаща само в натура, като цените варират според сексапила на клиентите. Грозните ще трябва повече да се потрудят.", "Карам си колата с 300 километра, нещо се изпречи като самолет! Но какво да видя самолетът изостава като костенурка!", "Върви народе възродени, към Англия, САЩ и Европа върви! И в гъза се еби!", "Когато бях овчарче и овците пасях, бях много благодарен, макар и сиромах! Амин!", "Императорът се обади на любовницата си от Париж: скъпа, чакам те в Рим. Времето е чудесно!", "Да бъдеш или да не бъдеш? - попита Терминаторът и застреля Хамлет, който полетя към стената."]
  texts = ["Той каза на жена си, че много я обича и винаги след нея ще тича, а тя се разсмя: Иване, купи ми кола или ще си намеря друг ебач!", "Интел участват в корупционна оргия с Dell, в която са замесени висши търговски представители. За да злепоставят конкурентите си от AMD, те са изключили 10% от ядрата на графичния ускорител GeForce 3."]
  
  texts = ["Intel участват в корупционна оргия с Dell и се бият с AMD, обаче компютрите им са стари като Пентиум."]
  texts = ["Предсказването на бъдещето е основна способност на мозъка - казал Конфуций и изпил една чаша ракия."]
  texts = ["Мезалианс, принцесата се отказва от привилегиите си. Или майка ѝ, която е кралица, по всички правила на родословията, те обявява тържествено за рицар, след определен брой подвизи в името на верността към короната.", "Intel участват в корупционна оргия с Dell и се бият с AMD, обаче компютрите им са стари като Пентиум.", "Предсказването на бъдещето е основна способност на мозъка - казал Конфуций и изпил една чаша ракия.", "Барам си хуя и му късам главата! Свършавам във банята, свършвам на земята! Барам си хуя и му късам главата!", "Банките спират депозитите на граждани. Вече ще се плаща само в натура, като цените варират според сексапила на клиентите. Грозните ще трябва повече да се потрудят.", "Карам си колата с 300 километра, нещо се изпречи като самолет! Но какво да видя самолетът изостава като костенурка!", "Върви народе възродени, към Англия, САЩ и Европа върви! И в гъза се еби!", "Когато бях овчарче и овците пасях, бях много благодарен, макар и сиромах! Амин!", "Императорът се обади на любовницата си от Париж: скъпа, чакам те в Рим. Времето е чудесно!", "Да бъдеш или да не бъдеш? - попита Терминаторът и застреля Хамлет, който полетя към стената.", "Тодор Живков се срещна с Владимир Путин на тристранна среща с президента на САЩ Ким Кардашиян, след което се развихри дива оргия, при която има пострадали животни."]
  texts = ["Microsoft се обадили на Apple за да се разберат за процесора Пентиум.", "- Не! - раздра простора Бай Гочо. - Народът е омаян от змейщината. Змейовете са разляли лудо биле по всички извори на словото.", "Къде се е чуло и видяло, куче да лети и тухла да чете вестник?", "- Не знам, но печката е включена и телевизорът работи. Знаеш ли колко ток гори?!", "Херкулес извадил пистолета и гръмнал злия робот в дупарата."]
  
  texts = ["Той каза на жена си, че много я обича и винаги след нея ще тича, а тя се разсмя: Ивaне, купи ми кола или ще си намеря друг ебач!", "Интел участват в корупционна оргия с Dell, в която са замесени висши търговски представители. За да злепоставят конкурентите си от AMD, те са изключили 10% от ядрата на графичния ускорител GeForce 3.", "Microsoft се обадили на Apple за да се разберат за процесора на Intel.", "- Не! - раздра простора Бай Гочо. - Народът е омаян от змейщината!", "Къде се е чуло и видяло, куче да лети и тухла да чете вестник?", "- Не знам, но печката е включена и телевизорът работи. Знаеш ли колко ток гори?!", "Херкулес извадил пистолета и гръмнал злия робот в дупарата. Терминаторът се разсмял и отвърнал.", "Американският президентът Байдън се срещнал с Ким Кардашиян, която била любовница на Бойко Борисов в резиденцията му. Те отпразнували демокрацията с чаша вино.", "Боговете сигурно са полудели, но компютрите са бързи! - рекъл Тош и звъннал на Калоян да се видят с чичо Ачо на лостовете.", "Предсказването на бъдещето е основна способност на мозъка - казал Конфуций и изпил една чаша ракия с бай Ганьо.", "Барам си хуя и му късам главата! Свършавам във банята, свършвам на земята! Барам си хуя и му късам главата!", "Банките спират депозитите на граждани. Вече ще се плаща само в натура, като цените варират според сексапила на клиентите.", "Мезалианс, принцесата се отказва от привилегиите си. Или майка ѝ, която е кралица, по всички правила на родословията, те обявява тържествено за рицар, след определен брой подвизи в името на верността към короната.", "Когато бях овчарче и овците пасях, бях много благодарен, макар и сиромах!", "Алелуя, хвани ме за хуя!", "Телевизионните новини и СМИ - системите за масова дезинформация тровят ума на скотонаселението. Изхвърлете си телевизора и ще прогледнете! - казал доктор Пламен Пасков.", "Карам си колата с 300 километра, нещо се изпречи като самолет! Но какво да видя самолетът изостава като костенурка!", "Върви народе възродени, към Англия, САЩ и Европа върви! И в гъза се еби!", "Тодор Живков се срещна с Владимир Путин на тристранна среща с президента на САЩ Ким Кардашиян, след което се развихри дива оргия, при която има пострадали животни.", "Императорът се обади на любовницата си от Париж: скъпа, чакам те в Рим. Времето е чудесно!", "Да бъдеш или да не бъдеш? - попита Терминаторът и застреля Хамлет, който полетя към стената."]
  #texts = ["Тодор Живков се срещна с Владимир Путин на тристранна среща с президента на САЩ Ким Кардашиян, след което се развихри дива оргия, при която има пострадали животни."]
  #for b in [16, 8, 4, 2, 1]:
  #for b in [16, 16, 16, 16, 16]:
  #for b in [8, 8, 8, 16, 16]:
  #set_seed(random.randint(1,9999999))
  #texts = ["Windows 11 е най-якият процесор на AMD!","Intel пускат нова версия на операционната система AMD 11", "ЕИМ СВЯТ и юнаците срещу GPU-тата"]
  texts.append("Windows 11 е най-якият процесор на AMD!")
  texts.append("Intel пускат нова версия на операционната система AMD 11")
  texts.append("ЕИМ СВЯТ и юнаците срещу GPU-тата")
  #3-7-2021 prostotiya
  #texts = ["Да бъдеш или да не бъдеш - попита проститутката? Това е въпросът, задник! - отговори Терминаторът - застреля БМВ-то с пушката си и колата с Джон Конър се преобърна. Тогава момичето засмука хуя му, докато той не свърши в устата и тя рече: О, толкова ти е голям!"]
  
  b = beams
  top_k = 40
  sd = 0
  for text in texts:
    f.write(str(n) + ":" + ", BEAMS = "+str(b)+" seed: " + str(sd) + "t: " + str(t) + ", top_k: " + str(top_k) + "\r\n")
    #set_seed(random.randint(1,9999999))
    sd = random.randint(1,9999999)
    set_seed(sd)        
    gn = gen_return(tokenizer, length=length, beams=b, t=t, ngram=2, seq=1, top_k=top_k, text=text) #texts[n])
    for nm, item in enumerate(gn):
      output = "\r\n" + str(nm) + "\r\n" + tokenizer.decode(item)      
      nm+=1
    f.write(output)
    f.write("\r\n") 
    n+=1    
  f.close()  
  
#params = [0 = text, 1 = length, 2 = beams, 3 = temperature, 4 = ngram, 5 = top_k]
#or text - separated?
#def advancedSingleRet(tokenizer, text, params) --> str : 
def advancedSingleRet(tokenizer, model, params) -> str : 
  text, sd, length, beams, t, ngram, top_k = params
  seq = 1 #one only for now - possible future many and select from them etc. but too slow
  now = datetime.now() 
  #length = 200#125 #250 #250 #400 #150 #200  
  date_time = now.strftime("%d-%m-%Y_%H-%M-%S")
  #f = open("gen.txt", "wt", encoding='utf-8') #date etc.
  fname = "gen-" +  date_time + ".txt"
  f = open(fname, "wt", encoding='utf-8') #date etc.  
  #beams = 8 #16 #8 #16 # 8 #16  
  #t = 1 #3 #1.2 #not 1.5 #.2 #until 24.6. incl. was 1.2 then a run ~ 20:00 25.6 =1; now 1.5
  #n = 0
  #ngram = 2 #2 #3 - not good # was 2 until 25.6 20:hh
  f.write("gn = gen_return(tokenizer, " + "length="+str(length)+" , beams= " + str(beams) + ", t=" +str(t) + ", ngram=" + str(ngram))
  print("Generating...")  
  input_ids = tokenizer.encode(text, return_tensors='tf')
  # getting out output
  beam_output = model.generate(
    input_ids,
    max_length = length, #150,
    num_beams = beams, #16,
    temperature = t, #1.0,
    no_repeat_ngram_size=ngram, #2,
    num_return_sequences=seq, #1
    top_k = top_k
  ) 
  #ret = []  
  #for i in range(0,seq):
  #  print(tokenizer.decode(beam_output[i]))    
  #  ret.append(beam_output[i])
  #return beam_output[0] #this is encoded! 
  dec = tokenizer.decode(beam_output[0]) #beam_output[0] #this is encoded!
  f.write(dec); #includes the input -- sometimes would be excluded in sequential generation
  f.close()
  return dec #tokenizer.decode(beam_output[0]) #beam_output[0] #this is encoded!
  

def advancedCycle(tokenizer, feed=None):
  pass
  
def genMany():
  text = "Той каза на жена си, че много я обича и винаги след нея ще тича, а тя се разсмя: Иване, купи ми кола или ще си намеря друг!"
  #advanced(text)
  set_seed(345)
  advancedMany(tokenizer, None)  
  

simpleEnd = ' '
def endSentence():
  if simpleEnd != None: return simpleEnd
  ends = ['.','!',';','?','...','?!']
  r = random.randint(1,len(ends)-1)
  return ends[r]
def endSentenceGeneration(text):
  return ' ' #more complex, ensure finishing previous burst properly
  #return '.' #more complex, ensure finishing previous burst properly
  
def genRecurse(): #28.6.2021
    '''
    0 -- characters, names
    1 -- locations
    2 -- topics
    3 -- specifics ...
    '''
    feed = []
    
    feed.append([["Емил"], ["Ада"], ["Иван"], ["Петър"], ["Ангел"], ["Мария"]])
    feed.append([["София"], ["България"], ["Париж"], ["Франция"]])
    feed.append([["отивам"], ["пристигам"], ["заминавам"], ["кацам"], ["срещна"], ["видя"], ["целуна"], ["прегърна"]])
    feed.append([["телевизора"], ["колата"], ["ракия"], ["москвич"], ["летище"], ["самолет"], ["хляб"], ["нива"]])    
    
    ln = 80
    ln_step = 50 #80
    total = ''
    ftotal = open(r"e:\gpt\total.txt", "wt", encoding='utf-8')
    print(type(feed[0][0]),type(feed[1][0]),type(feed[2][0]),type(feed[3][0]))
    print(type(feed[0][0][0]),type(feed[1][0]),type(feed[2][0]),type(feed[3][0]))
    mix = feed[0][0][0] + " " + feed[1][0][0] + " " + feed[2][0][0] + " " + feed[3][0][0] + endSentence()
    sd = set_seed(random.randint(1,9999))
    par = (mix, sd, ln, 16, 1.2, 2, 40)
    lenmix = len(mix)
        
    #LOAD
    #'''
    model_dir = r"Z:\gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
    model = TFGPT2LMHeadModel.from_pretrained(model_dir)
    #'''

    ret = advancedSingleRet(tokenizer, model, par)
    print(ret)
    fn = ret.find(mix) #initial
    print("FN=",fn)
    if fn > -1:
               trim = ret[fn+len(mix):]
               print(fn+len(mix))
               ftotal.write("\r\n=======\r\n"+trim+"\r\n")
    else: trim = ret               
    total = trim + endSentenceGeneration(trim) #ret[len(mix):]  not+
    ftotal.write("\r\n"+ret[fn:fn+len(mix)] + "\r\n" + "\r\n" + mix + "\r\n=====\r\n")
    ftotal.write("\r\n"+total+"\r\n")
    
    #next = ret[len(mix):] #exclude the beginning already given
    next = total
    start = len(total)
    #to_add =". " + feed[0][1] + " на " + feed[1][1] + " тогава " + feed[2][1] + "когато " + feed[3][1]
    
    #ADD PRE-
    to_add = ". " + feed[0][1][0] + " за да " + feed[1][1][0] + " понеже " + feed[2][1][0] + " когато " + feed[3][1][0] + endSentence()
    #next = next + to_add
    next = to_add + next  #in the beginning in order to smooth the connection
    #new_start = len(to_add) + start #trim from here
    new_start = len(to_add) # + start #trim from here

    ln+=ln_step #should tokenize, check len etc...
    len_to_add = len(to_add)    
    sd = set_seed(random.randint(1,9999))
    
    input_ids = tokenizer.encode(next, return_tensors='tf')
    if len(input_ids) > ln: ln = len(input_ids)+lnstep
    
    par = (next, sd, ln, 16, 1.2, 2, 40)
    ret = advancedSingleRet(tokenizer,model, par)
    
    fn = ret.find(to_add) #, len(mix)) #this is not exactly - not precise; there are no repetitions anyway
    print("FN=",fn)    
    if fn > -1:
               trim = ret[fn+len(mix):]
               ftotal.write("\r\n=======\r\n"+trim+"\r\n")               
    else: trim = ret               
    #total += trim
    total +=ret[new_start:] + endSentenceGeneration(trim)
    print(fn)    
    
    #total += trim #ret[len(next):] 
    print(ret)
    print(total)
    ftotal.write("\r\n"+total+"\r\n")

    #THIRD    
    next = total #ret[len(mix):] #exclude the beginning already given
    pred_len = len(next)
    #to_add =". " + feed[0][1] + " на " + feed[1][1] + " тогава " + feed[2][1] + "когато " + feed[3][1]
    to_add = ". " + feed[0][2][0] + " към " + feed[1][2][0] + " защото " + feed[2][2][0] + " голям " + feed[3][2][0] + endSentence()       
    #next = next + to_add
    next = to_add + next
    #new_start = len(next) #to_add)
    new_start = len(to_add)
    ln+=ln_step
    len_to_add = len(to_add) 
    sd = set_seed(random.randint(1,9999))    
    
    input_ids = tokenizer.encode(next, return_tensors='tf')
    if len(input_ids) > ln: ln = len(input_ids)+lnstep
    par = (next, sd, ln, 16, 1.2, 2, 40)
    
    ret = advancedSingleRet(tokenizer,model, par)
    
    fn = ret.find(to_add, pred_len)
    print("FN=",fn)
    if fn > -1:
               trim = ret[fn+len(to_add):]
               ftotal.write("\r\n=======\r\n"+trim+"\r\n")
    else: trim = ret               
    #total += trim
    print(fn)
    
    total +=ret[new_start:] + endSentenceGeneration(trim)
    #total += trim #ret[len(next):] 
    #total += ret[len(next):] 
    print(ret)
    print(total)
    ftotal.write("\r\n"+total+"\r\n")

    ftotal.write(total)
    ftotal.close()

    #Generate in a batch etc. ... 
    #Interactive ... Keep model loaded etc. - takes a lot of time

    '''
      f.write("\r\nbeams = 8 etc. down to 1\r\n")
      gn = gen_return(tokenizer, length=150, beams=8, t=1.0, ngram=2, seq=1, text=None)
      f.write(''.join(tokenizer.decode(gn)))      
      f.write("\r\n")
      gn = gen_return(tokenizer, length=150, beams=4, t=1.0, ngram=2, seq=1, text=None)
      f.write(''.join(tokenizer.decode(gn)))      
      f.write("\r\n")
      gn = gen_return(tokenizer, length=150, beams=2, t=1.0, ngram=2, seq=1, text=None)
      f.write(''.join(tokenizer.decode(gn)))      
      f.write("\r\n")
      gn = gen_return(tokenizer, length=150, beams=1, t=1.0, ngram=2, seq=1, text=None)
      f.write(''.join(tokenizer.decode(gn)))    
      f.write("\r\n")
      f.close()
    '''
    


def genRecurseTwo():
    '''
    0 -- characters, names
    1 -- locations
    2 -- topics
    3 -- specifics ...
    '''
    feed = []
    '''
    feed.append([["Емил"], ["Ада"], ["Иван"], ["Петър"], ["Ангел"], ["Мария"]])
    feed.append([["София"], ["България"], ["Париж"], ["Франция"]])
    feed.append([["отивам"], ["пристигам"], ["заминавам"], ["кацам"], ["срещна"], ["видя"], ["целуна"], ["прегърна"]])
    feed.append([["телевизора"], ["колата"], ["ракия"], ["москвич"], ["летище"], ["самолет"], ["хляб"], ["нива"]])    
  
    feed.append([["Емил"], ["Петя"], ["Иван"], ["Петър"], ["Ангел"], ["Мария"]])
    feed.append([["Лондон"], ["България"], ["Париж"], ["Франция"]])
    feed.append([["идвам"], ["карам"],["пристигам"], ["заминавам"], ["кацам"], ["срещна"], ["видя"], ["целуна"], ["прегърна"]])
    feed.append([["професор"],["университет"], ["колата"], ["ракия"], ["москвич"], ["летище"], ["самолет"], ["хляб"], ["нива"]])
    '''
    '''
    feed.append([["Георги"], ["говори"], ["Иван"], ["Петър"], ["Ангел"], ["Мария"]])
    feed.append([["Морето"], ["България"], ["Париж"], ["Франция"]])
    feed.append([["целувам"], ["красива"],["обичам"], ["заминавам"], ["кацам"], ["срещна"], ["видя"], ["целуна"], ["прегърна"]])
    feed.append([["леглото"],["града"], ["колата"], ["ракия"], ["москвич"], ["летище"], ["самолет"], ["хляб"], ["нива"]])
    '''
   
    feed.append([["жена"], ["процесор"], ["Иван"], ["Петър"], ["Ангел"], ["Мария"]])
    #feed.append([["процесор"], ["България"], ["Париж"], ["Франция"], ["Италия"], ["Гърция"]])
    feed.append([["обичам"], ["България"], ["Париж"], ["Microsoft"], ["Италия"], ["Гърция"]])
    feed.append([["целувам"], ["красива"],["обичам"], ["заминавам"], ["кацам"], ["срещна"], ["видя"], ["целуна"], ["прегърна"]])
    feed.append([["леглото"],["града"], ["колата"], ["вода"], ["терминатор"], ["летище"], ["самолет"], ["хляб"], ["нива"]])
    
    #del feed
    #feed = []
    
    feed.append([["AMD"], ["процесор"], ["Intel"], ["секс"], ["ускорител"], ["Мария"]])
    #feed.append([["процесор"], ["България"], ["Париж"], ["Франция"], ["Италия"], ["Гърция"]])
    feed.append([["обичам"], ["България"], ["Париж"], ["Франция"], ["Италия"], ["1080"]])
    feed.append([["тест"], ["издание"],["обичам"], ["Microsoft"], ["съюз"], ["система"], ["видя"], ["целуна"], ["прегърна"]])
    feed.append([["летя"],["цена"], ["3080"], ["вода"], ["нов"], ["летище"], ["самолет"], ["хляб"], ["нива"]])
    
    feed = []
    '''
    feed.append([["жена"], ["процесор"], ["Иван"], ["Петър"], ["Ангел"], ["Мария"], ["хляб"], ["маса"]])
    #feed.append([["процесор"], ["България"], ["Париж"], ["Франция"], ["Италия"], ["Гърция"]])
    feed.append([["обичам"], ["България"], ["Париж"], ["Microsoft"], ["Италия"], ["Гърция"], ["часовник"], ["кацам"]])
    feed.append([["целувам"], ["красива"],["обичам"], ["заминавам"], ["кацам"], ["срещна"], ["видя"], ["целуна"], ["прегърна"], ["падам"]])
    feed.append([["леглото"],["града"], ["колата"], ["вода"], ["терминатор"], ["летище"], ["самолет"], ["общество"], ["нива"]])
    '''
    feed.append([["жена"], ["стая"], ["Тодор"], ["Терминатор"], ["Ангел"], ["целувам"], ["месо"], ["летя"]])
    #feed.append([["процесор"], ["България"], ["Париж"], ["Франция"], ["Италия"], ["Гърция"]])
    feed.append([["обичам"], ["лягам"], ["София"], ["Иван"], ["Италия"], ["гърди"], ["часовник"], ["кацам"]])
    feed.append([["целувам"], ["красива"],["обичам"], ["победа"], ["летище"], ["крака"], ["мъж"], ["целуна"], ["прегърна"], ["киборг"]])
    feed.append([["леглото"],["град"], ["колата"], ["тенис"], ["терминатор"], ["оргазъм"], ["самолет"], ["общество"], ["любов"]])


    #москвич
    print(len(feed[0]))
    #return
    #print(feed[0][0], feed[1][0], feed[2][0])
    # must be three redirections
    #return
    #1)
    ln = 120
    ln_step = 100 #100 #100 #80
    maxln = 200#220 #250 #180 less, was 180, to 130 - 3.7.2021
    bms = 8 #16
    total = ''
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y_%H-%M-%S")
    fname = "gen-recurse-total-" +  date_time + ".txt"
    dir = ''    
    #ftotal = open(r"e:\gpt\totalTwo.txt", "wt", encoding='utf-8')
    ftotal = open(dir + fname, "wt", encoding='utf-8') #+ "total-" + ".txt"
    print(type(feed[0][0]),type(feed[1][0]),type(feed[2][0]),type(feed[3][0]))
    print(type(feed[0][0][0]),type(feed[1][0]),type(feed[2][0]),type(feed[3][0]))
    mix = feed[0][0][0] + " " + feed[1][0][0] + " " + feed[2][0][0] + " " + feed[3][0][0] + endSentence()
    sd = set_seed(random.randint(1,9999))
    par = (mix, sd, ln, bms, 1.2, 2, 40)
    lenmix = len(mix)
    last_context = 70 #80 #symbols from the previous stretch  #intermediate?
    #LOAD
    #'''
    model_dir = r"Z:\gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
    model = TFGPT2LMHeadModel.from_pretrained(model_dir)
    #'''

    ret = advancedSingleRet(tokenizer, model, par)
    print(ret)
    fn = ret.find(mix) #initial
    print("FN=",fn)
    if fn > -1:
               trim = ret[fn+len(mix):]
               print(fn+len(mix))
               ftotal.write("\r\n=======================\r\n"+trim+"\r\n")
    else: trim = ret               
    total = trim + endSentenceGeneration(trim) #ret[len(mix):]  not+
    ftotal.write("\r\n"+ret[fn:fn+len(mix)] + "\r\n" + "\r\n" + mix + "\r\n=====\r\n")
    ftotal.write("\r\n"+total+"\r\n")
    
    #next = ret[len(mix):] #exclude the beginning already given
    next = total
    start = len(total)
    #to_add =". " + feed[0][1] + " на " + feed[1][1] + " тогава " + feed[2][1] + "когато " + feed[3][1]
    
    #last context + ... should split words etc.
    #ADD PRE-
    to_add = total[-last_context:] + " " + feed[0][1][0] + " за да " + feed[1][1][0] + " понеже " + feed[2][1][0] + " когато " + feed[3][1][0] + endSentence()
    #or POST?
    #to_add = feed[0][1][0] + " за да " + feed[1][1][0] + " понеже " + feed[2][1][0] + " когато " + feed[3][1][0] + endSentence() + total[-last_context:] + " "
    #next = next + to_add
    next = to_add # only the new words ... + next  #in the beginning in order to smooth the connection
    #new_start = len(to_add) + start #trim from here
    new_start = len(to_add) # + start #trim from here

    ln+=ln_step #should tokenize, check len etc...
    len_to_add = len(to_add)    
    sd = set_seed(random.randint(1,9999))
    temp = 2.0 #1.2
    par = (next, sd, ln, bms, temp, 2, 40)
    ret = advancedSingleRet(tokenizer,model, par)
    
    fn = ret.find(to_add) #, len(mix)) #this is not exactly - not precise; there are no repetitions anyway
    print("FN=",fn)    
    if fn > -1:
               trim = ret[fn+len(mix):]
               ftotal.write("\r\n=======\r\n"+trim+"\r\n")               
    else: trim = ret               
    #total += trim
    total +=ret[new_start:] + endSentenceGeneration(trim)
    print(fn)    
    
    #total += trim #ret[len(next):] 
    print(ret)
    print(total)
    ftotal.write("\r\n"+total+"\r\n")

    #THIRD    
    next = ret[-last_context:]  #ret[len(mix):] #exclude the beginning already given
    pred_len = len(next)
    #to_add =". " + feed[0][1] + " на " + feed[1][1] + " тогава " + feed[2][1] + "когато " + feed[3][1]
    to_add = ret[-last_context:] +  "  " +feed[0][2][0] + " към " + feed[1][2][0] + " защото " + feed[2][2][0] + " голям " + feed[3][2][0] + endSentence()
    #to_add = feed[0][2][0] + " към " + feed[1][2][0] + " защото " + feed[2][2][0] + " голям " + feed[3][2][0] + endSentence() + ret[-last_context:] + " "  #PRE new keywords
    
    #next = next + to_add
    next = to_add #+ next
    #new_start = len(next) #to_add)
    new_start = len(to_add)
    #ln+=ln_step
    len_to_add = len(to_add) 
    sd = set_seed(random.randint(1,9999))
    par = (next, sd, ln, bms, 1.0, 2, 40) #1.2, 2, 40)
    
    input_ids = tokenizer.encode(next, return_tensors='tf')
    if len(input_ids) > ln: ln = len(input_ids)+lnstep
    
    ret = advancedSingleRet(tokenizer,model, par)
    
    fn = ret.find(to_add, pred_len)
    print("FN=",fn)
    if fn > -1:
               trim = ret[fn+len(to_add):]
               ftotal.write("\r\n=======\r\n"+trim+"\r\n")
    else: trim = ret               
    #total += trim
    print(fn)
    
    total +=ret[new_start:] + endSentenceGeneration(trim)
    #total += trim #ret[len(next):] 
    #total += ret[len(next):] 
    print(ret)
    print(total)
    ftotal.write("\r\n"+total+"\r\n")

    choose = "към,защото,голям,малък,хубав,и,но,ако,с,без,да,където,когато,никога,ха-ха,не мога,мога,искам,не искам,къде,най-голям,стига,нея,аз,ти,той,тя,ние,вие,те"
    spl = choose.split(',')
    print(spl)
    space = " "
    for k in range(3,8): #5): #, len(feed[0])):     
      print("K=",k)    
      #random.choice(seq)¶
      #to_add = ret[-last_context:] + ". " + feed[0][k][0] + " към " + feed[1][k][0] + " защото " + feed[2][k][0] + " голям " + feed[3][k][0] + endSentence()      
      rch1 = space + random.choice(spl) + space  
      rch2 = space + random.choice(spl) + space
      rch3 = space + random.choice(spl) + space
      #rch4 = random.choice(seq)
      
      #step = ret[-last_context:] should split on whole words etc. ... #11-7-2021
      #to_add = ret[-last_context:] + ". " + feed[0][k][0] + " " + rch1 + " " + feed[1][k][0] + rch2 + feed[2][k][0] + rch3 + feed[3][k][0] + endSentence() 
      to_add = feed[0][k][0] + " " + rch1 + " " + feed[1][k][0] + rch2 + feed[2][k][0] + rch3 + feed[3][k][0] + endSentence() + ret[-last_context:] + " " # за да не прекъсва изреченията неестествено?
      
      ftotal.write("\r\n:TO_ADD=["+to_add+"]\r\n")
      next = to_add #+ next
      #new_start = len(next) #to_add)
      new_start = len(to_add)
      #ln+=ln_step
      len_to_add = len(to_add) 
      sd = set_seed(random.randint(1,9999))
      
      input_ids = tokenizer.encode(next, return_tensors='tf')
      if len(input_ids) > ln: ln = len(input_ids)+lnstep   
      else: ln = min(ln, maxln)
      print("LN=",ln)      
      par = (next, sd, ln, bms, 1.2, 2, 40)    
      ret = advancedSingleRet(tokenizer,model, par)
   
      fn = ret.find(to_add, pred_len)
      print("FN=",fn)
      if fn > -1:
                 trim = ret[fn+len(to_add):]
                 ftotal.write("\r\n=======\r\n"+trim+"\r\n")
      else: trim = ret               
      #total += trim
      print(fn)
    
      total +=ret[new_start:] + endSentenceGeneration(trim)
      #total += trim #ret[len(next):] 
      #total += ret[len(next):] 
      print(ret)
      print(total)
      ftotal.write("\r\n"+total+"\r\n")
      ftotal.write(total)      
 

    #Generate in a batch etc. ... 
    #Interactive ... Keep model loaded etc. - takes a lot of time  
    
#genRecurse()
#genRecurseTwo()
if tokenizer == None: tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
if model == None: model = TFGPT2LMHeadModel.from_pretrained(model_dir)

genRecurseTwo()
advancedMany(tokenizer)
