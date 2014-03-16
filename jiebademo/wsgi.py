#!/usr/bin/python
# -*- coding: utf-8 -*-
from bottle import route,run, request, get,post,template, static_file, default_app
import jieba
import domain

jieba.set_dictionary("/Users/mac/NLTK/jiebademo/jiebademo/jieba/dict.txt.big")
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
    os.remove('./static/temp/' + filename)
    return tempfile

@route('/static/js/:filename')
def serve_temp(filename):
    tempfile = static_file(filename, root='./static/js')
    os.remove('./static/js/' + filename)
    return tempfile

@route('/static/css/:filename')
def serve_css(filename):
    return static_file(filename, root='./static/css')

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
    sample_text='''
外媒:习近平"一己之私"讲话似在警告朝鲜
2013-04-08 08:37:01　来源: 新华网(广州)　有2641人参与
英国《金融时报》4月8日刊发题为《习近平警告：不准任何人搞乱亚洲》的文章，主要内容如下：

中国国家主席习近平表示，不能允许任何国家把亚洲搞乱。最近几周朝鲜半岛紧张升级，拥有核武的朝鲜威胁称，即将对美国及其盟友发起攻击。

习近平周日在中国一个商务论坛上发表演讲时，对中国的盟友朝鲜发出上述含蓄谴责。来自亚洲、非洲和欧洲的数十名国家领导人出席了博鳌亚洲论坛。

“不能为一己之私把一个地区乃至世界搞乱，”习近平表示，他没有点出具体国家的名称。“国家无论大小、强弱、贫富，都应该做和平的维护者和促进者。”

这些言论暗示，中方对朝鲜的好战姿态和持续数周的战争叫嚣越来越烦。同时，美国军方官员对路透社(Reuters)表示，考虑到与朝鲜之间的紧张局势，美方决定推迟原定下周进行的导弹试验，“以避免任何误解或误判”。

周日出席博鳌论坛的西方外交官表示，习近平刻意含糊的措辞似乎是在含蓄警告平壤方面：不要把事情做过头，但习近平的话也可能在一定程度上针对华盛顿方面，中国领导人经常指控美国插手亚洲事务。

美国和亚洲其它国家呼吁中国作为朝鲜唯一真正的盟友采取更多行动，迫使这个“隐士王国”及其喜怒无常的年轻领导人金正恩(Kim Jong-eun)收敛行为。

澳大利亚总理朱莉娅 吉拉德(Julia Gillard)周日在中国海南岛举行的博鳌论坛上发言时，提到了朝鲜问题。

“（朝鲜半岛上的）任何攻击行为，都将威胁本地区每个国家的利益，”吉拉德表示。“出于这个原因，我确实欢迎亚洲所有国家的政府加强合作，防止朝鲜半岛爆发冲突，制止朝鲜的好战行为。”

新西兰总理约翰 基(John Key)周日晚些时候在博鳌会晤习近平时，预计也将敦促中国运用其影响力约束平壤方面。

中国外交部周日表示，已促请朝鲜方面确保在朝鲜的中国公民、外交官以及投资的安全，而中国驻朝鲜大使馆仍在正常运作。

“当前朝鲜半岛形势不断紧张升级，中方对此表示严重关切，”中国外交部在一份声明中表示。

上周朝鲜当局对常驻该国的外交使团表示，他们应当考虑撤离朝鲜，下周三（4月10日）后他们的安全将无法保证。近日朝鲜还宣称，核战争已经不可避免，但截至周日，没有迹象显示有任何国家在认真计划从平壤撤出外交人员。

多数国家的判断是，战争叫嚣是朝鲜国内政治的一种反映，也是该国年轻领导人巩固其对军队和官僚体制掌控的企图的一部分。金正恩在他父亲2011年12月去世后上台。


习近平发出警告的同一天，中国宣布将让邮轮前往南海有争议岛屿，此举本身也可能引起邻国不满，这些国家也对蕴藏丰富石油资源的南海有主权主张。

反映中国经济和政治影响力与日俱增的一个迹象是，阵容空前的世界领导人出席博鳌论坛，包括哈萨克斯坦、缅甸、秘鲁、赞比亚、墨西哥、柬埔寨和芬兰的总统或总理，以及文莱苏丹。

习近平在周日的演讲中强调了中国的经济吸引力，预测5年内中国的进口将达到10万亿美元，而对外投资将超过5000亿美元。他还表示，出国旅游的中国人将超过4亿。（吉密欧 博鳌报道　译者/何黎）

(原标题：外媒关注：习近平警告不准任何人搞乱亚洲)'''
    return template("extract_form",content=sample_text,tags="",topk=15,keyImgUrl="", texts=sqlitedb.getTexts(), selectedFile="")

import cgi, os
from datetime import *
import cgitb; cgitb.enable()
import matplotlib
matplotlib.use('Agg')

@get('/:filename')
def extractFile_action(filename):
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
    yValues = []
    yTexts = []
    for key,val in fd.iteritems():
        keyCount = domain.KeyCount(key, val)
        keyCounts.append(keyCount)
        tagsString += '{0}:{1} '.format(key.encode('utf-8'), val)
        if (val in yValues):
            yTexts.append("," + key)
        else:
            yValues.append(val)
            yTexts.append(key)
    from pylab import plt
    from matplotlib.font_manager import FontProperties
    fontPath = u'/Library/Fonts/Songti.ttc'
    font = FontProperties(fname=fontPath, size=9)
    plt.xlabel(u'')
    plt.ylabel(u'')
    plt.title(u'')
    plt.grid()
    #plt.bar(range(len(fd)), fd.values(), align='center')
    plt.xticks(range(len(fd)), fd.keys(), fontproperties=font)
    plt.plot(range(len(fd)), fd.values())
    plt.xticks(rotation=defaultrotation)
    imgUrl = 'static/temp/test' + str(datetime.now()) + '.png'
    plt.savefig(imgUrl, bbox_inches='tight')
    plt.close()
    if charencoding['encoding'] != 'utf-8':
        text = unicode(text, charencoding['encoding'], errors="ignore")
    return template("extract_form",content=text,tags=keyCounts,topk=topk,keyImgUrl=imgUrl, texts=sqlitedb.getTexts(), selectedFile=filename)

@post('/extract')
def extractSubmit_action():
    if "extract" in request.forms:
        text = request.forms.text
    elif "upload" in request.forms:
        try: # Windows needs stdio set for binary mode.
            import msvcrt
            msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
            msvcrt.setmode (1, os.O_BINARY) # stdout = 1
        except ImportError:
            pass
        # A nested FieldStorage instance holds the file
        fileitem = request.files.file
        # Test if the file was uploaded
        if fileitem.filename:

            # strip leading path from file name to avoid directory traversal attacks
            fn = fileitem.raw_filename.decode('utf-8').encode('cp936')
            filename = fn.split('.')[0]
            text =fileitem.file.read()
            open('/Users/mac/NLTK/jiebademo/jiebademo/files/' + fn, 'wb').write(text)
            name = filename
            author = ""
            period = ""
            uploader = ""
            sqlitedb.addText(unicode(name, "cp936"),author,period,unicode(fn, "cp936"),uploader)
            message = 'The file "' + filename + '" was uploaded successfully'
            charencoding = chardet.detect(text)
            text = unicode(text, charencoding['encoding'], errors="ignore")
        else:
           message = 'No file was uploaded'

    topk = int(request.forms.topk)
    defaulttopk = topk
    tags = jieba.analyse.extract_tags(text,topK=topk)
    tagsString = ""
    from nltk.probability import FreqDist
    fd = FreqDist(tags)

    counts = []
    for keyword in tags:
        #keyword = keyword.encode("utf-8")
        count = text.count(keyword)
        fd[keyword] = count
        counts.append(str(count))
    #fd = sorted(fd, key=fd.get, reverse=True)
    #fd = sorted(fd.items(), key=lambda x: x[1])
    keyCounts = []
    yValues = []
    yTexts = []
    for key,val in fd.iteritems():
        keyCount = domain.KeyCount(key, val)
        keyCounts.append(keyCount)
        tagsString += '{0}:{1} '.format(key.encode('utf-8'), val)
        if (val in yValues):
            yTexts.append("," + key)
        else:
            yValues.append(val)
            yTexts.append(key)
    from pylab import plt
    from matplotlib.font_manager import FontProperties
    fontPath = u'/Library/Fonts/Songti.ttc'
    font = FontProperties(fname=fontPath, size=9)
    plt.xlabel(u'')
    plt.ylabel(u'')
    plt.title(u'')
    plt.grid()
    #plt.bar(range(len(fd)), fd.values(), align='center')
    plt.xticks(range(len(fd)), fd.keys(), fontproperties=font)
    plt.plot(range(len(fd)), fd.values())
    plt.xticks(rotation=defaultrotation)
    imgUrl = 'static/temp/test' + str(datetime.now()) + '.png'
    plt.savefig(imgUrl, bbox_inches='tight')
    print request.forms.selectFile
    plt.close()
    #fd = sorted(fd.items(), key=lambda x: x[1])
    #for key,val in fd.iteritems():
        #tagsString += '{0}:{1} '.format(key.encode('utf-8'), val)
    return template("extract_form",content=text,tags=keyCounts,topk=topk,keyImgUrl=imgUrl, texts=sqlitedb.getTexts(), selectedFile=request.forms.selectedFile)

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


@post('/')
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
    run(host='localhost', port=8082, debug=True)
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