# all relevant imports
import random
import re
import os.path
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')


def lemmatize_text(text):
    # preprocess the text by lowering it and removing all the punctuation
    processed_text = re.sub(r'[.?!,:;()\-\n\d]', ' ', text.lower())
    # tokenize the text
    tokens = nltk.word_tokenize(processed_text)
    # set up the lemmatizer
    lemmatizer = WordNetLemmatizer()
    # lemmatize the tokens and return them
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens


def search_response(user_response, sent_tokens):
    # set up a blank response to append to later
    response = ''
    # append the user response to the sentence tokens
    sent_tokens.append(user_response)
    # set up the vectorizer
    vectorizer = TfidfVectorizer(tokenizer=lemmatize_text, stop_words='english')
    tfidf = vectorizer.fit_transform(sent_tokens)
    # find cosine similarity of the user response against the remaining document
    values = cosine_similarity(tfidf[-1], tfidf)
    idx = values.argsort()[0][-2]
    # flatten and sort the values
    flattened = values.flatten()
    flattened.sort()
    # get the final term frequency
    final_freq = flattened[-2]
    # if the term frequency is 0, then respond about not understanding
    # else, respond with a relevant piece of information
    if (final_freq == 0):
        response = response + "Sorry, I don't understand what you mean."
    else:
        response = response + sent_tokens[idx]
    # remove the user response from the sentence tokens in the end
    sent_tokens.remove(user_response)
    return response


def sentiment_analysis(user_response):
    # get the tokens of the user response
    # and make variable for negative and positive values
    tokens = nltk.word_tokenize(user_response)
    neg = 0
    pos = 0
    # for each token, generate a positive or negative score
    # and sum it up at the end
    for token in tokens:
        syn_list = list(swn.senti_synsets(token))
        if syn_list:
            syn = syn_list[0]
            neg += syn.neg_score()
            pos += syn.pos_score()
    # at the end, respond based on the sentiment analysis
    if pos > neg:
        print("BOT: I'm glad you liked that fact!")
    else:
        print("BOT: Aw, I'm sorry you didn't like that.")


def parse_color(user_input):
    # get the color synset and assign newcolor to user_input
    color = wn.synset('color.n.01')
    newcolor = user_input
    # cycle through the synsets of the user input
    # until a match is found with color
    for synset in wn.synsets(newcolor):
        if wn.wup_similarity(synset, color) >= .8:
            newcolor_synset = synset
            newcolor_val = wn.wup_similarity(synset, color)
            break
    # if the match value is .8, it is a more niche color
    # get the hypernym to get the overall color
    if newcolor_val == .8:
        newcolor_synset = newcolor_synset.hypernyms()

    # convert the synset to a string and process it to get the color value
    newcolor_string = str(newcolor_synset)
    newcolor_string = re.sub(r'[.?!,:;()\-\n\d]', ' ', newcolor_string.lower())
    newcolor_string = nltk.word_tokenize(newcolor_string)
    newcolor_string = newcolor_string[2]
    newcolor_string = newcolor_string.strip('\'')
    return newcolor_string


def convo_meanings(sent_tokens):
    # ask the user a question
    print("BOT: Whats your favorite color?")
    # get the user response and append it to file
    user_response = input()
    color = parse_color(user_response)
    user_file.write("really like " + color + "\n")
    # then, search the file for the fact associated with their response
    # and print it
    response = search_response(color, sent_tokens)
    print("BOT: " + response)
    # then, get the user respnse and run sentiment analysis on it
    user_response = input()
    sentiment_analysis(user_response)


def convo_scheme(sent_tokens):
    # ask the user a question
    print("BOT: Whats your favorite color scheme?")
    # get the user response and append it to file
    user_response = input()
    user_file.write("really like " + user_response + "\n")
    # then, search the file for the fact associated with their response
    # and print it
    response = search_response(user_response, sent_tokens)
    print("BOT: " + response)
    # then, get the user respnse and run sentiment analysis on it
    user_response = input()
    sentiment_analysis(user_response)


def convo_random(sent_tokens):
    # set up random topics to choose from
    random_topics = ["additive", "subtractive", "warm colors", "cold colors", "newton",
                     "aristotle", "color wheel", "color theory"]
    # choose one and grab it from the file
    choice = random.choice(random_topics)
    user_file.write("learned about " + choice + "\n")
    fact = search_response(choice, sent_tokens)
    # ask the user if they know the fact
    print("BOT: Did you know " + fact)
    # get input and run a sentiment analysis on it
    user_response = input()
    sentiment_analysis(user_response)


def scrape_web(user_response):
    url = "https://google.com/search?q=" + user_response
    # get data from the url
    r = requests.get(url)
    data = r.text
    # make a soup out of it
    soup = BeautifulSoup(data, features ="lxml")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()
    # get the text and output it
    text = soup.get_text()
    text_tokenized = nltk.sent_tokenize(text)
    target_sentence = ''
    counter = 0
    for sentence in text_tokenized:
        counter += 1
        if counter == 3:
            target_sentence = target_sentence + sentence
            break
    print("BOT: Maybe this is along the lines of what you're looking for?")
    print(target_sentence)


def parse_name(user_input):
    # add a period at the end to be able to tokenize into words
    # regardless of if the input is a single word or not
    user_input = user_input + '.'
    # get the tokens
    tokens = nltk.word_tokenize(user_input)
    # get the parts of speech
    tags = nltk.pos_tag(tokens)
    # if one of the tokens is a proper noun, that means it's a name
    for tag in tags:
        if tag[1] == 'NNP':
            name = tag[0]
    return name


if __name__ == "__main__":
    # all variable declarations that can be defined in advance
    return_phrases = ["Oh, I remember you!", "Welcome back!", "It's nice to see you again!"]
    bye_phrases = ["goodbye", "bye", "salutations", "farewell"]
    chatbot_status = True

    # read in the file
    with open('chatbot.txt', 'r', encoding='utf8', errors='ignore') as file:
        raw_data = file.read().lower()
    # tokenize into sentences
    sent_tokens = nltk.sent_tokenize(raw_data)

    # intro question
    print("BOT: Hello! I'm here to chat about color theory with you.")
    response = input()
    print("BOT: What's your name?")
    # get users name and make a filename of it
    user_name = input()
    # parse the user input first though
    user_name = parse_name(user_name)
    user_filename = user_name.lower() + ".txt"

    # if the file already exists, generate a response based on past interactions
    if os.path.exists(user_filename):
        # open file to read and get last line
        user_fileread = open(user_filename, "r", encoding="utf8")
        user_last_interaction = user_fileread.readlines()[-1:]
        # choose a random return response and say something about the last interaction
        print("BOT: " + random.choice(return_phrases) + " You " + user_last_interaction)
        # get user response and close file to proceed
        response = input()
        user_fileread.close()

    # open file to append
    # this will ensure that a new file is created if one doesn't already exist
    # and that we will keep writing to a file if it already exists
    user_file = open(user_filename, "a", encoding="utf8")

    # start running the chatbot while the flag is true
    while chatbot_status:
        # ask the user what they want to talk about
        print(
            "BOT: What would you like to talk about? I can talk about color meanings, "
            "color schemes, or any random color theory fact.")
        # parse response
        user_response = input()
        user_response = re.sub(r'[.?!,:;()\-\n\d]', ' ', user_response.lower())
        user_response_tokens = nltk.word_tokenize(user_response)
        # if there is a word that's one of the goodbye phrases, end interactions
        for word in user_response_tokens:
            if word in bye_phrases:
                chatbot_status = False
                print("BOT: Bye! It was nice talking to you.")

                # close the file
                user_file.close()
                exit(1)
        # else, check if the user mentioned any of the keywords
        # and go down the associated conversational path
        if "color meanings" in user_response:
            convo_meanings(sent_tokens)
        elif "color scheme" in user_response:
            convo_scheme(sent_tokens)
        elif "random" in user_response:
            convo_random(sent_tokens)
        else:
            #if response not found, scrape web for result
            print("BOT: Sorry, I didn't understand that.")
            scrape_web(user_response)
