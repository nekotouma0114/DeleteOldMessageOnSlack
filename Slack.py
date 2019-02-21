import requests
import urllib,urllib.request

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


    def channel_id(self):
        self._channel_id = id

    def print_messages(self):
        channel_parm ={
            "token"     : self.token,
            "channel"   : self.channel_id
        }
        history_request = requests.get(self.history_api,params=channel_parm)
        history_data = history_request.json()
        if history_data['ok']:
            history_message = history_data['messages']
            [print (msg['text']) for msg in history_message if "reactions" not in msg.keys()]
        else:
            print("cannot get history data")
