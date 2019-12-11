# -*- coding: utf-8 -*-
import json

from bottle import route, run, request, get, post, template, static_file, default_app, response
import jieba
import jieba.analyse
import domain
#path = os.path.dirname(os.path.abspath(__file__))
#jieba.set_dictionary(path + "/jieba/dict_old.txt")
# jieba.set_dictionary("D:\\Ctrip\\github\\jiebademo\\jiebademo\\jieba\\dict_old.txt")
jieba.initialize()
# jieba.load_userdict("D:\Ctrip\github\jiebademo\jiebademo\jieba\dict_old.txt")
# if jieba.initialized == False:
    # jieba.set_dictionary("D:\Ctrip\github\jiebademo\jiebademo\jieba\dict_old.txt")
    # jieba.load_userdict("D:\Ctrip\github\jiebademo\jiebademo\jieba\dict_old.txt")
    # jieba.initialize()

#import threading
#thr = threading.Thread(target=jieba.initialize)
#thr.start()

# jieba.set_dictionary("D:\Ctrip\github\jiebademo\jiebademo\jieba\dict_old.txt")
# jieba.load_userdict("D:\Ctrip\github\jiebademo\jiebademo\jieba\dict_old.txt")
import functools
#from nltk.probability import FreqDist
import sqlitedb
import chardet
import nltk

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

@route('/static/design/sequenceimage/:imageName')
def serve_css(imageName):
    return static_file(imageName, root='./static/design/sequenceimage')

@route('/image/:name&:length&:keys&:values')
def serve_css(name, length, keys, values):
    from pylab import plt, mpl
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    from matplotlib.font_manager import FontProperties
    # font = FontProperties(fname="d:\Users\ll.tong\Desktop\msyh.ttf", size=12)
    font = FontProperties(fname="/usr/share/fonts/msyh.ttf", size=11)
    plt.xlabel(u'')
    plt.ylabel(u'出现次数',fontproperties=font)
    plt.title(u'词频统计',fontproperties=font)
    plt.grid()
    keys = keys.decode("utf-8").split(' ')
    values = values.split(' ')
    valuesInt = []
    for value in values:
        valuesInt.append(int(value))

    plt.xticks(range(int(length)), keys)
    plt.plot(range(int(length)), valuesInt)
    plt.xticks(rotation=defaultrotation, fontsize=9,fontproperties=font)
    plt.yticks(fontsize=10,fontproperties=font)
    name = name + str(datetime.now().date()).replace(':', '') + '.png'
    imgUrl = 'static/temp/' + name
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(12.2, 2)
    plt.savefig(imgUrl, bbox_inches='tight', figsize=(20,4), dpi=100)
    plt.close()
    tempfile = static_file(name, root='./static/temp/')
    #os.remove(imgUrl)
    return tempfile

def match(a,b):
  if a==b:
    return "checked"
  else:
    return ""

defaulttopk=25
defaultrotation=45

@get('/')
@get('/extract')
def extract():
    sample_text='''
    金观涛2：“自然哲学”和科学的观念:从《继承与叛逆：现代科学为何出现于西方》谈起

● 金观涛 (进入专栏)
　　


　　 原载于《科学文化评论》第6卷 第4期（2009）

　　


　　 多么巨大的存在之链啊！它从上帝那里开始，自然，以太，人类，天使，人；野兽，鸟，鱼，昆虫，眼睛看不见的东西；显微镜都无法达到的东西，从无限到你；从你到无……你从自然之链中撇掉任何一环；第十，或者第一万，一样会打破这个链条。――蒲柏

　　


　　 一 方法的转变：从“科技史”到“思想史”

　　


　　 很多20世纪的大问题，到21世纪纷纷消解，李约瑟问题似乎就是其中一个。20世纪80年代，“现代科学为什么没有在中国产生”这一历史的发问，曾在中国第二次启蒙运动中引起巨大的社会回响。2002年，中国科学院自然科学史研究所刘钝和王扬宗在《中国科学与科学革命：李约瑟难题及其相关问题研究论著选》一书中，收集了有关李约瑟问题研究各种观点的文章，力图对该问题的20世纪思考作一个总结。今年5月，香港中文大学高级研究员陈方正博士的60万字著作《继承与叛逆：现代科学为何出现于西方》由北京三联书店出版(陈方正 2009a，以下简称《继承与叛逆》)。该书分析了李约瑟问题的缘起、其内在预设和展开逻辑，详细考察了西方现代科学兴起的各环节，最后得出的结论是，现代科学只能起源于西方；指出李约瑟把技术等同于科学，因此“李约瑟问题”是问错了问题。通过陈方正整本大着的论述，这个起源于20世纪初的大问题似乎终于可以划上句号了。

　　 陈方正参考了四五百部西方科学史和有关著作，思考及写作历时十年以上，分析严谨，很多数据和观点是中文世界第一次出现，其方法和结论都很值得学界重视。首先，陈方正确定了“外史”不能取代“内史”的大原则，即“科学家与他们的思想、发现的研究毫无疑问仍然是科学史的核心”。在完成把“科技”转化为“科学思想”的定位后，他指出：“革命”与“传统”的交互作用为“科学思想”内在逻辑的展开。《继承与叛逆》正是立足于这种内在逻辑来论证现代科学是西方思想大传统不可分割的一部分，正如余英时为该书作序时所说：“这是一部出色当行的西方科学与科学思想的发展史。”

　　 为了寻找内在逻辑链的各个环节，陈方正冒化约主义的危险，把数学物理作为科学思想的核心[陈方正 2009a，页27－34]。一旦把牛顿的《自然哲学的数学原理》作为现代科学思想的典范，探索科学思想的起源（更准确地讲，应是“自然哲学”在西方的起源），也就是可行的了。《继承与叛逆》中，我们看到一条从牛顿及他踏足肩膀之巨人――笛卡尔、伽利略、开普勒、第谷和哥白尼开始，一直追溯到古希腊的托勒密和欧几里得长链；分析这条长链的起源、传承和演化，也就抓住了作为思想的现代科学的形成。在这由传承和革命组成的演化链中，陈方正注意到以往的研究存在两大缺环，一是作为“新普罗米修斯革命”结果的欧几里得、托勒密等集大成者是如何出现的；二是作为“渡过鸿沟的载筏”的伊斯兰科学思想（公元800－1450）在西方科学思想形成中的意义。[陈方正 2009b]

　　 确实，陈方正的分析十分到位。早在1980年代，刘青峰在《让科学的光芒照亮自己》一书中，把欧几里得《几何原本》视为现代科学结构的种子，称为原始科学技术结构，近代科学结构正是在欧几里得《几何原本》示范下形成的。刘青峰指出，现代科学结构在西方的形成实为种子成长为大树的过程，可以从原始科学技术结构和社会的互动来把握[刘青峰 2006，页117－159]。但是，这作为现代科学种子的原始科学技术结构又是从何而来的呢？对这个重要问题，刘青峰没有说明。《继承与叛逆》则在这个方向上大踏步地前进了，论证了作为思想的现代科学实际上是经过两次革命形成的。哥白尼至牛顿的第二次革命已广为人知，但它是建立在希腊欧几里得几何和数理天文学之上的。换言之，早在古希腊已经奠定了科学思想的基本模式，在该模式的背后，是鲜为人知的人类第一次科学革命。正是第一次科学革命创造了用数学表达宇宙秩序的基本范式，无论是欧几里得几何，还是托勒密的数理天文学，都是这一次思想革命的结果。他将其称为“新普罗米修斯革命”。陈方正认为，为什么古希腊会出现第一次革命，古希腊科学思想和哲学文化是一种什么关系，这是一个远没有解决的大问题。

　　 研究科学思想发展的内在理路，还必须去把握古希腊罗马文明衰落时科学思想之保存、传承以及再兴起过程。如果把托勒密的《大汇编》视为第一次革命产生的古希腊科学思想之绝响，而哥白尼的工作为第二次革命的开始，两者相距1400年。陈方正列举许多无法抗辩的证据，证明哥白尼的《天体运行论》中的模型结构、参数、甚至图解都取自14世纪回教科学家沙蒂尔（al-Shatir）的著作[陈方正 2009b，页20]。也就是说，正是伊斯兰科学作为“渡过鸿沟的载筏”，使得第一次革命成果得以传承最终引发了第二次革命。这一以住忽视的环节，今日看来是至关重要的。

　　 事实上，正是这两个环节成为《继承与叛逆》探讨的重点，亦是该书最大的贡献。

　　


　　 二 科学和终极关怀

　　


　　 在古希腊，科学被称为自然哲学，它是哲学的一部分。泰勒（C.C.W.Taylor）和罗宾?奥斯本（Robin Osborne）曾为古希腊哲学、科技、艺术和政治宗教，从公元前9世纪到柏拉图的发展做出历史年表，从中明显可以看到古希腊人对自然的认识（自然哲学和技术发展）和宗教、哲学、艺术发展的同步性（甚至是提前性）[泰勒主编 2003，页7－17]。但古希腊科学和哲学究竟是一种甚么关系，却一直处于黑暗之中。目前西方主流看法是把古希腊科学（主要指数学和几何学）当作希腊哲人用理性主义精神研究自然的结果，它只是哲学的附带物。这在古希腊哲学分期上就可看出。思想史学者往住将希腊哲学分为“早期希腊哲学”、“苏格拉底和柏拉图”、“亚里士多德”和“亚里士多德之后的希腊哲学”四阶段[奥康诺 1998]。因为苏格拉底才开始提问：“何为知道？”指出知识始于正确的定义，形成了关于从思考本身之思考（二阶思维），故被认为是古希腊哲学之奠基者。接着，柏拉图提出理型论，开启了古希腊哲学的主流思维模式，使得希腊思想围绕着对柏拉图理型论的肯定、否定和修正展开。在这一从苏格拉底到亚里士多德的希腊哲学主线中，第一阶段只是准备性的，古希腊科学思想统统被归为准备性的第一阶段之中，不占重要位置。该分期最大的问题，是不能解释希腊思想到罗马的变化，更不能理解新柏拉图主义在希腊思想后期的位置以及它对基督教的接引。

　　 陈方正根据格思里(W.K.C. Guthrie)、布尔克特(Walter Burkert)、卡恩(Charles Kahn)等人的研究，勾划出另一幅希腊思想演化的图画。他指出，在“早期希腊哲学”中，毕达哥拉斯独树一职，毕氏对数学之重视，开启了西方思想的严格证明之传统。特别是毕达哥拉斯“万物皆数”的信念，直接影响到柏拉图理型论的形成。换言之，正是在毕达哥拉斯主义的笼罩下，柏拉图一度脱离苏格拉底的“道德”和“社会”的轨道，转向追求永恒真理的神秘主义，这是《对话录》风格转变的原因。他认为，柏拉图《对话录》中记录了柏拉图接受毕达哥拉斯主义的证据。柏拉图曾这样写道：“诸神借着一位新普罗米修斯之手将一件有光芒随伴的天赐礼物送到人间；比我们更贤明也更接近诸神的古人相传，万物是由一与多组成，而且也必然包含了有限与无限。”[陈方正 2009a，页150]这个新普罗米修斯即毕达哥拉斯。

　　 这样一来，以柏拉图为代表的希腊哲学乃是毕达哥拉斯传统和苏格拉底二阶思维的结合，而非原来认为的只沿苏格拉底主智哲学这一条线索发展而成。陈方正认为，它带来了古希腊哲学的两大划时代特征：一是高度重视数学之《对话录》的诞生；二是作为包括大量数学家在内的开放性学者聚会的“学园”（academy）之出现[陈方正 2009a，页148－154]。正因为柏拉图哲学中存在毕达哥拉斯主义基因，才使得追求严格证明成为古希腊哲学演进的内部动力。例如无理数的发现挑战了“万物皆数”之信念，使得数学和数理天文学得以在柏拉图学园中成熟。《继承与叛逆》列举出数学的危机、特别是“不可测比”观念的震撼，是如何导致尤多索斯提出“比例理论”和“极限与归谬法”；古希腊科学和现代科学一样，也有自己的哥白尼和牛顿。因此，“以数学建构宇宙模型”的天文学革命，实为响应柏拉图号召而发生。而欧几里得的《几何原本》、阿基米得的度量几何学、阿波隆尼亚斯的圆锥曲线和阿里斯它喀斯的日月测量、喜帕克斯的恒星进动的发现，都是顺这一范式展开之结果。陈方正提出的“新普罗米修斯革命”，就是毕达哥拉斯主义和柏拉图知识追求之结合。从该观点看，古希腊科学思想始终是古希腊哲学的核心部分，正如现代科学是当代西方文明的不可分割的一部分一样。

　　 如果陈方正的分析正确，我们可以从一个新的角度考察古希腊罗马思想。20世纪文明研究最重要的进展之一，是从轴心文明角度看古希腊哲学，把它视为实现了超越突破的结果。所谓超越突破是人从社会中走出来思考生命的终极意义和正当性最终标准，亦可称之为终极关怀的觉醒，而终极关怀最重要的是解决生死问题[金观涛、刘青峰 2007]。希伯来救赎宗教、印度解脱思想和中国儒家以道德为终极关怀都是面对生死问题，那么，希腊哲学也是围绕着终极关怀展开的吗？以往，人们多从“爱智精神”来分析古希腊思想的形成，它排斥神秘主义，似乎与生死问题无关。“爱智精神”背后是认知的意志，它无疑准确地代表了古希腊哲人的追求。但是认知能解决生死问题么？

　　 在《继承与叛逆》一书中，这个问题迎刃而解，因为毕达哥拉斯主义正是为解决生死问题而形成的。该书描述了毕达哥拉斯创立的神秘教派是这样理解宇宙秩序和追求永生关系的：“人的灵魂本来就是宇宙整体的一部分，因此才得以分享其条理、秩序，从而得以自由自在，长存不灭。要受世俗躯体污染的灵魂回复到这个状态，首先要做的，自然便是充分明白宇宙本身的原理、结构和奥秘，因为这思索、理解、明白的过程自然会改变灵魂本身的状态。”[陈方正2009a，页123]柏拉图正是认同上述基本主张，才接受毕达哥拉斯主义。以往的研究也注意到柏拉图力图用他的理型理论去克服死亡，但不清楚克服死亡的模式。如果科学（主要是数学）真是柏拉图追求永生的内在动力和方法，那么，就应该对以柏拉图主义为核心的希腊哲学重新定位。希腊哲学一直被认为是理性的，关注现世社会的；现在必须加入它以科学作为终极关怀这一面。或者说，表面上以人文社会精神为主的古希腊哲学中一直暗藏着另外一个维度：它一方面强调思维推理的严格性，另一方面指向认识神秘的宇宙以克服死亡（为什么要通过认识宇宙的方式来克服死亡？）。今天，人们早已接受了科学和终极关怀无关的见解，皆知科学不能解决人生意义问题，但这种现代科学观和古希腊哲学的看法大不相同。可以说，古希腊哲人比今日科学主义者还要“科学主义”！他们是为了从宇宙秩序中追求永生而沉迷于科学。

这样一来，新柏拉图主义在罗马帝国时期兴起，直指神秘主义的救赎宗教，成为希腊爱智精神（还有罗马的经验理性主义）和基督教之间的桥梁也就不难理解了。在传统社会，科学只有成为终极关怀的一部分，才能在轴心文明思想传承中延续下去。本来，古希腊科学和认知之意志都是寄生在神人同形的古代宗教之中的。当神人同形的古代宗教消失时，作为终极关怀的科学和认知的意志都失去了根植的土壤。在寻找新的载体过程中，柏拉图的理型论转化为新柏拉图主义。由此亦可理解，当希腊罗马文化衰亡之际，科学的黑暗时代必然来临。事实上，当救赎作为大多数人的终极关怀在西方确立之际，古希腊科学必须明确它和救赎宗教的关系。如果不能建立联系，它必定被遗忘；如果建立了联系，它只能是神学的婢女。这正是我们看到的源于古希腊之科学思想在中世纪的命运。

　　


　　 三 自然法、ratio和理性

　　


　　 在希伯来人的终极关怀中，认知的意志从一开始就没有位置。当基督教从犹太教中分离出来时，完成了两个变化，一是普世化，二是出世转向。这样，爱智精神就和救赎对立起来，故早期基督教是反对科学思想的。正因为如此，《继承与叛逆》在寻找科学思想“渡过鸿沟的载筏”时，更重视伊斯兰教的作用。伊斯兰教作为救赎宗教的入世转向，同样不存在把认知之意志作为终极关怀的精神，那么，为什么伊斯兰教比基督教更有资格充当“渡过鸿沟的载筏”？关键正在于伊斯兰教对其他宗教信仰的包容性。

　　 伊斯兰教不否定先知以前的神人对话，只是把穆罕默德视为封顶使者，是神最后一次给人启示。这样，只要其它宗教不挑战伊斯兰教的统治地位，它们都可以包容进来。确实，伊斯兰教对其他宗教各种教派（包括古希腊罗马科学思想）比早期基督教开放得多，以至于有人甚至认为：“伊斯兰应该是能与任何有价值的文化和谐共存的宗教信仰，而不管这种文化的来源如何。”[鲁宾逊编 2005，页24]当然，实际上伊斯兰教只是工具性地吸纳其它宗教所包含的政治文化，以建立帝国。从伊比利半岛至中亚地区，先后出现过伍麦耶王朝（661-750）、阿拔斯帝国（750-1258）、法蒂玛王朝（909-1171）、塞尔柱王朝（1038-1194）、阿尤布王朝（1169-1250）、马木路克王朝（1250-1517）和奥托曼帝国（1299-1922）等。伍麦耶王朝结合的是阿拉伯部落传统，阿拔斯帝国则吸收了拜占廷、波斯政治和宗教文化。法蒂玛王朝属什叶派，把北非神秘主义带进伊斯兰教。自塞尔柱王朝起，突厥人的草原文化大现模地和伊斯兰教结合，一直到奥托曼帝国时期发展到顶峰。正因为如此，伊斯兰教如一大熔炉，可以把中古时期各种宗教文化的成果结合起来，使它可以充当科学思想“渡过鸿沟的载筏”。关于这一点，《继承与叛逆》有详尽讨论。正如书中所指出，伊斯兰科学的一个重要贡献是对巴比伦科学的接引，在科学思想中加入了古希腊科学没有的新要素，这就是柯列兹米(Al-Khwarizmi)根据巴比伦计算系统发展出的代数学。书中列举了39位回教科学家，其中14位属伊拉克和叙利亚，17位来自伊朗与中亚，8位生活在埃及、北非与西班牙[陈方正2009a，页311]。若没有伊斯兰教这一时期对其他宗教文化的包容，就不可能把这么多地区和形形色色古文明对科学思想之贡献，都吸纳到伊斯兰科学中来。

　　 在比较中世记晚期基督教和伊斯兰教对科学思想的态度时，陈方正碰到一个困难。这就是，12世纪前伊斯兰教对科学思想的包容远胜过基督教，但12世纪后基督教对科学思想的接纳却后来居上，使得第二次科学思想的大革命是在天主教大传统中蕴育的。为什么会出现这种情况呢？《继承与叛逆》将其归为欧洲大学与伊斯兰高等学院的不同发展。西方大学起源于专科（法律和医学）学校与教会办的座堂学校；这些学校慢慢从教会中获得独立，成为教授知识和科学研究的中心。这与伊斯兰高等学院一直处于宗教、宫廷的强褓中呈现出极大的差别[陈方正2009a，页418]。这种解释固然有道理，但是为什么西方大学和伊斯兰高等学院会有这么大的区别呢？我在本文一开始就指出，《继承与叛逆》在方法论上最大的特点是从科学外史转到内史，即从科学发展所依赖的政治经济制度转到思想本身，这是极为重要的；但在回答这个问题时，陈方正却没有将自己的立场贯彻到底，即没有循文化思想找到更深的原因，而是又退到制度层面来寻找科学思想革命的原因，这不能不令人有点遗憾。

　　 我认为，12世纪基督教对古代科学态度的转变，以及在此后对科学的包容终于超过伊斯兰教，是有更为深刻的思想文化根源的，这就是教皇革命所引发的希伯来超越视野与古希腊超越视野的融合。据伯尔曼的研究，西方几乎所有近代事物均起源于1050年至1150年这一时期，而不是在此以前；近代事物不仅包括近代的法律制度，而且还包括近代的法制政府、近代的城市、近代的大学和许多其它近代事物[伯尔曼 1993，页439－441]。为什么会如此？关键在于西方大一统教会为了摆脱世俗王权的控制，必须把罗马法作为权力和政治制度正当性的最终根据。古希腊罗马法治背后是理性精神，教皇革命导致了理性和救赎的结合。也就是说，教皇革命带来一个深远后果，这就是在政教分离和西欧进入法制封建社会同时，和认知的意志相联的理性首次被纳入救赎宗教，这就使得天主教的终极关怀中包含着希伯来宗教和希腊文化两种要素，我们可称为文明融合。这时，科学虽然仍是神学的婢女，但科学背后的认知意志已成为终极关怀的一部分，即理性（包括法律的精神）是认识上帝、获得救赎必不可缺少的，这与伊斯兰教中科学思想只是作为工具性被接纳具有本质的不同。

　　 希伯来宗教和希腊文化两种超越视野的结合，表现在研究法律和经院哲学的大学可以向教会要求独立的权利，更重要的是，作为科学理论的自然哲学如亚里士多德学说也出现在天主教经院哲学的教义之中。从上帝开始到万物的存在巨链成为人们对自然有机体的认识，而新拉图主义的唯实论对封建等级的论证也都运用了同样的模式。我们曾在有关著作中论证过，可以用表达观念的关键词意义的变化作为观念深层结构的长程变迁的证据[金观涛、刘青峰 2008]。这方面最著名的例子是natural law的出现。众所周知，该词一方面指涉“自然律”，但同时又是“自然法”。自然法在古希腊罗马就存在，它和表达自然律的词是不同的。为什么两者必须有别？在相当长时间中，法律存在着立法者的意志部分，它不可能和逻格斯混同。自然律和正义的法律（自然法）的合一需要一个前提，这就是人间立法者的意志从法律中的隐退，也就是rule of law（法制）取代rule by law（法治）。在希伯来精神的出世转向中，法律的形式结构大于实质的意义，它被理解为上帝对有罪人类的惩罚。当它只能通过理性被发现而不是被发明时，自然法和自然律的差别不再存在，它们都是上帝的法律。甚至上帝在某种意义上就是natural law本身。确实，这一切只能发生在两种超越视野融合之际。由此我们可以理解，为什么12世纪以后西方的法律一定要有逻辑自洽的形式结构，甚至以数学作为其理性之象征。[登特列夫 1984，页50－51]

　　 也许，另一个更重的证据是“理性”这个关键词本身了。众所周知，今日“理性的”（rational）这个词来自拉丁文“比例”（ratio）。该用法起源于12世纪后经院哲学的成熟。为何“比例”（ratio）可以成为理性的代名词？不了解古希腊自然哲学中“比例”的重要性，是无法理解这一点的。柏拉图在讨论可感知世界和理型世界关系时，就是用了“比例”（ratio）作为例子。他曾这样论证，把AB线段不均等地在C点分开，然后以相同比例在E点将BC分成两部份，使得BC：CA＝BE：EC。如果CA 表示理型以及我们认识它们的精神活动，BC是代表可感知世界及我们的感知方法；要理解它们是怎样互为条件的，必须研究BE和CE的关系。CE是马、床、树这一类客体，BE则为它们的摹本，如镜像、影子和反映物。在可感知世界中摹本与其原形之间的关系，就如被信念所认识的感性世界BC和被理性或思想认识的理型CA之间的关系一样[奥康诺 1998，页55－56]。请注意，柏拉图把知识定义为被证明的信念后，进而指出用镜像认识客体之所以可以等同于用精神认识理型，靠的是“比例”（ratio）的存在。这里，“比例”不仅意味着事物是可比的，即某种关系和另一种关系同构可以帮助我们认识世界。“比例”是人接近理型的方法！《继承与叛逆》用相当的篇幅谈尤多索斯提出的“比例理论”，指出它在数学上已达到19世纪戴德金分割（Dedekind cut）的高度[陈方正2009a，页163－164]。实际上，在古希腊“比例理论”的意义远超过数学本身，而是力图用ratio理解整个世界。

　　 请想想，用ratio表达“理性”意味着什么？这不仅是古希腊万物皆数在拉丁文世界的复活，亦是新柏拉图主义在经院哲学中不可取代位置之奠定。由此可见，12世纪天主教中的科学既不同于希腊罗马，亦不同于伊斯兰教，因为它同时具有救赎和认知两种超越视野。现代科学思想的革命和现代性均是在这一母体中孕育成熟，绝不是偶然的。

　　


　　 四 科学和现代性：工具理性和受控实验的起源

　　


　　 如果说《继承与叛逆》有什么不足，我认为是该书对现代科学思想和现代性关系的忽略。作为现代思想的科学和古希腊罗马科学思想究竟有何本质不同？其内容是可以用数学物理思想传承中的革命来说明的，这一点《继承与叛逆》作出了相当充分的论述。但除了科学理论本身外，作为整体性精神层面的思想革命又是什么呢？该著作却很少论及。

　　 现代科学思想之所以是现代的，它与古希腊罗马科学、伊斯兰科学以及中国程朱理学的格致具有本质的不同，就是它不再必然地和终极关怀相联系。韦伯把现代化视为工具理性的扩张，所谓工具理性就是指理性和终极关怀处于二元分裂状态。现代科学思想作为现代理性的核心，这一特点十分明确。实际上，理性和对上帝信仰二元断裂，在唯名论那里已经开始。《继承与叛逆》虽也谈到经院哲学内部唯名论和唯实论的争论，但没有抓住这一本质。

　　 在唯名论宣称共性为名（不真实的）背后，蕴含着否定新柏拉图主义的两项最基本的主张。首先，和新柏拉图主义相反，唯名论者认为上帝是无所不能的意志。这样，认识上帝必须依靠启示，和理性无涉。虽然这一点与早期基督教一致，但它出现在天主教神学中则有完全不同的意义。因为，其后果不是如早期基督教那样排斥认知意志，而只是把认知意志放到和信仰无关的层面而已；结果导致理性和终极关怀的二元分裂。更有甚者，唯名论认为唯有个体才是真实的，而经院哲学中来自亚里士多德哲学的新柏拉图主义式的“种”和“属”，它们作为共相，只是一个名称，不是实在。这样一来，人和存在巨链的关系发生了根本的改变。人一旦从存在巨链中独立出来，不仅自然界变成一部机器，将封建社会视为一个上帝设计的理性有机体观念不再成立。国家亦是由一个个不可进一步分割之个人根据法律组成的。吉莱斯皮（Gillespie）将这种来自唯名论的个体观称为本体论个人主义(ontological individualism)，详细论述过它对西方现代思想形成的三个方面的持久影响。

　　 第一，从此之后寻找真理不应在修辞学和三段论的语言分析中花费时间，因为它们不是实在，而应转向自然界。正是这一思想转向促进了实验科学的兴起。第二，唯有个体才是真实的这一观念经意大利文艺复兴时期人文主义者的发挥，个人生活即私人领域的意义和正当性得到确立，它和自然法结合，形成了个人权利和个人自由等近代观念。第三，它直接促成了17世纪的宗教改革。唯名论相信上帝无所不能，通过其意志创造了每一个具体之个体，这样一来，人和上帝的沟通(得到启示)就可以依靠个人与上帝之间的单独交流来进行，教会不再是必不可缺的中介。换言之，唯名论对经院哲学之颠覆构成了现代性在天主教神学内部的起源。[Gillespie 2008]

实际上，所有新教徒（还包括17世纪所有自由主义者）均相信唯名论，故工具理性的兴起直接与宗教改革有关。正因为如此，韦伯才能将新教伦理视为现代性确立之关键性因素。在现代科学起源研究上，与韦伯命题相对应的是默顿命题。默顿（Robert King Merton）在1930年代当研究生的时候，就对为什么以牛顿力学为代表的科学革命产生在17世纪的英国这个问题感兴趣。他发现当时科学家大多是清教徒，因此想起韦伯关于新教伦理的论述。默顿把有关研究运用到科学史，建立了科学社会学这门新学科。近年来，科学史家对默顿命题是否正确作了系统考察，发现促成科学革命的是新教徒，而非一定是清教徒。这说明只要实现理性和信仰二元分裂，就能促进现代科学的发展。[本-戴维 2007]

　　 关于现代科学思想不涉及终极关怀这一点，是众所周知的，理性和信仰的二元分裂只是其早期形态。《继承与叛逆》虽然间接触及了这问题，并且详细讨论了牛顿（他有“最后一个巫师”之称）对于炼金术、神学又及所谓“上帝作为”的入迷，但很可惜，却没有就其意义展开讨论，这可能与该著作把牛顿思想作为现代科学思想代表有关。陈方正把科学史还原为科学思想史，这无疑是科学史研究方法的巨大进步。但是，如同以往一样，在进行科学思想分析时，往往不得不用某个最重要科学家的思想来代表一个时代普遍的科学思想，这样就很容易忽略现代科学思想兴起的主线。我认为，真正彻底的方法论转变，应该是进一步把作为思想的科学史转化为科学的观念史。观念史注重普遍观念本身的变化，这样个别思想家个别论述带来的干扰就不会掩盖科学观念主线。整个讨论可以更为准确地进行。

　　 一旦把思想史还原到观念史，就可以用关键词意义变化来揭示普遍观念深层结构的变迁。如前所说，理性在中世纪的形成可以找到语言的证据，而工具理性的形成同样也可以在语言变化中找到历史的痕迹。西方中世纪用来表示理性的有两个词，一个是reason；另一个是ratio。reason意义较宽，有理由、理解和前后联贯的思想之意，它来自古法文reisun或raison、拉丁文reri（“思考、计算”）。ratio意义较明确，它来自古希腊哲学的“比例”。指人运用概念、判断和推理的能力，它有别于感觉、意志、情绪等心理活动[冯契主编 1992]。到17世纪，ratio和reason出现了微妙的差别，这就是ratio是用来专指不相信启示真理的理性主义[威廉士 2003，页314]。这难道不正是反映了工具理性形成使得ratio和终极关怀（启示真理）的分离吗？

　　 我认为，真正代表作为思想革命的现代科学之出现，是现代科学观念的形成。理性和终极关怀二元分裂只是其一个方面，另一个更重要的方面是受控实验精神的兴起，成为现代科学观念的核心。关于实验精神在中世纪欧洲起源的过程，在科学史研究中历来就是一个谜。《继承与叛逆》谈到实验精神和中世纪魔法热潮及炼金术有关，称之为“人定胜天”的科学小传统[陈方正 2009a，页454－458，507－520]。但是我们不要忘记，魔法在教廷看来是大逆不道的，炼金术亦一直受到宗教的禁止。没有宗教大传统本身的变化，实验精神兴起是不可能的。在文艺复兴时期，实验精神是在大学甚至修道院中出现和发展的，这又是怎么回事呢？其实，理性和终极关怀的二元分裂只是唯名论革命的一个方面，另一个更重要的巨变，是自然界已经除魅，被视为一架巨大的机器。这时，将自然律视为上帝为自然立法的信念必定会被新的观念所取代。在做实验的研究者心中，自然定律更多是作为机器的原理（机制），它应如何研究？对它做某种输入，再考察其输出是顺理成章的，受控实验从技艺中分离出来，成为现代科学观念的核心。

　　 换言之，当自然法在唯有个体才真实的剌激下转化为个体不可让渡之权利时，作为个人主义者的唯名论信徒，意识到自己面对着两种机器。一种是由个人契约组织起来的社会机器，另一种是如同钟表般精确的自然机器。研究它们的方法本质上是类同的，对自然必须用受控实验显现事实，而社会研究中应价值中立地用因果性（而不是目的论）来解释事实。实验精神（包括事实与价值的分离）和现代性核心价值――不可让渡的个人权利是同步形成的！也就是说，现代科学与现代性核心价值（个人权利）本是挛生兄弟。只有认识到这一点，才能解理解为什么作为现代思想的科学（更准确地讲是现代科学的观念），是现代性的有机组成部分。在此意义上，用牛顿的数学物理思想和价值追求来代表现代科学是远远不够的，因为作为思想的现代科学已不再是自然哲学，而是全新的科学观念了。

　　 或许，“科学”这个词本身意义的变迁以及它最终取代“自然哲学”，可以为上述实验精神的起源、特别是科学观念的形成提供证据。“科学”一词来自于拉丁文scientia，原意是指“知识”。教皇革命后该词进入天主教基本观念之中，中世纪普遍认为“上帝是具有知识（sciens）的主宰”。值得注意的是，自17世纪起，scientia开始和其它知识区别开来。Science是指“需要理论知识的技艺”，它和“只需要实用知识的技艺”art是不可混同的。有趣的是，当科学与技艺拉开距离之时，同步发生的是science和做实验联系起来，“科学的”（scientific，拉丁文为scientificus）越来愈和“理论上”（theoretical）或“demonstrative proof”（论证）不可区分[威廉士 2003，页346－347]。我认为，这表明现代科学观念强调科学必须是能被证明的，即受控实验是科学不可分割的组成部分。所谓受控实验，是为了验证（或提出）理论而做实验。这样，不仅实验和理论不可分割，而且在做实验过程中，由于强调实验的可重复性和对实验条件的控制。控制自然的重要性在实验中被意识到，成为现代科学观念的一部分。

　　 科学观念的灵魂是工具理性，不再和终极关怀有关，做实验的目的不是去理解上帝用理性为自然设立的律法，而是揭示因果关系使自然这架大机器服务于人类。这样，随着控制自然之精神进入17世纪的科学观念，刚从自然哲学中脱胎出来的现代科学观念与技术系统结合，现代科学技术观念逐步成熟了，作为改造世界的力量登上了历史舞台。在17世纪， technology(技术）本是指arts（技艺），它和art的差别在于更注重技艺的系统性。technology一词来自拉丁文technologia，意为“有系统的处理”[威廉士 2003，页399]。确实，只有通过科学实验，才能发现、发明层出不穷的新原理和新技术，使arts系统化不再和工匠的艺术发生关系。作为科学和技术的综合体的科技终于取代科学的位置。在以上对现代科学观念形成的描绘中，我们高度强调受控实验中控制自然的思想从对科学理论检验中独立出来、且和工具理性相结合。在信仰与理性的二元分裂的结构中，信仰可以被保留，亦可以被其它观念取代。当占有的欲望以控制自然为名成为理性的匹配物时，现代科技的观念才全面确立。从此，改造自然和市场的无限扩张总是互为表里的。在此意义上，歌德的《浮士德》或许比牛顿的《自然哲学的数学原理》更代表现代科学的精神。

　　


　　 五 李约瑟问题真的不成立吗？

　　


　　 据我观察，21世纪的科学技术观念不仅与17世纪自然哲学根本不同，可能也与19、20世纪有别。相对于实验精神和控制自然，数学物理在科学中的地位已不如上个世纪那么重要。作为衡量科学发展象征的，今天也许已不是数学难题的证明，甚至不是天体和基本粒子的发现，而是各式各样的实验成就和大型研究计划的实施所带来的突破。在今日，如何定义现代科学？是牛顿定律、广义相对论，还是DNA研究？这决不是没有争议的。孕育现代科学的古希腊哲学和自然哲学，只代表了科学的幼年和童年。作为科学精神基本要素的工具理性和受控实验已经如此强大；21世纪科学观念的核心，已不是单纯认知的意志所能概括的了。在改造自然带来全球暖化和控制自然变成无穷的占有欲面前，人们再也不会如19世纪那样把科学等同于使人变得崇高、纯洁而坚强的庙堂。在这种前未有过的新反思意识下，科学观念将面临新的改变，它会对科学史的研究将发生什么影响呢？

　　 如果上述观察不无道理，那么，也许应该重新评价李约瑟将科学等同于技术的“错误”。我认为，虽然李约瑟对科学作出技术化的理解是不够深刻的，但李约瑟问题的提出，更有利于突破西方中心论的局限，以便更广泛地考察受控实验在不同文明中起源的历史。如果以受控实验为中心来考察科学史，因实验更依赖于同时代提供的技术，而中国传统社会技术的发达程度最少是可以和西方比拟的；那么，追问受控实验精神是否可以在其它文明中最先形成，也就绝不是没有意义的。

　　 当然，受控实验亦受观念的支配。但这些观念不一定是数学物理，显然，使用自然哲学起源的逻辑来刻划它也就不再合适。必须指出的是，即使在这一维度上，陈方正著作整个论述也不是没有意义的。正如我前面所论证的，受控实验在古代虽蕴含在技术中，它是工匠传统的一部分，但它在中世纪后期于西方兴起，却和自然哲学的数学化大有关系。再往前追溯，几何测量是最早的受控实验，古希腊万物皆数的猜想，或许正是人类用受控变量来描述宇宙的最初尝试。进一步讲，如果不是天主教具有两种超越视野，没有唯名论革命，受控实验的观念是不可能出现的。也就是说，研究者经过一番艰苦的努力，很可能仍然回到陈方正在《继承与叛逆》中得到的结论：现代科学只能出现在西方，而不可能从中国古代大一统技术或道教炼丹术中脱颖而出。但是，研究者在完成考察之前，是不能经易得出这些结论的。而激发他们进行考察的，恰恰是李约瑟问题。我们自然可以问，随着今后科学观念进一步变异，这样的重新提问会不会一而再再而三地发生呢？如果会，李约瑟问题真的不成立吗？因为，虽然每一次研究结果都否定了作为其出发点的问题，但如果李约瑟问题一开始就被划上句号，所有后面的新探索还会有吗？

　　 今天，人们终于发现李约瑟问题的意义恰恰在于它具有方法论层面的悖论性质。它的提出是出于科学具有超越文化的普遍性，而它的解答却必须回到轴心文明的差异。既然科学知识和技术的普世性和客观性是公认的，那么追问现代知识和技术为何在某种文化中没有最早出现，也总是有意义的。然而，作为研究的结果，只要不是诉诸偶然性，就会去追究某种文化的价值系统对某一类知识和技术是接纳或拒斥，其答案必定是现代科学技术的起源和文化价值系统的关系，甚至科学技术本身就属于某种价值系统。这些答案，在一开始就预设了对问题本身的否定。换言之，李约瑟问题在其结构上存在着提问和解答的自相矛盾！

　　 这种悖论性的大问题只能出现在20世纪，因为这是一个伟大而特殊的时期。正是在20世纪，人类经历了第一次全球化带来的现代性所面临的严重挑战，经历了两次惨烈的民族国家战争的世界性浩劫。正是在这一百年中，人类不得不重新思考有无超越现代性的可能，不同轴心文明的传统都被激发出来。在对现代性危机的思考中，现代思想和价值与轴心文明的关系被发现，引起讨论。只有这类在方法论层面具有的悖论性质的大问题，才能容纳最大量最持久的超越专业的思索，它犹如遥不可及的星座指引着研究者，在学术探索的黑夜里寻找方向。其中有些问题不可能解决，也不必解决，因为这类问题的背后是对现代性的本质和人类的认知意志本身的好奇心。

　　 李约瑟问题实为中西文化以及其现代化道路巨大差异激发出来的反思，它是构成20世纪特有的问题意识（这是健全心灵不可少的）之元素。20世纪已经过去，在日益专业化的研究中，它不再引起人们的注意，这是理所当然的。但我想强调的是，在21世纪世俗大都会的光污染中，整个星空已暗淡无光。不仅各种20世纪的问题星座不再引起注意，星空的秘密和我们心中的道德律引起的惊奇，只是过去一代人的怀旧而已。在此意义上，我们或许真是要给李约瑟问题划上句号了。只有对于我们这些20世纪出生的人，不能忘记20世纪宏大气魄和胸襟，李约瑟问题仍是永恒的发问，指引着我们去研究轴心文明之谜。在这一意义上，如果说李约瑟问题仍然值得新一代人注意的话，陈方正的巨著亦是后继者不可轻易逾越而必须认真对待的。

　　


　　 参考文献

　　 Gillespie, M. A. 2008. The Theological Origins of Modernity. Chicago: University of Chicago Press.

　　 奥康诺 1998. 《批评的西方哲学史》（上）. 洪汉鼎等译. 台北：桂冠图书股份有限公司.

　　 本-戴维 2007.《清教与现代科学》. 张明悟、郝刘祥译. 《科学与文化评论》 4 (5).

　　 伯尔曼 1993. 《法律与革命――西方法律传统的形成》. 北京：中国大百科全书出版社.

　　 陈方正 2009a. 《继承与叛逆：现代科学为何出现于西方》. 北京：三联书店.

　　 陈方正 2009b. 《一个传统，两次革命――论现代科学的渊源与李约瑟问题》. 《科学文化评论》6 (2). 北京：社会科学文献出版社.

　　 登特列夫 1984. 《自然法：法律哲学导论》. 李日章译. 台北：联经出版事业公司.

　　 冯契主编 1992. 《哲学大辞典》. 上海：上海辞书出版社.

　　 金观涛、刘青峰 2007. 《从中国文化看终极关怀理念形态》. 《生死学研究》 (6). 南华大学（台湾）.

　　 金观涛、刘青峰 2008. 《观念史研究：中国现代重要政治术语的形成》. 香港：中文大学当代中国文化研究中心.

　　 刘青峰 2006. 《让科学的光芒照亮自己：近代科学为什么没有在中国产生》. 北京：新星出版社.

　　 鲁宾逊编 2005. 《剑桥插图伊斯兰世界史》. 北京：世界知识出版社.

　　 泰勒主编 2003. 《劳特利奇哲学史》（第一卷）：《从开端到柏拉图》. 韩东辉等译. 北京：中国人民大学出版社.

　　 威廉士 2003. 《关键词：文化与社会的词汇》. 刘建基译. 台北：巨流图书公司. '''
    topk = defaulttopk
    tags = jieba.analyse.extract_tags(sample_text, topK=int(-1))

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
    totalWordCount = 0
    keywords = []
    words = []
    words = jieba.cut(sample_text);
    texttemp = nltk.Text(word for word in words)
    for key,val in fd.iteritems():
        keyword = domain.Keyword(id=0, name=key, count=val, textId=0,similarWords='')
        keywords.append(keyword)
        totalWordCount += val
    keywords = sorted(keywords, key=lambda keyword : keyword.count, reverse=True)
    keywordtopk = keywords[:topk]

    for tempkeyword in keywordtopk:
        textword = '';
        if charencoding['encoding'] != 'utf-8':
            textword = tempkeyword.name.encode(charencoding['encoding'])
        else:
            textword = tempkeyword.name.encode("utf-8")
        texttemp.similar(textword)
        tempsimilarWords = texttemp._word_context_index.similar_words(tempkeyword.name)
        tempsimilarWordsStr = u" ".join(tempsimilarWords)
        # tempsimilarWordsStr = str(tempsimilarWords)
        tempkeyword.similarWords = tempsimilarWordsStr;

    imgUrl = createKeywordImageUrl(keywordtopk)
    totalDifferentWordCount = len(set([ keyword.count for keyword in keywords]))
    words = jieba.cut(sample_text);
    texttemp = nltk.Text(word for word in words)
    keyword = domain.Keyword(0, name=u"不同词汇总数", count=len(keywords), textId=-1, similarWords= '')
    # similarWords = texttemp.similar(u'科学')
    # similarWords = texttemp.similar(u'思想')
    # similarWords = texttemp.similar(u'哲学')
    # similarWords = texttemp.similar(u'问题')
    # similarWords = texttemp.similar(u'理性')
    # similarWords = texttemp.similar(u'观念')
    # similarWords = texttemp.similar_words(u'科学')
    commonWords = []
    # commonWords.append(u'科学')
    # commonWords.append(u'上帝')
    # commonContexta = texttemp.common_contexts(u'科学')
    # commonContexta = texttemp.concordance(u'科学')
    # commonContexta2 = texttemp.common_contexts(commonWords)
    # nltk.download('stopwords')
    # concordance_list = texttemp.concordance_list(u'科学')
    # texttemp.collocations()
    keywordtopk.append(keyword)
    keyword = domain.Keyword(0, name=u"词汇总数", count=totalWordCount, textId=0, similarWords= '')
    keywordtopk.append(keyword)
    keyword = domain.Keyword(0, name=u"关键词汇临界次数", count=totalDifferentWordCount, textId=0, similarWords= '')
    keywordtopk.append(keyword)
    keywordsPercentage = 100*sum([keyword.count for keyword in list(filter((lambda x: x.count > totalDifferentWordCount), keywords))])/totalWordCount
    keyword = domain.Keyword(0, name=u"关键词数量百分比", count=keywordsPercentage, textId=0, similarWords= '')
    keywordtopk.append(keyword)
    return template("extract_form",content=sample_text,tags=keywordtopk,topk=defaulttopk,keyImgUrl=imgUrl, texts=sqlitedb.getTexts(), selectedFile="", totalDifferentWordCount=totalDifferentWordCount)

import os
from datetime import *
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import matplotlib
matplotlib.use('Agg')


def createKeywordImageUrl(keywords):
    imgUrl = u"/image/" + u"test" + u"&" + str(len(keywords)) + u"&" + u" ".join(
        [keyword.name for keyword in keywords]) + u"&" + u" ".join(str(keyword.count) for keyword in keywords)
    return imgUrl


@get('/:id')
def extractFile_action(id):
    if(id == 'favicon.ico'):
        return ''
    textObject = sqlitedb.getText(id)
    if textObject is not None:
        text = textObject.content
    else:
        return None
    charencoding = chardet.detect(text)
    topk = defaulttopk
    keywords = sqlitedb.getKeywords(id, int(-1))

    #words = jieba.__lcut(text);
    #text = nltk.Text(word for word in words)
    #similarWords = text.similar(u'收费')

    if(keywords is not None and len(keywords) > 0):
        imgUrl = createKeywordImageUrl(keywords)
        totalWordCount = 0
        for keyword in keywords:
            totalWordCount += keyword.count
        keywords = sorted(keywords, key=lambda keyword : keyword.count, reverse=True)
        keywordtopk = keywords[:topk]
        imgUrl = createKeywordImageUrl(keywordtopk)
        keyword = domain.Keyword(0, name=u"不同词汇总数", count=len(keywords), textId=-1)
        keywordtopk.append(keyword)
        totalDifferentWordCount = len(set([ keyword.count for keyword in keywords]))
        keyword = domain.Keyword(0, name=u"词汇总数", count=totalWordCount, textId=0)
        keywordtopk.append(keyword)
        keyword = domain.Keyword(0, name=u"关键词临界次数", count=totalDifferentWordCount, textId=0)
        keywordtopk.append(keyword)
        keywordsPercentage = 100*sum([keyword.count for keyword in list(filter((lambda x: x.count > totalDifferentWordCount), keywords))])/totalWordCount
        keyword = domain.Keyword(0, name=u"关键词数量百分比", count=keywordsPercentage, textId=0)
        keywordtopk.append(keyword)
    else:
        tags = jieba.analyse.extract_tags(text, topK=int(-1))
        tagsString = ""
        from nltk.probability import FreqDist
        fd = FreqDist(tags)
        counts = []
        for keyword in tags:
            if charencoding['encoding'] != 'utf-8':
                keywordtext = keyword.encode(charencoding['encoding'])
            else:
                keywordtext = keyword.encode("utf-8")
            count = text.count(keywordtext)
            fd[keyword] = count
            counts.append(str(count))
        totalWordCount = 0
        keywords = []
        for key,val in fd.iteritems():
            keyword = domain.Keyword(id=0, name=key, count=val, textId=0)
            keywords.append(keyword)
            totalWordCount += val
        keywords = sorted(keywords, key=lambda keyword : keyword.count, reverse=True)
        keywordtopk = keywords[:topk]
        imgUrl = createKeywordImageUrl(keywordtopk)

        keyword = domain.Keyword(0, name=u"不同词汇总数", count=len(keywords), textId=0)
        keywordtopk.append(keyword)
        totalDifferentWordCount = len(set([ keyword.count for keyword in keywords]))
        keyword = domain.Keyword(0, name=u"词汇总数", count=totalWordCount, textId=0)
        keywordtopk.append(keyword)
        keyword = domain.Keyword(0, name=u"关键词临界次数", count=totalDifferentWordCount, textId=0)
        keywordtopk.append(keyword)
        keywordsPercentage = 100*sum([keyword.count for keyword in list(filter((lambda x: x.count > totalDifferentWordCount), keywords))])/totalWordCount
        keyword = domain.Keyword(0, name=u"关键词数量百分比", count=keywordsPercentage, textId=0)
        keywordtopk.append(keyword)
    if charencoding['encoding'] != 'utf-8':
        text = unicode(text, charencoding['encoding'], errors="ignore")
    return template("extract_form",content=text,tags=keywordtopk,topk=topk,keyImgUrl=imgUrl, texts=sqlitedb.getTexts(), selectedFile=id, totalDifferentWordCount=totalDifferentWordCount)

@post('/')
@post('/extract')
def extractSubmit_action():
    id = request.forms.selectedFile
    if "extract" in request.forms:
        text = request.forms.text
        #text = "/ ".join(jieba.cut(text))
        topk = int(request.forms.topk)
        defaulttopk = topk
        tags = jieba.analyse.extract_tags(text, topK=int(-1))
        from nltk.probability import FreqDist
        fd = FreqDist(tags)

        #words = jieba.__lcut(text);
        #text = nltk.Text(word for word in words)
        #similarWords = text.similar(u'别墅', 10)

        for keyword in tags:
            #keyword = keyword.encode("utf-8")
            count = text.count(keyword)
            fd[keyword] = count
        keywords = []
        totalWordCount = 0
        words = jieba.cut(text);
        texttemp = nltk.Text(word for word in words)
        for key, val in fd.iteritems():
            keyword = domain.Keyword(id=0, name=key, count=val, textId=0, similarWords='')
            keywords.append(keyword)
            totalWordCount += val
        keywords = sorted(keywords, key=lambda keyword : keyword.count, reverse=True)
        keywordtopk = keywords[:topk]
        for tempkeyword in keywordtopk:
            textword = tempkeyword.name.encode("utf-8");
            texttemp.similar(textword)
            tempsimilarWords = texttemp._word_context_index.similar_words(tempkeyword.name)
            tempsimilarWordsStr = u" ".join(tempsimilarWords)
            # tempsimilarWordsStr = str(tempsimilarWords)
            tempkeyword.similarWords = tempsimilarWordsStr;
        imgUrl = createKeywordImageUrl(keywordtopk)
        keyword = domain.Keyword(0, name=u"不同词汇总数", count=len(keywords), textId=-1, similarWords='')
        keywordtopk.append(keyword)
        totalDifferentWordCount = len(set([ keyword.count for keyword in keywords]))
        keyword = domain.Keyword(0, name=u"词汇总数", count=totalWordCount, textId=0, similarWords='')
        keywordtopk.append(keyword)
        keyword = domain.Keyword(0, name=u"关键词临界次数", count=totalDifferentWordCount, textId=0, similarWords='')
        keywordtopk.append(keyword)
        keywordsPercentage = 100*sum([keyword.count for keyword in list(filter((lambda x: x.count > totalDifferentWordCount), keywords))])/totalWordCount
        keyword = domain.Keyword(0, name=u"关键词数量百分比", count=keywordsPercentage, textId=0, similarWords='')
        keywordtopk.append(keyword)
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
            author = ""
            period = ""
            uploader = ""
            charencoding = chardet.detect(text)
            text = unicode(text, charencoding['encoding'], errors="ignore")
            textObject = domain.Text('',name,author,period,fn,uploader,'',text)
            id = sqlitedb.addText(textObject)
            topk = int(request.forms.topk)
            defaulttopk = topk
            tags = jieba.analyse.extract_tags(text, topK=-1)
            from nltk.probability import FreqDist
            fd = FreqDist(tags)
            for keyword in tags:
                #keyword = keyword.encode("utf-8")
                count = text.count(keyword)
                fd[keyword] = count
            keywords = []
            totalWordCount = 0
            for key,val in fd.iteritems():
                keyword = domain.Keyword(0, name=key, count=val, textId=id)
                keywords.append(keyword)
                totalWordCount += val
            sqlitedb.addKeywords(keywords)
            keywordtopk = keywords[:topk]
            imgUrl = createKeywordImageUrl(keywordtopk)
            keyword = domain.Keyword(0, name=u"不同词汇总数", count=len(keywords), textId=-1)
            keywordtopk.append(keyword)
            totalDifferentWordCount = len(set([ keyword.count for keyword in keywords]))
            keyword = domain.Keyword(0, name=u"词汇量总数", count=totalWordCount, textId=0)
            keywordtopk.append(keyword)
            keyword = domain.Keyword(0, name=u"关键词临界次数", count=totalDifferentWordCount, textId=0)
            keywordtopk.append(keyword)
            keywordsPercentage = 100*sum([keyword.count for keyword in list(filter((lambda x: x.count > totalDifferentWordCount), keywords))])/totalWordCount
            keyword = domain.Keyword(0, name=u"关键词数量百分比", count=keywordsPercentage, textId=0)
            keywordtopk.append(keyword)

    return template("extract_form",content=text,tags=keywordtopk,topk=topk,keyImgUrl=imgUrl, texts=sqlitedb.getTexts(), selectedFile=id, totalDifferentWordCount=totalDifferentWordCount)

@post('/analyze')
def analyzefile():
    text = request.json['text']
    response.headers['Content-Type'] = 'application/json'

    # text = "/ ".join(jieba.cut(text))
    topk = 100
    defaulttopk = topk
    tags = jieba.analyse.extract_tags(text, topK=int(-1))
    from nltk.probability import FreqDist
    fd = FreqDist(tags)

    # words = jieba.__lcut(text);
    # text = nltk.Text(word for word in words)
    # similarWords = text.similar(u'别墅', 10)

    for keyword in tags:
        # keyword = keyword.encode("utf-8")
        count = text.count(keyword)
        fd[keyword] = count
    keywords = []
    totalWordCount = 0
    words = jieba.cut(text);
    texttemp = nltk.Text(word for word in words)
    for key, val in fd.iteritems():
        keyword = domain.Keyword(id=0, name=key, count=val, textId=0, similarWords='')
        keywords.append(keyword)
        totalWordCount += val
    keywords = sorted(keywords, key=lambda keyword: keyword.count, reverse=True)
    keywordtopk = keywords[:topk]
    for tempkeyword in keywordtopk:
        textword = tempkeyword.name.encode("utf-8");
        texttemp.similar(textword)
        tempsimilarWords = texttemp._word_context_index.similar_words(tempkeyword.name)
        tempsimilarWordsStr = u" ".join(tempsimilarWords)
        # tempsimilarWordsStr = str(tempsimilarWords)
        tempkeyword.similarWords = tempsimilarWordsStr;

    json_string = json.dumps([tempkeyword.__dict__ for tempkeyword in keywordtopk])

    return json_string;


@get('/managefile')
def managefile():
    return template("managefile_form", texts=sqlitedb.getTexts())

@post('/managefile')
def managefile():
    if "upload" in request.forms:
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
            charencoding = chardet.detect(text)
            text = unicode(text, charencoding['encoding'], errors="ignore")
            textObject = domain.Text('',name,author,period,fn,uploader,'',text)
            sqlitedb.addText(textObject)
    else:
        checkedtexts = request.forms.dict['checkedtext']
        print checkedtexts
        sqlitedb.deleteTexts(checkedtexts)
    return template("managefile_form", texts=sqlitedb.getTexts())

@get('/cut')
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
峨嵋山下少人行，旌旗无光日色薄。
蜀江水碧蜀山青，圣主朝朝暮暮情。
行宫见月伤心色，夜雨闻铃肠断声。
天旋日转回龙驭，到此踌躇不能去。
马嵬坡下泥土中，不见玉颜空死处。
君臣相顾尽沾衣，东望都门信马归。
归来池苑皆依旧，太液芙蓉未央柳。
芙蓉如面柳如眉，对此如何不泪垂。
春风桃李花开日，秋雨梧桐叶落时。
西宫南内多秋草，落叶满阶红不扫。
梨园弟子白发新，椒房阿监青娥老。
夕殿萤飞思悄然，孤灯挑尽未成眠。
迟迟钟鼓初长夜，耿耿星河欲曙天。
鸳鸯瓦冷霜华重，翡翠衾寒谁与共。
悠悠生死别经年，魂魄不曾来入梦。
子曰：「学而时习之，不亦说乎？有朋自远方来，不亦乐乎？人不知而不愠，不亦君子乎？」
'''
    return template("cut_form",content=sample_sentences,selected=functools.partial(match,1))

@post('/cut')
def cut_action():
    from jieba import posseg
    # jieba.load_userdict("D:\Ctrip\github\jiebademo\jiebademo\jieba\dict_old.txt")
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

@get('/design/sequence')
def desgin_sequence():
    return template("design_sequence_form")

if __name__ == "__main__":
    # Interactive mode
    #debug(True)
    #run(server='CherryPy',host='localhost', port=8080, debug=True)
    run(host='localhost', port=8083, reloader=True)
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
