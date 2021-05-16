import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import date 
from tkinter import *  
  
from tkinter import messagebox  

#----------------------------------------Update the following Configuration as per req----------------------------------------

#pincodes to check
pincodes = ["380001","380022","380008"]

#Set true if you are lookig for 1st Dose
lookForDose1 = True
#Set true if you are lookig for 2st Dose
lookForDose2 = False

#set true if you are looking for Covishield
lookForCoviShield = True
#set true if you are looking for Covaxin
lookForCovaxin = True

#-----------------------------------------------------------------------------------------------------------------------------

checkDoseString = ""
vaccineName = ""
sleepSec = 3

def init():
    global checkDoseString, vaccineName
    if lookForDose1 == True and lookForDose2 == True:
        checkDoseString = "available_capacity"
    elif lookForDose1 == True:
        checkDoseString = "available_capacity_dose1"
    else:
        checkDoseString = "available_capacity_dose2"
    
    if lookForCovaxin == True and lookForCoviShield == True:
        vaccineName = ""
    elif lookForCoviShield == True:
        vaccineName = "COVISHIELD"
    else:
        vaccineName = "COVAXIN"

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
                # print(session)
                # print(checkDoseString)
                # print(vaccineName)
                if session[checkDoseString] > 0:
                    if (not vaccineName) or (session['vaccine'] == vaccineName): 
                        output = pincode + " :: " + center['name'] + " :: " + session['vaccine'] + " :: " + session['date'] + " => "+ (str(session['available_capacity']))
                        generateAlert(output)
        print("No Req Slots found for pincode :: " + pincode)
        print("Sleeping for " + str(sleepSec) + " secs")
        time.sleep(sleepSec)

if __name__=="__main__":
    init()
    while(True):
        main()
