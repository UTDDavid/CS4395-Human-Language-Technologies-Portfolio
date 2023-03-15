'''
David Nguyen
CS4395 HW6
Web Crawler
'''

import sys
import os
import re
import urllib
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import pickle
import requests
from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk import sent_tokenize
import math
from nltk.corpus import stopwords

# get 15 relevent urls from starting link
def web_crawler(starter_url):
  r = requests.get(starter_url)
  data = r.text
  soup = BeautifulSoup(data, 'html.parser')
  urls = []

  # write urls to a file and list
  with open('urls.txt', 'w', encoding='utf-8') as f:
    for link in soup.find_all('a'):
      # stop at 15 urls
      if len(urls) == 15:
        break

      link_str = str(link.get('href'))

      # filter out unwanted urls and write urls to file and list
      if link_str.startswith('http') and 'google' not in link_str and 'archive' not in link_str and 'vg247' not in link_str \
        and 'wiki' not in link_str and 'nintendo.' not in link_str and 'worldcat' not in link_str and 'nx' not in link_str \
        and 'nintendo-ds' not in link_str and 'wii' not in link_str and 'mobile' not in link_str and 'fail' not in link_str \
        and 'smh.com' not in link_str and 'smartphones' not in link_str and 'mobile' not in link_str and 'pres' not in link_str \
        and 'rollingstone' not in link_str and 'switch-interview' not in link_str and 'glixel' not in link_str and 'thegamingsetup' not in link_str \
        and 'switch-news' not in link_str and 'siliconera' not in link_str and 'usgamer' not in link_str and 'vv.html' not in link_str \
        and 'fastcompany' not in link_str and 'nintendocu' not in link_str and 'culturageek' not in link_str and 'twitter' not in link_str \
        and 'il.ign' not in link_str and 'facebook' not in link_str and 'culturageek' not in link_str and 'twitter' not in link_str:
          f.write(link_str + '\n')
          urls.append(link_str)

    return urls

# function to determine if an element is visible
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

# scrape text from url(s) to files
def text_scraper(urls):
  counter = 0
  for url in urls:
    counter += 1

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}

    # get text from url
    req = Request(url, headers=hdr)
    html = urlopen(req, timeout=10)
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.findAll(text=True)
    result = filter(visible, data)
    temp_list = list(result)
    temp_str = ' '.join(temp_list)

    # write scraped url text to out file
    with open("scraped_text_{}.txt".format(counter), 'w', encoding='utf-8') as file:
      file.write(temp_str)

# clean scraped text files and output to new files
def clean_file():
  for num_files in range(1, 16):
    # read scraped text files
    with open("scraped_text_{}.txt".format(num_files), 'r', encoding='utf-8') as file:
      raw_text = file.read()

    # remove newlines and tabs
    text = re.sub(r'[\t\n]', '', raw_text)

    # extracts sentences
    sentences = sent_tokenize(text)

    # write the sentences for each file to a new file
    with open("sentences_{}.txt".format(num_files), 'w', encoding='utf-8') as file:
      for sent in sentences:
        file.write(sent + "\n")

# create tf dictionaries for a link/doc
def create_tf_dict(doc):
  stop = stopwords.words('english')
  tf_dict = {}
  tokens = word_tokenize(doc)
  tokens = [w for w in tokens if w.isalpha() and w not in stop]
    
  # get term frequencies
  for t in tokens:
    if t in tf_dict:
      tf_dict[t] += 1
    else:
      tf_dict[t] = 1
          
  # get term frequencies in a more Pythonic way
  token_set = set(tokens)
  tf_dict = {t:tokens.count(t) for t in token_set}
  
  # normalize tf by number of tokens
  for t in tf_dict.keys():
    tf_dict[t] = tf_dict[t] / len(tokens)
      
  return tf_dict

# create tf-idf
def create_tfidf(tf, idf):
    tf_idf = {}
    for t in tf.keys():
        tf_idf[t] = tf[t] * idf[t] 
        
    return tf_idf

# read each text from the 15 clean files and calculate tf-id and print top 40 words
def top_40():
  vocab = set()
  vocab_by_topic = []
  tf_dict_list = []
  
  # loop through each file
  for counter in range(1, 16):
    with open("sentences_{}.txt".format(counter), 'r', encoding='utf-8') as file:
      all_text = file.read()

      # remove punctuation and newlines with a regular expression
      all_text = re.sub(r'[.?!,:;()\-\n]',' ', all_text.lower())

      # create tf dictionaries for each document
      tf_text_dict = create_tf_dict(all_text)
      tf_dict_list.append(tf_text_dict)

      # add to vocab
      if counter == 1:
        vocab = set(tf_text_dict.keys())
      else:
        vocab = vocab.union(set(tf_text_dict.keys()))

      #print("number of unique words:", len(vocab))
      vocab_by_topic.append(vocab)

  # make an idf frequency dictionary
  idf_dict = {}
  tfidf = {}
  num_docs = 15

  for term in vocab:
    temp = ['x' for voc in vocab_by_topic if term in voc]
    idf_dict[term] = math.log((1+num_docs) / (1+len(temp)))

  # get tf-idf for each link/doc
  for link_tf in tf_dict_list:
    tfidf_temp = create_tfidf(link_tf, idf_dict)

    # union all the tfidf to one {}
    tfidf.update(tfidf_temp)

  # print the top 40 highest tf-idf terms
  doc_term_weights = sorted(tfidf.items(), key=lambda x:x[1], reverse=True)
  print('Top 40 Terms based on tf-idf:')
  for term in doc_term_weights[:40]:
    print('\t', term)

# create knowledge base using the top 10 terms I picked.
# is simple dictionary where keys=terms and values=sentence from my pages with that term
def knowledge_base():
  # manually made list of top 10 terms
  top_10_terms = ['nes', 'snes', 'kirby', 'bundled', 'trailer', 'cables', 'launches', 'bundle', 'plastic', 'watchlist']

  # Put all the text in each of the 15 sentences files into one big string
  all_text = ''
  for counter in range(1, 16):
    with open("sentences_{}.txt".format(counter), 'r', encoding='utf-8') as file:
      all_text += file.read()

  # tokenize all the sentences
  sentences = sent_tokenize(all_text)

  # create a dictionary with each top term as a key and value is a list of sentences
  my_knowledge_base = {}
  for term in top_10_terms:
    my_knowledge_base[term] = []

  for term in top_10_terms:
    for sent in sentences:
      if term in sent:
        my_knowledge_base[term].append(sent)

  # for x in my_knowledge_base:
  #   print(x)
  #   print(my_knowledge_base[x], '\n\n\n\n')

  # pickle my_knowledge_base
  pickle.dump(my_knowledge_base, open('knowledge_base.p', 'wb'))
  print('The knowledge base was created and then pickled')

# Main
if __name__ == '__main__':
  #  URL representing a topic
  url = 'https://en.wikipedia.org/wiki/Nintendo_Switch'

  # outputs a list of at least 15 relevant URLs and to a file
  urls = web_crawler(url)
  
  # loop through URLs and scrape all text off each page and output to file
  text_scraper(urls)

  # clean up the text from each file and extract sentences to new files
  clean_file()

  # print the top 25-40 terms
  top_40()

  # manually determine the top 10 terms from the top 40 terms, based on my domain knowledge
  print('\nThe top 10 terms determined manually based on my domain knowledge are: nes, snes, kirby, bundled, trailer, cables, launches, bundle, plastic, watchlist\n')
  
  # build and print my knowlege base
  knowledge_base()

  sys.exit(0)