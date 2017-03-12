# This script generates a number of corpus text files, 
# By crawling the Daily Mail homepage, finding links to 
# articles, and then saving them to disk, stripped of HTML.

import re, glob, os
import urllib.request
from bs4 import BeautifulSoup

# Initial homepage
host    = "http://www.dailymail.co.uk"
request = urllib.request.urlopen(host)
page    = request.read().decode('utf-8')

# Pattern to locate article URLs
articlepattern = re.compile('href="(/[^/"]*/article-\d*/[^/"]*)"')
articleurls    = articlepattern.findall(page)

print( "Crawling Daily Mail homepage" )
print( "{0} Article URLs found on homepage".format(len(articleurls)) )

idpattern = re.compile('article-(\d*)')
idlist    = []
crawled   = 0
skipped   = 0
errors    = 0

for url in articleurls:
	
	# Things prefixed '/home' are generic pages
	if url.startswith("/home"):
		skipped += 1
		continue

	# If we can't extract the ID, we can't prevent double-crawling
	idmatch = idpattern.search( url )
	if not idmatch:
		errors += 1
		continue

	id = idmatch.group(1)

	# An in-memory list of articles we've crawled today
	if id in idlist:
		skipped += 1
		continue

	# Check if we already have a disk entry for this article
	idglob = glob.glob('corpus/{0}.*'.format(id))
	if( len(idglob) > 0 ):
		skipped += 1
		continue

	print("\rCrawling article {0} - {1} / {2}...    "
		.format(id, crawled+skipped+errors, len(articleurls)), end='  ')
	articlerequest = urllib.request.urlopen( host + url )
	articlebody    = articlerequest.read().decode('utf-8')

	soup    = BeautifulSoup( articlebody, 'html.parser' )
	modules = soup.select('.moduleFull')
	if modules:
		[ m.decompose() for m in modules ]

	content = soup.find(id='js-article-text')

	# If we can't locate the main content, log the error
	if not content:
		errors += 1
		continue

	filepath = "corpus/{0}".format(id)
	lockfile = open(filepath + ".lock", 'w')
	lockfile.write('Crawling...')
	lockfile.close()

	title = content.find('h1').next
	body  = content.select('div[itemprop="articleBody"] p')

	bodytext = " ".join( str(tag.text) for tag in body )
	
	outputfile = open(filepath+'.txt', 'w')
	outputfile.write( title + " " + bodytext )

	# Clean up the lock file
	os.remove(filepath + '.lock')
	idlist.append(id)
	crawled += 1

print("URL Summary: {0} crawled, {1} skipped, {2} errors".format(crawled,skipped,errors))

