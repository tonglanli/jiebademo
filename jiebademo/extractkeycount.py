#coding: cp936
import sys
sys.path.append('../')

import jieba
import jieba.analyse
import nltk
from nltk.probability import FreqDist
from optparse import OptionParser

USAGE = "usage:    python extract_tags.py [file name]"

parser = OptionParser(USAGE)
opt, args = parser.parse_args()


if len(args) < 1:
    print USAGE
    sys.exit(1)

file_name = args[0]

content = open(file_name, 'rb').read()

cutedText = " ".join(jieba.cut(content))
#nltkText = nltk.corpus.gutenberg.raw(cutedText)
fd = FreqDist(cutedText)
items = fd.items()
print items[:30] 
#fd.plot()
#print cutedText
print dir(cutedText)
#print dir(nltkText)
print cutedText.count(u'ÃÏ¿Ì')

tags = jieba.analyse.extract_tags(content, topK=30)
fd = FreqDist(tags)
for keyword in tags:
    print "result of ",keyword
    count = cutedText.count(keyword)
    print count
    fd[keyword] = count
    #cutedText.split().concordance(keyword)

print fd

from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.xlabel(u'')
plt.ylabel(u'¥Œ ˝')
plt.title(u'')
fd.plot()
