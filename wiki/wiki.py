#WIKI DOWNLOAD
import tensorflow as tf
from gensim.corpora import WikiCorpus
import os
import argparse

'''
C:\Program Files\Python38\lib\site-packages\gensim\utils.py:1330: UserWarning: d
etected Windows; aliasing chunkize to chunkize_serial
  warnings.warn("detected %s; aliasing chunkize to chunkize_serial" % entity)
222000222111---000666---111777   000111:::111666:::111666...222222555555000000::
:   III   ttteeennnsssooorrrffflllooowww///ssstttrrreeeaaammm___eeexxxeeecccuuut
ttooorrr///ppplllaaatttfffooorrrmmm///dddeeefffaaauuulllttt///dddsssooo___lllooo
aaadddeeerrr...cccccc:::444444]]]   SSSuuucccccceeessssssfffuuullllllyyy   ooopp
peeennneeeddd   dddyyynnnaaammmiiiccc   llliiibbbrrraaarrryyy   cccuuudddaaarrrt
tt666444___111000111...dddllllll

--> Ctrl-C

'''
# lang = 'bg'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  #изключи GPU
def store(corpus, lang):
    print("###store(corpus,lang)")    
    base_path = os.getcwd()
    store_path = os.path.join(base_path, '{}_corpus'.format(lang))
    if not os.path.exists(store_path):
        os.mkdir(store_path)
    file_idx=1
    for text in corpus.get_texts():
        if (file_idx%500==0) : print(file_idx,end=', ')
        if (file_idx%10000==0): print(" ")
        current_file_path = os.path.join(store_path, 'article_{}.txt'.format(file_idx))
        with open(current_file_path, 'w' , encoding='utf-8') as file:
            file.write(bytes(' '.join(text), 'utf-8').decode('utf-8'))
        #endwith
        file_idx += 1
        #if (file_idx>10000): break
    #endfor

def tokenizer_func(text: str, token_min_len: int, token_max_len: int, lower: bool) -> list:
    return [token for token in text.split() if token_min_len <= len(token) <= token_max_len]

def run(lang):
    origin='https://dumps.wikimedia.org/{}wiki/latest/{}wiki-latest-pages-articles.xml.bz2'.format(lang,lang)    
    fname='{}wiki-latest-pages-articles.xml.bz2'.format(lang)
    file_path = tf.keras.utils.get_file(origin=origin, fname=fname, untar=False, extract=False)
    print("file_path=...?", file_path)
    corpus = WikiCorpus(file_path, lower=False, tokenizer_func=tokenizer_func)
    #lemmatize=False,  
    #lemmatize=False,
    '''
      File "z:\wiki\wiki.py", line 33, in run
    corpus = WikiCorpus(file_path, lemmatize=False, lower=False, tokenizer_func=
tokenizer_func)
  File "C:\Program Files\Python38\lib\site-packages\gensim\corpora\wikicorpus.py
", line 612, in __init__
    raise NotImplementedError(
NotImplementedError: The lemmatize parameter is no longer supported. If you need
 to lemmatize, use e.g. <https://github.com/clips/pattern>. Perform lemmatizatio
n as part of your tokenization function and pass it as the tokenizer_func parame
ter to this initializer.
    '''
    corpus = WikiCorpus(file_path, lower=False, tokenizer_func=tokenizer_func)
    store(corpus, lang)

if __name__ == '__main__':
    '''
    ARGS_PARSER = argparse.ArgumentParser()
    ARGS_PARSER.add_argument(
        '--lang',
        default='bg', #en',
        type=str,
        help='language code to download from wikipedia corpus'
    )
    #ARGS_PARSER = parser.parse_args(argv[1:])
    ARGS = ARGS_PARSER.parse_args()    
    run(**vars(ARGS))
    '''
    run('bg')
