class MarkovChain:
	
	def __init__( self, depth=2 ):
		self.links = {}

	def addLink( self, key, word ):
		if key not in self.links:
			self.links[key] = MarkovLink( word )
		else:
			self.links[key].addWord( word )

	def consume( self, corpus ):
		nonword = "\n"

	def dump( self ):
		print( self.links )

class MarkovLink:
	
	def __init__( self, word ):
		self.words = {}

	def addWord( self, word ):
		if word not in self.words:
			self.words[word] = 1
		else:
			self.words[word] += 1


