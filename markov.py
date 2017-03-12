import markov.MarkovChain as MarkovChain

dict  = input("Enter dictionary to use: ")
chain = MarkovChain.loadDictionary( dict )

if not chain:
	print("Dictionary '{0}' not found".format(dict))
	quit()

print("Loaded dictionary '{0}'.".format(dict))

for i in range(20):
	print(chain.getChain( 40 ), end="\n\n")