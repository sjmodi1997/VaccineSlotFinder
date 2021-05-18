import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import date 
from tkinter import *  
from tkinter import messagebox  
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

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
sleepSec = 5

#method to get the random user agent to hit more different request
def getRandomUserAgent():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value] 
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    #user_agents = user_agent_rotator.get_user_agents()
    user_agent = user_agent_rotator.get_random_user_agent()
    return user_agent

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
        random_user_agent = getRandomUserAgent()
        headers = {"User-Agent": random_user_agent}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content,'html.parser')

        ret = soup.prettify()
        #print(ret)
        try:
            my_map = json.loads(ret)
        except:
            print(ret)
            print("Sleeping for " + str(sleepSec) + " secs")
            time.sleep(sleepSec)
            continue
        for center in my_map['centers']:
            for session in center['sessions']:
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
