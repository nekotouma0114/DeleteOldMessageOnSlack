import requests
import urllib,urllib.request
from datetime import datetime

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
    # @return json() or None
    # TODO : can i get post from oldest ?
    #
    def get_channel_history(self,count = 100,latest= datetime.now()):
        # "count" should be set between 1 ando 1000
        if count < 1:
            # if count is under 1,dont get message in slack and return empty
            print ("get_channel_history \"count\" is " + count)
            return ""
        elif count > 1000 :
            # max "count" parms is 1000 by use of slack
            remaining_count = count - 1000
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
            if remaining_count == 0 :
                return history_data
            #get more remaining oldest_post
            #TODO : Maybe this cannnot get next latest post,
            #     :if oldest post and next latest post are some time
            else :
                oldest_post_time = datetime.formatimestamp(history_data['messages'][-1]['ts'] - 0.000001)
                return dict(history_date,get_channel_history(remaiing_count,oldest_post_time))
        #when return history_date has any problems
        else :
            print("Error type:"+ history_data['ok'] +"\n Process exit...")
            sys.exit()

    def delete_messages_in_channel(self):
        channel_messages = history

    def change_channel(self,channel_id):
        self.channel_id = channel_id

    #debug method
    def print_messages(self):
        history_data = self.get_channel_history()
        history_message = history_data['messages']
        [print (msg['text']) for msg in history_message if "reactions" not in msg.keys()]
