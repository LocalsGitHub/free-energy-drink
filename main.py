# Made with <3 by Local#5353
try:
    import requests
except:
    if "not recognized as an internal or external command" in __import__("os").system("pip install requests"):
        print("PIP is not properly installed.")
        __import__("os")._exit(0)
        
from time import sleep
import threading
import json
import ctypes
import os

ctypes.windll.kernel32.SetConsoleTitleW("Power Burn Energy Drink Coupon Generator | Made by Local#5353")
i = 0

with open("config.json", "r") as config:
    parse = json.loads(config.read())
    fullName = parse['full_name']
    if not " " in fullName:
        print("Please make sure you entered a valid full name in the config.")
        os._exit(0)
    email = parse['email']
    if not "@" in email:
        print("Please make sure you entered a valid email")
        os._exit(0)
    phoneNumber = parse['phone_number']
    if not len(phoneNumber) == 10:
        print("Please make sure you entered a valid phone number.")
        os._exit(0)
    config.close()
    combined = f'''{{"phone":"+1{phoneNumber}","email":"{email}","fullName":"{fullName}"}}'''

def getCoupon(combined):
    global i
    global email
    session = requests.session()
    getToken = session.get("https://peekage.com/widgets/6161364c-b92a-4260-8b70-b1e964523cd1").cookies['widget_token']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0", 
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=utf-8", 
        "Authorization": f"Bearer {getToken}"
        }
    getID = session.post("https://api.peekage.com/api/v2.0/widgets/6161364c-b92a-4260-8b70-b1e964523cd1/answer", headers=headers, data='''{"results":[{"questionId":"a07614dd-becd-4e2b-8243-9bac5ffa433f","results":[{"questionAnswerId":"384f2859-f2c0-4913-81bf-ecd9a5421a64"}]},{"questionId":"aacdd4a2-fc38-4da4-b2e7-6b3c99d18324","results":[{"questionAnswerId":"b7932991-1182-4d37-ba5f-39a20bd19613"}]},{"questionId":"01db4efd-319f-44c5-8e2f-7cfea3908eac","results":[{"questionAnswerId":"dd0b3a77-1234-41fa-9a28-bda496f01cd7"}]},{"questionId":"e4850e44-43d1-432e-86dd-b5f60c557ee0","results":[{"questionAnswerId":"2cadc602-1ec8-40db-91a2-0137162213f8"}]}]})''').json()['claimId']
    sendInfo = session.post(f"https://api.peekage.com/api/v2.0/widgets/claims/{getID}/personal-information", headers=headers, data=combined)
    if email in sendInfo.text:
        pass
    elif "The user already claimed the widget." in sendInfo.text:
        print("User has already claimed coupon")
        os._exit(0)
    elif "The phone number is not valid." in sendInfo.text:
        print("Please enter a valid phone number.")
        os._exit(0)
    else:
        print(sendInfo.text)
        print(sendInfo.status_code)
    getCoupon = session.post(f"https://api.peekage.com/api/v2.0/widgets/claims/{getID}/package", headers=headers, data='{}')
    if "You will receive a confirmation email soon." in getCoupon.text:
        i += 1
        with open("coupons.txt", "a") as save:
            save.write(f"{getCoupon.json()['items'][0]['pdfDownloadUri']}\n")
            save.close()
        print(f"Successfully created coupon and saved to file! | Iteration: {i} | Made by Local#5353")
    else:
        print(getCoupon.text)
        print(getCoupon.status_code)
        
while i < 1000:
    threading.Thread(target=getCoupon, daemon=True, args=(combined,)).start()
    sleep(0.3)
