Main Files

| Filename | Description |
|----------|-------------|
| corpus.py| Scrapes the Daily Mail website homepage for all article links, and then crawls each of them in turn, saving the output to a simple text format|
| dictionary.py | Creates a dictionary file from the saved corpus documents |
| markov.py | Generates Markov chains from a specified dictionary |

Dependencies:

* Python 3.2+
* BeautifulSoup4
