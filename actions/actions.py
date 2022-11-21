# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from pickletools import int4
from typing import Any, Text, Dict, List

import rasa.core.tracker_store
from rasa.shared.core.trackers import DialogueStateTracker
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionSaveConversation(Action):

    def name(self) -> Text:
        return "action_save_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conversation = tracker.events
        senderid = tracker.sender_id
        latestmessage = tracker.latest_message
        latestactionname = tracker.latest_action_name

        print(f'\nconversation: {conversation} \n')
        print(f'senderid: {senderid} \n')
        print(f'latestmessage: {latestmessage} \n')
        print(f'latestactionname: {latestactionname} \n')

        
        import os
        import io
        import pandas as pd

        if not os.path.isfile('chats.csv'):
            with io.open('chats.csv','w',encoding='utf8') as file:
                file.write("user_id,timestamp,intent_name,confidence,user_input,action,bot_reply\n")
        chat_data=''
        for i in conversation:
            if i['event'] == 'user':
                print('\n\ntimestamp: "{}"'.format(i['timestamp']))
                timestamp = str(i['timestamp'])
                user_input = '"' +  i['text'] + '"'
                print(f'\n\nuser_input: {user_input}')
                user_id = '"' + str(senderid) + '"'
                confidence = str(i['parse_data']['intent']['confidence']) 
                chat_data += user_id + ',' + timestamp + ',' + i['parse_data']['intent']['name'] + ',' + confidence + ',' + user_input + ','
                #print(f'\n\nChatData: {chat_data}')
                #print('user: "{}"'.format(i['text']))
            elif i['event'] == 'bot':
                bot_reply = '"' + i['text'] + '"'
                print(f'\n\nbot_reply: {bot_reply}')
                #print('Bot: "{}"'.format(i['text']))
                #data = '"' + str(latestmessage) + '"'
                try:
                    chat_data += i['metadata']['utter_action'] + ',' + bot_reply + '\n'
                except KeyError:
                    pass
        else:
            with open('chats.csv','a',encoding='utf8') as file:
                file.write(chat_data)

        df_chats=pd.read_csv('chats.csv')
        sem_duplicatas = df_chats.drop_duplicates()
        sem_duplicatas.to_csv('chats2.csv',index=False,encoding='utf8')
        #sem_duplicatas.to_csv('chats.csv',index=False,mode='w+',encoding='utf8')
        return []