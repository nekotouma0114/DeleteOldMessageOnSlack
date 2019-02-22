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

    #
    # get channel history,but dont check Errors in ['ok']
    # @return json() or None
    #
    def get_channel_history(self):
        #setting params
        channel_parm ={
            "token"     : self.token,
            "channel"   : self.channel_id
        }
        #get message on slack channel
        history_request = requests.get(self.history_api,params=channel_parm)
        history_data = history_request.json()
        #Error check
        if history_data['ok']:
            return history_data
        else:
            print("Error type:"+ history_data['ok'] +"\n Process exit...")
            sys.exit()

    def delete_messages_in_channel(self):
        pass

    def change_channel(self,channel_id):
        self.channel_id = channel_id

    #debug method
    def print_messages(self):
        history_data = self.get_channel_history()
        history_message = history_data['messages']
        [print (msg['text']) for msg in history_message if "reactions" not in msg.keys()]
