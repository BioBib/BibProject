from hammock import Hammock as Github
import json
import urllib
import sys
import base64
from pprint import pprint
import os
import content_short
import urllib
import subprocess, os

github = Github('https://api.github.com')
owner = 'maddyloo'
repo = 'BibProject'
path = 'tex_files/'
password = 'ef6a10e47a58a9b7a2a72ded2d292907354561d8'  #BibPoject token
#Aitken%2C%20Alexander%20C..tex

#loops through url list and downloads a copy of the tex file
for item in content_short.url_list:
	name = item.rpartition('/')
	#need to deal with replacing special characters in names (before or after replacing %20?)
	# ex:  ./tex_files/Ai%CC%88t-Sahalia, Yacine.tex created
	git_name = urllib.unquote_plus(name[2].replace('%20', ' '))
	filename = './tex_files/' + git_name
	urllib.urlretrieve(item, filename)
	print filename + ' created'
	#  compare each file with git diff FILE via system call
	diff = subprocess.check_output(["git","diff",git_name], cwd = "tex_files")
	#print diff
	#  compare each file with git diff FILE via system call
	if (diff != ''):
		#  IF difference, git commit FILE, git push via system call
		commit = subprocess.call(["git","commit",filename,"-m","\"update\""])
		sha = subprocess.call(["git","rev-parse","HEAD"])
		print sha
		#git push
		#  and submit pull request via API call
		
'''
#GET /repos/:owner/:repo/contents/:path
resp = github.repos(owner, repo).contents(path).GET(
	auth = (owner, password),
	headers = {'Content-type': 'textfile'})
	#data = json.dumps(data))

#j = json.loads(resp.text)
j = resp.json()
print(base64.b64decode(j['content']))
#pprint(j)
'''