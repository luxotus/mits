import bs4 as bs
import urllib.request
from re import sub
from heapq import nlargest
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer

def extract_word_frequencies(text, with_stem=True):
  ''' Measures how often words appear in a given text '''

  stop_words = stopwords.words('english')
  ps = PorterStemmer()
  word_frequencies = {}

  for word in word_tokenize(text.lower()):
    if with_stem:
      word = ps.stem(word)

    if word not in stop_words:
      if word not in word_frequencies.keys():
        word_frequencies[word] = 1
      else:
        word_frequencies[word] += 1

  return word_frequencies

def extract_keywords(text, keywords_count=5):
  ''' Grabs the top # of keywords of a body of text '''

  source_text = sub(r'\s+', ' ', sub(r'\[[0-9]*\]', ' ', text))
  cleaned_text = sub(r'\s+', ' ', sub('[^a-zA-Z]', ' ', source_text))
  word_frequencies = extract_word_frequencies(cleaned_text, False)

  keywords = nlargest(keywords_count, word_frequencies, key=word_frequencies.get)

  return keywords

def get_word_frequencies(text):
  ''' Measures frequency of a word based on the word that occurs most frequently '''

  word_frequencies = extract_word_frequencies(text)
  maximum_frequency = max(word_frequencies.values())

  for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

  return word_frequencies

def score(sentence_list, word_frequencies):
  ''' Scores sentences based on word occurrences '''

  scores = {}
  max_word_count = 20 # per sentence
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
  ''' Extracts relevant text from beautifulSoup '''

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

def get_source_text(sources):
  ''' Turns article links into a single body of text '''

  source_text = ''

  for source in sources:
    scraped_data = urllib.request.urlopen(source)
    source_data = bs.BeautifulSoup(scraped_data.read(),'lxml')
    source_text += text_from_soup(source_data)

  return source_text

def get_summary(source_text, sentence_count=7):
  ''' Summarizes a body of text '''

  # Removing square brackets and extra spaces then special characters and digits
  source_text = sub(r'\s+', ' ', sub(r'\[[0-9]*\]', ' ', source_text))
  cleaned_text = sub(r'\s+', ' ', sub('[^a-zA-Z]', ' ', source_text))

  sentence_list = sent_tokenize(source_text)
  word_frequencies = get_word_frequencies(cleaned_text)
  sentence_scores = score(sentence_list, word_frequencies)

  summary = ' '.join(nlargest(sentence_count, sentence_scores, key=sentence_scores.get))

  return summary

def get_summaries(sources, sentence_count_per_source=7):
  ''' Gets all summaries from the list of URL sources '''

  summaries = {
    'discrete': {},
    'joined': get_summary(get_source_text(sources), sentence_count_per_source)
  }

  for source in sources:
    summaries['discrete'][source] = get_summary(get_source_text([source]), sentence_count_per_source)

  return summaries

def get_keywords(sources, keywords_count_per_source=5):
  ''' Gets all keywords from the list of URL sources '''

  keywords = {
    'discrete': {},
    'joined': extract_keywords(get_source_text(sources), keywords_count_per_source)
  }

  for source in sources:
    keywords['discrete'][source] = extract_keywords(get_source_text([source]), keywords_count_per_source)

  return keywords

def get_summaries_keywords(sources, keywords_count_per_source=5, sentence_count_per_source=7):
  ''' Gets all the summaries and keywords from the list of URL sources '''

  results = {
    'summaries': get_summaries(sources, sentence_count_per_source),
    'keywords': get_keywords(sources, keywords_count_per_source),
  }

  return results

def print_summaries(summaries):
  ''' Prints all summaries '''

  for key in summaries['discrete']:
    print(key)
    print(summaries['discrete'][key])
    print('\n')

  print('-------- Joined --------')
  print(summaries['joined'])

def print_keywords(keywords):
  ''' Prints all Keywords '''

  for key in keywords['discrete']:
    print(key)
    print(keywords['discrete'][key])
    print('\n')

  print('-------- Joined --------')
  print(keywords['joined'])

def print_summaries_keywords(sk):
  ''' Prints all summaries and keywords '''

  print_keywords(sk['keywords'])
  print('\n')
  print_summaries(sk['summaries'])