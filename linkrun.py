import requests
import json
import re
from BeautifulSoup import BeautifulSoup, SoupStrainer

def ParseJSONData(listOfLinks,dictOfLinks,continueSearchVariable,url):
	urlcont = url + '&gplcontinue='
	r  = requests.get(url)
	data = r.content

	parsedJson = json.loads(data)

	for i in parsedJson['query']['pages'].keys():
		if(parsedJson['query']['pages'][i]['ns'] == 0):
			listOfLinks.append(i)
			dictOfLinks[i] = parsedJson['query']['pages'][i]['title']

	for i in parsedJson.keys():
		if  (i == 'continue'):
			continueSearchVariable = parsedJson['continue']['gplcontinue']
			url1 = urlcont 
			# print(url1)
			ParseJsonDataCont(listOfLinks,dictOfLinks,continueSearchVariable,url1)

def ParseJsonDataCont(listOfLinks,dictOfLinks,continueSearchVariable,url):
	urlcont = url + continueSearchVariable
	r = requests.get(urlcont)
	data = r.content

	parsedJson = json.loads(data)

	for i in parsedJson['query']['pages'].keys():
		if(parsedJson['query']['pages'][i]['ns'] == 0):
			listOfLinks.append(i)
			dictOfLinks[i] = parsedJson['query']['pages'][i]['title']

	# print(urlcont)
	
	for i in parsedJson.keys():
		if  (i == 'continue'):
			continueSearchVariable = parsedJson['continue']['gplcontinue']
			url1 = url 
			# print(urlcont)
			ParseJsonDataCont(listOfLinks,dictOfLinks,continueSearchVariable,url1)

def GetBacklinks(url,continueSearchVariableBacklink,count,LinkNo):
	urlcont = url + '&blcontinue='
	r = requests.get(url)
	data = r.content

	parsedJson = json.loads(data)

	count.append(0)
	count[LinkNo] = count[LinkNo] + len(parsedJson['query']['backlinks'])

	for i in parsedJson.keys():
		if  (i == 'continue'):
			continueSearchVariableBacklink = parsedJson['continue']['blcontinue']
			url1 = urlcont
			# print(urlcont)
			GetBacklinksCont(url1,continueSearchVariableBacklink,count,LinkNo)

def GetBacklinksCont(url,continueSearchVariableBacklink,count,LinkNo):
	urlcont = url + continueSearchVariableBacklink
	r = requests.get(urlcont)
	data = r.content

	parsedJson = json.loads(data)

	count[LinkNo] = count[LinkNo] + len(parsedJson['query']['backlinks'])


	for i in parsedJson.keys():
		if  (i == 'continue'):
			continueSearchVariableBacklink = parsedJson['continue']['blcontinue']
			url1 = url 
			# print(url1 + continueSearchVariableBacklink)
			GetBacklinksCont(url1,continueSearchVariableBacklink,count,LinkNo)

def WikiUrlChecker(urlInput):
	matchObj = re.match( r'https:\/\/en\.wikipedia\.org\/wiki\/.+',urlInput)
	start1 = 0

	if matchObj:
		# print "matchObj.group() : ", matchObj.group()
		if (urlInput.find('/wiki/') != -1):
			start = int(urlInput.find('/wiki/'))
			start = start + 6
			start1 = int(start)
			url = urlInput[start1:]
			url1 = 'https://en.wikipedia.org/w/api.php?action=query&prop=info&inprop=url&format=json&titles='+urlInput[start1:]
			r = requests.get(url1)
			data = r.content

			parsedJson = json.loads(data)

			for i in parsedJson['query']['pages'].keys():
				for j in parsedJson['query']['pages'][i].keys():
					if (j == 'missing'):
						# print "The page for this title doesnt exist"
						return True
	else:
		print "Nothing"

def WikiUrlChecker(urlInput):
	matchObj = re.match( r'https:\/\/en\.wikipedia\.org\/wiki\/.+',urlInput)
	start1 = 0

	if matchObj:
		# print "matchObj.group() : ", matchObj.group()
		if (urlInput.find('/wiki/') != -1):
			start = int(urlInput.find('/wiki/'))
			start = start + 6
			start1 = int(start)
			url = urlInput[start1:]
			url1 = 'https://en.wikipedia.org/w/api.php?action=query&prop=info&inprop=url&format=json&titles='+urlInput[start1:]
			r = requests.get(url1)
			data = r.content

			parsedJson = json.loads(data)

			for i in parsedJson['query']['pages'].keys():
				for j in parsedJson['query']['pages'][i].keys():
					if (j == 'missing'):
						# print "The page for this title doesnt exist"
						return 0
	else:
		return 1

def WikiUrlSeperator(urlInput):
	matchObj = re.match( r'https:\/\/en\.wikipedia\.org\/wiki\/.+',urlInput)
	start1 = 0

	if matchObj:
		# print "matchObj.group() : ", matchObj.group()
		if (urlInput.find('/wiki/') != -1):
			start = int(urlInput.find('/wiki/'))
			start = start + 6
			start1 = int(start)
			url = urlInput[start1:]	
			return url

#####################################################################################################################		

count1 = 1;
count = []
listOfLinks = []
dictOfLinks = {}
continueSearch = False
continueSearchVariable = ''
continueSearchVariableBacklink = ''
start1 = 0

print('Please enter the wikipedia URL:')
urlInput = raw_input()
urlCheck = WikiUrlChecker(urlInput)
if(urlCheck == 0):
	print "The Page does not exist!!Please try another one"
elif(urlCheck == 1):
	print "Please enter a valid Wikipedia domian url"
else:
	# print(WikiUrlSeperator(urlInput))
	url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&generator=links&gpllimit=max&titles='+WikiUrlSeperator(urlInput)
	urlbacklink = "https://en.wikipedia.org/w/api.php?action=query&list=backlinks&format=json&bllimit=max&blpageid="

	print('Extracting Links')
	ParseJSONData(listOfLinks,dictOfLinks,continueSearchVariable,url)
	counttest = 0
	for i in listOfLinks:
		if(int(i) > 0):
			counttest = counttest+1
				
	print 'Number of Links = %s' %counttest

	for i in listOfLinks:
		if(int(i) > 0):
			urlback = urlbacklink + i
			print 'Extracting number of backlinks for link no = %s with pageID = %s' %(count1,i)
			GetBacklinks(urlback,continueSearchVariableBacklink,count,count1-1)
			count1 = count1+1
	flag = 0
	flag1 = 0
	for i in range(0,len(count)):
		if(count[i] >= flag):
			flag1 = i;
			flag = count[i]

	urlpop = 'https://en.wikipedia.org/w/api.php?action=query&prop=info&inprop=url&format=json&pageids=' + listOfLinks[flag1]
	r = requests.get(urlpop)
	data = r.content

	parsedJsonDataPop = json.loads(data)

	PopUrl = parsedJsonDataPop['query']['pages'][listOfLinks[flag1]]['fullurl']

	r  = requests.get(urlInput)
	data = r.content

	start = PopUrl.find('/wiki/') 
	Chkurl = PopUrl[start:]
	soup = BeautifulSoup(data)
	print "The most popluar links are can be accesed using the following words"
	for a in soup.findAll('a', href=Chkurl):
		print(a.string)


	print 'The most popular link in %s' %PopUrl






