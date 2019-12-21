from summarizer import get_summaries, print_summaries


# Grab and clean text
sources = [
  'https://plato.stanford.edu/entries/life-meaning/',
  'https://en.wikipedia.org/wiki/Meaning_of_life',
  'https://qz.com/1310792/the-secret-to-a-meaningful-life-is-simpler-than-you-think/',
]

summaries = get_summaries(sources)
print_summaries(summaries)