from elasticsearch import Elasticsearch
from flask import Flask,render_template, url_for, request
app=Flask(__name__)
es = Elasticsearch('127.0.0.1', port=9200)

@app.route('/')
def home():
    return render_template('search.html')
    
@app.route('/search/results', methods=['POST'])
def reqst():
    search_term = request.form["input"]
    search_term=search_term.lower()
    if ' ' in search_term:
        term=search_term
        search_term=search_term.split(" ")
        res=getdata(search_term,"2")
    else:
        term=search_term
        res=getdata(search_term,"1")
    if len(res)==0:
        return render_template('error.html')
    return render_template('results.html',res=res,inputs=term)

def getdata(search_term,flag):
    res=[]
    if flag=="1":
        try:
            mm=es.get(index='storage',doc_type='dbs',id=search_term)
            for i in mm['_source'][search_term]:
                res.append(i)
        except:
            pass
    elif flag=="2":
        for i in search_term:
            try:
                mm=es.get(index='storage',doc_type='dbs',id=i)
                for j in mm['_source'][i]:
                    res.append(j)
            except:
                pass
    return res
    
if __name__=='__main__':
    app.run(host="0.0.0.0",port=80)
