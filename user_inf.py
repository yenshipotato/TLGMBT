import json
import os

usr_dic={}

def adduser(id):
    user={"latest":"","favorite":"","status":0,"lasttime":"14"}
    usr_dic[str(id)]=user
def wInFile(id):
    with open("user/"+str(id)+".json","w",encoding="utf-8") as f:
        json.dump(usr_dic[str(id)],f,ensure_ascii=False)
def saveAll():
    for key,value in usr_dic.items():
        wInFile(int(key))

def setLatest(id,latest):
    usr_dic[str(id)]["latest"]=latest
def setFavorite(id,F):
    usr_dic[str(id)]["favorite"]=F
def setStatus(id,S):
    usr_dic[str(id)]["status"]=S
def setLasttime(id,L):
    usr_dic[str(id)]["lasttime"]=L
def setRecord(id,R):
    usr_dic[str(id)]["record"]=R

def getLatest(id):
    return usr_dic[str(id)]["latest"]
def getFavorite(id):
    return usr_dic[str(id)]["favorite"]
def getStatus(id):
    return usr_dic[str(id)]["status"]
def getLasttime(id):
    return usr_dic[str(id)]["lasttime"]
def getRecord(id):
    return usr_dic[str(id)]["record"]    

def readData(id):
    if os.path.isfile("user/"+str(id)+".json"):
        #print("檔案存在。")
        with open("user/"+str(id)+".json",encoding="utf-8") as f:
            a=json.load(f)
        usr_dic[str(id)]=a
        
    else:
        #print("檔案不存在。")
        adduser(id)
        



if __name__ == '__main__':
    adduser(1013334846)
    setLatest(1013334846,"善化 南科")
    setFavorite(1013334846,"善化 台南")
    setStatus(1013334846,1)
    wInFile(1013334846)