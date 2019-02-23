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
    # @return json() of history or None
    # TODO : can i get post from oldest?ß
    #
    def get_channel_history(self,count = 10000,latest= datetime.now()):
        # "count" should be set between 1 ando 1000
        if count < 1:
            # if count is under 1,dont get message in slack and return empty
            print ("get_channel_history \"count\" is " + count)
            return ""
        elif count > 100 :
            # max "count" parms is 1000 by use of slack
            remaining_count = count - 100 if count - 100 > 0 else 0
            count = 100
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
            if remaining_count == 0 or not history_data['has_more']:
                return history_data
            #get more remaining oldest_post
            #TODO : Maybe this cannnot get next latest post,
            #     :if oldest post and next latest post are some time
            else :
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
    #ß
    def delete_messages_in_channel(self,keep_count=10000,keep_date='1970/01/01'):
        pass

    #
    #   Delete 'ts' message
    #
    #
    def delete_message(self,ts):
        delete_params = {
            "token"     :self.token,
            "channel"   :self.channel_id,
            "ts"        :ts
        }
        history_request = requests.get(self.delete_api,params=delete_parm)
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
