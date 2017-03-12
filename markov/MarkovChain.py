import pickle, os, random

class MarkovChain:
	"""
	Markov Chain class
	"""

	begin = "<BEGIN>"
	end   = "<END>"
	
	def __init__( self, depth=2 ):
		"""
		Construct a new Chain

		:param depth Number of words to use as the key
		"""
		self.links = {}
		self.depth = depth

	def addLink( self, key, word ):
		"""
		Add a word to the Chain

		:param key  Tuple to use as key
		:param word Word to add to Chain
		"""

		if len(key) < self.depth:
			return False

		if key not in self.links:
			self.links[key] = MarkovLink( word )
		else:
			self.links[key].addWord( word )

	def dump( self ):
		return self.links

	def getChain( self, length=25, weighted=False ):
		"""
		Compile a Makarov Chain

		:param length Number of words in Chain
		:param weighted True to use weighted guesses, False for uniform probability
		"""

		words = []
		key   = (self.begin,) * self.depth

		while (len(words) < length):
	
			if key in self.links:
				word = self.links[key].getWordWeighted() if weighted else self.links[key].getWordUniform()
				words.append(word)
			else:
				break

			key = key[1:] + (word,)

		return " ".join( words )


class MarkovLink:
	"""
	Individual 'link' in a Makarov Chain
	"""
	
	def __init__( self, word ):
		"""
		Create a new link

		:param word Word to add to link
		"""
		self.words = {}
		self.words[word] = 1

	def addWord( self, word ):
		"""
		Add a word to an existing Chain

		:param word Word to add
		"""
		if word not in self.words:
			self.words[word] = 1
		else:
			self.words[word] += 1

	def getWordUniform( self ):
		"""
		Get a new word for the Chain

		Uniform weighting treats all potential followers as equally likely
		"""
		return random.choice( list( self.words.keys() ))

	def getWordWeighted( self ):
		"""
		Get a new word for the chain, weighted by occurences

		This function treats each option as having a different weighting, depending
		on how many times the words has occured in the source corpus
		TODO: implement
		"""
		pass

	def __str__( self ):
		return str(self.words)

	def __repr__( self ):
		return str(self.words)

def loadDictionary( dictionary ):
	"""
	Load a Markov Chain from disk using a prebuilt dictionary
	"""
	
	path = os.path.relpath("dictionaries/{0}.dict".format(dictionary))
	
	if not os.path.isfile( path ):
		return False
	return pickle.load( open(path, 'rb') )


