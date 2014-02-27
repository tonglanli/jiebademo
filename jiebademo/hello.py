#!/usr/bin/python
# -*- coding: utf-8 -*-
from bottle import route,run,default_app,request, response,get,post,template,debug,static_file
import functools

import jieba
jieba.set_dictionary("jieba/dict.txt.big")
jieba.initialize()
jieba.initialize()
from jieba import posseg
import jieba.analyse
#from nltk.probability import FreqDist
import sqlitedb
import chardet


def match(a,b):
  if a==b:
    return "checked"
  else:
    return ""

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@get('/')
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

if __name__ == "__main__":
    # Interactive mode
    #debug(True)
    #run(server='CherryPy',host='localhost', port=8080, debug=True)
    run(host='localhost', port=8080)
    #from cherrypy import wsgiserver
    #from bottle import CherryPyServer
    #run(host='localhost', port=8099, server=CherryPyServer)
    #from wsgiref.simple_server import make_server
    #httpd = make_server('localhost', 8090, default_app())
    # Wait for a single request, serve it and quit.
    #httpd.serve_forever()

#else:
    # Mod WSGI launch
    #os.chdir(os.path.dirname(__file__))
    #application = default_app()
