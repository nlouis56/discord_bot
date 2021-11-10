from json import load

class Utils :

    def __init__(self) -> None:
        with open('settings.json', encoding='utf8') as f:
            self.data = load(f)
        try :
            self.lang = self.data["language_packs"]
            self.resp_file = self.data["dialogs"]["responses"]
            self.superusers = self.data["userinfo"]["superusers"]
            self.reactions = self.data["autoresponses"]
            self.chatroom_channels = self.data["chatroom"]["channels"]
            self.en_servers_file = self.data["dialogs"]["en_servers"]
        except Exception as e :
            print("Error : the json.settings is not configured correctly (possibly an invalid path).\n\nException : " + str(e))
        try :
            with open(self.en_servers_file, encoding="utf8") as fensrv :
                en = fensrv.read().splitlines()
            with open(self.resp_file, encoding="utf8") as fresp :
                pr = fresp.read().splitlines()
            with open(self.chatroom_channels, encoding="utf8") as fchr :
                ch = fchr.read().splitlines()
        except Exception :
            print ("ERROR !\n\nthe path to one of the files is not correct !\n\nERROR!")
        self.en_servers = en
        self.ping_response = pr
        self.channels = ch

    def refresh(self) :
        self.__init__()

    def is_su(self, user_id) :
        if user_id in self.superusers :
            return (True)
        else :
            return (False)

    def server_lang(self, server_id) :
        for s in self.en_servers :
            if s == str(server_id) :
                return ("en")
        return ("fr")
