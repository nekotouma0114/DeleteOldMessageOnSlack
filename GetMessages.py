import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/api')
import requests
import urllib,urllib.request
from datetime import datetime
from SlackBase import SlackBase

class GetMessages(SlackBase):
    HISTORY_API="https://slack.com/api/channels.history"

    def __init__(self,general_info,id=None):
        super().__init__(general_info,id)

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
        history_request = requests.get(self.HISTORY_API,params=channel_parm)
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
            print("Cannnot get messages \n Process exit...")
            sys.exit()

    #
    #   Get channel history only messages
    #
    def get_channel_messages(self):
        return self.get_channel_history()['messages']

    #debug method
    def print_messages(self):
        history_data = self.get_channel_history()
        history_message = history_data['messages']
        [print (msg['text']) for msg in history_message if "reactions" not in msg.keys()]
