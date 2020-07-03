import requests
import json

r=requests.session()


out=r.get("http://127.0.0.1:9200/storage/")

out= json.loads(out.text)

for i in out["storage"]["mappings"]["dbs"]["properties"]:
    print(i)
