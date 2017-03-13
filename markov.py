import markov.MarkovChain as MarkovChain
from markov.common import inputd

dict  = input("Enter dictionary to use: ")
chain = MarkovChain.loadDictionary( dict )

words  = inputd("Number of words to generate", 40)
lines  = inputd("Number of lines to generate", 20)
weight = inputd("Use weighted selections", "N") 

if not chain:
	print("Dictionary '{0}' not found".format(dict))
	quit()

print("Loaded dictionary '{0}'.".format(dict))

for i in range( int(lines) ):
	print(chain.getChain( int(words), weight ), end="\n\n")