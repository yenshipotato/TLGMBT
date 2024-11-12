import datetime

class Attribute():
    def __init__(self, TrainNum, TrainDate, TimeO, TimeD):
        self.TrainNum=TrainNum
        self.TrainDate=TrainDate
        self.TourTime=datetime.datetime.strptime(TimeD,"%H:%M")-datetime.datetime.strptime(TimeO,"%H:%M")
        self.prtTime="<b>"+TimeO+"</b>"+" → "+"<b>"+TimeD+"</b>"
