'''
David Nguyen
CS4395 HW1
Reads a CSV file from user, standardized the text,
store each person object in a dict and as a pickle,
and prints each person’s information
'''

import sys
import os
import re
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

class Person:
  # Parameterized constructor for Person object
  def __init__(self, last_name, first_name, middle_initial, id, phone):
    self.last_name = last_name
    self.first_name = first_name
    self.middle_initial = middle_initial
    self.id = id
    self.phone = phone

  # Prints the person object attributes
  def display(self):
    print("Employee id: ", self.id)
    print("\t", self.first_name, self.middle_initial, self.last_name)
    print("\t", self.phone)

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

# Open file for reading and returns file text as a list
def open_file(file_path):
  try:
    # No need for managing file streams due to 'with'
    # Encoding is 'utf-8-sig' to strip off the UTF-8 Byte Order Mark 'ï»¿'
    with open(os.path.join(os.getcwd(), file_path), 'r', encoding='utf-8-sig') as file:
      return file.read().splitlines()
  except Exception as file_error:
    print(SGR_colors.ERROR + "ERROR: file could not be read" + SGR_colors.RESET)
    print(SGR_colors.UNDERLINE, "\t", file_error, SGR_colors.RESET)
    print(SGR_colors.ERROR, "\tEXITING PROGRAM..", SGR_colors.RESET)
    sys.exit(1)

# Processes the csv text list to be standardized
def process_file(csv_text_list):
  # Creates a dict to hold person objects
  persons = {}

  # Iterate through each line in csv text
  for line in csv_text_list:
    # Split line up into list of words
    words = line.split(',')
    last_name, first_name, middle_initial, id, phone = words
    
    # Modifies last and first name to be Capital Case 
    last_name = last_name.capitalize()
    first_name = first_name.capitalize()

    # Modifies middle initial to be single upper case letter, is 'X' if none
    if len(middle_initial):
      middle_initial = middle_initial[0].capitalize()
    else:
      middle_initial = "X"

    # Modifies id using regex to be 2 letters followed by 4 digits
    # Prompts user to change ID to be a valid ID if not valid
    matched = re.match(r'^[A-Z]{2}\d{4}$', id)
    
    # ID input eror checking
    while not matched:
      print(SGR_colors.WARNING + "\nWARN: " + first_name, last_name + "'s ID is not valid" + SGR_colors.RESET)
      print(SGR_colors.WARNING + "\tA valid ID is 2 letters followed by 4 digits" + SGR_colors.RESET)
      print(SGR_colors.WARNING + "\tCurrent ID is: " + id + SGR_colors.RESET)
      new_id = input(SGR_colors.WARNING + "\tPlease enter a valid ID: " + SGR_colors.RESET)
      
      new_id = new_id.strip()
      matched = re.match(r'^[A-Z]{2}\d{4}$', new_id)
      if matched:
        print(SGR_colors.GREEN + "\tSuccess!" + SGR_colors.RESET)
        id = new_id
      else:
        print(SGR_colors.ERROR + "\tTry Again!" + SGR_colors.RESET)

    # Modifies phone number using regex to be in the form 999-999-9999
    phone_numerics_only = re.sub(r'\D', '', phone)   # get rid of non-digit chars
    
    # Phone number input error checking
    if len(phone_numerics_only) == 10:
      phone = phone_numerics_only[0:3] + '-' + phone_numerics_only[3:6] + '-' + phone_numerics_only[6:10]
    else:
      matched = False
    
      while not matched:
        print(SGR_colors.WARNING + "\nWARN: " + first_name, last_name + "'s phone number is not valid" + SGR_colors.RESET)
        print(SGR_colors.WARNING + "\tA valid phone number is in the form: 123-456-7890" + SGR_colors.RESET)
        print(SGR_colors.WARNING + "\tCurrent phone number is: " + phone_numerics_only + SGR_colors.RESET)
        new_phone = input(SGR_colors.WARNING + "\tPlease enter a valid phone number: " + SGR_colors.RESET)

        new_phone = new_phone.strip()
        matched = re.match(r'^\d{3}-\d{3}-\d{4}$', new_phone)
        if matched:
          print(SGR_colors.GREEN + "\tSuccess!" + SGR_colors.RESET)
          phone = new_phone
        else:
          print(SGR_colors.ERROR + "\tTry Again!" + SGR_colors.RESET)

    # Adds standardized data line to a dict
    if id not in persons.keys():
      persons[id] = Person(last_name, first_name, middle_initial, id, phone)
    else:
      print(SGR_colors.ERROR + "\nERROR: Duplicate ID" + SGR_colors.RESET)
      print(SGR_colors.WARNING + "\t" + first_name + "," + middle_initial + "," + last_name + "," + phone + SGR_colors.RESET)
      print(SGR_colors.WARNING + "\thas the same ID '" + id + "' as" + SGR_colors.RESET)
      print(SGR_colors.WARNING + "\t" + persons.get(id).first_name + "," + persons.get(id).middle_initial + "," + persons.get(id).last_name + "," + persons.get(id).phone + SGR_colors.RESET)
      print(SGR_colors.ERROR + "\tThe new entry with the duplicate ID will be ignored and not added to the persons dictionary" + SGR_colors.RESET)
  
  return persons

# main
if __name__ == '__main__':
  # read csv file and process text
  csv_text_list = open_file(get_file_path())
  persons_dict = process_file(csv_text_list[1:])   # slice notation to csv text ignore heading line

  # save the persons dictionary as a pickle file
  pickle.dump(persons_dict, open('persons_dict.p', 'wb'))   # write binary

  # read the pickle file into a dict
  persons_dict_pickle = pickle.load(open('persons_dict.p', 'rb'))    # read binary

  # print person objects
  print("\nEmployee list:\n")
  for id_key in persons_dict_pickle:
      persons_dict_pickle[id_key].display()
      print()

  sys.exit(0)