
#
#   All slack function should be inheritance this class
#
#
#
class SlackBase(object):
    def __init__(self,general_info,id=None):
        self.token=general_info['token']
        if id == None :
            self.channel_id=general_info['channel_id']
        else:
            self.channel_id = id

    def change_channel(self,channel_id):
        self.channel_id = channel_id
