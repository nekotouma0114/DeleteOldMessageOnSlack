import configparser
import datetime
from DeleteMessages import DeleteMessages
from SlackFuntions import SlackFunctions
from PostMessages import PostMessages
from DynamoDB import DynamoDB

def main():
    slack_params = read_config("./setting.ini")
    dynamoDB = DynamoDB()
    channel_params = dynamoDB.scan("")
    deleteMessages = DeleteMessages(slack_params)

    for channel_param in channel_params:
        deleteMessages.change_channel(channel_param['channel_id'])
        #delete post each channel
        delete_messages = deleteMessages.delete_channel_messages(channel_param['max_messages'],datetime.datetime.now() - datetime.timedelta(days=int(channel_param['keep_days'])))
        #TODO : post in slack if delete_count > 0
        if len(delete_messages) > 0:
            repost_messages = SlackFunctions.get_has_reaction_messages(delete_messages)
            if len(repost_messages) > 0:
                repost_text = SlackFunctions.get_text_in_messages(repost_messages)
                post_messages = PostMessages(slack_params)
                post_messages.post_messages(repost_text)

#
#   TODO:confの形式検討
#   @params
#   @return
#
def read_config(file_path):
    ini_file = configparser.SafeConfigParser()
    ini_file.read(file_path)
    general_info = dict()
    try:
        #Workspaceの共通情報を読み込む
        general_info["token"] = ini_file.get("General","token")

        #channel情報を読み込む。複数channelに対応できる様になんとかする予定
        general_info["channel_id"] = ini_file.get("channel1","id")
    except:
        #exceptが発生したパラメータを判別できる様になんとかする予定
        print ("any keyword is not found")
        return null;

    return general_info

if __name__ == '__main__':
    main()
