import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/api')
import requests
import urllib,urllib.request
from datetime import datetime
from SlackBase import SlackBase

class PostMessages(SlackBase):
    POST_API="https://slack.com/api/chat.postMessage"

    def __init__(self,general_info,id=None):
        super().__init__(general_info,id)


    #
    #   post messages in channel1
    #   @params messages is text array. not messages array
    #
    def post_messages(self,messages):
        for msg in messages:
            self.post_message(msg)

    #
    #   post message in channel
    #
    def post_message(self,text,count=0):
        post_params = {
            "token"     :self.token,
            "channel"   :self.channel_id,
            "text"      :text
        }

        post_request = requests.get(self.POST_API,params=post_params)
        response = post_request.json()

        if not response['ok']:
            #If cannot post message,there's a possibility that many request  in short time
            #Use sleep and try again when that case
            #but if it continues 3 times,skip and go next message
            #TODO:Cehck error messages as failed request
            if count < 3:
                sleep(0.1)
                self.post_message(ts,count + 1)
            else:
                print ("Cannnot post message : " + text)
