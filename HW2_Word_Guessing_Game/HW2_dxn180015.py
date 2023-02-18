'''
David Nguyen
CS4395 HW1
This program uses NLTK features to explore a text file and create a word guessing game
'''

import sys
import os
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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

# Get input file path from user via argv (command line arguments)
def get_file_path():
  if len(sys.argv) == 2:
    file_path = sys.argv[1]
    return file_path

  # Too many args
  elif len(sys.argv) > 2:
    print(SGR_colors.ERROR + "ERROR: \tProgram takes the 'file path' as 1 argument"
      "\n\tPaths with space should be enclosed in quotes", 
      "\n\tEXITING PROGRAM..."  + SGR_colors.RESET)
    sys.exit(1)

  # No file path
  else:
    print(SGR_colors.ERROR + "ERROR: \tNo file path inputted"
      "\n\tProgram takes the 'file path' as 1 argument", 
      "\n\tEXITING PROGRAM..."  + SGR_colors.RESET)
    sys.exit(1)

# Open file for reading and returns file text as string
def open_file(file_path):
  try:
    print(file_path)
    with open(os.path.join(os.getcwd(), file_path), 'r', encoding='utf-8-sig') as file:
      return file.read()
  except Exception as file_error:
    print(SGR_colors.ERROR + "ERROR: file could not be read" + SGR_colors.RESET)
    print(SGR_colors.UNDERLINE, "\t", file_error, SGR_colors.RESET)
    print(SGR_colors.ERROR, "\tEXITING PROGRAM..", SGR_colors.RESET)
    sys.exit(1)

# Processes the raw text and returns the tokens & nouns
def preprocess(text):
  # Tokenize the lower-case raw text
  tokens = word_tokenize(text.lower())

  # Reduce the tokens to only those that are alphabetical
  tokens = [token for token in tokens if token.isalpha() and
           token not in stopwords.words('english')]
  
  # Removes tokens not in the NLTK stopword list
  tokens = [token for token in tokens if token not in stopwords.words('english')]

  # Removes tokens that are <= 5 characters
  tokens = [token for token in tokens if len(token) > 5]

  # lemmatize the tokens and use set() to make a list of unique lemmas
  wnl = WordNetLemmatizer()
  lemmas = [wnl.lemmatize(t) for t in tokens]
  lemmas_unique = list(set(lemmas))

  # POS tagging on the unique lemmas and print the first 20 tagged
  tags = nltk.pos_tag(lemmas_unique)
  print(SGR_colors.CYAN, "\nUnique Lemmas Tagged (First 20): ", SGR_colors.RESET, tags[:20])

  # Get nouns, NN, NNS, NNP, NNPS
  nouns = [tuple[0] for tuple in tags if tuple[1].startswith('N')]
  # Prints # of tokens and # of nouns
  print(SGR_colors.CYAN, "\nThe number of tokens are:", SGR_colors.RESET, len(tokens))
  print(SGR_colors.CYAN, "\nThe number of nouns are:", SGR_colors.RESET, len(nouns))

  return(tokens, nouns)

# Make dictionary of {noun:count of noun in tokens} and returns top 50 most common words
def make_dict(tokens, nouns):
  # Makes a dictionary of nouns and its number of occurances in tokens
  noun_dict = {}
  for noun in nouns:
    noun_dict[noun] = tokens.count(noun)

  # Sort the dict by noun count
  noun_dict = dict(sorted(noun_dict.items(), key=lambda x: x[1], reverse=True))

  # Prints the 50 most common words and their counts
  print(SGR_colors.CYAN, "\nThe Top 50 Most Common Words Are: ", SGR_colors.RESET, list(noun_dict.items())[:50])

  # Returns list of these words to be used in guessing game
  return list(noun_dict.keys())[:50]

# Guessing word game using the top 50 words used
def guessing_game(top_50_words):
  # Game variables
  user_score = 5
  guess = ''
  word = random.choice(top_50_words)
  hidden = list('_') * len(word)

  # Game starts
  print(SGR_colors.CYAN + "\nLet's play a word guessing game!")
  print("Input is 1 letter only.")
  print("Enter '!' to exit the game.")
  print(word, "\n", SGR_colors.RESET)

  # Loop game till user has negative score or enters '!'
  while(user_score >= 0 and guess != '!'):
    # Print hidden word with their correct guesses
    print(*hidden)

    # Get letter as guess (trims white space and turns into lowercase)
    guess = input("Guess a letter: ").lower().strip()

    # Input is not a letter
    if len(guess) != 1:
      print(SGR_colors.WARNING + "Your guesses must be one letter only\n" + SGR_colors.RESET)

    # Letter already guessed
    elif guess in hidden:
        print(SGR_colors.WARNING + "Sorry you already gussed this letter, guess again\n" + SGR_colors.RESET)

    # Guess correct
    elif guess in word:
      # Increment score and unhide correct letter
      user_score += 1
      for i in range(len(word)):
        if guess == word[i]:
          hidden[i] = guess
      print(SGR_colors.GREEN, end="")
      print("Right! Score is", user_score, "\n", SGR_colors.RESET)

      # Entire word was guessed
      if '_' not in hidden:
        print(SGR_colors.GREEN, end="")
        print(*hidden)
        print("You solved it!")
        print("Current total score: ", user_score, SGR_colors.RESET, "\n")
        print("Guess another word!")

        # Restart game
        word = random.choice(top_50_words)
        hidden = ['_' for letter in word]
        print(word)

    # Wrong guess or exit game / negative score
    else:
      user_score -= 1
      print(SGR_colors.ERROR, end="")
      if guess == "!":
        print("Exiting game...")
      elif user_score < 0:
        print("Sorry, you lost! Your score is negative!", "\n")
      else:
        print("Sorry, guess again. Score is ", user_score, "\n")
      print(SGR_colors.RESET, end="")
  return

# Main
if __name__ == '__main__':
  # Read text file
  text = open_file(get_file_path())

  # Print lexical diversity of raw text (# of unique words / # of words)
  tokens = word_tokenize(text)
  print(SGR_colors.CYAN + "\nLexical diversity of raw text: " + SGR_colors.RESET + "%.2f" % (len(set(tokens)) / len(tokens)) )

  # Preprocess the raw text
  tokens, nouns = preprocess(text)
 
  # Make sorted dictionary of nouns count and get top 50 most common words
  top_50_words = make_dict(tokens, nouns)
  
  # Start guessing game
  guessing_game(top_50_words)

  sys.exit(0)