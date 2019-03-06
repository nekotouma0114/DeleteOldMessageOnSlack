import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/api')
import requests
import urllib,urllib.request
from datetime import datetime
import time

class Slack:

    def __init__(self,general_info,id=None):
        self.delete_api=general_info['delete_api']
        self.history_api= general_info['history_api']
        self.token=general_info['token']
        self.workspace=general_info['workspace']
        if id == None :
            self.channel_id=general_info['channel_id']
        else:
            self.channel_id = id

    #
    # get channel history,but dont check Errors in ['ok']
    # @params count : Get "count" messages From the latest post
    # @params latest: Latest time of post in datetime format
    # @return json() of history or None
    # TODO : can i get post from oldest?
    #
    def get_channel_history(self,count = 10000,latest= datetime.now()):
        # "count" should be set between 1 ando 1000
        if count < 1:
            # if count is under 1,dont get message in slack and return empty
            print ("get_channel_history \"count\" is " + count)
            return ""
        elif count > 1000 :
            # max "count" parms is 1000 by use of slack
            remaining_count = count - 1000 if count - 1000 > 0 else 0
            count = 1000
        else:
            remaining_count = 0

        #"latest" is need to trans datetime to unixtime
        channel_parm ={
            "token"     : self.token,
            "channel"   : self.channel_id,
            "count"     : count,
            "latest"    : latest.timestamp()
        }
        #get message on slack channel
        history_request = requests.get(self.history_api,params=channel_parm)
        history_data = history_request.json()
        #Error check
        if history_data['ok']:
            #get more remaining oldest_post
            #TODO : Maybe this cannnot get next latest post,
            #     :if oldest post and next latest post are some time
            if remaining_count > 0 and history_data['has_more']:
                oldest_post_time = datetime.fromtimestamp(float(history_data['messages'][-1]['ts']))
                history_data['messages'].extend(self.get_channel_history(remaining_count,oldest_post_time)['messages'])

            return history_data
        #when return history_date has any problems
        else :
            print("Error type:"+ history_data['ok'] +"\n Process exit...")
            sys.exit()

    #
    #   Get channel history only messages
    #
    def get_channel_messages(self):
        return self.get_channel_history()['messages']

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
    def delete_message(self,ts):
        delete_params = {
            "token"     :self.token,
            "channel"   :self.channel_id,
            "ts"        :ts
        }
        time.sleep(1)
        history_request = requests.get(self.delete_api,params=delete_params)
        response = history_request.json()

        if not response['ok']:
            print("message :" + datetime.fromimestamp(ts) + response['ok'])


    def change_channel(self,channel_id):
        self.channel_id = channel_id

    #debug method
    def print_messages(self):
        history_data = self.get_channel_history()
        history_message = history_data['messages']
        [print (msg['text']) for msg in history_message if "reactions" not in msg.keys()]
