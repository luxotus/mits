# Multiple Input Text Summarizer
Mits was created for bloggers that researching a new topic and want to quickly get a better understanding of a collection of articles. All user has to do is provide a list of URLS to the articles of interest and MITS will output summaries of each article and a combined summary of all the articles together. Also went ahead and included a list of the top keywords for each article and all the articles together. Just make sure to keep in mind this is only intended as a research tool, and not to reword/rewrite articles for you.

## Usage

```python
import summarizer

example_links = [
  'https://plato.stanford.edu/entries/life-meaning/',
  'https://en.wikipedia.org/wiki/Meaning_of_life',
  'https://qz.com/1310792/the-secret-to-a-meaningful-life-is-simpler-than-you-think/',
]

summarizer.get_summaries(sources) # returns summaries
summarizer.get_keywords(sources) # returns keywords
summarizer.get_summaries_keywords(sources) # returns both summaries and keywords
```

## License
[MIT](https://github.com/luxotus/mits/blob/master/LICENSE)