import bs4 as bs
import urllib.request
from re import sub
from heapq import nlargest
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer

def get_word_frequencies(text):
  stop_words = stopwords.words('english')
  ps = PorterStemmer()
  word_frequencies = {}

  for word in word_tokenize(text):
    word = ps.stem(word)

    if word not in stop_words:
      if word not in word_frequencies.keys():
        word_frequencies[word] = 1
      else:
        word_frequencies[word] += 1

  maximum_frequency = max(word_frequencies.values())

  for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

  return word_frequencies

def score(sentence_list, word_frequencies):
  scores = {}
  max_word_count = 30 # per sentence
  ps = PorterStemmer()

  for sent in sentence_list:
    for word in word_tokenize(sent.lower()):
      word = ps.stem(word)

      if word in word_frequencies.keys() and len(sent.split(' ')) < max_word_count:
        if sent in scores.keys():
          scores[sent] += word_frequencies[word]
        else:
          scores[sent] = word_frequencies[word]

  return scores

def text_from_soup(source_data):
  tags = [
    'p',
    'h1',
  ]
  source_text = ""

  for t in tags:
    elements = source_data.find_all(t)

    for el in elements:
      source_text += el.text

  return source_text

def get_summary(source):
  scraped_data = urllib.request.urlopen(source)
  source_data = bs.BeautifulSoup(scraped_data.read(),'lxml')
  source_text = text_from_soup(source_data)

  # Removing square brackets and extra spaces then special characters and digits
  source_text = sub(r'\s+', ' ', sub(r'\[[0-9]*\]', ' ', source_text))
  cleaned_text = sub(r'\s+', ' ', sub('[^a-zA-Z]', ' ', source_text))

  sentence_list = sent_tokenize(source_text)
  word_frequencies = get_word_frequencies(cleaned_text)
  sentence_scores = score(sentence_list, word_frequencies)
  sentence_count = 7

  summary = ' '.join(nlargest(sentence_count, sentence_scores, key=sentence_scores.get))

  return summary

def get_summaries(sources):
  summaries = []

  for source in sources:
    summaries.append(get_summary(source))

  return summaries