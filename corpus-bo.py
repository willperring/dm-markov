# This script generates a number of corpus text files, 
# By crawling the Daily Mail homepage, finding links to 
# articles, and then saving them to disk, stripped of HTML.

import re, glob, os, gzip
import urllib.request
from bs4 import BeautifulSoup

# Initial homepage
host    = "http://obamaspeeches.com/"
request = urllib.request.urlopen(host)
page    = request.read()
soup    = BeautifulSoup( page, 'html.parser' )

# Pattern to locate article URLs
articlepattern = re.compile('href="(/?[A-Za-z0-9]?[0-9]{0,3}[^/"]*\.htm)"')
articleurls    = articlepattern.findall( str(soup) )

print( "Crawling Barack Obama Speeched homepage" )
print( "{0} Speech URLs found on homepage".format(len(articleurls)) )

idlist    = []
crawled   = 0
skipped   = 0
errors    = 0

for url in articleurls:
	
	if not url.startswith('/'):
		url = "/" + url

	id = url[1:-4]

	# An in-memory list of articles we've crawled today
	if id in idlist:
		skipped += 1
		continue

	# Check if we already have a disk entry for this article
	idglob = glob.glob('corpus/obama/{0}.*'.format(id))
	if( len(idglob) > 0 ):
		skipped += 1
		continue

	print("\rCrawling article {0} / {1}...    "
		.format(crawled+skipped+errors, len(articleurls)), end='  ')

	articlerequest = urllib.request.urlopen( host + url )
	articlebody    = articlerequest.read()

	soup    = BeautifulSoup( articlebody, 'html.parser' )
	content = soup.select('table td font p font')
	if not len(content):
		content = soup.select('table table td font')

	# If we can't locate the main content, log the error
	if not content or (len(content) < 15):
		skipped += 1
		continue


	filepath = "corpus/obama/{0}".format(id)
	lockfile = open(filepath + ".lock", 'w')
	lockfile.write('Crawling...')
	lockfile.close()

	bodytext = " ".join( str(tag.text).strip() for tag in content )
	bodytext = bodytext.replace("\n", "")
	bodytext = re.sub( '\s+', ' ', bodytext ).strip()

	outputfile = open(filepath+'.txt', 'w')
	outputfile.write( bodytext )

	# Clean up the lock file
	os.remove(filepath + '.lock')
	idlist.append(id)
	crawled += 1

print("\rURL Summary: {0} crawled, {1} skipped, {2} errors".format(crawled,skipped,errors))

