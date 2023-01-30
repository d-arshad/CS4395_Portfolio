#imports
import sys
import os
import re
import pickle

#Person class, defines last, first, middle initial, ID, and phone #
class Person:
  #init function definition
  def __init__(self, last, first, mi, id, phone):
    self.last = last
    self.first = first
    self.mi = mi
    self.id = id
    self.phone = phone
  #display function, prints out employee id, full name, and phone #
  def display(self):
    print("Employee ID: ", self.id)
    print("\t\t", self.first, self.mi, self.last)
    print("\t\t", self.phone)

#function open_file that takes in filepath and Dict
def open_file(filepath, Dict):
    #opens file
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        #skip header line
        next(f)
        #loops until there is no more text to process
        while(True):
            #reads in text from file into text_in
            text_in = f.readline()
            #if text_in is empty, break
            if not text_in:
                break
            #process the text, taking in input of text_in and Dict
            process_text(text_in, Dict)

#fuction process_text that takes in text_in and Dict
def process_text(text_in, Dict):
    #split by comma
    tokens = text_in.split(',')

    #capitalize first and last name
    tokens[0] = tokens[0].capitalize()
    tokens[1] = tokens[1].capitalize()

    #if middle initial exists, uppercase it
    if tokens[2]:
        tokens[2] = tokens[2].upper()

    #else if it doesn't exist, then make the middle initial is X
    else:
        tokens[2] = 'X'

    #while loop that checks if ID is in the right format
    #of [2 letters][4 digits]
    while(True):
        x = re.search("[a-zA-Z]{2}\d{4}", tokens[3])
        #if the ID is in the right format, it breaks
        if x:
            break
        #else, print error and ask user to re input ID
        else:
            print("ID Invalid:", tokens[3])
            print("ID must be 2 letters followed by 4 digits.")
            tokens[3] = input("Please enter a valid ID: ")

    #strip phone number of newline
    tokens[4] = tokens[4].strip()
    #while loop that checks if phone number is in the right format
    #of 123-456-7890
    while(True):
        x = re.search("\d{3}-\d{3}-\d{4}", tokens[4])
        #if the phone number is in the right format, it breaks
        if x:
            break
        #else, print error and ask user to re input ID
        else:
            print("Phone number invalid:", tokens[4])
            print("Enter phone number in form 123-456-7890")
            tokens[4] = input("Please enter phone number again: ")

    #make person object and input all the fixed information
    p1 = Person(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4])
    #check if id is already in dict
    #if it is, print error
    if tokens[3] in Dict:
        print("ERROR: This ID has already been inputted.")
    #else, input it into dict
    else:
        Dict[tokens[3]] = p1
        #print(Dict)

#main function
if __name__ == '__main__':
    #if sys arguments less than 2, ask for filename
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    #else, open file through given filepath
    else:
        fp = sys.argv[1]
        open_file(fp)
    #open_file("data/data.csv", Dict)

    #create dictionary
    Dict = {}
    #pickle dictionary
    pickle.dump(Dict, open('dict.p', 'wb'))
    #read pickle file
    newDict = pickle.load(open('dict.p', 'rb'))

    #print employee list
    print("Employee list: \n")
    #go through every object in dictionary and print
    for x in newDict:
        Person.display(newDict[x])
        print("\n")


