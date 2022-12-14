'''
Created on Jun 20, 2012

@author: cer28

Step 1: Read word frequencies (from the Leeds file, which has more words) sorted by rank
Step 2: For each word:
            - split into characters
            - for each character, add the cloze to each character's cloze list
Step 3: Read character ranks from the Jun Da file
Step 4: Output the character clozes in order by character rank (not necessary, but
        useful when the output is used elsewhere)

'''

import os
import sys
import re
import codecs

out = codecs.getwriter('utf-8')(sys.stdout)


#filename_words = "../data/simplified/Freq_per_Million_Leeds_internet_50k.u8";
filename_words = "../data/simplified/Freq_per_Million.U8";

words = {}
clozes = {}



try:
    fh = open(filename_words)  #throws IOError
    lines = unicode(fh.read(), "utf-8").splitlines()
    fh.close()
except (WindowsError, IOError), e:
    print "Error: Failed to load source file %s: %s" % (filename, e.message)
    sys.exit(1)


for line in lines:
    if re.match(u'\s*#', line) or re.match(u'\s*$', line):
        continue
    word = line.split("\t")[0]
    
    if len(word) > 1:
        for char in set(word):
            pattern = re.compile(char)
            tmpword = re.sub(pattern, "__", word)
            if not re.match(u'^_+$', tmpword):  # can leave out repetition words ____ as not useful
                try:
                    clozes[char].append(tmpword)
                except KeyError:
                        clozes[char] = [tmpword]
        

out.write("""#
# Heading: Character clozes from Leeds Web Corpus
# Source: %s
#
# For each character, print the top 4 cloze deletions in order of decreasing frequency
#
#term\tcloze
""" % (filename_words))
for char in clozes.keys():
    out.write("%s\t%s\n" % (char, u", ".join(clozes[char][0:4])))

'''
fh = open("../dict/chardict-unihan_readingsX.u8", "w")

for cp in codepoints:
    if int(cp, 16) < 65536:
        fh.write(" ".join([unichr(int(cp, 16)), unichr(int(cp, 16)), "[" + pinyin.get(cp) + "]", "/" + (defs.get(cp) or '<no definition>') + "/"]).encode('utf-8'))
        fh.write("\n")
'''