import datetime
import schedule
import time
import requests
import json

head = {'Authorization': 'Token placeyourtokenHERE'}  #header
bot_token =  ''  # telegram bot token
monitor_chatID = ''  # telegram chat id used for monitoring
bot_alert_chatID = ''  # telegram chat id used for notification
alert_me_1 = 'Mann in the Machine' #word to get notified
alert_me_2 = 'ESS SEE PEE' #word n.2

url = 'https://redsun.tf/api/servers/?format=json'
     

def getapiredsun():
    response = requests.get(url, headers=head)
    if response.ok:
       json_response = response.json()
       current_gm_name = json_response["results"][0]["currentmap"]["gamemode"]["name"]
       current_name_map = json_response["results"][0]["currentmap"]["map"]["name"]
       current_usa_gm_name = json_response["results"][1]["currentmap"]["gamemode"]["name"]
       current_usa_name_map = json_response["results"][1]["currentmap"]["map"]["name"]
       if json_response['results'][0]['nextmap'] is not None and 'gamemode' in json_response['results'][0]['nextmap'] and 'name' in json_response['results'][0]['nextmap']['gamemode'] and 'map' in json_response['results'][0]['nextmap'] and 'name' in json_response['results'][0]['nextmap']['map']:
            next_gm_name = json_response["results"][0]["nextmap"]["gamemode"]["name"]
            next_map_name = json_response["results"][0]["nextmap"]["map"]["name"]
       else:
            next_gm_name = "Not set"
            next_map_name = "Not set"     
       #print("\n")
       if json_response['results'][1]['nextmap'] is not None and 'gamemode' in json_response['results'][1]['nextmap'] and 'name' in json_response['results'][1]['nextmap']['gamemode'] and 'map' in json_response['results'][1]['nextmap'] and 'name' in json_response['results'][1]['nextmap']['map']:
            next_usa_gm_name = json_response["results"][1]["nextmap"]["gamemode"]["name"]
            next_usa_map_name = json_response["results"][1]["nextmap"]["map"]["name"]
       else:
            next_usa_gm_name = "Not set"
            next_usa_map_name = "Not set"
       stringtext = "*RAIDEN*\n" + current_gm_name + " - " + current_name_map + "\n" + "- - - - - - nextmap - - - - -\n" + next_gm_name + " - " + next_map_name + "\n\n*ARMSTRONG*\n" + current_usa_gm_name + " - " + current_usa_name_map + "\n- - - - - - nextmap - - - - - -\n" + next_usa_gm_name + " - " + next_usa_map_name
       return stringtext

    else:
       print(response.content)

def send_to_telegram():
    stringtext = getapiredsun()
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + monitor_chatID + '&parse_mode=Markdown&text=' + stringtext
    response = requests.get(send_text) #TRACKING MAPS
    if alert_me_1 in stringtext:
        alert_request = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_alert_chatID + '&parse_mode=Markdown&text=' + 'MITM!!!!!!'
        requests.get(alert_request)
    if alert_me_2 in stringtext:
        alert_request2 = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_alert_chatID + '&parse_mode=Markdown&text=' + 'feed and seed'
        requests.get(alert_request2)
    
    return response.json()   

def checktime():
    timecurrent = datetime.datetime.now()
    displaytime = timecurrent.strftime("%H:%M")
    display_time = str(displaytime)
    #print(display_time)
    time2am = "02:10"
    time2amm = "02:18"
    if display_time > time2am and display_time < time2amm:
        print ("time to sleep")
        time.sleep(21000)
    else:
        #print("sneed")
        send_to_telegram()
       

#checktime()
send_to_telegram()



schedule.every(120).seconds.do(send_to_telegram)
while True:
    schedule.run_pending()
    time.sleep(1)