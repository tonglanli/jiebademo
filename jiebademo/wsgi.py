# -*- coding: utf-8 -*-
from bottle import route,run, request, get,post,template, static_file, default_app
import jieba
import domain
import sys, os
#path = os.path.dirname(os.path.abspath(__file__))
#jieba.set_dictionary(path + "/jieba/dict.txt.big")
import thread
thread.start_new_thread(jieba.initialize, ())

#import threading
#thr = threading.Thread(target=jieba.initialize)
#thr.start()
from jieba import posseg
import jieba.analyse
import functools
#from nltk.probability import FreqDist
import sqlitedb
import chardet

@route('/static/:filename')
def serve_static(filename):
    return static_file(filename, root='./static')

@route('/files/:filename')
def serve_files(filename):
    return static_file(filename, root='./files')

@route('/static/temp/:filename')
def serve_temp(filename):
    tempfile = static_file(filename, root='./static/temp')
    #path = os.path.dirname(os.path.abspath(__file__))
    os.remove('static/temp/' + filename)
    return tempfile

@route('/static/js/:filename')
def serve_temp(filename):
    tempfile = static_file(filename, root='./static/js')
    return tempfile

@route('/static/css/:filename')
def serve_css(filename):
    return static_file(filename, root='./static/css')

@route('/image/:name&:length&:keys&:values')
def serve_css(name, length, keys, values):
    from pylab import plt, mpl
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    plt.xlabel(u'')
    plt.ylabel(u'')
    plt.title(u'')
    plt.grid()
    keys = keys.decode("utf-8").split(' ')
    values = values.split(' ')
    plt.xticks(range(int(length)), keys)
    plt.plot(range(int(length)), values)
    plt.xticks(rotation=defaultrotation)
    name = name + str(datetime.now()) + '.png'
    imgUrl = 'static/temp/' + name
    plt.savefig(imgUrl, bbox_inches='tight')
    plt.close()
    tempfile = static_file(name, root='./static/temp')
    os.remove(imgUrl)
    return tempfile

def match(a,b):
  if a==b:
    return "checked"
  else:
    return ""

defaulttopk=15
defaultrotation=45

@get('/')
@get('/extract')
def extract():
    sample_text = open('static/sampleFile.txt', 'rb').read()
    print 'ddd'
    topk = defaulttopk
    tags = jieba.analyse.extract_tags(sample_text,topK=topk)
    tagsString = ""
    from nltk.probability import FreqDist
    fd = FreqDist(tags)
    counts = []
    charencoding = chardet.detect(sample_text)
    for keyword in tags:
        if charencoding['encoding'] != 'utf-8':
            keywordtext = keyword.encode(charencoding['encoding'])
        else:
            keywordtext = keyword.encode("utf-8")
        count = sample_text.count(keywordtext)
        fd[keyword] = count
        counts.append(str(count))
    keyCounts = []
    for key,val in fd.iteritems():
        keyCount = domain.KeyCount(key, val)
        keyCounts.append(keyCount)
    if charencoding['encoding'] != 'utf-8':
        sample_text = unicode(sample_text, charencoding['encoding'], errors="ignore")
    return template("extract_form",content=sample_text,tags=keyCounts,topk=15,keyImgUrl="static/sample_keywords.png", texts=sqlitedb.getTexts(), selectedFile="")

import cgi, os
from datetime import *
import cgitb; cgitb.enable()
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import matplotlib
matplotlib.use('Agg')

@get('/:filename')
def extractFile_action(filename):
    if(filename == 'favicon.ico'):
        return ''
    #path = os.path.dirname(os.path.abspath(__file__))
    text = open('files/'+filename, 'rb').read()
    topk = defaulttopk
    tags = jieba.analyse.extract_tags(text,topK=topk)
    tagsString = ""
    from nltk.probability import FreqDist
    fd = FreqDist(tags)
    counts = []
    charencoding = chardet.detect(text)
    for keyword in tags:
        if charencoding['encoding'] != 'utf-8':
            keywordtext = keyword.encode(charencoding['encoding'])
        else:
            keywordtext = keyword.encode("utf-8")
        count = text.count(keywordtext)
        fd[keyword] = count
        counts.append(str(count))
    keyCounts = []
    for key,val in fd.iteritems():
        keyCount = domain.KeyCount(key, val)
        keyCounts.append(keyCount)
    imgUrl = u"/image/" + u"test" + u"&" + str(len(fd)) + u"&" + u" ".join(fd.keys()) + u"&" + u" ".join(str(v) for v in fd.values())
    if charencoding['encoding'] != 'utf-8':
        text = unicode(text, charencoding['encoding'], errors="ignore")
    return template("extract_form",content=text,tags=keyCounts,topk=topk,keyImgUrl=imgUrl, texts=sqlitedb.getTexts(), selectedFile=filename)

@post('/')
@post('/extract')
def extractSubmit_action():
    selectedFileName = request.forms.selectedFile
    if "extract" in request.forms:
        text = request.forms.text
    elif "upload" in request.forms:
        #try: # Windows needs stdio set for binary mode.
            #import msvcrt
            #msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
            #msvcrt.setmode (1, os.O_BINARY) # stdout = 1
        #except ImportError:
            #pass
        # A nested FieldStorage instance holds the file
        fileitem = request.files.file
        # Test if the file was uploaded
	if fileitem.filename:

            # strip leading path from file name to avoid directory traversal attacks
            fn = fileitem.filename
	    filename = fn.split('.')[0]
            text =fileitem.file.read()
            #path = os.path.dirname(os.path.abspath(__file__))
            open('files/' + fn, 'wb').write(text)
            name = filename
            selectedFileName = fn
            author = ""
            period = ""
            uploader = ""
            sqlitedb.addText(name,author,period,fn,uploader)
            message = 'The file "' + filename + '" was uploaded successfully'
            charencoding = chardet.detect(text)
            text = unicode(text, charencoding['encoding'], errors="ignore")
        else:
           message = 'No file was uploaded'

    topk = int(request.forms.topk)
    defaulttopk = topk
    tags = jieba.analyse.extract_tags(text,topK=topk)
    from nltk.probability import FreqDist
    fd = FreqDist(tags)

    counts = []
    for keyword in tags:
        #keyword = keyword.encode("utf-8")
        count = text.count(keyword)
        fd[keyword] = count
        counts.append(str(count))
    keyCounts = []
    for key,val in fd.iteritems():
        keyCount = domain.KeyCount(key, val)
        keyCounts.append(keyCount)
    imgUrl = u"/image/" + u"test" + u"&" + str(len(fd)) + u"&" + u" ".join(fd.keys()) + u"&" + u" ".join(str(v) for v in fd.values())
    return template("extract_form",content=text,tags=keyCounts,topk=topk,keyImgUrl=imgUrl, texts=sqlitedb.getTexts(), selectedFile=selectedFileName)

def main():
    sample_sentences='''
我不喜欢日本和服。
雷猴回归人间。
工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作。
我需要廉租房。
永和服装饰品有限公司。
我爱北京天安门。
abc
隐马尔可夫
雷猴是个好网站
“Microsoft”一词由“MICROcomputer（微型计算机）”和“SOFTware（软件）”两部分组成
草泥马和欺实马是今年的流行词汇
伊藤洋华堂总府店
中国科学院计算技术研究所
罗密欧与朱丽叶
我购买了道具和服装
PS: 我觉得开源有一个好处，就是能够敦促自己不断改进，避免敞帚自珍
湖北省石首市
湖北省十堰市
总经理完成了这件事情
这是一个伸手不见五指的黑夜。我叫孙悟空，我爱北京，我爱Python和C++。
电脑修好了
做好了这件事情就一了百了了
人们审美的观点是不同的。
我们买了一个美的空调
线程初始化时我们要注意
一个分子是由好多原子组织成的
祝你马到功成
他掉进了无底洞里
中国的首都是北京
孙君意
外交部发言人马朝旭
领导人会议和第四届东亚峰会
在过去的这五年
还需要很长的路要走
60周年首都阅兵
你好人们审美的观点是不同的
买水果然后来世博园
买水果然后去世博园
张晓梅去人民医院做了个B超然后去买了件T恤
AT&T是一件不错的公司，给你发offer了吗？
C++和c#是什么关系？11+122=133，是吗？
'''
    return template("cut_form",content=sample_sentences,selected=functools.partial(match,1))


def cut_action():
    text = request.forms.text
    if request.forms.opt=="1":
      result = "/ ".join(jieba.cut(text))
    elif request.forms.opt=="2":
      result = "/ ".join(jieba.cut_for_search(text))
    elif request.forms.opt=="3":
      result = []
      for w in posseg.cut(text):
        result.append(w.word+"/"+w.flag)
      result = " ".join(result)
    else:
      result = ""
    return template("cut_form",content=result,selected=functools.partial(match,int(request.forms.opt)))


if __name__ == "__main__":
    # Interactive mode
    #debug(True)
    #run(server='CherryPy',host='localhost', port=8080, debug=True)
    run(host='localhost', port=8083)
    #from cherrypy import wsgiserver
    #from bottle import CherryPyServer
    #run(host='localhost', port=8099, server=CherryPyServer)
    #from wsgiref.simple_server import make_server
    #httpd = make_server('localhost', 8090, default_app())
    # Wait for a single request, serve it and quit.
    #httpd.serve_forever()

else:
    # Mod WSGI launch
    os.chdir(os.path.dirname(__file__))
    application = default_app()
