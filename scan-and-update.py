import os, sys
import subprocess
import filecmp
import urllib

from hammock import Hammock as Github
import json
import base64
import re

# Make sure to update the repo's contents before we start
# Otherwise comparisons won't make sense.
# Note, need to make sure that the cron user has permissions, shouldn't
# be a problem because I've added the script to the crontab for "joe"
# and joe has access to the /bibserver/ directory.
p = subprocess.Popen(["git", "pull"],cwd="/bibserver/ims_legacy/BibProject/")
p.wait()

# A checked out version of miniBibServer
lib_path = os.path.abspath('/bibserver/ims_legacy/miniBibServer/')
sys.path.append(lib_path)

# Subdirectory containing functions for doing the distributed update operation
lib_path = os.path.abspath('/bibserver/ims_legacy/miniBibServer/github_api_stuff/')
sys.path.append(lib_path)

# A checked out version of the BibProject
lib_path = os.path.abspath('/bibserver/ims_legacy/BibProject/')
sys.path.append(lib_path)

import ims_legacy
import distributed_update

from pprint import pprint

# This file will contain the list of names and URLs of source material.
# (It needs to be maintained by the IMS editor.)
## For convenience of the IMS editor we no longer load the list of members from
##  python data, but parse a tab-separated file, index.txt, so the following line is not needed:
# import ims_sources
## and instead we run this:

import read_member_index
urllist = read_member_index.read_member_index()

## Now go through this script, which works as follows:

## Step 1: download copies of all files in our list

## Step 2: compare downloaded files to local copies

for item in urllist:
    member_id=item[0]
    # print "person name: " + member_id
    source=item[1]
    # Maybe the only thing to do in this case is produce some new HTML,
    # assuming we keep "staged" and "working" copies separate.  But as
    # a first step, let's assume there's nothing to do in this case, and
    # we just need to process the upstream files.
    if (source[:9] == "tex_files"):
        upstream_filename = urllib.unquote(source.rsplit("/",1)[1])
        # print "filename:" + upstream_filename
        distributed_update.check_local(source)
    else:
        upstream_filename = urllib.unquote(source.rsplit("/",1)[1])

        try: 
            content = urllib.urlopen(source).read()
        except urllib2.HTTPError, e:
            # we could do some more sophisticated logging here, and throughout
            print('HTTPError = ' + str(e.code))
        else:
            local_filename = "/bibserver/ims_legacy/BibProject/tex_files/" + member_id + ".tex"
            new_filename = member_id + ".tex"
            with open(new_filename, "w") as new_file:
                # the comparison won't work unless the file has been written and closed!
                new_file.write(content)
                new_file.close()
            # val will be True if the files are the same, and False if they differ.
            val = filecmp.cmp(member_id + ".tex", local_filename)
            #print "local filename:" + local_filename
            #print "new filename:" + new_filename
            #print "content:" + content[:36]
            if (not(val)):
                print new_filename + " differs."
                basename = re.sub('[ ,.]', '', member_id)
                distributed_update.make_branch(basename)
                distributed_update.make_commit(basename,"tex_files",new_filename,content)

                # we should probably update the HTML automatically as well, but maybe
                # just what we do about it will depend on what IMS wants...

                # I guess that part can wait until after deploying this version,
                # it's not going to require a major change to the code.

                # Something like this:
                htmlcontent = ims_legacy.make_one("/bibserver/ims_legacy/"+new_filename)
                htmlname = unicode(new_filename.split('.tex',1)[0],'utf-8')+".html"
                distributed_update.make_commit(basename,"new_html_files",htmlname,htmlcontent)
                distributed_update.make_pull_request(new_filename,basename)
            else:
                sys.stdout.write('.')

print "done."
