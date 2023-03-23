import pickle
import re
import requests
import urllib
from urllib import request
from bs4 import BeautifulSoup
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

stopwords = stopwords.words('english')

# function to determine if an element is visible
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

#function to scrape through text and output to files
def scrape_text(queue):
    #iterate through queue and parse through
    filename_counter = 0
    for url in queue:
        #get text
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, features="lxml")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out
        text = soup.get_text()
        #then write to file
        filename = "url_text" + str(filename_counter) + ".txt"
        f = open(filename, "w", encoding="utf8")
        f.write(text)
        f.close()
        filename_counter += 1

#function to go through text files and clean the text
def clean_text():
    #iterate through files
    filename_counter = 0
    while(filename_counter < 15):
        #open up the appropriate file
        filename_open = "url_text" + str(filename_counter) + ".txt"
        f = open(filename_open, "r", encoding="utf8")
        #read the text and remove new lines and tabs, then sentencify
        text = f.read()
        text = re.sub(r'[\n\t]', ' ', text)
        sents = sent_tokenize(text)
        #get output file name, open it, and write the sentences to it
        filename_output = "url_text_cleaned" + str(filename_counter) + ".txt"
        with open(filename_output, 'w', encoding="utf8") as f2:
            for sentence in sents:
                f2.write(sentence)
                f2.write('\n')
        #close files
        f.close()
        f2.close()

        filename_counter += 1

def get_frequent_terms():
    #iterate through files
    filename_counter = 0
    while(filename_counter < 15):
        #terms = []
        #open up the appropriate file
        filename_open = "url_text_cleaned" + str(filename_counter) + ".txt"
        with open(filename_open, 'r', encoding="utf8") as f:
            text = f.read().lower()
            text = text.replace('\n', ' ')
        tokens = word_tokenize(text)
        tokens = [w for w in tokens if w.isalpha() and w not in stopwords]
        #print(tokens)
        # get term frequencies
        freq_terms = FreqDist(tokens)
        top_most_frequent = freq_terms.most_common(25)
        #print the top most frequent
        print("The top 25 terms in file " + str(filename_counter + 1) + " are:")
        i = 1
        for term in top_most_frequent:
            print(str(i) + ": " +  term[0])
            i += 1
        #print(top_most_frequent)
        filename_counter += 1

def knowledge_base():
    #movie, marvel, animation, comic, miles, cameo, sony, spiderman, oscar, anime
    knowledge_base_dict = {
        'movie': "A story or event recorded by a camera as a "
                 "set of moving images and shown in a theater or on television; a motion picture.",
        'marvel': "Marvel Entertainment, LLC is an American entertainment company founded in June "
                  "1998 and based in New York City, New York, formed by the merger of Marvel Entertainment Group and Toy Biz.",
        'animation' : "Animation is a method by which still figures are manipulated to appear as moving images.",
        'comic':"Comics is a medium used to express ideas with images, often combined with text or other visual information.",
        'miles': "Miles Gonzalo Morales is a fictional character, a superhero appearing in American comic books published by Marvel Comics.",
        'cameo': "A small character part in a play or movie, played by a distinguished actor or a celebrity.",
        'sony':"Sony Group Corporation is a Japanese multinational conglomerate corporation headquartered in Minato, Tokyo, Japan.",
        'spiderman':"Spider-Man is a superhero appearing in American comic books published by Marvel Comics.",
        'oscar':"The Academy Awards, better known as the Oscars, are awards for artistic and technical merit "
                "for the American film industry. ",
        'anime':"A style of Japanese film and television animation, typically aimed at adults as well as children."
    }
    pickle.dump(knowledge_base_dict, open('knowledge_base.p', 'wb'))

if __name__ == '__main__':
    #make a variable with the starter url
    starter_url = "https://en.wikipedia.org/wiki/Spider-Man:_Into_the_Spider-Verse"

    #get data from the url
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data, features ="lxml")

    #make a queue and a counter for the list of urls
    queue = []
    counter = 0

    #find all relevant links to the starter url
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        if 'Spider-man' in link_str or 'spiderman' in link_str:
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if link_str.startswith('http') and 'google' not in link_str:
                queue.append(link_str)
                counter += 1
        if counter == 15:
            break

    #now lets go through the urls and print them
    i = 0
    #iterate through queue with while loop
    while i < len(queue):
        print(queue[i])
        i += 1

    #scrape text off of urls
    scrape_text(queue)
    #clean the text
    clean_text()
    #get frequent terms
    get_frequent_terms()
    #make the knowledge base
    knowledge_base()