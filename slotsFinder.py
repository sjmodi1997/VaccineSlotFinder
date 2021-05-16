import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import date 
from tkinter import *  
  
from tkinter import messagebox  

#pincodes to check
pincodes = ["380001","380022","380008"]

#generates alert if you find the matching slot
def generateAlert(output):
    top = Tk()  
    top.geometry("100x100")       
    messagebox.showinfo("information",output)

def main():
    today = date.today().strftime('%d-%m-%Y')
    for pincode in pincodes:
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin?pincode=" + pincode + "&date=" + today
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content,'html.parser')

        ret = soup.prettify()
        #print(ret)
        try:
            my_map = json.loads(ret)
        except:
            print(ret)
            continue
        for center in my_map['centers']:
            #print(center)
            for session in center['sessions']:
                #print(session)
                if session['available_capacity_dose1'] > 0:
                    output = pincode + " :: " + center['name'] + " :: " + session['date'] + " => "+ (str(session['available_capacity']))
                    generateAlert(output)
        print("Done!!")
        sec = 15
        print("Sleeping for " + str(sec) + " secs")
        time.sleep(sec)

if __name__=="__main__":
    #generateAlert("test")
    sec = 60
    while(True):
        main()
        # print("Sleeping for " + str(sec) + " secs")
        # time.sleep(sec)

