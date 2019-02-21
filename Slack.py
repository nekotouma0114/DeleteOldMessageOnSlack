import requests
import urllib,urllib.request

class Slack:
    def __init__(self):
        self.delete_api_url="https://slack.com/api/chat.delete"
        self.history_api_url= "https://slack.com/api/channels.history"
        self.slack_token=""
        self.slack_channel=""
        workspace_url="alice-f-cat.slack.com"


    def debug(self):
        channel_parm ={
            "token"     : self.slack_token,
            "channel"   : self.slack_channel
        }
        history_request = requests.get(self.history_api_url,params=channel_parm)
        history_data = history_request.json()
        if history_data['ok']:
            history_message = history_data['messages']
            [print (msg['text']) for msg in history_message if "reactions" not in msg.keys()]
        else:
            print("cannot get history data")
