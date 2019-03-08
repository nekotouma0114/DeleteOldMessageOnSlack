import configparser
import datetime
from DeleteMessages import DeleteMessages

def main():
    slack_params = read_config("./setting.ini")
    slack = DeleteMessages(slack_params)
    #delete post when 2weeks ago or 500 post
    delete_count = slack.delete_channel_messages(100,datetime.datetime.now() - datetime.timedelta(weeks=1))
    #TODO : post in slack if delete_count > 0
    print (delete_count)
    return delete_count

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
        print ("any keywork is not found")
        return null;

    return general_info

if __name__ == '__main__':
    main()
