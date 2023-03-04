'''
David Nguyen
CS4395 HW4 Part 2
Ngrams
'''

import sys
import os
import pickle
import math
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

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
      # removes newline and white space at end of each line
      return [line.rstrip() for line in file]
  except Exception as file_error:
    print(SGR_colors.ERROR + "ERROR: file could not be read" + SGR_colors.RESET)
    print(SGR_colors.UNDERLINE, "\t", file_error, SGR_colors.RESET)
    print(SGR_colors.ERROR, "\tEXITING PROGRAM..", SGR_colors.RESET)
    sys.exit(1)

def compute_prob(text, unigram_dict, bigram_dict, N, V):
  # N is the number of tokens in the training data
  # V is the vocabulary size in the training data (unique tokens)

  unigrams_test = word_tokenize(text)
  bigrams_test = list(ngrams(unigrams_test, 2))
  
  p_gt = 1       # calculate p using a variation of Good-Turing smoothing
  p_laplace = 1  # calculate p using Laplace smoothing
  p_log = 0      # add log(p) to prevent underflow

  for bigram in bigrams_test:
      n = bigram_dict[bigram] if bigram in bigram_dict else 0
      n_gt = bigram_dict[bigram] if bigram in bigram_dict else 1/N
      d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
      if d == 0:
          p_gt = p_gt * (1 / N)
      else:
          p_gt = p_gt * (n_gt / d)
      p_laplace = p_laplace * ((n + 1) / (d + V))
      p_log = p_log + math.log((n + 1) / (d + V))

  #print("\nprobability with simplified Good-Turing is %.5f" % (p_gt))
  #print("probability with laplace smoothing is %.5f" % p_laplace)
  #print("log prob is %.5f == %.5f" % (p_log, math.exp(p_log)))

  # returns prob with laplace smoothing
  return p_laplace

# Main
if __name__ == '__main__':
  # Read in your pickled dictionaries
  unigram_dict_eng = pickle.load(open('data/unigram_dict_eng.p', 'rb'))
  bigram_dict_eng = pickle.load(open('data/bigram_dict_eng.p', 'rb'))

  unigram_dict_fre = pickle.load(open('data/unigram_dict_fre.p', 'rb'))
  bigram_dict_fre = pickle.load(open('data/bigram_dict_fre.p', 'rb'))

  unigram_dict_itl = pickle.load(open('data/unigram_dict_itl.p', 'rb'))
  bigram_dict_itl = pickle.load(open('data/bigram_dict_itl.p', 'rb'))

  # calc N (number of tokens in the training data) and v (vocabulary size in the training data (unique tokens))
  N_eng = sum(unigram_dict_eng.values())
  V_eng = len(unigram_dict_eng)

  N_fre = sum(unigram_dict_fre.values())
  V_fre = len(unigram_dict_fre)

  N_itl = sum(unigram_dict_itl.values())
  V_itl = len(unigram_dict_itl)

  # read in text file
  langid_test = open_file("data/LangId.test")

  # For each line in the test file, calculate a probability for each language
  count = 1
  outfile = open("data/lang_guesses.txt", "w")
  for line in langid_test:
    prob_eng = compute_prob(line, unigram_dict_eng, bigram_dict_eng, N_eng, V_eng)
    prob_fre = compute_prob(line, unigram_dict_fre, bigram_dict_fre, N_fre, V_fre)
    prob_itl = compute_prob(line, unigram_dict_itl, bigram_dict_itl, N_itl, V_itl)

    # write the language with the highest probability to a file
    if prob_eng == max(prob_eng, prob_fre, prob_itl):
      outfile.write(str(count) + " English\n")
      count += 1

    elif prob_fre == max(prob_fre, prob_itl):
      outfile.write(str(count) + " French\n")
      count += 1
    else:
      outfile.write(str(count) + " Italian\n")
      count += 1
      
  outfile.close()
    
  # Compute and output your accuracy as the percentage of correctly classified instances in the test set. The file LangId.sol holds the correct classifications
  lang_guesses = open_file("data/lang_guesses.txt")
  lang_solutions = open_file("data/LangId.sol")
  num_guesses = len(lang_guesses)
  correct = 0
  for line_g, line_s in zip(lang_guesses, lang_solutions):
    if line_g == line_s:
      correct += 1
    else:
      # output the line numbers of the incorrectly classified items
      words_g = line_g.split()
      words_s = line_s.split()
      print("Line", words_g[0], "is wrong, the guess", words_g[1], "is supposed to be", words_s[1])

  # output your accuracy
  print("\nNumber of Correct Guesses:", correct)
  print("Number of Wrong Guesses:", (num_guesses - correct))
  print("Total Number of Guesses:", num_guesses)
  print("Accuracy:", (correct/num_guesses))

  sys.exit(0)