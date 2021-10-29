from json import load

class Utils :

    def __init__(self) -> None:
        with open('settings.json', encoding='utf8') as f:
            self.data = load(f)
        try :
            self.resp_file = self.data["dialogs"]["responses"]
        except Exception as e :
            print("Error : the path to the responses file is not valid or the json.settings is not configured correctly.\n\nException : " + str(e))
        try :
            self.superusers = self.data["userinfo"]["superusers"]
        except Exception as e :
            print("Error : the superusers property is not valid or the json.settings is not configured correctly.\n\nException : " + str(e))
        try :
            self.reactions = self.data["autoresponses"]
        except Exception as e :
            print("Error : the autoresponse property is not valid or the json.settings is not configured correctly.\n\nException : " + str(e))
        try :
            self.chatroom_channels = self.data["chatroom"]["channels"]
        except Exception as e :
            print("Error : the path to the chatroom_channels file is not valid or the json.settings is not configured correctly.\n\nException : " + str(e))
        try :
            with open(self.resp_file, encoding="utf8") as fresp :
                pr = fresp.read().splitlines()
            with open(self.chatroom_channels, encoding="utf8") as fchr :
                ch = fchr.read().splitlines()
        except Exception :
            print ("ERROR !\n\nthe path to one of the files is not correct !\n\nERROR!")
        self.ping_response = pr
        self.channels = ch

    def refresh(self) :
        self.__init__()

    def is_su(self, user_id) :
        if user_id in self.superusers :
            return (True)
        else :
            return (False)
