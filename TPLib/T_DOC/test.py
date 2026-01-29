import json
from Tsugi import Tsugi, WashBlocks, JSON2TDOC, TDOC2JSON


f=open('./.test.json','r',encoding='utf-8')
tdoc = json.load(f)["drawflow"]["Home"]["data"]
f.close()

func = WashBlocks(tdoc)

f=open('./.func.json','w', encoding='UTF-8')
f.write(json.dumps(tdoc, ensure_ascii=False, indent=4)) # 缩进
f.close()

#f=open('./func.tdoc','wb')
#f.write(JSON2TDOC(func))
#f.close()

#f=open('./func.tdoc','rb')
#func=TDOC2JSON(f.read())
#f.close()


t=Tsugi(func, debug=False)
t.run()
input()