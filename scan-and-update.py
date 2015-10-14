import os, sys
import subprocess
import filecmp
import urllib2

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

# After checking out the material from Github, we can see whether any of those files changed.
# This will include material that has been modified by the IMS editor by hand
# (As well as anything from the distributed update that has been pulled in.)
changed_tex_files = subprocess.Popen(["git", "diff-index", "--name-only", "HEAD~1"],cwd="/bibserver/ims_legacy/BibProject/",stdout=subprocess.PIPE).communicate()[0].splitlines()

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

# Double check (debugging code)
print "Changed tex files:"
pprint(changed_tex_files)

import read_member_index
urllist = read_member_index.read_member_index()

## Now go through this script, which works as follows:

## Step 1: download copies of all files in our list

## Step 2: compare downloaded files to local copies

local_commit_flag = False

for item in urllist:
    member_id=item[0]
    # print "person name: " + member_id
    source=item[1]
    # The only thing to do when the member's information is stored in the Git repository is to produce some new HTML
    if (source[:11] == "./tex_files"):
        relative_path = source[2:]
        # check that the path is correct; we might want 'source' here.
        if (relative_path not in changed_tex_files):
            print relative_path + " is not in list of changed tex files."
            break
        else:
            local_filename = "/bibserver/ims_legacy/BibProject/tex_files/" + member_id + ".tex"
            htmlcontent = ims_legacy.make_one(local_filename)
            distributed_update.make_commit("master","new_html_files",member_id + ".html",htmlcontent)
            with open("/bibserver/ims_legacy/WorkingDirectory/"+member_id+".json", "r") as f:
                jsonstring = f.read()
                distributed_update.make_commit("master","json_files",member_id + ".json",jsonstring)
    else:
        upstream_filename = urllib2.unquote(source.rsplit("/",1)[1])

        try: 
            content = urllib2.urlopen(source).read()
        except urllib2.HTTPError, e:
            # we could do some more sophisticated logging here, and throughout
            print('HTTPError = ' + str(e.code))
        else:

            # Now we need to compare the checked out version from Git...
            local_filename = "/bibserver/ims_legacy/BibProject/tex_files/" + member_id + ".tex"
            # The latest upstream version...
            new_filename = "/bibserver/ims_legacy/WorkingDirectory/" + member_id + ".tex"
            # ...and the most recently checked upstream version
            stash_filename = "/bibserver/ims_legacy/StashDirectory/" + member_id + ".tex"

            with open(new_filename, "w") as new_file:
                # the comparison won't work unless the file has been written and closed!
                new_file.write(content)
                new_file.close()
            # val will be True if the files are the same, and False if they differ.
            val = filecmp.cmp(new_filename, local_filename)
            print "local filename:" + local_filename
            print "upstream file:" + new_filename
            print "Upstream the same as local?: " + str(val)
            # print "content:" + content[:36]
            if (not(val)):
                # compare again, against the stash...
                # if it exists.
                stashval = False
                if os.path.isfile(stash_filename):
                    stashval = filecmp.cmp(new_filename, stash_filename)
                    print "stash filename:" + stash_filename
                    print "Upstream the same as stash?: " + str(stashval)
                    #print "local filename:" + local_filename
                if (not(stashval)):
                    # if there is a (further) change, write to the stash
                    with open(stash_filename, "w") as new_stash_file:
                        new_stash_file.write(content)
                        new_stash_file.close()
                    basename = re.sub('[ ,.]', '', member_id)

                    # this step should be conditional in a smart way
                    try: distributed_update.make_branch(basename)
                    except: pass

                    distributed_update.make_commit(basename,"tex_files",member_id + ".tex",content)

                    # we should probably update the HTML automatically as well, but maybe
                    # just what we do about it will depend on what IMS wants...

                    # I guess that part can wait until after deploying this version,
                    # it's not going to require a major change to the code.

                    # Something like this:
                    htmlcontent = ims_legacy.make_one(stash_filename)
                    distributed_update.make_commit(basename,"new_html_files",member_id + ".html",htmlcontent)
                    with open("/bibserver/ims_legacy/WorkingDirectory/"+member_id+".json", "r") as f:
                        jsonstring = f.read()
                        distributed_update.make_commit(basename,"json_files",member_id + ".json",jsonstring)
                    distributed_update.make_pull_request(member_id,basename)
                else:
                    sys.stdout.write('.')

# If we've prepared any commits changing HTML files, then we should
# push them... Oh wait, actually the commits are just made directly
# without need to push.  Let's see if this works.

print "done."
