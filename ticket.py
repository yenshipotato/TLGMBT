import auth
import requests

class Ticket:
    def __init__(self,dct):
        if dct==0:
            self.stdList=0
        else:
            self.stationList=list()
            self.stdList=list()
            self.busiList=list()
            lst=dct["StopStations"]
            for inf in lst:
                self.stationList.append(inf["StationID"])
                self.stdList.append(inf['StandardSeatStatus'])
                self.busiList.append(inf['BusinessSeatStatus'])
            self.stationList.append(lst[-1]["NextStationID"])
    
    def ini(self):
        stdList=list()
        busiList=list()
        for tct in self.stdList:
            if tct=="X":
                stdList.append(0)
            elif tct=="L":
                stdList.append(1)
            elif tct=="O":
                stdList.append(2)

        for tct in self.busiList:
            if tct=="X":
                busiList.append(0)
            elif tct=="L":
                busiList.append(1)
            elif tct=="O":
                busiList.append(2)
        self.stdList=stdList
        self.busiList=busiList

    def getStatus(self,O,D):
        status=str()
        if not self.stdList:
            print("ept")
            return " "

        self.result_std=min(self.stdList[self.stationList.index(O):self.stationList.index(D)])
        self.result_busi=min(self.busiList[self.stationList.index(O):self.stationList.index(D)])

        status=status+"標準車廂："
        if self.result_std == 0:
            status=status+"已無座位"
        elif self.result_std == 1 :
            status=status+"座位有限"
        elif self.result_std == 2:
            status=status+"尚有座位"
        
        status=status+"    商務車廂："
        if self.result_busi == 0:
            status=status+"已無座位"
        elif self.result_busi == 1 :
            status=status+"座位有限"
        elif self.result_busi == 2:
            status=status+"尚有座位"
        
        return status

def getTicket(dateStr,lst,trainNum='0'):

    #response = auth.crawl("https://ptx.transportdata.tw/MOTC/v2/Rail/THSR/AvailableSeatStatus/Train/Leg/TrainDate/"+dateStr+"?$format=JSON")
    #lst=response.json()["AvailableSeats"]
    if lst.__len__()==0:
        return 0
    for train in lst:
        if trainNum == train["TrainNo"]:
            return train

    return lst[1]
if __name__ == '__main__':
    TK1=Ticket(getTicket("2021-04-30","0121")) 
    TK1.ini()
    print(TK1.getStatus("1040","1070"))
    #print(getTicket("2021-04-30"))