from flask import Flask, request, abort
from flask import jsonify
from newsapi import NewsApiClient
import json
import datetime
import string
from collections import Counter as cnt
application = Flask(__name__,static_url_path='')

newsapi = NewsApiClient(api_key='cd8354b9683141f1a67cd5eb340f27bb')

@application.route('/index')
def hello_world():
    return application.send_static_file("hw6.html")

# @application.route("/data")
# def getdata():
#     return jsonify({"error":"Invalid email"})

@application.route("/getAllSources")
def getAllSources():
    mylist1=[]
    mydict1={}
    myid=''
    myname=''
    # cid = request.args.get('category')
    sources = newsapi.get_sources(language='en',country='us')
    for x in sources:
        if x=='sources':
            for y in sources[x]:
                for z in y:
                    if z=='id':
                        myid=y[z]
                    if z=='name':
                        myname=y[z]
                mydict1={'id':myid,'name':myname}
                mylist1.append(mydict1)
    return jsonify(mylist1)
    return 'OK'

@application.route("/sources")
def getCategory():
    mylist1=[]
    mydict1={}
    myid=''
    myname=''
    cid = request.args.get('category')
    sources = newsapi.get_sources(language='en',country='us',category=cid)
    for x in sources:
        if x=='sources':
            for y in sources[x]:
                for z in y:
                    if z=='id':
                        myid=y[z]
                    if z=='name':
                        myname=y[z]
                mydict1={'id':myid,'name':myname}
                mylist1.append(mydict1)
    return jsonify(mylist1)
    return 'OK'

@application.route("/everything")
def getNews():
    news=""
    mydict2={}
    mylist2=[]
    keyword = request.args.get('q')
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    source = request.args.get('sources')
    news = newsapi.get_everything(q=keyword,from_param=from_date,to=to_date,sources=source,language='en',page_size=30,sort_by='publishedAt')
    print("this is news",news)
    flag=False
    for x in news:
        if(x=='status'):
            if news[x]=="error":
                print("error occurred")
        if(x=='articles'):
            for y in news[x]:
                for z in y:
                    if(z=='source'):
                        temp={}
                        temp = y[z]
                        for x in temp:
                            if(temp[x]=='' or temp[x]==None or temp[x]=="null"):
                                flag=True
                            else:
                                if x=='name':
                                    source_name = temp[x]
                    if z=='urlToImage':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            imageUrl = y[z]
                        else:
                            flag=True
                    if z=='title':
                         if y[z]!='' and y[z]!=None and y[z]!="null":
                             newsTitle = y[z]
                         else:
                             flag=True
                    if z=='description':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            newsD = y[z]
                        else:
                            flag=True
                    if z=='url':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            newsUrl = y[z]
                        else:
                            flag=True
                    if z=='author':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            author = y[z]
                        else:
                            flag=True
                            # print("author made flag true ")
                    if z=='publishedAt':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            publishedAt = y[z]
                        else:
                            flag=True
                if flag!=True:
                    mydict2={'Image':imageUrl,'Title':newsTitle,'Description':newsD,'URL':newsUrl,'Author':author,'Source':source_name,'Date':publishedAt}
                    mylist2.append(mydict2)
                flag=False

    return jsonify(mylist2)
    return 'OK'

@application.route("/everything")
def debugEverythig():
    abort(500)
@application.errorhandler(500)
def throwError(e):
    print(e)
    error = str(e)
    return jsonify(error)

@application.route("/fromAllSources")
def getAllNews():
    print("reached call")
    news=""
    mydict2={}
    mylist2=[]
    keyword = request.args.get('q')
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    # source = request.args.get('sources')
    news = newsapi.get_everything(q=keyword,from_param=from_date,to=to_date,language='en',page_size=30,sort_by='publishedAt')
    flag=False
    for x in news:
        if(x=='articles'):
            for y in news[x]:
                for z in y:
                    if(z=='source'):
                        temp={}
                        temp = y[z]
                        for x in temp:
                            if(temp[x]=='' or temp[x]==None  or temp[x]=="null"):
                                flag=True
                            else:
                                if x=='name':
                                    source_name = temp[x]
                    if z=='urlToImage':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            imageUrl = y[z]
                        else:
                            flag=True
                    if z=='title':
                         if y[z]!='' and y[z]!=None and y[z]!="null":
                             newsTitle = y[z]
                         else:
                             flag=True
                    if z=='description':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            newsD = y[z]
                        else:
                            flag=True
                    if z=='url':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            newsUrl = y[z]
                        else:
                            flag=True
                    if z=='author':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            author = y[z]
                        else:
                            flag=True
                            # print("author made flag true ")
                    if z=='publishedAt':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            publishedAt = y[z]
                        else:
                            flag=True
                if flag!=True:
                    mydict2={'Image':imageUrl,'Title':newsTitle,'Description':newsD,'URL':newsUrl,'Author':author,'Source':source_name,'Date':publishedAt}
                    mylist2.append(mydict2)
                flag=False
    return jsonify(mylist2)
    return 'OK'

@application.route("/fromAllSources")
def debugfromAllSources():
    abort(500)

@application.route("/top_headlines")
def getTopHeadlines():
    top_headlines = ""
    wordString=""
    top_headlines = newsapi.get_top_headlines(language='en',
                                              country='us',
                                              page_size=30)
    flag=False
    mydict={}
    mylist=[]
    for x in top_headlines:
        if(x=='articles'):
            for y in top_headlines[x]:
                for z in y:
                    if(z=='source'):
                        temp={}
                        temp = y[z]
                        for x in temp:
                            if(temp[x]=='' or temp[x]==None  or temp[x]=="null"):
                                flag=True
                    if z=='urlToImage':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            imageUrl = y[z]
                        else:
                            flag=True
                    if z=='title':
                         if y[z]!='' and y[z]!=None and y[z]!="null":
                             newsTitle = y[z]
                         else:
                             flag=True
                    if z=='description':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            newsD = y[z]
                        else:
                            flag=True
                    if z=='url':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            newsUrl = y[z]
                        else:
                            flag=True
                    if z=='author':
                        if y[z]=='' or y[z]==None or y[z]=="null":
                            flag=True
                    if z=='publishedAt':
                        if y[z]=='' or y[z]==None or y[z]=="null":
                            flag=True
                if flag!=True:
                    wordString+=newsTitle
                    mydict={'Image':imageUrl,'Title':newsTitle,'Description':newsD,'URL':newsUrl}
                    mylist.append(mydict)
                flag=False
    return jsonify(mylist)
    mylist.clear()
    mydict.clear()

@application.route("/getWordCloud")
def getWordCloud():
    top_headlines = ""
    wordString=""
    top_headlines = newsapi.get_top_headlines(language='en',
                                              country='us',
                                              page_size=80)
    flag=False
    mydict={}
    mylist=[]
    for x in top_headlines:
        if(x=='articles'):
            for y in top_headlines[x]:
                for z in y:
                    if(z=='source'):
                        temp={}
                        temp = y[z]
                        for x in temp:
                            if(temp[x]=='' or temp[x]==None  or temp[x]=="null"):
                                flag=True
                    if z=='urlToImage':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            imageUrl = y[z]
                        else:
                            flag=True
                    if z=='title':
                         if y[z]!='' and y[z]!=None and y[z]!="null":
                             newsTitle = y[z]
                         else:
                             flag=True
                    if z=='description':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            newsD = y[z]
                        else:
                            flag=True
                    if z=='url':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            newsUrl = y[z]
                        else:
                            flag=True
                    if z=='author':
                        if y[z]=='' or y[z]==None or y[z]=="null":
                            flag=True
                    if z=='publishedAt':
                        if y[z]=='' or y[z]==None or y[z]=="null":
                            flag=True
                if flag!=True:
                    wordString+=newsTitle
                    mydict={'Image':imageUrl,'Title':newsTitle,'Description':newsD,'URL':newsUrl}
                    mylist.append(mydict)
                flag=False
    print("this is wordstring",wordString)
    alp=""
    alp2=""
    for char in wordString:
        if char.isalnum() or char.isspace():
            alp+=char
    for char in alp:
        if (not char.isdigit()):
            alp2+=char
    print("this is alp",alp2)
    splitList = alp2.split()
    Counter = cnt(splitList)
    most_occur = Counter.most_common(100)
    print(most_occur)
    wordList=[]
    for k,v in most_occur:
        # print(k)
        wordList.append(k)
    stopWordList=[]
    newList=[]
    
    file = open("stopwords_en.txt","r")
    lines = file.readlines()
    for l in lines:
        stopWordList.append(l.split('\n')[0])

    print("stopWordList",stopWordList)
    for i in stopWordList:
        newList.append(i)
        # print(i)
        x=i.capitalize()
        # print(x)
        newList.append(x)
    print("stopWordList",newList)
    finalList = list(set(wordList)-set(newList))
    print("useful",finalList)
    return jsonify(finalList)
    # return jsonify(mylist)
    mylist.clear()
    mydict.clear()


@application.route("/cnn_headlines")
def getCNNHeadlines():
    cnn_news = ""
    cnn_news = newsapi.get_top_headlines(language='en',
                                         page_size=10,
                                         sources='cnn')
    mydict={}
    mylist_cnn=[]
    flag=False
    for x in cnn_news:
        #print("%%%%%%%%%%%%%%%%%%%%%%%%%%",x)
        # #print(type(x))
        if(x=='articles'):
            for y in cnn_news[x]:
                #print(y)
                for z in y:
                    #print(z,"=",y[z])
    #                 #print(y[z])
                    if(z=='source'):
                        temp={}
                        temp = y[z]
                        #print(temp)
                        #print(y[z])
                        for x in temp:
                            #print(x,"=",temp[x])
                            if(temp[x]=='' or temp[x]==None  or temp[x]=="null"):
                                flag=True
                                #print("source made flag true ")
                    if z=='urlToImage':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            imageUrl = y[z]
                        else:
                            flag=True
                            #print("urlToImage made flag true ")
                    if z=='title':
                         if y[z]!='' and y[z]!=None and y[z]!="null":
                             newsTitle = y[z]
                         else:
                             flag=True
                             #print("title made flag true ")
                    if z=='description':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            newsD = y[z]
                        else:
                            flag=True
                            #print("desc made flag true ")
                    if z=='url':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            newsUrl = y[z]
                        else:
                            flag=True
                            #print("url made flag true ")
                    if z=='author':
                        if y[z]=='' or y[z]==None or y[z]=="null":
                            flag=True
                            #print("author made flag true ")
                    if z=='publishedAt':
                        if y[z]=='' or y[z]==None or y[z]=="null":
                            flag=True
                            #print("publishedAt made flag true ")
                #print(flag)
                if flag!=True:
                    mydict={'Image':imageUrl,'Title':newsTitle,'Description':newsD,'URL':newsUrl}
                    mylist_cnn.append(mydict)
                # #print("#printing every dictionary",mydict)
                flag=False

    return jsonify(mylist_cnn)
    mylist_cnn.clear()
    mydict.clear()

@application.route("/fox_headlines")
def getFoxHeadlines():
    fox_news = ""
    fox_news = newsapi.get_top_headlines(language='en',
                                         page_size=10,
                                         sources='fox-news')
    mydict={}
    mylist_fox=[]
    flag=False
    for x in fox_news:

        if(x=='articles'):
            for y in fox_news[x]:
                #print(y)
                for z in y:
                    #print(z,"=",y[z])
    #                 #print(y[z])
                    if(z=='source'):
                        temp={}
                        temp = y[z]
                        #print(temp)
                        #print(y[z])
                        for x in temp:
                            #print(x,"=",temp[x])
                            if(temp[x]=='' or temp[x]==None  or temp[x]=="null"):
                                flag=True
                                #print("source made flag true ")
                    if z=='urlToImage':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            imageUrl = y[z]
                        else:
                            flag=True
                            #print("urlToImage made flag true ")
                    if z=='title':
                         if y[z]!='' and y[z]!=None and y[z]!="null":
                             newsTitle = y[z]
                         else:
                             flag=True
                             #print("title made flag true ")
                    if z=='description':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            newsD = y[z]
                        else:
                            flag=True
                            #print("desc made flag true ")
                    if z=='url':
                        if y[z]!='' and y[z]!=None and y[z]!="null":
                            newsUrl = y[z]
                        else:
                            flag=True
                            #print("url made flag true ")
                    if z=='author':
                        if y[z]=='' or y[z]==None or y[z]=="null":
                            flag=True
                            #print("author made flag true ")
                    if z=='publishedAt':
                        if y[z]=='' or y[z]==None or y[z]=="null":
                            flag=True
                            #print("publishedAt made flag true ")
                #print(flag)
                if flag!=True:
                    mydict={'Image':imageUrl,'Title':newsTitle,'Description':newsD,'URL':newsUrl}
                    mylist_fox.append(mydict)
                # #print("#printing every dictionary",mydict)
                flag=False

    return jsonify(mylist_fox)
    mylist_fox.clear()
    mydict.clear()


if __name__ == "__main__":
    application.run(debug=True)
