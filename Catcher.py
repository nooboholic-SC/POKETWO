import requests
import json
import time
import datetime

last_checked_time = {}  # Initialize last checked time for each channel
copied_message_sent = {}  # Initialize flag for each channel

token = "Change with discord token"
DM_channel_ID = ""  # to get ping when u get captcha
Naming_BOT_USER_ID = ""


def retrieve_messages(channel_id, user_id, user_checks, exit_user_id, exit_phrase, copy_user_id, copy_phrase):
    global last_checked_time, copied_message_sent  # Add the flag to the global variables

    try:
        current_time = int(time.time() * 1000)  # Get the current timestamp in milliseconds
        if channel_id not in last_checked_time or current_time - last_checked_time[channel_id] < 1000:  # Check if 1 second has passed since last check
            return  # If not, skip this iteration

        last_checked_time[channel_id] = current_time  # Update last checked time

        headers = {
            'authorization': token
        }

        params = {'limit': 2}  # Retrieve the last 100 messages

        r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers, params=params)
        print(f"Status Code: {r.status_code}")

        if r.status_code == 200:
            try:
                messages = r.json()  # Using .json() to directly parse the response
                if not messages:
                    print("No new messages found.")
                else:
                    print("New messages received.")

                for message in messages:
                    # Check if the message has an author and ID field
                    if 'author' in message and 'id' in message['author'] and 'timestamp' in message:
                        timestamp = message['timestamp']
                        dt = datetime.datetime.fromisoformat(timestamp)
                        timestamp_ms = int(dt.timestamp() * 1000)  # Convert timestamp to milliseconds
                        if timestamp_ms > last_checked_time[channel_id] - 30000:  # Check if the message was sent within the last 1 second
                            # Update the last checked time
                            last_checked_time[channel_id] = timestamp_ms

                            # Check if the message author ID matches the exit user ID and the message content contains the exit phrase
                            if message['author']['id'] == exit_user_id and exit_phrase.lower() in message['content'].lower():
                                send_message(DM_channel_ID, f"BAN Alert :exclamation: ") #captcha alert
                                print(f"Exiting due to message from {exit_user_id} containing '{exit_phrase}': {message['content']}\n")
                                exit()

                           # Check if the message author ID matches the copy user ID and the message content contains the copy phrase
                            
                            """                       
                            #Poke_name
                            if message['author']['id'] == copy_user_id and copy_phrase.lower() in message['content'].lower():
                                    copied_word = message['content']
                                    copied_word = copied_word.replace("#","")
                                    # Remove text between 【 and 】
                                    start_index = copied_word.find('【')
                                    end_index = copied_word.find('】')
                                    if start_index != -1 and end_index != -1:
                                        copied_word = copied_word[:start_index] + copied_word[end_index+1:]
                                        # Remove text between 【 and 】
                                    start_index = copied_word.find('<')
                                    end_index = copied_word.find('>')
                                    if start_index != -1 and end_index != -1:
                                        copied_word = copied_word[:start_index] + copied_word[end_index+1:]
                                        copied_word = copied_word.replace('<', '').replace('>', '').replace('【', '').replace('】', '').replace('\n', '').replace('\u200e', '').replace('(M)','').replace('(F)','')
                                        print({copied_word.strip()})
                                        send_message(channel_id, f"<@{Naming_BOT_USER_ID}> C {copied_word.strip()}")
                                        copied_message_sent[channel_id] = False  # Reset the flag to False after sending the message
                            #poke_name         
                            """  
                            #p2assist
                            if message['author']['id'] == copy_user_id and copy_phrase.lower() in message['content'].lower():
                                colon_index = message['content'].find(':')
                                if colon_index != -1:
                                    copied_word = message['content'][:colon_index].strip()         
                                    copied_word = copied_word.replace('null', 'null: type')
                                    print(f"Copying message from {copy_user_id} containing '{copy_phrase}': Copied word is '{copied_word}'\n")
                                    send_message(channel_id, f"<@{Naming_BOT_USER_ID}> C {copied_word.strip()}")
                                    copied_message_sent[channel_id] = False  # Reset the flag to False after sending the message
                            #p2assist
                            
                                          

            except json.JSONDecodeError as e:
                print("Failed to decode JSON:", e)
        else:
            print(f"Failed to retrieve messages. Status code: {r.status_code}")
            print(f"Response Text: {r.text}")
            print(f"Headers: {r.headers}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def send_message(channel_id, message):
    headers = {
        'authorization': token,
        'content-type': 'application/json'
    }

    payload = {
        'content': message
    }

    try:
        r = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers, json=payload)
        print(f"Status Code: {r.status_code}")
        if r.status_code != 200:
            print(f"Failed to send message. Status code: {r.status_code}")
            print(f"Response Text: {r.text}")
            print(f"Headers: {r.headers}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

channel_ids = ['Channel_1', 'Channel_2', 'Channel_3', 'Channel_4', 'Channel_n']  # Replace with the list of channel IDs
user_checks = {
    'Naming_BOT_USER_ID': ':',  #Pokename or Poke assist user ID;  Change accordingly
    '716390085896962058': 'please' #Poketwo user ID do not change
    # Replace with the second user ID and the corresponding search text
}

exit_user_id = '716390085896962058'  #PokeTwo user ID
exit_phrase = 'human'  # Replace with the phrase that triggers exit, DO NOT CHNAGE

copy_user_id = 'Naming_BOT_USER_ID'  #Pokename or Poke assist user ID; Change accordingly 
copy_phrase = ':'  # Replace with the phrase that triggers copying

for channel_id in channel_ids:
    last_checked_time[channel_id] = int(time.time() * 1000)  # Initialize last checked time for each channel
    copied_message_sent[channel_id] = False  # Initialize flag for each channel

# Continuously retrieve messages every second
while True:
    for channel_id in channel_ids:
        retrieve_messages(channel_id, None, user_checks, exit_user_id, exit_phrase, copy_user_id, copy_phrase)
    time.sleep(1)