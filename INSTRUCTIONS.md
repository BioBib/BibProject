# The basic idea

This repository helps distribute the task of managing public
biographic profiles of members of the Institute of Mathematical
Stastics (IMS).  TeX files containing biographical data can be updated
remotely by IMS members or their representatives, and changes will be
pulled in here once they are approved by the IMS editor.  The
information can then be moved to the IMS website.

## Tips on formatting TeX files

TeX files should be written following the standard outlined in the
accompanying [user docs](https://github.com/maddyloo/miniBibServer/raw/master/docs/imscv-style.pdf).

## Webpage for testing for IMS members

http://ims.metameso.org/ is a webpage that can be used by IMS members
to test their TeX files and see the generated HTML.

# For the IMS editor

To use the BibProject code locally, check out the code from github:

```sh
git clone git@github.com:BioBib/BibProject.git
```

The first thing to look at is:
[`index.txt`](https://github.com/BioBib/BibProject/blob/master/index.txt).

(Note, this file can be edited over the web if you find that simpler.
Some other interaction steps described below require the use of the
web interface.  However, for now, these instructions proceed under the
assumption that you are using a command line version of Git for
editing purposes.  The actual underlying operations are essentially
the same in either case.)

# The automated component

A script runs every day at 1AM UK time, via the following crontab
entry in joe's directory on li311-58.members.linode.com:

```
0 1 * * * python /bibserver/ims_legacy/scan-and-update.py
```

Its facilitates distributed updating of this Github repository.

The first thing it does when it runs is it pulls in the latest version
of `index.txt` from the BibProject repository to the server where it
runs.  It then starts reading the paths and URLs stored in this file,
and makes pull requests when these differ from the content in the
`master` branch.  All of this will become more clear later on in
these instructions.

# Maintaining the index

Let's have a look at the
[`index.txt`](https://github.com/BioBib/BibProject/blob/master/index.txt#L33)
file now.

You'll see that there is a very long list of IMS member IDs, and most
of them are currently associated to files that are stored in the Git
repository, specifically in the `./tex_files` directory).  For
illustrative purposes, the last line is a fictitious person, who is
associated to a tex file stored separately on my webpage, 
[line 1080](https://github.com/BioBib/BibProject/blob/master/ims_sources.py#L33)
of the file:

```
public__john_q                	http://metameso.org/~joe/jqp.tex
```

The IMS editor can update this file to associate any of the tex
sources with remote URLs (or to point back to files in this repository).
Remote files will typically be maintained by IMS members or their representatives.

Try that now, by

1. Copying a tex file from the `./tex_files` directory to some
publicly-accessible webpage that you control, and
2. Changing the corresponding entry in `index.txt` to point to that
   URL.

You can also use a `%` sign at the beginning of the line to add
comments or to comment out entries (you will eventually want to remove
the illustrative entry for "John Q. Public").

# Working with Git and Github

I call the example file you've put on your own webpage the "remote
file."

In order to make the updated index accessible to the server, you must
add, commit, and push the file to Github.

```
git add ims_sources.py
git commit -m "A demonstration of remote editing."
git push
```

The next time the `scan-and-update.py` script runs, it will find the
.tex source for that member on the webpage where you put it.  It will
check to see if it is different from the most current version stored
in the repository.

If you haven't changed the remote file, the script won't find any
difference, and nothing will happen.  So, go ahead and make a change
to the file now, even if it's just adding in a new `%`'ed comment
line.  You don't have to update the Github repository again, because
it already knows where to look for this file.

When `scan-and-update.py` notices that the file has changed, it will
create a new branch in the BibProject repository, along with a pull
request addressed to the maintainer of the BioBib/BibProject
repository.  The IMS editor can then process this request using the
Github web interface.  This is the editor's second point of control in
addition to the index.

Assuming the change is agreeable, the request can be merged in
directly.  If the change is *not* agreeable, then the editor should
reject it, and contact the person maintaining the webpage in question,
and sort out an agreed version with them.

As a temporary measure, if desired, the editor can modify the
corresponding entry in `index.txt` to point to the relevant file in
`./tex_files`, so that the system doesn't poll the unwanted remote
file until the discrepancy has been addressed.

The logic of the update script is such that if an IMS Member makes
further changes to their remote file before the IMS Editor has time to
update the repository, these changes will be accumulated into the same
pull request.

Notifications of updates to this repository are currently sent to
jimpitman00 and holtzermann17 via the email service.  The recipients
can be adjusted at:

> https://github.com/BioBib/BibProject/settings/hooks

Finally, note that HTML versions of the files are generated and
included in the `./new_html_files` directory.  The intention is that
the contents of this directory can be used directly in the IMS site.

The contents are accessible anywhere via a `git clone` and can be
updated with `git pull` -- or this could be automated via cron.

## For testing purposes

Feel free to run these commands to run the scan and update process
without waiting 24 hours:

```
ssh jim@li311-58.members.linode.com [enter password]
cd /bibserver/
python ./ims_legacy/scan-and-update.py
```

Or contact me for assistance.

-- Joe Corneli (`holtzermann17@gmail.com`).
