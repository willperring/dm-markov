# This file creates a chain dictionary from the corpus source files
# Some support needs to be added to this for variable length keys

import os, glob, pickle
import markov.MarkovChain as MarkovChain

sources = glob.glob('corpus/*.txt')
print("{0} corpus articles found for dictionary".format(len(sources)))

# This doesn't do anything yet @TODO: implement
keys = input("Enter the number of keys to use (default: 2): ")
keys = keys if keys else 2

# "Terminator" strings
begin = MarkovChain.MarkovChain.begin
end   = MarkovChain.MarkovChain.end

chain = MarkovChain.MarkovChain( int(keys) )
wordcount   = 0
sourcecount = 0

for source in sources:

	sourcefile  = open( source, 'r' )
	sourcetext  = sourcefile.read()
	sourcewords = sourcetext.split()

	sourcewords.append( end )
	sourcecount += 1

	key = (begin,) * int(keys)

	for word in sourcewords:

		chain.addLink( key, word )
		key = key[1:] + (word,)

		wordcount += 1
		print("\rReading source {0}, {1} words added".format(sourcecount, wordcount), end='    ')
	
print("\rScanned {0} souces, {1} words added to dictionary".format(sourcecount,wordcount));

dictionary = input("Enter a save name for the dictionary, or blank to exit: ")

if dictionary is not "":
	savepath = "dictionaries/{0}.dict".format(dictionary)
	pickle.dump( chain, open(savepath, 'wb') )


