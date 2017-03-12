import pickle, os, random

class MarkovChain:

	begin = "<BEGIN>"
	end   = "<END>"
	
	def __init__( self, depth=2 ):
		self.links = {}

	def addLink( self, key, word ):
		if key not in self.links:
			self.links[key] = MarkovLink( word )
		else:
			self.links[key].addWord( word )

	def dump( self ):
		return self.links

	def getChain( self, length=25, weighted=False ):

		w1 = self.begin
		w2 = self.begin

		words = []

		while (len(words) < length):

			key = (w1, w2)
	
			if key in self.links:
				word = self.links[key].getWordWeighted() if weighted else self.links[key].getWordUniform()
				words.append(word)
				w1 = w2
				w2 = word
			else:
				break

		return " ".join( words )


class MarkovLink:
	
	def __init__( self, word ):
		self.words = {}
		self.words[word] = 1

	def addWord( self, word ):
		if word not in self.words:
			self.words[word] = 1
		else:
			self.words[word] += 1

	def getWordUniform( self ):
		return random.choice( list( self.words.keys() ))

	def getWordWeighted( self ):
		pass

	def __str__( self ):
		return str(self.words)

	def __repr__( self ):
		return str(self.words)

def loadDictionary( dictionary ):
	
	path = os.path.relpath("dictionaries/{0}.dict".format(dictionary))
	
	if not os.path.isfile( path ):
		return False
	return pickle.load( open(path, 'rb') )


