'''
David Nguyen
CS4395 HW4 Part 1
Ngrams
'''

import sys
import os
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import pickle

# Class containing list of ANSI color escape sequences for use in print()
class SGR_colors:
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  RESET = '\033[0m'

  WARNING = '\033[33m'    # YELLOW
  GREEN = '\033[32m'
  ERROR = '\033[31m'      # RED
  BLUE = '\033[34m'
  MAGENTA = '\033[35m'
  CYAN = '\033[36m'

# Open file for reading and returns file text as string
def open_file(file_path):
  try:
    print(file_path)
    with open(os.path.join(os.getcwd(), file_path), 'r', encoding='utf-8') as file:
      return file.read()
  except Exception as file_error:
    print(SGR_colors.ERROR + "ERROR: file could not be read" + SGR_colors.RESET)
    print(SGR_colors.UNDERLINE, "\t", file_error, SGR_colors.RESET)
    print(SGR_colors.ERROR, "\tEXITING PROGRAM..", SGR_colors.RESET)
    sys.exit(1)

# Create ngrams lists and dicts
def make_ngrams(path):
  # read in text file
  text = open_file(path)

  # remove newlines from text
  text = text.replace("\n", "")
  
  # tokenize text
  tokens = word_tokenize(text)

  #  use nltk to create a bigrams list
  unigrams = tokens
  #unigrams

  #  use nltk to create a unigrams list
  bigrams = list(ngrams(unigrams, 2))
  #bigrams

  # use the bigram list to create a bigram dictionary of bigrams and counts
  bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}
  #bigram_dict

  # use the unigram list to create a unigram dictionary of unigrams and counts
  unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}
  #unigram_dict

  # return the unigram dictionary and bigram dictionary
  return unigram_dict, bigram_dict

# Main
if __name__ == '__main__':
  # create ngrams for 3 training files
  unigram_dict_eng, bigram_dict_eng = make_ngrams("data/LangId.train.English")
  unigram_dict_fre, bigram_dict_fre = make_ngrams("data/LangId.train.French")
  unigram_dict_itl, bigram_dict_itl = make_ngrams("data/LangId.train.Italian")
 
  #  pickle the 6 dictionaries, and save to files with appropriate names
  pickle.dump(unigram_dict_eng, open('data/unigram_dict_eng.p', 'wb'))
  pickle.dump(bigram_dict_eng, open('data/bigram_dict_eng.p', 'wb'))

  pickle.dump(unigram_dict_fre, open('data/unigram_dict_fre.p', 'wb'))
  pickle.dump(bigram_dict_fre, open('data/bigram_dict_fre.p', 'wb'))

  pickle.dump(unigram_dict_itl, open('data/unigram_dict_itl.p', 'wb'))
  pickle.dump(bigram_dict_itl, open('data/bigram_dict_itl.p', 'wb'))

  sys.exit(0)