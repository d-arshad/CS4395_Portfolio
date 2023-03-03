import pickle
from nltk import word_tokenize, ngrams

if __name__ == '__main__':
    #unpickle all the dictionaries
    eng_unigram = pickle.load(open('eng_unigram.p', 'rb'))
    eng_bigram = pickle.load(open('eng_bigram.p', 'rb'))
    fr_unigram = pickle.load(open('fr_unigram.p', 'rb'))
    fr_bigram = pickle.load(open('fr_bigram.p', 'rb'))
    it_unigram = pickle.load(open('it_unigram.p', 'rb'))
    it_bigram = pickle.load(open('it_bigram.p', 'rb'))

    #opens files
    text = open("LangID.test", encoding="utf8").readlines()
    correct_results = open("LangId.sol", 'r').readlines()

    #define total size var, counter var, and wrong guesses counter, and a wrong guesses list
    v = len(eng_unigram) + len(fr_unigram) + len(it_unigram)
    counter = 1
    wrong_guess = 0
    wrong_guesses = []

    #open output file
    output_file = open("wordLangId.out", "w")

    for line in text:
        #get unigrams and bigrams
        unigrams_test = word_tokenize(line)
        bigrams_test = list(ngrams(unigrams_test, 2))

        # define initial probabilities
        eng_prob = 1
        fr_prob = 1
        it_prob = 1

        #get the probabilities
        for bigram in bigrams_test:
            #get english probability
            eng_b = eng_bigram[bigram] if bigram in eng_bigram else 0
            eng_u = eng_unigram[bigram[0]] if bigram[0] in eng_unigram else 0
            eng_prob = eng_prob * ((eng_b + 1) / (eng_u + v))

            #get french probability
            fr_b = fr_bigram[bigram] if bigram in fr_bigram else 0
            fr_u = fr_unigram[bigram[0]] if bigram[0] in fr_unigram else 0
            fr_prob = fr_prob * ((fr_b + 1) / (fr_u + v))

            #get italian probability
            it_b = it_bigram[bigram] if bigram in it_bigram else 0
            it_u = it_unigram[bigram[0]] if bigram[0] in it_unigram else 0
            it_prob = it_prob * ((it_b + 1) / (it_u + v))

        #find the language with the greatest probability
        biggest_prob = max(eng_prob, fr_prob, it_prob)

        #write the language with the greatest probability to a file
        if eng_prob == biggest_prob:
            lang_guess = "English"
            output_str = "The language with the greatest probability at line " \
                         + str(counter) + " is English, with the probability of: " + str(biggest_prob)
        elif fr_prob == biggest_prob:
            lang_guess = "French"
            output_str = "The language with the greatest probability at line " \
                         + str(counter) + " is French, with the probability of: " + str(biggest_prob)
        elif it_prob == biggest_prob:
            lang_guess = "Italian"
            output_str = "The language with the greatest probability at line " \
                         + str(counter) + " is Italian, with the probability of: " + str(biggest_prob)
        output_file.write(output_str)

        #check if caculation was wrong, count # of wrongs and where
        if ((counter - 1) < len(correct_results)):
            if correct_results[counter - 1] != str(str(counter) + " " + lang_guess + "\n"):
                wrong_guess += 1
                wrong_guesses.append(counter)

        #increase counter
        counter += 1

    accuracy = (((counter - 1) - wrong_guess) / (counter - 1)) * 100
    print("The accuracy of my calculations is: " + str(accuracy))
    print("The line numbers where I calculated wrong are: \n")
    print(wrong_guesses)

