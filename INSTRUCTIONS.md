To use the BibProject code, check out the code from github:

```sh
git clone git@github.com:BioBib/BibProject.git
```

A script runs every day at 1AM UK time, via the following crontab
entry in joe's directory on li311-58.members.linode.com:

```
0 1 * * * python /bibserver/ims_legacy/scan-and-update.py
```

I've copied `scan-and-update.py` into the BibProject github repository
so that you can see what it does.  It's the central piece of plumbing
in the miniBibServer project -- it facilitates distributed updating of
a shared Github repository.

The first thing it does when it runs is it pulls in the latest version
of `ims_sources.py` from the BibProject repository to the server on
which the update process runs.  It then starts reading the URLs stored
there.  The `ims_sources.py` file will be the IMS Editor's first point
of control.  Let's have a look at the [`ims_sources.py`](https://github.com/BioBib/BibProject/blob/master/ims_sources.py#L33) file now.

You'll see that there is a very long list of IMS members, and most of
them are currently associated to files that are stored in the Git
repository, specifically in the `./tex_files` directory).  For
illustrative purposes, *one* of the members is associated to a tex
file stored separately on my webpage, as you'll see on [line
33](https://github.com/BioBib/BibProject/blob/master/ims_sources.py#L33)
of the file:

```python
 ["Aitken, Alexander C.", "http://metameso.org/~joe/aitken.tex"], 
```

The IMS editor can update this file to associate any of the tex
sources with remote URLs, in general maintained by IMS members or
their representatives.  Try that now, by (1) copying a tex file from
the `./tex_files` directory to some publicly-accessible webpage that
you control, and (2) changing the corresponding entry in
`ims_sources.py`.

Below, I call the file you've put on your webpage the "remote file."

In order to make this remote file accessible to the process, **update
the corresponding entry** in `ims_sources.py` and then add, commit,
and push the updated `ims_sources.py` file to Github:

```
git add ims_sources.py
git commit -m "Adding another demo member"
git push
```

The next time the `scan-and-update.py` script runs, it will find the
.tex source for that member on the webpage where you put it.  It will
check to see if it is different from the most current version stored
in the repository.  (If you haven't changed the remote file, the
script won't find any difference, and nothing will happen.  So, go
ahead and make a change to the file now, even if it's just adding in a
new `%`'ed comment.  You don't have to update the Github repository
again, because it already knows where to look for this file.)

The next time `scan-and-update.py` runs, it will create a new branch
in the BibProject repository, along with a pull request addressed to
the maintainer of the BioBib/BibProject repository.  The IMS editor
can then process this request using the Github web interface.  This is
the editor's second point of control.

Assuming the change is agreeable, the request can be merged in
directly.  If the change is *not* agreeable, then the editor should
contact the person maintaining the webpage in question, and sort out
an agreed version with them.  

As a temporary measure, if desired, the editor can modify the
corresponding entry in `ims_sources.py` to point to the relevant file
in `./tex_files`, so that the system doesn't poll the unwanted remote
file until the discrepancy has been addressed.

The logic of the update script is such that if an IMS Member makes
further changes to their remote file before the IMS Editor has time to
update the repository, these changes will all be accumulated into the
same pull request.  If days go by without the IMS Editor taking
action, and without any new changes from the IMS member, only the
original change will appear.

Notifications of updates will be sent to jimpitman00 and holtzermann17
via the email service.  The recipients can be adjusted at:

  https://github.com/BioBib/BibProject/settings/hooks

Finally, note that HTML versions of the files are generated and
included in the `./new_html_files` directory.  The intention is that
the contents of this directory can be used directly in the IMS site.
The contents are accessible anywhere via a `git clone` and `git pull`,
or this could be automated (as with the process described in this
note).

## Reminder of Webpage for testing

http://ims.metameso.org/ is a webpage that can be used by IMS members
to test their TeX files and see the generated HTML.

## One further thing to mention about testing

For testing purposes, feel free to run these commands to scan and
update without waiting 24 hours:

```
ssh jim@li311-58.members.linode.com
cd /bibserver/
python ./ims_legacy/scan-and-update.py
```
