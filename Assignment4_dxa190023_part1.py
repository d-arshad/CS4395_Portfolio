#FIRST PROGRAM for CS4395 A4

import pickle
from nltk import word_tokenize, ngrams

#function open_file that takes in filename
def open_file(filename):
    #opens file
    text = open(filename, encoding="utf8").read()

    #remove newlines and tokenize the text
    tokens = text.split()

    #create vars to hold the list of unigrams and bigrams
    unigrams = tokens
    bigrams = list(ngrams(tokens, 2))

    #make dicitonaries of their counts
    unigram_dict = {t: unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}

    #return dictionaries
    return unigram_dict, bigram_dict

if __name__ == '__main__':
    #get unigrams and bigrams for english, french, and italian
    eng_unigram,eng_bigram = open_file("LangId.train.English")
    fr_unigram,fr_bigram = open_file("LangId.train.French")
    it_unigram,it_bigram = open_file("LangId.train.Italian")

    #pickle all the dictionaries
    pickle.dump(eng_unigram, open('eng_unigram.p', 'wb'))
    pickle.dump(eng_bigram, open('eng_bigram.p', 'wb'))
    pickle.dump(fr_unigram, open('fr_unigram.p', 'wb'))
    pickle.dump(fr_bigram, open('fr_bigram.p', 'wb'))
    pickle.dump(it_unigram, open('it_unigram.p', 'wb'))
    pickle.dump(it_bigram, open('it_bigram.p', 'wb'))


