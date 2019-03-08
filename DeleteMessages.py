import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/api')
import requests
import urllib,urllib.request
from datetime import datetime
from GetMessages import GetMessages

class DeleteMessages(GetMessages):
    DELETE_API="https://slack.com/api/chat.delete"

    def __init__(self,general_info,id=None):
        super().__init__(general_info,id)


    #
    #   delete messages in channel,
    #   but keep messages "count" post
    #   and newer than keep_date
    #   @param  keep_count : int
    #   @param  keep_date  : datetime
    #   @return delete_count
    #
    def delete_channel_messages(self,keep_count=10000,keep_date=datetime.fromisoformat('1970-01-01')):
        channel_messages = self.get_channel_messages()
        #oder by ts desc
        if channel_messages[0]['ts'] > channel_messages[-1]['ts']:
            channel_messages.reverse()

        # keep_date is tranced string to unixtime
        keep_date = datetime.timestamp(keep_date)
        messages_count = len(channel_messages)
        delete_count = 0

        #Delete message by date
        while float(channel_messages[delete_count]['ts']) < keep_date :
            self.delete_message(channel_messages[delete_count]['ts'])
            delete_count += 1
        #Delete message by count
        while messages_count - delete_count > keep_count :
            self.delete_message(channel_messages[delete_count]['ts'])
            delete_count += 1

        return delete_count


    #
    #   Delete 'ts' message
    #   sleep For continuous requests
    #
    def delete_message(self,ts,count = 0):
        delete_params = {
            "token"     :self.token,
            "channel"   :self.channel_id,
            "ts"        :ts
        }

        history_request = requests.get(self.DELETE_API,params=delete_params)
        response = history_request.json()

        if not response['ok']:
            #If cannot delete message,there's a possibility that many request  in short time
            #Use sleep and try again when that case
            #but if it continues 3 times,skip and go next message
            if count < 3:
                sleep(0.1)
                self.delete_message(ts,count + 1)
            else:
                print ("Cannnot delete message : " + ts)
