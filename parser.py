import pickle
from os import system
from elasticsearch import Elasticsearch
import re
import time



def main():
    global resh
    es=Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
    temp_list=[]
    if system("wc -w dump.pickle > /dev/null 2>&1 &")==0:
        pickle_in = open("dump.pickle","rb")
        indexing = pickle.load(pickle_in)
        system("rm dump.pickle > /dev/null 2>&1 &")
        for i in indexing:
            temps=i
            i=re.sub("[^a-zA-Z]","",i)
            str=""
            i=str.join(i)
            if i=="":
                pass
            else:
                resh=es.exists(index='storage',doc_type='dbs',id=i.lower())
        #print(i)
            if resh==True:
                try:
                    #print ("i is {}".format(i))
                    res=es.get(index='storage',doc_type='dbs',id=i.lower())
                    temp_list=res['_source'][i.lower()]
                    for m in indexing[temps]:
                        temp_list.append(m)
                    data={
                    i.lower():temp_list,
                    }
                    res = es.index(index="storage", doc_type='dbs', body=data,id=i.lower())
                    if res['_shards']['successful']==1:
                        print("modified")
                    else:
                        print("ERROR!!!")
                except:
                    pass
            elif resh==False:
                data={
                    i.lower():indexing[temps],
                    }
                try:
                    res = es.index(index="storage", doc_type='dbs', body=data,id=i.lower())
                    if res['_shards']['successful']==1:
                        print("Uploaded")
                    else:
                        print("not uploaded")
                except:
                    pass
    else:
        pass


while True:

    if system("wc -w dump.pickle 2 > /dev/null 2>&1 &")==0:
        try:
            main()
        except:
            pass
    time.sleep(10)
