import sys,os
import json
import telegram
import TRA
import THSR
import bus
import user_inf
import thsr_usr
import keep_alive
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from requests import request
from user_agent import generate_user_agent
from telegram import Update


P_mode=telegram.ParseMode.HTML

#create inlinekeyboard
inline_markup = telegram.InlineKeyboardMarkup([ 
    [telegram.InlineKeyboardButton('telegram', url = 'https://telegram.org')],
    [telegram.InlineKeyboardButton('google', url = 'https://google.com') , telegram.InlineKeyboardButton('facebook',url = 'https://facebook.com')]
    ])

#create ticketkeybord
ticket_markup = telegram.InlineKeyboardMarkup([ 
    [telegram.InlineKeyboardButton('訂票連結', url = 'https://irs.thsrc.com.tw/')],
    ])

#create replykeyboard
reply_markup = telegram.ReplyKeyboardMarkup([
    [telegram.KeyboardButton("TRA"),telegram.KeyboardButton("THSR")],
    [telegram.KeyboardButton("Metro"),telegram.KeyboardButton("BUS"),telegram.KeyboardButton("Transfer")]
    ],resize_keyboard=True,one_time_keyboard=False)
remove = telegram.ReplyKeyboardRemove(True)

#create TRAkeyboard
TRA_markup=telegram.ReplyKeyboardMarkup([
    [telegram.KeyboardButton("常用路線"),telegram.KeyboardButton("修改常用路線")],
    [telegram.KeyboardButton("起訖互換"),telegram.KeyboardButton("之後車輛")],
    #[telegram.KeyboardButton("對號車輛"),telegram.KeyboardButton("非對號車輛")],
    [telegram.KeyboardButton("退出TRA")]
],resize_keyboard=True,one_time_keyboard=False)

#create THSRkeyboard
THSR_markup=telegram.ReplyKeyboardMarkup([
    [telegram.KeyboardButton("網路訂票")],
    [telegram.KeyboardButton("回程查詢"),telegram.KeyboardButton("之後車輛")],
    #[telegram.KeyboardButton("對號車輛"),telegram.KeyboardButton("非對號車輛")],
    [telegram.KeyboardButton("退出THSR")]
],resize_keyboard=True,one_time_keyboard=False)

#create Metrokeyboard
Metro_markup=telegram.ReplyKeyboardMarkup([
    [telegram.KeyboardButton("臺北捷運"),telegram.KeyboardButton("桃園捷運")],
    [telegram.KeyboardButton("台中捷運"),telegram.KeyboardButton("高雄捷運")],
    #[telegram.KeyboardButton("對號車輛"),telegram.KeyboardButton("非對號車輛")],
    [telegram.KeyboardButton("退出Metro")]
],resize_keyboard=True,one_time_keyboard=False)

#Taipei

#create BUSkeyboard
BusZONE=["None","Taipei","NewTaipei","Taoyuan","Taichung","Tainan"]
Bus_markup=telegram.ReplyKeyboardMarkup([
    [telegram.KeyboardButton("臺北市"),telegram.KeyboardButton("新北市")],
    [telegram.KeyboardButton("桃園市"),telegram.KeyboardButton("台中市")],
    [telegram.KeyboardButton("臺南市"),telegram.KeyboardButton("退出Bus")]
],resize_keyboard=True,one_time_keyboard=False)



#create Cancelkeyboard
Cancel_markup=telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton("取消目前動作")]],resize_keyboard=True,one_time_keyboard=True)

#create SearchKeyboard
Search_markup=telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton("直接查詢")],[telegram.KeyboardButton("取消目前動作")]],resize_keyboard=True,one_time_keyboard=True)

#定義bot的行為
def act(update: Update, _: CallbackContext):
    user_inf.readData(update.message.from_user.id)
    
    
    if update.message.text == "TRA": 
        #update.message.reply_text("",reply_markup = remove)
        #update.message.reply_text("",reply_markup = TRA_markup)
        update.message.reply_text(getPTXTRA(),reply_markup = TRA_markup)

        user_inf.setStatus(update.message.from_user.id,1)

    elif update.message.text == "THSR":
        update.message.reply_text(getPTXTHSR(),reply_markup = THSR_markup)

        user_inf.setStatus(update.message.from_user.id,3)
    elif update.message.text == "Metro":
        update.message.reply_text(getMetro(),reply_markup = Metro_markup)

        user_inf.setStatus(update.message.from_user.id,4)
    elif update.message.text == "BUS":
        update.message.reply_text(getBus(),reply_markup = Bus_markup)        

        user_inf.setStatus(update.message.from_user.id,5)     
    
    else:
        if user_inf.getStatus(update.message.from_user.id)==0:#Base mode---------------------------------------------------
            if update.message.text == "inline":
                update.message.reply_text("inline : ",reply_markup = inline_markup)
            #elif update.message.text == "reply":
            #    update.message.reply_text("reply",reply_markup = reply_markup)
            elif update.message.text == "remove":
                update.message.reply_text("remove",reply_markup = remove)
            # elif update.message.text == "PTX":
            #     update.message.reply_text(getPTX())
            else:
                update.message.reply_text(update.message.text)
                print(update.message)
        
        elif user_inf.getStatus(update.message.from_user.id)==1:#TRA mode--------------------------------------------------

            if update.message.text == "退出TRA":
                #update.message.reply_text("",reply_markup = remove)
                update.message.reply_text("Exited",reply_markup = reply_markup)
                user_inf.setStatus(update.message.from_user.id,0)
            
            elif update.message.text == "起訖互換":#接續輸入時間-----------------
                
                if user_inf.getLatest(update.message.from_user.id)=="":
                    update.message.reply_text("未有查詢紀錄")
                else :
                    update.message.reply_text(TRA.toTelegram(update.message.from_user.id,user_inf.getLatest(update.message.from_user.id)),parse_mode=P_mode)
            
            elif update.message.text == "常用路線":#接續輸入時間-----------------
                if user_inf.getFavorite(update.message.from_user.id)=="":
                    update.message.reply_text("未設定常用路線\n請輸入起訖站",reply_markup=Cancel_markup)
                    user_inf.setStatus(update.message.from_user.id,2)
                else :
                    update.message.reply_text(user_inf.getFavorite(update.message.from_user.id))
                    update.message.reply_text(TRA.toTelegram(update.message.from_user.id,user_inf.getFavorite(update.message.from_user.id)),parse_mode=P_mode)
            
            elif update.message.text == "修改常用路線":
                if user_inf.getFavorite(update.message.from_user.id)=="":
                    update.message.reply_text("未設定常用路線\n請輸入起訖站",reply_markup=Cancel_markup)
                    user_inf.setStatus(update.message.from_user.id,2)
                else:
                    update.message.reply_text("目前常用路線：\n"+user_inf.getFavorite(update.message.from_user.id),reply_markup=Cancel_markup)
                    update.message.reply_text("請輸入新起訖站")
                    user_inf.setStatus(update.message.from_user.id,2)
            elif update.message.text == "之後車輛":
                if user_inf.getLasttime(update.message.from_user.id)=="" or user_inf.getRecord(update.message.from_user.id)=="":
                    update.message.reply_text("未有查詢紀錄")
                else :
                    update.message.reply_text(TRA.Train_later(update.message.from_user.id),parse_mode=P_mode)
                
            else :
                update.message.reply_text(TRA.toTelegram(update.message.from_user.id,update.message.text),parse_mode=P_mode)

        elif user_inf.getStatus(update.message.from_user.id)==2:#TRA常用路線MODE--------------------------------------------
            if update.message.text=="取消目前動作":
                update.message.reply_text("已取消",reply_markup=TRA_markup)
            else :
                user_inf.setFavorite(update.message.from_user.id,update.message.text)
                update.message.reply_text(TRA.toTelegram(update.message.from_user.id,update.message.text),reply_markup=TRA_markup)
            user_inf.setStatus(update.message.from_user.id,1)

        elif user_inf.getStatus(update.message.from_user.id)==3:#THSR MODE-------------------------------------------------
            thsr_usr.readData(update.message.from_user.id)
            if update.message.text == "網路訂票":   
                update.message.reply_text("前往訂票",reply_markup = ticket_markup,parse_mode=P_mode)
            
            elif update.message.text == "回程查詢":
                if thsr_usr.getRecord(update.message.from_user.id)=="":
                    update.message.reply_text("未有查詢紀錄")
                else :
                    update.message.reply_text("直接查詢或輸入時間如 : \n0101 09 或 0101 或 09",reply_markup = Search_markup,parse_mode=P_mode)
                    user_inf.setStatus(update.message.from_user.id,31)
            elif update.message.text == "之後車輛":
                if thsr_usr.getLasttime(update.message.from_user.id)=="" or thsr_usr.getRecord(update.message.from_user.id)=="":
                    update.message.reply_text("未有查詢紀錄")
                else :
                    update.message.reply_text(THSR.Train_later(update.message.from_user.id),parse_mode=P_mode)

            elif update.message.text == "退出THSR":
                update.message.reply_text("Exited",reply_markup = reply_markup,parse_mode=P_mode)
                user_inf.setStatus(update.message.from_user.id,0)
                   
            else:
                update.message.reply_text(THSR.toTelegram(update.message.from_user.id,update.message.text),parse_mode=P_mode)

            thsr_usr.wInFile(update.message.from_user.id)
        
        elif user_inf.getStatus(update.message.from_user.id)==31:#THSR BACK MODE--------------------------------------------
            thsr_usr.readData(update.message.from_user.id)
            if update.message.text == "直接查詢":
                update.message.reply_text(thsr_usr.getLatest(update.message.from_user.id))
                update.message.reply_text(THSR.toTelegram(update.message.from_user.id,thsr_usr.getLatest(update.message.from_user.id)),reply_markup = THSR_markup,parse_mode=P_mode)
           
            elif update.message.text == "取消目前動作":
                update.message.reply_text("已取消",reply_markup = THSR_markup)
            
            else:
                update.message.reply_text(thsr_usr.getLatest(update.message.from_user.id))
                update.message.reply_text(THSR.toTelegram(update.message.from_user.id,update.message.text+" "+thsr_usr.getLatest(update.message.from_user.id)),reply_markup = THSR_markup,parse_mode=P_mode)
            thsr_usr.wInFile(update.message.from_user.id)
            user_inf.setStatus(update.message.from_user.id,3)
       
        elif user_inf.getStatus(update.message.from_user.id)==4:#Metro MODE-------------------------------------------------
            if update.message.text == "臺北捷運":
                update.message.reply_photo("AgACAgUAAxkBAAIDFWB2tHGVC9G3P4pMynZFq3zZcqvXAAJ_qzEbhWG4VxmBOg7PgmmLM_K-c3QAAwEAAwIAA3kAAxPDAAIfBA")
            elif update.message.text == "桃園捷運":  
                update.message.reply_photo("AgACAgUAAxkBAAIDFGB2tHCaHJXuck20-4nxztPX3ISzAAJ-qzEbhWG4V49NwuAAAfX7euuiuG50AAMBAAMCAAN5AAP1AwQAAR8E")
            elif update.message.text == "台中捷運":
                update.message.reply_photo("AgACAgUAAxkBAAIDE2B2tG9zgogtAAGH6V9yaQ4s1YQyTQACfasxG4VhuFfNBpOfFZ0_7DuJw3N0AAMBAAMCAAN5AAM6xAACHwQ")  
            elif update.message.text == "高雄捷運":  
                update.message.reply_photo("AgACAgUAAxkBAAIDEmB2tG6eji271wUhX5U_UtiIxU98AAJ8qzEbhWG4Vy79Xy9Hh1VnHv5Kc3QAAwEAAwIAA3kAA3jRAAIfBA")
            elif update.message.text == "臺南捷運" or update.message.text == "台南捷運":    
                update.message.reply_text("不存在的")
            elif update.message.text == "退出Metro":
                update.message.reply_text("Exited",reply_markup = reply_markup)
                user_inf.setStatus(update.message.from_user.id,0)

        elif user_inf.getStatus(update.message.from_user.id)==5:#bus MODE---------------------------------------------------
            if update.message.text == "臺北市":
                update.message.reply_text("請輸入路線",reply_markup = Cancel_markup)

                user_inf.setStatus(update.message.from_user.id,51)
            elif update.message.text == "新北市":
                update.message.reply_text("請輸入路線",reply_markup = Cancel_markup)

                user_inf.setStatus(update.message.from_user.id,52)  
            elif update.message.text == "桃園市":
                update.message.reply_text("請輸入路線",reply_markup = Cancel_markup)

                user_inf.setStatus(update.message.from_user.id,53)  
            elif update.message.text == "臺中市":
                update.message.reply_text("請輸入路線",reply_markup = Cancel_markup)

                user_inf.setStatus(update.message.from_user.id,54)  
            elif update.message.text == "臺南市":
                update.message.reply_text("請輸入路線",reply_markup = Cancel_markup)

                user_inf.setStatus(update.message.from_user.id,55)  
            elif update.message.text == "退出Bus":
                update.message.reply_text("已退出",reply_markup = reply_markup)

                user_inf.setStatus(update.message.from_user.id,0)  
            else:
                update.message.reply_text("請以按鈕選擇地區")   

        elif user_inf.getStatus(update.message.from_user.id)//10==5:#bus zone MODE---------------------------------------------------

            if update.message.text == "取消目前動作":
                update.message.reply_text("已取消",reply_markup = Bus_markup)        

                user_inf.setStatus(update.message.from_user.id,5)  

            else :
                text=bus.toTelegram(BusZONE[user_inf.getStatus(update.message.from_user.id)%10],update.message.text)
                if type(text)==type("0"):
                    update.message.reply_text(text)
                else:
                    update.message.reply_text(text[0])
                    update.message.reply_text(text[1])


    #print(update.message)

    user_inf.wInFile(update.message.from_user.id)
    

def stk(update: Update, _: CallbackContext):
    print(update.message)
    pass
def getPTX():
    str1=""
    user_agent = generate_user_agent()
    response = request('get', 'https://ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/Taipei?$top=30&$format=JSON', headers= {"user-agent": user_agent})
    for i in range(0,30):
        str1=str1+response.json()[i]["StopName"]["Zh_tw"]+"\n"
    return str1
def getPTXTRA():
    return "In Mode TRA\n輸入起訖站 如:台北 板橋\n或\n日期+起訖站 如:\n0101 09 台北 板橋\n0101 台北 板橋\n09 台北 板橋"

def getPTXTHSR():
    return "In Mode THSR\n輸入起訖站 如:台北 板橋\n或\n日期+起訖站 如:\n0101 09 台北 板橋\n0101 台北 板橋\n09 台北 板橋"

def getMetro():
    return "選取區域以取得路網圖"

def getBus():
    return "目前僅提供以下縣市，以按鈕選取"

def start(update: Update, _: CallbackContext):
    update.message.reply_text("Hi! click the botton to enter the corresponding mode.",reply_markup = reply_markup)


def main():

    #load token
    
    my_secret = os.environ['token']
    #create bot
    updater = Updater(token=my_secret)
    
    #針對不同類別訊息執行指定函式
    updater.dispatcher.add_handler(CommandHandler("start",start)) 
    updater.dispatcher.add_handler(MessageHandler(Filters.text, act)) 
    updater.dispatcher.add_handler(MessageHandler(Filters.location,stk))
    #updater.dispatcher.add_handler(MessageHandler(Filters.sticker,stk))
    keep_alive.keep_alive()
    #用polling取得新訊息
    updater.start_polling()
    updater.idle()


if __name__=="__main__":
    main()