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
prev_stringtext = ""
def getapiredsun():
    response = requests.get(url, headers=head)
    if response.ok:
        json_response = response.json()

        if json_response is not None and 'results' in json_response:
            results = json_response['results']

            if results is not None and len(results) >= 2:
                if 'currentmap' in results[0] and 'gamemode' in results[0]['currentmap'] and 'name' in results[0]['currentmap']['gamemode'] and 'map' in results[0]['currentmap'] and 'name' in results[0]['currentmap']['map']:
                    current_gm_name = results[0]["currentmap"]["gamemode"]["name"]
                    current_name_map = results[0]["currentmap"]["map"]["name"]
                    current_filename = results[0]["currentmap"]["map"]["filename"]
                    current_filename = current_filename.replace("_", " ").replace(".", " ").replace("workshop/", "")
                else:
                    current_gm_name = "Not set"
                    current_name_map = "Not set"
                    current_filename = "Not set"

                if results[1] is not None and 'currentmap' in results[1] and results[1]['currentmap'] is not None and 'gamemode' in results[1]['currentmap'] and 'name' in results[1]['currentmap']['gamemode'] and 'map' in results[1]['currentmap'] and 'name' in results[1]['currentmap']['map']:
                    current_usa_gm_name = results[1]["currentmap"]["gamemode"]["name"]
                    current_usa_name_map = results[1]["currentmap"]["map"]["name"]
                    current_usa_filename = results[1]["currentmap"]["map"]["filename"]
                    current_usa_filename = current_usa_filename.replace("_", " ").replace(".", " ").replace("workshop/", "")
                else:
                    current_usa_gm_name = "Not set"
                    current_usa_name_map = "Not set"
                    current_usa_filename = "Not set"

                if 'nextmap' in results[0] and results[0]['nextmap'] is not None and 'gamemode' in results[0]['nextmap'] and 'name' in results[0]['nextmap']['gamemode'] and 'map' in results[0]['nextmap'] and 'name' in results[0]['nextmap']['map']:
                    next_gm_name = results[0]["nextmap"]["gamemode"]["name"]
                    next_map_name = results[0]["nextmap"]["map"]["name"]
                else:
                    next_gm_name = "Not set"
                    next_map_name = "Not set"

                if results[1] is not None and 'nextmap' in results[1] and results[1]['nextmap'] is not None and 'gamemode' in results[1]['nextmap'] and 'name' in results[1]['nextmap']['gamemode'] and 'map' in results[1]['nextmap'] and 'name' in results[1]['nextmap']['map']:
                    next_usa_gm_name = results[1]["nextmap"]["gamemode"]["name"]
                    next_usa_map_name = results[1]["nextmap"]["map"]["name"]
                else:
                    next_usa_gm_name = "Not set"
                    next_usa_map_name = "Not set"

                stringtext = "*RAIDEN*\n" + current_gm_name + "   " + current_name_map + "\n" + current_filename + "\n              - nextmap -        \n" + next_gm_name + "   " + next_map_name + "\n\n" + "*ARMSTRONG*\n" + current_usa_gm_name + "   " + current_usa_name_map + "\n" + current_usa_filename + "\n               - nextmap -       \n" + next_usa_gm_name + "   " + next_usa_map_name
                #stringtext = "*RAIDEN*\n" + current_gm_name + " - " + current_name_map + "\n" + "- - - - - - nextmap - - - - -\n" + next_gm_name + " - " + next_map_name + "\n\n*ARMSTRONG*\n" + current_usa_gm_name + " - " + current_usa_name_map + "\n- - - - - - nextmap - - - - - -\n" + next_usa_gm_name + " - " + next_usa_map_name
                return stringtext
            else:
                print("Results not available in the JSON response.")
        else:
            print("JSON response does not contain the necessary data.")
    else:
        print(response.content)

def send_to_telegram():
    global prev_stringtext
    stringtext = getapiredsun()
    if stringtext is None:
        stringtext = ""
    if stringtext != prev_stringtext:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + monitor_chatID + '&parse_mode=Markdown&text=' + stringtext
        #MONITORING MAPS
        #response = requests.get(send_text) #TRACKING MAPS
        #return response.json()
        prev_stringtext = stringtext
        if alert_me_1 in stringtext:
            alert_request = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_alert_chatID + '&parse_mode=Markdown&text=' + 'MITM!!!!!!'
            requests.get(alert_request)
        if alert_me_2 in stringtext:
            alert_request2 = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_alert_chatID + '&parse_mode=Markdown&text=' + 'feed and seed' #the last string is the text sent for notification
            requests.get(alert_request2)
        #if alert_me_2 in stringtext:
            #alert_request3 = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_alert_chatID + '&parse_mode=Markdown&text=' + 'feed and seed' #the last string is the text sent for notification
            #requests.get(alert_request3)
    else:
        response = ""

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


#the number indicates how often you execute the function in seconds, don't go under 60 seconds plz
schedule.every(100).seconds.do(send_to_telegram)
while True:
    schedule.run_pending()
    time.sleep(1)