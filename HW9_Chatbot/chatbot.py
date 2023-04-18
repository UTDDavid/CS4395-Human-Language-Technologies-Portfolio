# David Nguyen
# dxn180015
# CS 4395.001
# Chatbot
import os
import random
import nltk
import pickle
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_knowledge():
    # read in knowledge base
    with open('kb.txt', 'r', encoding='utf-8') as f:
        knowledge_base = f.read()

    # tokenize all the sentences in the KB
    sentence_tokens = sent_tokenize(knowledge_base)

    # tokenize all the lower-case words in the KB
    word_tokens = word_tokenize(knowledge_base.lower())

    # Reduce the words to only those that are alphabetical and not in the NLTK stopword list
    word_tokens = [w for w in word_tokens if w.isalpha() and w not in stopwords.words('english')]

    return sentence_tokens, word_tokens

# create a dictionary of list of sentences that contain the top 10 terms
def make_knowledge(top_10_terms, sentence_tokens):
    # create empty dictionary of lists where each key is a top term
    knowledge_base_dict = {}
    for term in top_10_terms:
        knowledge_base_dict[term] = []

    # go through each sentence token and check if contains top 10 term to put in
    for sentence in sentence_tokens:
        # tokenize sentence
        word_tokens = word_tokenize(sentence)

        # if sentence contains top term, add to dict
        for term in top_10_terms:
            if term in word_tokens:
                knowledge_base_dict[term].append(sentence)
    
    return knowledge_base_dict

# when user says hi to bot
def user_greet_bot(user_input):        
    greet = False
    user_token = word_tokenize(user_input.lower())
    for word in user_token:
        if word in key_greetings:
            greet = True
    return greet

# if user asks chatbot question
def user_ask_bot(user_input):
    question = False
    user_token = word_tokenize(user_input.lower())
    for word in user_token:
        if word in 'you':
            question = True
    return question

# lemmatize words
lemmatizer = nltk.WordNetLemmatizer()
def Lemmatize(tokens):
    return [lemmatizer.lemmatize(t) for t in tokens]

# replace punctuation
def lem(text):
    return Lemmatize(word_tokenize(text.lower().translate(dict((ord(p),None) for p in string.punctuation))))

# function to calc the most similar sentencee for responce
def response(user_input):
    response_sent = ''

    # TfidfVectorizer senteces
    tfidvector = TfidfVectorizer(tokenizer=Lemmatize)
    tfidf = tfidvector.fit_transform(sentence_tokens)

    # find the most similar sentence to input with cosine similarity
    vals = cosine_similarity(tfidf[-1],tfidf)
    index = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    required = flat[-2]

    # returns the most similar sentence or empty string
    if required == 0:
        response_sent += ""
        return response_sent
    else:
        response_sent += sentence_tokens[index]
        return response_sent

# Main
if __name__ == '__main__':
    # key phrases for chatbot to say or recognize
    key_greetings = ('hello', 'hi', 'greetings', 'howdy', 'bonjour', 'shalom','hey', 'welcome')
    user_likes_dislike = ('i like', 'i believe', 'i think', 'i wish', "i don't like", "i hate", "i dislike")

    # manually made list of top 10 terms
    top_10_terms = ['nintendo','switch','game','console','system','controller','hardware','gaming','developer','mario']

    # tokenize knowledge base and get KB dict
    sentence_tokens, word_tokens = get_knowledge()
    dict = make_knowledge(top_10_terms, sentence_tokens)

    # opening statement from chatbot and get user's name
    print("Chatbot started....")
    print("Type 'exit' or 'bye' to leave the conversation")
    print("Bot: Hello there! I can talk about the Nintendo Switch!")
    user_name = input("Bot: What is your name?\n")

    # check is new or old user in user model file
    if os.path.isfile("user_model.p"):
        user_model = pickle.load(open("user_model.p","rb"))

        if user_name in user_model:
            print("Welcome back", user_name, "! I'm ready to chat with you again!")
        else:
            print("Hi", user_name, "! I'm ready to talk!")
            user_model[user_name] = []

    # no user model, so create (dict of lists (contains user opinions) with user name as the key)
    else:
        user_model = {}
        print("Hi", user_name, "! I'm ready to talk!")
        user_model[user_name] = []

    # chatbot loop till user says exit or bye
    loop = True
    
    while loop:
        # get user input
        user_input = input().lower()

        # if user adds opinion (like/hate), add to user model
        for key_words in user_likes_dislike:
            if key_words in key_words:
                user_model[user_name].append(user_input)

        # if user says bye, set flag to end while loop
        if user_input == "bye" or user_input == "exit":
            loop = False
            print("Bot: Goodbye!")
            print("Exiting chatbot...")
        
        # continue leting user ask questions
        # possible bot paths to talk about
        else:
            # if user says hi to bot
            if user_greet_bot(user_input) == True:
                print("Bot: ", random.choice(key_greetings))

            # if user asks bot a question
            elif user_ask_bot(user_input) == True:
                print("Bot: To be honest, I don't know how to answer that.")

            else:
                sentence_tokens.append(user_input)
                word_tokens.append(word_tokenize(user_input))
            
                # bot responds with most related sentence
                bot_responce = response(user_input)
                
                # no related sentence or no user input
                if bot_responce == "":
                    if user_model:
                        old_user_opinion = random.choice(user_model[user_name])
                        print("Bot: why did you say'", old_user_opinion,"' again?")
                    else:
                        print("Bot: I am not familiar with that.")
                else:
                    print("Bot: ", bot_responce)
                
                sentence_tokens.remove(user_input)

    # pickle user model
    pickle.dump(user_model, open('user_model.p', 'wb'))
        