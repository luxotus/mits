from summarizer import get_summaries_keywords, print_summaries_keywords


# Grab and clean text
sources = [
  'https://plato.stanford.edu/entries/life-meaning/',
  'https://en.wikipedia.org/wiki/Meaning_of_life',
  'https://qz.com/1310792/the-secret-to-a-meaningful-life-is-simpler-than-you-think/',
]

results = get_summaries_keywords(sources)
print_summaries_keywords(results)