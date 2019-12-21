from summarizer import get_summaries


# Grab and clean text
sources = [
  'https://en.wikipedia.org/wiki/Artificial_intelligence',
]

summaries = get_summaries(sources)

for summary in summaries:
  print(summary)
  print('-'*100)