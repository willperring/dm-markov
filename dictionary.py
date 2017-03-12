import os, glob, pickle
import markov.MarkovChain as MarkovChain

sources = glob.glob('corpus/*.txt')
print("{0} corpus articles found for dictionary".format(len(sources)))

keys = input("Enter the number of keys to use (default: 2): ")
keys = keys if keys else 2

begin = MarkovChain.MarkovChain.begin
end   = MarkovChain.MarkovChain.end

chain = MarkovChain.MarkovChain()
wordcount   = 0
sourcecount = 0

for source in sources:

	sourcefile  = open( source, 'r' )
	sourcetext  = sourcefile.read()
	sourcewords = sourcetext.split()

	prev1 = begin
	prev2 = begin

	sourcewords.append( end )
	sourcecount += 1

	for word in sourcewords:

		key = ( prev2, prev1 )
		chain.addLink( key, word )
		prev2 = prev1
		prev1 = word

		wordcount += 1
		print("\rReading source {0}, {1} words added".format(sourcecount, wordcount), end='    ')
	
print("Scanned {0} souces, {1} words added to dictionary");

dictionary = input("Enter a save name for the dictionary, or blank to exit: ")

if dictionary is not "":
	savepath = "dictionaries/{0}.dict".format(dictionary)
	pickle.dump( chain, open(savepath, 'wb') )


