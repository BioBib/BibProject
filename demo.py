from hammock import Hammock as Github
import json
import urllib
import datetime
import sys
import base64
from pprint import pprint
from bs4 import BeautifulSoup

#soup = BeautifulSoup(urllib.urlopen('www.google.com/'))
html = urllib.urlopen('https://news.google.com/?ar=1403895110')
#h = html.decode("utf-8")
soup = BeautifulSoup(html)

#get the string in all <span> tags w/ class "titletext"
spans = soup.find_all('span', attrs={'class':'titletext'})

#get time 
#time = datetime.datetime.now().strftime("%m/%d/%y %H:%M")
time = datetime.datetime.now().strftime("%H:%M")
filename = time + '.txt'
print filename

#write all titletexts to a new file w/title of time
file = open(filename, 'w')

for span in spans:
	if span.string:
		#deal with unicode problem (not very efficiently)
		if __name__ == "__main__":
			reload(sys)
			sys.setdefaultencoding("utf-8")
		#write each headline to new line	
		file.write(span.string + "\n")

file.close()

#upload file to github

with open( filename, "rb") as text_file:
	encoded_string = base64.b64encode(text_file.read())

data = {'message':'Adding "'+filename+'".',
      'committer':{'name':'Madeleine Corneli',
                   'email':'mlc299@cornell.edu'},
      'content':encoded_string,
      'branch':'master'}

github = Github('https://api.github.com')
user = 'maddyloo'
password = raw_input("Github password:")
repo = 'miniBibServer'
resp = github.repos(user, repo).contents(filename).PUT(
	auth = (user, password),
	headers = {'Content-type': 'textfile'},
	data = json.dumps(data))

pprint (vars(resp))

#edit to test git :/