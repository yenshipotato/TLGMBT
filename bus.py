import auth
import json
import requests
import math

def rt(place,route):
    res = auth.crawl("https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/City/"+place+"/"+route+"?$orderby=StopSequence&$format=JSON")
    res1 = auth.crawl("https://ptx.transportdata.tw/MOTC/v2/Bus/DisplayStopOfRoute/City/"+place+"/"+route+"?$format=JSON")

    data = res.json()
    data1 = res1.json()

    time=list()
    stop=list()
    srtdStop=list()

    time0=list()
    time1=list() 

    if data.__len__()==0:
        return 0

    for inf in data:
        if inf["RouteName"]["Zh_tw"]==route:
            if "EstimateTime" in inf.keys():
                time.append((inf["StopSequence"],inf['StopName']["Zh_tw"],inf["EstimateTime"]))
            elif inf["StopStatus"]==1:
                time.append((inf["StopSequence"],inf['StopName']["Zh_tw"],"尚未發車"))
            elif inf["StopStatus"]==2:
                time.append((inf["StopSequence"],inf['StopName']["Zh_tw"],"交管不停靠"))
            elif inf["StopStatus"]==3:
                time.append((inf["StopSequence"],inf['StopName']["Zh_tw"],"末班駛離"))
            elif inf["StopStatus"]==4:
                time.append((inf["StopSequence"],inf['StopName']["Zh_tw"],"今日未營運"))
            
    
    for inf in data1:
        if inf["RouteName"]["Zh_tw"]==route:
            stop=inf["Stops"]
    
    
    for stopInf in stop:
        srtdStop.append(stopInf["StopName"]["Zh_tw"])

    for Inf in srtdStop:
        for timing in time:
            if timing[1]==Inf:
                if type(timing[2])==type(1):
                    if timing[2]<120:
                        time0.append(timing[1]+"  即將進站")
                    else:
                        time0.append(timing[1]+"  "+str(timing[2]//60)+"min")
                else:
                    time0.append(timing[1]+"  "+str(timing[2]))
    if time.__len__()!=stop.__len__():
        time1=time0[1::2]
        time0=time0[::2]
        time1.reverse()
        return((time0,time1))
    return(time0)

# place="Tainan"
# route="6"

def toTelegram(place,route):
    temp=rt(place,route)
    str1=str()
    str2=str()



    if type(temp) == type([0,1]) :
        #return temp
        for rslt in temp:
            str1=str1+rslt+"\n"
        return str1[0:str1.__len__()-1]
    elif type(temp) == type((0,1)) :
        for rslt in temp[0]:
            str1=str1+rslt+"\n"
        for rslt in temp[0]:
            str2=str1+rslt+"\n"
        return (str1[0:str1.__len__()-1],str2[0:str2.__len__()-1])

    else:
        return "沒有路線結果"
    

if __name__ == '__main__':
    print(toTelegram("Tainan","6"))


