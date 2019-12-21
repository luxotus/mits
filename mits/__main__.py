from summarizer import get_summary


# Grab and clean text
sources = [
  'https://en.wikipedia.org/wiki/Artificial_intelligence',
]


print(get_summary(sources))