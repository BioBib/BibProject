import re

# from pprint import pprint

# any white spaces followed by % followed by arbitrary stuff
parenline = re.compile(r"^\s*%.*")
# only spaces
emptyline = re.compile(r'^\s*$')
# blocks of text without parens in them.  In theory there COULD be a "%" in the second block of text,
# as with URLs like https://en.wikipedia.org/wiki/Acad%C3%A9mie_fran%C3%A7aise, so having filtered out
# the lines that "begin" with a percent sign, we allow it here
source_line = re.compile(r"^\s*([^ \t\n\r\f\v%]+)\s*([^ \t\n\r\f\v]+)\s*?$")

def read_member_index():
    with open("BibProject/index.txt", "r") as f:
        location_list = []
        # bibdata part [optional]
        filestring = f.read()
        for line in filestring.split('\n'):
            if not (parenline.match(line) or emptyline.match(line)):
                match = re.search(source_line,line)
                #print '"'+line+'"'
                #print match.groups()
                if (match.group(1) and match.group(2)):
                    location_list.append([match.group(1),match.group(2)])
        return location_list
