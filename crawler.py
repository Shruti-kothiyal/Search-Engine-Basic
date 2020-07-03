import asyncio
import aiohttp
import re
import sys
import pickle
from os import system


#security measure
verify={}
#for taking headings and titles
slate=[]
final={}

#for indexing
indexing={}
keeper=[]

#for logging data
counter=0

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main(url):
    global slate,counter
    url_list=[url]
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        while True:
            if url_list:
                for i in url_list:

                    print("==========URL :  {} =========== ".format(i))
                    url=i
                    #print (url_list)
                    try:
                        html = await fetch(session, i)
                        urlz = i
                    except:
                        pass
                    x=re.findall("href=\"[http?://]+.+\"/?>",html)
                    for i in x:
                        j=re.sub("href=\"","",i)
                        #print(j)
                        z=re.findall("http[?s]:\/\/+.+\"\s",j)
                        if len(z)<=0:
                            j=re.findall("\/+.+\"\s",j)
                        else:
                            j=z
                        #print(j)
                        z=re.sub("\"\s+.+","",str(j))
                        if len(z)<=0:
                            j=re.sub("\"\s","",str(j))
                        else:
                            j=z
                        j=j.replace(" ","")
                        j=j.replace("['","")
                        set = re.compile("^\/\/")
                        if set.search(j)!=None:
                            j=j.replace("//",urlz)
                        set = re.compile("http[s:]+\/\/")
                        if set.search(j)==None:
                            j=urlz+j
                        if j.find("[]"):
                            j=j.replace("[]","")
                        
                        if (j):
                            if j in verify:
                                pass
                            else:
                                if len(j)>50:
                                    verify[j]='i'
                                    pass
                                else:
                                    verify[j]='1'
                                    url_list.append(j)
                                    m=re.findall("<title>.+[</title>]|<h1>.+[/h1>]|<h2>.+[/h2>]",html)
                                    slate.clear()
                                    for i in m:
                                        m=re.sub("<title>|<h1>|<h2>|</title>|</h1>|</h2>","",i)
                                        if len(m)<50:
                                            #print (len(m))

                                            slate.append(m)
                                            slate=list(dict.fromkeys(slate))
                                            final[j]=slate
                                        else:
                                            #print (m)
                                            final[j]="1"
                                    try:
                                        if final[j]!="1":
                                            for i in final[j]:
                                                i=i.split()
                                                #print (i)
                                                for s in i:
                                                    if len(s)>3:
                                                        if s in indexing:
                                                            keeper=indexing[s]
                                                            keeper.append(j)
                                                            del indexing[s]
                                                            indexing[s]=keeper
                                                        else:
                                                            indexing[s]=[j]
                                                        counter=counter+1
                                                        #print (s)
                                            #print(counter)
                                            if counter>100:
                                                if system("wc -w dump.pickle > /dev/null 2>&1 ")==0:

                                                    pass

                                                else:

                                                    pickle_out = open("dump.pickle","wb")
                                                    pickle.dump(indexing, pickle_out)
                                                    pickle_out.close()
                                                    indexing.clear()
                                                    counter=0

                                            print (j)


                                    except:
                                        pass
                                    #print (j)
                    url_list.remove(url)


            else:
                sys.exit()








def start(url):
    try:
        slate.clear()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(url))
    except:
        #this is incase program crash so it won't lose the scraped data
        pickle_out = open("crash.pickle","wb")
        pickle.dump(indexing, pickle_out)
        pickle_out.close()
        indexing.clear()
