from json import load

class Utils :
    def __init__(self) -> None:
        with open('settings.json', encoding='utf8') as f:
            self.data = load(f)
        self.resp_file = self.data["dialogs"]["responses"]
        self.superusers = self.data["userinfo"]["superusers"]
        self.reactions = self.data["autoresponses"]
        self.chat_chans_file = self.data["chatroom"]["channels"]
        with open(self.resp_file, encoding="utf8") as fresp :
            self.ping_response = fresp.read().splitlines()
        with open(self.chat_chans_file, encoding="utf8") as fchr :
            self.channels = fchr.read().splitlines()
        
    def refresh(self) :
        self.__init__()

    def is_su(self, user_id) :
        if user_id in self.superusers :
            return (True)
        else :
            return (False)
