# This file is a little rough around the edges
# It's primarily just a diagnostic tool for checking
# The status of the dictionary files

import markov.MarkovChain as MarkovChain
from markov.common import inputd

dict  = input("Enter dictionary to use: ")
chain = MarkovChain.loadDictionary( dict )

def stats( chain ):
	print("Key Depth:       {0}".format(chain.depth))
	print("Normalised keys: {0}".format(chain.normalise))
	print("Key count:       {0}".format(len(chain.links)))
	print()

def output( chain ):
	chain.printout()
	print()

def lookup( chain ):
	keys = chain.depth

	key = ()
	for i in range(keys):
		value = input("Enter key {0}: ".format(i))
		key = key + (value,)

	print()

	link = chain.getLink( key )
	if link is None:
		print("No valid entry found for key {0}".format(key))
	else:
		print(key)
		print(link)

	print()

def countopts( chain ):
	counts = {}
	total  = len(chain.links)

	for key in chain.links:
		workopts  = len(chain.links[key].words)
		
		if workopts > 10:
			roundopts = workopts - ( workopts%10 ) 
		else:
			roundopts = workopts

		if not roundopts in counts:
			counts[roundopts] = 0
		counts[roundopts] += 1

	sortedcounts = sorted( counts.items() )
	sortedcounts.reverse()

	for opts,count in sortedcounts:
		bracket = str(opts) if opts < 10 else "{0}-{1}".format(opts, opts+9)
		print("{0:10} options: {1:6} keys ( {2:3}% )".format(bracket, count, (count*100)//total))

	print()

functionmap = {
	1: stats,
	2: output,
	3: lookup,
	4: countopts
}

cmd = "-"
while cmd != "":
	print("Options:")
	print()
	print("1. Dictionary Stats")
	print("2. Output full dictionary")
	print("3. Key Lookup")
	print("4. Option Count")
	print()
	print("Or press enter to quit")
	print()
	cmd = input("Enter choice: ")

	if cmd == "":
		quit()

	if int(cmd) in functionmap:
		print()
		functionmap[ int(cmd) ]( chain )
	elif cmd != "":
		print("Option {0} not found".format(cmd))

	print()


