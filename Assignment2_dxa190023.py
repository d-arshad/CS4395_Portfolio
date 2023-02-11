#imports
import sys
import os
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from random import randint

#function open_file that takes in filepath
def open_file(filepath):
    #opens file
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        #read in text
        text = f.read()
    #return text back to caller
    return text

#function get_lexical_diversity to calculate the lexical diversity of a text
def get_lexical_diversity(text):
    #have processed_text hold lowercase unpunctuated text
    processed_text = re.sub(r'[.?!,:;()\-\n\d]',' ', text.lower())
    #tokenize processed_text and get unique tokens
    tokens = word_tokenize(processed_text)
    unique_tokens = set(tokens)
    #print lexical diversity
    print("\nLexical diversity: %.2f" % (len(unique_tokens) / len(tokens)))

def preprocess_text(text):
    #tokenize, lowercase, ignore stop words, and have length > 5 for all words
    tokens = [t.lower() for t in word_tokenize(text) if t.isalpha() and
              t not in stopwords.words('english') and len(t) > 5]
    #lemmatize words
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(t) for t in tokens]
    #get unique lemmas
    unique_lemmas = set(lemmatized)
    #tag lemmas by part of speech
    tags = nltk.pos_tag(unique_lemmas)
    #print out the first 20 tagged lemmas
    print("First 20 tagged lemmas: ")
    n = 0
    for x in range(0, 20):
        print(tags[x])
    #make a list of all the nouns by parsing through the list of tagged lemmas
    nouns = []
    for word, pos in tags:
        if re.search("\AN", pos):
            nouns.append(word)
    #print out number of tokens and number of nouns
    print("\nNumber of tokens: ", len(tokens))
    print("Number of nouns: ", len(nouns))

    return tokens, nouns

#function guessing_game takes in input of list and generates a looping guessing game
def guessing_game(list):
    #set up initial variables and print guessing game header
    score = 5
    guess = ''
    print("Lets play a guessing game! ")

    #outer while loop that generates the random word and keeps looping to let the player keep playing
    #even after correctly guessing one word
    while(score > -1 and guess != '!'):
        rand_number = randint(0, 49)
        guess_word = list[rand_number]
        #make string of _ for each letter of guess_word
        guess_output = re.sub("\w", "_", guess_word)

        #inner while loop that hosts the actual game
        while(score > -1 and guess != '!'):
            #print output, ask for letter guess
            print(guess_output)
            guess = input("Guess a letter in the word: ")
            #look for letter in word
            found = [x.start() for x in re.finditer(guess, guess_word)]
            #if letter was found, increase score, congratulate player
            #and replace all correct spaces in the _ string with the right letter
            if bool(found):
                score += 1
                print("Right! Score is ", score)
                guess_output_list = [x for x in guess_output]
                for x in found:
                    guess_output_list[x] = guess
                guess_output = "".join(guess_output_list)
            #else, decrease score and let the player know they've guessed wrong
            else:
                score -= 1
                if score > -1:
                    print("Wrong! Guess again. Score is ", score)
                #if the score is too low, let the player know game is over
                else:
                    print("Sorry, game over.")
            #if player successfully guessed word, congratulate them and let them play another game
            if guess_output == guess_word:
                print("Congratulations! You found the word.")
                print(guess_output)
                print("Your score is ", score)
                print("\nGuess another word:")
                break

#main function
if __name__ == '__main__':
    #if sys arguments less than 2, ask for filename
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    #else, open file through given filepath
    else:
        fp = sys.argv[1]
        text = open_file(fp)
    #text = open_file("anat19.txt")
    #get the lexical diversity of the text
    get_lexical_diversity(text)
    #get the tokens and nouns of the text
    tokens, nouns = preprocess_text(text)
    #make a dictionary of the counts of each noun
    counts = {t:tokens.count(t) for t in nouns}
    #sort the counts
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    guessing_game_list = []
    #print the 50 most common nouns
    print("\n50 most common nouns: ")
    #loop through and print, and also store each word in guessing_game_list
    for x in range(0, 50):
        print(sorted_counts[x])
        guessing_game_list.append(sorted_counts[x][0])
    #call guessing_game with the list of common nouns
    guessing_game(guessing_game_list)