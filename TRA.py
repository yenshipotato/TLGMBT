import json
import auth
import datetime
import user_inf

class TrainInf:
    def __init__(self,TrainNum,TrainTypeName,TrainDate,TimeO,TimeD):

        self.TrainNum=TrainNum
        self.TrainTypeName=TrainTypeName
        self.TrainDate=TrainDate
        self.TourTime=datetime.datetime.strptime(TimeD,"%H:%M")-datetime.datetime.strptime(TimeO,"%H:%M")
        self.prtTime="<b>"+TimeO+"</b>"+" → "+"<b>"+TimeD+"</b>"

        if self.TrainTypeName.find("(")!=-1:
            self.TrainTypeName=self.TrainTypeName[0:self.TrainTypeName.find("(")]
    def format(self):
        
        return (self.TrainDate+'  \n車次：'+self.TrainNum+"  車種："+self.TrainTypeName+"\n"+self.prtTime+" ， "+str(self.TourTime.seconds//60)+"mins")

def toTelegram(id,message):
    s = message.split(' ')

    if s.__len__() ==2:
        user_inf.setLatest(id,s[1]+" "+s[0])
        user_inf.setRecord(id,s[0]+" "+s[1])

        timeStr=OtoD(s[0],s[1])
        if timeStr!="":
            user_inf.setLasttime(id,timeStr[timeStr.rfind("-")-2:timeStr.rfind("-")]+timeStr[timeStr.rfind("-")+1:timeStr.rfind("-")+3]+" "+timeStr[timeStr.rfind("→ ")-10:timeStr.rfind("→ ")-5])
            return timeStr
        else:
            return ("Not Found")

    elif s.__len__()==4:
        user_inf.setLatest(id,s[0]+" "+s[3]+" "+s[2])
        user_inf.setRecord(id,s[2]+" "+s[3])
        
        date=datetime.date(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+8))).date().year,int(s[0][0:2]),int(s[0][2:4]))
        time=datetime.time(int(s[1]),0,0,0)
        time=datetime.datetime.combine(date,time)

        timeStr=(OtoD(s[2],s[3],str(date),time))
        if timeStr!="":
            user_inf.setLasttime(id,timeStr[timeStr.rfind("-")-2:timeStr.rfind("-")]+timeStr[timeStr.rfind("-")+1:timeStr.rfind("-")+3]+" "+timeStr[timeStr.rfind("→ ")-10:timeStr.rfind("→ ")-5])
            return timeStr
        else:
            return ("Not Found")

    elif s.__len__()==3:
        user_inf.setLatest(id,s[0]+" "+s[2]+" "+s[1])
        user_inf.setRecord(id,s[1]+" "+s[2])

        if s[0].__len__()==4:
            date=datetime.date(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+8))).date().year,int(s[0][0:2]),int(s[0][2:4]))
            time=datetime.time(4,0,0,0)
            time=datetime.datetime.combine(date,time)

            timeStr=(OtoD(s[1],s[2],str(date),time))
            if timeStr!="":
                user_inf.setLasttime(id,timeStr[timeStr.rfind("-")-2:timeStr.rfind("-")]+timeStr[timeStr.rfind("-")+1:timeStr.rfind("-")+3]+" "+timeStr[timeStr.rfind("→ ")-10:timeStr.rfind("→ ")-5])
                return timeStr
            else:
                return ("Not Found")   

        elif s[0].__len__()<=2:
            time=datetime.time(int(s[0]),0,0,0)
            time=datetime.datetime.combine(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+8))).date(),time)
            
            timeStr=(OtoD(s[1],s[2],timeFlag=time))
            if timeStr!="":
                user_inf.setLasttime(id,timeStr[timeStr.rfind("-")-2:timeStr.rfind("-")]+timeStr[timeStr.rfind("-")+1:timeStr.rfind("-")+3]+" "+timeStr[timeStr.rfind("→ ")-10:timeStr.rfind("→ ")-5])
                return timeStr
            else:
                return ("Not Found")
    
    else :
        return "Input Error"

def Train_later(id):
    s=(user_inf.getLasttime(id)+" "+user_inf.getRecord(id)).split(' ')
        
    date=datetime.date(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+8))).date().year,int(s[0][0:2]),int(s[0][2:4]))
    time=datetime.time(int(s[1][0:2]),int(s[1][3:5]),0,0)
    time=datetime.datetime.combine(date,time)

    timeStr=(OtoD(s[2],s[3],str(date),time))
    if timeStr!="":
        user_inf.setLasttime(id,timeStr[timeStr.rfind("-")-2:timeStr.rfind("-")]+timeStr[timeStr.rfind("-")+1:timeStr.rfind("-")+3]+" "+timeStr[timeStr.rfind("→ ")-10:timeStr.rfind("→ ")-5])
        return timeStr
    else:
        return ("Not Found")

def stationInf(name,data):
    if(name[0]=='台'):
        name="臺"+name[1::]

    return data.get(name)

def TimeInf():
    with open("Today.json",encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)

def OtoD(station1,station2,date=str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+8))).date()),timeFlag=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+8)))):
    
    with open("TRAID.json",encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)

    Oringin=stationInf(station1,data)
    Dest=stationInf(station2,data)
    

    res = auth.crawl("https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/DailyTimetable/OD/"+
                    Oringin+"/to/"+Dest+"/"+date+
                    "?$format=JSON")

    Train=[]
    s=str("")
    timeFlag=datetime.datetime.combine(timeFlag.date(),timeFlag.time())
    for t in res.json():
        if Train.__len__()>=5:
            break
        if datetime.datetime.strptime(date+' '+ t['OriginStopTime']['DepartureTime'],"%Y-%m-%d %H:%M")>=timeFlag:
            Train.append(t)
    
    for i in range(0,5):
        if i>=Train.__len__():
            break

        inf=TrainInf(Train[i]["DailyTrainInfo"]["TrainNo"],Train[i]["DailyTrainInfo"]["TrainTypeName"]["Zh_tw"],Train[i]["TrainDate"],
                    Train[i]['OriginStopTime']['DepartureTime'],Train[i]['DestinationStopTime']['ArrivalTime'])
        
        s=s+inf.format()+'\n\n'

    return s[0:s.__len__()-2]


    
if __name__ == '__main__':
    #print(OtoD("台南","台北"))
    #print(OtoD("台北","松山"))
    user_inf.readData(730270828)
    
    print(toTelegram(730270828,"善化 台中"))
    print(user_inf.getLasttime(730270828))
    user_inf.saveAll()