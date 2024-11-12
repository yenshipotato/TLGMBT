import json
import auth
import datetime
import time
import thsr_usr
import ticket

lst=dict()

class TrainInf:
    def __init__(self,TrainNum,TrainDate,TimeO,TimeD,oID,dID):
        global lst
        self.TrainNum=TrainNum
        self.TrainDate=TrainDate
        self.TourTime=datetime.datetime.strptime(TimeD,"%H:%M")-datetime.datetime.strptime(TimeO,"%H:%M")
        self.prtTime="<b>"+TimeO+"</b>"+" → "+"<b>"+TimeD+"</b>"
        self.ticket=ticket.Ticket(ticket.getTicket(self.TrainDate,lst,self.TrainNum))
        self.O=oID
        self.D=dID

    def format(self):
        self.ticket.ini()
        
        return (self.TrainDate+'  車次：'+self.TrainNum+"\n"+self.prtTime+" ， "+str(self.TourTime.seconds//60)+"mins\n"+self.ticket.getStatus(self.O,self.D))

    def format1(self):
        return (self.TrainDate+'  車次：'+self.TrainNum+"\n"+self.prtTime+" ， "+str(self.TourTime.seconds//60)+"mins")
import datetime

def toTelegram(id, message):
    s = message.split(' ')
    if len(s) == 2:
        return handle_two_parts(id, s)
    elif len(s) == 4:
        return handle_four_parts(id, s)
    elif len(s) == 3:
        return handle_three_parts(id, s)
    else:
        return "Input Error"

def handle_two_parts(id, s):
    thsr_usr.setLatest(id, s[1] + " " + s[0])
    thsr_usr.setRecord(id, s[0] + " " + s[1])
    timeStr = OtoD(s[0], s[1])
    if timeStr != "":
        thsr_usr.setLasttime(id, format_time_str(timeStr))
        return timeStr
    else:
        return "Not Found"

def handle_four_parts(id, s):
    thsr_usr.setLatest(id, s[3] + " " + s[2])
    thsr_usr.setRecord(id, s[2] + " " + s[3])
    date = datetime.date(datetime.date.today().year, int(s[0][0:2]), int(s[0][2:4]))
    time = datetime.time(int(s[1]), 0, 0, 0)
    time = datetime.datetime.combine(date, time)
    timeStr = OtoD(s[2], s[3], str(date), time)
    if timeStr != "":
        thsr_usr.setLasttime(id, format_time_str(timeStr))
        return timeStr
    else:
        return "Not Found"

def handle_three_parts(id, s):
    if len(s[0]) == 4:
        return handle_three_parts_date(id, s)
    elif len(s[0]) <= 2:
        return handle_three_parts_time(id, s)
    else:
        return "Input Error"

def handle_three_parts_date(id, s):
    thsr_usr.setLatest(id, s[2] + " " + s[1])
    thsr_usr.setRecord(id, s[1] + " " + s[2])
    date = datetime.date(datetime.date.today().year, int(s[0][0:2]), int(s[0][2:4]))
    time = datetime.time(4, 0, 0, 0)
    time = datetime.datetime.combine(date, time)
    timeStr = OtoD(s[1], s[2], str(date), time)
    if timeStr != "":
        thsr_usr.setLasttime(id, format_time_str(timeStr))
        return timeStr
    else:
        return "Not Found"

def handle_three_parts_time(id, s):
    thsr_usr.setLatest(id, s[2] + " " + s[1])
    thsr_usr.setRecord(id, s[1] + " " + s[2])
    time = datetime.time(int(s[0]), 0, 0, 0)
    time = datetime.datetime.combine(datetime.date.today(), time)
    timeStr = OtoD(s[1], s[2], timeFlag=time)
    if timeStr != "":
        thsr_usr.setLasttime(id, format_time_str(timeStr))
        return timeStr
    else:
        return "Not Found"

def format_time_str(timeStr):
    return timeStr[timeStr.rfind("-")-2:timeStr.rfind("-")] + timeStr[timeStr.rfind("-")+1:timeStr.rfind("-")+3] + " " + timeStr[timeStr.rfind("→ ")-10:timeStr.rfind("→ ")-5]

def Train_later(id):
    s=(thsr_usr.getLasttime(id)+" "+thsr_usr.getRecord(id)).split(' ')
        
    date=datetime.date(datetime.date.today().year,int(s[0][0:2]),int(s[0][2:4]))
    time=datetime.time(int(s[1][0:2]),int(s[1][3:5]),0,0)
    time=datetime.datetime.combine(date,time)

    timeStr=(OtoD(s[2],s[3],str(date),time))
    if timeStr!="":
        thsr_usr.setLasttime(id,timeStr[timeStr.rfind("-")-2:timeStr.rfind("-")]+timeStr[timeStr.rfind("-")+1:timeStr.rfind("-")+3]+" "+timeStr[timeStr.rfind("→ ")-10:timeStr.rfind("→ ")-5])
        return timeStr
    else:
        return ("Not Found")

def stationInf(name,data):

    if(name[0]=='臺'):
        name="台"+name[1::]

    return data.get(name)



def OtoD(station1,station2,date=str(datetime.date.today()),timeFlag=datetime.datetime.fromtimestamp(time.time())):

    if date==str(datetime.date.today()) and timeFlag<=datetime.datetime.fromtimestamp(time.time()):
        timeFlag=datetime.datetime.fromtimestamp(time.time())
    global lst
    lst=auth.crawl("https://ptx.transportdata.tw/MOTC/v2/Rail/THSR/AvailableSeatStatus/Train/Leg/TrainDate/"+date+"?$format=JSON").json()["AvailableSeats"]
    with open("THSRID.json",encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)

    Oringin=stationInf(station1,data)
    Dest=stationInf(station2,data)

    res = auth.crawl("https://ptx.transportdata.tw/MOTC/v2/Rail/THSR/DailyTimetable/OD/"+
                    Oringin+"/to/"+Dest+"/"+date+
                    "?$format=JSON")

    Train=[]
    s=str("")

    for t in res.json():
        if Train.__len__()>=8:
            break
        if datetime.datetime.strptime(date+' '+ t['OriginStopTime']['DepartureTime'],"%Y-%m-%d %H:%M")>=timeFlag:
            Train.append(t)
    
    for i in range(0,8):
        if i>=Train.__len__():
            break

        inf=TrainInf(Train[i]["DailyTrainInfo"]["TrainNo"],Train[i]["TrainDate"],
                    Train[i]['OriginStopTime']['DepartureTime'],Train[i]['DestinationStopTime']['ArrivalTime'],
                    Oringin,Dest)
        
        if lst.__len__()!=0:
            s=s+inf.format()+'\n\n'
        else :
            s=s+inf.format1()+'\n\n'

    return s[0:s.__len__()-2]


    
if __name__ == '__main__':
    #print(OtoD("台南","台北"))
    thsr_usr.readData(730270828)
    #print(OtoD("台北","高雄"))
    print(toTelegram(730270828,"0502 17 高雄 台北"))
    thsr_usr.saveAll()
